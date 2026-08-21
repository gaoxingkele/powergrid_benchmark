# Figure 5: Mapping from the optimal solution of DP equations to the optimal solution of the dual problem

- **Source**: Figure 5, Section 3.3 (single-unit commitment approach), page 11
- **Caption**: "Mapping from the optimal solution of DP equations to the optimal solution of the dual problem."
- **Screenshot**: figure5.png (figure in the middle-lower band of PDF page 11)
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components**: Two convex-set shapes side by side. Left trapezoid labeled "Convex hull of the single-unit commitment problem" in the "Original-variable domain", with a marked vertex "Optimal solution of DP equations". Right trapezoid labeled "Convex hull of the dual problem" in the "Dual-variable domain", with a marked vertex "Optimal solution of the dual problem". A horizontal arrow labeled "Mapping" connects the two optimal vertices.
- **Annotations (center text box)**: "Physical meanings of variables in the dual problem: (1) Represent commitment statuses (e.g., the unit start at time slot t for the first time) (2) Represent generation levels and costs".
- **Connections**: Each vertex of the original single-unit convex hull maps to one vertex of the dual-problem convex hull; the dual variables carry physical meaning (statuses, generation levels, costs).
- **What it conveys**: In [12,13], DP equations for a single-unit commitment problem are converted to an LP whose dual directly delineates the convex hull X_g^c in the dual-variable domain; because the dual cost is fully convex, integer relaxation yields the convex envelope. Time-dependent costs/constraints are naturally handled by the DP structure, at the cost of many constraints (combinatorial DP states).
