# Experiments

## E01: Hourly load prediction comparison across four models
- **Verifies**: C01, C02, C03
- **Evidence**: evidence/tables/table3.md (RMSE/MAE per model), evidence/figures/figure9.md (hourly prediction overlay for one user)
- **Run**: Not released as code; model built on the Keras platform using the CuDNNLSTM implementation (§5.2). No public repository provided.
- **Setup**:
  - Model: CEEMDAN-LSTM (experimental group) vs LSTM, RNN, EMD-LSTM (comparison group); per-component LSTM with BN, dropout, three dense layers
  - Hardware: Not specified in paper (GPU implied by CuDNNLSTM)
  - Dataset: Actual smart-meter measurements from Ireland; electricity consumption data from 50 users; raw data sampled at hourly intervals for next-hour prediction
  - System: Input sequence length 48 historical IMF values to predict the next IMF value; sliding-window decomposition front-end (60-day span, step 1)
- **Procedure**:
  1. Decompose each user's hourly load with CEEMDAN through the sliding window into IMF components + residual.
  2. Train one LSTM sub-model per component to predict the next value from 48 historical values.
  3. Reconstruct (overlay) component predictions into the final load forecast.
  4. Repeat with the raw-signal baselines (LSTM, RNN) and the EMD front-end (EMD-LSTM).
  5. Compute RMSE and MAE, statistically analyzed over the 50 users.
- **Metrics**: RMSE (kW·h; stability), MAE (kW·h; accuracy)
- **Expected outcome**:
  - The decomposition-based model attains lower RMSE and MAE than the undecomposed LSTM and RNN.
  - The adaptive-noise decomposition model attains lower error than the plain-EMD decomposition model.
  - The advantage appears in both metrics simultaneously.
- **Baselines**: LSTM [8], RNN [10], EMD-LSTM [9]
- **Dependencies**: none

## E02: Daily load prediction comparison across four models
- **Verifies**: C01, C02, C03
- **Evidence**: evidence/tables/table4.md (RMSE/MAE per model), evidence/figures/figure10.md (daily prediction overlay for one user)
- **Run**: Not released as code; Keras / CuDNNLSTM (§5.2).
- **Setup**:
  - Model: same four models as E01
  - Hardware: Not specified in paper
  - Dataset: 50 users, Irish smart-meter data; raw data sampled at daily intervals for next-day prediction; training set of 500 days (daily interval), sliding window of 180 days with step 1 for the training set; last 30 days reserved as the test set
  - System: 48 historical IMF values → next IMF value; sliding-window decomposition front-end
- **Procedure**:
  1. Sample raw data at daily intervals.
  2. Decompose with CEEMDAN via sliding window; extract rear-of-window component segments.
  3. Train per-component LSTM sub-models; reconstruct forecasts.
  4. Repeat with LSTM, RNN, EMD-LSTM baselines.
  5. Compute RMSE and MAE over the 50 users; also plot one user's actual-vs-predicted daily trace.
- **Metrics**: RMSE, MAE
- **Expected outcome**:
  - CEEMDAN-LSTM yields the lowest RMSE and MAE among the four models at the daily scale.
  - The model ordering is consistent with the hourly experiment.
- **Baselines**: LSTM, RNN, EMD-LSTM
- **Dependencies**: none

## E03: Sequence decomposition analysis of a user's load
- **Verifies**: C04, C05
- **Evidence**: evidence/figures/figure6.md (raw hourly load of one user), evidence/figures/figure7.md (CEEMDAN decomposition into IMF1–IMF8 + RES)
- **Run**: Not released as code; CEEMDAN decomposition step (§5.1). No public repository.
- **Setup**:
  - Model: CEEMDAN decomposition only (no forecasting)
  - Hardware: Not specified in paper
  - Dataset: Data from 50 randomly selected users to validate generalization/diversity; one specific user's hourly load profile shown; sampling interval 1 h, ~1440+ sampling points
  - System: White noise amplitude 0.1× the standard deviation of the original data; 200 sets of white noise; 60-day sliding window, step 1; number of IMF components set to 8; endpoint effects handled by linearly extending extreme points
- **Procedure**:
  1. Take a user's hourly load series (Figure 6).
  2. Apply CEEMDAN within the sliding window to decompose it into 8 IMFs and a residual.
  3. Inspect the frequency/regularity of each component and assign physical roles (stochastic / periodic / trend).
- **Metrics**: Qualitative — frequency content and regularity per component (no error metric)
- **Expected outcome**:
  - The high-index (highest-frequency) IMFs show no apparent regular pattern (stochastic role).
  - The mid IMFs show clear periodicity (periodic role).
  - The lowest-frequency IMF plus the residual show trend behavior (trend role).
  - A window spanning multiple cycles yields this clean separation.
- **Baselines**: none (analysis, not comparison)
- **Dependencies**: none
