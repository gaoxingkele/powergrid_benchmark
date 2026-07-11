# Claims

| Claim ID | Claim | Status | Proof |
|---|---|---|---|
| C1 | `BiLo-NSGA` improves budget-constrained project review quality against target-journal-level baselines on the public RTS-GMLC + SimBench + NERC-report-cache derived benchmark. | Supported for proxy benchmark v1 | E-main: `evidence/tables/real_project_review_leaderboard.csv`; proposed `1.70989680` vs AHP-TOPSIS `1.64612807` |
| C2 | Bidirectional local search contributes beyond the strongest ablation. | Supported for proxy benchmark v1 | E-ablation: `evidence/tables/real_project_review_leaderboard.csv`; strongest ablation `1.65100922` |
| C3 | The method remains feasible and ranking-stable under budget/dependency review scenarios. | Supported for proxy benchmark v1 | E-robust: `mean_feasibility_rate=1.00000000`, `mean_ranking_stability=0.87960000`, `mean_move_trace_completeness=1.00000000` |
| C4 | The experiment package is reproducible from public or benchmark-derived data. | Supported structurally | E-repro: `src/code/run_real_project_review.py`, `src/configs/real_project_review_config.json`, `evidence/source/real_project_review_source_profile.csv` |

Exact engineering-economic manuscript claims remain prohibited until expert labels, calibrated costs, and load-flow checks are added.
