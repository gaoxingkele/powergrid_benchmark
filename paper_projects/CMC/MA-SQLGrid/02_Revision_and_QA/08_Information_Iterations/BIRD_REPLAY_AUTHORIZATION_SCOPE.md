# Proposed BIRD replay — implementation/execution confirmation

2026-09-13. Status: awaiting explicit implementation/execution confirmation.
No adapter has been implemented or executed; this is not an experiment freeze.

## Read-only inspection findings

- `framework/QueryAnalyst` and `offline_coordination_study_v2.validation_for`
  can derive the historical score from question and candidate SQL without gold.
- The historical executor has read-only URI, query_only, disabled extensions,
  authorizer and opcode/time/row limits.
- The later `final_executor/sqlite_readonly_executor_final.py` adds cell/result
  byte and output-column limits. These are post-review controls and must not
  be described as the historical environment.
- Both timeouts rely on SQLite progress callbacks. Neither source supplies an
  independent worker-process wall-clock boundary. The new runner should execute
  candidate queries in a worker process with a hard timeout, and retain failures
  without automatic retry. Do not claim the callback alone bounds every call.

## Proposed authorized scope

Implement an additive replay adapter and synthetic isolation tests, preserving
all old code/data. Freeze adapter/source/database hashes and runtime before the
new diagnostic run. Run the 4000 retained final SQL candidates in two separate
four-slot pools across 500 questions and 11 databases. Preserve empty SQL and
all failures. Use original 10/5/capped-5 score and fixed B0/B1/B2/B3 tie order;
no tuning based on results. Run validation-only, not invented witness transfer.

Proposed resource bounds: 2-second SQLite callback deadline, 5-second worker
wall timeout per candidate, 2 million opcodes, 10000 rows, 1 MiB per cell,
8 MiB budgeted result, 256 output columns; record rather than hide limit hits.
No network, LLM calls, database writes, raw-data publication, submission or fees.
These are proposed operational controls, not universal scientific standards.

Separate stages: candidate-only input export → sealed score/selection records
→ offline correctness join → per-question and per-database failure partition.
Validate that changing gold labels cannot change selection. Statistical output
is descriptive; no new inferential significance claims are proposed.

The intended new CLI (not yet present) is:

```text
python -B run_bird_validation_replay.py --protocol <retained-protocol-directory> --output <new-run-directory>
```

The ARS experiment workflow permits only explicitly user-confirmed experiment
commands and forbids autonomous generation/modification of experiment scripts.
User confirmation must cover both the additive adapter/tests and this one
exploratory run. It does not confer unseen-test status, expert validation,
redistribution permission or authority to submit.
