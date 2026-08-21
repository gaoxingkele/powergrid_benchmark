# Figure 3 - Optimal Placement and Sizing of CBs

**Source**: Figure 3, Section 2
**Caption**: Optimal placement and sizing of CBs.
**Screenshot**: figure3.png
**Figure type**: diagram
**Extraction method**: visual_description
**Reading confidence**: medium

## Visual description
- **Components**:
  - Start block: "Enter network data (load data, bus data, line data)"
  - Classification block: "Classify branches based on reactive power consumption; Sort branches descending"
  - CB initialization: CB size = branch reactive power demand
  - Power flow analysis block
  - Constraint checks: voltage limits, thermal limits, CB capacity limits (sum(QCB,j) < 0.9 x sum(Qld,i))
  - Ft evaluation and minimization decision
  - CB sizing adjustment loop
  - Output block: "Optimal CB placement and sizing"
- **Connections**: Data entry -> branch classification (reactive power) -> select candidate bus -> initialize CB size -> run power flow -> check constraints -> evaluate Ft -> if not minimized, adjust CB size and repeat -> output optimal configuration.
- **Annotations**: The key difference from Figure 2 is that CB classification is based on reactive power demand rather than active power demand. CB capacity is constrained by 90% of total reactive load.
- **What it conveys**: CB placement uses the same deterministic, classification-based methodology as EVCS and DG planning, adapted for reactive power compensation.
