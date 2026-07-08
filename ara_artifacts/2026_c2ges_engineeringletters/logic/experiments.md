# Experiments

## E01: Imported C2GES Smoke Run

- Verifies: Local environment readiness for the C2GES experiment wrapper.
- Setup: `paper_projects/2026_c2ges_engineeringletters/source/code/main.py`
- Procedure: Run `python source/code/main.py --limit-docs 1 --bootstrap-samples 10 --out-dir debug/c2ges_smoke_run`.
- Expected: Script starts and produces smoke output.
- Evidence: `paper_projects/2026_c2ges_engineeringletters/debug/initial_smoke.md`
- Status: Blocked because `numpy` is missing.

## E02: Primary K=3 Evidence Selection Comparison

- Verifies: Imported quantitative C2GES comparison claims.
- Setup: Imported source package summary artifact.
- Procedure: Inspect existing summary values; do not invent rerun values.
- Expected: Full C2GES evidence F1 and ablation deltas match source package.
- Evidence: `paper_projects/2026_c2ges_engineeringletters/source/supplement/bm25_k_sensitivity/summary.json`
- Status: Imported evidence.
