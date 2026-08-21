# Problem Specification

## Observations

### O1: Standalone sequence learners leave residual error on high-resolution grid load
- **Statement**: On the Elia 15-min 2022 load data, a standalone LSTM records RMSE = 119.41 MW, MAPE = 1.30%, R2 = 0.992 — the worst of the three tested models on error metrics.
- **Evidence**: Table 1 (§4.2); §4.4.1–4.4.3; §5.
- **Implication**: A purely sequential model captures broad temporal trend but not all short-term/non-linear structure, leaving headroom for a residual-correcting stage.

### O2: A tree-based learner alone beats the LSTM on error but lacks temporal modeling
- **Statement**: Standalone XGBoost records RMSE = 109.48 MW, MAPE = 1.21%, R2 = 0.994 — better error than LSTM but "its application to the time-series data, where sequentiality is essential, still did not outperform the hybrid model."
- **Evidence**: Table 1 (§4.2); §5.
- **Implication**: Gradient-boosted trees handle non-linearity well but cannot learn temporal dependencies from the raw sequence; the two model families are complementary.

### O3: Electricity load has spikes, non-stationarity, and human-driven randomness
- **Statement**: Load data exhibits "sudden spikes, pronounced non-stationarity across daily, weekly, and seasonal cycles, and randomness stemming from unpredictable human consumption patterns."
- **Evidence**: §1.2; Figures 2, 3 (seasonal U-shape, low outliers), Figure 5 (box-plot outliers), Figure 6 (hour×date heatmap).
- **Implication**: Linear/stationary statistical models (ARIMA, SARIMA) degrade on this data; a non-linear temporal-aware model is required.

### O4: Error concentrates during high-volatility / spike periods
- **Statement**: "The LSTM model struggles during sudden spikes in demand … and fails to capture extreme anomalies"; "The XGBoost model exhibits a lower sensitivity to spikes but underperforms for continuous patterns."
- **Evidence**: §4.5 Error Analysis; Figure 7(a)–(d).
- **Implication**: The two error profiles are anti-correlated across regimes, motivating a combination that inherits the strengths of both.

## Gaps

### G1: No single model minimizes both absolute and relative error on volatile high-resolution load
- **Statement**: Neither the LSTM (temporal, weak on spikes) nor XGBoost (non-linear, no sequence memory) individually minimizes RMSE, MAPE, and R2 together.
- **Caused by**: O1, O2, O4.
- **Existing attempts**: ARIMA/SARIMA (linear, stationary — degrade); standalone LSTM; standalone XGBoost; ARIMA-LSTM and CNN-LSTM hybrids in the literature (Table 2), mostly on hourly / lower-resolution data.
- **Why they fail**: Statistical models cannot model non-linearity; single ML models cover only one of {temporal dependency, non-linear residual}; several literature hybrids simplify the task by using coarser resolution.

### G2: Added architectural complexity does not guarantee accuracy gains
- **Statement**: It is unclear whether stacking more mechanisms (e.g., attention) onto the hybrid improves accuracy.
- **Caused by**: O1, O2.
- **Existing attempts**: Attention mechanisms / transformers used widely in other forecasting studies.
- **Why they fail**: In this hybrid setting the authors found "a limited benefit," so attention was excluded (documented dead end).

## Key Insight
- **Insight**: Rather than pick one model family, feed the LSTM's temporal prediction into an XGBoost stage that learns to correct the LSTM's residual (non-linear) error — a cascade so each stage handles the error the other cannot.
- **Derived from**: O1, O2, O4.
- **Enables**: A hybrid that lowers RMSE/MAPE below either component while preserving the best R2, and is most helpful in the volatile regimes where a single model fails.

## Assumptions
- A1: The load series is approximately stationary / bell-shaped enough for model generalization (argued from the histogram, Figure 4).
- A2: Missing values can be adequately restored by linear interpolation / forward-filling; outliers handled by the IQR method.
- A3: Min-Max normalization to [0,1] is an appropriate scaling for both stages.
- A4: A December 2022 hold-out (or 80/20 split) is representative of the model's generalization to unseen load.
