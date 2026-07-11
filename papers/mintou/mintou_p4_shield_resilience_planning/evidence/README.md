# Evidence

- `evidence/runs/synthetic_smoke_results.csv`: deterministic smoke benchmark outputs.
- `evidence/tables/synthetic_smoke_leaderboard.csv`: method-level aggregate table.
- `evidence/runs/analysis.md`: interpretation boundary and next optimization action.
- `src/configs/experiment_manifest.json`: experiment, baseline, ablation, dataset, and metric manifest.
- `evidence/runs/real_simbench_planning_results.csv`: public SimBench benchmark-derived resilience planning results.
- `evidence/tables/real_simbench_planning_leaderboard.csv`: aggregate resilience-planning leaderboard.
- `evidence/runs/real_simbench_planning_analysis.md`: current public-data result analysis.
- `evidence/runs/real_simbench_planning_analysis_v1_weak.md`: preserved first weak result before compliant scenario/repair refinement.
- `evidence/source/real_simbench_planning_source_profile.csv`: exact SimBench source profile and candidate count.

The synthetic files validate the ARA and experiment pipeline. The SimBench files are public benchmark-derived evidence with a positive SHIELD-MOEA signal, bounded by the lack of full AC/pandapower feasibility validation.
