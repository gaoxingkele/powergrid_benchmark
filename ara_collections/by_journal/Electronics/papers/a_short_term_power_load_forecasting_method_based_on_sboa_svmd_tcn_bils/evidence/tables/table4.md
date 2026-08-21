# Table 4: Comparison of prediction errors between different decomposition methods

- **Source**: Table 4, Section 5.5, p. 17
- **Caption**: "Comparison of prediction errors between different decomposition methods."
- **Screenshot**: table4.png (page 17; PNG renders the page whose top holds Table 4, and whose lower half holds Figure 12)
- **Extraction type**: raw_table

| Model | MAE/MW | RMSE/MW | R²/% |
|-------|--------|---------|------|
| CEEMDAN-TCN-BiLSTM | 309.5300 | 402.4907 | 0.8854 |
| ICEEMDAN-TCN-BiLSTM | 267.1721 | 369.5974 | 0.9063 |
| SBOA-SVMD-TCN-BiLSTM | 219.7098 | 309.2698 | 0.9273 |

Text-stated deltas for SBOA-SVMD vs the two baselines: MAE reduced 29.01% (vs CEEMDAN) and 23.16% (vs ICEEMDAN); RMSE reduced 17.76% and 16.32% respectively. (R²/% column header printed as percentages but values are the raw R² fraction 0–1.)
