# Evidence Index

All 5 numbered Tables and 24 numbered Figures in the source are filed below, each with a markdown
transcription/description and a rendered screenshot (`.png`). No numbered object is omitted.

## Tables
| File | Source | Claims | Description |
|------|--------|--------|-------------|
| [tables/table1.md](tables/table1.md) | Table 1, §5.1 (p11) | C01 | Parameters of the 4 DGs (node, type, capacity, power factor) |
| [tables/table2.md](tables/table2.md) | Table 2, §5.1 (p12) | C01, C05 | Load weight coefficients (100/10/1) and their nodes |
| [tables/table3.md](tables/table3.md) | Table 3, §5.3.1 (p20) | C04 | Loss & min/max voltage before/after reconfig — fault S28+DG3 |
| [tables/table4.md](tables/table4.md) | Table 4, §5.3.2 (p21) | C04, C06 | Loss & min/max voltage before/after reconfig — fault S28 |
| [tables/table5.md](tables/table5.md) | Table 5, §5.3.3 (p24) | C04 | Loss & min/max voltage before/after reconfig — fault S9+S22 |

## Figures
| File | Source | Claims | Description |
|------|--------|--------|-------------|
| [figures/figure1.md](figures/figure1.md) | Figure 1, §5.1 (p11) | C01 | Diagram: improved IEEE 33-node topology, DG siting |
| [figures/figure2.md](figures/figure2.md) | Figure 2, §5.1 (p12) | C02 | Plot: 500 generated wind-power scenarios |
| [figures/figure3.md](figures/figure3.md) | Figure 3, §5.1 (p13) | C02 | Plot: 5 reduced wind-power scenarios |
| [figures/figure4.md](figures/figure4.md) | Figure 4, §5.1 (p13) | C02 | Plot: 500 generated PV scenarios |
| [figures/figure5.md](figures/figure5.md) | Figure 5, §5.2 (p14) | C02 | Plot: 5 reduced PV scenarios |
| [figures/figure6.md](figures/figure6.md) | Figure 6, §5.2 (p14) | C01, C03 | Diagram: two-island partition after extreme fault |
| [figures/figure7.md](figures/figure7.md) | Figure 7, §5.2 (p15) | C03 | Plot: island voltages per period, wind connected |
| [figures/figure8.md](figures/figure8.md) | Figure 8, §5.2 (p16) | C03 | Plot: DG output/load/loss per period, wind |
| [figures/figure9.md](figures/figure9.md) | Figure 9, §5.2 (p16) | C03 | Plot: island voltages per period, PV connected |
| [figures/figure10.md](figures/figure10.md) | Figure 10, §5.2 (p17) | C03 | Plot: DG output/load/loss per period, PV |
| [figures/figure11.md](figures/figure11.md) | Figure 11, §5.2 (p18) | C03 | Box plot: island voltage over 20 wind scenarios |
| [figures/figure12.md](figures/figure12.md) | Figure 12, §5.2 (p18) | C03 | Plot: Island 1 voltages, initial storage 50% |
| [figures/figure13.md](figures/figure13.md) | Figure 13, §5.2 (p19) | C03 | Plot: Island 1 voltages, initial storage 80% |
| [figures/figure14.md](figures/figure14.md) | Figure 14, §5.3.1 (p20) | C04 | Diagram: reconfiguration, fault S28+DG3 |
| [figures/figure15.md](figures/figure15.md) | Figure 15, §5.3.1 (p20) | C04 | Plot: node voltage before/after reconfig, S28+DG3 |
| [figures/figure16.md](figures/figure16.md) | Figure 16, §5.3.2 (p21) | C04, C06 | Diagram: reconfiguration, fault S28 |
| [figures/figure17.md](figures/figure17.md) | Figure 17, §5.3.2 (p21) | C04, C06 | Plot: node voltage before/after reconfig, S28 |
| [figures/figure18.md](figures/figure18.md) | Figure 18, §5.3.3 (p22) | C04 | Diagram: reconfiguration, fault S9+S22 |
| [figures/figure19.md](figures/figure19.md) | Figure 19, §5.3.3 (p22) | C04 | Plot: node voltage before/after reconfig, S9+S22 |
| [figures/figure20.md](figures/figure20.md) | Figure 20, §5.3.4 (p23) | C05 | Diagram: reconfiguration with baseline β=α (comparison) |
| [figures/figure21.md](figures/figure21.md) | Figure 21, §6 (p24) | C07 | Diagram: OPAL-RT + DSP semi-physical framework |
| [figures/figure22.md](figures/figure22.md) | Figure 22, §6 (p25-26) | C07 | Qual: node voltage waveforms, period 1 |
| [figures/figure23.md](figures/figure23.md) | Figure 23, §6 (p26-27) | C07 | Qual: node voltage waveforms, period 2 |
| [figures/figure24.md](figures/figure24.md) | Figure 24, §6 (p27-28) | C07 | Qual: node voltage waveforms, period 3 |

## Proofs / derivations
| File | Source | Description |
|------|--------|-------------|
| [proofs/socp_relaxation.md](proofs/socp_relaxation.md) | §2.2, §4.2, Eqs. (16),(43)-(48) | Second-order cone relaxation of branch power flow + scenario-weighted stochastic form |

Notes:
- Figures 22-24 each span two pages; the screenshot is the page carrying the figure's main caption
  (p26, p27, p28 respectively). The continuation panels are on the preceding page (p25, p26, p27).
- No source table/figure is a derived subset; all files are raw source objects.
