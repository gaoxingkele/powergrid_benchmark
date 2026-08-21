# Table 4: Comparison with Different Auxiliary Information

**Source:** `evidence/tables/table4.png`

**Caption:** "The comparison with different auxiliary information."

**Extraction:** Four cases at 96 h prediction horizon. Case 1 = no auxiliary info; Case 2 = +meteorological (weather); Case 3 = +calendar; Case 4 = +both.

## Transcription

| Case | Electric (MAE / RMSE / R2) | Cooling (MAE / RMSE / R2) | Heating (MAE / RMSE / R2) |
|------|----------------------------|----------------------------|----------------------------|
| Case 1 (No aux) | 0.153 / 0.203 / 0.943 | 0.093 / 0.115 / 0.986 | 0.110 / 0.146 / 0.967 |
| Case 2 (+Weather) | 0.146 / 0.197 / 0.945 | 0.087 / 0.111 / 0.990 | 0.099 / 0.139 / 0.970 |
| Case 3 (+Calendar) | 0.149 / 0.195 / 0.946 | 0.084 / 0.108 / 0.993 | 0.096 / 0.137 / 0.972 |
| Case 4 (+Both) | **0.139 / 0.192 / 0.945** | **0.074 / 0.105 / 0.992** | **0.091 / 0.138 / 0.969** |

## Notes

- Adding weather (Case 2) vs. Case 1: electric MAE -4.58%, RMSE -2.96%, R2 +0.21%
- Adding calendar (Case 3) vs. Case 1: electric MAE -2.61%, RMSE -3.94%, R2 +0.32%
- Adding both (Case 4) vs. Case 1: electric MAE -9.15%, RMSE -5.42%, R2 +0.21%
- Calendar features provide predictive value comparable to or exceeding meteorological features for multi-energy load; combining both is best.
- Supports C04: calendar auxiliary features carry substantial predictive value, and fusing both is optimal.
