# Figure 10: Analysis of the load residual in the power data set of Tétouan City

- **Source**: Figure 10, Section 4, p12
- **Caption**: "Analysis of the load residual in the power data set of Tétouan City."
- **Screenshot**: figure10.png (page 12; lower plot on the page)
- **Figure type**: quantitative_plot
- **Extraction method**: digitized_estimate
- **Reading confidence**: medium
- **Plot kind**: bar (stacked/overlaid per-model residual magnitudes over time)
- **Axes**: X = Time (10 min intervals, linear, 0–150), Y = Electrical load residuals (kW, linear, 0–13,000)

| Region | LSTM residual | TCN residual | Three-channel (LSTM-CNN, red) |
|--------|---------------|--------------|-------------------------------|
| x≈0–30 (stable) | ≈500–2,000 | ≈300–1,500 | lowest, mostly < ≈1,000 |
| x≈35–55 (volatile) | tallest, up to ≈8,500 peak | ≈1,500–3,000 | lowest, mostly < ≈1,000 |
| x≈75–110 | intermittent ≈2,000–5,000 | moderate | lowest |

## Trend summary
Residual magnitude is largest for LSTM (darkest bars, peaking ≈8,500 kW around x≈45), smaller for
TCN (green), and smallest/most stable for the three-channel LSTM-CNN (red), whose residuals are
"mostly less than 1000 kW" per §4 even at hard-to-predict volatile regions. The legend lists LSTM,
LSTM-CNN, TCN, LSTM-CNN (the paper's legend repeats "LSTM-CNN" for two series — reproduced as
printed). Supports C06 (E04). Directional reading only; exact residuals not tabulated in the paper.
</content>
