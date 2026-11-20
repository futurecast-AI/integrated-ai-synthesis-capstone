# Integration plan, written before the new pipeline was executed

Industry: urban bike-share operations / sustainable transportation.
Problem: an analyst needs trustworthy retrospective demand estimates and
interpretable evidence about their errors before considering operational use.
Not a live forecast, station allocation tool, causal analysis or deployment.

## Three explicit contributions

1. **Project 3: Machine Learning Foundations.** Refit the same fixed random
   forest, features, baseline and chronological 80/20-date split. Reuse the
   model recipe rather than introduce a new algorithm or hyperparameter search.
2. **Project 2: Statistical Analysis.** Transfer descriptive group summaries,
   Spearman rank association and disciplined noncausal/plain-language
   interpretation. Compute a new descriptive association between daily mean
   temperature and daily mean signed model error, without an independence-based
   p-value. Do not transfer the educational study's data, effect size or p-value.
3. **Project 6: Agentic Workflows.** Adapt structured requests, read-only
   allowlisted tools, per-run memory, aggregate observations, bounded calls,
   stop-on-failure and human review into a new five-stage orchestrator.
   Unlike the earlier penguin reviewer, validation findings here stop
   downstream model fitting and statistical diagnosis.

## New interaction

Registered CSV → load → dataset-specific quality gate → chronological split →
fixed model/baseline → daily/hourly error diagnosis → human review report.
Any gate finding holds the run; failures and budget exhaustion are incomplete.
No tool edits data, sends messages, dispatches bikes or trains on test labels.
No LLM, API credentials, deep learning or generative component is necessary:
irrelevant techniques would increase complexity without serving this problem.

## Evaluation fixed before implementation

Run the unmodified historical source end-to-end. Report both model scores, full
test predictions, day/hour error summaries, training-defined upper-quartile
demand stress errors and descriptive daily Spearman correlation. Keep the prior
model unchanged even if scores lose. The same benchmark has already been seen
in Project 3, so it is not independent evidence of performance on a new city,
new deployment or unseen research test.

Designed scenarios (declared fixtures, never presented as field defects):
missing value; duplicate timestamp; invalid hour; unknown weather category;
nonfinite measurement; missing required column. All should hold after the
quality gate without splitting, fitting or diagnosis.
An automatic-allocation request should be blocked before any tool.
A two-call budget should stop before split.
An injected model-tool failure should stop before statistical diagnosis.
Source hashes and fixture equality should demonstrate no data modification.

Known limitations to retain: high errors in demanding periods, contemporaneous
weather required, historical city-specific data, recorded rentals not unmet
demand, absent station/demographic data, incomplete plausibility checks and
no causal interpretation of descriptive error associations.

Deliver an integrated executed notebook, full implementation/configuration,
architecture diagram, trace/scenario evidence, pinned prior-artifact map,
original data/attribution, actual pip freeze and tested reproducibility.
Write a 1,500–2,000-word APA synthesis paper with the seven required sections.
Project 8 presentation/mentor defense is not part of this submission.
