# Experiments

Status: all planned experiment slots are implemented as deterministic synthetic smoke tests and upgraded to a public benchmark-derived RTS-GMLC + SimBench + NERC-report-cache project review experiment.

## Main Experiments

| Experiment ID | Purpose | Evidence | Status |
|---|---|---|---|
| `budget_constrained_selection` | Validate `budget-constrained power grid project review and portfolio ranking` under `budget_constrained_selection` scenario. | `evidence/runs/real_project_review_results.csv` | public benchmark-derived |
| `reliability_prioritized_review` | Validate `budget-constrained power grid project review and portfolio ranking` under `reliability_prioritized_review` scenario. | `evidence/runs/real_project_review_results.csv` | public benchmark-derived |
| `renewable_accommodation_review` | Validate `budget-constrained power grid project review and portfolio ranking` under `renewable_accommodation_review` scenario. | `evidence/runs/real_project_review_results.csv` | public benchmark-derived |
| `dependency_constrained_review` | Validate `budget-constrained power grid project review and portfolio ranking` under `dependency_constrained_review` scenario. | `evidence/runs/real_project_review_results.csv` | public benchmark-derived |
| `local_move_explainability` | Validate `budget-constrained power grid project review and portfolio ranking` under `local_move_explainability` scenario. | `evidence/runs/real_project_review_results.csv` | public benchmark-derived |
| `ranking_robustness` | Validate `budget-constrained power grid project review and portfolio ranking` under `ranking_robustness` scenario. | `evidence/runs/real_project_review_results.csv` | public benchmark-derived |
| `budget_sensitivity` | Validate `budget-constrained power grid project review and portfolio ranking` under `budget_sensitivity` scenario. | `evidence/runs/real_project_review_results.csv` | public benchmark-derived |
| `project_pool_scalability` | Validate `budget-constrained power grid project review and portfolio ranking` under `project_pool_scalability` scenario. | `evidence/runs/real_project_review_results.csv` | public benchmark-derived |

## Ablation Experiments

| Ablation | Purpose | Evidence | Status |
|---|---|---|---|
| `no_forward_search` | Isolate the contribution removed by this variant. | `evidence/runs/real_project_review_results.csv` | public benchmark-derived |
| `no_backward_search` | Isolate the contribution removed by this variant. | `evidence/runs/real_project_review_results.csv` | public benchmark-derived |
| `random_mutation_only` | Isolate the contribution removed by this variant. | `evidence/runs/real_project_review_results.csv` | public benchmark-derived |
| `no_dependency_moves` | Isolate the contribution removed by this variant. | `evidence/runs/real_project_review_results.csv` | public benchmark-derived |
| `no_feasibility_recovery` | Isolate the contribution removed by this variant. | `evidence/runs/real_project_review_results.csv` | public benchmark-derived |
| `weighted_ranking_only` | Isolate the contribution removed by this variant. | `evidence/runs/real_project_review_results.csv` | public benchmark-derived |
| `shallow_local_search` | Isolate the contribution removed by this variant. | `evidence/runs/real_project_review_results.csv` | public benchmark-derived |
| `low_dependency_density` | Isolate the contribution removed by this variant. | `evidence/runs/real_project_review_results.csv` | public benchmark-derived |
| `loose_budget` | Isolate the contribution removed by this variant. | `evidence/runs/real_project_review_results.csv` | public benchmark-derived |

## Metrics

- hypervolume
- feasibility_rate
- ranking_stability
- move_trace_completeness
- runtime_s

## Preserved Negative Evidence

- `evidence/runs/real_project_review_analysis_v1_weak.md`: random-feasible size bias exposed a weak metric design.
- `evidence/runs/real_project_review_analysis_v2_weak.md`: budget-aware selection improved but remained weak before task-quality aggregation was corrected.
