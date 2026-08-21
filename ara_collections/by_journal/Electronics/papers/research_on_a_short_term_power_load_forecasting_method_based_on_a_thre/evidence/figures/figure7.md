# Figure 7: Three-channel LSTM-CNN combined model structure

- **Source**: Figure 7, Section 2.3, p8
- **Caption**: "Three-channel LSTM-CNN combined model structure."
- **Screenshot**: figure7.png (page 8; diagram in upper half of page)
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components**: Three parallel LSTM stacks at the bottom — LSTM 1 (Historical load), LSTM 2 (Meteorological environment), LSTM 3 (Time class), each an unrolled chain of LSTM units. Their outputs feed a middle block of three stacked neuron rows (LSTM1/LSTM2/LSTM3) that is **transposed** ("Transposition" label) and fed in the "Convolution direction" into the top pipeline: Conv → Conv → Maxpooling → FC → Prediction result. An "LSTM Unit" callout details one cell.
- **Connections**: Historical/Meteorological/Time inputs → respective LSTM channels → concatenated neuron matrix → transpose → 2× Conv1D → Maxpooling → FC → Prediction result. Arrows mark "Transposition" and "Convolution direction" (convolution runs across the three channels).
- **Annotations**: Dashed boxes group each LSTM channel and the top CNN pipeline; the convolution window spans the three channel rows.
- **What it conveys**: The paper's central contribution — independent per-modality LSTM encoding fused late by a CNN across channels (supports C01, C02). This is the backbone mirrored into logic/solution/architecture.md.
</content>
