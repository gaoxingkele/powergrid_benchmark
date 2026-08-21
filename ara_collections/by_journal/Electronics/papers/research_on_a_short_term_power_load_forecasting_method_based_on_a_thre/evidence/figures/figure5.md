# Figure 5: Maximum pooling and average pooling processes

- **Source**: Figure 5, Section 2.2, p6
- **Caption**: "Maximum pooling and average pooling processes."
- **Screenshot**: figure5.png (page 6; diagram in lower-middle of page)
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components**: A 4×4 input matrix; two 2×2 output matrices — one for "Maximum pooling" and one labeled "Minimum pooling" (caption text says maximum/average; figure label reads "Minimum pooling").
- **Connections**: 2×2 pooling window, stride 2; each output cell aggregates its window (max → maxima; the second branch aggregates the window per its label).
- **Annotations**: Arrows labeled "Maximum pooling" and "Minimum pooling"; colored 2×2 quadrants.
- **What it conveys**: Pooling compresses feature-map dimensions. The paper's model uses 1-D **max** pooling (MaxPooling1D). Note: figure's second-branch label ("Minimum pooling") is inconsistent with the caption ("average pooling") — reproduced as printed.
</content>
