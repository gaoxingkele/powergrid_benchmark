# Experiments

## E01 — Full Benchmark Comparison

**Objective:** Evaluate the proposed DAF-BT model against eight baseline models across standard regression metrics to establish relative performance positioning.

**Methodology:** Nine models trained and evaluated on identical train/val/test splits (7:1:2). Hyperparameters optimized via Grid Search for each baseline. Metrics: MAE, RMSE, MAPE, R-squared. Input features: load, temperature, wind speed at 0.5h resolution.

**Results:** DAF-BT achieves best overall performance: MAE=4.560, RMSE=5.925, MAPE=1.58%, R²=0.983. Next best: Transformer (MAE=7.482, MAPE=2.31%) and TCN-GRU (MAE=7.905, MAPE=2.44%). CNN-LSTM hybrid performs worse (MAE=9.345, MAPE=2.89%) than standalone Transformer, consistent with the identified 25% information loss in cascade hybrids.

**Evidence mapping:** Table 2 (quantitative metrics), Figure 5 (fitting performance curves for all 9 models), Figure 6 (representative forecasting model overlay).

---

## E02 — Multi-Time-Scale Daily and Weekly Evaluation

**Objective:** Assess model performance at daily and weekly forecasting horizons to evaluate robustness across different temporal granularities.

**Methodology:** Daily load forecasting (48 time steps per day) and weekly load forecasting (336 time steps per week) using best-performing models from E01. Qualitative comparison via overlay curves and quantitative comparison via error metrics at each scale.

**Results:** DAF-BT tracks actual load curves more closely during the weekend transition period (Friday-Saturday-Sunday) compared to baselines. Error distributions (box plots / bar charts) consistently show lower median error and narrower dispersion for DAF-BT across both daily and weekly scales.

**Evidence mapping:** Figure 7 (daily load forecasting curves), Figure 8 (quantitative error metrics for daily load), Figure 9 (weekly load forecasting curves), Figure 10 (quantitative error metrics for weekly load).

---

## E03 — Ablation Study

**Objective:** Isolate the contribution of each architectural component through systematic removal/addition.

**Methodology:** Evaluate six model variants: (1) BiLSTM only, (2) Transformer only, (3) BiLSTM + DAF, (4) BiLSTM + Transformer (no DAF), (5) Transformer + DAF, (6) Full BiLSTM + Transformer + DAF. All variants evaluated under identical conditions.

**Results:**
| Variant | MAE | RMSE | MAPE | R² |
|---------|------|------|------|-----|
| BiLSTM | 7.085 | 9.374 | 2.18% | 0.954 |
| Transformer | 7.482 | 9.568 | 2.31% | 0.952 |
| BiLSTM-DAF | 6.227 | 7.914 | 1.92% | 0.969 |
| BiLSTM-Transformer | 6.645 | 8.403 | 2.04% | 0.965 |
| Transformer-DAF | 5.642 | 7.182 | 1.74% | 0.975 |
| Full (DAF-BT) | 4.560 | 5.025 | 1.58% | 0.983 |

Key findings: (1) Adding DAF to any backbone improves accuracy. (2) Transformer-DAF (MAPE 1.74%) outperforms BiLSTM-Transformer (MAPE 2.04%), establishing fusion dominance over layer stacking. (3) Full model achieves best results with all components.

**Evidence mapping:** Table 3 (metrics), Figure 11 (individual load fitting curves for each variant), Figure 12 (combined overlay of all ablation prediction trajectories).

---

## E04 — Complexity and Efficiency Analysis

**Objective:** Quantify the computational cost of the proposed model relative to baselines, measuring parameter count, training time, and inference latency.

**Methodology:** All models evaluated on identical hardware (RTX 3090). Parameters counted from model definitions. Training time measured as seconds per epoch averaged over 150 epochs. Inference time measured as milliseconds per sample averaged over 1000 runs.

**Results:**
| Model | Params | Train Time (s/epoch) | Inference (ms) |
|-------|--------|---------------------|-----------------|
| LSTM | 0.42M | 8.2 | 3.1 |
| CNN-LSTM | 0.89M | 14.7 | 6.8 |
| Transformer | 0.95M | 16.1 | 7.3 |
| BiLSTM-Transformer | 1.16M | 22.3 | 10.6 |
| **Ours (DAF-BT)** | **1.28M** | **24.5** | **12.4** |

DAF adds only 0.12M parameters (10.3% increase), 2.2s/epoch training overhead (9.9%), and 1.8ms inference increase (17.0%), demonstrating practical deployability.

**Evidence mapping:** Table 4.

---

## E05 — Qualitative Scenario Evaluation

**Objective:** Provide visual and qualitative assessment of model behavior under challenging operating conditions: peak load periods, valley periods, and weekend transition boundaries.

**Methodology:** Examine prediction curves from E01 and E02 results, focusing on temporal regions where baseline models exhibit systematic errors. Analyze DAF-BT behavior during Spring Festival transition (referenced O2), PV fluctuation periods (O3), and weekend boundaries.

**Results:** DAF-BT maintains tighter tracking during: (1) sharp morning ramp-up periods (6:00-9:00), (2) evening peak periods (17:00-21:00), (3) weekend transition days (Friday-to-Saturday and Sunday-to-Monday). Baselines show systematic overshoot/undershoot patterns at these boundaries. The DAF model's adaptive weighting appears to reweight feature contributions appropriately during transition contexts.

**Evidence mapping:** Figures 5, 6, 7, 8, 9, 10, 11, 12 (qualitative analysis of prediction trajectories and error patterns across all visualizations).
