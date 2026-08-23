# Balanced development tuning (equal nine configurations)

Status: development-only configuration selection for a future unseen-series experiment. The retained test was not an input and must not be re-evaluated with these choices.

| Method | Selected parameter | Grid index | Mean ROUGE-L | K=5 | K=10 | Mean redundancy |
|---|---:|---:|---:|---:|---:|---:|
| semantic_mmr | 0.9 | 8 | 0.13097 | 0.11426 | 0.14768 | 0.09179 |
| textrank | 0.65 | 2 | 0.12061 | 0.10247 | 0.13875 | 0.18280 |
| c2ges_normalized_path | 0.0 | 0 | 0.13919 | 0.12495 | 0.15343 | 0.07959 |

Each method received exactly nine configurations under one ordered objective. This closes the development-budget asymmetry for the planned future comparison, not for the historical retained-test result.
