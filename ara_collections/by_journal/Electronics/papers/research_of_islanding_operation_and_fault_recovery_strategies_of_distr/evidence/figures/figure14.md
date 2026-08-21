# Figure 14: Network reconfiguration result when the fault locates at line S28 and DG3

**Source**: Figure 14, Section 5.3.1, page 20
**Location on page**: top of page 20
**Caption**: "Network reconfiguration result when the fault locates at line S28 and DG3."
**Screenshot**: figure14.png
**Figure type**: diagram
**Extraction method**: visual_description
**Reading confidence**: high

## Visual description
- **Scenario**: fault branch = S28 AND DG3 (DG3 malfunctions). Main network has resumed supply
  (fault-recovery stage).
- **Reconfiguration actions** (from text): DG4 (node 31) present downstream, so switch S29 is turned
  OFF and DG4 switches to island operation. DG3 exits the system (stops supplying) and switch S22 is
  reconnected to the main network. DG1 (node 6) and DG2 (node 13) connect to the remaining system to
  participate in recovery. Node 28 connects to the main network through interconnection switch S37.
- **Connections**: green lines/paths = re-energised routing after reconfiguration; blue = normal
  feeder.
- **What it conveys**: how tie/segment switches are re-set to restore lost load and isolate the
  faulted S28/DG3 while a healthy DG (DG4) islands. Corresponds to Table 3 loss/voltage results.

Structure mirrored into logic/solution/method.md (fault-recovery reconfiguration).
