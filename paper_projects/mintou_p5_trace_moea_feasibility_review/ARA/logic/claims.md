# Claims

| Claim ID | Claim | Status | Proof |
|---|---|---|---|
| C1 | `TRACE-MOEA` improves traceable feasibility-review portfolio quality against target-journal-level baselines on the public RTS-GMLC + SimBench + NERC-report-cache derived benchmark. | Supported for proxy benchmark v1 | E-main: `evidence/tables/real_project_review_leaderboard.csv`; proposed `1.74461503` vs AHP-TOPSIS `1.72349050` |
| C2 | The trace-aware coevolutionary components contribute beyond the strongest ablation. | Supported for proxy benchmark v1 | E-ablation: `evidence/tables/real_project_review_leaderboard.csv`; strongest ablation `1.68212661` |
| C3 | The method remains feasible and stable under review scenarios. | Supported for proxy benchmark v1 | E-robust: `mean_budget_feasibility_rate=1.00000000`, `mean_ranking_stability=0.89220000` |
| C4 | The experiment package is reproducible from public or benchmark-derived data. | Supported structurally | E-repro: `src/code/run_real_project_review.py`, `src/configs/real_project_review_config.json`, `evidence/source/real_project_review_source_profile.csv` |

Exact engineering-economic manuscript claims remain prohibited until expert labels, calibrated costs, and load-flow checks are added.
