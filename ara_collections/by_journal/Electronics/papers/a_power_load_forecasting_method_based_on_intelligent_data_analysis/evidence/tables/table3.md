# Table 3 - Prediction errors of four models for hourly load of fifty users

**Source**: Table 3, §5.2 (p.13)
**Caption**: "Prediction errors of four models for hourly load of fifty users."
**Screenshot**: table3.png
**Extraction type**: raw_table
**Location on page**: bottom of the page, below the RMSE/MAE formula paragraph.

| Model | RMSE | MAE |
|-------|------|-----|
| LSTM | 0.274 | 0.175 |
| RNN | 0.292 | 0.18 |
| EMD-LSTM | 0.265 | 0.167 |
| CEEMDAN-LSTM | 0.246 | 0.153 |

**Note**: Column group header is "Performance Metrics". CEEMDAN-LSTM has the lowest RMSE (0.246) and
MAE (0.153) of the four models; ordering by RMSE: CEEMDAN-LSTM < EMD-LSTM < LSTM < RNN. Supports
C01, C02, C03. (MAE for RNN printed as "0.18".)
