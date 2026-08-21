# Evidence Index

Systematic sweep of every numbered Table and Figure in the paper (main text + Appendix A). All 2 tables and 10 figures are filed as both a markdown transcription/description and a rendered screenshot (`.png`). No numbered object is omitted.

## Tables
| File | Source | Claims | Description |
|------|--------|--------|-------------|
| [tables/table1.md](tables/table1.md) | Table 1, §5 (p.9) | C01, C02, C05 | Multi-objective function values (voltage f1, network loss f2, capacity f3) across the four comparison scenarios |
| [tables/tableA1.md](tables/tableA1.md) | Table A1, Appendix A (p.13) | C01 | EV sampling parameters (arrival/departure time, initial SOC, per-station EV counts) for 3 EV types |

## Figures
| File | Source | Claims | Description |
|------|--------|--------|-------------|
| [figures/figure1.md](figures/figure1.md) | Figure 1, §3 (p.5) | C03 | Copula-based wind/PV daily-curve generation pipeline (diagram) |
| [figures/figure2.md](figures/figure2.md) | Figure 2, §4.1 (p.6) | C04 | CNN structure (diagram) |
| [figures/figure3.md](figures/figure3.md) | Figure 3, §4.1 (p.6) | C04 | Bi-LSTM schematic (diagram) |
| [figures/figure4.md](figures/figure4.md) | Figure 4, §5 (p.7) | C03 | Wind power reduced scenarios, 5 scenarios × 24 h with probabilities |
| [figures/figure5.md](figures/figure5.md) | Figure 5, §5 (p.7) | C03 | PV power reduced scenarios, 5 scenarios × 24 h with probabilities |
| [figures/figure6.md](figures/figure6.md) | Figure 6, §5 (p.8) | C04 | EV inbound/outbound time & initial SOC: True vs CNN vs BiLSTM vs CNN-BiLSTM |
| [figures/figure7.md](figures/figure7.md) | Figure 7, §5 (p.9–10) | C01 | 24-h node voltage surfaces for scenarios 1/2/3 |
| [figures/figure8.md](figures/figure8.md) | Figure 8, §5 (p.10) | C01 | Charge/discharge power & SOC curves of the two EVS storage devices |
| [figures/figure9.md](figures/figure9.md) | Figure 9, §5 (p.11) | C01, C05 | Selected EVS sites (nodes 13 & 33) on the 33-node layout |
| [figures/figureA1.md](figures/figureA1.md) | Figure A1, Appendix A (p.12) | C05 | End-to-end algorithm flowchart (CNN-BiLSTM → Frank copula → MOPSO loop) |

Notes:
- Figure 7 spans a page break ("Figure 7. Cont."): panels (a)/(b) render on page 9 (figure7.png), panel (c) on page 10.
- Figures 2 and 3 share page 6; Figures 4 and 5 share page 7 — each has its own screenshot of the full page with the object's on-page location noted in its `.md`.
- Table 1's printed caption says "three scenarios" but the body lists four columns; transcribed faithfully as four (see table1.md).
