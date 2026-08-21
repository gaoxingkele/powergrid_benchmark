# Experiments

## E01: Activation-function ablation
- **Verifies**: C03
- **Evidence**: evidence/tables/table1.md
- **Run**: Not externally persisted (no released code); three-channel LSTM-CNN trained with each activation, per §3.
- **Setup**:
  - Model: three-channel LSTM-CNN (1 LSTM layer × 64 neurons per channel; 2 Conv1D layers with 8 then 2 kernels; 1 MaxPooling1D; FC head)
  - Hardware: Intel Core i5-8300H CPU, NVIDIA GTX 1050Ti GPU, Windows 11
  - Dataset: Electrician Cup competition dataset (the parameter-tuning dataset; its tuned three-channel result matches the three-channel row of Table 5)
  - System: Keras on TensorFlow 2.6.0; batch_size 256; lr 0.001; MAE loss; 80 iterations
- **Procedure**:
  1. Fix the three-channel architecture and all hyperparameters.
  2. Swap the network activation among Sigmoid, Tanh, ReLU, Leaky ReLU.
  3. Train and evaluate on the test set; record RMSE, MAE, MAPE.
- **Metrics**: RMSE (MW), MAE (MW), MAPE (%)
- **Expected outcome**:
  - Leaky ReLU best, ReLU worst; saturating activations (Sigmoid, Tanh) in between.
- **Baselines**: The four activation functions compared against each other.
- **Dependencies**: none

## E02: Optimizer ablation
- **Verifies**: C04
- **Evidence**: evidence/tables/table2.md
- **Run**: Not externally persisted; three-channel LSTM-CNN trained with each optimizer, per §3.
- **Setup**:
  - Model: three-channel LSTM-CNN (same as E01), with Leaky ReLU fixed
  - Hardware: Intel Core i5-8300H CPU, NVIDIA GTX 1050Ti GPU, Windows 11
  - Dataset: Electrician Cup competition dataset
  - System: Keras/TensorFlow 2.6.0; batch_size 256; lr 0.001; MAE loss; 80 iterations
- **Procedure**:
  1. Fix architecture and activation.
  2. Swap optimizer among SGD, RMSprop, Nadam, Adam.
  3. Train and evaluate; record RMSE, MAE, MAPE (and note convergence behavior qualitatively).
- **Metrics**: RMSE (MW), MAE (MW), MAPE (%)
- **Expected outcome**:
  - Adam best; SGD worst; RMSprop converges faster early but does not win final accuracy; Nadam slightly worse than Adam.
- **Baselines**: The four optimizers compared against each other.
- **Dependencies**: E01 (activation fixed to the winner)

## E03: Historical-load lookback-length study
- **Verifies**: C05
- **Evidence**: evidence/tables/table3.md
- **Run**: Not externally persisted; three-channel LSTM-CNN with varied historical-load input length, per §3.
- **Setup**:
  - Model: three-channel LSTM-CNN (Leaky ReLU, Adam)
  - Hardware: Intel Core i5-8300H CPU, NVIDIA GTX 1050Ti GPU, Windows 11
  - Dataset: Electrician Cup competition dataset
  - System: Keras/TensorFlow 2.6.0; batch_size 256; lr 0.001; MAE loss; 80 iterations
- **Procedure**:
  1. Feed the historical-load LSTM channel the same-hour load from the previous 1, 2, 3, and 4 days respectively.
  2. Keep the other two channels fixed.
  3. Train and evaluate; record RMSE, MAE, MAPE.
- **Metrics**: RMSE (MW), MAE (MW), MAPE (%)
- **Expected outcome**:
  - Accuracy is best at 1-day lookback and worsens monotonically as lookback grows, with an abrupt jump at 4 days.
- **Baselines**: Lookback lengths 1–4 days compared against each other.
- **Dependencies**: E01, E02

## E04: Model comparison on the Tétouan City dataset
- **Verifies**: C01, C02, C06
- **Evidence**: evidence/tables/table4.md, evidence/figures/figure9.md, evidence/figures/figure10.md
- **Run**: Not externally persisted; three-channel model vs baselines, per §4(1).
- **Setup**:
  - Model: three-channel LSTM-CNN vs LSTM, CNN-LSTM, TCN
  - Hardware: Intel Core i5-8300H CPU, NVIDIA GTX 1050Ti GPU, Windows 11
  - Dataset: Tétouan (Morocco) distribution-network power data, full year 2017
  - System: Keras/TensorFlow 2.6.0; LSTM/CNN-LSTM/S-LSTM baselines use the same hyperparameters as the three-channel model; remaining baselines tuned to best over multiple runs
- **Procedure**:
  1. Train all models on the training split, predict on the test split.
  2. Record RMSE, MAE, MAPE per model.
  3. Plot prediction curves vs actual (Figure 9) and residual magnitudes (Figure 10).
- **Metrics**: RMSE (MW), MAE (MW), MAPE (%); residual magnitude (kW)
- **Expected outcome**:
  - Three-channel model lowest error on all metrics; ordering three-channel < TCN < CNN-LSTM < LSTM; three-channel tracks sudden changes best and has the gentlest residuals.
- **Baselines**: LSTM, CNN-LSTM, TCN
- **Dependencies**: E01, E02, E03 (configuration fixed by ablations)

## E05: Model comparison on the Electrician Cup dataset
- **Verifies**: C01, C02, C06
- **Evidence**: evidence/tables/table5.md, evidence/figures/figure11.md, evidence/figures/figure12.md
- **Run**: Not externally persisted; three-channel model vs baselines, per §4(2).
- **Setup**:
  - Model: three-channel LSTM-CNN vs LSTM, CNN-LSTM, TCN
  - Hardware: Intel Core i5-8300H CPU, NVIDIA GTX 1050Ti GPU, Windows 11
  - Dataset: Electrician Cup competition dataset
  - System: Keras/TensorFlow 2.6.0; matched hyperparameters for LSTM/CNN-LSTM/S-LSTM baselines
- **Procedure**:
  1. Train all models on the training split, predict on the test split.
  2. Record RMSE, MAE, MAPE per model.
  3. Plot prediction curves vs actual (Figure 11) and residual magnitudes (Figure 12).
- **Metrics**: RMSE (MW), MAE (MW), MAPE (%); residual magnitude (MW)
- **Expected outcome**:
  - Three-channel model lowest error on all metrics; ordering three-channel < TCN < CNN-LSTM < LSTM; accurate morning/evening tracking with more stable residuals.
- **Baselines**: LSTM, CNN-LSTM, TCN
- **Dependencies**: E01, E02, E03
</content>
