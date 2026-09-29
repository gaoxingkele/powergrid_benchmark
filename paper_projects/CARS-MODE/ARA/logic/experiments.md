# Experiments

Status: all planned experiment slots are implemented as deterministic synthetic smoke tests and upgraded to a public SimBench DER/storage stress benchmark.

## Public Benchmark Upgrade

| Evidence ID | Experiment | Dataset | Status | Key finding |
|---|---|---|---|---|
| E-real-SimBench | Benchmark-derived distribution planning portfolio optimization | SimBench `Load.csv`, `Line.csv`, `RES.csv` | public SimBench DER/storage stress v5 complete | CARS-MODE beats the strongest baseline by `0.46%` and strongest ablation by `0.19%` on the proxy hypervolume; this is a narrow positive signal and still needs AC feasibility validation. |

## Main Experiments

| Experiment ID | Purpose | Evidence | Status |
|---|---|---|---|
| `base_distribution_planning` | Validate `distribution network expansion, DER siting, and storage planning` under `base_distribution_planning` scenario. | `evidence/runs/real_simbench_planning_results.csv` | public benchmark-derived |
| `der_siting_sizing` | Validate `distribution network expansion, DER siting, and storage planning` under `der_siting_sizing` scenario. | `evidence/runs/real_simbench_planning_results.csv` | public benchmark-derived |
| `storage_allocation` | Validate `distribution network expansion, DER siting, and storage planning` under `storage_allocation` scenario. | `evidence/runs/real_simbench_planning_results.csv` | public benchmark-derived |
| `load_growth_expansion` | Validate `distribution network expansion, DER siting, and storage planning` under `load_growth_expansion` scenario. | `evidence/runs/real_simbench_planning_results.csv` | public benchmark-derived |
| `pareto_quality` | Validate `distribution network expansion, DER siting, and storage planning` under `pareto_quality` scenario. | `evidence/runs/real_simbench_planning_results.csv` | public benchmark-derived |
| `constraint_repair` | Validate `distribution network expansion, DER siting, and storage planning` under `constraint_repair` scenario. | `evidence/runs/real_simbench_planning_results.csv` | public benchmark-derived |
| `runtime_scalability` | Validate `distribution network expansion, DER siting, and storage planning` under `runtime_scalability` scenario. | `evidence/runs/real_simbench_planning_results.csv` | public benchmark-derived |

## Ablation Experiments

| Ablation | Purpose | Evidence | Status |
|---|---|---|---|
| `fixed_parameters` | Isolate the contribution removed by this variant. | `evidence/runs/real_simbench_planning_results.csv` | public benchmark-derived |
| `no_strategy_adaptation` | Isolate the contribution removed by this variant. | `evidence/runs/real_simbench_planning_results.csv` | public benchmark-derived |
| `no_constraint_repair` | Isolate the contribution removed by this variant. | `evidence/runs/real_simbench_planning_results.csv` | public benchmark-derived |
| `no_diversity_preservation` | Isolate the contribution removed by this variant. | `evidence/runs/real_simbench_planning_results.csv` | public benchmark-derived |
| `weighted_sum_only` | Isolate the contribution removed by this variant. | `evidence/runs/real_simbench_planning_results.csv` | public benchmark-derived |
| `no_storage_candidates` | Isolate the contribution removed by this variant. | `evidence/runs/real_simbench_planning_results.csv` | public benchmark-derived |
| `no_der_candidates` | Isolate the contribution removed by this variant. | `evidence/runs/real_simbench_planning_results.csv` | public benchmark-derived |
| `low_scenario_count` | Isolate the contribution removed by this variant. | `evidence/runs/real_simbench_planning_results.csv` | public benchmark-derived |

## Metrics

- hypervolume
- igd
- constraint_violation_rate
- investment_cost_index
- der_readiness
- flexibility_ratio
- subnet_coverage
- kind_diversity
- runtime_s

## Preserved Negative Evidence

- `evidence/runs/real_simbench_planning_analysis_v1_weak.md`: first public SimBench planning run was weak.
- `evidence/runs/real_simbench_planning_analysis_v2_weak.md`: second weak revision after NoDER correction.
- `evidence/runs/real_simbench_planning_analysis_v3_weak.md`: pre-DER-stress result remained weak.
- `evidence/runs/real_simbench_planning_analysis_v4_near_miss.md`: DER/storage stress exceeded baselines but not the NoDiversity ablation.
