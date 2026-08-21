# Figure 5: Model architecture of the LSTM-based user load prediction

- **Source**: Figure 5, §4.3 (p.10)
- **Caption**: "Model architecture of the LSTM-based user load prediction."
- **Screenshot**: figure5.png
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high
- **Location on page**: lower-middle of the page, above Section 5.

## Visual description
- **Components**:
  - Top: an unrolled **LSTM chain** — repeated LSTM cells indexed by inputs x0, x1, …, xt, each cell
    showing the standard internal gates (σ, σ, tanh, σ with weights W_f, W_i, W_c, W_o; ×, +, tanh
    operators) carrying cell state c and hidden state h from c0/h0 to ct/ht.
  - Bottom: a left-pointing pipeline of boxes — **Batch Normalization → Dropout → Dense → Dense →
    Result** — fed from the LSTM's final hidden state ht.
- **Connections**: The LSTM's last-time-step output (ht) flows down into Batch Normalization, then
  Dropout, then two Dense layers, then Result (the prediction). Arrows in the bottom row point
  right→left ending at "Result".
- **Annotations**: The unrolled cells share weights across the 48 time steps; only the last step's
  output is used as the feature.
- **What it conveys**: The per-component sub-model: LSTM encoder (last-step output) → BN → Dropout →
  Dense layers → single predicted value. Each IMF/residual component gets its own such sub-model,
  run in parallel. Supports C01. Mirrored into logic/solution/architecture.md. (Figure 8 gives the
  concrete per-layer sizes.)
