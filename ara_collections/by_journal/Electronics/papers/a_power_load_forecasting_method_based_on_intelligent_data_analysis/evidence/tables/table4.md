# Table 4 - Prediction errors of four models for daily load of fifty users

**Source**: Table 4, §5.2 (p.14)
**Caption**: "Prediction errors of four models for daily load of fifty users."
**Screenshot**: table4.png
**Extraction type**: raw_table
**Location on page**: top of the page.

| Model | RMSE | MAE |
|-------|------|-----|
| LSTM | 6.457 | 4.610 |
| RNN | 6.698 | 4.965 |
| EMD-LSTM | 6.353 | 4.330 |
| CEEMDAN-LSTM | 5.973 | 3.821 |

**Note**: Column group header is "Performance Metrics". CEEMDAN-LSTM has the lowest RMSE (5.973) and
MAE (3.821); ordering by RMSE: CEEMDAN-LSTM < EMD-LSTM < LSTM < RNN, consistent with Table 3.
Supports C01, C02, C03. Daily-scale magnitudes are much larger than hourly because loads are summed
over a day. The conclusion's headline reductions (21%/30%/13% vs LSTM/RNN/EMD-LSTM) are not a direct
per-metric ratio of any single Table 3 or Table 4 row (see logic/solution/constraints.md).
