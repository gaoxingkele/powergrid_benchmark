# Figure 1: A two-layer model considering multi-entity participation in IES optimization

- **Source**: Figure 1, Section 3 (page 6). Located in the lower half of the page.
- **Caption**: "A two-layer model considering multi-entity participation in IES optimization."
- **Screenshot**: figure1.png
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components**:
  - Upper-layer box (dashed border): Optimization Objectives = "Maximize the revenue of the IES operator and maximize system flexibility"; Optimization Variables = "Outputs of various devices in the system"; solved by "The improved PSO algorithm performs multi-objective solving for the upper-layer objectives".
  - Lower-layer box (dashed border): two Optimization Objectives = "Minimize the total cost of the user aggregator" and "Maximize the self-utility of electric vehicles"; Optimization Variables = "Power purchased by users" and "Charging and discharging power of electric vehicles"; solved by "The CPLEX solves the lower-layer objective function".
- **Connections**:
  - Downward arrow (upper → lower): "Transmit energy prices to the lower-layer model".
  - Upward arrow (lower → upper): "Transmit the equivalent of cold energy, etc. to the upper-layer model" (i.e., purchased quantities / EV charge-discharge fed back).
- **Annotations**: Two dashed rectangular groupings separate the leader (upper, IES operator) from the followers (lower, aggregator + EVs), depicting the Stackelberg-style bi-level structure.
- **What it conveys**: The paper's bi-level (Stackelberg leader–follower) architecture: the IES operator leads by setting prices; aggregator and EVs respond; iteration between the two layers reaches the global solution. Mirrored into logic/solution/architecture.md and formulation.md.
