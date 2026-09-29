# P6 S3 Matched-Effort Analysis

## Protocol

Each matched-evaluation run consumed exactly 3,200 search-evaluation units. Each matched-time run used the same 0.20-second search deadline; realized times and deadline overshoot are retained per run. Hypervolume uses only the final feasible non-dominated front.

## Scenario-balanced descriptive means

| Protocol | Method | Mean HV | Mean search runtime (s) | Mean feasibility rate |
|---|---|---:|---:|---:|
| matched_evaluation | BiLo-NSGA | 0.162766 | 0.116261 | 1.000000 |
| matched_evaluation | NSGA-II | 0.172131 | 0.197495 | 1.000000 |
| matched_evaluation | Pareto Local Search | 0.116259 | 0.259798 | 1.000000 |
| matched_time | BiLo-NSGA | 0.170979 | 0.200668 | 1.000000 |
| matched_time | NSGA-II | 0.172211 | 0.200483 | 1.000000 |
| matched_time | Pareto Local Search | 0.115926 | 0.200037 | 1.000000 |

## Declared multiplicity families

The primary family is the 16 matched-evaluation BiLo-NSGA contrasts (two comparators by eight scenarios). The matched-time protocol is a separate 16-contrast secondary family. Both use exact paired sign tests and Holm correction. Sensitivity outputs are descriptive.

| Family | Significant contrasts | Positive mean differences | Total |
|---|---:|---:|---:|
| primary_matched_evaluation_16 | 12 | 8 | 16 |
| secondary_matched_time_16 | 13 | 12 | 16 |

## Hypervolume and local-parameter sensitivity

The registered scheme's scenario/method cells have an unweighted mean HV of 0.150386; the analytic-bound reference-1.1 scheme has 0.025718. These scales are not interchangeable. The CSVs retain per-run clipping incidence and the reference-point alternatives.

The one-factor local scan retains every registered and adverse/null setting. Scenario-balanced descriptive differences from the registered cell are:

| Cell | Difference in mean HV | Relative difference (%) |
|---|---:|---:|
| bonus_1p00 | -0.000233 | -0.145 |
| bonus_1p12 | +0.000155 | +0.096 |
| depth_16 | +0.000354 | +0.220 |
| depth_2 | +0.006912 | +4.288 |
| penalty_20 | +0.000000 | +0.000 |
| penalty_5 | +0.000000 | +0.000 |
| registered | +0.000000 | +0.000 |

## Scope

The NSGA-II search is the fully specified stage-local implementation recorded in the config, not a silent substitution for the unavailable recorded pymoo 0.6.2 runtime. Wall-clock results are machine-specific. PLS evidence applies to this bounded add/delete/swap implementation. No result establishes deployment, expert agreement, calibrated economics, or electrical feasibility.
