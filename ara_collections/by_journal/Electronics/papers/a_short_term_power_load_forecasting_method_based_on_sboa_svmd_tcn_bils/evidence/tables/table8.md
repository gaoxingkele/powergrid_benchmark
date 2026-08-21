# Table 8: Comparison of prediction accuracy across different seasons

- **Source**: Table 8, Section 5.7 (Comparison of Prediction Accuracy across Different Seasons), p. 20
- **Caption**: "Comparison of prediction accuracy across different seasons."
- **Screenshot**: table8.png (top of page 20; PNG renders the page whose top holds Table 8 and whose body holds Figure 14)
- **Extraction type**: raw_table

Errors (MAE/MW, RMSE/MW) for a specific day in each season; each season's data split 5:1 train/test.

| Model | Spring MAE | Spring RMSE | Summer MAE | Summer RMSE | Autumn MAE | Autumn RMSE | Winter MAE | Winter RMSE |
|-------|-----------|------------|-----------|------------|-----------|------------|-----------|------------|
| LSTM | 648.59 | 705.48 | 542.21 | 697.25 | 263.04 | 339.69 | 530.43 | 630.01 |
| ELM | 395.40 | 542.41 | 434.63 | 494.68 | 253.51 | 287.28 | 320.14 | 350.18 |
| BiLSTM | 337.50 | 379.72 | 442.66 | 490.69 | 206.13 | 258.42 | 251.24 | 323.73 |
| TCN-BiLSTM | 116.23 | 132.33 | 238.88 | 275.29 | 157.05 | 191.63 | 218.11 | 298.60 |

Text-stated average deltas (TCN-BiLSTM vs LSTM, ELM, BiLSTM): average MAE improved 63.2%, 47.97%, 41%; average RMSE reduced 62.15%, 46.38%, 38.19%.
