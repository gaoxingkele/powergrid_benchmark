# Method — Formulation, Preprocessing, and Feature Engineering

Source: §3 (Proposed Methodology), §3.1–3.6. All equations printed in the paper; no runnable code
is printed, so this is a prose/equation method (no `src/execution/` stub — see Rule 14).

## Mathematical formulation

**Min-Max normalization (Eq. 1):**
$$X_{norm} = \frac{X - \min(X)}{\max(X) - \min(X)}$$
where $X$ is the original value and $X_{norm}$ the normalized value.

**LSTM residual (Eq. 2):**
$$e_t = y_t - \hat{y}_t^{LSTM}$$
$y_t$ = actual observed value at time $t$; $\hat{y}_t^{LSTM}$ = LSTM prediction; $e_t$ = residual used as input to XGBoost.

**RMSE (Eq. 3):**
$$\mathrm{RMSE} = \sqrt{\frac{1}{n}\sum_{i=1}^{n}(y_i - \hat{y}_i)^2}$$

**MAPE (Eq. 4):**
$$\mathrm{MAPE} = \frac{1}{n}\sum_{t=1}^{n}\left|\frac{y_t - \hat{y}_t}{y_t}\right|\times 100$$

**R2 / coefficient of determination (Eq. 5):**
$$R^2 = 1 - \frac{\sum_{i=1}^{N}(y_i-\hat{y}_i)^2}{\sum_{i=1}^{N}(y_i-\bar{y})^2}$$

**Lag features (Eq. 6):**
$$X_{lag_k}(t) = y(t-k)$$

**Rolling statistics (Eq. 7):**
$$\text{Rolling Mean}(t) = \frac{1}{N}\sum_{i=t-N+1}^{t} y(i), \qquad
\text{Rolling Std}(t) = \sqrt{\frac{1}{N}\sum_{i=t-N+1}^{t}\big(y(i)-\text{Rolling Mean}(t)\big)^2}$$
where $N$ is the window size.

**LSTM hidden state (Eq. 8):**
$$h_t = \mathrm{LSTM}(x_t, h_{t-1})$$

**XGBoost prediction (Eq. 9):**
$$\hat{y}_t = \sum_{k=1}^{T}\alpha_k f_k(x)$$
$f_k(x)$ = $k$-th tree's prediction; $T$ = total number of trees.

**Hybrid final prediction (Eq. 10):**
$$\hat{y}_{final} = f_{XGB}(\hat{y}_{LSTM})$$

## Preprocessing (§3.1, §3.5, §4.1)
1. **Cleaning**: remove missing / duplicate / erroneous values; missing values handled by interpolation or forward-filling; §4.1 specifically states missing values were **linearly interpolated**.
2. **Outliers**: handled with the Interquartile Range (IQR) method.
3. **Scaling**: Min-Max to [0,1] via scikit-learn MinMaxScaler (Eq. 1).
4. **Splitting**: train / validation / test to avoid overfitting and assess generalization (see constraints.md for the two conflicting split statements).

## Feature engineering (§3.5)
- **Datetime features**: hour of day, day of week, month, weekday indicator.
- **Lag features**: previous grid loads, e.g. load at $t-1$, $t-2$ (Eq. 6).
- **Rolling-window features**: mean, median, standard deviation over the last $N$ periods (Eq. 7). The exact $N$ and full lag set are Not specified in paper.

## Model configuration (§4.2, §3.6)
- **LSTM**: sequence length 60 (15-min intervals over 15 h); two LSTM layers of 50 neurons each; dropout layer; dense output; trained to minimize RMSE.
- **XGBoost**: trained on the same feature set as the LSTM; n_estimators and learning rate tuned by grid search; committee of boosted trees.
- **Hybrid**: LSTM produces short-term prediction; XGBoost handles long-term trends / residuals; final forecast per Eq. 10.

## Stated principal benefits (§3.4)
- Improved prediction accuracy (temporal learning + non-linear refinement).
- Error reduction (captures residual errors a single model misses).
- Scalability across power-distribution tasks (forecasting, outlier/fault detection).
- Conceptual enhancement: combined high accuracy + stability suited to dynamic distribution demand.
