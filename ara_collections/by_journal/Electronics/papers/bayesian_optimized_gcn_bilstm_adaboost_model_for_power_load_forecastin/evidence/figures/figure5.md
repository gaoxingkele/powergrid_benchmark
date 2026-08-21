# Figure 5: BiLSTM structure

- **Source**: Figure 5, §2.3 (page 8, top of page)
- **Caption**: "BiLSTM structure."
- **Screenshot**: figure5.png (full-page render of p.8)
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components**: three unrolled time-step cells (dashed rounded boxes, for steps t−1, t, t+1),
  each containing:
  - a forward LSTM block (top row) producing $\overrightarrow{h}$, chained left-to-right (arrow
    labeled **Forward**);
  - a backward LSTM block (second row) producing $\overleftarrow{h}$, chained right-to-left (arrow
    labeled **Backward**);
  - an input node $x_t$ (yellow circle, bottom) feeding BOTH the forward and backward LSTM of its
    step;
  - a σ merge node (orange) combining $\overrightarrow{h}_t$ and $\overleftarrow{h}_t$ into the
    output $y_t$ (red circle, top).
- **Connections**: forward hidden states propagate t−1 → t → t+1; backward hidden states propagate
  t+1 → t → t−1; at every step the two directional hidden states are concatenated
  ($h_t = [\overrightarrow{h}_t, \overleftarrow{h}_t]$, Eq. 8) and passed through the output layer.
- **What it conveys**: each step's representation depends on both past and future context — the
  bidirectionality that lets the model capture, e.g., pre-holiday load adjustments (§1) — unlike a
  unidirectional LSTM. Mirrored into `logic/solution/architecture.md` (component 5) and
  `logic/concepts.md` (BiLSTM).
