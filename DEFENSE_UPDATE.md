# Project 7 — Revised Study Guide and Adversarial Answers

AI Foundations (Edward Hickman)

This replaces older Project 7 preparation that described a rule-only controller,
no LLM, five tools or ten scenarios. The Project 8 timed talk remains about
Project 7 only. Timing values below are rehearsal targets, not measured times.
Use the actual code and traces alongside this guide; suggested answers are not
claims that Edward independently wrote or personally reran every component.

## The central argument

The revised system helps a bike-share analyst inspect historical model evidence.
An LLM interprets the task, chooses appropriate local tools, reads observations
and decides what to do next. Enforced checks prevent fitting on flagged data.
The same fixed rental model feeds statistical error diagnostics. The improvement
is task-directed evidence selection and controlled execution, not higher model
accuracy. A human remains responsible for interpreting results.

## A plain-language opening

“A model can beat a simple average and still be a poor basis for moving bikes.
This project connects data checks, rental estimates and error analysis. A language
model chooses which evidence to request, but it cannot override the checks or
dispatch bikes. The historical model misses most during busier hours. The system
therefore supports human investigation, not automatic operational decisions.”

## What changed

The old program ran a fixed list of five steps. The revised LangGraph program
alternates an LLM node and a guarded execution node. The LLM chooses tool calls,
not Python keyword conditions. The former combined diagnostic is now three
independent tools. Current tools are load, quality, split, model, daily association,
hourly errors and demand stress. A full review can execute seven tools; a
quality-only request needs two, and an hourly-only analysis needs five.

Maximums are seven actual tool executions and sixteen model response turns.
Messages, observations, counters and temporary frames last one run. The persona
is a cautious retrospective evidence analyst. Public reasons explain requested
actions; they are not private chain-of-thought or proof of correct reasoning.

## Follow the computation

1. Instructions and persona reach MiniMax-M3 through LangChain's compatibility client.
2. The LLM selects a tool; Python checks its name, arguments, budget and prerequisites.
3. The selected local function returns aggregate observations in a ToolMessage.
4. The LLM reads the accumulated message history and selects another action or answers.
5. Quality findings forbid further executions. Model failure prevents diagnostics.
6. Actual predictions support selected diagnostics; tables and traces go to human review.

The graph's two-node loop is fixed, but the model's tool selection, diagnostic
order and stopping are not a predefined Python checklist. Dependencies are
necessary correctness constraints, not a replacement planner.

## The three-project integration

- Project 2 contributes group/rank analysis and cautious communication, not school data.
- Project 3 contributes the unchanged model, baseline, features and historical split.
- Corrected Project 6 contributes actual LLM agency, tool feedback, memory and guards,
  not penguin data. Its immutable source is recorded in PRIOR_PROJECT_MAP.md.

## Facts to retrieve without guessing

- Source: 17,379 hourly records, 17 columns; Capital Bikeshare, 2011–2012.
- Development: 13,891 rows; test: 3,488 rows, 147 dates, August 7–December 31, 2012.
- Forest: 150 trees, depth 14, minimum leaf 2, seed 20261119.
- Forest RMSE 104.6461; baseline 232.5588; forest MAE 72.5738 rentals/recorded hour.
- Test R-squared .774754 is not classification accuracy.
- Higher actual-demand threshold 258: n=1,413 hours, MAE 123.8008,
  mean actual-minus-predicted residual +119.7388.
- Other hours: n=2,075; MAE 37.6901.
- Daily temperature/mean-residual Spearman −.0771468 over 147 dates;
  descriptive only, no p-value or causal claim.
- Thirteen designed scenarios include one structured rejection before any LLM call.
- Numerical tables match the old Project 7 outputs; this is not independent validation.

Residual = actual minus predicted. **Positive means the estimate was too low;
negative means too high.** Mean signed error is not MAE and can hide cancellation.
The stress groups count hours, not days. A positive group mean does not establish
that every individual hour was underestimated.

## The 13:30 speaking route

1. Bounded problem and central claim — 0:45.
2. Industry context: completed rentals versus unmet demand — 1:15.
3. Architecture: LLM/tool/observation loop and mandatory guards — 1:45.
4. Integration of corrected Projects 2, 3 and 6 — 1:30.
5. Choices: fixed model, baseline, chronology, leakage exclusions, scoped tools — 1:45.
6. Model results and the previously seen benchmark — 1:30.
7. Focused requests, stress errors, quality holds, failure and actual LLM mistakes — 1:30.
8. Ethics: access bias, provider data flow, generated errors and human authority — 1:30.
9. Limits: observed weather, absent fairness data and deployment requirements — 1:15.
10. Professional relevance and conclusion — 0:45.

Leave 1:30 contingency inside the fifteen-minute limit. Practice with a real
timer; do not describe these targets as measured rehearsal durations.

## Adversarial answer guide

### 1. Is this just the same deterministic workflow with an LLM label?

No. The LLM emits actual tool calls from user instructions and observations.
Quality-only and hourly-only tasks take different paths, and the three diagnostics
are independently selectable. Python checks permissions; it does not substitute
a chosen next action. Show `_ask`, `_execute` and the current transcripts.

### 2. Isn't a fixed LangGraph graph itself deterministic?

The graph fixes the decision/execution protocol, not which tool the model requests.
A constrained agent can use a fixed loop and still make model-driven decisions.
This is bounded agency, not an unrestricted autonomous planner.

### 3. What happened when the model disobeyed?

