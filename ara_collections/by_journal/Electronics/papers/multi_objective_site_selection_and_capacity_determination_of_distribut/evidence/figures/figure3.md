# Figure 3: A schematic diagram of Bi-LSTM

- **Source**: Figure 3, Section 4.1 (Data Processing Process of EV Cluster), page 6
- **Caption**: "A schematic diagram of Bi-LSTM."
- **Screenshot**: figure3.png (lower diagram on page 6; note figure2.png and figure3.png share page 6 — figure 3 is the lower unrolled-network diagram)
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components**: Input layer (x_{t-1}, x_t, x_{t+1}), a Forward LSTM chain (hidden states h_{i-1}, h_i, h_{i+1}), a Reverse LSTM chain (hidden states h_{t-1}, h_t, h_{t+1}), and an Output layer (y_{t-1}, y_t, y_{t+1}).
- **Connections**: forward LSTM passes hidden state left→right (solid red arrows); reverse LSTM passes hidden state right→left (dashed blue arrows); each output y_t combines the forward and reverse hidden states at time t.
- **Annotations**: two parallel recurrent passes over the same input sequence in opposite temporal directions.
- **What it conveys**: bidirectional temporal modeling — each prediction sees both past and future context, which the paper argues improves EV-cluster state prediction over a unidirectional LSTM. Combined with Figure 2 this forms the CNN-BiLSTM model. Mirrored in `logic/solution/method.md`.
