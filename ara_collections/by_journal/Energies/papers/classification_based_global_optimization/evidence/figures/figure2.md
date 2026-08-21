# Figure 2 - Optimal Placement and Sizing of DGs

**Source**: Figure 2, Section 2
**Caption**: Optimal placement and sizing of DGs.
**Screenshot**: figure2.png
**Figure type**: diagram
**Extraction method**: visual_description
**Reading confidence**: medium

## Visual description
- **Components**:
  - Start block: "Enter network data (load data, bus data, line data)"
  - Classification block: "Classify branches based on active power consumption; Sort branches descending"
  - DG initialization: DG size = branch active power demand
  - Power flow analysis block
  - Constraint checks: voltage limits, thermal limits (|Sij| <= Sij,max), DG capacity limits
  - Ft evaluation and minimization decision
  - DG sizing adjustment loop
  - Output block: "Optimal DG placement and sizing"
- **Connections**: Data entry -> branch classification (active power) -> select candidate bus -> initialize DG size -> run power flow -> check constraints -> evaluate Ft -> if not minimized, adjust DG size and repeat -> output optimal configuration.
- **Annotations**: The flowchart shows an iterative inner loop for DG sizing adjustment, with constraint satisfaction checks at each iteration. Thermal capacity limit |Sij| <= Sij,max is explicitly shown as a constraint gate.
- **What it conveys**: DG placement follows the same classification-driven approach as EVCS but adds explicit thermal capacity checking and DG-specific constraints. The process is deterministic with no random initialization.
