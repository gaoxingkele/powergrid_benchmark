# Figure 18: Network reconfiguration result when the fault locates at line S9 and S22

**Source**: Figure 18, Section 5.3.3, page 22
**Location on page**: middle of page 22
**Caption**: "Network reconfiguration result when the fault locates at line S9 and S22."
**Screenshot**: figure18.png
**Figure type**: diagram
**Extraction method**: visual_description
**Reading confidence**: high

## Visual description
- **Scenario**: fault branches = S9 and S22. Main network resumed supply.
- **Reconfiguration actions** (from text): two isolated islands form after reconstruction.
  Downstream of S9 contains DG2 (node 13), so S17 is disconnected and DG2 operates in island mode
  supplying nodes 10-16. Downstream of S22 contains DG3 (node 24), so contact switch S3 remains
  disconnected; DG3 operates in island mode supplying nodes 22-24. DG1 and DG4 connect to the
  remaining system to participate in recovery; switch S29 closed again; node 17 connects to remaining
  system through contact switch S36.
- **Connections**: green routing = energised paths; two islanded sub-regions around DG2 and DG3.
- **What it conveys**: a multi-fault case yielding a hybrid recovery (main-network reconnection plus
  two DG islands). Corresponds to Table 5 loss/voltage results.

Structure mirrored into logic/solution/method.md.
