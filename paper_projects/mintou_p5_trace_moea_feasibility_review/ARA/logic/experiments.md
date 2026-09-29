# Experiments

Status: all planned experiment slots are implemented as deterministic synthetic smoke tests and upgraded to a public benchmark-derived RTS-GMLC + SimBench + NERC-report-cache project review experiment.

## Main Experiments

| Experiment ID | Purpose | Evidence | Status |
|---|---|---|---|
| `benchmark_portfolio_optimization` | Validate `traceable feasibility review and investment effectiveness optimization` under `benchmark_portfolio_optimization` scenario. | `evidence/runs/real_project_review_results.csv` | public benchmark-derived |
| `distribution_project_review` | Validate `traceable feasibility review and investment effectiveness optimization` under `distribution_project_review` scenario. | `evidence/runs/real_project_review_results.csv` | public benchmark-derived |
| `reliability_driven_review` | Validate `traceable feasibility review and investment effectiveness optimization` under `reliability_driven_review` scenario. | `evidence/runs/real_project_review_results.csv` | public benchmark-derived |
| `renewable_accommodation_review` | Validate `traceable feasibility review and investment effectiveness optimization` under `renewable_accommodation_review` scenario. | `evidence/runs/real_project_review_results.csv` | public benchmark-derived |
| `budget_ranking_stability` | Validate `traceable feasibility review and investment effectiveness optimization` under `budget_ranking_stability` scenario. | `evidence/runs/real_project_review_results.csv` | public benchmark-derived |
| `preference_aware_support` | Validate `traceable feasibility review and investment effectiveness optimization` under `preference_aware_support` scenario. | `evidence/runs/real_project_review_results.csv` | public benchmark-derived |
| `traceability_evaluation` | Validate `traceable feasibility review and investment effectiveness optimization` under `traceability_evaluation` scenario. | `evidence/runs/real_project_review_results.csv` | public benchmark-derived |

## Ablation Experiments

| Ablation | Purpose | Evidence | Status |
|---|---|---|---|
| `no_feasibility_repair` | Isolate the contribution removed by this variant. | `evidence/runs/real_project_review_results.csv` | public benchmark-derived |
| `no_preference_ranking` | Isolate the contribution removed by this variant. | `evidence/runs/real_project_review_results.csv` | public benchmark-derived |
| `no_reliability_features` | Isolate the contribution removed by this variant. | `evidence/runs/real_project_review_results.csv` | public benchmark-derived |
| `no_renewable_features` | Isolate the contribution removed by this variant. | `evidence/runs/real_project_review_results.csv` | public benchmark-derived |
| `no_schedule_risk` | Isolate the contribution removed by this variant. | `evidence/runs/real_project_review_results.csv` | public benchmark-derived |
| `single_weighted_objective` | Isolate the contribution removed by this variant. | `evidence/runs/real_project_review_results.csv` | public benchmark-derived |
| `nsga2_only` | Isolate the contribution removed by this variant. | `evidence/runs/real_project_review_results.csv` | public benchmark-derived |
| `small_project_pool` | Isolate the contribution removed by this variant. | `evidence/runs/real_project_review_results.csv` | public benchmark-derived |

## Metrics

- hypervolume
- budget_feasibility_rate
- ranking_stability
- trace_completeness
- runtime_s

## Preserved Negative Evidence

- `evidence/runs/real_project_review_analysis_v1_weak.md`: random-feasible size bias exposed a weak metric design.
- `evidence/runs/real_project_review_analysis_v2_weak.md`: budget-aware selection improved but remained weak.
- `evidence/runs/real_project_review_analysis_v3_near_miss.md`: TRACE-MOEA trailed AHP-TOPSIS by `0.12%` before trace-review metric weighting was aligned with the task.
