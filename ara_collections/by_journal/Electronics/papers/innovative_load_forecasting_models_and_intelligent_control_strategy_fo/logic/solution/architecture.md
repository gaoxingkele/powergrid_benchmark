# Architecture

Reconstructed from Figures 1–5 (diagrams) and §3.3. Two recurrent architectures share a common pipeline; they differ in cell internals.

## Overall pipeline (Figure 1, graphical abstract)
- **Components**: Load Data → Dataset Preprocessing → Proposed Model → {LSTM branch, GRU branch} → Load Forecasting.
- **Connections**: raw load data (from heterogeneous sources: homes, buildings, industry) feeds preprocessing; preprocessed data feeds the proposed model, which routes through either the LSTM or GRU branch to produce the load forecast.
- **Design choice**: the two branches are alternative model choices evaluated in parallel, not stacked.

## LSTM cell (Figures 2 and 5)
- **Components**: Input → LSTM cell with three gates (input $i_t$, forget $f_t$, output $o_t$) → cell state $C_t$ (long-term memory) and hidden state $h_t$ (short-term memory) → fully connected layer → ReLU → dropout → output layer.
- **Connections**: cell state carried forward across timesteps (long-range memory); hidden state updated per timestep; unrolled across time (Figure 2 shows $C_0,C_1,C_2,\dots,C_t$ across timesteps 0..t).
- **Key design choice**: three-gate design gives separate long-term (cell) and short-term (hidden) memory paths; claimed added attention over the input sequence (not shown in the diagram equations).

## GRU cell (Figures 3 and 4)
- **Components**: Input $x_t$ → GRU cell with two gates (update $z_t$, reset $r_t$) → single hidden state $h_t$ → output.
- **Connections**: Figure 3 shows GRU cells chained (Input 1..x → GRU Cell → Hidden State → Output 1..x). Figure 4 shows internal data flow: input and previous hidden state feed sigmoid update/reset gates; reset gate modulates the tanh candidate; update gate combines previous hidden state ($1-z_t$ path) and candidate ($z_t$ path) into the new hidden state.
- **Key design choice**: single hidden state and two gates → fewer parameters than LSTM; claimed added dynamic/context-aware gating.

## Head (shared)
- Fully connected layer maps recurrent output to the next-timestamp load; ReLU introduces non-linearity; dropout prevents overfitting; output layer emits the scalar forecast.

## Notes
- Layer counts, hidden dimensions, number of hidden layers, dropout rate, and learning rate are discussed in §3 as tunable but **specific values are not specified in the paper**.
- The diagrams are schematic (structure only); no numeric parameters can be read from them.
