# Experiment Artifact Audit and Paired Statistics

- Overall audit: **PASS**
- Input: `D:\aicoding\powergrid_benchmark\paper_projects\applied_sciences_dual_rebuild\MA_SQLGrid\statistics\canonical_recomputed_rows.jsonl`
- SHA-256: `df7ef2bb6990fda50d1e0ba69a1bdcaeab08ffc47c01423afe750044333f027f`
- Rows / items / clusters: 720 / 180 / 70
- Conditions: F00_Full_NoShape, F01_Full_WithShape, F10_Compact_NoShape, F11_Compact_WithShape
- Cartesian cells (observed/expected): 720/720

## Audit findings

No schema, completeness, identity, cluster, or hash defects were detected.

## Paired comparisons

| Baseline | Treatment | Metric | Pairs | Delta | Bootstrap CI | McNemar p | Holm p |
|---|---|---|---:|---:|---|---:|---:|
| F00_Full_NoShape | F01_Full_WithShape | correct_int | 180 | 0.294444 | [0.131817, 0.490198] | 1.18933e-13 | 9.51461e-13 |
| F00_Full_NoShape | F01_Full_WithShape | shape_int | 180 | 0.466667 | [0.232255, 0.671002] | 2.5313e-23 | 2.5313e-22 |
| F00_Full_NoShape | F10_Compact_NoShape | correct_int | 180 | 0.0111111 | [-0.00970874, 0.0373134] | 0.625 | 1 |
| F00_Full_NoShape | F10_Compact_NoShape | shape_int | 180 | -0.0611111 | [-0.170456, 0.00584795] | 0.0127258 | 0.0381775 |
| F00_Full_NoShape | F11_Compact_WithShape | correct_int | 180 | 0.177778 | [-0.0318471, 0.403634] | 4.2237e-05 | 0.000253422 |
| F00_Full_NoShape | F11_Compact_WithShape | shape_int | 180 | 0.461111 | [0.21965, 0.666667] | 3.79889e-22 | 3.419e-21 |
| F01_Full_WithShape | F10_Compact_NoShape | correct_int | 180 | -0.283333 | [-0.476197, -0.125628] | 4.29018e-13 | 3.00313e-12 |
| F01_Full_WithShape | F10_Compact_NoShape | shape_int | 180 | -0.527778 | [-0.722222, -0.30303] | 1.56226e-26 | 1.87471e-25 |
| F01_Full_WithShape | F11_Compact_WithShape | correct_int | 180 | -0.116667 | [-0.234513, -0.0197044] | 0.000103716 | 0.000414863 |
| F01_Full_WithShape | F11_Compact_WithShape | shape_int | 180 | -0.00555556 | [-0.0340909, 0.0193564] | 1 | 1 |
| F10_Compact_NoShape | F11_Compact_WithShape | correct_int | 180 | 0.166667 | [-0.04, 0.387643] | 7.33322e-05 | 0.000366661 |
| F10_Compact_NoShape | F11_Compact_WithShape | shape_int | 180 | 0.522222 | [0.29746, 0.715056] | 3.06204e-26 | 3.36825e-25 |

## Interpretation contract

Positive delta means treatment minus baseline. Confidence intervals use paired cluster resampling; McNemar is emitted only for binary paired outcomes. Holm adjustment spans all applicable pairwise metric tests in this report.
