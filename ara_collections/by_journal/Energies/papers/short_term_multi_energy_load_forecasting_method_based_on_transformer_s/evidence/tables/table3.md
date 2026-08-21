# Table 3: Comparison Between Combined Load Forecasting and Individual Forecasting

**Source:** `evidence/tables/table3.png`

**Caption:** "The comparison between combined load forecasting and individual forecasting results."

**Extraction:** Case 1 = independent forecasting (ignoring inter-load coupling); Case 2 = joint forecasting (TSTG full model).

## Transcription

### Case 1: Independent Forecasting (per-load models)

| Horizon | Electric (MAE / RMSE / R2) | Cooling (MAE / RMSE / R2) | Heating (MAE / RMSE / R2) |
|---------|----------------------------|----------------------------|----------------------------|
| 6 h | 0.123 / 0.160 / 0.963 | 0.084 / 0.106 / 0.989 | 0.097 / 0.132 / 0.975 |
| 12 h | 0.126 / 0.163 / 0.960 | 0.089 / 0.110 / 0.988 | 0.103 / 0.139 / 0.973 |
| 24 h | 0.143 / 0.181 / 0.951 | 0.096 / 0.122 / 0.986 | 0.113 / 0.146 / 0.968 |
| 96 h | 0.158 / 0.202 / 0.941 | 0.094 / 0.119 / 0.987 | 0.114 / 0.145 / 0.969 |

### Case 2: Joint Forecasting (TSTG full model)

| Horizon | Electric (MAE / RMSE / R2) | Cooling (MAE / RMSE / R2) | Heating (MAE / RMSE / R2) |
|---------|----------------------------|----------------------------|----------------------------|
| 6 h | **0.118 / 0.159 / 0.965** | **0.069 / 0.101 / 0.993** | **0.087 / 0.130 / 0.978** |
| 12 h | **0.120 / 0.163 / 0.963** | **0.073 / 0.106 / 0.991** | **0.090 / 0.131 / 0.975** |
| 24 h | **0.131 / 0.178 / 0.956** | **0.081 / 0.114 / 0.989** | **0.094 / 0.141 / 0.972** |
| 96 h | **0.139 / 0.192 / 0.945** | **0.074 / 0.105 / 0.992** | **0.091 / 0.138 / 0.969** |

## Improvements (Case 2 vs. Case 1, 24h representative)

- Electric: MAE -8.39%, RMSE -1.66%, R2 +0.53%
- Cooling: MAE -15.62%, RMSE -6.56%, R2 +0.30%
- Heating: MAE -16.81%, RMSE -3.42%, R2 +0.41%

Joint forecasting outperforms independent across all loads and horizons, confirming C03.
