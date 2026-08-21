# Table 2: Training and Inference Time Comparison

**Source:** `evidence/tables/table2.png`

**Caption:** "Training and inference time comparison using different methods."

**Extraction note:** Training time in seconds (wall-clock on same GPU hardware), inference time per sample average.

## Transcription

| Method | Training Time (s) | Inference Time (s) |
|--------|-------------------|---------------------|
| FEDformer | 3600 | 0.95 |
| LightTS | 1800 | 0.65 |
| Pyraformer | 3200 | 0.85 |
| TiDE | 2400 | 0.70 |
| Autoformer | 3000 | 0.88 |
| ARIMA | 900 | 0.50 |
| Prophet | 1200 | 0.55 |
| **TSTG (proposed)** | **2700** | **0.72** |

## Notes

- TSTG trains in 2700s — slower than lightweight models (LightTS 1800s, TiDE 2400s) but faster than heavy Transformer variants (Autoformer 3000s, FEDformer 3600s, Pyraformer 3200s).
- TSTG inference is 0.72s — competitive with TiDE (0.70s) and faster than FEDformer (0.95s).
- ARIMA and Prophet (statistical) have lowest wall-clock time but must be re-fitted per series, scaling poorly in multi-load settings.
- TSTG trains once for all loads and horizons, supporting batched GPU inference with sub-second latency.
