# Figure 3: Methodological framework to evaluate system performance

- **Source**: Figure 3, §V (p.181189)
- **Caption**: "Methodological framework to evaluate system performance."
- **Screenshot**: figure3.png (top-left column of the page)
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components (top→bottom)**:
  - "Simulate DA UC by DP, on IEEE RTS at full load, without n-1 generator contingencies" → labeled **Base Case** → outputs: "i) DA UC cost without n-1 generator contingencies; ii) Generator bus Ranking"
  - "Create n-1 generator contingencies." → "Perform n-1 generator contingency based DA UC" → two labeled outcomes:
    - **Case 1**: "i) Evaluate DA UC costs; ii) Find weak generator buses with CM of 310.5 MW"
    - **Case 2**: "i) Evaluate DA UC costs; ii) Find weak generator buses with CM of 248 MW, 155 MW and zero MW for Cases 2(a), 2(b) and 2(c)"
  - Grouped label: "n-1 generator contingency based DA UC Analysis to determine criticality and robustness as per the proposed methodology"
  - "Determine the system criticality (i.e. critical contingencies and weak buses) and system robustness (i.e. stable contingencies and robust buses)"
  - "Evaluate LOLP considering single generator outages" → "Find the reliability of the system for the 24 hours of the next day, for Case 1 and Case 2(a),(b),(c)" and "Find the operating margin of the system for the 24 hours of the next day, for Case 1 and Case 2(a),(b),(c)"
  - Grouped label: "LOLP based Reliability, operating margin estimation"
- **Connections**: Base Case → contingency-based analysis (Case 1, Case 2) → criticality/robustness → LOLP reliability + operating margin.
- **Annotations**: two-stage structure — Stage 1 (criticality/robustness vs Base Case), Stage 2 (LOLP + margin validation).
- **What it conveys**: the full 3-case, 2-stage evaluation pipeline. Mirrored in `logic/solution/method.md`.
