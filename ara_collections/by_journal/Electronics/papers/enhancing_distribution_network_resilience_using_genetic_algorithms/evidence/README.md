# Evidence Index

All six numbered tables and all five numbered figures in the source are filed below, each with a
markdown transcription/description AND a screenshot (.png). No numbered object is omitted.

## Tables
| File | Source | Claims | Description |
|------|--------|--------|-------------|
| [tables/table1.md](tables/table1.md) | Table 1, §4, p.8 | C01 | Line data — R, X, thermal limit for L1–L5 |
| [tables/table2.md](tables/table2.md) | Table 2, §4, p.8 | C01 | Load data — P/Q demand at buses 2–6 |
| [tables/table3.md](tables/table3.md) | Table 3, §6, p.10 | C02 | Voltage profile, base vs optimized, buses 1–6 |
| [tables/table4.md](tables/table4.md) | Table 4, §6, p.10 | C03 | Real power loss, base (55.3 kW) vs optimized (29.7 kW) |
| [tables/table5.md](tables/table5.md) | Table 5, §6, p.11 | C05 | Optimal DER dispatch P/Q at buses 2, 3, 4 |
| [tables/table6.md](tables/table6.md) | Table 6, §6, p.11 | C04 | Resilience assessment under DER-trip contingency |

## Figures
| File | Source | Claims | Description |
|------|--------|--------|-------------|
| [figures/figure1.md](figures/figure1.md) | Figure 1, §2, p.5 | (concept) | Trapezoidal resilience curve (diagram) |
| [figures/figure2.md](figures/figure2.md) | Figure 2, §3, p.7 | C01 | GA block diagram / flowchart (diagram) |
| [figures/figure3.md](figures/figure3.md) | Figure 3, §4, p.7 | C01 | 6-bus radial network topology (diagram) |
| [figures/figure4.md](figures/figure4.md) | Figure 4, §6, p.9 | C02 | Voltage profile comparison (line plot) |
| [figures/figure5.md](figures/figure5.md) | Figure 5, §6, p.10 | C03 | GA power-loss convergence curve (line plot) |

## Notes
- Figures 1, 2, 3 are diagrams (visual description, no fabricated data table).
- Figure 4 uses `exact_from_labels` — its values are the exact numbers printed in Table 3.
- Figure 5 uses `digitized_estimate` — curve read off gridlines (`≈`); exact endpoints in Table 4.
- Table 4 base case is labeled "(No DER)"; Table 6 base case is a DER-trip contingency. The two
  "base cases" are different operating points — see the note in each file.
- Figure 3 as drawn conflicts with Table 1 on line L5's upstream endpoint (figure: bus 3;
  table/prose: bus 5) — recorded in figures/figure3.md, not silently resolved.
