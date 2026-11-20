# Verification record

## Working environment and tests

Python 3.11.18; exact packages in the actual `pip freeze` requirements.
`python -m pytest tests -q`: **27 passed**, saved in `outputs/validation.txt`.
Python implementation/builders/tests compiled successfully.

Tests check original run order and bounded trace, exact scenario replay,
six gate holds with no downstream fit, structured-request restrictions,
failure/budget handling, fresh memory, fixture immutability, additional
range/count/date checks, tampered-source rejection, unknown tools, whole-day
partitioning, leakage exclusions, independently recomputed metric/rank values,
paper sections/word counts, prior-artifact mapping, template preservation and
the actual dependency freeze/source hash.

Compared all 3,488 new prediction and target values with the pinned Project 3
output: every value matches exactly. This is a wiring/reproduction check,
not an accuracy improvement or independent research validation.

The higher-demand group underestimates 1,337 of 1,413 recorded hours, supporting
the report's plain statement that its busy-hour estimates are usually too low.
The group is defined using actual outcomes and cannot identify future busy
hours before those outcomes are known.

## Clean-environment reproduction

Created a fresh Python 3.11.18 environment from `requirements.txt` and a clean
directory containing only implementation, configuration, notebook and original
CSV. No old outputs were copied.

Ran the notebook top to bottom. Every generated JSON/CSV matched the original
byte-for-byte: ten scenario records, all test predictions, daily/hourly
diagnostics, scenario summary, source-integrity record and runtime versions.
This verifies the specified stack, not every platform or package combination.

## Source integrity and visual review

Original CSV SHA-256:
`e03de4ee4ef4dc376ac6e04bf829673c6269e8eba5c60fa121640fa2f829504f`.
Source hashes before and after the suite are identical; fixture copies are
unchanged by the agent. The raw CSV retains its original CRLF line endings.

Viewed the full architecture image and all nine rendered PDF pages.
No clipped content or missing pages found. The plain-language workflow
explanation is on page 2; plain busy-hour interpretation is on page 6.

The report has 1,564 body words. Counting headings/references gives 1,653;
counting cover and caption text gives 1,713. Thus both body-only and inclusive
document counts are within 1,500–2,000 words. Counts use whitespace-separated
words and exclude the diagram's embedded raster labels and page fields.

Template styles, section XML and existing header/footer parts were preserved.
See `outputs/report_template_audit.json` for the source template and audit.
The figure and references are included in the report and package.

## Limits of evidence

Ten purpose-built scenarios do not establish broad robustness or security.
No live operator, station allocation, intervention, demographic fairness audit,
causal analysis, cost saving or environmental benefit was tested.
No OS isolation or wall-clock tool timeout is implemented.
The earlier benchmark is already known and is not independent deployment evidence.

There is no GitHub Actions workflow; local checks do not mean CI passed.
Remote head/state/required checks are inspected separately after publication.
No classroom submission or mentor defense has been completed by this workflow.
