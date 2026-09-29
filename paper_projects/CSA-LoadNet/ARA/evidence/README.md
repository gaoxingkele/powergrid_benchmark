# Evidence

- `evidence/runs/synthetic_smoke_results.csv`: deterministic smoke benchmark outputs.
- `evidence/tables/synthetic_smoke_leaderboard.csv`: method-level aggregate table.
- `evidence/runs/analysis.md`: interpretation boundary and next optimization action.
- `src/configs/experiment_manifest.json`: experiment, baseline, ablation, dataset, and metric manifest.
- `evidence/runs/real_opsd_forecasting_results.csv`: public OPSD load-forecasting benchmark v4.
- `evidence/tables/real_opsd_leaderboard.csv`: OPSD leaderboard for 1h and 24h horizons.
- `evidence/runs/real_opsd_analysis.md`: public-data result analysis and limitation statement.
- `evidence/runs/real_opsd_analysis_v1_weak.md`: preserved weak v1 result before compliant residual-seasonal refinement.
- `evidence/runs/real_opsd_analysis_v2_mixed.md`: preserved mixed v2 result before rolling evidence.
- `evidence/runs/real_opsd_analysis_v3_gate_mixed.md`: preserved rejected global validation-gate revision.
- `evidence/runs/real_opsd_rolling_results.csv`: rolling temporal split OPSD results.
- `evidence/tables/real_opsd_rolling_leaderboard.csv`: rolling OPSD aggregate table.
- `evidence/runs/real_opsd_rolling_analysis.md`: rolling OPSD stability analysis.
- `evidence/source/real_opsd_source_profile.csv`: exact OPSD source profile and train/test boundary.
- `evidence/runs/real_simbench_forecasting_results.csv`: public SimBench feeder/profile benchmark.
- `evidence/tables/real_simbench_leaderboard.csv`: SimBench leaderboard for 1h and 24h horizons.
- `evidence/runs/real_simbench_analysis.md`: SimBench result analysis with MAPE and normalized-MAE boundary.
- `evidence/runs/real_simbench_analysis_v1_mixed.md`: preserved first mixed SimBench result.
- `evidence/runs/real_simbench_analysis_v2_gate_mixed.md`: preserved rejected global gate revision.
- `evidence/runs/real_simbench_rolling_results.csv`: rolling temporal split SimBench results.
- `evidence/tables/real_simbench_rolling_leaderboard.csv`: rolling SimBench aggregate table.
- `evidence/runs/real_simbench_rolling_analysis.md`: rolling SimBench stability analysis.
- `evidence/source/real_simbench_source_profile.csv`: exact SimBench source profile and train/test boundary.

The synthetic files validate the ARA and experiment pipeline. The OPSD and SimBench files are public-data benchmark evidence, but current manuscript claims must be limited to observed 24h/day-ahead signals and must acknowledge the weak 1h results and SimBench MAPE limitation.
