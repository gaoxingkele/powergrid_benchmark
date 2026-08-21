# Figure 7: Topological morphology optimization result

- **Source**: Figure 7, Section 5.1 (page 13)
- **Caption**: "Topological morphology optimization result." Panels: (a) Scenario 1, (b) Scenario 2.
- **Screenshot**: figure7.png
- **Location on page**: Middle of page 13. Black line = AC, red line = DC.
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: medium

## Visual description
- **Components**: Two 13-node distribution networks fed from an "Upper Grid" at bus 1, with PV/WT distributed generation and a diesel generator (near bus 13). Each bus is annotated AC or DC.
- **Panel (a) Scenario 1** (data center with DC loads + AC loads, PV, WT): a large share of buses/lines are DC (red). Buses with DC loads or new-energy units tend to be selected as DC buses (e.g. bus 3, bus 11, bus 12); buses with AC loads/new energy tend to be AC (e.g. bus 2, bus 13). DC component occupies a major part of the topology.
- **Panel (b) Scenario 2** (same loads but DC loads superimposed as AC loads — 0% DC penetration): AC component (black) dominates; only a few DC transformations, tending to DC distributed-generation/network buses such as bus 4 and bus 11.
- **What it conveys**: The optimal DC share of the network scales with the DC-load / new-energy proportion. Higher DC-load penetration (Scenario 1) drives a larger DC portion of the topology; near-zero penetration (Scenario 2) keeps it mostly AC. Bus type is chosen to minimize converter investment and converter loss.
