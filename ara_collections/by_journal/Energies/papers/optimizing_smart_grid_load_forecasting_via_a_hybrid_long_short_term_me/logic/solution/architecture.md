# Architecture — Hybrid LSTM-XGBoost Forecasting Pipeline

Structural source: Figure 1 ("Proposed model", §3), §3.1–3.6. This is a pipeline/flowchart, not a
measurement plot; the component graph below mirrors Figure 1 (see evidence/figures/figure1.md).

## Pipeline overview

The system is a linear pipeline with two parallel-then-merged model phases:

```
Start
  → Load Raw Data
  → Preprocessing (Cleaning, Scaling, Splitting)
  → ┌ LSTM Phase ─────────────┐      ┌ XGBoost Phase ──────────────┐
    │ Build LSTM Model        │  →   │ Prepare Data for XGBoost     │
    │ Train LSTM on Time Series│      │ Train XGBoost Model          │
    │ Generate LSTM Predictions│  →   │ Predict Data for XGBoost     │
    └─────────────────────────┘      └──────────────────────────────┘
  → Evaluation
  → End
```
(Note: Figure 1 box labels contain typos — "Prediav Data for XGBoost" is read as "Predict Data
for XGBoost".)

## Components

### C-1: Data Loading
- **Purpose**: Acquire historical and real-time power-distribution data.
- **Inputs**: Raw Elia grid load series (Datetime CET/CEST, Datetime UTC, Elia Grid Load [MW]); the paper also names generic features (load consumption, voltage levels, weather, operational parameters) as typical, though the Elia dataset used has only load + timestamps.
- **Outputs**: Raw dataframe.
- **Interactions**: Feeds Preprocessing.

### C-2: Preprocessing
- **Purpose**: Clean, scale, and split the data.
- **Inputs**: Raw load series.
- **Outputs**: Cleaned, normalized, split dataset.
- **Key design choices**: Missing values handled by linear interpolation / forward filling; outliers by the IQR method; Min-Max scaling to [0,1] (Eq. 1, scikit-learn MinMaxScaler); split into train/validation/test (see constraints for the two conflicting split descriptions).
- **Interactions**: Feeds both the LSTM Phase and (its scaled features) the XGBoost Phase.

### C-3: Feature Engineering
- **Purpose**: Add datetime, lag, and rolling-window features.
- **Inputs**: Cleaned series.
- **Outputs**: Feature matrix (hour, day-of-week, month, weekday indicator; lag features $X_{lag_k}(t)=y(t-k)$ Eq. 6; rolling mean/median/std over window $N$, Eq. 7).
- **Interactions**: Combined with LSTM output as XGBoost input.

### C-4: LSTM Phase (temporal learner)
- **Purpose**: Learn temporal dependency / sequence patterns and produce a base prediction.
- **Inputs**: Normalized sequences (sequence length 60).
- **Outputs**: LSTM predictions $\hat{y}_{LSTM}$ (intermediate values), hidden state $h_t = \mathrm{LSTM}(x_t, h_{t-1})$ (Eq. 8).
- **Key design choices**: Two LSTM layers × 50 neurons; dropout layer (overfitting); dense output layer; trained to minimize RMSE.
- **Interactions**: Its output flows to the XGBoost Phase.

### C-5: XGBoost Phase (residual/non-linear refiner)
- **Purpose**: Refine the LSTM output by modeling non-linear residual structure.
- **Inputs**: LSTM predictions + engineered features; the paper also describes the residual $e_t = y_t - \hat{y}_t^{LSTM}$ (Eq. 2) as the XGBoost learning signal.
- **Outputs**: Final forecast $\hat{y}_{final} = f_{XGB}(\hat{y}_{LSTM})$ (Eq. 10), $\hat{y}_t = \sum_{k=1}^{T}\alpha_k f_k(x)$ (Eq. 9).
- **Key design choices**: n_estimators and learning rate tuned by grid search; committee of boosted decision trees.
- **Interactions**: Output goes to Evaluation.

### C-6: Evaluation
- **Purpose**: Score models on RMSE, MAPE, R2.
- **Inputs**: Final forecast + actuals.
- **Outputs**: Metric table (Table 1); visual overlays (Figures 2–7).
- **Interactions**: Terminal node (End).

## Design ambiguity (carried forward, not resolved)
The paper describes the XGBoost stage two different ways: (a) as learning the LSTM **residual** $e_t$
(Eq. 2, §3.2.3–3.2.4), and (b) as a **regression on the LSTM output** $f_{XGB}(\hat{y}_{LSTM})$
(Eq. 10, §3.6.3). It also says elsewhere XGBoost was "trained with the same feature set as the LSTM."
These are not fully reconciled in the text; see constraints.md.
