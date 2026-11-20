# Bike-Share Evidence Review: An Integrative Industry Synthesis

AI Foundations (Edward Hickman)

## Overview and Industry Context

Urban bike-share analysts need evidence they can inspect before using AI estimates in planning discussions. A model can summarize patterns in recorded rentals, but a low overall error alone does not establish that its inputs are valid or its outputs support operational decisions. This project addresses that gap through an LLM-directed evidence-review workflow for sustainable transportation. It combines data-quality control, rental estimation and statistical error interpretation, ending with human review rather than automatic bike allocation.

The historical input is the UCI Bike Sharing dataset: real 2011–2012 Capital Bikeshare records with calendar and observed weather variables (Fanaee-T, 2013; Fanaee-T & Gama, 2014). The included hourly file contains 17,379 records; its actual contents and source Readme, rather than the landing page's inconsistent count, determine computations. The source is attributed under CC BY 4.0. No live operator partnership, contemporary data access or measured environmental benefit is claimed.

In practical terms, the program first checks a rental table, then builds estimates only if those checks find no listed problem. It shows a person where the estimates miss most. A problem in a test copy stops the next steps; finishing the checks does not prove that every record is correct. The result helps an analyst ask better questions, not decide how many bikes to move.

Success is defined narrowly: accepted historical input must produce traceable estimates and error evidence, while specified invalid inputs must not reach fitting. The workflow must preserve the original records and expose incomplete runs rather than silently substitute old results. These criteria can be demonstrated locally without pretending that an educational prototype has earned an operator's authorization to act.

## Integration Rationale

Three earlier capstones contribute distinct methods to one connected artifact. Project 3, Machine Learning Foundations, supplies the fixed random-forest recipe, twelve predictors, training-mean baseline and chronological date partition. Random forests combine randomized trees and support regression (Breiman, 2001). Retaining this already examined recipe makes predictive behavior traceable and avoids confusing new integration with unreported tuning. Its score is reproduced, not improved.

Project 2, Statistical Analysis, contributes descriptive group summaries, rank-based association and careful separation of association from cause. Its school-study records, effect sizes and significance results are not transferred into transportation. Instead, the new diagnostic computes daily mean temperature versus daily mean signed model error and summarizes errors by hour and demand level. SciPy defines Spearman's coefficient as a measure of monotonic association (SciPy developers, n.d.). The earlier reviewer's emphasis on ordinary language also informs the explanation of what these estimates can and cannot support.

The corrected Project 6 contributes a real MiniMax language-model agent, LangGraph's decision/tool loop, natural-language task interpretation, message memory and bounded execution. Its penguin data are not reused. The language model selects tools and reads their aggregate observations; Python enforces permissions rather than supplying a checklist. Here, quality findings prevent fitting and actual predictions feed three independently selectable diagnostics. LangGraph supports this distinction between fixed workflows and model-directed agents (LangChain, n.d.).

PRIOR_PROJECT_MAP.md identifies the prior notebooks, plans and exact repository commits. The earlier deterministic plan is superseded by a documented revision after Project 6's reviewer rejected rule-only agency. The new model is an interface and evidence-selection component, not a replacement for statistical computation. Neural networks and image generation remain excluded because they add no relevant contribution. The development scenarios are not a preregistered or held-out evaluation.

## System Design and Technical Decisions

Figure 1 shows the implemented architecture. A request permits only the registered historical dataset and retrospective-review intent. A cautious analyst persona and user instructions enter a LangGraph loop: model decision, guarded tool execution, returned observation, next model decision. Seven tools expose loading, quality, splitting, modeling, daily association, hourly errors and demand stress. The model chooses relevant diagnostics and when to stop. A focused quality request needs no fitting; an hourly-only request omits the other diagnostics. State stores messages, observations, counters, public justifications and temporary frames, starting fresh each run. Public reasons are not private chain-of-thought.

Loading checks the original file's size and SHA-256. The quality gate checks required columns, missingness, repeated date/hour keys, finite numeric values, category membership, normalized weather ranges, rental count consistency and basic calendar agreement. Findings hold the run before splitting or fitting. Dependencies cannot be waived by model text. Seven executions and sixteen model turns bound a run; failures and exhausted budgets cannot approve partial evidence. Multiple requested tools are rejected together, with feedback for a new model decision. These are configured checks, not complete semantic validation. The evaluation harness writes outputs; tools do not edit the source or dispatch resources.

The model stage keeps whole dates together: 13,891 earlier rows train the estimators and 3,488 later rows test them. Preprocessing is fitted only on development inputs. Target-derived casual and registered counts are excluded because their sum equals the target; identifiers are also excluded. The forest retains 150 trees, depth fourteen and the earlier seed. No model search follows the new diagnostics.

Predictions then drive daily and hourly error summaries. A higher-demand stress group uses the development count's seventy-fifth percentile, 258 rentals, as a fixed threshold. Group membership uses actual test outcomes, so this is retrospective analysis, not a future routing rule. Observed weather also prevents calling the model an advance forecast. The 165 absent clock hours are audited, not filled with invented zeros.

## Ethical Considerations and Responsible AI

Recorded rentals are not unconstrained demand. People unable to find available bikes leave no completed rental in this aggregate table. Automatically allocating supply according to historical recorded use could therefore reinforce existing service shortages. The dataset lacks station and demographic information needed to evaluate that possibility. Hourly error differences are not a geographic or demographic fairness audit, and no equitable-service claim is justified.

Underestimation also has an operational meaning: a planner who treats point estimates as reliable capacity requirements could provision too little service. The implemented response is limited authority, not an invented optimal allocation. Outputs remain evidence for a named human decision-maker; no write, repair, messaging or bike-dispatch tool exists. Transparent limitations and contextual accountability align with risk management principles, but this prototype is not NIST-certified (National Institute of Standards and Technology [NIST], 2023).

