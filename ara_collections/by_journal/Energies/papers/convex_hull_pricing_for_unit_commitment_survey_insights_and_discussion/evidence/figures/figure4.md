# Figure 4: Enumeration of commitment statuses based on a state transition diagram

- **Source**: Figure 4, Section 3.2 (state transition approach), page 9
- **Caption**: "Enumeration of commitment statuses based on a state transition diagram of one unit. Two-slot example with minimum-up time of two time slots and minimum-down time of two time slots."
- **Screenshot**: figure4.png (upper figure on PDF page 9)
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components**: A layered node-edge graph across two time slots (`t=1`, `t=2`). Nodes (circles) are commitment statuses split into an ONLINE band (upper) and OFFLINE band (lower), separated by a dashed horizontal line. The number inside each node indicates how many slots the unit has been online/offline. Directed edges (arrows) connect nodes between `t=1` and `t=2`, representing state transitions.
- **Legend**: "Node — Commitment status"; "Edge — State transition"; "Number in node — Online/offline state in which a unit has been in the respective slots".
- **Connections**: Multiple directed edges cross between ONLINE and OFFLINE bands, enumerating all feasible transitions consistent with minimum-up = 2 and minimum-down = 2 time slots.
- **What it conveys**: The [9] approach reformulates the unit in the (x_e, y_e) edge domain — binary x_e activates edge e (a transition), continuous y_e is generation above P_g^min on edge e. This yields a network-flow model whose integer relaxation gives the convex hull, and a per-unit cost linear in (x_e, y_e) so integer relaxation also gives the convex envelope. The enumeration causes a large constraint count (motivating the Bienstock–Zuckerberg decomposition).
