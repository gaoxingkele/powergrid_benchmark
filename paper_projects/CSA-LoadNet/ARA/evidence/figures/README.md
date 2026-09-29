# Figures

Manuscript figures are generated and versioned at
`mintou_p2_hygraph_load_forecasting/manuscript/figures/` (repository root):

- `fig_leaderboard.png` — Figure 1: merged day-ahead leaderboards (OPSD 24 h MAPE, SimBench 24 h normalized MAE)
- `fig_component.png` — Figure 2: component significance matrix (Mann–Whitney U, Holm-corrected, all five dataset/horizon settings)
- `fig_ausgrid.png` — Figure 3: Ausgrid hierarchical 24 h leaderboard (sMAPE)

All are 300 dpi PNGs. Regenerate with `manuscript/figures/make_figures.py`, which
reads the v7 evidence tables in `evidence/tables/` (`real_opsd_v7_leaderboard.csv`,
`real_simbench_v7_leaderboard.csv`, `real_ausgrid_v7_leaderboard.csv`,
`real_p2_v7_significance.csv`).

This directory intentionally holds no figure binaries.
