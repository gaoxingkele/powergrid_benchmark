# Evidence

- `evidence/runs/synthetic_smoke_results.csv`: deterministic smoke benchmark outputs.
- `evidence/tables/synthetic_smoke_leaderboard.csv`: method-level aggregate table.
- `evidence/runs/analysis.md`: interpretation boundary and next optimization action.
- `src/configs/experiment_manifest.json`: experiment, baseline, ablation, dataset, and metric manifest.
- `evidence/runs/real_rts_dispatch_results.csv`: public RTS-GMLC benchmark-derived dispatch results.
- `evidence/tables/real_rts_dispatch_leaderboard.csv`: aggregate RTS-GMLC dispatch leaderboard.
- `evidence/tables/real_rts_dispatch_stress_leaderboard.csv`: high-renewable, high-topology, ramp-stress, and renewable-ramp stress subset leaderboard.
- `evidence/tables/real_rts_dispatch_rolling_leaderboard.csv`: window-level rolling scenario leaderboard.
- `evidence/tables/real_rts_dispatch_rolling_summary.csv`: rolling scenario aggregate table.
- `evidence/runs/real_rts_dispatch_analysis.md`: current public-data result analysis.
- `evidence/runs/real_rts_dispatch_stress_analysis.md`: pressure-subset result analysis.
- `evidence/runs/real_rts_dispatch_rolling_analysis.md`: rolling scenario-window result analysis.
- `evidence/runs/real_rts_dispatch_analysis_v1_weak.md`: preserved first weak dispatch result before adaptive renewable/retrieval refinement.
- `evidence/runs/real_rts_dispatch_analysis_v2_marginal.md`: preserved marginal v2 result before stress/rolling evidence.
- `evidence/source/real_rts_dispatch_source_profile.csv`: exact RTS-GMLC source profile and evaluated scenario count.

The synthetic files validate the ARA and experiment pipeline. The RTS-GMLC files are public benchmark-derived evidence with a narrow positive DSTAR-GRU signal, bounded by the lack of full OPF/UC feasibility validation.
