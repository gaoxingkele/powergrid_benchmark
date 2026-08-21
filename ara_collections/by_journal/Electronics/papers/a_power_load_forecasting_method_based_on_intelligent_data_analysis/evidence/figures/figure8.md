# Figure 8: Visualization of model parameters

- **Source**: Figure 8, §5.2 (p.13)
- **Caption**: "Visualization of model parameters."
- **Screenshot**: figure8.png
- **Figure type**: diagram (per-layer input/output shape table)
- **Extraction method**: exact_from_labels (shapes are printed text in the diagram)
- **Reading confidence**: high
- **Location on page**: upper-middle of the page.

## Visual description (per-layer input/output shapes, top→bottom)
| Layer | Input | Output |
|-------|-------|--------|
| InputLayer | (None, 48, 1) | (None, 48, 1) |
| LSTM | (None, 48, 1) | (None, 81) |
| Batch Normalization | (None, 81) | (None, 81) |
| Dropout | (None, 81) | (None, 81) |
| Dense1 | (None, 81) | (None, 27) |
| Dense2 | (None, 27) | (None, 9) |
| Result | (None, 9) | (None, 1) |

- **Connections**: A vertical stack; each layer's output shape is the next layer's input shape.
- **What it conveys**: The concrete tensor shapes through the sub-model: 48-step univariate input →
  LSTM width 81 → BN/Dropout (81) → Dense 27 → Dense 9 → scalar output.
- **Internal discrepancy (noted)**: The prose in §5.2 states "The Dense layer is composed of 3
  layers, with the respective number of neurons being 27, 8, and 1." Figure 8 instead shows the
  middle dense layer (Dense2) with output width **9**, not 8. The two disagree on the middle dense
  layer size (8 vs 9); recorded verbatim from both sources, not resolvable from the paper.

Supports C01. Mirrored into logic/solution/architecture.md and src/configs/model.md.
