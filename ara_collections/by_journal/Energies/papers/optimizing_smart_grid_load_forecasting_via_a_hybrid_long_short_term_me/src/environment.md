# Environment

The paper reports no code release, no hardware details, and no random seeds. Only partial
hyperparameter values are stated. The method's mathematics is captured in
[logic/solution/method.md](../logic/solution/method.md) and its structure in
[logic/solution/architecture.md](../logic/solution/architecture.md) (no fabricated code stub
is added — the paper describes a prose/equation method, not runnable code).

- **Language/runtime**: Python (version not specified, implied by TensorFlow and scikit-learn)
- **Framework / libraries**:
  - TensorFlow (version not specified) — LSTM implementation
  - scikit-learn (version not specified) — MinMaxScaler for normalization
  - XGBoost (version not specified) — gradient boosting regressor
  - Implied: pandas, NumPy, matplotlib (versions not stated)
- **Hardware**: Not specified in paper (no GPU/CPU type, RAM, or memory reported)
- **Data sources**: Elia Grid (Belgium transmission system operator) load dataset, 15-min resolution,
  1 January 2022 – 14 December 2022. Data columns: DateTime (CET/CEST), DateTime (UTC), Elia Grid
  Load (MW). Approximately 33,600 time steps. **Publicly available** from the Elia group website
  (https://www.elia.be/en/grid-data).
- **Key dependencies**: TensorFlow, scikit-learn, XGBoost (versions not stated)
- **Training / optimization protocol**:
  - LSTM architecture: 2 layers x 50 neurons, dropout layer, dense output
  - Sequence length: 60 (15-min intervals covering 15 hours look-back)
  - XGBoost hyperparameters: n_estimators and learning rate tuned by grid search (exact grid
    values and best parameters not individually reported)
  - Optimizer: not specified (LSTM "trained to minimize RMSE")
  - Epochs: not specified
  - Batch size: not specified
  - Activation functions: not specified (ReLU / tanh typical for LSTM — not confirmed in text)
- **Preprocessing**:
  - Missing values: linear interpolation or forward filling (Section 4.1 specifically states
    linear interpolation)
  - Outliers: Interquartile Range (IQR) method
  - Scaling: Min-Max normalization to [0,1] via scikit-learn MinMaxScaler
  - Feature engineering: datetime features (hour, day-of-week, month, weekday indicator);
    lag features (load at t-1, t-2, ...); rolling-window statistics (mean, median, std
    over last N periods). Exact N and full lag set not specified.
- **Train/validation/test split**: Two conflicting descriptions in the paper:
  1. Section 3.5: "training set consists of data from 1 January 2022 to 30 November 2022,
     while the testing set includes data from 1 December 2022 to 14 December 2022"
  2. Section 4.1: "the dataset was split into 80% training and 20% testing data"
  These are not equivalent and are documented as an internal inconsistency in
  `logic/solution/constraints.md`.
- **Random seeds**: Not specified in paper.

## Reproducibility note

No source code was released. The paper provides a prose description of the pipeline, seven
equations (Eqs. 1–10), and a flowchart (Figure 1). Key details needed for independent
reproduction — hardware configuration, specific hyperparameter values, optimizer settings,
epoch count, batch size, and random seeds — are absent. The split ambiguity (date-based vs
80/20) alone prevents exact replication of the reported metrics.
