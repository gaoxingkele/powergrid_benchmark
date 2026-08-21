# Figure 11: One-day forecasting result comparison (ablation variants)

- **Source**: Figure 11, §4.4 (page 15, lower half of page)
- **Caption**: "One-day forecasting result comparison."
- **Screenshot**: figure11.png (full-page render of p.15; also contains Figure 10)
- **Figure type**: quantitative_plot
- **Extraction method**: digitized_estimate
- **Reading confidence**: medium (line plot without data labels)
- **Plot kind**: line
- **Axes**: X = Time Step (h), linear, 0–29; Y = Power Load (MW), linear, ≈60–93
- **Series**: BiLSTM (yellow), GCN-BiLSTM (dark), GCN-BiLSTM-Adaboost (steel blue), Proposed
  model (red), Real (black)

Approximate readings (all ≈, digitized): Real rises from ≈62 (t=0) to a peak ≈93 (t≈5–6),
declines through ≈80 (t≈10) to a trough ≈68 (t≈15–16), then recovers to ≈75 (t≈18), plateaus
≈74–76, and climbs to ≈81 by t=29. At the peak, BiLSTM reads ≈88.5 (≈4.5 MW under real);
GCN-BiLSTM and GCN-BiLSTM-Adaboost read ≈91–92; the Proposed model overlaps the Real curve.

## Trend summary
The four variants form a visible accuracy ladder exactly at the load turning points (the daily
peak at t≈5–6, the trough at t≈15–16, and the evening inflection at t≈17–18): BiLSTM deviates
most, adding GCN tightens the peak, adding Adaboost tightens it further, and the full
Bayesian-weighted model is nearly indistinguishable from the real load even at the turning
points. Away from turning points (stable segments) all variants are close. This is the
qualitative core of C02/C04 (robustness at abrupt load changes comes from the ensemble
weighting stages) and pairs with the quantitative stagewise drop in Table 4.
