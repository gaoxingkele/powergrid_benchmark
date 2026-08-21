# Figure 1: Topology diagram of the distribution network

**Source**: Figure 1, Section 5.1, page 11
**Location on page**: middle-lower half of page 11, above Table 1
**Caption**: "Topology diagram of the distribution network."
**Screenshot**: figure1.png
**Figure type**: diagram
**Extraction method**: visual_description
**Reading confidence**: high

## Visual description
- **Components**: Improved IEEE 33-node distribution network. Root/source substation G1 (node 0)
  feeds a main feeder of nodes 0-1-2-...-17 (switches s1-s17). Branches: nodes 22-23-24 (via s22-s24),
  nodes 25-26-27-28-29-30-31-32 (via s26-s32), nodes 18-19-20-21 (via s18-s21). Tie/interconnection
  switches s33, s34, s35, s36, s37 (dashed lines) connect branches.
- **DG placement**: DG1 at node 6 (wind or PV), DG2 at node 13 (energy storage), DG3 at node 24
  (diesel generator), DG4 at node 31 (diesel generator).
- **Connections**: arrows indicate power flow direction along lines; solid lines = normally-closed
  segment switches (s1-s32), dashed lines = normally-open tie switches (s33-s37).
- **Annotations**: numbers below each switch are node indices; s## labels above are switch/line names.
- **What it conveys**: the test-system topology and DG siting used for all islanding and
  fault-recovery experiments; establishes which lines are segment vs tie switches (needed for the
  radiality and reconfiguration constraints).

Structure mirrored into logic/solution/method.md (system model) and logic/concepts.md.
