# Data attribution and integrity

Fanaee-T, H. (2013). *Bike Sharing* [Data set]. UCI Machine Learning Repository.
https://doi.org/10.24432/C5W894

Original download:
https://archive.ics.uci.edu/static/public/275/bike+sharing+dataset.zip

`hour.csv` is included unchanged from the prior ML capstone:
17,379 rows × 17 columns; 2011–2012 Capital Bikeshare hourly rental logs.
SHA-256: `e03de4ee4ef4dc376ac6e04bf829673c6269e8eba5c60fa121640fa2f829504f`

The actual file/source Readme contain 17,379 rows; the UCI landing page lists
17,389. Calculations use the included file, not the inconsistent landing count.

License: Creative Commons Attribution 4.0 International,
https://creativecommons.org/licenses/by/4.0/
UCI allows sharing/adaptation with attribution. The original dataset is not
altered. Test fixtures are transparent in-memory alterations, not discovered
problems in these historical observations.

The source requests attribution to Fanaee-T and Gama (2014), *Event labeling
combining ensemble detectors and background knowledge*, *Progress in Artificial
Intelligence, 2*, 113–127. https://doi.org/10.1007/s13748-013-0040-3

Weather variables retain source normalization. `cnt` is recorded rentals,
not unique riders or unmet demand. `casual` and `registered` sum to the target
and are excluded from predictors, along with row identifier `instant`.
No station/demographic information is available for allocation/fairness audits.
