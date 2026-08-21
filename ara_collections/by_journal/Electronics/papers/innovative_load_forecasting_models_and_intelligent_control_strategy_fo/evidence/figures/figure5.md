# Figure 5: Architecture of LSTM

- **Source**: Figure 5, §3.4.1 (page 11, bottom)
- **Caption**: "Architecture of LSTM."
- **Screenshot**: figure5.png
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components**: A single LSTM cell interior — inputs "Cell State / Long-term Memory" (top-left), "Hidden State / Short-term Memory" (bottom-left), and "Input" (bottom); internal sigmoid gates (forget, input, output) and tanh blocks; elementwise operators (×, +); outputs "Output" (top), "NEW Cell state" (right), "NEW Hidden state" (right).
- **Connections**: cell state passes along the top with a forget-gate multiply (×) then an input-gate/candidate add (+); the input gate (sigmoid) × tanh candidate feeds the cell-state add; output gate (sigmoid) × tanh(cell state) produces the new hidden state; new cell state and hidden state exit right.
- **Annotations**: red "X" = multiply, red "+" = add; "sigmoid" and "tanh" activation blocks; separate long-term (cell) and short-term (hidden) memory paths.
- **What it conveys**: internal dataflow implementing LSTM Eqs. 9–14 (input/forget/output gates, candidate, cell-state update, hidden state). Mirrored into architecture.md (LSTM cell).
