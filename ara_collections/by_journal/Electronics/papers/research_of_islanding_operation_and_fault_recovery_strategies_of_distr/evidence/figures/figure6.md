# Figure 6: Results of the islanding partition

**Source**: Figure 6, Section 5.2, page 14
**Location on page**: middle of page 14, below Figure 5
**Caption**: "Results of the islanding partition."
**Screenshot**: figure6.png
**Figure type**: diagram
**Extraction method**: visual_description
**Reading confidence**: high

## Visual description
- **Scenario**: extreme fault — upstream substation outlet breaker trips (distribution network
  disconnected from higher-level grid) and line s28 malfunctions (marked with a red X between nodes
  28 and 29).
- **Components / partition**: two shaded distribution islands are formed.
  - **Island 1** (right region): contains DG4 (node 31, diesel) and DG2 (node 13, energy storage) —
    "two DGs and 11 loads" per text.
  - **Island 2** (upper-left region): contains DG3 (node 24, diesel) and DG1 (node 6, wind/PV) —
    "two DGs and 12 loads" per text.
- **Connections**: island boundaries drawn as dashed enclosures; the s28 fault splits the feeder.
- **What it conveys**: all DGs and important loads are successfully divided into two self-sustaining
  islands after the extreme fault; this is the input configuration for the per-island operation
  analysis (Figures 7-13). Island 2 (with uncertain wind/PV at node 6) is analyzed first.

Structure mirrored into logic/solution/method.md and logic/solution/constraints.md.
