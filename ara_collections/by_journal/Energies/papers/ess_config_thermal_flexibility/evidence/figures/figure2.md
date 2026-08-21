# Figure 2: POA-GWO-CSO Algorithm Flow Diagram

**Source**: Figure 2, Section 5, Energies 2025, 18, 2527
**Caption**: "POA-GWO-CSO algorithm flow diagram."
**Screenshot**: figure2.png
**Figure type**: diagram
**Extraction method**: visual_description
**Reading confidence**: medium

## Visual description
The flow diagram is a structured flowchart with the following steps:

1. **Start** — entry point
2. **Initialize**: "Population size N, Maximum number of iterations T" — rectangular process box
3. **Calculate fitness**: "Calculating fitness values for pelican populations" — rectangular process box
4. **Random prey**: "Randomly generated prey" — rectangular process box
5. **Phase I update (POA + GWO)**: "Improved Pelican Position Formula Update" — applies the GWO-enhanced position update (Eq. 43, combining POA move-to-prey with GWO α/β/δ leader strategy)
6. **Decision diamond**: "Whether the fitness value is improved?" — yes/no branch
   - YES → "Updating Phase I Adaptation Values" → proceeds to Phase II
   - NO → skips update, goes to Phase II
7. **Phase II update (CSO)**: "Vertical and horizontal crossover to Phase II pelican position" — applies CSO horizontal crossover (Eq. 44) and vertical crossover (Eq. 45) to all positions
8. **Phase II position**: "Updated Phase II Pelican Position"
9. **Decision diamond**: "Whether the fitness value is improved?" — yes/no branch
   - YES → "Updating Phase II adaptation values"
   - NO → skips update
10. **Decision diamond**: "Determine if the iteration condition is satisfied?" — checks if t < T
    - YES → loops back to "Randomly generated prey" (step 4)
    - NO → "output solution"
11. **End** — termination

The diagram uses three labeled position variables: \(x^{p1}_i\) (Phase I updated position) and \(x^{p2}_i\) (Phase II updated position), shown in marginal annotations.
