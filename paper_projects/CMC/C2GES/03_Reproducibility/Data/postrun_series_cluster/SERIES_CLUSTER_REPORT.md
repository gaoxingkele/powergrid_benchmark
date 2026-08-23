# C2GES series-cluster sensitivity report

Status: post-run sensitivity analysis; not a fresh confirmatory test.

The 15 retained reports form 10 frozen `report_series_id` clusters. Each series first contributes its within-series mean delta; the series-equal estimand then assigns equal weight to the 10 series. The interval is a deterministic 10,000-draw cluster bootstrap. Exact sign flips enumerate all 1,024 series-level assignments, followed by Holm adjustment across the six contrasts.

| K | Contrast | Report-equal delta | Series-equal delta | Cluster bootstrap 95% | Exact p | Holm p | LOSO range |
|---:|---|---:|---:|---:|---:|---:|---:|
| 5 | c2ges_full_minus_graph_no_cf_strict | -0.003332 | -0.005744 | [-0.015986, 0.002230] | 0.316406 | 0.316406 | [-0.007531, -0.001415] |
| 5 | c2ges_full_minus_semantic_mmr | 0.020737 | 0.021864 | [0.015484, 0.028248] | 0.001953 | 0.011719 | [0.020085, 0.023792] |
| 5 | c2ges_full_minus_textrank | 0.025438 | 0.028557 | [0.019927, 0.038486] | 0.001953 | 0.011719 | [0.025037, 0.030877] |
| 10 | c2ges_full_minus_graph_no_cf_strict | -0.003360 | -0.004773 | [-0.010494, -0.000084] | 0.091797 | 0.183594 | [-0.005997, -0.002388] |
| 10 | c2ges_full_minus_semantic_mmr | 0.014360 | 0.014205 | [0.003626, 0.023764] | 0.031250 | 0.125000 | [0.012037, 0.017422] |
| 10 | c2ges_full_minus_textrank | 0.012029 | 0.011010 | [0.001883, 0.019764] | 0.044922 | 0.134766 | [0.008067, 0.014642] |

These values describe robustness to the recorded series clustering. They do not repair unequal output length, tuning asymmetry, extraction-unit contamination, embedding truncation, or the absence of expert semantic validation.
