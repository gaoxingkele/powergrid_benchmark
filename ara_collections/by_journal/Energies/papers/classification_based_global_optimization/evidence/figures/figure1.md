# Figure 1 - Optimal Placement and Sizing of EVCSs

**Source**: Figure 1, Section 2
**Caption**: Optimal placement and sizing of EVCSs.
**Screenshot**: figure1.png
**Figure type**: diagram
**Extraction method**: visual_description
**Reading confidence**: medium

## Visual description
- **Components**: 
  - Start block: "Enter network data (load data, bus data, line data)"
  - Classification block: "Classify branches based on active power consumption; Sort branches descending (high to low)"
  - Loop structure: iteration over selected branches with IF conditions
  - Decision diamonds: checking if objective function Ft improves
  - EVCS sizing adjustment block
  - Output block: "Optimal EVCS placement and sizing"
- **Connections**: Linear flow from data entry through classification, candidate evaluation, Ft minimization check, sizing adjustment, and final output. Feedback loop from "Ft minimized?" back to sizing adjustment until Ft no longer improves.
- **Annotations**: The flowchart shows the sequential process for EVCS allocation: classify branches by active power -> evaluate candidate locations on high-demand branches -> adjust EVCS sizing iteratively -> check Ft improvement -> output solution.
- **What it conveys**: The EVCS placement process is guided by bus classification (active power demand) before any location search, narrowing candidate locations to high-load branches.
