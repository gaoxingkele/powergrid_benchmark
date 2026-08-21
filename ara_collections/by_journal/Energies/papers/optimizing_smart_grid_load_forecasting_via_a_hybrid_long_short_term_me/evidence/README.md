# Evidence Index

All 3 numbered tables and 7 numbered figures in the paper are filed below, each with a markdown
transcription/description AND a page-level screenshot (`.png`). No numbered object is omitted.

## Tables
| File | Source | Claims | Description |
|------|--------|--------|-------------|
| [tables/table1.md](tables/table1.md) | Table 1, Section 4.2 | C01, C02 | Comparative results of LSTM, XGBoost, and LSTM-XGBoost hybrid on RMSE/MAPE/R2 |
| [tables/table2.md](tables/table2.md) | Table 2, Section 4.6 | C05 | Comparison of forecasting models from five recent studies [35]–[39] |
| [tables/tableA1.md](tables/tableA1.md) | Appendix A | — | Sample entries from the Elia Grid Load dataset |

## Figures
| File | Source | Claims | Description |
|------|--------|--------|-------------|
| [figures/figure1.md](figures/figure1.md) | Figure 1, Section 3 | C01 | Proposed model pipeline flow diagram (LSTM to XGBoost cascade) |
| [figures/figure2.md](figures/figure2.md) | Figure 2, Section 3.1 | C01, C03 | Time series plot of actual vs predicted load |
| [figures/figure3.md](figures/figure3.md) | Figure 2 (in-text ref), Section 3.1 | O3 | Scatter plot of load vs datetime showing seasonal U-shaped trend |
| [figures/figure4.md](figures/figure4.md) | Figure 3 (in-text ref), Section 3.1 | A1 | Histogram of load showing approximately normal distribution |
| [figures/figure5.md](figures/figure5.md) | Figure 4 (in-text ref), Section 3.1 | O3, C03 | Box plot of load by date showing distribution and outliers |
| [figures/figure6.md](figures/figure6.md) | Figure 5 (in-text ref), Section 3.1 | O3 | Heatmap of load by hour and date showing temporal patterns |
| [figures/figure7.md](figures/figure7.md) | Figure 6 (in-text ref), Section 4.5 | C01, C03 | Visual comparison: 4-panel (a) LSTM, (b) XGBoost, (c) LSTM vs hybrid, (d) full training+test |

## Notes
- Figure 1 is a pipeline diagram (architecture flow) — mirrored into `logic/solution/architecture.md`.
- Figures 2–6 are exploratory data analysis and visualization plots with approximate axis readings.
- Figure 7 is a 4-panel quantitative comparison; axis values are readable where printed by the Python plotting library.
- Table 1 contains the paper's headline numerical results; Table 2 compares against external studies with heterogeneous data resolutions.
- Table A1 shows five sample rows from the Elia Grid Load dataset (Appendix A).
