# Table 4: Prediction results of different models in the Tétouan City power dataset

- **Source**: Table 4, Section 4 (Analysis of Experimental Results), p11
- **Caption**: "Prediction results obtained of different models in the Tétouan City power dataset."
- **Screenshot**: table4.png (page 11; table appears in the lower half of the page)
- **Extraction type**: raw_table

| Method | RMSE/MW | MAE/MW | MAPE/% |
|--------|---------|--------|--------|
| LSTM                   | 799.783 | 652.3 | 1.942 |
| CNN-LSTM               | 776.214 | 627.8 | 1.823 |
| TCN                    | 588.468 | 492.2 | 1.471 |
| Three-channel LSTM-CNN | 560.581 | 450.2 | 1.367 |

**Notes**: Three-channel model best on all metrics. Per §4(1), vs LSTM / CNN-LSTM / TCN the
three-channel RMSE decreased by 239.202, 215.660, 27.887 MW; MAE by 202.1, 177.6, 42.0 MW; MAPE by
0.566%, 0.465%, 0.104%. Supports C01, C02 (E04). Ordering: three-channel < TCN < CNN-LSTM < LSTM.
</content>
