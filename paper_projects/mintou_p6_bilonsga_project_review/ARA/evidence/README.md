# Evidence

- `evidence/runs/synthetic_smoke_results.csv`: deterministic smoke benchmark outputs.
- `evidence/tables/synthetic_smoke_leaderboard.csv`: method-level aggregate table.
- `evidence/runs/analysis.md`: interpretation boundary and next optimization action.
- `src/configs/experiment_manifest.json`: experiment, baseline, ablation, dataset, and metric manifest.

These files validate the ARA and experiment pipeline. They do not yet constitute final public benchmark results.

## Public Benchmark-Derived Evidence

- `evidence/runs/real_project_review_results.csv`: RTS-GMLC + SimBench + NERC-report-cache derived project review runs.
- `evidence/tables/real_project_review_leaderboard.csv`: method-level aggregate table for BiLo-NSGA, baselines, and ablations.
- `evidence/runs/real_project_review_analysis.md`: current interpretation boundary and value signal.
- `evidence/source/real_project_review_source_profile.csv`: source mix and candidate-pool profile.
- `src/configs/real_project_review_config.json`: data sources, methods, experiments, and repeat count.
- `src/configs/real_project_review_methods.json`: method manifest for the public benchmark-derived run.
- `evidence/runs/*_v1_weak.*`, `*_v2_weak.*`: preserved negative revisions.

Current value signal: promising proxy-level public signal, with BiLo-NSGA exceeding the strongest baseline by `3.87%` and strongest ablation by `3.57%`.
