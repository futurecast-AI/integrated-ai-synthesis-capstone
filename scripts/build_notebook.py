from pathlib import Path
from textwrap import dedent
import nbformat as nbf

ROOT = Path(__file__).resolve().parents[1]
cells = []


def md(text):
    cells.append(nbf.v4.new_markdown_cell(dedent(text).strip()))


def code(text):
    cells.append(nbf.v4.new_code_cell(dedent(text).strip()))


md("""
# LLM-directed bike-share evidence review
**AI Foundations (Edward Hickman) · Udacity · Project 7, revised**

Urban bike-share analysts need inspectable evidence, not automatic dispatch.
This revision integrates Project 2's statistical reasoning, Project 3's unchanged
fixed rental model, and **corrected Project 6's real MiniMax/LangGraph agent**.
The prior rule-only agentic contribution is superseded, not relabeled.

AI assisted with preparation, code, tests and drafting. Edward must review,
understand and personalize the work under course policy. No claim of independent
authorship, classroom acceptance, production deployment or completed defense.
""")
code("""
from pathlib import Path
import hashlib, inspect, json, platform
from importlib.metadata import version
import pandas as pd
from IPython.display import Code, Image, display
import integrated_system
from integrated_system import ROOT, CONFIG, Request, SynthesisAgent

OUT = Path("outputs")
SAVED = OUT / "llm_runs"
versions = {"python": platform.python_version(),
            **{p: version(p) for p in ["numpy", "pandas", "scipy", "scikit-learn",
                                      "langgraph", "langchain-openai", "langchain-core"]}}
(OUT / "runtime_versions.json").write_text(json.dumps(versions, indent=2) + "\\n")
display(versions)
assert hashlib.sha256(Path("data/hour.csv").read_bytes()).hexdigest() == CONFIG["source_sha256"]
print("Pinned public source: 17,379 records, 17 columns; no raw rows sent to the provider.")
""")
md("""
## 1. Architecture and responsibility
The LLM interprets instructions and selects a tool or final response after each
observation. LangGraph alternates decision and execution nodes. There is no
Python-selected checklist. Dependencies enforce valid computation; after modeling,
daily association, hourly errors and demand stress are independently selectable.

Python—not model persuasion—enforces registered data, read-only tools, quality
holds, seven executions, sixteen model turns, one tool per turn and no repeats.
Memory contains messages, observations, counters and temporary data for one run.
Raw source records stay local; instructions and aggregate tool results go to MiniMax.
Public reasons are brief justifications, not hidden chain-of-thought.
""")
code("""
display(Image(filename=str(OUT / "architecture_diagram.png")))
display(Code(inspect.getsource(integrated_system), language="python"))
""")
md("""
## 2. Saved real-provider suite: provenance before interpretation
These are genuine saved provider responses, not scripted test doubles.
The evaluator records thirteen designed development cases, including one invalid
structured request blocked without any provider call. They are not a held-out
reliability benchmark. Earlier live attempts are retained separately.
""")
code("""
manifest = json.loads((SAVED / "run_manifest.json").read_text())
assert manifest["implementation_sha256"] == hashlib.sha256(Path("integrated_system.py").read_bytes()).hexdigest()
assert manifest["evaluator_sha256"] == hashlib.sha256(Path("evaluate_system.py").read_bytes()).hexdigest()
result = json.loads((SAVED / "original.json").read_text())
scenarios = pd.read_csv(SAVED / "scenario_summary.csv")
display(manifest)
display(scenarios[["scenario", "status", "model_turns", "tool_calls"]])
print("Actual full-run tool sequence:", " → ".join(result["completed_tools"]))
assert result["status"] == "completed" and result["full_pipeline_coverage"]
""")
md("""
## 3. Inspect the reasoning/action/observation loop
Every requested action below came from an actual AIMessage. Every tool observation
was returned in a ToolMessage before the next LLM decision. Final prose is separate
from authoritative computed observations. This does not expose private model reasoning.
Read `outputs/explanation_audit.json`: current prose still contains unsupported
interpretations, including an untested error mechanism and an accuracy judgment
without an operational tolerance. The stored LLM narrative is evidence to critique,
not a model answer to memorize.
""")
code("""
for message in result["messages"]:
    if message["role"] == "ai":
        print("\\nMODEL:", message["content"])
        for call in message["tool_calls"]:
            print("SELECTED:", call["name"], "| PUBLIC REASON:", call["args"]["reason"])
    elif message["role"] == "tool":
        print("OBSERVATION:", message["name"], message["content"])
display(pd.DataFrame(result["trace"]))
""")
md("""
## 4. A separate live focused request — this cell requires the API secret
The following cell makes a **new real MiniMax call sequence**. It is not replaying
the saved suite. Supply `MINIMAX_API_KEY` through environment/Secrets; never paste
it into the notebook. Viewing the already executed notebook needs no key.
Future provider wording and decisions may differ.
""")
code("""
live = SynthesisAgent().run(Request(scope="focused",
    instructions="Check only data quality. Do not split, fit a model or run diagnostics. Explain the limits."))
(OUT / "notebook_live_demo.json").write_text(json.dumps(live, indent=2, allow_nan=False) + "\\n")
display({k: live[k] for k in ["status", "disposition", "tool_calls", "model_turns", "completed_tools"]})
print(live["answer"])
assert live["status"] == "completed"
assert live["completed_tools"] == ["load", "quality"]
""")
md("""
## 5. Requests and observations change behavior
Quality-only requests stop after data checks. Hourly-only analysis requires a
model but omits daily association and demand stress. Six flawed-input fixtures
cannot reach fitting. Natural-language allocation is refused; a structured
invalid intent is separately blocked before the model. Budget and model-tool
failure cases remain incomplete, never borrowing an old success.

Initial real runs attempted to bypass or repeat checks after quality findings.
Guards prevented execution; explicit permission feedback was then added.
The initial suite is retained in `outputs/development_attempts/first_live_suite`.
A second suite exposed a sign reversal and hours/days confusion in generated prose;
its raw responses remain in `second_live_suite`. Contracts now define signs and
units explicitly. Positive actual-minus-predicted error means underestimation.
These are observed limitations and development changes, not a universal truthfulness claim.
""")
code("""
for name in ["quality_only", "hourly_only", "missing_value", "allocation_request",
             "blocked_structured_request", "low_budget", "model_failure"]:
    case = json.loads((SAVED / f"{name}.json").read_text())
    print("\\n", name, case["status"], case["disposition"])
    print("Selected:", case["completed_tools"], "| Model turns:", case["model_turns"])
    print("Answer:", case["answer"])
""")
md("""
## 6. Same mathematics, newly controlled execution
Loading, quality, chronological splitting and the model method are unchanged.
The former combined diagnosis is exposed as three independently selectable tools.
The forest retains 150 trees, depth 14, minimum leaf 2 and seed 20261119.
Target-derived counts and identifiers remain excluded. Preprocessing fits only
earlier records; whole dates separate 13,891 development and 3,488 test records.

This is the already-seen Project 3 historical benchmark, not independent new
research validation. Observed weather prevents calling it an advance forecast.
The 165 missing clock hours are not invented as zero demand.
""")
code("""
observed = result["observations"]
display(pd.DataFrame({name: observed["model"][name] for name in ["forest", "baseline"]}).T)
p = pd.read_csv(SAVED / "test_predictions.csv")
daily = pd.read_csv(SAVED / "daily_diagnostics.csv")
hourly = pd.read_csv(SAVED / "hourly_diagnostics.csv")
display(observed["demand_stress"])
display(observed["daily_association"])
display(hourly)
assert len(p) == 3488 and len(daily) == 147
display(json.loads((OUT / "numerical_equivalence.json").read_text()))
""")
md("""
## 7. Plain-language explanation and responsible use
The system checks historical rental records, builds an estimate only after the
checks allow it, and shows where estimates miss. Average absolute error is about
73 rentals per recorded hour; in busier actual hours it is about 124, usually
because estimates are too low. Completed rentals cannot reveal everyone who
wanted a bike but could not obtain one.

The demand threshold is 258 from development data, but group membership uses
actual test outcomes. This is retrospective stress analysis, not a future routing
rule. Daily temperature/mean-residual Spearman is −0.0771 over 147 dates:
descriptive only, with no p-value or causal claim. R-squared .774754 is not
77.5% classification accuracy. No station/demographic fairness audit, cost saving,
emissions benefit, production readiness or permission to move bikes is established.

The LLM can misunderstand evidence or disobey instructions. Computed tables,
enforced permissions and human review remain necessary. No persistent memory,
OS isolation, global deadline or broad injection-resistance claim is made.
""")
md("""
## References and defense preparation
Breiman (2001), *Random forests*: https://doi.org/10.1023/A:1010933404324

Fanaee-T (2013), *Bike Sharing*: https://doi.org/10.24432/C5W894

Fanaee-T & Gama (2014): https://doi.org/10.1007/s13748-013-0040-3

LangChain, *Workflows and agents*:
https://docs.langchain.com/oss/python/langgraph/workflows-agents

NIST (2023), *AI RMF 1.0*: https://doi.org/10.6028/NIST.AI.100-1

SciPy, *spearmanr*: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.spearmanr.html

The formal Project 8 talk remains about Project 7 only. Use the included revised
defense notes; old statements that this system has no LLM or only five tools
are obsolete. Upload/submission and mentor scheduling remain separate user actions.
""")
notebook = nbf.v4.new_notebook(cells=cells)
notebook.metadata.kernelspec = {"display_name": "Python 3", "language": "python", "name": "python3"}
notebook.metadata.language_info = {"name": "python", "version": "3.11.18"}
nbf.write(notebook, ROOT / "integrated_synthesis.ipynb")
