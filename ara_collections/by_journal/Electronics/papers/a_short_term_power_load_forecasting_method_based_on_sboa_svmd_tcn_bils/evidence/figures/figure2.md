# Figure 2: SBOA optimization flowchart

- **Source**: Figure 2, Section 2.2, p. 8 (middle/lower half of page)
- **Caption**: "SBOA optimization flowchart."
- **Screenshot**: figure2.png
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components**: Start → Parameter initialization settings → Calculate the fitness value of each individual to find the optimal position → decision `t < 1/3 T` → (Y) Calculate Xi using equation (12) [search stage]; (N) → decision `t < 2/3 T` → (Y) Calculate Xi using equation (15) [consume stage]; (N) Calculate Xi using equation (17) [attack stage] → decision `rand > 0.5` → (Y) Update Xi using formula C1 in equation (22) [camouflage]; (N) Update Xi using formula C2 in equation (22) [escape] → Update the fitness of Xi and Xbest → decision "Check if the maximum number of iterations is met" → (N) loop back to the `t < 1/3 T` hunting branch; (Y) Output Xbest → End.
- **Connections**: Two decision layers select the hunting sub-stage by iteration interval; a `rand>0.5` gate selects escape strategy C1 vs C2; outer loop repeats until max iterations.
- **What it conveys**: SBOA alternates a three-interval hunting phase (Eqs. 12/15/17) and a two-branch escape phase (Eq. 22 C1/C2) each iteration, tracking the best position Xbest until the iteration budget is exhausted.

Note: the flowchart labels the search-stage box with Eq. (12); the consume stage box appears on the left labeled Eq. (15) and the attack stage box on the right labeled Eq. (17), matching the interval conditions in the text.
