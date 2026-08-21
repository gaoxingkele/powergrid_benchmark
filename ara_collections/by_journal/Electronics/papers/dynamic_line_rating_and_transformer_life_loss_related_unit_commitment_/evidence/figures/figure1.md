# Figure 1: The 10-generator, 39-bus system and its regional partitioning structure

- **Source**: Figure 1, §5 (Case Study), page 10 (lower half of page, above the Table 1 reference text)
- **Caption**: "The 10-generator, 39-bus system and its regional partitioning structure."
- **Screenshot**: figure1.png
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components**: The standard IEEE 39-bus one-line diagram with 39 numbered buses and 10 generators
  (marked "G"); a synchronous condenser/compensator marked "C" near bus 36. Buses are grouped into
  five dashed-outline regions labeled Area1–Area5.
- **Connections**: Transmission lines connect buses per the IEEE 39-bus topology; the five regions
  are delineated by dashed red rectangles cutting across tie lines. Generators sit at buses including
  30, 37, 38, 31, 32, 33, 34, 35, 36 (condenser) and the slack at bus 31.
- **Annotations**: Region labels Area1 (lower left), Area2 (mid-left), Area3 (upper right), Area4
  (mid-right), Area5 (lower right). Equivalent wind turbines (DFIG) are connected at buses 17 and 21
  per the accompanying text (not separately glyphed in the figure).
- **What it conveys**: The regional partition is the structural basis for assigning each area its own
  ambient-temperature curve (Figure 2) and for the interface/section flow limits (Interface 1 = tie
  lines 1-2, 1-39, 3-4). This regional temperature heterogeneity is what lets the DLR + life-loss
  model reallocate generation between hot and cool areas. Mirrored in
  logic/solution/method.md ("Network / regional structure").
