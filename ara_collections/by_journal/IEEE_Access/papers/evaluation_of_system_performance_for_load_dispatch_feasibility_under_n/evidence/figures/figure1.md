# Figure 1: Proposed methodology for the system performance assessment of n-1 contingency based DA UC

- **Source**: Figure 1, §II/§III (p.181185)
- **Caption**: "Proposed methodology for the system performance assessment of n-1 contingency based DA UC."
- **Screenshot**: figure1.png (top-right column of the page)
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components (top→bottom flow)**:
  1. "Forced outage of single generating unit (n-1 generator contingency)"
  2. "For feasible DA UC under above contingency (as per forecasted load demand)"
  3. Two parallel branches:
     - Left: "Identify stable contingencies" → "Identify robust buses" → *System Robustness*
     - Right: "Identify critical contingencies" → "Identify weak buses" → *System Criticality*
  4. "System Reliability estimation"
  5. "System Operating Reliability margin"
- **Connections**: single downward flow that forks into the robustness/criticality branches, then
  reconverges into reliability estimation and finally the operating reliability margin.
- **Annotations**: the robustness branch and criticality branch are grouped/labeled separately.
- **What it conveys**: the paper's pipeline — from a single-unit outage, classify contingencies into
  stable (→robust buses→robustness) vs critical (→weak buses→criticality), then estimate reliability
  and the operating margin. Mirrored in `logic/solution/method.md`.
