# Figure and Table Trace

This internal map records the accepted input and regenerated artifact behind each result figure and table. Source paths and SHA-256 digests are fixed in `RESULTS_ARTIFACT_MANIFEST.json`; `figures/make_figures.py` verifies those digests before writing any artifact.

| Manuscript item | Regenerated artifact | Accepted evidence used | Comparison scope |
|---|---|---|---|
| Table 4 | `derived_tables/p5_main_leaderboard.csv` | Main run rows | Pooled descriptive summary; deterministic rows represent seven unique outputs |
| Figure 2 | `figures/fig_hv_boxplot.svg` and `.png` | Main run rows | Seed distributions for stochastic methods; deterministic methods shown as unique-output markers |
| Table 5 | `derived_tables/p5_nsga2_scenario_comparison.csv` | Main inference rows | Two-sided Mann--Whitney U; Holm across 12 stochastic opponents within scenario |
| Figure 3 | `figures/fig_ablation.svg` and `.png` | Main run and named-configuration inference rows | Pooled effects descriptive; objective-hiding rows are combined controls; scenario tests retain their stated multiplicity families |
| Figure 4 | `figures/fig_event_record_diagnostics.svg` and `.png` | Main run rows | Descriptive implemented-record count and pool-position co-occurrence; no lineage or replay claim |
| Table 6 | `derived_tables/p5_matched_budget_controls.csv` | Accepted three-budget summary and inference rows | Hypervolume Holm family contains two comparators within each budget; preference distance descriptive |
| Figure 5 | `figures/fig_preference_budget_controls.svg` and `.png` | Accepted three-budget summary rows | Hypervolume and preference distance kept in separate panels |
| Table 7 | `derived_tables/p5_matched_output_summary.csv` | Accepted matched-compromise summary | Descriptive, one preserved compromise output per run |
| Table 8 | `derived_tables/p5_normalization_bounds_benchmark.csv` | Accepted bound table | Descriptive benchmark-scenario bound definitions |
| Table 9 | `derived_tables/p5_normalization_summary.csv` | Accepted normalization summary | Descriptive bound, clipping, and reference-point sensitivity |
| Table 10 | `derived_tables/p5_sensitivity_effects.csv` | Accepted prespecified sensitivity effects | Descriptive; no p-values |
| Figure 6 | `figures/fig_external_validity.svg` and `.png` | Accepted NERC and MTEP16 backtests | Descriptive external consistency |
| Figure 7 | `figures/fig_search_event_efficiency.svg` and `.png` | Main run rows | Descriptive native-unit panels; NSGA-II event fields not instrumented |
| Figure 8 | `figures/fig_mtep_outcome_backtest.svg` and `.png` | Accepted MTEP16 backtest | Descriptive broad-versus-strict outcome sensitivity |

Auxiliary regenerated checks are `p5_component_multiplicity.csv`, `p5_clipping_totals.csv`, `p5_event_record_summary.csv`, `p5_nerc_descriptive_summary.csv`, `p5_mtep_outcome_summary.csv`, and `p5_search_event_efficiency.csv`. They preserve the same scope labels and are not additional experiments.
