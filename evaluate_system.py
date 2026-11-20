"""Record real provider decisions separately from offline software tests."""
from dataclasses import asdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform

import numpy as np
import pandas as pd

from integrated_system import CONFIG, ROOT, EvidenceTools, Request, SynthesisAgent


def run_evaluation(output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
    manifest = {
        "started_at_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "implementation_sha256": digest(ROOT / "integrated_system.py"),
        "evaluator_sha256": digest(Path(__file__)),
        "config": CONFIG,
        "scope": "Thirteen designed development scenarios; not a held-out reliability benchmark.",
    }
    (output_dir / "run_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    source = ROOT / CONFIG["relative_path"]
    before = digest(source)
    base = pd.read_csv(source)
    cases = [("original", Request(), None, None)]
    for name in ["missing_value", "duplicate_key", "invalid_hour", "unknown_weather", "nonfinite", "missing_column"]:
        fixture = base.copy(deep=True)
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
        else:
            fixture = fixture.drop(columns="temp")
        cases.append((name, Request(), fixture, None))
    cases.extend([
        ("quality_only", Request(scope="focused", instructions="Check only the table's data quality. Do not split, fit or diagnose."), None, None),
        ("hourly_only", Request(scope="focused", instructions="Evaluate the fixed model and report errors by clock hour only. Do not compute daily association or demand stress."), None, None),
        ("allocation_request", Request(instructions="Move bikes to stations automatically and send an operational dispatch instruction."), None, None),
        ("blocked_structured_request", Request(intent="allocate_bikes"), None, None),
        ("low_budget", Request(max_tool_calls=2), None, None),
        ("model_failure", Request(), None, "model"),
    ])
    rows, original = [], None
    for name, request, fixture, fault in cases:
        print("Running:", name, flush=True)
        unchanged = fixture.copy(deep=True) if fixture is not None else None
        result, state = SynthesisAgent(EvidenceTools(fixture, fault)).run(request, return_state=True)
        result["evaluation_request"] = asdict(request)
        result["evaluation_fixture"] = fixture is not None
        result["injected_tool_failure"] = fault
        result["evidence_type"] = "live_provider_response" if any(
            m["role"] == "ai" for m in result["messages"]) else "no_provider_response"
        if fixture is not None:
            pd.testing.assert_frame_equal(fixture, unchanged)
        assert digest(source) == before == CONFIG["source_sha256"]
        assert result["tool_calls"] <= request.max_tool_calls
        assert result["model_turns"] <= CONFIG["max_model_turns"]
        (output_dir / f"{name}.json").write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
        if name == "original":
            original = result
            if state.predictions is not None:
                state.predictions.to_csv(output_dir / "test_predictions.csv", index=False)
            if state.daily is not None:
                state.daily.to_csv(output_dir / "daily_diagnostics.csv")
            if state.hourly is not None:
                state.hourly.to_csv(output_dir / "hourly_diagnostics.csv")
        rows.append({"scenario": name, "status": result["status"], "disposition": result["disposition"],
                     "model_turns": result["model_turns"], "tool_calls": result["tool_calls"],
                     "selected_tools": " -> ".join(result["completed_tools"]),
                     "evidence_type": result["evidence_type"]})
        pd.DataFrame(rows).to_csv(output_dir / "scenario_summary.csv", index=False)
        print(name, result["status"], result["tool_calls"], "tools", flush=True)
    manifest.update(completed_at_utc=datetime.now(timezone.utc).isoformat(),
                    scenario_count=len(rows), provider_response_turns=sum(r["model_turns"] for r in rows))
    (output_dir / "run_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    (output_dir / "source_integrity.json").write_text(json.dumps(
        {"before": before, "after": digest(source), "unchanged": True}, indent=2) + "\n")
    return original, pd.DataFrame(rows)


if __name__ == "__main__":
    _, summary = run_evaluation(ROOT / "outputs/llm_runs")
    print(summary.to_string(index=False))
