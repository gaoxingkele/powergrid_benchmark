# Semantic reliability design audit

This directory is an independent, non-formal audit. It does not modify or certify `semantic_reliability_experiment` and must not be cited as a completed claim-promoting experiment.

Artifacts:

- `INDEPENDENT_SEMANTIC_RELIABILITY_DESIGN_AUDIT.md`: decision, design, risks, gates, and release checklist;
- `audit_design_inventory.py`: read-only source audit plus transient in-memory diagnostic states;
- `diagnostic_inventory.json`: hashes, ledger-integrity evidence, feature/QID inventory, per-state distinguishability, evaluator contract checks, and provisional prediction collision counts;
- `go_no_go_gates.json`: machine-readable gate state and required closure evidence.

Reproduce the diagnostic from this directory with:

```powershell
python audit_design_inventory.py
```

The script writes only `diagnostic_inventory.json` in this directory. Source databases, ledgers, the formal semantic experiment, and manuscript are never written.

