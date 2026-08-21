# Figure 4: LSTM structure

- **Source**: Figure 4, §2.3 (page 7, middle of page)
- **Caption**: "LSTM structure."
- **Screenshot**: figure4.png (full-page render of p.7)
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components** (one LSTM cell, dashed boundary):
  - Inputs: cell state $C_{t-1}$ (top-left, dark blue), hidden state $h_{t-1}$ (mid-left, light
    blue), input $x_t$ (bottom, yellow).
  - Gate blocks (pink) each fed by $[h_{t-1}, x_t]$: forget gate $f_t$ via σ (Eq. 2), input gate
    $i_t$ via σ (Eq. 3), candidate state $\tilde{C}_t$ via tanh (Eq. 4), output gate $o_t$ via σ
    (Eq. 6).
  - Operation nodes (yellow circles): × (Hadamard product) and + (elementwise addition).
- **Connections**: $C_{t-1}$ × $f_t$ → (+) ← ($i_t$ × $\tilde{C}_t$) → new cell state $C_t$
  (Eq. 5, top-right); $C_t$ → tanh → × with $o_t$ → hidden output $h_t$ (Eq. 7, bottom-right).
- **Annotations**: σ and tanh activation bubbles (orange) under each gate; arrows show the
  left-to-right flow of the cell state along the top "conveyor".
- **What it conveys**: the gating mechanism (forget/input/output) by which LSTM controls what is
  discarded, stored, and emitted at each time step — the basis of the BiLSTM temporal extractor
  (Eqs 2–7). Structure mirrored into `logic/solution/architecture.md` (component 5).
