# Experiments

Status: all planned experiment slots are implemented as deterministic synthetic smoke tests and upgraded to public OPSD/SimBench fixed-split plus rolling-split benchmarks.

## Public Benchmark Upgrade

| Evidence ID | Experiment | Dataset | Status | Key finding |
|---|---|---|---|---|
| E-real-OPSD | Real multi-country load forecasting with 1h and 24h horizons | OPSD `time_series_60min_singleindex.csv` | public-data benchmark v4 complete | HyG-LoadFormer shows fixed and rolling 24h/day-ahead signal; 1h remains weaker than the no-calendar ablation. |
| E-real-SimBench | Real feeder/profile-level load forecasting with hourly aggregation and 1h/24h horizons | SimBench `LoadProfile.csv` | public-data benchmark v3 complete | HyG-LoadFormer shows fixed and rolling 24h normalized-MAE signal, while SimBench MAPE and 1h results remain limitations. |
| E-rolling | Rolling temporal split stability check | OPSD and SimBench | rolling split complete | OPSD 24h rolling MAPE improves over best baseline by `39.16%`; SimBench 24h rolling normalized MAE improves by `5.15%`. |

## Main Experiments

| Experiment ID | Purpose | Evidence | Status |
|---|---|---|---|
| `one_step_forecast` | Validate `hierarchical short-term and day-ahead power load forecasting` under `one_step_forecast` scenario. | `evidence/runs/real_opsd_forecasting_results.csv`; `evidence/runs/real_simbench_forecasting_results.csv` | public benchmark-derived limitation |
| `multi_step_forecast` | Validate `hierarchical short-term and day-ahead power load forecasting` under `multi_step_forecast` scenario. | `evidence/runs/real_opsd_forecasting_results.csv`; `evidence/runs/real_simbench_forecasting_results.csv` | public benchmark-derived |
| `day_ahead_forecast` | Validate `hierarchical short-term and day-ahead power load forecasting` under `day_ahead_forecast` scenario. | `evidence/runs/real_opsd_rolling_results.csv`; `evidence/runs/real_simbench_rolling_results.csv` | public benchmark-derived positive |
| `feeder_profile_forecast` | Validate `hierarchical short-term and day-ahead power load forecasting` under `feeder_profile_forecast` scenario. | `evidence/runs/real_simbench_forecasting_results.csv`; `evidence/runs/real_simbench_rolling_results.csv` | public benchmark-derived mixed |
| `cross_region_transfer` | Validate `hierarchical short-term and day-ahead power load forecasting` under `cross_region_transfer` scenario. | `evidence/runs/synthetic_smoke_results.csv` | smoke-tested |
| `missing_node_robustness` | Validate `hierarchical short-term and day-ahead power load forecasting` under `missing_node_robustness` scenario. | `evidence/runs/synthetic_smoke_results.csv` | smoke-tested |
| `weather_aware_extension` | Validate `hierarchical short-term and day-ahead power load forecasting` under `weather_aware_extension` scenario. | `evidence/runs/synthetic_smoke_results.csv` | smoke-tested |
| `dispatch_sensitivity` | Validate `hierarchical short-term and day-ahead power load forecasting` under `dispatch_sensitivity` scenario. | `evidence/runs/synthetic_smoke_results.csv` | smoke-tested |

## Ablation Experiments

| Ablation | Purpose | Evidence | Status |
|---|---|---|---|
| `euclidean_gcn` | Isolate the contribution removed by this variant. | `evidence/runs/synthetic_smoke_results.csv` | smoke-tested |
| `fixed_curvature` | Isolate the contribution removed by this variant. | `evidence/runs/synthetic_smoke_results.csv` | smoke-tested |
| `temporal_only` | Isolate the contribution removed by this variant. | `evidence/runs/synthetic_smoke_results.csv` | smoke-tested |
| `no_weather_features` | Isolate the contribution removed by this variant. | `evidence/runs/synthetic_smoke_results.csv` | smoke-tested |
| `physical_edges_only` | Isolate the contribution removed by this variant. | `evidence/runs/synthetic_smoke_results.csv` | smoke-tested |
| `poincare_only` | Isolate the contribution removed by this variant. | `evidence/runs/synthetic_smoke_results.csv` | smoke-tested |
| `short_horizon_only` | Isolate the contribution removed by this variant. | `evidence/runs/synthetic_smoke_results.csv` | smoke-tested |

## Metrics

- mae
- rmse
- mape
- peak_load_error
- normalized_mae
- smape
- rolling_split_std
- spatial_transfer_error
- runtime_s

## Preserved Negative Evidence

- `evidence/runs/real_opsd_analysis_v1_weak.md`: first OPSD weak result before residual refinement.
- `evidence/runs/real_opsd_analysis_v2_mixed.md`: OPSD v2 mixed result before rolling split evidence.
- `evidence/runs/real_opsd_analysis_v3_gate_mixed.md`: validation gate harmed OPSD 1h/fixed split and was rejected.
- `evidence/runs/real_simbench_analysis_v1_mixed.md`: first SimBench mixed result.
- `evidence/runs/real_simbench_analysis_v2_gate_mixed.md`: global gate harmed SimBench 24h normalized-MAE signal and was rejected.
