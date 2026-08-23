# Reproduction Plan

## Target Scope

Validate the MA-SQLGrid local Text-to-SQL benchmark and preserve its claims as local to GridDB-Maintenance-v2 v0.1.

## Shared Code Dependencies

- Python standard library plus any imports required by `source/code/experiment_final/`.
- SQLite database bundled in the uploaded package.
- LaTeX environment if local PDF rebuild is required.

## Paper-Specific Implementation

- Preserve `source/manuscript/paper.tex` as the current final manuscript source.
- Preserve `source/manuscript/references_verified.bib` as the 45-key citation set.
- Treat `source/verification/verification_report.json` and `source/verification/stage23_decision.json` as the current verification state.

## Dataset and Grid System

- Dataset: `GridDB-Maintenance-v2 v0.1`.
- Dev questions: 20.
- Test questions: 180.
- Database engine: SQLite.

## Experiment Matrix

- C1 SchemaOnly Direct.
- C2 FullSchemaValues Direct.
- C3 CHESSLite Generic.
- C4 MASQLGrid DomainContext.
- C5 MASQLGrid DomainContext Validated.
- Component ablations: C4 without value hints and C4 without shape hints.

## Expected Outputs

- prediction records
- score records
- traces
- `results.json`
- diagnostic reports
- manuscript PDF
- ARA evidence entries under `ara_artifacts/2026_ma_sqlgrid_cmc/evidence/`

## Acceptance Criteria

- Stage 23 citation verification remains complete: 45 cited keys, 0 missing, 0 extra verified keys.
- Claims remain local to the fixed GridDB-Maintenance-v2 v0.1 protocol.
- No external Spider/BIRD-style benchmark claim is added without a new run.
- Evaluator tests pass after packaging-path repair.

## Known Blockers

- `pytest -q source/code/evaluator/tests` currently fails because test code resolves dataset paths to `source/code/data/...` instead of `source/data/...`.
- `pdflatex` is not available in the current shell.
