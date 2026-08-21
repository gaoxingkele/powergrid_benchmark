# Evidence Index

All 4 numbered tables and all 10 numbered figures in the paper are filed below, each with a markdown
transcription/description and a screenshot PNG (rendered from the source PDF). No numbered object is
omitted.

## Tables
| File | Source | Claims | Description |
|------|--------|--------|-------------|
| [tables/table1.md](tables/table1.md) | Table 1, §1 (p.2) | C02 | Comparison of related works across Adaptive Data / Signal Frequency Overlap / Vanishing Gradient properties |
| [tables/table2.md](tables/table2.md) | Table 2, §5.2 (p.12) | C01 | LSTM input settings (predicted period, sampling interval, sequence length, input length) |
| [tables/table3.md](tables/table3.md) | Table 3, §5.2 (p.13) | C01, C02, C03 | Prediction errors (RMSE, MAE) of four models for hourly load of fifty users |
| [tables/table4.md](tables/table4.md) | Table 4, §5.2 (p.14) | C01, C02, C03 | Prediction errors (RMSE, MAE) of four models for daily load of fifty users |

## Figures
| File | Source | Claims | Description |
|------|--------|--------|-------------|
| [figures/figure1.md](figures/figure1.md) | Figure 1, §3.1 (p.5) | — (method) | Flowchart of the EMD algorithm (diagram) |
| [figures/figure2.md](figures/figure2.md) | Figure 2, §3.3 (p.8) | C04 | Windowed CEEMDAN decomposition and IMF component extraction (diagram) |
| [figures/figure3.md](figures/figure3.md) | Figure 3, §4.1 (p.9) | — (method) | Batch Normalization structure (diagram) |
| [figures/figure4.md](figures/figure4.md) | Figure 4, §4.2 (p.10) | — (method) | Standard vs Dropout neural network (diagram) |
| [figures/figure5.md](figures/figure5.md) | Figure 5, §4.3 (p.10) | C01 | Model architecture of the LSTM-based user load prediction (diagram) |
| [figures/figure6.md](figures/figure6.md) | Figure 6, §5.1 (p.11) | C05 | Hourly raw load profile of a specific user (quantitative plot) |
| [figures/figure7.md](figures/figure7.md) | Figure 7, §5.1 (p.12) | C04, C05 | CEEMDAN decomposition (IMF1–IMF8 + RES) of a specific user (quantitative plot) |
| [figures/figure8.md](figures/figure8.md) | Figure 8, §5.2 (p.13) | C01 | Visualization of model parameters — per-layer input/output shapes (diagram) |
| [figures/figure9.md](figures/figure9.md) | Figure 9, §5.2 (p.14) | C03 | Hourly specific load prediction: four models vs actual (quantitative plot) |
| [figures/figure10.md](figures/figure10.md) | Figure 10, §5.2 (p.14) | C03 | Daily load prediction for a specific user: four models vs actual (quantitative plot) |

## Notes
- Figures 1–5 and 8 are diagrams/schematics; their structure is mirrored into
  `logic/solution/method.md` and `logic/solution/architecture.md`.
- Figures 6, 7, 9, 10 are quantitative plots read visually (no printed data labels); readings are
  marked `≈` where estimated.
- The paper prints no code or pseudocode, so there is no `src/execution/` artifact; the EMD/CEEMDAN
  procedures live as prose+equations in `logic/solution/method.md`.
