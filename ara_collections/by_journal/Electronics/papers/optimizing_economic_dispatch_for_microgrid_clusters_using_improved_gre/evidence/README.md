# Evidence Index

All numbered Tables (1-5, A1-A5) and Figures (1-10) from the paper are filed below, each as a
markdown transcription/description plus a rendered page screenshot (`.png`). No numbered object is
omitted. Page screenshots are full-page renders at scale 2.5 (pypdfium2); the exact location of each
object on its page is noted in the object's `.md` under "Location on page".

## Tables
| File | Source | Claims | Description |
|------|--------|--------|-------------|
| [tables/table1.md](tables/table1.md) | Table 1, §2.2.1 | C07 | Symbol definitions for the per-MG power balance equation (2) |
| [tables/table2.md](tables/table2.md) | Table 2, §3.1 | C02 | GWO wolf-pack hierarchy roles (α/β/δ/ω) |
| [tables/table3.md](tables/table3.md) | Table 3, §3.2.1 | C03 | Expressions of Tent/Sine/Chebyshev/Logistic chaotic maps |
| [tables/table4.md](tables/table4.md) | Table 4, §4.2 | C03 | Fitness value and runtime per chaotic map + traditional GWO |
| [tables/table5.md](tables/table5.md) | Table 5, §4.3.1 | C04, C05 | CDGWO vs FA/PSO/WOA/GWO/GA/SA: fitness, runtime, iterations, variance |
| [tables/tableA1.md](tables/tableA1.md) | Table A1, App. A | C06 | Actual daily MGC cost per algorithm (FA/PSO/WOA/GWO/CDGWO) |
| [tables/tableA2.md](tables/tableA2.md) | Table A2, App. A | C08 | Per-MG grid purchase/sale and inter-MG exchange, normal conditions |
| [tables/tableA3.md](tables/tableA3.md) | Table A3, App. A | C08, C09 | Per-MG grid purchase/sale and inter-MG exchange, with disturbance |
| [tables/tableA4.md](tables/tableA4.md) | Table A4, App. A | C06, C09 | Per-MG operational/pollution/ESS-loss costs, normal conditions |
| [tables/tableA5.md](tables/tableA5.md) | Table A5, App. A | C09 | Per-MG operational/pollution/ESS-loss costs, with disturbance |

## Figures
| File | Source | Claims | Description |
|------|--------|--------|-------------|
| [figures/figure1.md](figures/figure1.md) | Figure 1, §2.1 | C07 | Diagram: MGC system structure (Main Grid, EMC, three MGs) |
| [figures/figure2.md](figures/figure2.md) | Figure 2, §3.1 | C02 | Diagram: GWO wolf-pack leadership hierarchy pyramid |
| [figures/figure3.md](figures/figure3.md) | Figure 3, §3.2.3 | C04 | Flowchart: CDGWO procedure (Steps 1-7) |
| [figures/figure4.md](figures/figure4.md) | Figure 4, §3.3 | C01, C07 | Diagram: construction + solution of the MGC dispatch model |
| [figures/figure5.md](figures/figure5.md) | Figure 5, §4.1 | C08 | Plot: time-of-use purchase/sale/inter-MG electricity prices |
| [figures/figure6.md](figures/figure6.md) | Figure 6, §4.2 | C03 | Plot: convergence of four CGWO variants vs traditional GWO |
| [figures/figure7.md](figures/figure7.md) | Figure 7, §4.3.1 | C04, C05 | Plot: convergence of CDGWO vs six metaheuristics |
| [figures/figure8.md](figures/figure8.md) | Figure 8, §4.3.2 | C08, C09 | Plot: MG1 power-balance schedule, normal (a) and disturbed (b) |
| [figures/figure9.md](figures/figure9.md) | Figure 9, §4.3.2 | C08, C09 | Plot: MG2 power-balance schedule, normal (a) and disturbed (b) |
| [figures/figure10.md](figures/figure10.md) | Figure 10, §4.3.2 | C08, C09 | Plot: MG3 power-balance schedule, normal (a) and disturbed (b) |

## Notes on completeness
- 10 tables and 10 figures are the complete numbered-object set of the paper; all are filed.
- Figures 8-10 each contain two sub-panels (a) normal and (b) with disturbance; both are described
  within the single figure file (they are one numbered figure each). No derived-subset files were
  created — every file faithfully represents its exact source object.
- Figures 6, 7, 8, 9, 10 are low-resolution plots; readings are marked `≈` / `reading confidence: low`
  and exact numbers are taken from the corresponding tables rather than digitized off the plots.
- Equations (1)-(21) are not numbered "Figures/Tables" and are transcribed in `logic/solution/`
  (formulation.md, algorithm.md, constraints.md) rather than the evidence layer.
