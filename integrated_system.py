"""Offline bike-share evidence pipeline; no LLM, API, data repair or dispatch."""
from dataclasses import dataclass, field
import hashlib
import io
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr
from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score, root_mean_squared_error
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


ROOT = Path(__file__).resolve().parent
CONFIG = json.loads((ROOT / "config.json").read_text())
FEATURES = CONFIG["categorical"] + CONFIG["numeric"]
REQUIRED = FEATURES + ["instant", "dteday", "casual", "registered", "cnt"]


class ToolFailure(Exception):
    pass


@dataclass(frozen=True)
class Request:
    dataset_id: str = "bike_hourly_2011_2012"
    intent: str = "retrospective_review"
    max_tool_calls: int = 5


@dataclass
class State:
    completed: list = field(default_factory=list)
    observations: dict = field(default_factory=dict)
    trace: list = field(default_factory=list)
    calls: int = 0
    frame: pd.DataFrame | None = None
    development: pd.DataFrame | None = None
    test: pd.DataFrame | None = None
    predictions: pd.DataFrame | None = None
    daily: pd.DataFrame | None = None
    hourly: pd.DataFrame | None = None

    def log(self, action, reason, outcome):
        self.trace.append({"sequence": len(self.trace) + 1, "action": action,
                           "reason": reason, "outcome": outcome})


