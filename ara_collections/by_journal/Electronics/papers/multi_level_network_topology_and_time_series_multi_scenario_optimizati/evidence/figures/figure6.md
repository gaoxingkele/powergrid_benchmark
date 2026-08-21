# Figure 6: Planning Flowchart

- **Source**: Figure 6, Section 4.2 (page 11)
- **Caption**: "Planning Flowchart."
- **Screenshot**: figure6.png
- **Location on page**: Lower-middle of page 11.
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components / flow (top to bottom)**:
  1. "Input planning original shape"
  2. "Initialising the population, let the population size be N, the number of iterations I = 1, and the maximum number of iterations is Imax"
  3. "Population individual number p=1"
  4. "Calculate the multi-objective function of individual p with its corresponding fitness level"
  5. Decision "p<N": if yes → "p=p+1" loop back to step 4; if No → continue
  6. "Judging the dominance relationship between each particle, forming a non-dominated set, the new solution set is merged with the old dominated set to become the new parent dominated set"
  7. Decision "I<Imax": if Yes → "I=I+1, Renewal of upper stocks" loop back to step 3; if No → continue
  8. "Output optimal solution based on small habitat sharing technology"
- **Connections**: Nested loops — inner loop over population individuals (p<N), outer loop over iterations (I<Imax).
- **What it conveys**: The overall NSGA/BPSO-style multi-objective optimization workflow: population init → per-individual fitness → non-dominated sorting/merge → iterate → output compromise optimum via niche (small-habitat) sharing. Mirrors the 14-step procedure in Section 4.2.
