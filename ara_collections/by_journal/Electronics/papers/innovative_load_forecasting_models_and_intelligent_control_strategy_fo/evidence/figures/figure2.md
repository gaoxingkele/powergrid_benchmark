# Figure 2: Modified LSTM

- **Source**: Figure 2, §3.3.1 (page 7)
- **Caption**: "Modified LSTM."
- **Screenshot**: figure2.png
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components**: An LSTM cell (green box) unrolled across timesteps; outputs C0, C1, C2, ..., Ct (orange circles) at the top; an input source f(t) (yellow) at the left; a time axis 0, 1, 2, ..., t at the bottom with a red dashed curve tracing the input signal over time.
- **Connections**: the folded LSTM cell "Unroll"s into a left-to-right chain of LSTM cells; each cell emits an output C_i and passes state to the next; the red dashed line depicts the temporal input trajectory feeding successive timesteps.
- **Annotations**: "Unroll" label between the folded and unfolded views; timestep axis labelled "Timestep".
- **What it conveys**: the LSTM processes a sequence by unrolling over time, carrying state across timesteps to produce per-step outputs — the structural basis for the cell-state update Eq. 3/Eq. 12. Mirrored into architecture.md (LSTM cell).
