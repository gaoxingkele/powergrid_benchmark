# Figure 3: The procedure for the improved GWO algorithm

- **Source**: Figure 3, Section 3.2.3
- **Caption**: "The procedure for the improved GWO algorithm."
- **Screenshot**: figure3.png
- **Location on page**: Page 10 (PDF page 10), lower half of the page.
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components (flowchart, top to bottom)**: Begin → Initializing the parameters → Using chaotic maps to generate sequences as initial positions for the wolf population → Calculating the fitness value (F_MGC = C_Operation + C_Pollution + C_ESS + F_Main-MGC + F_ESS) → The three grey wolves with the lowest fitness are designated as the α wolf, β wolf, and δ wolf → Implement dynamic opposition-based learning operations on all individuals → Updating position of each wolf and the global optimum → decision diamond "Whether the iteration limit is reached".
- **Connections**: "No" branch from the decision diamond loops back up to "Calculating the fitness value"; "Yes" branch proceeds to "Output the optimal fitness value" → End.
- **Annotations**: The fitness function block explicitly restates the MGC objective (Eq. 8); minimization convention (lowest fitness = best).
- **What it conveys**: The CDGWO control flow: chaotic initialization (once) + per-iteration DOBL + α/β/δ-guided position update, iterated until the iteration cap. Transcribed step-by-step (Steps 1-7) into `logic/solution/algorithm.md`.
