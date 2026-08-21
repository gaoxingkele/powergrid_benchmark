# Figure 7: Node voltage curves for different scenarios

- **Source**: Figure 7, Section 5 (Case Analysis); panels (a) scenario 1 and (b) scenario 2 on page 9, panel (c) scenario 3 on page 10 (the figure is split with "Figure 7. Cont." across the page break)
- **Caption**: "Node voltage curves for different scenarios."
- **Screenshot**: figure7.png (page 9 portion, showing panels (a) scenario 1 and (b) scenario 2; panel (c) continues on page 10 — also visible in figure8.png's page)
- **Figure type**: quantitative_plot (3 surface panels)
- **Extraction method**: visual_description / digitized_estimate (3-D surfaces; exact node-hour values not readable)
- **Reading confidence**: low

- **Plot kind**: 3-D surface ("24-hour node voltage graph")
- **Axes (each panel)**: X = Time (h) 0–25; Y = Node sequence number 0–30 (IEEE 33-node); Z = voltage (p.u.), ≈0–1.2

## Trend summary
- **(a) scenario 1 (no DG)**: baseline voltage surface, generally smooth, Z up to ≈1.0 p.u.
- **(b) scenario 2 (DG, no storage)**: markedly rougher/rippled surface — adding DG raises voltage volatility across nodes and hours (visible extra ridges), confirming DG access strongly perturbs node voltage.
- **(c) scenario 3 (DG + EVS storage)**: surface peaks reach ≈1.2 p.u. but the node-to-node voltage profile is smoothed relative to scenario 2 — the EV-cluster dispatchable storage reduces the voltage fluctuation introduced by DG.

Text-reported point comparison (Section 5, p.9, verbatim): "the voltage deviation of node 16 in scenario 3 is 9.4% compared with that of node 16 in scenario 1, and the voltage deviation of node 16 in scenario 2 compared with node 16 in scenario 1 is 40%". I.e. EVS storage (sc3) cuts the DG-induced deviation from 40% to 9.4%. Supports C01.
