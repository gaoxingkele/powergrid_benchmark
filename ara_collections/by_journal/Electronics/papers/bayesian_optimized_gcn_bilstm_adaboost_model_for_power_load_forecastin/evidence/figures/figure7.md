# Figure 7: One day power-load prediction results comparison

- **Source**: Figure 7, §4.3 (page 14, upper third of page)
- **Caption**: "One day power-load prediction results comparison."
- **Screenshot**: figure7.png (full-page render of p.14; also contains Figures 8–9)
- **Figure type**: quantitative_plot
- **Extraction method**: digitized_estimate
- **Reading confidence**: medium (line plot without data labels)
- **Plot kind**: line
- **Axes**: X = Time Step (h), linear, 0–29; Y = Power Load (MW), linear, ≈62–93
- **Series**: GCN-LSTM (blue), GRU (yellow), CNN-LSTM (teal), LSTM (dark khaki), Proposed model
  (red), Real (black)

Approximate readings of the Real curve (all values ≈, digitized from the plot):

| Time step (h) | Real load (MW) |
|---------------|----------------|
| 0 | ≈62 |
| 1 | ≈79 |
| 5–6 (peak) | ≈93 |
| 8 | ≈88.5 |
| 11–12 | ≈78 |
| 15–16 (trough) | ≈68 |
| 18 | ≈75 |
| 19–21 | ≈74 |
| 25 | ≈78 |
| 29 | ≈81 |

## Trend summary
All models track the daily shape (morning ramp → mid-day peak at t≈5–6 → afternoon decline →
trough at t≈15–16 → evening recovery). The Proposed model (red) overlaps the Real curve (black)
almost everywhere, including at the peak and the trough turning points. LSTM undershoots the peak
worst (≈87 vs ≈93 real, ≈6 MW low); GRU and CNN-LSTM undershoot by ≈3–4 MW; GCN-LSTM is closest
among baselines but deviates at t≈11–13 and t≈21–23. Supports C01 (proposed model visually hugs
the real curve more tightly than every single-model baseline on the one-day horizon).