class EvidenceTools:
    def __init__(self, fixture=None, fail_tool=None):
        self.fixture = fixture
        self.fail_tool = fail_tool

    def dispatch(self, name, state):
        tools = {"load": self.load, "quality": self.quality, "split": self.split,
                 "model": self.model, "diagnose": self.diagnose}
        if name not in tools or name == self.fail_tool:
            raise ToolFailure("Unknown or deliberately failed evaluation tool")
        return tools[name](state)

    def load(self, state):
        if self.fixture is None:
            path = ROOT / CONFIG["relative_path"]
            if path.stat().st_size > CONFIG["max_bytes"]:
                raise ToolFailure("Registered source exceeds byte limit")
            raw = path.read_bytes()
            if hashlib.sha256(raw).hexdigest() != CONFIG["source_sha256"]:
                raise ToolFailure("Registered source fingerprint mismatch")
            frame = pd.read_csv(io.BytesIO(raw))
        else:
            frame = self.fixture.copy(deep=True)
        if not 0 < len(frame) <= CONFIG["max_rows"] or not 0 < len(frame.columns) <= 20:
            raise ToolFailure("Invalid input dimensions")
        if not frame.columns.is_unique:
            raise ToolFailure("Repeated column names")
        state.frame = frame
        return {"rows": len(frame), "columns": len(frame.columns),
                "source": "declared test fixture" if self.fixture is not None else "pinned historical CSV"}

    def quality(self, state):
        frame = state.frame
        missing = sorted(set(REQUIRED) - set(frame.columns))
        extra = len(set(frame.columns) - set(REQUIRED))
        issues = []
        if missing:
            issues.append("required_columns_missing")
        if extra:
            issues.append("unrecognized_columns")
        if missing or extra:
            return {"issues": issues, "missing_columns": missing, "extra_columns": extra}
        if frame.isna().any().any():
            issues.append("missing_values")
        if frame.duplicated(["dteday", "hr"]).any():
            issues.append("duplicate_timestamp")
        numeric = frame.drop(columns="dteday").apply(pd.to_numeric, errors="coerce")
        if not np.isfinite(numeric.to_numpy(dtype=float)).all():
            issues.append("nonnumeric_or_nonfinite")
        categories = [c for c, allowed in CONFIG["allowed_categories"].items()
                      if not frame[c].isin(allowed).all()]
        if categories:
            issues.append("unexpected_category")
        if not numeric[CONFIG["numeric"]].ge(0).all().all() or not numeric[CONFIG["numeric"]].le(1).all().all():
            issues.append("normalized_weather_out_of_range")
        counts = numeric[["casual", "registered", "cnt"]]
        if not counts.ge(0).all().all() or not counts.mod(1).eq(0).all().all():
            issues.append("invalid_rental_count")
        if not (numeric.casual + numeric.registered).eq(numeric.cnt).all():
            issues.append("count_components_disagree")
        dates = pd.to_datetime(frame.dteday, format="%Y-%m-%d", errors="coerce")
        if dates.isna().any():
            issues.append("invalid_date")
        else:
            if not dates.dt.year.sub(2011).eq(frame.yr).all() or not dates.dt.month.eq(frame.mnth).all():
                issues.append("calendar_inconsistency")
            if dates.nunique() < 10:
                issues.append("insufficient_dates")
        return {"issues": issues, "missing_cells": int(frame.isna().sum().sum()),
                "duplicate_keys": int(frame.duplicated(["dteday", "hr"]).sum()),
                "invalid_category_columns": categories,
                "scope": "Configured structural/range checks; no quality certification or automatic cleaning."}

    def split(self, state):
        data = state.frame.copy(deep=True)
        data["date"] = pd.to_datetime(data.dteday, format="%Y-%m-%d")
        data["timestamp"] = data.date + pd.to_timedelta(data.hr, unit="h")
        data = data.sort_values("timestamp").reset_index(drop=True)
        dates = data.date.drop_duplicates().to_numpy()
        cutoff = pd.Timestamp(dates[int(np.floor(.8 * len(dates)))])
        state.development = data.loc[data.date < cutoff].copy()
        state.test = data.loc[data.date >= cutoff].copy()
        return {"development_rows": len(state.development), "test_rows": len(state.test),
                "development_end": str(state.development.timestamp.max()),
                "test_start": str(state.test.timestamp.min()),
                "test_end": str(state.test.timestamp.max()),
                "test_dates": int(state.test.date.nunique()),
                "unrecorded_clock_hours": len(pd.date_range(data.timestamp.min(), data.timestamp.max(), freq="h")) - len(data)}

    def model(self, state):
        dev, test = state.development, state.test
        preprocess = ColumnTransformer([
            ("categorical", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CONFIG["categorical"]),
            ("numeric", "passthrough", CONFIG["numeric"])], remainder="drop")
        forest = Pipeline([("preprocess", preprocess),
                           ("model", RandomForestRegressor(random_state=CONFIG["seed"], **CONFIG["forest"]))])
        forest.fit(dev[FEATURES], dev.cnt)
        baseline = DummyRegressor(strategy="mean").fit(dev[FEATURES], dev.cnt)
        predicted = forest.predict(test[FEATURES])
        dummy = baseline.predict(test[FEATURES])
        p = test[["instant", "timestamp", "date", "hr", "temp"]].copy()
        p["actual"] = test.cnt.to_numpy()
        p["prediction"] = predicted
        p["baseline_prediction"] = dummy
        p["residual"] = p.actual - p.prediction
        p["absolute_error"] = p.residual.abs()
        state.predictions = p

        def metrics(values):
            return {"mae": float(mean_absolute_error(test.cnt, values)),
                    "rmse": float(root_mean_squared_error(test.cnt, values)),
                    "r2": float(r2_score(test.cnt, values))}

        return {"forest": metrics(predicted), "baseline": metrics(dummy),
                "train_demand_q75": float(dev.cnt.quantile(.75)),
                "features": FEATURES,
                "note": "Reuses Project 3 fixed recipe and previously seen benchmark; not independent validation."}

    def diagnose(self, state):
        p = state.predictions
        state.daily = p.groupby("date").agg(n=("actual", "size"), mean_temp=("temp", "mean"),
                                            mean_residual=("residual", "mean"),
                                            mae=("absolute_error", "mean"))
        state.hourly = p.groupby("hr").agg(n=("actual", "size"), mae=("absolute_error", "mean"),
                                          mean_residual=("residual", "mean"))
        rho = float(spearmanr(state.daily.mean_temp, state.daily.mean_residual).statistic)
        cutoff = state.observations["model"]["train_demand_q75"]
        high = p.loc[p.actual >= cutoff]
        lower = p.loc[p.actual < cutoff]
        return {"daily_n": len(state.daily), "daily_temp_residual_rho": rho,
                "inference": "Descriptive only; serial dependence and season/year confounding; no p-value or causal claim.",
                "higher_demand": {"n": len(high), "mae": float(high.absolute_error.mean()),
                                  "mean_residual": float(high.residual.mean())},
                "lower_demand": {"n": len(lower), "mae": float(lower.absolute_error.mean())},
                "group_definition": "Actual test count >= development count 75th percentile; retrospective stress analysis, not a deployable routing rule.",
                "worst_hour_by_mae": int(state.hourly.mae.idxmax()),
                "recommendation": "Human review only; no allocation, staffing, causal or fairness approval."}


