# Figure 13: Prediction results of different methods

- **Source**: Figure 13, Section 5.6, p. 18 (lower half of page)
- **Caption**: "Prediction results of different methods. (a) Prediction comparison for three specific days in the first month of the test set; (b) Prediction comparison for three specific days in the second month of the test set."
- **Screenshot**: figure13.png (page 18; two-panel plot (a)/(b) below Table 5)
- **Figure type**: quantitative_plot
- **Extraction method**: digitized_estimate
- **Reading confidence**: medium

- **Plot kind**: line (multi-day forecast vs measured, two months)
- **Axes**: X = Time / 15 min, linear, 0–≈300 (three days). Y = Electrical Load / MW, linear — panel (a) ≈7000–11500 MW; panel (b) ≈0.8×10⁴–1.25×10⁴ MW.
- **Series (both panels)**: ELM; LSTM; BiLSTM; TCN-BiLSTM; Measured Data. All fed the same SBOA-SVMD IMFs.

## Trend summary
Both panels show three daily double-peak cycles. TCN-BiLSTM tracks Measured Data most closely (best at peaks/troughs and abrupt changes). BiLSTM is next-best but deviates on sharp changes. ELM reflects the overall trend but under-predicts in high-change regions. LSTM is worst, struggling at peaks/troughs and rapid fluctuations. Visual ranking (TCN-BiLSTM > BiLSTM > ELM > LSTM) matches Table 6 metric ordering. Exact values not label-printed.
