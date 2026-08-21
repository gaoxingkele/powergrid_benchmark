# Figure 8: One week power-load prediction results comparison

- **Source**: Figure 8, §4.3 (page 14, middle of page)
- **Caption**: "One week power-load prediction results comparison."
- **Screenshot**: figure8.png (full-page render of p.14; also contains Figures 7 and 9)
- **Figure type**: quantitative_plot
- **Extraction method**: digitized_estimate
- **Reading confidence**: medium (dense 200-step line plot without data labels; inset zoom on
  t = 0–10)
- **Plot kind**: line
- **Axes**: X = Time Step (h), linear, 0–200 (one week, hourly); Y = Power Load (MW), linear,
  ≈17–100
- **Series**: GCN-LSTM (blue), GRU (yellow), CNN-LSTM (teal), LSTM (dark khaki), Proposed model
  (red), Real (black); inset (bottom-left) magnifies the first ~10 hours

Point-level values are not reliably readable at this density; representative approximate features
of the Real curve: daily oscillation between deep troughs ≈17–20 MW (e.g., t≈38, t≈62, t≈87) and
peaks ≈80–100 MW (e.g., t≈5, t≈150, t≈172, t≈195); seven daily cycles are visible across the
200-hour span.

## Trend summary
Across all seven daily cycles the Proposed model (red) stays visually coincident with the Real
curve (black), including at deep troughs and sharp ramps. Baselines separate from the real curve
mainly around peaks and turning points: GRU overshoots the final peaks (t≈190–200, up to ≈98),
GCN-LSTM overshoots at t≈148–150, and all baselines wobble at the mid-week partial-peak clusters
(t≈70–90). The inset shows that even in the first 10 hours the baselines fan out at the first peak
while the proposed curve holds to the real one. Supports C01 (one-week horizon).
