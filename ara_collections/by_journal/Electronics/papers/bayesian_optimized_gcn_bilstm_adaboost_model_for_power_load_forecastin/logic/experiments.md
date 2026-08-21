# Experiments

## E01: Stagewise ablation — BiLSTM → GCN-BiLSTM → GCN-BiLSTM-Adaboost → proposed
- **Verifies**: C01, C02, C04
- **Evidence**: `evidence/tables/table4.md`, `evidence/figures/figure11.md`, `evidence/figures/figure12.md`
- **Run**: `src/execution/adaboost_bayesian_weighting.py` (reconstructed ensemble/weighting); base learner per `src/configs/model.md`
- **Setup**:
  - Model: GCN-BiLSTM base learner; ablated variants (single BiLSTM; GCN-BiLSTM; GCN-BiLSTM + AdaBoost; full GCN-BiLSTM-AB with Bayesian weighting)
  - Hardware: NVIDIA RTX 4060Ti GPU, 13th-Gen Intel Core i7, 32 GB RAM
  - Dataset: one year of regional hourly load + 8 weather features (2018)
  - System: PyTorch; Adam; the four variants share preprocessing and graph
- **Procedure**:
  1. Train each variant on the same normalized, 24-h-windowed data.
  2. Forecast over a one-day and a one-week horizon.
  3. Compare MAE/MAPE/RMSE across the four variants; inspect turning-point tracking.
- **Metrics**: MAE (MW), MAPE (%), RMSE (MW); qualitative turning-point fidelity
- **Expected outcome**:
  - Errors decrease monotonically as stages are added, on both horizons.
  - The full model tracks abrupt load transitions where earlier variants deviate.
- **Baselines**: The earlier variants themselves (each is the baseline for the next stage).
- **Dependencies**: none

## E02: Accuracy vs single-model baselines (LSTM, GRU, CNN-LSTM, GCN-LSTM, CNN-BiLSTM)
- **Verifies**: C01
- **Evidence**: `evidence/figures/figure7.md`, `evidence/figures/figure8.md`, `evidence/figures/figure9.md`, `evidence/figures/figure10.md`
- **Run**: base learner per `src/configs/model.md`; baselines reimplemented in PyTorch (not released)
- **Setup**:
  - Model: proposed GCN-BiLSTM-AB
  - Hardware: as E01
  - Dataset: as E01
  - System: identical preprocessing/normalization
- **Procedure**:
  1. Train each baseline and the proposed model on identical data.
  2. Produce one-day and one-week forecasts.
  3. Plot predicted vs real curves (Figs 7–8) and grouped error bars (Figs 9–10).
- **Metrics**: MAE (MW), MAPE (%), RMSE (MW)
- **Expected outcome**:
  - Proposed model has the lowest error on every metric and both horizons.
  - Proposed curve visually hugs the real-load curve more tightly than baselines.
- **Baselines**: LSTM, GRU, CNN-LSTM, GCN-LSTM, CNN-BiLSTM
- **Dependencies**: none

## E03: Graph-construction comparison — Spearman vs KNN vs learned graphs vs mutual information
- **Verifies**: C03
- **Evidence**: `evidence/tables/table2.md`, `evidence/figures/figure2.md`
- **Run**: adjacency built per `data/preprocessing.md`; downstream model fixed
- **Setup**:
  - Model: fixed GCN-BiLSTM(-AB) downstream, only the adjacency-construction rule changes
  - Hardware: as E01
  - Dataset: as E01
  - System: identical otherwise
- **Procedure**:
  1. Build four adjacency matrices (Spearman-threshold, KNN, learned, mutual information).
  2. Train/forecast the same downstream model with each.
  3. Compare one-week MAE/MAPE/RMSE.
- **Metrics**: MAE, MAPE (%), RMSE (one-week horizon)
- **Expected outcome**:
  - Spearman-threshold adjacency yields the lowest error of the four.
- **Baselines**: KNN, learned graphs, mutual information
- **Dependencies**: none

## E04: Robustness at abrupt load changes / turning points
- **Verifies**: C02, C04
- **Evidence**: `evidence/figures/figure11.md`, `evidence/tables/table4.md`
- **Run**: `src/execution/adaboost_bayesian_weighting.py`
- **Setup**:
  - Model: proposed vs BiLSTM / GCN-BiLSTM / GCN-BiLSTM-Adaboost
  - Hardware: as E01
  - Dataset: one-day window containing load turning points
  - System: as E01
- **Procedure**:
  1. Overlay each model's one-day forecast on the real load through a mutation window.
  2. Qualitatively assess tracking at turning points; read stagewise error drop.
- **Metrics**: qualitative turning-point fidelity; MAE/MAPE/RMSE (day)
- **Expected outcome**:
  - Proposed model stays close to real load at turning points where others deviate.
- **Baselines**: BiLSTM, GCN-BiLSTM, GCN-BiLSTM-Adaboost
- **Dependencies**: E01

## E05: Uncertainty quantification and runtime
- **Verifies**: C05
- **Evidence**: `evidence/figures/figure12.md`
- **Run**: `src/execution/adaboost_bayesian_weighting.py` (MC-Dropout sampling path)
- **Setup**:
  - Model: proposed GCN-BiLSTM-AB with MC Dropout
  - Hardware: as E01
  - Dataset: one-week horizon
  - System: repeated stochastic dropout passes at inference
- **Procedure**:
  1. Run repeated dropout passes per weak learner to obtain mean and variance.
  2. Form the weighted ensemble mean and a 95% predictive interval.
  3. Overlay actual, predicted, and interval; record wall-clock run time.
- **Metrics**: predictive-interval band vs actual coverage (visual); wall-clock time
- **Expected outcome**:
  - Actual load largely falls within the 95% band; the model emits point + interval.
  - A single full run completes in a few minutes on the stated hardware.
- **Baselines**: none (self-evaluation of the uncertainty output)
- **Dependencies**: E01
