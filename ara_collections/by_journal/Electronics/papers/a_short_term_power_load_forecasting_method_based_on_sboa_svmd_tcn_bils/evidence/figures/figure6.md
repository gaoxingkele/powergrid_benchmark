# Figure 6: BiLSTM model structure diagram

- **Source**: Figure 6, Section 3.2, p. 11 (top of page)
- **Caption**: "BiLSTM model structure diagram."
- **Screenshot**: figure6.png
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components**: Inputs xt−1, xt, xt+1 at bottom; a forward LSTM chain (ht−1 → ht → ht+1, left→right) and a backward LSTM chain (hi+1 ← hi ← hi−1, right→left); outputs yt−1, yt, yt+1 at top.
- **Connections**: Each output yt is formed from both the forward hidden state ht and the backward hidden state hi at that step; each hidden node combines the current input xt with the previous forward state ht−1 and previous backward state hi−1.
- **What it conveys**: BiLSTM processes the sequence in both directions so each prediction draws on past and future context — the temporal-modeling head applied to each IMF after TCN.
