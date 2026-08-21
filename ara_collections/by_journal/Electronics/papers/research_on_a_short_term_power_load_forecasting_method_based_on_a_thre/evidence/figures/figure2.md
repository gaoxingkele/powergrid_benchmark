# Figure 2: LSTM neural network structure

- **Source**: Figure 2, Section 2.1, p4
- **Caption**: "LSTM neural network structure."
- **Screenshot**: figure2.png (page 4; diagram in upper-middle of page)
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components**: A single LSTM cell showing inputs $C_{t-1}$ (previous cell state), $y_{t-1}$ (previous hidden output), $x_t$ (current input); three gates with Sigmoid ($\delta$) activations — forget $f_t$, input $i_t$, output $o_t$ — plus a `tanh` candidate branch; multiplicative ($\times$) and additive nodes; outputs $c_t$ (new cell state) and $y_t$ (hidden output).
- **Connections**: $C_{t-1}$ modulated by forget gate then combined with input-gate·candidate to form $c_t$; $c_t$ passed through `tanh` and gated by $o_t$ to yield $y_t$. Each gate takes $[x_t, y_{t-1}]$ with weights $w$ and biases $b$.
- **Annotations**: $\delta$ = Sigmoid activation; gate weights/biases labeled $w_f b_f$, $w_i b_i$, $w_c b_c$, $w_0 b_0$.
- **What it conveys**: The gating mechanism (Eqs. 1–6) that lets LSTM selectively retain/forget memory and handle long-term dependencies. Mirrored into logic/solution/method.md §2.
</content>
