# Table 4: Comparison of Computational Complexity and Time Costs

**Source:** `evidence/tables/table4.png`

**Caption:** "Comparison of computational complexity and time costs."

**Extraction Method:** Direct crop from paper PDF.

## Key Data Transcription

| Model | Parameters (Millions) | Training Time (s/Epoch) | Inference Time (ms) |
|-------|----------------------|------------------------|---------------------|
| LSTM | 0.45 | 11.2 | 4.5 |
| CNN-LSTM | 0.65 | 13.5 | 6.8 |
| Transformer | 0.82 | 14.6 | 8.2 |
| BiLSTM-Transformer | 1.16 | 21.5 | 10.6 |
| **DAF-BT (Ours)** | **1.28** | **24.5** | **12.4** |

## Key Observations
- DAF-BT has 1.28M total parameters, only 0.12M (10.3%) more than BiLSTM-Transformer (1.16M)
- Training time increases by 3.0 s/epoch (14.0%) compared to BiLSTM-Transformer
- Inference time increases by 1.8ms (17.0%) to 12.4ms per sample, remaining within real-time requirements for 0.5h resolution forecasting
- LSTM has the lowest resource requirements (0.45M params, 4.5ms inference) but also the worst accuracy
- The DAF module's computational footprint is modest relative to the accuracy improvement it delivers (MAPE 2.04% -> 1.58%)
