# Figure 1: TSTG Overall Framework

**Source:** `evidence/figures/figure1.png`

**Caption:** "Overview of the proposed TSTG framework for short-term multi-energy load forecasting."

**Figure type:** Diagram

**Extraction method:** Screenshot from PDF page 5

**Reading confidence:** High — the diagram is a clear architectural block diagram in the paper.

## Structured Visual Description

The figure shows an encoder-decoder architecture diagram arranged vertically:

1. **Input layer (bottom):** A block labeled "Historical Multi-Energy Load Data" with dimensions N x T x D, feeding into an embedding layer.

2. **Encoder (middle left):** A stack of L identical layers, each consisting of two sub-modules:
   - "Multi-head Spatio-Temporal Attention Module" (rounded rectangle)
   - "Dynamic Adaptive Graph Convolution Module" (rounded rectangle)
   - Skip connections and layer normalization around each sub-module

3. **Decoder (middle right):** Similar L layers as the encoder, with an additional cross-attention connection from the encoder output. The decoder takes "Target Sequence Embedding" as input.

4. **Output layer (top):** A linear projection producing "Multi-Energy Load Forecast" with dimensions N x T' x D.

5. **Arrows:** Directed arrows show the data flow from input -> encoder -> decoder -> output. Curved arrows indicate skip connections. A dashed arrow from encoder output to decoder cross-attention is labeled "Memory".

6. **Labels:** Clear text labels for each component, plus annotations for "Spatio-Temporal Joint Optimization" spanning both modules.

No data values, axes, or numerical information are present.
