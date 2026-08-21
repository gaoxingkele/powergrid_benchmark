# Figure 2: Block diagram of a GA

- **Source**: Figure 2, Section 3 (AI Techniques—Genetic Algorithms), page 7
- **Caption**: "Block diagram of a GA."
- **Screenshot**: figure2.png (top flowchart on page 7; the network diagram Figure 3 is lower on the same page)
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components (flowchart nodes, top→bottom)**: START → INITIALIZE POPULATION → ENCODE → SELECTION →
  CROSSOVER → EVALUATE → REPLACE → decision "TERMINATION CRITERION MET?" → (YES) STOP.
- **Connections**: Sequential single-path flow through the operators; the decision node branches
  "NO" back via a loop edge to re-enter the SELECTION→CROSSOVER→EVALUATE→REPLACE cycle, and "YES"
  proceeds to STOP.
- **Annotations**: Rounded terminators (START/STOP), rectangular process blocks (operators), a
  diamond decision block for the termination test.
- **What it conveys**: The canonical GA loop used in the paper — population init and binary encoding,
  then iterated selection/crossover/evaluation/replacement until a termination criterion (no
  significant improvement in mean error, or generations exceed N_max). Mirrors the prose in
  Section 3 and grounds `logic/solution/algorithm.md`.
- **Supports**: C01 (method framing); grounds the pseudocode/flow in algorithm.md.
