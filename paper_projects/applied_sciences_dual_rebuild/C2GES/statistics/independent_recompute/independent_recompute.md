# C2GES Independent Five-Seed Recompute

The official aggregate was excluded from all calculations and opened only for the final cell-by-cell comparison.

- Diff status: **PASS** (1060/1060 comparable cells matched; max numeric difference `3.2e-13`).
- Hard artifact/row/resource failures: **0**.
- Successful resource runs: **15/15**.

## Recomputed full evidence F1

| Protocol | K=1 | K=3 | K=5 | K=10 |
|---|---:|---:|---:|---:|
| oracle-label | 0.670505 +/- 0.004950 | 0.492617 +/- 0.001495 | 0.416041 +/- 0.000942 | 0.356277 +/- 0.000101 |
| predicted-label | 0.668751 +/- 0.005052 | 0.492017 +/- 0.002128 | 0.414963 +/- 0.000738 | 0.356300 +/- 0.000239 |
| label-blind | 0.667699 +/- 0.002095 | 0.491046 +/- 0.002062 | 0.415429 +/- 0.000555 | 0.356046 +/- 0.000301 |

## Recomputed BM25 F1

| Protocol | K=1 | K=3 | K=5 | K=10 |
|---|---:|---:|---:|---:|
| oracle-label | 0.699363 | 0.486402 | 0.410906 | 0.352958 |
| predicted-label | 0.699363 | 0.486402 | 0.410906 | 0.352958 |
| label-blind | 0.699363 | 0.486402 | 0.410906 | 0.352958 |

## Failure counts

| Check | Count |
|---|---:|
| `cross_protocol_alignment_failures` | 0 |
| `duplicate_prediction_keys` | 0 |
| `incomplete_mode_k_cells` | 0 |
| `invalid_metric_values` | 0 |
| `malformed_json` | 0 |
| `missing_required_fields` | 0 |
| `nonidentical_bm25_cells` | 0 |
| `resource_run_failures` | 0 |
| `summary_f1_mismatches` | 0 |
| `summary_protocol_mismatch` | 0 |
| `unexpected_mode_or_k` | 0 |
| `unexpected_prediction_row_count` | 0 |
| `hard_failure_total` | 0 |
| `successful_resource_runs` | 15 |
| `expected_resource_runs` | 15 |

## Reproducibility

Input file hashes are embedded in `independent_recompute.json`; every compared leaf is recorded in `diff.json`.
