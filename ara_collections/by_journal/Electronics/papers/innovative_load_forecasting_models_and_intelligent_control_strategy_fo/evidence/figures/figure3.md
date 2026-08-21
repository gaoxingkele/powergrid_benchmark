# Figure 3: GRU cells

- **Source**: Figure 3, §3.3.1 (page 8)
- **Caption**: "GRU cells."
- **Screenshot**: figure3.png
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components**: A chain of GRU cells (green boxes) labelled "GRU Cell"; each takes an "Input 1", "Input 2", ..., "Input x" (bottom), maintains a "Hidden State" (blue oval), and emits "Output 1", "Output 2", ..., "Output x" (top).
- **Connections**: input → GRU cell → hidden state → output; hidden state passed rightward to the next cell (chained across the sequence, indicated by the dotted arrow between cell 2 and cell x).
- **Annotations**: sequence indices 1, 2, ..., x for inputs/outputs.
- **What it conveys**: the GRU processes the sequence step-by-step, threading a single hidden state through the chain to produce per-step outputs — basis for the hidden-state update Eq. 4/Eq. 8. Mirrored into architecture.md (GRU cell).
