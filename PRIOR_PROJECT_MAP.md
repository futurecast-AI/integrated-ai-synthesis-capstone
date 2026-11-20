# Explicit provenance: three prior projects → one new workflow

All source projects belong to Edward Hickman's capstone sequence. Their
development artifacts are identified by immutable commit, not a moving `main`
branch. Prior PRs remain unmerged; this synthesis does not change them.

| Prior capstone | Identified artifact | Contribution to this new system | New integration |
| --- | --- | --- | --- |
| Project 2 — Statistical Analysis | `analysis.ipynb`, `ANALYSIS_PLAN.md`, revised `module_summary.pdf` at `0e232535674bb36e51d3fe177110c67d5940d7a5` | Rank-based description, group summaries, noncausal interpretation and reviewer-driven plain-language communication | `EvidenceTools.diagnose()` receives actual model residuals and computes a new descriptive daily association; no student data/effect sizes/p-values are transplanted |
| Project 3 — Machine Learning Foundations | `modeling.ipynb`, `MODELING_PLAN.md`, `hour.csv`, `outputs/test_predictions.csv` at `cc3919479ee9c4f67cca6992ae9ea5dcf217c434` | Same twelve predictors, leakage exclusions, 150-tree fixed forest, mean baseline and chronological 80/20-date partition | `EvidenceTools.model()` runs only after the new data gate; freshly computed predictions feed diagnosis |
| Project 6 — Agentic AI Systems | `agentic_system.py`, `DESIGN_PLAN.md` and scenario traces at `5f8fb2a12b6ee137b1414004169019d95ccac870` | Structured requests, bounded allowlisted tools, fresh run-local state, fixed policy reasons and safe stopping | `SynthesisAgent` now orchestrates data validation, split, modeling and statistical diagnosis; quality findings actively prevent downstream fitting |

Open the identified versions:

- Project 2: https://github.com/futurecast-AI/statistical-analysis-capstone/tree/0e232535674bb36e51d3fe177110c67d5940d7a5
- Project 3: https://github.com/futurecast-AI/machine-learning-foundations-capstone/tree/cc3919479ee9c4f67cca6992ae9ea5dcf217c434
- Project 6: https://github.com/futurecast-AI/agentic-ai-systems-capstone/tree/5f8fb2a12b6ee137b1414004169019d95ccac870

No prior report is resubmitted as this report. No prior agent is simply renamed.
The new deliverable links its components by control flow and typed in-memory
data, exposes gate failures, adds new daily and demand-stress diagnostics, and
evaluates the integrated behavior. It intentionally does not add unrelated
image generation, neural networks or new technologies to inflate domain count.

The dataset and fixed model benchmark have already been examined in Project 3.
Reproducing those scores checks integration; it is not independent validation
on unseen research data. The new diagnostic is descriptive and post hoc, not
used to retune the model or claim a confirmed hypothesis.
