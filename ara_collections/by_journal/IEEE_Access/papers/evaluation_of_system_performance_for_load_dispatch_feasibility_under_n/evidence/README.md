# Evidence Index

Systematic sweep of every numbered Table and Figure in the paper (main text only; the paper has no
appendix). All 13 tables and 10 figures are filed with a markdown transcription AND a page-level
screenshot (`.png`). Screenshots are full-page renders at scale 2.5; each markdown notes where on the
page the object sits.

## Tables
| File | Source | Claims | Description |
|------|--------|--------|-------------|
| [tables/table1.md](tables/table1.md) | Table 1, §IV/§VI (p.181188) | C01 | Cases for the performed analysis (Base, Case 1, Case 2a/b/c) |
| [tables/table2.md](tables/table2.md) | Table 2, §VI-B (p.181190) | C02, C06 | Data of generation units (26 units, 3105 MW) |
| [tables/table3.md](tables/table3.md) | Table 3, §VI-B (p.181190) | C08 | MTTF and failure rate by generator capacity |
| [tables/table4.md](tables/table4.md) | Table 4, §VII-A1 (p.181191) | C01 | DA hourly cumulative UC costs — Base Case |
| [tables/table5.md](tables/table5.md) | Table 5, §VII-A2 (p.181192) | C02, C03 | Case 1 vs Base: DA UC costs, % rise, ranking (10% CM) |
| [tables/table6.md](tables/table6.md) | Table 6, §VII-A2 (p.181192) | C02, C03, C04 | DA UC costs across Base, Case 1, Case 2a/b/c |
| [tables/table7.md](tables/table7.md) | Table 7, §VII-A/B (p.181192) | C06, C08 | Case 1 COPT — post-outage capacity & unavailability prob |
| [tables/table8.md](tables/table8.md) | Table 8, §VII-B1 (p.181193) | C04, C08 | Case 2 COPT for 2(a),(b),(c) |
| [tables/table9.md](tables/table9.md) | Table 9, §VII-B2 (p.181193) | C04, C08 | Case 1 hourly LOLP (overall 0.050113) |
| [tables/table10.md](tables/table10.md) | Table 10, §VII-B2 (p.181194) | C04, C08 | Case 2 hourly LOLP for 2(a),(b),(c) |
| [tables/table11.md](tables/table11.md) | Table 11, §VII-C (p.181194) | C04, C05 | Operating margin for Cases 1 and 2 |
| [tables/table12.md](tables/table12.md) | Table 12, §VII-D (p.181197) | C01, C04, C05, C07 | Assessment of system performance under N-1 |
| [tables/table13.md](tables/table13.md) | Table 13, §VII-D (p.181197) | C01, C05 | Feasibility of real-time load dispatch & corrective actions |

## Figures
| File | Source | Claims | Description |
|------|--------|--------|-------------|
| [figures/figure1.md](figures/figure1.md) | Figure 1, §II/§III (p.181185) | C01 | Proposed methodology (flow diagram) |
| [figures/figure2.md](figures/figure2.md) | Figure 2, §IV-A (p.181187) | C02, C03 | Criticality & robustness estimation flow |
| [figures/figure3.md](figures/figure3.md) | Figure 3, §V (p.181189) | C01 | Methodological framework (3-case, 2-stage) |
| [figures/figure4.md](figures/figure4.md) | Figure 4, §VI (p.181189) | C02, C06 | Single-line diagram of IEEE RTS |
| [figures/figure5.md](figures/figure5.md) | Figure 5, §VI-B (p.181190) | C02, C07 | Nine identified N-1 generator contingencies (bar) |
| [figures/figure6.md](figures/figure6.md) | Figure 6, §VI-B (p.181191) | C06, C08 | Hourly forecasted load demand (peak 2670 MW) |
| [figures/figure7.md](figures/figure7.md) | Figure 7, §VII-A2 (p.181194) | C02 | % variation in DA UC costs, Case 1 & 2(a),(b) (bar) |
| [figures/figure8.md](figures/figure8.md) | Figure 8, §VII-A2 (p.181195) | C02, C07 | Ranking of contingencies, Case 1 & 2(a),(b) (bar) |
| [figures/figure9.md](figures/figure9.md) | Figure 9, §VII-A2c (p.181196) | C02 | % variation in DA UC costs, Case 2(c) (bar) |
| [figures/figure10.md](figures/figure10.md) | Figure 10, §VII-A2c (p.181196) | C02, C07 | Ranking of contingencies, Case 2(c) (bar) |

Notes:
- Figures 1, 2, 3, 4 are **diagrams** (flowcharts / single-line network) — captured as visual
  descriptions, mirrored into `logic/solution/method.md`; no numeric tables fabricated.
- Figures 5, 7, 8, 9, 10 are **bar charts** whose category labels/values are printed on the bars or
  duplicated in tables; readings marked accordingly. Figure 6 is a **line plot** (demand curve).
- No object is omitted; all 23 numbered objects are filed.
