# Figure 5: LSTM model structure diagram

- **Source**: Figure 5, Section 3.2, p. 10
- **Caption**: "LSTM model structure diagram."
- **Screenshot**: figure5.png
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components**: A single LSTM cell showing cell state Ct−1 → Ct along the top, hidden state ht−1 → ht along the bottom, input xt, and four gate activations (three σ sigmoid gates + one tanh) plus a tanh on the output path.
- **Connections**: Forget gate multiplies Ct−1; input gate × tanh candidate adds to cell state; output gate × tanh(Ct) yields ht. Corresponds to Eqs. (27)–(32).
- **What it conveys**: The classic LSTM gating (input it, forget ft, output ot gates) that regulates long/short-term memory in the cell state — the base unit that BiLSTM (Figure 6) runs bidirectionally.
