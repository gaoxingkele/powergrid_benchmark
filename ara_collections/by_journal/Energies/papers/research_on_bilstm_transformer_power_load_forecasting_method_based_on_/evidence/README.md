# Evidence Index

## Tables

| # | File | Caption | Content |
|---|------|---------|---------|
| 1 | `tables/table1.md` | Table 1. Experimental environment and common parameter settings. | Hardware: Intel i9 CPU, RTX 3090 GPU; Software: PyTorch 1.12, Python 3.8; Optimizer: Adam (lr=0.001); Training: batch=64, epochs=150, Early Stopping (patience=15), ReduceLROnPlateau (patience=5); Model: hidden_dim=64, num_layers=2. |
| 2 | `tables/table2.md` | Table 2. Comparative analysis of model predictive accuracy metrics. | Nine models with MAE, RMSE, MAPE, R². DAF-BT best: MAE=4.560, RMSE=5.925, MAPE=1.58%, R²=0.983. |
| 3 | `tables/table3.md` | Table 3. Ablation study results across model variants. | Six variants showing contribution of BiLSTM, Transformer, DAF components individually and in combination. |
| 4 | `tables/table4.md` | Table 4. Computational complexity comparison. | Parameter count, training time per epoch, inference time per sample for five models. DAF-BT: 1.28M params, 24.5s/epoch, 12.4ms inference. |

## Figures

| # | File | Caption | Type |
|---|------|---------|------|
| 1 | `figures/figure1.md` | Figure 1. Structure diagram of Transformer model encoder. | Diagram |
| 2 | `figures/figure2.md` | Figure 2. Architecture of CNN-LSTM model. | Diagram |
| 3 | `figures/figure3.md` | Figure 3. Overall framework of BiLSTM-Transformer-DAF. | Diagram |
| 4 | `figures/figure4.md` | Figure 4. Principle diagram of DAF module. | Diagram |
| 5 | `figures/figure5.md` | Figure 5. Fitting performance of different models in the dataset. | Quantitative plot |
| 6 | `figures/figure6.md` | Figure 6. Comparison of representative forecasting models. | Quantitative plot |
| 7 | `figures/figure7.md` | Figure 7. Daily load forecasting curves. | Quantitative plot |
| 8 | `figures/figure8.md` | Figure 8. Quantitative error metrics for daily load forecasting. | Quantitative plot |
| 9 | `figures/figure9.md` | Figure 9. Weekly load forecasting curves. | Quantitative plot |
| 10 | `figures/figure10.md` | Figure 10. Quantitative error metrics for weekly load forecasting. | Quantitative plot |
| 11 | `figures/figure11.md` | Figure 11. Individual load fitting curves for ablation study variants. | Quantitative plot |
| 12 | `figures/figure12.md` | Figure 12. Combined overlay of ablation prediction trajectories. | Quantitative plot |

## Total Evidence Items

- **Tables:** 4 (Table 1 through Table 4)
- **Figures:** 12 (Figure 1 through Figure 12)
- **Source PNGs:** 16 (unchanged, archived as-is)
