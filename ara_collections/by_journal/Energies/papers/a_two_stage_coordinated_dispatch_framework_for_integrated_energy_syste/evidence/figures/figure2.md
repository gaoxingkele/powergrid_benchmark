# Figure 2: Information Flow of the Two-Stage Coordinated Dispatch Framework

- **Source**: Figure 2, Section 3
- **Caption**: "Information flow of the proposed two-stage coordinated dispatch framework."
- **Screenshot**: figure2.png
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components**: Stage 1 box (Retail pricing and demand shaping: TOU price vector determination, cross-price elasticity, load reshaping), Stage 2 box (Security-constrained dispatch: generation, EESS, V2G, P2G, electricity–gas network), output box (Dispatch schedule and prices)
- **Connections**: One-directional price-to-load information flow from Stage 1 to Stage 2. The reshaped total load from Stage 1 becomes boundary condition for Stage 2
- **Annotations**: Both stages share the same 24 h day-ahead horizon and are assembled as a single MILP instance
- **What it conveys**: The sequential coupling where pricing decisions drive load reshaping, which then determines the dispatch
