# Table 3: Quantitative Performance Metrics for Ablation Study Variants

**Source:** `evidence/tables/table3.png`

**Caption:** "Quantitative performance metrics for ablation study variants."

**Extraction Method:** Direct crop from paper PDF.

## Key Data Transcription

| Variant | MAE (MW) | RMSE (MW) | MAPE (%) | R2 |
|---------|----------|-----------|----------|-----|
| BiLSTM | 8.252 | 10.95 | 2.85 | 0.942 |
| Transformer | 6.768 | 8.851 | 2.34 | 0.962 |
| BiLSTM-DAF | 6.121 | 8.152 | 2.18 | 0.965 |
| BiLSTM-Transformer | 5.895 | 7.585 | 2.04 | 0.970 |
| Transformer-DAF | 4.870 | 6.492 | 1.74 | 0.979 |
| **BiLSTM-Transformer-DAF (Full)** | **4.560** | **5.025** | **1.58** | **0.983** |

## Key Observations
- Adding DAF to any backbone consistently improves metrics (BiLSTM vs. BiLSTM-DAF: MAPE 2.85% -> 2.18%; Transformer vs. Transformer-DAF: MAPE 2.34% -> 1.74%)
- Transformer-DAF (MAPE 1.74%) outperforms BiLSTM-Transformer (MAPE 2.04%), demonstrating DAF fusion is more impactful than stacking additional temporal layers (supports C06)
- Full model achieves best results with all components combined
- Note: The full model RMSE in this table (5.025) differs from Table 2 (5.925) under the same model name — this is an inconsistency in the source paper itself, possibly reflecting slightly different evaluation conditions
