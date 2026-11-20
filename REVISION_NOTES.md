# What changed and why

The user requested this targeted revision after the Project 6 reviewer rejected
deterministic rule-based execution as a demonstration of LLM agency.
Project 7's own rubric does not universally require an LLM. However, its selected
three-project integration explicitly relies on Project 6, so its agentic
contribution is now grounded in that project's corrected implementation.

## Implementation

- Replaced the fixed `for name, reason` execution list with a LangGraph model/tool loop.
- Added persona, natural-language instructions, message memory, public reasons,
  provider usage metadata and actual observation feedback.
- Exposed the former combined diagnosis as three independent post-model tools
  so the model can select appropriate analyses and their order.
- Kept loading, quality, date splitting, forest/baseline and numeric calculations.
- Retained hard guards: data/intent restrictions, prerequisites, quality holds,
  no repeats, execution/model-turn bounds, no source edits or allocation capability.
- Preserved initial live failures to follow quality-stop instructions; improved
  permission feedback rather than hiding traces or replacing model responses.
- Retained a second live suite whose narrative reversed error signs and confused
  hours with days; added explicit residual definitions/units to tool observations
  and the persona. This does not guarantee that future prose will be correct.

## Evidence and reporting

Current real traces have code/config fingerprints. Scripted software tests are
separate. Prediction and daily/hourly CSVs are byte-identical to the earlier
Project 7 numerical outputs, which already reproduce Project 3's seen benchmark.
No new accuracy gain, untouched holdout, deployment or passing course decision
is claimed. Fresh notebook/report/diagram replace the old “no LLM/five tools” account.

`DEFENSE_UPDATE.md` contains revised Project 7-only study and adversarial answers.
Any old presentation saying “rule-only/no LLM/five calls/ten scenarios” is obsolete.
The statistical results and their limitations remain unchanged.
