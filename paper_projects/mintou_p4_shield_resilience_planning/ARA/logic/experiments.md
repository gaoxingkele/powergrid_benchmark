# Experiments

Status: all planned experiment slots are implemented as deterministic synthetic smoke tests and upgraded to a public SimBench resilience-planning proxy benchmark.

## Public Benchmark Upgrade

| Evidence ID | Experiment | Dataset | Status | Key finding |
|---|---|---|---|---|
| E-real-SimBench | Benchmark-derived resilience-oriented distribution planning | SimBench `Load.csv`, `Line.csv`, `RES.csv` | public SimBench planning v2 complete | SHIELD-MOEA improves the hypervolume proxy over the strongest baseline and ablation, while still requiring full AC/pandapower feasibility validation. |

## Main Experiments

| Experiment ID | Purpose | Evidence | Status |
|---|---|---|---|
| `deterministic_vs_scenario` | Validate `resilience-oriented distribution planning under DER, load, and outage scenarios` under `deterministic_vs_scenario` scenario. | `evidence/runs/real_simbench_planning_results.csv` | public benchmark-derived |
| `der_uncertainty` | Validate `resilience-oriented distribution planning under DER, load, and outage scenarios` under `der_uncertainty` scenario. | `evidence/runs/real_simbench_planning_results.csv` | public benchmark-derived |
| `load_uncertainty` | Validate `resilience-oriented distribution planning under DER, load, and outage scenarios` under `load_uncertainty` scenario. | `evidence/runs/real_simbench_planning_results.csv` | public benchmark-derived |
| `outage_contingency` | Validate `resilience-oriented distribution planning under DER, load, and outage scenarios` under `outage_contingency` scenario. | `evidence/runs/real_simbench_planning_results.csv` | public benchmark-derived |
| `restoration_aware_evaluation` | Validate `resilience-oriented distribution planning under DER, load, and outage scenarios` under `restoration_aware_evaluation` scenario. | `evidence/runs/real_simbench_planning_results.csv` | public benchmark-derived |
| `scenario_screening_efficiency` | Validate `resilience-oriented distribution planning under DER, load, and outage scenarios` under `scenario_screening_efficiency` scenario. | `evidence/runs/real_simbench_planning_results.csv` | public benchmark-derived |
| `pareto_quality` | Validate `resilience-oriented distribution planning under DER, load, and outage scenarios` under `pareto_quality` scenario. | `evidence/runs/real_simbench_planning_results.csv` | public benchmark-derived |
| `unseen_stress_generalization` | Validate `resilience-oriented distribution planning under DER, load, and outage scenarios` under `unseen_stress_generalization` scenario. | `evidence/runs/real_simbench_planning_results.csv` | public benchmark-derived |

## Ablation Experiments

| Ablation | Purpose | Evidence | Status |
|---|---|---|---|
| `no_scenario_screening` | Isolate the contribution removed by this variant. | `evidence/runs/real_simbench_planning_results.csv` | public benchmark-derived |
| `no_local_repair` | Isolate the contribution removed by this variant. | `evidence/runs/real_simbench_planning_results.csv` | public benchmark-derived |
| `no_resilience_objective` | Isolate the contribution removed by this variant. | `evidence/runs/real_simbench_planning_results.csv` | public benchmark-derived |
| `no_der_uncertainty` | Isolate the contribution removed by this variant. | `evidence/runs/real_simbench_planning_results.csv` | public benchmark-derived |
| `no_outage_uncertainty` | Isolate the contribution removed by this variant. | `evidence/runs/real_simbench_planning_results.csv` | public benchmark-derived |
| `low_scenario_count` | Isolate the contribution removed by this variant. | `evidence/runs/real_simbench_planning_results.csv` | public benchmark-derived |
| `weighted_sum_only` | Isolate the contribution removed by this variant. | `evidence/runs/real_simbench_planning_results.csv` | public benchmark-derived |

## Metrics

- hypervolume
- survivability_rate
- voltage_violation_probability
- expected_loss_index
- runtime_s
