# Figure 20: Network reconfiguration result when the fault locates at line S28 (comparison method)

**Source**: Figure 20, Section 5.3.4, page 23
**Location on page**: bottom half of page 23
**Caption**: "Network reconfiguration result when the fault locates at line S28 (comparison method)."
**Screenshot**: figure20.png
**Figure type**: diagram
**Extraction method**: visual_description
**Reading confidence**: high

## Visual description
- **Scenario**: comparison / ablation. Same S28 fault and 20 h isolated operation, but the load
  weight uses the reduced form β_{i,k} = α_{i,k} (Eq. 36 with ξ1=ξ2=0), ignoring island-scheme
  changes and no-power periods during islanding.
- **Reconfiguration result**: node 28 does NOT receive power (unlike the proposed method in
  Figure 16). Nodes 28-onward on that branch are left unsupplied.
- **What it conveys**: the comparison method assigns excessive weight to switch actions and neglects
  the effect of intermittent supply during islanding on user satisfaction; node 6 experienced an
  outage->supply->outage sequence, so the proposed β design gives it higher recovery weight and
  restores it, whereas the baseline does not. This is the qualitative dead-end / baseline contrast
  behind claim on β design (Eq. 36).

Structure mirrored into logic/solution/method.md and logic/experiments.md (E-comparison).
