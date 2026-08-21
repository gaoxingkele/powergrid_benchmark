# Figure 3

**Source:** `evidence/figures/figure3.png`

**Caption:** Figure 3. Overall framework of BiLSTM-Transformer-DAF (DAF-BT).

**Figure type:** Diagram

**Extraction Method:** Direct crop from paper PDF.

**Reading Confidence:** High — full proposed architecture diagram.

**Structured Description:**

The figure presents the complete DAF-BT architecture as a block diagram with data flow arrows. The processing pipeline is:

1. **Input Layer:** Multi-dimensional time series input comprising load, temperature, and wind speed features at 0.5h intervals.
2. **N-Space Transformation:** Feature embedding/projection into higher-dimensional representation space.
3. **BiLSTM Layer:** Bidirectional LSTM processing the embedded sequence in both forward and backward directions, producing concatenated hidden states at each time step that capture local bidirectional dependencies.
4. **Transformer Encoder with Local Enhanced Attention:** Processes BiLSTM outputs through self-attention with a local mask matrix M, constraining attention to a neighborhood window while maintaining global pattern capture through residual connections.
5. **DAF Module:** Receives features from both the BiLSTM and Transformer branches. Contains two parallel sub-units:
   - Feature Channel Adaptive Unit (computes ω_c)
   - Temporal Contribution Evaluation Unit (computes ω_t)
   - Synergistic fusion combining weighted features with nonlinear interaction term
6. **Output Layer:** Linear projection to produce the final load forecast.

The diagram emphasizes the parallel information pathways feeding into the DAF module and the adaptive weighting mechanism that distinguishes this architecture from static fusion approaches.
