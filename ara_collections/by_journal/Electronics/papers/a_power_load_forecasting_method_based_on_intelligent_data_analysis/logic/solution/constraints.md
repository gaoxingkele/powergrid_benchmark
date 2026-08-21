# Constraints, Assumptions, and Limitations

## Boundary conditions
- **Domain**: Residential (user-level) electricity load; short-term forecasting. Validated on smart-meter data from Ireland; 50 users for the prediction experiments (data from "50 randomly selected users" for the decomposition analysis).
- **Forecast horizon**: One step ahead — next hour (hourly sampling) or next day (daily sampling). No multi-step horizon reported.
- **Input configuration**: 48 historical IMF component values predict the next IMF value (Table 2): hourly → 1 h sampling, sequence length 48, input length 2 days; daily → 24 h sampling, sequence length 48, input length 24 days.
- **Decomposition depth**: Number of IMF components fixed at 8 (plus one residual RES) to avoid excessive components that complicate later training.
- **Window**: 60-day sliding window, step size 1; fixed-length component segment extracted from the rear of the window. For the daily training set, a 180-day window with step 1 was used; training set of 500 days; last 30 days as test set.

## Assumptions
- A1 (decomposability): The load at any moment is a superposition of stochastic, periodic, and trend components, so decomposition into IMFs + residual is physically meaningful.
- A2 (reconstruction fidelity): CEEMDAN's near-0% reconstruction error preserves the essential information of the original sequence while distributing it among more stable components.
- A3 (window adequacy): A 60-day window is large enough to encompass the periodic and trend scales of the studied users' load.
- A4 (noise sizing): White-noise amplitude of 0.1× the data standard deviation, with 200 noise realizations, gives a decomposition that reflects the load's periodicity, trend, and other characteristics; too-small or too-large amplitude yields suboptimal decomposition.
- A5 (BN placement): Given the small scale of the electricity data, placing the BN layer after the LSTM layer works better than vertical BN before the LSTM.
- A6 (parallelism): Because each component is modeled by an independent LSTM sub-model, the sub-models can execute in parallel.

## Known limitations
- **No released code or exact hardware**: The model is built on Keras with CuDNNLSTM, but no repository, GPU model, software versions, or random seeds are reported.
- **Single-step, single-region evaluation**: Only one dataset (Irish smart meters), one region, and one-step horizons are tested; generalization to other regions, industrial/commercial load, or longer horizons is unverified.
- **Design rationale not fully ablated**: The necessity of a large window (vs a network-input-sized window), the choice of 8 IMFs, the noise amplitude (0.1× std), and the ensemble size (200) are asserted or set, not swept; their sensitivity is not quantified.
- **No statistical significance test**: RMSE/MAE are averaged/statistically analyzed over 50 users, but no per-user variance, confidence interval, or significance test of the model differences is reported.
- **Internal inconsistency in reported architecture**: The text (§5.2) states the three dense layers have 27, 8, and 1 neurons, while Figure 8 shows Dense1 output 27, Dense2 output 9, and Result output 1 — i.e. the middle dense layer is reported as 8 in text but 9 in the figure. Recorded verbatim in evidence/figures/figure8.md; not resolvable from the paper.
- **Endpoint effects only partially handled**: Endpoints are managed by linearly extending extreme points; residual endpoint error is not quantified.
- **Stated error reductions vs per-table numbers**: The conclusion states reductions of 21%, 30%, and 13% versus LSTM, RNN, and EMD-LSTM; these headline percentages are not broken down by metric/time-scale and do not correspond to a single row of Table 3 or Table 4. Recorded as the paper's claim; the per-model RMSE/MAE values are in the tables.
