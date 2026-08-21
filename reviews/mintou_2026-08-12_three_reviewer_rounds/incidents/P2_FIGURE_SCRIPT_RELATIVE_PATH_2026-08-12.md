# P2 figure-script relative-path incident

- Date: 2026-08-12 (Asia/Shanghai)
- Command: `python paper_projects/mintou_p2_hygraph_load_forecasting/manuscript/figures/make_figures.py`
- Failure: the script resolved the repository root as `paper_projects`, then searched for `paper_projects/papers/.../real_opsd_v7_leaderboard.csv`.
- Stage: input loading for the first figure.
- Data/figure impact: no evidence file was modified and the script stopped before saving a figure; existing PNG timestamps were unchanged.
- Correction: changed `FIG_DIR.parents[2]` to `FIG_DIR.parents[3]`, matching the current directory depth.
- Disposition: retain this record with the review evidence; use only the successful corrected run for regenerated figures.
