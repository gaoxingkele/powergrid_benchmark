# Table 5: Prediction results of different models in the Electrician Cup competition dataset

- **Source**: Table 5, Section 4 (Analysis of Experimental Results), p13
- **Caption**: "The prediction results of different models in the Electrician Cup competition dataset."
- **Screenshot**: table5.png (page 13; table appears at the top of the page)
- **Extraction type**: raw_table

| Method | RMSE/MW | MAE/MW | MAPE/% |
|--------|---------|--------|--------|
| LSTM                   | 508.857 | 407.1 | 1.522 |
| CNN-LSTM               | 426.196 | 343.8 | 1.246 |
| TCN                    | 358.294 | 304.7 | 1.083 |
| Three-channel LSTM-CNN | 321.198 | 278.6 | 0.974 |

**Notes**: Three-channel model best on all metrics. Per §4(2): three-channel RMSE 321.198 MW, MAE
278.6 MW, MAPE 0.974%; vs LSTM / CNN-LSTM / TCN, RMSE decreased by 187.659, 104.998, 37.096 MW; MAE
by 128.5, 65.2, 26.1 MW; MAPE by 0.548%, 0.272%, 0.109%. This three-channel row (RMSE 321.198 /
MAPE 0.974%) matches the tuned-model values in Tables 1–3, indicating the ablations were run on this
dataset. Supports C01, C02 (E05).
</content>
