# Figure 12: One-week prediction result (with 95% confidence interval)

- **Source**: Figure 12, §4.4 (page 16, middle of page)
- **Caption**: "One-week prediction result."
- **Screenshot**: figure12.png (full-page render of p.16; also contains Table 4)
- **Figure type**: quantitative_plot
- **Extraction method**: digitized_estimate
- **Reading confidence**: medium (dense 200-step line plot; band edges approximate)
- **Plot kind**: line (with shaded uncertainty band)
- **Axes**: X = Time Step (h), linear, 0–200; Y = Power Load (MW), linear, ≈15–105
- **Series**: Actual Value (blue), Predicted Value (red), 95% Confidence Interval (gray shaded
  band). Plot title inside the figure: "GCN-BiLSTM-Adaboost with Bayesian Uncertainty and
  Confidence Intervals".

Point-level values are not reliably readable at this density; representative approximate
features: load oscillates daily between troughs ≈17–20 MW and peaks ≈80–100 MW over the 200-h
window; the band half-width is ≈3–5 MW on stable segments and visibly widens (≈8–12 MW) around
the high peaks, most prominently at t≈165–200.

## Trend summary
The predicted mean (red) tracks the actual load (blue) closely across all seven daily cycles —
the two curves are nearly coincident, consistent with the week-level errors in Table 4. The
actual curve stays inside the shaded 95% interval essentially everywhere, and the interval
inflates exactly where prediction is hardest (sharp high peaks), i.e., the MC-Dropout variance
is largest at volatile segments. §4.4 states the full model run takes 5 min and 56 s. Together
these support C05: the model emits a point forecast plus a risk-quantification band, with
coverage asserted from construction (not calibration-tested — see constraints item 8).
