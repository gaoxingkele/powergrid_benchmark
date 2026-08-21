# Evidence Index

Complete sweep of every numbered table (9) and figure (7) in the paper. Each object has BOTH a
markdown transcription/description and a screenshot `.png` rendered from the source PDF page.
All figures in this review are diagrams/flowcharts — there are no quantitative plots; no numbered
object was omitted. Figures 1 and 2 share page 7, so `figure1.png` and `figure2.png` are renders of
the same page (each `.md` states which block is its object). Tables 4 and 6 each span a page break;
their `.md` files state which page the screenshot shows.

## Tables

| File | Source | Claims | Description |
|------|--------|--------|-------------|
| [tables/table1.md](tables/table1.md) | Table 1, §2.1 (p. 10) | C02, C07 | Comparison of 9 energy storage technologies: energy density, response time, lifespan, key applications |
| [tables/table2.md](tables/table2.md) | Table 2, §2.2.3 (p. 13) | C07 | Battery-only vs supercapacitor-only vs HESS: response, energy, degradation stress, lifetime, use |
| [tables/table3.md](tables/table3.md) | Table 3, §3.4 (p. 16) | C06 | External sizing optimization [39] vs external dispatch control [40]: focus, HOMER critique, insight |
| [tables/table4.md](tables/table4.md) | Table 4, §3.5 (pp. 16–17) | C01, C08 | Alignment of physical (PVsyst/Helioscope) and economic (HOMER Pro 3.18.4) optimization tools |
| [tables/table5.md](tables/table5.md) | Table 5, §4.1 (p. 18) | C04, C05 | Forecasting accuracy and dispatch impact synthesis (refs [58,59,61,62]) |
| [tables/table6.md](tables/table6.md) | Table 6, §4.3 (pp. 20–21) | C05 | Data preprocessing techniques: Min–Max, Z-score, EMD, VMD, WT, PCA, STL |
| [tables/table7.md](tables/table7.md) | Table 7, §5 (p. 22) | C09 | Key NNS integration factors for AC microgrids and their framework linkage |
| [tables/table8.md](tables/table8.md) | Table 8, §5 (p. 23) | C02, C09 | Summary of six advanced planning/control studies for hybrid microgrids |
| [tables/table9.md](tables/table9.md) | Table 9, §5/BMS (p. 25) | C01, C03, C04 | Quantitative improvements in SoC/SoE state tracking and their economic effects |

## Figures

| File | Source | Claims | Description |
|------|--------|--------|-------------|
| [figures/figure1.md](figures/figure1.md) | Figure 1, §1.3 (p. 7) | (E10 methodology; C01) | PRISMA-informed screening flowchart: 186 identified → 103 included |
| [figures/figure2.md](figures/figure2.md) | Figure 2, §1.3 (p. 7) | C01, C08 | Proposed multi-layer framework: inputs → PVsyst/ETAP → HOMER → MATLAB/Simulink → outputs, with feedback |
| [figures/figure3.md](figures/figure3.md) | Figure 3, §2 (p. 9) | C01, C03, C07 | Proposed AC-coupled hybrid renewable microgrid architecture with central EMS |
| [figures/figure4.md](figures/figure4.md) | Figure 4, §2.2.1 (p. 11) | C07 | AC-coupled architecture (separate inverters onto common AC bus) |
| [figures/figure5.md](figures/figure5.md) | Figure 5, §2.2.2 (p. 12) | C07 | DC-coupled architecture (common DC bus, single grid-tied inverter) |
| [figures/figure6.md](figures/figure6.md) | Figure 6, §2.2.3 (p. 13) | C02, C07 | DC-coupled HESS (battery + supercapacitor branches, grid-forming inverter) |
| [figures/figure7.md](figures/figure7.md) | Figure 7, §5 (p. 22) | C04 | Hybrid GWO-PSO workflow: GWO exploration → seed PSO particles → PSO exploitation → gbest |

## Known source-numbering quirks (transcribed faithfully, noted in the files)
- §4.1 text refers to the forecasting table as "Table 4"; the printed caption is "Table 5" (see table4.md/table5.md).
- §4.2 text refers to the GWO-PSO workflow as "Figure 6"; the printed caption is "Figure 7" (see figure6.md/figure7.md).
- Table 8's bracketed reference numbers are shifted by one relative to the §5 text attributions (see table8.md).
- Table 9's first column header is printed as "Parameter/3." (see table9.md).
