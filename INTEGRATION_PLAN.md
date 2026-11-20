# Integration plan — revised agentic contribution

The original deterministic plan preceded the first Project 7 implementation.
This revision follows Project 6's reviewer feedback and its corrected LLM
implementation. Development findings informed the revision; this is not a claim
of preregistration or a held-out experiment.

## Bounded industry problem

Urban bike-share analysts need inspectable retrospective model evidence.
The system cannot move bikes, repair data, serve a live forecast or establish
causal/fairness/business outcomes. Completed rentals are not unmet demand.

## Three prior contributions

1. Project 3 supplies unchanged loading, quality/split conventions, fixed forest,
   features and mean baseline. No search or retuning follows the diagnostics.
2. Project 2 supplies descriptive group/rank reasoning and nontechnical,
   noncausal communication, not school records or school-study effect sizes.
3. Corrected Project 6 supplies MiniMax/LangGraph agency: persona, instructions,
   explicit messages, dynamic tool calls, observations, run-local memory and guards.
   No penguin data enter the bike model.

## Integrated behavior

User task → LLM → guarded selected tool → aggregate observation → LLM.
Seven available tools expose load, quality, split, model and three independent
post-model diagnostics: daily association, hourly errors and demand stress.
The model chooses applicable evidence and when to finish; guards enforce the
computation prerequisites without choosing its next action.

Quality-only requests need no fitting. Hourly-only reviews need the model but
not the other diagnostics. Quality findings prohibit all further tool execution.
Failures and insufficient budgets cannot become approval; partial pipeline
coverage is explicit even when a focused task is completed.

## Development evaluation

Use thirteen declared cases: unmodified source; six flawed-input fixtures;
quality-only and hourly-only natural-language requests; natural-language allocation;
structured invalid intent; two-call budget; injected model failure.
Record actual model messages, public justifications, tool observations, usage
metadata and source/code/config fingerprints. Do not replace failed responses
or treat designed cases as a universal success rate.

Initial real attempts to continue/repeat checks after quality findings are retained
under `outputs/development_attempts/first_live_suite`. Guards stopped execution;
explicit hold feedback was added. Current and development manifests are distinct.

Verify unchanged numerical methods against the previous Project 7 implementation
and byte-compare predictions and diagnostic tables. The historical benchmark
has already been seen in Project 3; equality checks integration, not new
generalization. Software tests with scripted responses are separately labeled.

## Responsible use and delivery

Only instructions and aggregate observations go to MiniMax. The model can
misinterpret evidence or ignore instructions; machine-enforced state and human
checking are authoritative. Keep source read-only, no operational action tools,
seven execution/sixteen model-turn bounds and provider timeout. These are not
OS isolation, scientific certification or an end-to-end deadline.

Deliver executed notebook, source/config/data, actual freeze, fresh real traces,
architecture and revised 1,500–2,000-word APA paper. Update defense notes to match.
Project 8 remains a separate Project 7-focused presentation and live discussion.
