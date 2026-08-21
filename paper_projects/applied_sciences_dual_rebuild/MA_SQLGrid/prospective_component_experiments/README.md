# Prospective component experiments

Frozen Round-1 supplements for MA-SQLGrid:

- `PROTOCOL_FREEZE.md/json`: design, identities, hashes, populations, and call budget.
- `STATISTICAL_ANALYSIS_PLAN.md`: cluster-aware inference and claim rules.
- `FEASIBILITY_AND_LEAKAGE_AUDIT.md`: reusable assets, rejected reuse, and leakage boundary.
- `CALL_BUDGET_AND_RUNBOOK.md`: execution gates and entry points.
- `build_freeze.py`, `verify_freeze.py`, `run_frozen.py`, `offline_replay.py`, `aggregate_results.py`: preparation, verification, opt-in local execution, two-phase replay/scoring, and registered aggregation.
- `tests/fixtures/synthetic_pairs.json` and `tests/test_aggregate_results.py`: pre-run synthetic validation of weighting, bootstrap, randomization, Holm adjustment, claim rules, modifier orientation, and latency back-transformation.

Current state: prompt/call ledgers are frozen and verified; no formal model execution or outcome analysis has started.

Run `python current_status.py` for a fail-closed state check. The expected pre-execution value is `FROZEN_NOT_RUN`.
