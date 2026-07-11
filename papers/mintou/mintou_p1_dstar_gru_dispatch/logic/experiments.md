# Experiments

Status: all planned experiment slots are implemented as deterministic synthetic smoke tests and upgraded to RTS-GMLC fixed, rolling, and pressure-subset dispatch proxy benchmarks.

## Public Benchmark Upgrade

| Evidence ID | Experiment | Dataset | Status | Key finding |
|---|---|---|---|---|
| E-real-RTS | RTS-GMLC benchmark-derived dispatch recommendation | RTS-GMLC `gen.csv`, `branch.csv`, day-ahead load/wind/PV | public RTS dispatch v3 complete | DSTAR-GRU shows narrow fixed and rolling positive signal, with stronger value in high-renewable stress subset. |

## Main Experiments

| Experiment ID | Purpose | Evidence | Status |
|---|---|---|---|
| `nominal_dispatch` | Validate `similarity-aware load and topology constrained dispatch recommendation` under `nominal_dispatch` scenario. | `evidence/runs/real_rts_dispatch_results.csv` | public benchmark-derived |
| `opf_transfer` | Validate `similarity-aware load and topology constrained dispatch recommendation` under `opf_transfer` scenario. | Not yet available | planned OPF/UC layer |
| `load_perturbation` | Validate `similarity-aware load and topology constrained dispatch recommendation` under `load_perturbation` scenario. | `evidence/tables/real_rts_dispatch_rolling_summary.csv` | rolling proxy |
| `renewable_uncertainty` | Validate `similarity-aware load and topology constrained dispatch recommendation` under `renewable_uncertainty` scenario. | `evidence/tables/real_rts_dispatch_stress_leaderboard.csv` | high-renewable proxy |
| `topology_disturbance` | Validate `similarity-aware load and topology constrained dispatch recommendation` under `topology_disturbance` scenario. | `evidence/tables/real_rts_dispatch_stress_leaderboard.csv` | proxy tie/limitation |
| `similarity_retrieval` | Validate `similarity-aware load and topology constrained dispatch recommendation` under `similarity_retrieval` scenario. | `evidence/runs/real_rts_dispatch_results.csv` | public benchmark-derived |
| `scalability_runtime` | Validate `similarity-aware load and topology constrained dispatch recommendation` under `scalability_runtime` scenario. | `evidence/source/real_rts_dispatch_source_profile.csv` | public benchmark-derived |

## Ablation Experiments

| Ablation | Purpose | Evidence | Status |
|---|---|---|---|
| `no_siamese_branch` | Isolate the contribution removed by this variant. | `evidence/runs/synthetic_smoke_results.csv` | smoke-tested |
| `lstm_encoder` | Isolate the contribution removed by this variant. | `evidence/runs/synthetic_smoke_results.csv` | smoke-tested |
| `no_retrieval_bank` | Isolate the contribution removed by this variant. | `evidence/runs/synthetic_smoke_results.csv` | smoke-tested |
| `no_topology_features` | Isolate the contribution removed by this variant. | `evidence/runs/synthetic_smoke_results.csv` | smoke-tested |
| `single_objective_layer` | Isolate the contribution removed by this variant. | `evidence/runs/synthetic_smoke_results.csv` | smoke-tested |
| `small_reference_bank` | Isolate the contribution removed by this variant. | `evidence/runs/synthetic_smoke_results.csv` | smoke-tested |

## Metrics

- dispatch_cost_index
- constraint_violation_rate
- renewable_curtailment_rate
- retrieval_hit_rate
- topology_risk_proxy
- composite_dispatch_score
- rolling_score_std
- runtime_s

## Preserved Negative Evidence

- `evidence/runs/real_rts_dispatch_analysis_v1_weak.md`: first RTS-GMLC dispatch result was weak.
- `evidence/runs/real_rts_dispatch_analysis_v2_marginal.md`: adaptive retrieval v2 was positive but too marginal for strong claims.
- Current v3 stress evidence still shows high-topology and ramp-stress ties; these are limitations until OPF/UC or topology-control validation is added.
