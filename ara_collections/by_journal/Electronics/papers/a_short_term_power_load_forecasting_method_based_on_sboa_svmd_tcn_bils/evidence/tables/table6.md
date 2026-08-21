# Table 6: Comparison of prediction accuracy of different models

- **Source**: Table 6, Section 5.6, p. 19
- **Caption**: "Comparison of prediction accuracy of different models."
- **Screenshot**: table6.png (page 19; PNG renders the page holding both Table 6 (upper) and Table 7 (lower))
- **Extraction type**: raw_table

All four models take the SBOA-SVMD-decomposed IMFs as input; they differ only in the per-component forecaster.

| Model | MAE/MW | RMSE/MW | R²/% |
|-------|--------|---------|------|
| LSTM | 420.6167 | 542.0793 | 0.7766 |
| ELM | 326.9141 | 508.3097 | 0.8035 |
| BiLSTM | 248.1770 | 348.7726 | 0.9075 |
| TCN-BiLSTM | 219.7098 | 309.2698 | 0.9273 |

Text-stated deltas (TCN-BiLSTM vs LSTM, ELM, BiLSTM): MAE reduced 47.8%, 32.8%, 11.5%; RMSE reduced 42.9%, 39.2%, 11.3%. These are the abstract's headline numbers.
