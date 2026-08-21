# Evidence Index

All 7 numbered tables and all 16 numbered figures in the source are filed below, each with a markdown transcription/description and a rendered screenshot (`.png`). No numbered object is omitted.

## Tables
| File | Source | Claims | Description |
|------|--------|--------|-------------|
| [tables/table1.md](tables/table1.md) | Table 1, §4.1 | C06 | Parameters of flexibility resources (gas turbine, boiler, chillers, storage) |
| [tables/table2.md](tables/table2.md) | Table 2, §4.1 | C02 | Demand-response compensation prices per load type |
| [tables/table3.md](tables/table3.md) | Table 3, §4.1 | C02, C05 | Time-of-use purchase/sale electricity prices |
| [tables/table4.md](tables/table4.md) | Table 4, §4.1 | C03, C07 | Electric-vehicle category parameters (grid-connection, capacity, proportion) |
| [tables/table5.md](tables/table5.md) | Table 5, §4.2.1 | C01, C02, C03, C04, C05 | Scheduling results across the 5 scenarios (all entities) |
| [tables/table6.md](tables/table6.md) | Table 6, §4.2.4 | C08 | Carbon emissions & operator revenue vs carbon-price multiple |
| [tables/table7.md](tables/table7.md) | Table 7, §4.3 | C09 | 30-run statistics (max/mean/variance/runtime) for PSO/DBO/IPSO |

## Figures
| File | Source | Claims | Description |
|------|--------|--------|-------------|
| [figures/figure1.md](figures/figure1.md) | Figure 1, §3 | C01 | Bi-level (Stackelberg) two-layer model diagram |
| [figures/figure2.md](figures/figure2.md) | Figure 2, §3 | C06 | IES physical structure / multi-energy coupling diagram |
| [figures/figure3.md](figures/figure3.md) | Figure 3, §3.3.2 | C09 | Bi-level solution-process flowchart (PSO + CPLEX + TOPSIS) |
| [figures/figure4.md](figures/figure4.md) | Figure 4, §4.1 | C06 | Renewable output & load forecast curves |
| [figures/figure5.md](figures/figure5.md) | Figure 5, §4.2.1 | C05 | Scenario-5 optimized electrical power balance |
| [figures/figure6.md](figures/figure6.md) | Figure 6, §4.2.1 | C05, C08 | Scenario-5 optimized heating power balance |
| [figures/figure7.md](figures/figure7.md) | Figure 7, §4.2.1 | C05 | Scenario-5 optimized cooling power balance |
| [figures/figure8.md](figures/figure8.md) | Figure 8, §4.2.1 | C03 | Electric flexibility: Scenario 5 vs Scenario 2 |
| [figures/figure9.md](figures/figure9.md) | Figure 9, §4.2.2 | C02 | Scenario-5 electricity demand-response result |
| [figures/figure10.md](figures/figure10.md) | Figure 10, §4.2.2 | C02 | Scenario-5 thermal demand-response result |
| [figures/figure11.md](figures/figure11.md) | Figure 11, §4.2.2 | C02 | Scenario-5 cooling demand-response result |
| [figures/figure12.md](figures/figure12.md) | Figure 12, §4.2.2 | C02 | Scenario-5 energy prices (electricity/heat/cooling) |
| [figures/figure13.md](figures/figure13.md) | Figure 13, §4.2.3 | C03 | EV charge/discharge power by category |
| [figures/figure14.md](figures/figure14.md) | Figure 14, §4.2.3 | C03 | EV charge/discharge price curve |
| [figures/figure15.md](figures/figure15.md) | Figure 15, §4.2.4 | C07 | Electric flexibility under adjusted EV proportions |
| [figures/figure16.md](figures/figure16.md) | Figure 16, §4.3 | C09 | Convergence comparison: IPSO vs DBO vs PSO |

## Source inconsistencies noted (see figure16.md, figure15.md)
- Iteration-reduction figure: Abstract states **52.0%**, body (§4.3, §5) states **54.0%**. The 54.0% is consistent with the reported 100→46 iterations.
- Figure cross-references in the body of §4.2.4/§4.3 mislabel Figure 16 as "Figure 15" in one sentence.
