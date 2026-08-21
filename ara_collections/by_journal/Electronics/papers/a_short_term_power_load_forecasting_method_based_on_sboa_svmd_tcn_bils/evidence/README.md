# Evidence Index

Every numbered Table (1–9) and Figure (1–14) in the source is filed below with BOTH a markdown file and a screenshot `.png`. No object is omitted. Several objects share a PDF page; each object's PNG is the rendered page, and the object's location on that page is noted in its markdown file.

## Tables
| File | Source | Claims | Description |
|------|--------|--------|-------------|
| [tables/table1.md](tables/table1.md) | Table 1, §5.2 | C01 | SVMD + SBOA parameter settings (maxAlpha=19,990.25; pop=30; max_iter=60) |
| [tables/table2.md](tables/table2.md) | Table 2, §5.3 | C01 | Permutation entropy vs SVMD compactness; optimized value lowest (0.1245) |
| [tables/table3.md](tables/table3.md) | Table 3, §5.5 | C02 | CEEMDAN / ICEEMDAN parameter settings (baselines) |
| [tables/table4.md](tables/table4.md) | Table 4, §5.5 | C02 | Prediction errors: SVMD vs CEEMDAN/ICEEMDAN decomposition |
| [tables/table5.md](tables/table5.md) | Table 5, §5.6 | C03 | Errors with vs without SBOA-SVMD decomposition |
| [tables/table6.md](tables/table6.md) | Table 6, §5.6 | C04 | Prediction accuracy across forecasters (LSTM/ELM/BiLSTM/TCN-BiLSTM) |
| [tables/table7.md](tables/table7.md) | Table 7, §5.6 | C06 | Per-IMF training/testing times |
| [tables/table8.md](tables/table8.md) | Table 8, §5.7 | C05 | Per-season accuracy of the four forecasters |
| [tables/table9.md](tables/table9.md) | Table 9, §5.7 | C05 | Peak-period errors across seasons/days |

## Figures
| File | Source | Claims | Description |
|------|--------|--------|-------------|
| [figures/figure1.md](figures/figure1.md) | Figure 1, §2.1 | — | SVMD flowchart (diagram) |
| [figures/figure2.md](figures/figure2.md) | Figure 2, §2.2 | C01 | SBOA optimization flowchart (diagram) |
| [figures/figure3.md](figures/figure3.md) | Figure 3, §3.1 | — | TCN dilated causal convolution structure (diagram) |
| [figures/figure4.md](figures/figure4.md) | Figure 4, §3.1 | — | TCN residual unit (diagram) |
| [figures/figure5.md](figures/figure5.md) | Figure 5, §3.2 | — | LSTM cell structure (diagram) |
| [figures/figure6.md](figures/figure6.md) | Figure 6, §3.2 | — | BiLSTM structure (diagram) |
| [figures/figure7.md](figures/figure7.md) | Figure 7, §3.3 | C04 | TCN-BiLSTM combined model structure (diagram) |
| [figures/figure8.md](figures/figure8.md) | Figure 8, §4 | — | Full pipeline flowchart (diagram; 4 IMFs → 4 TCN-BiLSTM) |
| [figures/figure9.md](figures/figure9.md) | Figure 9, §5.3 | C01 | SVMD decomposition into 4 IMFs (quantitative plot) |
| [figures/figure10.md](figures/figure10.md) | Figure 10, §5.4 | C07 | Optimization fitness curves SBOA/SSA/GWO (quantitative plot) |
| [figures/figure11.md](figures/figure11.md) | Figure 11, §5.5 | C02 | Forecast vs measured across decomposition methods (quantitative plot) |
| [figures/figure12.md](figures/figure12.md) | Figure 12, §5.6 | C03 | Forecast with vs without decomposition (quantitative plot) |
| [figures/figure13.md](figures/figure13.md) | Figure 13, §5.6 | C04 | Forecast vs measured across forecasters, 2 months (quantitative plot) |
| [figures/figure14.md](figures/figure14.md) | Figure 14, §5.7 | C05 | Per-season error distributions (histograms) |

Notes:
- Figures 1–8 are architecture/pipeline diagrams — described structurally, not transcribed as data tables (mirrored into `logic/solution/architecture.md` and `algorithm.md`).
- Figures 9–14 are quantitative plots without printed data labels; numeric readings are `≈` estimates. The exact performance numbers live in the corresponding Tables (4/5/6/8/9).
