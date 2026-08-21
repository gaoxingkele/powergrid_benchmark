# Experiments

## E01: Standalone-vs-hybrid comparative evaluation on Elia grid load
- **Verifies**: C01, C02
- **Evidence**: evidence/tables/table1.md; evidence/figures/figure7.md
- **Run**: Not published as code; described in §4.2 (procedure) — LSTM (TensorFlow), XGBoost (DMLC), hybrid cascade. See src/environment.md.
- **Setup**:
  - Model: LSTM (2 layers × 50 neurons, dropout, dense, sequence length 60); XGBoost (n_estimators & learning rate grid-searched); hybrid LSTM→XGBoost cascade.
  - Hardware: Not specified in paper.
  - Dataset: Elia Grid Load (Belgium), 15-min resolution, 2022; min-max normalized to [0,1].
  - System: LSTM trained on preprocessed sequences; XGBoost trained on same feature set / on LSTM output.
- **Procedure**:
  1. Preprocess (clean, IQR outlier handling, interpolate missing, min-max scale).
  2. Split into train/test (see constraints — paper gives two conflicting splits).
  3. Train LSTM; generate LSTM predictions.
  4. Feed LSTM output (+ engineered features) to XGBoost; produce final forecast.
  5. Compute RMSE, MAPE, R2 for LSTM, XGBoost, and the hybrid.
- **Metrics**: RMSE (MW), MAPE (%), R2 (dimensionless).
- **Expected outcome**:
  - Hybrid attains the lowest RMSE and lowest MAPE of the three; R2 tied at the ceiling between XGBoost and the hybrid.
- **Baselines**: Standalone LSTM; standalone XGBoost.
- **Dependencies**: none

## E02: Per-metric decomposition of the model ranking
- **Verifies**: C01, C02
- **Evidence**: evidence/tables/table1.md
- **Run**: §4.4.1–4.4.3 detailed per-metric discussion of Table 1.
- **Setup**:
  - Model: same three models as E01.
  - Hardware: Not specified in paper.
  - Dataset: Elia Grid Load, 15-min, 2022.
  - System: read the three metric columns independently.
- **Procedure**:
  1. Rank models separately under RMSE, MAPE, and R2.
  2. Observe whether the improvement between XGBoost and hybrid appears in all metrics or only error-magnitude metrics.
- **Metrics**: RMSE (MW), MAPE (%), R2.
- **Expected outcome**:
  - The XGBoost→hybrid improvement shows up in RMSE and MAPE but not in R2 (tied at ceiling).
- **Baselines**: cross-metric self-comparison.
- **Dependencies**: E01

## E03: Regime-level error analysis via prediction overlays
- **Verifies**: C01, C03
- **Evidence**: evidence/figures/figure7.md; evidence/figures/figure2.md; evidence/figures/figure5.md
- **Run**: §4.5 (error analysis narrative) + Figure 7(a)–(d) prediction overlays.
- **Setup**:
  - Model: LSTM, XGBoost, hybrid ensemble.
  - Hardware: Not specified in paper.
  - Dataset: Elia Grid Load, 15-min, 2022 (train + test overlays).
  - System: visual overlay of actual vs predicted across the full series and test window.
- **Procedure**:
  1. Plot actual load against each model's predictions over time steps.
  2. Inspect behavior during spikes / high-volatility windows vs. calm windows.
  3. Compare how closely the hybrid tracks actual load during dynamic variations.
- **Metrics**: Qualitative tracking fidelity (visual); directional only.
- **Expected outcome**:
  - The ensemble tracks actual load more precisely than the standalone LSTM, especially during volatile/spike periods.
- **Baselines**: standalone LSTM overlay; standalone XGBoost overlay.
- **Dependencies**: E01

## E04: Attention-augmented hybrid trial (dead end)
- **Verifies**: C04
- **Evidence**: pending (no metrics table published for the attention variant)
- **Run**: Reported in Abstract, §1.2, §2.3, §4.6 — attention experimentally integrated then removed.
- **Setup**:
  - Model: hybrid LSTM-XGBoost with an added attention mechanism.
  - Hardware: Not specified in paper.
  - Dataset: Elia Grid Load, 15-min, 2022.
  - System: attention module added to the hybrid pipeline.
- **Procedure**:
  1. Add attention mechanism to the hybrid.
  2. Re-evaluate accuracy against the plain hybrid.
  3. Decide inclusion based on accuracy delta.
- **Metrics**: RMSE / MAPE / R2 (relative to plain hybrid) — exact values not reported.
- **Expected outcome**:
  - Attention variant does not beat the plain hybrid; it is excluded.
- **Baselines**: plain hybrid LSTM-XGBoost.
- **Dependencies**: E01

## E05: Comparison against recent state-of-the-art forecasting studies
- **Verifies**: C05
- **Evidence**: evidence/tables/table2.md
- **Run**: §4.6 comparative discussion; Table 2 summarizes 2022–2025 studies.
- **Setup**:
  - Model: this hybrid vs. literature models (ARIMA-LSTM, TimeGAN-CNN-LSTM, DNN regression, CNN-BiLSTM-Attention, CNN-LSTM).
  - Hardware: Not specified in paper.
  - Dataset: heterogeneous — Elia 15-min vs. hourly/national/seasonal grids (mixed units MW/GWh).
  - System: tabular comparison of reported metrics, resolutions, and data sources.
- **Procedure**:
  1. Tabulate each study's model, data source, resolution, and reported RMSE/MAPE/R2.
  2. Discuss how resolution/aggregation confounds the raw-metric comparison.
- **Metrics**: RMSE, MAPE, R2 (as reported per study; not recomputed).
- **Expected outcome**:
  - Lower reported RMSE in some hourly/national studies is attributable to easier (smoother) data, not necessarily better method — so ranking must control for resolution.
- **Baselines**: five external studies [35]–[39].
- **Dependencies**: E01
