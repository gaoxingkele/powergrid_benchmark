# Constraints — Boundary Conditions, Assumptions, Limitations

## Boundary conditions
- Single dataset: Elia (Belgium TSO) grid load, calendar year 2022, one geographic grid.
- Short-term horizon at 15-min resolution; sequence length 60 (15 h look-back).
- Evaluation limited to three metrics (RMSE, MAPE, R2) on one train/test split.
- Only load + timestamp columns are actually used, despite the pipeline text naming weather/voltage/operational features as "common."

## Assumptions
- A1: Load series is approximately stationary / bell-shaped (argued from Figure 4 histogram) — supports generalization.
- A2: Linear interpolation / forward-fill adequately reconstruct missing values; IQR adequately flags outliers.
- A3: Min-Max [0,1] scaling is appropriate for both the LSTM and XGBoost stages.
- A4: The chosen hold-out is representative of unseen load.

## Known limitations (paper-stated)
- **Architectural complexity**: "the hybrid model presented some challenges during the development due to the architectural complexity of combining the two learning paradigms" (§4.6).
- **Attention did not help**: an attention mechanism was tested and excluded because accuracy was "inferior to the base hybrid model" (§4.6; Abstract; §1.2; §2.3) — documented dead end (C04).
- **No hyperparameter sensitivity analysis**: future work explicitly calls for "a systematic hyperparameter sensitivity analysis" on LSTM units, sequence length, epochs, and train/test splits (§Future Work) — i.e., not done here.
- **Single-region generalization untested**: authors plan to evaluate on other regional grids (incl. the Iraqi national grid) and other resolutions to assess generalizability (§Future Work).
- **No published code / hardware**: implementation details (hardware, seeds, exact hyperparameter values, epochs) are not reported.

## Internal inconsistencies (carried forward, NOT silently resolved — Rule 16)
These are genuine tensions in the source; the ARA records them rather than picking one:

1. **Train/test split conflict**:
   - §3.5: "The training set consists of data from 1 January 2022 to 30 November 2022, while the testing set includes data from 1 December 2022 to 14 December 2022."
   - §4.1: "the dataset was split into 80% training and 20% testing data."
   These two descriptions are not equivalent (Jan 1–Nov 30 vs Dec 1–14 is not an 80/20 split of a Jan–Dec 14 series).

2. **Resolution / "hourly" vs "15-min" conflict**:
   - Abstract, §4.1, Table 2: 15-min resolution.
   - §3.5: "the hourly energy load data from Elia" — contradicts the 15-min resolution stated elsewhere. Table A1 shows 15-min timestamps (00:00, 00:15, 00:30…), supporting 15-min.

3. **Date range**: Abstract says data "throughout 2022"; §3.5 and §4.1 say 1 Jan 2022 – 14 Dec 2022 (not full year).

4. **"all four datasets"**: §5 states "for all four datasets the proposed LSTM-XGBoost hybrid model has better accuracy," but only one dataset (Elia) is actually used/reported — likely a template artifact; treated as an error, not evidence of four datasets.

5. **Residual vs output cascade**: XGBoost is described both as learning the LSTM residual $e_t$ (Eq. 2) and as a regression on the LSTM output $f_{XGB}(\hat{y}_{LSTM})$ (Eq. 10) — see architecture.md / method.md.

6. **Figure 2 label mismatch**: Figure 2 caption is "Time series plot" (framed as actual vs predicted) but the plotted title is "Load vs. Datetime" and shows only actual load points (no prediction series visible) — see evidence/figures/figure2.md.
