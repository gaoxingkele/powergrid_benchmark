# Table 5: Comparison of prediction errors between models with and without decomposition algorithms

- **Source**: Table 5, Section 5.6 (Comparison of Predictive Model Performance), p. 18
- **Caption**: "Comparison of prediction errors between models with and without decomposition algorithms."
- **Screenshot**: table5.png (page 18; PNG renders the page whose top holds Table 5, and whose lower half holds Figure 13)
- **Extraction type**: raw_table

| Model | MAE/MW | RMSE/MW | R²/% |
|-------|--------|---------|------|
| TCN-BiLSTM | 337.4591 | 464.9645 | 0.8346 |
| SBOA-SVMD-TCN-BiLSTM | 219.7098 | 309.2698 | 0.9273 |

Text-stated deltas: compared to plain TCN-BiLSTM (raw processed load as input, no decomposition), the proposed model reduces MAE by 34.89% and RMSE by 33.49%, and improves R² by 11.1%.
