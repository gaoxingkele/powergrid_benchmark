# C2GES MiniLM ranking sensitivity

Status: post-run representation sensitivity. The production 256-token selections and metrics were reproduced before alternatives were accepted.

| K | Contrast | Changed cells | Equal-series ROUGE-L difference | Cluster-bootstrap 95% interval | Holm p |
|---:|---|---:|---:|---:|---:|
| 5 | extended_512_minus_production_256 | 0/15 | +0.00000 | [+0.00000, +0.00000] | 1.000000 |
| 5 | chunk_mean_254_minus_production_256 | 1/15 | -0.00057 | [-0.00171, +0.00000] | 1.000000 |
| 10 | extended_512_minus_production_256 | 2/15 | +0.00058 | [+0.00000, +0.00148] | 1.000000 |
| 10 | chunk_mean_254_minus_production_256 | 2/15 | +0.00012 | [-0.00044, +0.00078] | 1.000000 |

The alternatives diagnose whether the small truncated subset can change Semantic-MMR rankings. They are post-run rules on one retained corpus and do not establish a preferred long-text encoder.