class SynthesisAgent:
    def __init__(self, tools=None):
        self.tools = tools if tools is not None else EvidenceTools()

    def run(self, request, return_state=False):
        state = State()

        def finish(status, reason):
            state.log("finish", reason, status)
            result = {"status": status, "reason": reason,
                      "disposition": "human_review" if status in ["completed", "held"] else "incomplete_review",
                      "tool_calls": state.calls, "completed_tools": state.completed,
                      "observations": state.observations, "trace": state.trace,
                      "data_modified": False, "automatic_allocation": False}
            return (result, state) if return_state else result

        if not isinstance(request, Request):
            return finish("blocked", "Structured requests only.")
        if request.dataset_id != CONFIG["dataset_id"] or request.intent != "retrospective_review":
            return finish("blocked", "Only registered historical review is permitted.")
        if type(request.max_tool_calls) is not int or not 1 <= request.max_tool_calls <= CONFIG["max_tool_calls"]:
            return finish("blocked", "Budget must be an integer between one and five.")
        reasons = {
            "load": "Load the registered read-only source.",
            "quality": "Observe required schema, completeness, keys and configured ranges.",
            "split": "Quality gate has no configured findings; isolate later dates.",
            "model": "Fit fixed Project 3 recipe on development only; score the later period.",
            "diagnose": "Use model residuals for descriptive Project 2-style human interpretation.",
        }
        for name, reason in reasons.items():
            if name == "split" and state.observations["quality"]["issues"]:
                return finish("held", "Quality findings block splitting, model fitting and diagnosis.")
            if state.calls >= request.max_tool_calls:
                return finish("budget_exhausted", "Next required tool would exceed the call budget.")
            state.calls += 1
            state.log(name, reason, "requested")
            try:
                observation = self.tools.dispatch(name, state)
            except (ToolFailure, OSError, ValueError, TypeError, UnicodeError):
                state.log(name, "Tool failed; remaining stages were not performed.", "error")
                return finish("failed", "No retry and no approval inferred from partial evidence.")
            state.observations[name] = observation
            state.completed.append(name)
            state.log(name, "Aggregate observation stored in fresh run-local memory.", "observed")
        return finish("completed", "All five stages completed; operational decisions remain with a human.")


def evaluate(output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    source = ROOT / CONFIG["relative_path"]
    before = hashlib.sha256(source.read_bytes()).hexdigest()
    result, state = SynthesisAgent().run(Request(), return_state=True)
    if result["status"] != "completed":
        raise ToolFailure("Original-data workflow did not complete")
    state.predictions.to_csv(output_dir / "test_predictions.csv", index=False)
    state.daily.to_csv(output_dir / "daily_diagnostics.csv")
    state.hourly.to_csv(output_dir / "hourly_diagnostics.csv")
    results = {"original": result}
    base = pd.read_csv(source)
    for name in ["missing_value", "duplicate_key", "invalid_hour", "unknown_weather",
                 "nonfinite", "missing_column", "allocation_request", "low_budget", "model_failure"]:
        fixture = base.copy(deep=True)
        request = Request()
        fail_tool = None
        expected = "held"
        if name == "missing_value":
            fixture.loc[0, "temp"] = np.nan
        elif name == "duplicate_key":
            fixture = pd.concat([fixture, fixture.iloc[[0]]], ignore_index=True)
        elif name == "invalid_hour":
            fixture.loc[0, "hr"] = 24
        elif name == "unknown_weather":
            fixture.loc[0, "weathersit"] = 99
        elif name == "nonfinite":
            fixture.loc[0, "windspeed"] = np.inf
        elif name == "missing_column":
            fixture = fixture.drop(columns="temp")
        elif name == "allocation_request":
            request, expected = Request(intent="allocate_bikes"), "blocked"
        elif name == "low_budget":
            request, expected = Request(max_tool_calls=2), "budget_exhausted"
        elif name == "model_failure":
            fail_tool, expected = "model", "failed"
        unchanged = fixture.copy(deep=True)
        results[name] = SynthesisAgent(EvidenceTools(fixture, fail_tool)).run(request)
        assert results[name]["status"] == expected
        assert "model" not in results[name]["completed_tools"]
        pd.testing.assert_frame_equal(fixture, unchanged)
    after = hashlib.sha256(source.read_bytes()).hexdigest()
    assert before == after == CONFIG["source_sha256"]
    for name, item in results.items():
        (output_dir / (name + ".json")).write_text(json.dumps(item, indent=2, allow_nan=False) + "\n")
    table = pd.DataFrame([{"scenario": name, "status": r["status"], "tool_calls": r["tool_calls"],
                           "completed_stages": ",".join(r["completed_tools"])}
                          for name, r in results.items()])
    table.to_csv(output_dir / "scenario_summary.csv", index=False)
    (output_dir / "source_integrity.json").write_text(json.dumps(
        {"before": before, "after": after, "unchanged": True}, indent=2) + "\n")
    return result, table


if __name__ == "__main__":
    original, scenarios = evaluate(ROOT / "outputs")
    print(json.dumps(original["observations"], indent=2))
    print(scenarios.to_string(index=False))
