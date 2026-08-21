# Existing-to-Original-Title Asset Map

Audit date: 2026-08-08 (Asia/Shanghai). This map distinguishes reusable evidence
from new, unevaluated functionality. Paths are relative to the repository root.

| Asset | Audited evidence | Use in original-title version | Status/boundary |
|---|---|---|---|
| `paper_projects/2026_ma_sqlgrid_cmc/source/code/experiment_final/main.py` | 950 lines; SHA-256 `2D5BC317C25DFB903E261D1B7CE5A0362F13C4D9F022133A169AB55E1952F7E6` | Reuse prompt construction, context bundles, candidate parsing, reference-free validation interfaces, scoring contracts | Historical implementation; its old C5 candidate/rank/repair path is not the formal four-cell run |
| `paper_projects/2026_ma_sqlgrid_cmc/source/code/experiment_final/experiment_harness.py` | 59 lines; SHA-256 `38F4E022E5DD6804F77DDE371AC5A2829850FD30C147C720A27417442D4923AD` | Reuse run/condition loop concepts and trace discipline | Adapter required; do not overwrite |
| `round1_revision_assets/METHOD_AND_PROMPT_ASSETS.md` | Documents F00/F01/F10/F11 and gold-exclusion contract | Authoritative method boundary for inherited four-cell experiment | Formal algorithm is one generation per prompt with no ranking/repair |
| `formal_run/qwen25coder7b_q4km_seed20260805_clean_rerun1/predictions.jsonl` | 720 rows; SHA-256 `53AAF0C9659F6A6B71B66FF64D34ED925664742205D0CA4FD7585D7FE5C9F5E3` | Inherited Qwen factorial evidence and candidate source for offline diagnostics where protocol permits | Read-only; never relabel as multi-agent coordination results |
| `granite_formal/granite33_8b_q4km_seed20260805_clean1/predictions.jsonl` | 720 rows; SHA-256 `BE433AC853F60EBC8882FDCC7BD01033BCA8868FA23B298114B0977476983E3D` | Inherited Granite factorial evidence and cross-backbone analysis | Read-only; never relabel as multi-agent coordination results |
| `statistics/` and `statistics_granite/` | Canonical manifests, recomputed rows, registered contrasts, independent audits | Reuse reported factorial estimates after manifest verification | Supports inherited factor analysis, not the new coordinator |
| `prospective_component_experiments/` | Frozen component protocol, run harness, aggregation and tests | Reuse design vocabulary and resource accounting | Keep its protocol identity; do not merge denominators with a new run |
| `semantic_reliability_experiment/` | Frozen state-generation/evaluation code, formal-v5 atomic scores and release manifests | Reuse named-state semantics and counterfactual evidence schema | Synthetic schema-valid stress states are not operator-certified grid snapshots |
| `formal_bird_runs/` | BIRD call ledgers, final scores, incidents and retained failed runs | Public-benchmark evidence and audit trail | Incident runs remain excluded; no continuation or overwrite |
| `original_title_rebuild/ma_sqlgrid_agents.py` | New deterministic coordination core | Prospective multi-agent condition only | **Unevaluated** until a new approved freeze is executed |

## Integration rules

- Inherited results retain their original run IDs, hashes, denominators and method
  labels (`Inherited`).
- A result created with this coordination core receives a new run ID and is
  labelled `New`; it cannot be pooled with inherited rows before the statistical
  analysis plan says how.
- `Diagnostic` outputs may test interfaces or failure mechanisms but are not main
  accuracy results.
- No existing prediction, score, call ledger, incident directory, manifest or
  manuscript file may be rewritten by this workspace.
- Gold SQL/result is allowed only in the offline evaluator after the blackboard is
  sealed. It is forbidden from Query Analyst, Schema Cartographer, Synthesizer,
  Validator, Counterfactual Critic and Adjudicator inputs.

