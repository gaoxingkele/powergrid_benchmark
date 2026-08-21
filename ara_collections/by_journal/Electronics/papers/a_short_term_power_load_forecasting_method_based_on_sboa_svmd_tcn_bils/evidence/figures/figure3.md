# Figure 3: TCN dilated causal convolution structure

- **Source**: Figure 3, Section 3.1, p. 9 (top of page)
- **Caption**: "TCN dilated causal convolution structure."
- **Screenshot**: figure3.png
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components**: Stacked layers Input layer → Hidden layer → Hidden layer → Output layer, with inputs x0 … xt at the bottom and output yt at the top.
- **Annotations**: Dilation factor grows across layers: p = 1 (input→hidden), p = 2 (hidden→hidden), p = 4 (hidden→output); convolution kernel size k = 2 at each level.
- **Connections**: Each output node connects only to current and earlier inputs (causal); dilation skips increase the receptive field exponentially without pooling.
- **What it conveys**: Dilated causal convolutions expand the receptive field (1→2→4) with fixed kernel k=2, letting TCN capture long-range dependencies while preserving causality (no future leakage).
