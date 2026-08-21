# Figure 3: Solution process of the bi-level optimization model

- **Source**: Figure 3, Section 3.3.2 (page 13). Located in the lower half of the page.
- **Caption**: "Solution process of the bi-level optimization model."
- **Screenshot**: figure3.png
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description (flowchart, top to bottom)
- **Components / steps**:
  1. Start
  2. Input electrical load, thermal load, cooling load, wind and solar output data and relevant equipment parameters
  3. Initialize the improved PSO optimization algorithm and randomly generate relevant variables
  4. Bring the relevant data into the lower-layer model and use CPLEX to solve the electric-vehicle electricity purchase and user-aggregator energy purchase
  5. Transmit the lower-layer energy and electric-vehicle charging status to the upper-layer model
  6. Calculate the upper-layer objective function value and record the individual best and global best
  7. Update the position and velocity of each particle in accordance with the improved PSO algorithm
  8. Decision: "Is the number of iterations satisfied?" — No → loop back to step 4; Yes → continue
  9. Output the Pareto frontier solution set
  10. Use TOPSIS to select the optimal solution and obtain the optimal scheduling result
  11. End
- **Connections**: Sequential arrows; the "No" branch of the iteration check returns to the CPLEX lower-layer solve (step 4), forming the upper–lower iteration loop.
- **What it conveys**: The nested solution loop — improved PSO drives the upper layer, CPLEX solves the lower layer each iteration, iterating until the max-iteration stopping rule; TOPSIS then selects a compromise from the Pareto front. Mirrored into logic/solution/algorithm.md (pseudocode) and src/environment.md.
