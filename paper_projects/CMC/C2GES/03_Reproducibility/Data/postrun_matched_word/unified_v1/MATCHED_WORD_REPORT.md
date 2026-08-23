# C2GES matched-word-budget sensitivity

Status: post-run sensitivity; the retained test outcomes were already visible. Budgets were mechanically derived from development candidate lengths, and no text was truncated after selection.

| Budget | Contrast | Equal-series difference | Cluster-bootstrap 95% interval | Exact series p | Holm p |
|---:|---|---:|---:|---:|---:|
| 110 | c2ges_full_minus_graph_no_cf_strict | +0.0020 | [-0.0002, +0.0041] | 0.132812 | 0.796875 |
| 110 | c2ges_full_minus_semantic_mmr | +0.0019 | [-0.0034, +0.0079] | 0.560547 | 1.000000 |
| 110 | c2ges_full_minus_textrank | -0.0008 | [-0.0066, +0.0046] | 0.750000 | 1.000000 |
| 260 | c2ges_full_minus_graph_no_cf_strict | -0.0015 | [-0.0072, +0.0021] | 0.964844 | 1.000000 |
| 260 | c2ges_full_minus_semantic_mmr | +0.0062 | [-0.0006, +0.0142] | 0.156250 | 0.796875 |
| 260 | c2ges_full_minus_textrank | +0.0001 | [-0.0065, +0.0059] | 0.978516 | 1.000000 |

The audit constrains complete sentences within the frozen top-10 rankings. It does not search lower-ranked candidates, retune a method, or provide unseen-series confirmation.
