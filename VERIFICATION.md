# Verification of the revised Project 7 submission

## Actual execution, not invented results

- Python 3.11.18/Linux; installed the LLM dependencies into the existing environment.
- Created a separate Python 3.11 environment from the included actual pip freeze.
- **54 offline tests passed in each environment.** These include scripted-model
  guards and real deterministic numerical computation, not an LLM success rate.
- Executed all seven notebook code cells with the clean environment's explicit
  kernel; zero error outputs. The image cell was re-executed after improving
  diagram readability; saved live-provider outputs were not fabricated.
- The notebook's separate narrow demonstration made actual provider calls.
- PDF/DOCX opened; report is ten pages and the focused defense guide six pages.
  Rendered all pages and checked extracted text bounds; no out-of-page text.
- The report has **1,814 body words**, 1,909 with headings/references.
  Template styles, section geometry and headers are preserved by executable audit.

## Current real-provider suite

`outputs/llm_runs/run_manifest.json` fingerprints the implementation, evaluator
and configuration. Thirteen designed cases contain **44 real AI response turns**
across twelve live-response cases; the invalid structured request uses no model.

| Case | Recorded outcome |
|---|---|
| Full historical review | completed, seven tools, full coverage |
| Six flawed-input fixtures | held after two executions; no split or fitting |
| Quality-only request | completed focused task, two tools, partial pipeline |
| Hourly-only request | completed focused task, five tools; no other diagnostics |
| Natural-language allocation | refused without tools; no full review inferred |
| Invalid structured intent | blocked before model or tools |
| Two-tool full-review budget | budget exhausted; incomplete |
| Injected model-tool fault | failed after four attempts; no diagnostics |

“Completed” can mean a focused task ended with partial pipeline coverage.
No “13/13 means general reliability” or “hallucination-free” claim is made.
Future provider behavior and availability can differ.

## Numerical continuity

`outputs/numerical_equivalence.json` compares the revised output with previous
Project 7 commit `01a5d7916b57000faa6c44e55012dfa8cdd0ef81`.
The loading, quality, split and model method sources are unchanged. Prediction,
daily-diagnostic and hourly-diagnostic CSVs are byte-identical.
Forest RMSE 104.6461, baseline 232.5588, MAE 72.5738 and R-squared .774754
are preserved, as are the stress-group and daily rank-association statistics.
This is integration reproduction on a previously seen benchmark, not independent
generalization evidence or a new accuracy gain.

## Retained negative evidence

- `first_live_suite` records attempted continuation/repetition after quality flags.
  Application guards prevented downstream execution; permission feedback improved.
- `second_live_suite` records a generated sign reversal, hours/days confusion
  and an overclaim about baseline R-squared. Contracts now define signs and units.
- `outputs/explanation_audit.json` records remaining unsupported interpretations
  in current prose. Mechanism suggestions and “accurate” labels need evidence.
- Raw model messages are unchanged. Computed observations and human-corrected
  interpretation take precedence over fluent narrative.

No station-level fairness, real operational benefit, causal conclusion,
comprehensive injection resistance, OS isolation or production readiness is
established. No classroom submission, passing review, PR merge or defense was
performed. Saved artifacts open offline; new LLM execution requires secure
MiniMax access and may incur charges.
