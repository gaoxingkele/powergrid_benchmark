# Figure 3: Portugal 54 nodes system topology

- **Source**: Figure 3, Section 5.1
- **Caption**: "Portugal 54 nodes system topology."
- **Screenshot**: figure3.png
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components**: Four substations (S1, S2, S3, S4, drawn as station symbols) and 54 source-load nodes numbered 1–50 plus new nodes. DG boxes attached at several nodes; ESS boxes attached at several nodes.
- **Connections / line types (per legend)**:
  - Solid black lines = Existing Lines.
  - Dashed black lines = To-be-built (candidate) Lines.
  - Red lines = SOP and Interconnection Switch candidate positions.
  - Red dots = Existing Nodes; blue dots = New Nodes.
- **Annotations**: legend box (right) lists Station, Existing Lines, To-be-built Lines, SOP And Interconnection Switch Candidate Position, Existing Nodes, New Nodes, Distributed Generation (DG), Energy Storage (ESS).
- **What it conveys**: the base test network for all cases — four supply substations feeding a meshed set of candidate feeders, with the candidate SOP/switch tie positions and the DG/ESS placements (detailed in Tables 1–2) that the planning model chooses among.

Data source for node/line parameters: reference [31] (Miranda, Ranito, Proenca, IEEE Trans. Power Syst. 1994).
Mirrored into `src/environment.md` (test system) and `logic/solution/method.md`.
