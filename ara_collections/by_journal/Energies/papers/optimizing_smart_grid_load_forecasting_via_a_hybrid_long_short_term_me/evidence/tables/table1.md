# Table 1: Comparative Results

- **Source**: Table 1, Section 4.2 (p.10)
- **Caption**: "Comparative Results."
- **Screenshot**: table1.png
- **Extraction type**: raw_table

## Table data

| Model | RMSE (MW) | MAPE (%) | R2 |
|-------|-----------|----------|----|
| LSTM | 119.41 | 1.30 | 0.992 |
| XGBoost | 109.48 | 1.21 | 0.994 |
| LSTM-XGBoost (Hybrid) | **106.54** | **1.18** | **0.994** |

**Best values** are bolded: the hybrid achieves the lowest RMSE (106.54 MW) and lowest MAPE (1.18%) while tying XGBoost at the highest R2 (0.994).

## Notes (from Sections 4.2, 4.4.1–4.4.3, 5)
- The hybrid improves RMSE by **10.78%** over LSTM (119.41 to 106.54) and **2.68%** over XGBoost (109.48 to 106.54).
- The hybrid improves MAPE by **9.23%** over LSTM (1.30% to 1.18%) and **2.48%** over XGBoost (1.21% to 1.18%).
- R2 is identical between XGBoost and the hybrid (0.994), indicating that on this dataset R2 is saturated at the ceiling and does not discriminate between good models — the discriminating signal is in RMSE and MAPE (supports C02).
- The LSTM has the weakest performance across all three metrics among the tested models.
- Primary evidence for claims C01 (hybrid outperforms standalone models) and C02 (improvement in error-magnitude metrics, not R2).
