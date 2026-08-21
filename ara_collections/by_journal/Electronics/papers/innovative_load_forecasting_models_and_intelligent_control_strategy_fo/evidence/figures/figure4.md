# Figure 4: Architecture of GRU

- **Source**: Figure 4, §3.4.1 (page 11, top)
- **Caption**: "Architecture of GRU."
- **Screenshot**: figure4.png
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components**: A single GRU cell interior — inputs "Hidden State, h_{t-1}" (left) and "Input, x_t" (bottom); internal blocks "Update Gate" and "Reset Gate" (sigmoid σ); "tanh" candidate block; elementwise operators (×, +, 1−); outputs "Output" (top) and "NEW Hidden state, h_t" (right).
- **Connections**: input and previous hidden state feed both the update and reset gates (sigmoid); the reset gate modulates (×) the tanh candidate branch; the update gate feeds a "1−" branch (×) combined (+) with the candidate branch (× by update gate) to form the new hidden state; new hidden state also routed to output.
- **Annotations**: red "X" = multiply, red "+" = add, "1−" = complement of update gate; yellow highlights the update-gate path, green the reset/candidate path.
- **What it conveys**: the internal dataflow implementing GRU Eqs. 5–8 (update gate, reset gate, candidate, hidden-state combination). Mirrored into architecture.md (GRU cell).
