# Figure 11: Comparison of prediction results with different sequence decomposition algorithms

- **Source**: Figure 11, Section 5.5, p. 16 (bottom of page)
- **Caption**: "Comparison of prediction results with different sequence decomposition algorithms."
- **Screenshot**: figure11.png (page 16; Figure 11 is the load-curve plot at the bottom, below Table 3)
- **Figure type**: quantitative_plot
- **Extraction method**: digitized_estimate
- **Reading confidence**: medium

- **Plot kind**: line (one day of forecast vs measured, overlaid)
- **Axes**: X = Time / 15 min, linear, 0–≈96. Y = Electrical Load / MW, linear, ≈7500–10000+.
- **Series**: Measured Data; SBOA-SVMD-TCN-BiLSTM; CEEMDAN-TCN-BiLSTM; ICEEMDAN-TCN-BiLSTM.

## Trend summary
Daily double-peaked load curve. The SBOA-SVMD-TCN-BiLSTM curve tracks the Measured Data most closely across the whole day, especially at peaks/troughs; CEEMDAN and ICEEMDAN curves deviate more (visibly under/overshooting around the peaks). Supports the ranking quantified in Table 4 (SBOA-SVMD lowest MAE/RMSE). Exact values not label-printed.
