# Experiment Artifact Audit and Paired Statistics

- Overall audit: **PASS**
- Input: `D:\aicoding\powergrid_benchmark\paper_projects\applied_sciences_dual_rebuild\MA_SQLGrid\statistics_granite\granite_canonical_recomputed_rows.jsonl`
- SHA-256: `f6dfe9eb975cf5a9f08964c4aaa12df39bfe154bc752999c474c5dec1b998955`
- Rows / items / clusters: 720 / 180 / 70
- Conditions: F00_Full_NoShape, F01_Full_WithShape, F10_Compact_NoShape, F11_Compact_WithShape
- Cartesian cells (observed/expected): 720/720

## Audit findings

No schema, completeness, identity, cluster, or hash defects were detected.

## Paired comparisons

| Baseline | Treatment | Metric | Pairs | Delta | Bootstrap CI | McNemar p | Holm p |
|---|---|---|---:|---:|---|---:|---:|
| F00_Full_NoShape | F01_Full_WithShape | correct_int | 180 | 0.127778 | [-0.101852, 0.362255] | 0.00444402 | 0.0222201 |
| F00_Full_NoShape | F01_Full_WithShape | shape_int | 180 | 0.422222 | [0.238806, 0.629413] | 3.80354e-20 | 3.80354e-19 |
| F00_Full_NoShape | F10_Compact_NoShape | correct_int | 180 | -0.0166667 | [-0.0791367, 0.030889] | 0.607239 | 1 |
| F00_Full_NoShape | F10_Compact_NoShape | shape_int | 180 | -0.0166667 | [-0.0903226, 0.0507256] | 0.647606 | 1 |
| F00_Full_NoShape | F11_Compact_WithShape | correct_int | 180 | 0.172222 | [0.0151496, 0.355031] | 9.26355e-06 | 6.48448e-05 |
| F00_Full_NoShape | F11_Compact_WithShape | shape_int | 180 | 0.466667 | [0.252475, 0.672001] | 2.5313e-23 | 3.03756e-22 |
| F01_Full_WithShape | F10_Compact_NoShape | correct_int | 180 | -0.144444 | [-0.39151, 0.0813443] | 0.00185823 | 0.0111494 |
| F01_Full_WithShape | F10_Compact_NoShape | shape_int | 180 | -0.438889 | [-0.64, -0.258331] | 5.78273e-19 | 5.20445e-18 |
| F01_Full_WithShape | F11_Compact_WithShape | correct_int | 180 | 0.0444444 | [-0.0656934, 0.170986] | 0.200488 | 0.67455 |
| F01_Full_WithShape | F11_Compact_WithShape | shape_int | 180 | 0.0444444 | [-0.0632911, 0.173913] | 0.168638 | 0.67455 |
| F10_Compact_NoShape | F11_Compact_WithShape | correct_int | 180 | 0.188889 | [0.0378353, 0.382225] | 3.1028e-07 | 2.48224e-06 |
| F10_Compact_NoShape | F11_Compact_WithShape | shape_int | 180 | 0.483333 | [0.277416, 0.681376] | 1.67946e-22 | 1.84741e-21 |

## Interpretation contract

Positive delta means treatment minus baseline. Confidence intervals use paired cluster resampling; McNemar is emitted only for binary paired outcomes. Holm adjustment spans all applicable pairwise metric tests in this report.
