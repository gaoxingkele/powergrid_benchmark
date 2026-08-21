# Table 1: Accuracy of Multi-Energy Load Forecasting Using Different Methods

**Source:** `evidence/tables/table1.png`

**Caption:** "The accuracy of multi-energy load forecasting using different methods."

**Extraction note:** Table 1 reports MAE, RMSE, MAPE, and R2 for 11 baseline methods + TSTG across 3 load types (Electric, Cooling, Heating) and 4 horizons (6/12/24/96 h). The full 144-cell table is in the screenshot. Below are the TSTG results (exact from source) and key comparisons discussed in the paper.

## TSTG Performance (across all loads and horizons)

| Horizon | Electric (MAE / RMSE / MAPE / R2) | Cooling (MAE / RMSE / MAPE / R2) | Heating (MAE / RMSE / MAPE / R2) |
|---------|------------------------------------|-----------------------------------|-----------------------------------|
| 6 h | 0.118 / 0.159 / 0.059 / 0.965 | 0.069 / 0.101 / 0.046 / 0.993 | 0.087 / 0.130 / 0.048 / 0.978 |
| 12 h | 0.120 / 0.163 / 0.060 / 0.963 | 0.073 / 0.106 / 0.049 / 0.991 | 0.090 / 0.131 / 0.050 / 0.975 |
| 24 h | 0.131 / 0.178 / 0.066 / 0.956 | 0.081 / 0.114 / 0.054 / 0.989 | 0.094 / 0.141 / 0.052 / 0.972 |
| 96 h | 0.139 / 0.192 / 0.070 / 0.945 | 0.074 / 0.105 / 0.049 / 0.992 | 0.091 / 0.138 / 0.051 / 0.969 |

## Key Comparisons (from paper discussion)

**vs. Autoformer (second-best deep learning baseline):**
- Electric: MAE reduced by 44.98% (from 0.221 to TSTG 0.131), RMSE by 38.19%, MAPE by 39.62%, R2 increased by 8.77%
- Cooling: MAE reduced by 51.20%, RMSE by 47.94%, R2 +3.45%, MAPE -51.35%
- Heating: MAE reduced by 49.19%, RMSE by 45.97%, R2 +8.09%, MAPE -49.19%

**vs. TiDE (best MLP-based baseline):**
- Electric: MAE -36.10%, RMSE -33.33%, R2 +6.29%, MAPE -35.29%
- Cooling: MAE -29.82%, RMSE -25.97%, R2 +1.02%, MAPE -29.87%
- Heating: MAE -23.58%, RMSE -22.53%, R2 +4.21%, MAPE -25.20%

**vs. ARIMA (statistical baseline):**
- TSTG achieves average MAE/RMSE/MAPE reductions of over 40% across all loads and horizons

## Baselines (complete list)

Transformer-based: Transformer, Informer, Autoformer, FEDformer, Reformer, Pyraformer
MLP-based: LightTS, TiDE, TSMixer
Statistical: ARIMA, Prophet

TSTG achieves the best metrics across all 12 settings (3 loads × 4 horizons). The full data for all models and horizons is available in the PNG screenshot.
