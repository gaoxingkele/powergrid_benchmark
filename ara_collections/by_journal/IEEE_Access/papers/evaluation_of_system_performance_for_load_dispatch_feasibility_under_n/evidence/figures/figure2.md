# Figure 2: Estimation of criticality and robustness of system for n-1 generator contingency based DA UC

- **Source**: Figure 2, §IV-A (p.181187)
- **Caption**: "Estimation of criticality and robustness of system for n-1 generator contingency based DA UC."
- **Screenshot**: figure2.png (top-left column of the page)
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components**:
  - Top: "Forced outage of single generating unit (n-1 generator contingency)"
  - Decision diamond: "Is DA UC feasible? (i.e. supply-demand metric is not deterred)" with YES / NO
  - YES branch splits into two columns:
    - Green column (System Robustness): "Feasible and economic DA UC" → "Determine DA UC costs for all contingencies" → "Identify stable contingencies" → "Identify robust buses"
    - Middle column (System Criticality): "Relatively feasible but uneconomic DA UC" → "Higher DA UC costs" → "Identify critical contingencies" → "Identify weak buses"
  - NO branch (red column): "Critical system operation: DA UC not possible" → "Identify severe contingencies" → "Identify weakest buses"
- **Connections**: outage → feasibility check → three outcome columns (economic/robust, uneconomic/critical, infeasible/severe).
- **Annotations**: color coding — green = robust/feasible, red = infeasible/severe.
- **What it conveys**: how the feasibility of DA UC under an outage routes to robustness (stable
  contingencies/robust buses), criticality (critical contingencies/weak buses), or a severe-failure
  regime. Supports the classification behind claims C02 (weak buses) and C03 (robust buses).