Initial real runs tried to continue or repeat checks after quality findings.
Guards prevented further execution. Those raw traces are retained. Explicit hold
feedback was added, followed by another real evaluation. Do not claim instructions
alone make an LLM safe or that the final development cases prove universal obedience.

### 4. Did the generated explanation get everything right?

No. A retained second-suite narrative reversed hourly residual signs, confused
hours with days and overclaimed what negative baseline R-squared means. The
contracts and persona now state signs and units explicitly. Raw responses remain
unchanged. Read the explanation audit and current evidence; no prompt proves
future prose will be truthful. Human-corrected interpretation is essential.
The current audit also flags unsupported claims about accuracy tolerance and
the mechanism producing the errors. Describing a pattern is not identifying its cause.

### 5. What if the LLM requests two tools at once?

The application executes neither and returns feedback for a fresh model decision.
It does not quietly choose the first tool. Model-turn limits bound repeated
invalid requests. A rejected batch counts no executed tools.

### 6. Where is memory?

The graph holds the instruction/message history, observations, completed tools,
counters and temporary numerical frames for one run. A new run starts fresh.
There is no persistent autobiographical memory or supported resume-from-model feature.

### 7. Why use an LLM if a deterministic pipeline is simpler?

The revised contribution is a natural-language interface selecting relevant
evidence and stopping, not improving arithmetic. A fixed pipeline is simpler
for an invariant batch task. The LLM adds flexibility but also cost, latency,
provider dependence and explanation risk; this is an explicit tradeoff.

### 8. Can an eloquent answer bypass the quality gate?

No. The execution guard reads the stored quality result. A finding prevents
splitting, fitting and diagnostics regardless of model prose. This is a tested
application constraint, not comprehensive security against arbitrary code changes.

### 9. Does “completed” mean everything was checked?

No. A focused task can finish with partial pipeline coverage. Read status,
disposition, completed tools and observations together. Full configured coverage
still is not scientific validation or permission to act.

### 10. How do you know these are real model calls?

Current JSON transcripts include AI messages, requested calls, ToolMessages,
provider/model metadata and usage, with a manifest fingerprinting code/config.
The executed notebook also records a separate focused live run. Scripted unit
tests are separately labeled and cannot establish real provider behavior.

### 11. Did the revision improve accuracy?

No. The same recipe and data reproduce the previous outputs. Byte comparisons
check numerical continuity. The improvement is model-directed evidence selection,
control and interpretation; no new performance gain is claimed.

### 12. Was the test set untouched research data?

Not for this synthesis: Project 3 already examined it. Reusing it verifies
integration, not independent predictive generalization. A new deployment needs
an appropriate new evaluation, including data availability at decision time.

### 13. Why is this not an advance forecast?

The predictors use contemporaneously observed weather. A live forecast would
need weather information actually available at forecast time and evaluation
including its errors. Historical test scores do not establish that result.

### 14. Why does the baseline have negative R-squared?

R-squared compares squared error against the evaluation-set mean. A predictor
using the earlier training mean can do worse when periods differ. Negative values
are possible; they do not mean negative accuracy or universal uselessness.

### 15. Can the high-demand result route future requests?

No. The threshold comes from development data, but membership uses actual test
counts. This is a retrospective stress group. The outcome is unknown at decision
time, so this definition cannot choose a live route or allocation.

### 16. Does weak temperature correlation show weather does not matter?

No. It describes one aggregated monotonic relationship, with serial dependence
and seasonal confounding. It neither tests every weather effect nor supports
causal absence or a significance claim.

### 17. How did you prevent leakage?

Whole dates separate earlier development and later test data. Preprocessing fits
development inputs; target components `casual` and `registered`, the target and
identifiers are excluded. This does not eliminate serial dependence, the seen
benchmark limitation or unavailable future weather.

### 18. Is this a fairness audit?

No. Completed rentals reflect access as well as desired travel. The aggregate
table lacks station/demographic evidence. Error groups by hour or actual count
are not evidence of equitable service. Operational evaluation needs appropriate
local data and stakeholder review.

### 19. What leaves the machine?

User instructions and aggregate observations go to MiniMax. Raw hourly records
and local DataFrames are not tool-message payloads. That reduces exposure but
does not establish privacy or acceptable provider retention for future sensitive data.

### 20. What do passing tests establish?

Specified software behaviors: guards, feedback, fresh state and numerical
calculations. They do not prove model truthfulness, biological/scientific validity,
fairness, broad security or operational suitability. Designed live cases are
development evidence, not a general reliability rate.

### 21. What if the provider is unavailable?

The run reports model failure/incomplete evidence. It does not silently run a
Python checklist or substitute an old success. Saved evidence is viewable offline;
new real calls require valid provider access. The per-request timeout is not a
global runtime guarantee.

### 22. Who did the work?

Suggested honest wording: “Replit AI assisted with preparation, code, testing
and drafting. That is disclosed. I need to show that I understand the choices
and implementation; I do not claim to have independently written every line.”
Only claim personal review or reruns that you actually performed.

## Evidence retrieval and readiness

Open `integrated_system.py`, the current original/quality-only/hourly-only JSON,
one held fixture, the failure case and `outputs/explanation_audit.json`.
Trace one action into a ToolMessage and the next LLM response. Derive a two-point
MAE/RMSE example without reading. Explain the residual sign correctly.
Practice answering each challenge in thirty to sixty seconds with one artifact
and one limitation. Then record a timed Project 7-only rehearsal.

The report, notebook and replacement ZIP do not submit coursework, schedule the
mentor or complete the live defense. Follow the classroom's upload/Submit process
and use the resulting mentor scheduling instructions separately.
