# Mintou Submission Assets

This directory is the portfolio-level submission asset package for the six `mintou` ARA papers.

It does not replace each paper ARA. It indexes the current evidence, claim scope, preserved negative results, and remaining validation gaps so manuscript drafting can stay aligned with the evidence.

## Files

- `paper_asset_manifest.csv`: one-row summary for each paper.
- `evidence_index.csv`: all current evidence files under the six ARA directories.
- `claim_scope_matrix.md`: supported claim scope and boundary for each paper.
- `reviewer_readiness_checklist.md`: pre-submission checklist against reproducibility and evidence discipline.
- `remaining_validation_gaps.md`: unresolved validation items that must not be hidden.
- `experiment_strength_upgrade_plan.md`: dataset, baseline, ablation, robustness, and submission-gate upgrade plan for all six papers.
- `target_journal_experiment_dataset_comparison.md`: first-round comparison against same-theme target-journal papers on experiment quantity, experiment strength, and dataset sufficiency.

## Portfolio Snapshot

| Paper | Algorithm | Target | Signal | Evidence Files | Preserved Negative/Mixed |
|---|---|---|---|---:|---:|
| `mintou_p1` | `DSTAR-GRU` | IEEE Access | `narrow_promising_public_signal` | 20 | 6 |
| `mintou_p2` | `HyG-LoadFormer` | Electronics | `day_ahead_promising_public_signal` | 34 | 15 |
| `mintou_p3` | `CARS-MODE` | Energies | `narrow_promising_public_signal` | 21 | 12 |
| `mintou_p4` | `SHIELD-MOEA` | Energies | `promising_public_signal` | 12 | 3 |
| `mintou_p5` | `TRACE-MOEA` | IEEE Access | `promising_public_signal` | 18 | 9 |
| `mintou_p6` | `BiLo-NSGA` | Applied Sciences | `promising_public_signal` | 15 | 6 |

## Manuscript Discipline

- Claims must cite the exact evidence table or analysis file.
- Weak, mixed, marginal, and near-miss results are preserved as part of the research trace.
- Public benchmark-derived proxy results must not be rewritten as enterprise, AC-OPF, UC, or expert-labeled results.
