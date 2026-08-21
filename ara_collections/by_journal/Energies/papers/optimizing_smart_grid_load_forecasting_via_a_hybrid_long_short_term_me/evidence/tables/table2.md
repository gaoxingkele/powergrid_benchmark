# Table 2: Comparison of Forecasting Models

- **Source**: Table 2, Section 4.6 (p.13)
- **Caption**: "Comparison of forecasting models."
- **Screenshot**: table2.png
- **Extraction type**: raw_table

## Table data

| Study | Model | Data Source | Resolution | RMSE | MAPE (%) | R2 |
|-------|-------|-------------|------------|------|----------|----|
| [35] Zhou & Zhang (2024) | ARIMA-LSTM | Southern China Grid | Hourly | — | 2.828 | 0.9732 |
| [36] Liu, Liang & Li (2023) | TimeGAN-CNN-LSTM | I/C Buildings | 15-min | — | 4.486 | 0.812 |
| [37] Ibrahim et al. (2022) | DNN Regression | Panama Grid | Hourly | 50.34 MW | 2.90 | 0.93 |
| [38] Liu et al. (2025) | CNN-BiLSTM-Attention | — | — | 0.77 GWh | 1.08–1.67 | 0.985–0.991 |
| [39] Ullah et al. (2024) | CNN-LSTM | NTDC Pakistan | Hourly | 538.71 | 2.72 | N.R. |
| **This study** | **LSTM-XGBoost Hybrid** | **Elia Grid (Belgium)** | **15-min** | **106.54 MW** | **1.18** | **0.994** |

**Note**: "N.R." = Not Reported. Units vary across studies: RMSE in MW or GWh; direct cross-comparison is confounded by unit and resolution differences.

## Notes (from Section 4.6)
- The authors use this comparison to argue that **resolution / aggregation is a confound** when ranking load forecasters (C05): hourly or national-level data naturally smooths fluctuations, lowering RMSE even if the model is not inherently better.
- Study [37] reports a lower RMSE (50.34 MW) but on hourly Panama national data, which the authors argue is an easier smoothing regime than 15-min single-operator data.
- Study [39] reports a much higher RMSE (538.71) on NTDC Pakistan hourly data, attributed to different data characteristics.
- Study [36] uses the same 15-min resolution but reports much higher MAPE (4.486%) and lower R2 (0.812), using synthetic TimeGAN-augmented data.
- Study [38] reports competitive MAPE (1.08–1.67%) and R2 (0.985–0.991) with a complex decomposition-heavy pipeline, but the authors note the preprocessing complexity limits real-time scalability.
- The paper does not re-run any competitor model on the Elia 15-min data — the comparison is strictly literature-reported metrics with different data regimes, so the confounding argument is qualitative, not experimentally isolated.
