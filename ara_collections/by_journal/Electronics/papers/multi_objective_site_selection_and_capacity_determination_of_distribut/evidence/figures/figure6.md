# Figure 6: A comparison of data from different algorithms

- **Source**: Figure 6, Section 5 (Case Analysis), page 8
- **Caption**: "A comparison of data from different algorithms."
- **Screenshot**: figure6.png (three stacked panels on page 8)
- **Figure type**: quantitative_plot (three panels: a, b, c)
- **Extraction method**: digitized_estimate (curves overlap densely; only trends are reliably readable)
- **Reading confidence**: low
- **Series compared**: True value, CNN, BiLSTM, CNN-BiLSTM (predictions vs ground truth over 40 test samples)

- **Plot kind**: line (prediction vs test-sample index)
- **Panels / Axes**:
  - (a) EV inbound (arrival) time: X = Test samples (0–40), Y = "The inbound time of the EV/t" (≈15–21 h), linear
  - (b) EV outbound (departure) time: X = Test samples (0–40), Y = "The outbound time of the EV" (≈4–14 h), linear
  - (c) Initial SOC of the EV: X = Test samples (0–40), Y = "Initial SOC for EVs" (≈0.4–0.75), linear

## Trend summary
Across all three predicted EV-cluster quantities (arrival time, departure time, initial SOC), the CNN-BiLSTM prediction curve tracks the True-value curve more closely than the standalone CNN or standalone BiLSTM curves, which show larger point-wise deviations from ground truth. Exact per-sample values are not extractable (dense overlapping markers), but the qualitative ordering — CNN-BiLSTM closest to truth — is the point the paper draws. The paper's quantitative summary (§6 conclusion (2), p.11, verbatim): "The CNN-BiLSTM algorithm used in this paper can further reduce the data error of EV, which is 10.2% higher than the ordinary CNN method and 8.3% higher than that of the Bi-LSTM algorithm."

Supports the claim that bidirectional temporal modeling plus convolutional feature extraction lowers EV-state prediction error relative to either component alone.
