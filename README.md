# Integrated AI Synthesis — LLM-Directed Bike-Share Evidence Review

**AI Foundations (Edward Hickman) · Udacity · Project 7, revised**

An industry-focused evidence system integrating:

- **Project 2:** statistical interpretation, daily rank association and error groups.
- **Project 3:** the unchanged fixed forest, mean baseline and chronological partition.
- **Corrected Project 6:** a real MiniMax/LangGraph agent interpreting user instructions,
  choosing tools, receiving observations and deciding its next action.

The prior rule-only controller is superseded. This revision changes orchestration,
not the predictive model or the meaning of the historical benchmark.

## What is agentic and what is enforced

LangGraph alternates `llm_decision` and `read_only_tool`. The model selects tool
names and public justifications, reads aggregate observations and chooses whether
to continue or answer. Python does not choose a replacement action.

Seven tools: `load`, `quality`, `split`, `model`, `daily_association`,
`hourly_errors`, `demand_stress`. The final three have the same prediction
prerequisite but are independently selectable. An hourly-only request needs no
daily association or demand stress; a quality-only request needs no model.

Application guards enforce a registered dataset/intent, schema-valid calls,
one tool per turn, dependencies, no repeats, seven executions and sixteen model
turns. A quality finding prevents splitting/fitting regardless of model prose.
Batch calls execute nothing and return feedback. A tool failure returns an error
for the LLM to explain; no downstream tool is then permitted.

Persona, natural-language instructions, messages, observations, counters and
temporary frames are explicit in `integrated_system.py`. Each run starts fresh;
there is no persistent memory, data repair, bike dispatch or general planner.
Public action reasons are not hidden chain-of-thought.

## Submission contents

- `integrated_synthesis.ipynb`: executed source, real transcripts, live focused
  demonstration, scenario table and interpretation.
- `module_summary.pdf`: revised APA synthesis paper, all seven required sections.
- `module_summary.docx` / `.md`: editable supporting report versions.
- `integrated_system.py`, `evaluate_system.py`, `config.json`, bundled public data.
- `outputs/architecture_diagram.png`: implemented system diagram.
- `outputs/llm_runs`: current real evaluation, manifest, predictions and diagnostics.
- `outputs/development_attempts/first_live_suite`: retained initial behavior,
  including rejected attempts to continue after quality findings.
- `outputs/numerical_equivalence.json`: evidence of unchanged numerical outputs.
- `DEFENSE_UPDATE.md`: Project 7-only revised study/answer notes for Project 8.
- `PRIOR_PROJECT_MAP.md`, `VERIFICATION.md`, tests and actual environment freeze.

Everything needed for data/model computation is bundled. **New LLM runs require
your own valid MiniMax text-API access and may incur charges.** No key is included.
Viewing saved reports, HTML, notebooks or traces requires no account or key.

## Install and run offline checks

Prepared with Python **3.11.18 / Linux**:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip check
python -m pytest tests -q
```

Software tests deliberately inject scripted AIMessage objects. They verify guards,
observation feedback and state; they are not real LLM evaluations or a reliability
percentage. Separate numerical tests refit the same fixed forest.

## Execute real provider calls

Set `MINIMAX_API_KEY` securely in your environment/Secrets, never in a file.
`ChatOpenAI` is the LangChain compatibility client; requests go to MiniMax's
`https://api.minimax.io/v1`, not OpenAI. Model: **MiniMax-M3**.

```bash
python evaluate_system.py
python -m nbconvert --execute --to notebook --inplace integrated_synthesis.ipynb \
  --ExecutePreprocessor.timeout=600
python -m nbconvert --to html integrated_synthesis.ipynb --output-dir outputs
```

The evaluator overwrites `outputs/llm_runs`; save a copy first if preserving a run.
The notebook makes a separate narrow live request and reads the saved full suite.
Use a Python kernel belonging to the installed environment and inheriting the key.
Provider failures are recorded, never replaced with fabricated responses.
Future answers/tool sequences can vary; no exact-LLM-replay claim is made.

## Results and limitations

The full run uses 17,379 historical records, training on 13,891 and testing on
3,488 over 147 dates. Forest RMSE **104.65** versus baseline **232.56**;
MAE **72.57**, R-squared **.774754** (not classification accuracy).
Higher-actual-demand MAE **123.80**, signed error **+119.74**, n=1,413;
other MAE **37.69**, n=2,075. Threshold 258 is development-derived but membership
uses actual outcomes. Daily temperature/residual Spearman **−.0771** is descriptive.
This is the already-seen Project 3 benchmark, not independent validation.

Thirteen designed scenarios include full/focused reviews, six flawed fixtures,
allocation refusal, one pre-model structured rejection, a two-call budget and
an injected model-tool failure. Read actual statuses, not an “all scenarios passed”
claim. Initial model attempts to continue after quality findings are retained;
guards stopped them and explicit permission feedback was added.

Recorded rentals are not unmet demand; weather is observed, not forecast-time
input. No station allocation, demographic/geographic fairness, cost/emissions
benefit, causal inference, calibrated intervals or production readiness is shown.
Only instructions and aggregate observations go to MiniMax. Generated prose can
misinterpret results. Guards are not OS isolation, a global deadline, comprehensive
prompt-injection protection or scientific certification.

## Rebuild supporting artifacts

```bash
python scripts/build_diagram.py
python scripts/build_notebook.py
python scripts/build_report.py /path/to/course-APA-template.docx
```

Notebook rebuilding clears outputs: execute it afterward before calling it an
executed notebook. The report builder additionally needs the original course
APA template and LibreOffice; the supplied PDF/DOCX do not need those tools to open.
The template's styles, section setup and headers are preserved and audited.
Instructor/due date were not supplied and are omitted.

AI assistance in preparation, code, testing and drafting is disclosed. Edward
must understand, review and personalize the work under course policy. No classroom
submission, passed review, merged PR, live presentation or mentor booking is claimed.
