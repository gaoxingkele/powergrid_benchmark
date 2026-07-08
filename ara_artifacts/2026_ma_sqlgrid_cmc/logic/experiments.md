# Experiments

## E01: Setup Smoke

- Verifies: The imported experiment package can locate its local experiment assets.
- Setup: `paper_projects/2026_ma_sqlgrid_cmc/source/code/experiment_final/setup.py`
- Procedure: Run `python source/code/experiment_final/setup.py`.
- Expected: `SETUP_OK`.
- Evidence: `paper_projects/2026_ma_sqlgrid_cmc/debug/initial_smoke.md`
- Status: Passed.

## E02: Evaluator Unit Tests

- Verifies: The local evaluator can load the SQLite dataset and score known cases.
- Setup: `paper_projects/2026_ma_sqlgrid_cmc/source/code/evaluator/tests`
- Procedure: Run `pytest -q source/code/evaluator/tests`.
- Expected: All evaluator tests pass.
- Evidence: `paper_projects/2026_ma_sqlgrid_cmc/debug/initial_smoke.md`
- Status: Failed because tests resolve dataset paths under `source/code/data/...`.

## E03: Formal C1-C5 Comparison

- Verifies: Imported C1-C5 execution-accuracy claims.
- Setup: Imported final outputs and diagnostics.
- Procedure: Inspect existing final artifacts; do not invent rerun values.
- Expected: C4 and C5 scores match verified package.
- Evidence: `paper_projects/2026_ma_sqlgrid_cmc/source/code/experiment_final/outputs/results.json`; `paper_projects/2026_ma_sqlgrid_cmc/source/evidence/validator_diagnostics/validator_diagnostics.json`
- Status: Imported evidence.
