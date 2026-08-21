# Evidence Index

All 4 numbered tables and 12 numbered figures in the source are filed below, each with a markdown
transcription/description and a rendered screenshot (`.png`). Nothing is omitted.

## Tables
| File | Source | Claims | Description |
|------|--------|--------|-------------|
| [tables/table1.md](tables/table1.md) | Table 1, §3.1 (p.11) | — | Data example: one row of the 10-column load+weather dataset with units |
| [tables/table2.md](tables/table2.md) | Table 2, §4.1 (p.12) | C03 | One-week MAE/MAPE/RMSE for graph-construction methods (Spearman/KNN/learned/MI) |
| [tables/table3.md](tables/table3.md) | Table 3, §4.2 (p.13) | C01 | Model structure parameters (layer input/output dimensions) |
| [tables/table4.md](tables/table4.md) | Table 4, §4.4 (p.16) | C01, C02, C04 | Stagewise ablation MAE/MAPE/RMSE (week & day) |

## Figures
| File | Source | Claims | Description |
|------|--------|--------|-------------|
| [figures/figure1.md](figures/figure1.md) | Figure 1, §2.1 (p.4) | — | Model flow chart (diagram) |
| [figures/figure2.md](figures/figure2.md) | Figure 2, §2.2 (p.5) | C03 | Spearman correlation heatmap between features (quantitative) |
| [figures/figure3.md](figures/figure3.md) | Figure 3, §2.2 (p.6) | — | GCN structure (diagram) |
| [figures/figure4.md](figures/figure4.md) | Figure 4, §2.3 (p.7) | — | LSTM cell structure (diagram) |
| [figures/figure5.md](figures/figure5.md) | Figure 5, §2.3 (p.8) | — | BiLSTM structure (diagram) |
| [figures/figure6.md](figures/figure6.md) | Figure 6, §2.4 (p.9) | C04 | AdaBoost structure (diagram) |
| [figures/figure7.md](figures/figure7.md) | Figure 7, §4.3 (p.14) | C01 | One-day prediction results vs baselines (line plot) |
| [figures/figure8.md](figures/figure8.md) | Figure 8, §4.3 (p.14) | C01 | One-week prediction results vs baselines (line plot) |
| [figures/figure9.md](figures/figure9.md) | Figure 9, §4.3 (p.14) | C01 | One-day prediction error bars (labeled) |
| [figures/figure10.md](figures/figure10.md) | Figure 10, §4.3 (p.15) | C01 | One-week prediction error bars (labeled) |
| [figures/figure11.md](figures/figure11.md) | Figure 11, §4.4 (p.15) | C02, C04 | One-day forecasting vs ablation variants (line plot) |
| [figures/figure12.md](figures/figure12.md) | Figure 12, §4.4 (p.16) | C05 | One-week forecast with 95% confidence interval (line plot) |

Notes:
- Screenshots are **full-page renders** of the source PDF page containing each object; figures
  sharing a page share an identical render (Figures 7/8/9 = p.14; Figures 10/11 = p.15; Figure 12
  and Table 4 = p.16).
- Figures 1, 3, 4, 5, 6 are **diagrams** (structure/schematic) — described visually, no data table.
- Figure 2 is a **heatmap** with printed cell values (exact). Anomaly: Wind Speed–Pressure = 1.17 (>1).
- Figures 9 and 10 are bar charts with **printed data labels** (exact values).
- Figures 7, 8, 11, 12 are **line plots without data labels** — trend/qualitative reading (approximate).
