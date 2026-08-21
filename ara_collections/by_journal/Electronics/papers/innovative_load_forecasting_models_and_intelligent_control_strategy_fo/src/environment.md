# Environment

Reproducibility record. This is an experimental deep-learning paper, but it releases **no code and few implementation details**; most fields below are unspecified in the source and are marked as such rather than guessed. No pseudocode is printed, so no `src/execution/` stub is warranted (the method lives in `logic/solution/`); only standard/foundational LSTM/GRU equations (traceable to refs [27], [28]) and the claimed-but-unformalised attention/gating modifications appear.

- **Language/runtime**: Not specified in paper (deep-learning implementation implied; framework not named)
- **Framework**: Not specified in paper (no TensorFlow/PyTorch/Keras version given)
- **Hardware**: Not specified in paper (GPU/CPU type, count, memory all absent)
- **Data sources**: Regional hourly load CSVs collected from Kaggle, described as sourced from energy service providers and government agencies. Quantitative results use five files — `AEP_hourly.csv`, `COMED_hourly.csv`, `DAYTON_hourly.csv`, `DEOK_hourly.csv`, `DOM_hourly.csv`; qualitative comparison plots (Figure 9) additionally reference `EKPC_hourly.csv`, `NI_hourly.csv`, `PJM_Load_hourly.csv`. These correspond to the public "PJM Hourly Energy Consumption" dataset family. Per-file row counts, date ranges, and train/validation/test splits: Not specified in paper. Features: date/time, temperature (°C), load (MW), price (Cents/kWh) (Table 1). Data Availability Statement: "The data will be made available on request."
- **Key dependencies**: Not specified in paper
- **Protocols**:
  - Preprocessing: per-feature min–max normalisation to [0,1] (Eqs. 1–2).
  - Training: next-timestamp load prediction; loss minimises squared error (Eq. 15); optimisation via gradient descent + backpropagation.
  - Evaluation: MSE (Eq. 16) and MAPE (Eq. 17) per dataset.
  - Control-strategy evaluation: simulation of ESS/DR/DER dispatch over a 12-month horizon; simulator not specified.
- **Hyperparameters**: learning rate, hidden dimensions, number of hidden layers, dropout rate, epochs, batch size, sequence/lookback length — all discussed as tunable in §3 but **not specified numerically in the paper**.
- **Random seeds**: Not specified in paper
