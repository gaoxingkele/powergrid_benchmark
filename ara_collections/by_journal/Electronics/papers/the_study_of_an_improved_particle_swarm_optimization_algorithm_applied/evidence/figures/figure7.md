# Figure 7: Algorithm Flowchart

- **Source**: Figure 7, Section 4.3 (page 13, lower figure)
- **Caption**: "Algorithm Flowchart."
- **Screenshot**: figure7.png
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components** (top-to-bottom flowchart of the SCMPSO model-solution procedure):
  1. "Algorithm Parameter Settings"
  2. "Input the relevant data required for the system, such as load data, electricity price parameters, equipment parameters, etc."
  3. "Initialize Population"
  4. "Set Equipment Range (PV, DG, WT, ESS) According to the Scheduling Strategy and Variable Constraint Equations"
  5. "Calculate the Current Particle's Individual Best Solution and the Global Best Solution of the Population"
  6. Decision diamond: "Check if the Maximum Number of Iterations is Reached" — Yes/No branches
  7. Yes -> "Output the Scheduling Strategy and the Best Fitness Value, where the overall operating cost of the system is minimized."
  8. No -> "Continue Iterating, Update Particle Positions and the Current Global Best Position, and Calculate the Fitness Function Value for Each Particle"
  9. -> "Adjust the Scheduling Strategy Based on the Current Particle Position, Velocity, Global Best Position, Optimal Velocity, and Other Relevant Parameters, and Calculate the Current Operating Cost."
- **Connections**: linear top-to-bottom with a decision diamond; the No branch loops from box 8/9 back up to the iteration-check/update loop (feedback loop until max iterations).
- **Annotations**: the loop implements the iterative update of individual/global best; termination on maximum iteration count (2000).
- **What it conveys**: the concrete step sequence of applying SCMPSO to the dispatch problem. Mirrored into `logic/solution/algorithm.md` (pseudocode / Steps 1-8) and matches the Step 1-8 prose on page 14.
