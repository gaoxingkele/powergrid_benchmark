# Figure 4: Construction and solution of the MGC economic dispatch model

- **Source**: Figure 4, Section 3.3
- **Caption**: "Construction and solution of the MGC economic dispatch model."
- **Screenshot**: figure4.png
- **Location on page**: Page 11 (PDF page 11), middle of the page.
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components**: Left block = the algorithm: "Chaos Optimization" + "Dynamic Opposition-based Learning Strategy" feed an "Improve" arrow into "The Grey Wolf Optimization (GWO) Algorithm", producing "Improved GWO (CDGWO)". Center-top block = MGC Structure (Main Grid, Transformer, Microgrid 1/2/3). Center-bottom blocks = "Constraints of MGC" (Power Balance Constraints, Equipment Self-Constrains) and "Objective Function" (Operation Costs, Environmental Costs, ESS Loss Costs, Penalty Terms), both feeding the "Economic Dispatch Model". Right block = "Output" (Power balance scheduling result of the MGC system; Various cost of the MGC system).
- **Connections**: CDGWO "Solving" arrow points into the Economic Dispatch Model; the MGC structure + constraints + objective function define the model; the model produces the Output.
- **Annotations**: Groups the paper's two contributions (improved algorithm; enriched objective with penalties) and how they combine.
- **What it conveys**: The end-to-end methodology: build the MGC model (structure + constraints + penalized multi-objective objective), then solve it with CDGWO to output dispatch schedules and costs.
