# Table 2: Comparative Analysis of Model Predictive Accuracy Metrics

**Source:** `evidence/tables/table2.png`

**Caption:** "Comparative analysis of model predictive accuracy metrics."

**Extraction Method:** Direct crop from paper PDF.

## Key Data Transcription

| Model | MAE (MW) | RMSE (MW) | MAPE (%) | R2 |
|-------|----------|-----------|----------|-----|
| CNN | 12.24 | 15.72 | 4.23 | 0.879 |
| LSTM | 8.711 | 11.55 | 2.98 | 0.935 |
| GRU | 8.481 | 11.41 | 2.88 | 0.936 |
| TCN | 8.338 | 11.02 | 3.02 | 0.940 |
| CNN-LSTM | 7.362 | 9.486 | 2.62 | 0.956 |
| Transformer | 6.768 | 8.851 | 2.34 | 0.962 |
| TCN-GRU | 6.384 | 8.582 | 2.20 | 0.964 |
| TCN-LSTM-Attention | 5.112 | 6.658 | 1.81 | 0.978 |
| **DAF-BT (Ours)** | **4.560** | **5.925** | **1.58** | **0.983** |

## Key Observations
- DAF-BT achieves the lowest error across all four metrics
- Transformer and TCN-LSTM-Attention are the second-best group
- MAPE of 1.58% represents approximately a 12.7% relative improvement over the best baseline TCN-LSTM-Attention (1.81%)
- The R2 value of 0.983 indicates excellent variance explanation by the proposed model
