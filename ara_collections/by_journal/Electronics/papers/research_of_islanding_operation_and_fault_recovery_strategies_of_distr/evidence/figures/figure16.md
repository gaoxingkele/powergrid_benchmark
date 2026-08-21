# Figure 16: Network reconfiguration result when the fault locates at line S28

**Source**: Figure 16, Section 5.3.2, page 21
**Location on page**: top of page 21
**Caption**: "Network reconfiguration result when the fault locates at line S28."
**Screenshot**: figure16.png
**Figure type**: diagram
**Extraction method**: visual_description
**Reading confidence**: high

## Visual description
- **Scenario**: only line S28 is faulty (DG3 healthy). Main network resumed supply.
- **Reconfiguration actions** (from text): DG4 present downstream, so switch S29 turned OFF and DG4
  switches to island operation. DG1 and DG2 connect to the remaining systems to participate in
  recovery. Node 28 connects to the main network through interconnection switch S37. (Because DG3 is
  healthy here, it stays connected — this is the difference vs Figure 14, and reduces losses.)
- **Connections**: green routing paths = post-reconfiguration energised links.
- **What it conveys**: reconfiguration for a single-line fault where the DG at node 24 remains
  available, giving lower losses and higher minimum voltage than the S28+DG3 case (Table 4 vs Table 3).

Structure mirrored into logic/solution/method.md.
