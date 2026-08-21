# Evidence Index

All 5 numbered tables and 12 numbered figures in the source are filed below, each as a markdown
transcription/description **and** a screenshot (`.png`) rendered from the page containing it. No
numbered object is omitted. Figures 1–8 are diagrams/schematics (visual descriptions); Figures 9–12
are quantitative plots (digitized-estimate readings + trend summaries).

## Tables
| File | Source | Claims | Description |
|------|--------|--------|-------------|
| [tables/table1.md](tables/table1.md) | Table 1, §3, p10 | C03 | Activation-function comparison (RMSE/MAE/MAPE) |
| [tables/table2.md](tables/table2.md) | Table 2, §3, p10 | C04 | Optimizer comparison (RMSE/MAE/MAPE) |
| [tables/table3.md](tables/table3.md) | Table 3, §3, p11 | C05 | Historical-load lookback-length comparison |
| [tables/table4.md](tables/table4.md) | Table 4, §4, p11 | C01, C02, C06 | Model comparison on Tétouan dataset |
| [tables/table5.md](tables/table5.md) | Table 5, §4, p13 | C01, C02, C06 | Model comparison on Electrician Cup dataset |

## Figures
| File | Source | Claims | Description |
|------|--------|--------|-------------|
| [figures/figure1.md](figures/figure1.md) | Figure 1, §2, p3 | — | Training-pipeline flowchart (diagram) |
| [figures/figure2.md](figures/figure2.md) | Figure 2, §2.1, p4 | — | LSTM cell / gate structure (diagram) |
| [figures/figure3.md](figures/figure3.md) | Figure 3, §2.2, p5 | — | Generic CNN layer sequence (diagram) |
| [figures/figure4.md](figures/figure4.md) | Figure 4, §2.2, p6 | — | Convolution dot-product principle (diagram) |
| [figures/figure5.md](figures/figure5.md) | Figure 5, §2.2, p6 | — | Pooling processes (diagram) |
| [figures/figure6.md](figures/figure6.md) | Figure 6, §2.2, p7 | — | Fully-connected flatten process (diagram) |
| [figures/figure7.md](figures/figure7.md) | Figure 7, §2.3, p8 | C01, C02 | Three-channel LSTM-CNN structure (diagram, core contribution) |
| [figures/figure8.md](figures/figure8.md) | Figure 8, §2.3, p9 | C01, C02 | Cross-channel convolution fusion (diagram, Eq. 8) |
| [figures/figure9.md](figures/figure9.md) | Figure 9, §4, p12 | C01, C06 | Tétouan prediction curves vs actual (line plot) |
| [figures/figure10.md](figures/figure10.md) | Figure 10, §4, p12 | C06 | Tétouan per-model load residuals (bar plot) |
| [figures/figure11.md](figures/figure11.md) | Figure 11, §4, p13 | C01, C06 | Electrician Cup prediction curves vs actual (line plot) |
| [figures/figure12.md](figures/figure12.md) | Figure 12, §4, p13 | C06 | Electrician Cup per-model load residuals (bar plot) |

## Notes
- **No derived subsets**: every filed object is a raw transcription of the exact numbered source object.
- **Equations (1–8)** are not numbered figures/tables; they are captured in logic/solution/method.md and logic/concepts.md.
- **Diagrams** carry visual descriptions (no fabricated data tables); their structure is mirrored into logic/solution/architecture.md and method.md.
- **Quantitative plots** (F9–F12) use `≈` for every estimated reading with medium reading confidence; exact numeric results live only in the tables.
</content>
