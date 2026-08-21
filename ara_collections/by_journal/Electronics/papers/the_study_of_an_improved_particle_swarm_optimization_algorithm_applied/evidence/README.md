# Evidence Index

All 7 numbered tables and 14 numbered figures in the source are filed below, each with a markdown transcription/description AND a rendered screenshot (`.png`). No numbered object is omitted. Screenshots are page-level renders (dpi ~2.5x); when two objects share a page, each is filed under its own name and the object's location on the page is noted in its `.md`.

## Tables
| File | Source | Claims | Description |
|------|--------|--------|-------------|
| [tables/table1.md](tables/table1.md) | Table 1, §3.1 | C03 | Per-device operating parameters (lifespan, install/maintenance/depreciation cost, max power) for PV/WT/DG/ESS |
| [tables/table2.md](tables/table2.md) | Table 2, §3.1 | C03, C04 | Pollutant (CO2/SO2/NOX) treatment cost and DG vs main-grid emission factors |
| [tables/table3.md](tables/table3.md) | Table 3, §4.2.5 | C01 | Benchmark-function test parameters (dimension 50, search domain, acceptance 0.01, optimum 0) |
| [tables/table4.md](tables/table4.md) | Table 4, §5.1 | C03 | Time-of-use electricity purchase/sale prices (peak/standard/off-peak) |
| [tables/table5.md](tables/table5.md) | Table 5, §5.2 | C03 | Hourly 24-h dispatch: system load, PV/WT/DG/ESS output, grid interaction power |
| [tables/table6.md](tables/table6.md) | Table 6, §5.2 | C04 | Daily cost breakdown (O&M, fuel, depreciation, grid, environmental) for SCMPSO/CPSO/QPSO/PSO |
| [tables/table7.md](tables/table7.md) | Table 7, §5.2 | C04 | Pollutant emissions and treatment costs per algorithm (SCMPSO/CPSO/QPSO/PSO) |

## Figures
| File | Source | Claims | Description |
|------|--------|--------|-------------|
| [figures/figure1.md](figures/figure1.md) | Figure 1, §3.3 | C03 | Optimized scheduling flowchart (diagram) |
| [figures/figure2.md](figures/figure2.md) | Figure 2, §4.2.3 | C01 | Learning-factor iteration graph: c1 decreasing, c2 increasing (crossover at Tmax/2) |
| [figures/figure3.md](figures/figure3.md) | Figure 3, §4.2.4 | C02 | Oscillation convergence curve (two-sided damped envelope) |
| [figures/figure4.md](figures/figure4.md) | Figure 4, §4.2.4 | C02 | Progressive/asymptotic convergence curve (one-sided monotone decay) |
| [figures/figure5.md](figures/figure5.md) | Figure 5, §4.2.5 | C01 | SCMPSO convergence on five benchmark functions (multi-panel) |
| [figures/figure6.md](figures/figure6.md) | Figure 6, §4.2.5 | C01, C05 | Convergence comparison of SCMPSO vs CPSO/QPSO/PSO |
| [figures/figure7.md](figures/figure7.md) | Figure 7, §4.3 | C03 | SCMPSO model-solution algorithm flowchart (diagram) |
| [figures/figure8.md](figures/figure8.md) | Figure 8, §5.1 | C03 | Multi-source microgrid single-bus topology (diagram) |
| [figures/figure9.md](figures/figure9.md) | Figure 9, §5.1 | C03 | Typical summer daily system load profile |
| [figures/figure10.md](figures/figure10.md) | Figure 10, §5.1 | C03 | Typical summer 24-h wind speed |
| [figures/figure11.md](figures/figure11.md) | Figure 11, §5.1 | C03 | Typical summer 24-h temperature |
| [figures/figure12.md](figures/figure12.md) | Figure 12, §5.1 | C03 | 24-h solar irradiance intensity |
| [figures/figure13.md](figures/figure13.md) | Figure 13, §5.2 | C03 | 24-h output power curves of DG/PV/WT/ESS (multi-panel) |
| [figures/figure14.md](figures/figure14.md) | Figure 14, §5.2 | C03 | Microgrid<->main-grid electricity purchase/sale over 24 h |

## Notes / accounting
- No numbered object is unfiled. Objects sharing a page: Table 1 & Table 2 (p6); Table 3 & Figure 5 (p12); Figure 3 & Figure 4 (p11); Figure 6 & Figure 7 (p13); Figure 9/10/11 (p15); Table 4 & Figure 12 (p16); Figure 13 & Figure 14 (p17); Table 6 & Table 7 (p19).
- Diagrams (Figures 1, 7, 8) carry structured visual descriptions, not fabricated data tables.
- All plot readings from Figures 2-6, 9-14 are `digitized_estimate` (marked `≈`); exact tabulated values live in Tables 5-7 where the paper prints them.
