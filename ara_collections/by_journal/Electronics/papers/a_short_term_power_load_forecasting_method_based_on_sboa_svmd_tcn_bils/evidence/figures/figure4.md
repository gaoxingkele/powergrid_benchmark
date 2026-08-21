# Figure 4: TCN residual unit

- **Source**: Figure 4, Section 3.1, p. 9 (lower half of page)
- **Caption**: "TCN residual unit."
- **Screenshot**: figure4.png (same page as Figure 3; Figure 4 is the lower block diagram)
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components**: Two stacked convolution sub-blocks, each a sequence: Dilated causal convolution → Weight normalization → Activation function (ReLU) → Dropout operation. A parallel "Nonlinear mapping" (1×1 conv) branch bypasses the two sub-blocks.
- **Connections**: Input x feeds the first sub-block; output of the second sub-block f(x) is added to the (nonlinearly mapped) identity of x to give h(x). Residual relation printed as Eq. (26): f(x) = h(x) − x.
- **What it conveys**: The residual unit stacks two dilated-causal-conv blocks with weight-norm, ReLU and dropout, plus a skip connection (nonlinear mapping) to stabilise deep training and mitigate vanishing gradients.
