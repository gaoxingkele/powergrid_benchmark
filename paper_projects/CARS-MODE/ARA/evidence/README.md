# Evidence

- `evidence/runs/synthetic_smoke_results.csv`: deterministic smoke benchmark outputs.
- `evidence/tables/synthetic_smoke_leaderboard.csv`: method-level aggregate table.
- `evidence/runs/analysis.md`: interpretation boundary and next optimization action.
- `src/configs/experiment_manifest.json`: experiment, baseline, ablation, dataset, and metric manifest.
- `evidence/runs/real_simbench_planning_results.csv`: public SimBench benchmark-derived planning results.
- `evidence/tables/real_simbench_planning_leaderboard.csv`: aggregate planning leaderboard.
- `evidence/runs/real_simbench_planning_analysis.md`: current public-data limitation analysis.
- `evidence/runs/real_simbench_planning_analysis_v1_weak.md`: preserved first weak planning result before compliant repair revision.
- `evidence/runs/real_simbench_planning_analysis_v2_weak.md`: preserved second weak planning result before NoDER ablation correction.
- `evidence/runs/real_simbench_planning_analysis_v3_weak.md`: preserved weak result before DER/storage stress redesign.
- `evidence/runs/real_simbench_planning_analysis_v4_near_miss.md`: preserved near-miss result where CARS-MODE beat baselines but not NoDiversity.
- `evidence/source/real_simbench_planning_source_profile.csv`: exact SimBench source profile and candidate count.

The synthetic files validate the ARA and experiment pipeline. The SimBench files are public benchmark-derived evidence. Current CARS-MODE performance is a narrow proxy-level positive signal and must not be overstated as an AC-feasible engineering planning result.
