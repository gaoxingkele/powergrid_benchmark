# Figure 3: Batch Normalization

- **Source**: Figure 3, §4.1 (p.9)
- **Caption**: "Batch Normalization."
- **Screenshot**: figure3.png
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high
- **Location on page**: middle of the page, below Eq. 19.

## Visual description
- **Components (bottom→top)**: "K-1 Layer" (row of 5 neuron circles) → fully connected edges → a row
  of 4 "BN" boxes labeled "Batch Normalization" → "K Layer" (row of 4 neuron circles).
- **Connections**: Dense (all-to-all) connections from the K−1 layer neurons feed into the BN units;
  each BN unit outputs to a K-layer neuron.
- **Annotations**: The BN layer sits between two fully connected layers, normalizing the inputs to
  the K layer.
- **What it conveys**: BN is inserted between layers to normalize each mini-batch's activations
  (mean μ_P, variance σ_P², normalize, then scale γ and shift β per Eqs. 16–19) before the next
  layer. In this paper's model the BN layer is placed after the LSTM layer. Mirrored into
  logic/solution/architecture.md.
