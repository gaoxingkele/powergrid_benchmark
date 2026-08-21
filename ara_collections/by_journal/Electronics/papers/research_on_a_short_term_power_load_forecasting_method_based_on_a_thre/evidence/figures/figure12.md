# Figure 12: Load residuals of different models in the Electrician's Cup dataset

- **Source**: Figure 12, Section 4, p13
- **Caption**: "Load residuals of different models in the Electrician's Cup dataset."
- **Screenshot**: figure12.png (page 13; lower plot on the page)
- **Figure type**: quantitative_plot
- **Extraction method**: digitized_estimate
- **Reading confidence**: medium
- **Plot kind**: bar (stacked/overlaid per-model residual magnitudes over time)
- **Axes**: X = Time (Hour, linear, 0–24), Y = Electrical load residuals (MW, linear, 0–6,500)

| Time (Hour) | LSTM residual | TCN residual | Three-channel (LSTM-CNN, red) |
|-------------|---------------|--------------|-------------------------------|
| 1  | tall, ≈3,800 (peak) | ≈1,400 | ≈800 |
| 4–9 | low, ≈300–1,300 | low | lowest, ≈200–400 |
| 11–14 | ≈1,800–3,100 | ≈900–1,300 | ≈300–700 |
| 16–24 | ≈1,000–1,700 | small | small |

## Trend summary
LSTM residuals are largest (peaking ≈3,800 MW at hour≈1 and elevated near midday hours 11–14); TCN
(green) intermediate; the three-channel LSTM-CNN (red) has the smallest, most stable residuals
across the day. Legend lists LSTM, LSTM-CNN, TCN, LSTM-CNN (the "LSTM-CNN" label is repeated for two
series — reproduced as printed). Supports C06 (E05). Directional reading only; residuals not
tabulated in the paper.
</content>
