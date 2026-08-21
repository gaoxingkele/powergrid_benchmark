# Evidence Index

All 7 numbered tables and all 10 numbered figures in the source are filed below, each with a markdown transcription/description and a `.png` screenshot. No numbered object is omitted.

## Tables
| File | Source | Claims | Description |
|------|--------|--------|-------------|
| [tables/table1.md](tables/table1.md) | Table 1, §3.1.1 | C01 | Dataset feature descriptions (date/time, temperature, load, price) |
| [tables/table2.md](tables/table2.md) | Table 2, §4.1(a) | C01, C03 | LSTM MSE per dataset |
| [tables/table3.md](tables/table3.md) | Table 3, §4.1(b) | C01, C03 | LSTM MAPE per dataset |
| [tables/table4.md](tables/table4.md) | Table 4, §4.2(a) | C01, C03 | GRU MSE per dataset |
| [tables/table5.md](tables/table5.md) | Table 5, §4.2(b) | C01, C03 | GRU MAPE per dataset |
| [tables/table6.md](tables/table6.md) | Table 6, §4.2(c) | C02, C05 | Consolidated LSTM vs GRU MSE & MAPE |
| [tables/table7.md](tables/table7.md) | Table 7, §4.3 | C01 | Proposed method vs previous works (macro) |

## Figures
| File | Source | Claims | Description |
|------|--------|--------|-------------|
| [figures/figure1.md](figures/figure1.md) | Figure 1, §1 | — | Graphical abstract / study pipeline (diagram) |
| [figures/figure2.md](figures/figure2.md) | Figure 2, §3.3.1 | — | Modified LSTM unrolled over time (diagram) |
| [figures/figure3.md](figures/figure3.md) | Figure 3, §3.3.1 | — | GRU cells chained over sequence (diagram) |
| [figures/figure4.md](figures/figure4.md) | Figure 4, §3.4.1 | — | Internal GRU cell dataflow (diagram) |
| [figures/figure5.md](figures/figure5.md) | Figure 5, §3.4.1 | — | Internal LSTM cell dataflow (diagram) |
| [figures/figure6.md](figures/figure6.md) | Figure 6, §4.1(b) | C04 | Load balancing / peak shaving curve (LSTM) |
| [figures/figure7.md](figures/figure7.md) | Figure 7, §4.2(b) | C04 | Load balancing / peak shaving curve (GRU) |
| [figures/figure8.md](figures/figure8.md) | Figure 8, §4.3 | C04 | Peak-load reduction & voltage-fluctuation before/after control |
| [figures/figure9.md](figures/figure9.md) | Figure 9, §4.2(c) | C01, C02 | Predictions vs actual time series across 4 datasets |
| [figures/figure10.md](figures/figure10.md) | Figure 10, §4.3 | C05 | Grid resilience scores (LSTM > GRU, inverts error ranking) |

## Notes
- Figures 1–5 are diagrams (structure only) — no numeric tables fabricated; structure mirrored into `logic/solution/architecture.md`.
- Figures 6–10 are quantitative plots without printed data labels; readings are `digitized_estimate` marked `≈`, except exact text-stated anchors in Figure 8 (160→140 MW; 4–7.5%→3–5%).
- The five tabulated datasets are AEP, COMED, DAYTON, DEOK, DOM; Figure 9 additionally shows EKPC, NI, PJM_Load (no tabulated error numbers for these three).
- Equations (Eqs. 1–17) are transcribed into `logic/concepts.md` and `logic/solution/method.md`; they are not separate numbered evidence objects.
