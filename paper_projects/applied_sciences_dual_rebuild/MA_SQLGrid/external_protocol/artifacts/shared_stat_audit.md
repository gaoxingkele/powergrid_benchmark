# Experiment Artifact Audit and Paired Statistics

- Overall audit: **PASS**
- Input: `D:\aicoding\powergrid_benchmark\paper_projects\applied_sciences_dual_rebuild\MA_SQLGrid\external_protocol\artifacts\factorial_design_matrix.jsonl`
- SHA-256: `68cca8af27dcdbee2e4ad976bb2a6db06e67b4161f12f0bcf82f44f5b7db390a`
- Rows / items / clusters: 364 / 91 / 91
- Conditions: F00_Full_NoShape, F01_Full_WithShape, F10_Compact_NoShape, F11_Compact_WithShape
- Cartesian cells (observed/expected): 364/364

## Audit findings

No schema, completeness, identity, cluster, or hash defects were detected.

## Paired comparisons

| Baseline | Treatment | Metric | Pairs | Delta | Bootstrap CI | McNemar p | Holm p |
|---|---|---|---:|---:|---|---:|---:|
| F00_Full_NoShape | F01_Full_WithShape | registered_cell | 91 | 0 | [0, 0] | 1 | 1 |
| F00_Full_NoShape | F10_Compact_NoShape | registered_cell | 91 | 0 | [0, 0] | 1 | 1 |
| F00_Full_NoShape | F11_Compact_WithShape | registered_cell | 91 | 0 | [0, 0] | 1 | 1 |
| F01_Full_WithShape | F10_Compact_NoShape | registered_cell | 91 | 0 | [0, 0] | 1 | 1 |
| F01_Full_WithShape | F11_Compact_WithShape | registered_cell | 91 | 0 | [0, 0] | 1 | 1 |
| F10_Compact_NoShape | F11_Compact_WithShape | registered_cell | 91 | 0 | [0, 0] | 1 | 1 |

## Interpretation contract

Positive delta means treatment minus baseline. Confidence intervals use paired cluster resampling; McNemar is emitted only for binary paired outcomes. Holm adjustment spans all applicable pairwise metric tests in this report.
