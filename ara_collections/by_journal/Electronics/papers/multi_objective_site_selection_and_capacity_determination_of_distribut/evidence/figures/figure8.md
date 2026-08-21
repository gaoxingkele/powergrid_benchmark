# Figure 8: EVS output and SOC curve

- **Source**: Figure 8, Section 5 (Case Analysis), page 10
- **Caption**: "EVS output and SOC curve."
- **Screenshot**: figure8.png (two panels on page 10: (a) Energy storage device 1, (b) Energy storage device 2; panel Figure 7(c) also appears at the top of this rendered page)
- **Figure type**: quantitative_plot (2 panels, dual-axis bar + line)
- **Extraction method**: digitized_estimate
- **Reading confidence**: low

- **Plot kind**: bar (charge/discharge power) overlaid with line (SOC change curve), dual Y-axis
- **Panels / Axes**:
  - (a) Energy storage device 1: left Y = Power /Kwh (≈ -2 to 2, scaled ×10^-?), right Y = SOC /Kwh (≈0–0.8), X = Time /h (0–25)
  - (b) Energy storage device 2: left Y = Power /Kwh (≈ -1 to 1), right Y = SOC /Kwh (≈ -1 to 2.5), X = Time /h (0–25)
  - "Charge-discharge power" = bars (positive = charge, negative = discharge); "SOC change curve" = line.

## Trend summary
Both EV-cluster energy-storage devices alternate charge (positive bars) and discharge (negative bars) over the 24-hour horizon. Per the text, during the 10:00–15:00 window (high DG output) the devices hold their SOC range and charge to absorb surplus DG; when DG output is low they discharge to compensate. The SOC line rises during charging intervals and falls during discharging intervals, tracking the charge/discharge bars. Demonstrates the operational mechanism behind C01 — storage charges at DG surplus, discharges at DG deficit, smoothing net injection. Exact power/SOC values are not reliably readable (small scale factors, dense bars).
