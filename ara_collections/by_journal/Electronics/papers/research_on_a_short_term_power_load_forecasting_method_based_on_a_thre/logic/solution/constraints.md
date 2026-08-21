# Constraints — Boundary Conditions, Assumptions, Limitations

## Boundary conditions
- **Horizon**: Next-day (24-point) forecasting only. The model is an *improved single-step* predictor: the historical-load channel uses same-hour prior-day input so each output corresponds to a same-time future point, giving a full consecutive day. Multi-step direct forecasting is out of scope.
- **Modalities**: Exactly three input groups — time codes, meteorology, historical load. Adding/removing modalities is not evaluated.
- **Datasets**: Two distribution-network datasets (Tétouan 2017; Electrician Cup). No cross-dataset transfer or unseen-grid test.
- **Metrics**: RMSE, MAE (MW), MAPE (%); MAPE is the headline metric.

## Assumptions
- A1: Prediction-day meteorological features (temperature, humidity) are available at inference time (given by the dataset).
- A2: Same-hour prior-day load strongly predicts the target hour.
- A3: The three modality groups are the relevant driver set for STLF.
- A4: Training/test splits are drawn from the same distribution (no explicit split ratio or seed reported).
- A5: Baseline fairness — LSTM/CNN-LSTM/S-LSTM baselines share the three-channel model's hyperparameters; remaining baselines (TCN) are tuned to best over multiple runs.

## Known limitations
- **No released code or data**: "The datasets presented in this article are not readily available"; no repository is provided, so results are not independently reproducible from artifacts.
- **Ablations run on one dataset**: The activation/optimizer/lookback tables (1–3) report the tuned model at RMSE 321.198 / MAPE 0.974%, matching the Electrician Cup three-channel result — i.e. tuning appears done on the Electrician Cup set only, not cross-validated on Tétouan.
- **Interpretation, not measurement, for mechanism claims**: The gradient-pathology explanation (activation) and Adam first-moment-alignment explanation are the authors' rationale, not backed by gradient/loss-landscape measurements.
- **Metric-unit inconsistency**: Tables report RMSE/MAE in MW while residual plots (Figures 10, 12) label axes in kW/MW; the §4 text says most Tétouan residuals are "less than 1000 kW" while the RMSE is 560.581 MW — the unit labeling is internally inconsistent and reproduced as printed.
- **Equation transcription issue**: Eq. 3 is printed with `Sigmoid` for the candidate cell state although the text describes `tanh` (flagged in method.md).
- **No confidence intervals / significance tests**: Single-run point estimates; no variance across seeds reported.
- **Small hardware / dataset scale**: Trained on a laptop (i5-8300H, GTX 1050Ti); scaling behavior to large grids not assessed.
- **Data-availability / horizon caveats**: The "23.6% higher than single LSTM" headline is stated against ref [19]'s single-LSTM model; the exact denominator/scope of that comparison is only loosely specified.
</content>
