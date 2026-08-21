# Figure 12: Comparison of prediction models with and without decomposition algorithms

- **Source**: Figure 12, Section 5.6, p. 17 (lower half of page)
- **Caption**: "Comparison of prediction models with and without decomposition algorithms."
- **Screenshot**: figure12.png (page 17; Figure 12 is the load-curve plot below Table 4)
- **Figure type**: quantitative_plot
- **Extraction method**: digitized_estimate
- **Reading confidence**: medium

- **Plot kind**: line (one day forecast vs measured)
- **Axes**: X = Time / 15 min, linear, 0–≈100. Y = Electrical Load / MW, linear, ≈8000–11000.
- **Series**: Measured Data; TCN-BiLSTM (no decomposition, raw load input); SBOA-SVMD-TCN-BiLSTM (proposed).

## Trend summary
Double-peaked daily curve. The SBOA-SVMD-TCN-BiLSTM curve hugs the Measured Data much more closely (both peaks and the mid-day trough), while plain TCN-BiLSTM systematically under-predicts, especially at peaks. Visually demonstrates the necessity of the SBOA-SVMD decomposition step; quantified in Table 5. Exact values not label-printed.
