# Integrated AI Synthesis — Bike-Share Evidence Review

**AI Foundations (Edward Hickman) · Udacity · Project 7**

A new offline workflow for urban bike-share planning discussions:
**data-quality gate → retrospective rental estimates → error diagnosis →
human evidence review**. No automatic allocation, data repairs, LLM, live API
or paid service is involved.

## Explicit three-project integration

- **Project 2 — Statistical Analysis:** transfer group summaries, Spearman
  association and noncausal/plain-language interpretation to new error diagnostics.
- **Project 3 — Machine Learning Foundations:** refit the same fixed forest,
  mean baseline, twelve predictors and whole-date chronological split.
- **Project 6 — Agentic Workflows:** adapt structured requests, bounded
  read-only tools, run-local state, traces and stopping into a new orchestrator.

This is not three notebooks placed together. Gate findings prevent fitting;
actual fitted-model residuals are the inputs to the new statistical diagnosis.
`PRIOR_PROJECT_MAP.md` identifies the exact earlier artifacts and immutable
commits. `INTEGRATION_PLAN.md` was committed before execution.

## Required submission and supporting files

- `integrated_synthesis.ipynb` — executed integrated artifact with complete
  source display, diagram, original run, boundary scenarios and interpretation.
- `integrated_system.py` — full standalone implementation and evaluation harness.
- `module_summary.pdf` — nine-page APA synthesis paper; **1,564 body words**,
  1,653 including headings/references, 1,713 including cover/caption text.
- `outputs/architecture_diagram.png` — separate architecture diagram,
  also embedded in the notebook and report.
- `config.json`, `data/hour.csv`, `data/DATA_NOTICE.md` — full configuration
  and unmodified attributed public data.
- `requirements.txt` — actual working-environment `python -m pip freeze`.

The editable report, Markdown report, HTML notebook export, tests, scenario
traces, predictions, diagnostic tables and provenance map are extras. Everything
needed to run the integrated artifact is included; no separate prior-repository
checkout or dataset download is required.

## Reproduce

Tested on Python **3.11.18 / Linux**, using methods and libraries already used
in the prior capstones:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python integrated_system.py
python -m pytest tests -q
```

The script writes evaluation outputs under `outputs/`. The agent's tools do
not change source data. All model fitting occurs on the earlier-date partition;
the saved artifact includes predictions, not a separately required serialized
estimator. Running the script refits the fixed model.

Open `integrated_synthesis.ipynb` in Jupyter and restart/run all cells, or:

```bash
python -m nbconvert --to notebook --execute --inplace integrated_synthesis.ipynb \
  --ExecutePreprocessor.timeout=180
```

Run from the repository root so the notebook can import the implementation and
find the bundled data. To intentionally rebuild notebook source and HTML:

```bash
python scripts/build_notebook.py
python -m nbconvert --to notebook --execute --inplace integrated_synthesis.ipynb
python -m nbconvert --to html integrated_synthesis.ipynb --output-dir outputs \
  --output integrated_synthesis.html
```

## Actual results and limits

The original 17,379-row source passes the configured gate. The model fits 13,891
earlier rows and scores 3,488 later rows over 147 dates. Forest RMSE **104.65**
versus mean-baseline **232.56** rentals/hour exactly reproduces Project 3;
this is **not independent validation on unseen research data**.

New diagnostics show MAE **123.80** in 1,413 higher-demand hours versus **37.69**
in 2,075 other hours; the development-derived threshold is 258 actual rentals.
Higher-demand mean signed error is **+119.74** (actual minus prediction).
Daily temperature/residual Spearman correlation is **−0.0771**, descriptive
only, with no p-value or causal claim. The stress grouping uses actual test
outcomes, so it cannot route future requests.

Six deliberately flawed fixtures stop before fitting; an allocation request
is blocked, a limited budget stops incomplete and an injected model failure
prevents diagnosis. These designed scenarios are not field defects or a broad
safety benchmark. **27 tests passed**; a fresh environment reproduced every
scenario, prediction and daily/hourly diagnostic file exactly.

Recorded rentals are not unmet demand. Weather is contemporaneously observed,
not future forecast data. No station-level allocation, demographic fairness,
cost saving, emissions benefit, prediction interval or production readiness is
demonstrated. The rule gate is not complete scientific validation.

## Report and academic integrity

All seven required sections and five credible references are included,
including scholarly sources. The report preserves the supplied course APA
template's native styles, section geometry and headers. Arial is retained in
the DOCX; LibreOffice substitutes Liberation Sans in PDF export. Instructor
and due date were not supplied and are omitted.

Rebuilding the report is optional and requires the original course template
and LibreOffice in addition to the Python environment:

```bash
python scripts/build_report.py /path/to/course-apa-template.docx
```

The included PDF/DOCX can be opened without those authoring dependencies.
AI assistance is disclosed. Edward must review, understand and personalize the
work under course policy. Nothing automatically submits to Udacity or merges
the draft PR. **Project 8's presentation and mentor defense are separate**;
no slide deck or completed defense is claimed here.