Implemented safeguards must be distinguished from deployment requirements. Current controls include a source fingerprint, fixed request/tool names, bounded execution, quality holds and failure traces. A real service would additionally require current local records, forecast-weather availability checks, station-level service-equity consultation, access controls, protected logs, timeouts and monitoring with rollback responsibility. None is established by a passing notebook. The code is not isolated from a malicious developer. A sixty-second provider timeout is not an end-to-end deadline or arbitrary-defect recovery.

The public historical table contains no individual identities, but that does not establish privacy for future rider-level extensions. Only user instructions and aggregate observations go to MiniMax; raw dataset rows remain local. Provider access, costs, retention and availability therefore need review. Generated explanations may misstate evidence and require human checking; computed observations, not fluent prose, are authoritative. Ethical review must change with the data and intended use, rather than inherit approval from this small demonstration (NIST, 2023). AI assistance in coding, testing and drafting is disclosed; Edward must review, understand and personalize the submission under course policy.

## Evaluation and Reflection

The recorded full review completes all seven tools. The forest's test RMSE is 104.65 rentals per recorded hour, compared with 232.56 for the training-mean baseline; MAE is 72.57. These match Project 3 because the data, recipe and split are unchanged. Reproduction validates the integration, not predictive generalization to an independent new city or research holdout. No business savings or service improvement was measured.

The new stress analysis exposes a practical weakness. Across 1,413 test hours with at least 258 rentals, MAE is 123.80 and mean actual-minus-predicted error is positive 119.74. The other 2,075 hours have MAE 37.69. In ordinary language, busy-hour estimates are usually too low and miss by about 124 rentals on average, despite the better overall score. This is evidence for caution, not proof that moving a particular number of bikes would solve the problem.

Across 147 dates, daily mean temperature and mean signed error have Spearman correlation −0.0771, a weak descriptive association. Season, year, serial dependence and daily aggregation limit interpretation. No p-value, causal temperature effect or claim that weather errors are absent is inferred. The analysis transfers Project 2's reasoning discipline instead of treating its previous test as a universal recipe.

Twelve designed boundary or focused scenarios accompany the original. Six altered fixtures—missing value, duplicate timestamp, invalid hour, unknown weather, nonfinite value and absent column—are held after two executions without fitting. Focused requests demonstrate shorter model-selected paths; natural-language allocation is refused, while an invalid structured intent is blocked before any model call. A two-call budget ends incomplete; an injected model failure prevents diagnosis. Live transcripts are distinct from scripted-model software tests.

Initial real traces revealed attempted continuation or repeated checks after quality findings. Guards stopped execution. Those traces remain included; revised permission feedback lets the model explain a hold. A second live narrative reversed residual signs and mislabeled hourly groups as days. Raw responses are retained; tool contracts now explicitly define actual-minus-predicted signs and units. This is development evidence, not proof that the model always obeys or explains correctly. Current prose still suggests an untested error mechanism and calls one error group accurate without operational tolerances; the explanation audit distinguishes observations from such interpretations. Unchanged loading, quality, split and model implementations and byte-identical prediction/diagnostic tables support numerical continuity. Source hashes remain unchanged; no field deployment was tested.

Integration thus adds control and explanation, not predictive accuracy. The important lesson is that a data gate can prevent certain invalid computations while error analysis can still reveal an unsuitable operational assumption. Better average prediction and responsible deployment are separate questions. A clean-looking table can still reflect constrained access, and a successful software run cannot resolve missing business context. Combining components makes those boundaries more visible, but also adds interfaces that require testing. Retaining an explicit incomplete status is preferable to producing a confident report after a failed prerequisite.

## Professional Relevance

The artifact demonstrates work expected in applied AI roles: defining a bounded decision problem, preserving data provenance, separating training from evaluation, specifying component interfaces and communicating evidence to non-specialists. Its value is an inspectable connection between model quality, workflow behavior and professional responsibility, not a claim of production readiness.

The executed notebook, full source, configuration, scenario traces and architecture diagram let another analyst reproduce and challenge the design. The actual environment freeze supports reconstruction, while immutable prior-artifact identifiers make the contribution of each earlier capstone explicit. This distinction matters in a portfolio: reused methods are credited honestly, and the new integration can be assessed on its own merits.

Next work should validate present-day, local performance and meaningful service outcomes with stakeholders before introducing any action capability. Project 8's separate presentation and mentor defense should explain why the model is retrospective, why busy-hour errors matter, why quality checks are incomplete and why humans retain operational authority. This submission supplies evidence for that discussion; it does not replace Edward's own understanding.

## References

Breiman, L. (2001). Random forests. Machine Learning, 45, 5–32. https://doi.org/10.1023/A:1010933404324

Fanaee-T, H. (2013). Bike Sharing [Data set]. UCI Machine Learning Repository. https://doi.org/10.24432/C5W894

Fanaee-T, H., & Gama, J. (2014). Event labeling combining ensemble detectors and background knowledge. Progress in Artificial Intelligence, 2, 113–127. https://doi.org/10.1007/s13748-013-0040-3

LangChain. (n.d.). Workflows and agents. https://docs.langchain.com/oss/python/langgraph/workflows-agents

National Institute of Standards and Technology. (2023). Artificial intelligence risk management framework (AI RMF 1.0) (NIST AI 100-1). https://doi.org/10.6028/NIST.AI.100-1

SciPy developers. (n.d.). scipy.stats.spearmanr. https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.spearmanr.html
