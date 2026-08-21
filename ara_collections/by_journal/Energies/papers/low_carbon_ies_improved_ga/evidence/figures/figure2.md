# Figure 2 - Research Flow Chart of the Proposed IGA

- **Source**: Figure 2, Section 3
- **Caption**: "Research Flow chart of the proposed IGA."
- **Screenshot**: figure2.png
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components**: The flow chart shows the IGA optimization process:
  1. Input: IES operational parameters (CHP limits, GB limits, ESS parameters, load profiles, pricing data, renewable generation profiles)
  2. Start: Population initialization with random decision variables within boundaries
  3. Step: Parent selection using binary tournament with constraint-prioritizing criteria
  4. Step: Cyclic crossover operation to generate offspring
  5. Step: Polynomial mutation operation to introduce genetic variation
  6. Step: Offspring evaluation (objective functions + constraint violation)
  7. Step: Selection between parents and offspring (constraint-violating individuals eliminated)
  8. Step: Fast non-dominated sorting and crowding distance calculation
  9. Decision: Has maximum generation been reached? → No: return to Step 3; Yes: continue
  10. Output: Pareto-optimal solutions from the final population, with weight-based selection
- **What it conveys**: The IGA follows the standard GA loop but incorporates three key innovations: cyclic crossover, polynomial mutation, and constraint-prioritizing selection, embedded within the NSGA-II fast non-dominated sorting and crowding distance framework.
