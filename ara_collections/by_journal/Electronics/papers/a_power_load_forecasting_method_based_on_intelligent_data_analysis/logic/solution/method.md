# Method: The CEEMDAN-LSTM Forecasting Pipeline

The proposed method (CEEMDAN-LSTM) is a two-stage decompose-then-forecast pipeline for
non-stationary residential load. Stage 1 decomposes each user's load series into physically
meaningful sub-components via sliding-window CEEMDAN; Stage 2 forecasts each component with a
dedicated LSTM sub-model and overlays (reconstructs) the component forecasts into the final
prediction.

## Stage 0 — Data analysis premise
A user's load is a multi-scale time series with periodicity (hours/days/weeks/months/years) plus
random behavior. Directly forecasting this raw non-stationary signal hinders extraction of deeper
temporal features. The method therefore first characterizes the load by separating it into trend,
periodic, and random components (§3.3, §5.1).

## Stage 1 — Sliding-window CEEMDAN decomposition

### 1a. Decomposition mathematics (EMD → EEMD → CEEMDAN)
- **EMD (§3.1)**: Iteratively sift the signal — identify extrema, fit upper/lower envelopes by cubic
  spline interpolation, compute the envelope mean $m(t)$, and form $h(t)=x(t)-m(t)$ (Eq. 1). Repeat
  until $h(t)$ meets the two IMF conditions (zero envelope mean; extrema and zero-crossings equal or
  differ by ≤1). Accept an IMF when the standard-deviation criterion satisfies $0.1<SD<0.3$ (Eq. 2).
  Subtract each IMF to get residuals (Eqs. 3–4) until the residual is monotonic; the signal
  reconstructs as $x(t)=\sum_{i=1}^{n} c_i + r_n(t)$ (Eq. 5). Flowchart: evidence/figures/figure1.md.
- **EEMD (§3.2)**: To fight mode mixing, add Gaussian white noise $\omega_n(t)$ to the signal
  (Eq. 6), EMD each noisy realization (Eq. 7), and ensemble-average IMFs/residuals over $N$
  realizations (Eqs. 8–9). Costly and leaves residual noise.
- **CEEMDAN (§3.3)**: Add adaptive noise via the EMD-mode operator $E_k(\cdot)$ at each stage with a
  per-stage coefficient $\varepsilon_k$ controlling the signal-to-noise ratio. Step 1: average the
  first IMF over $I$ noisy trials, $\widetilde{IMF_1}=\frac{1}{I}\sum_i IMF_1^{i}$ (Eq. 10). Step 2:
  residual $r_1(t)=x(t)-\widetilde{IMF_1}$ (Eq. 11). Step 3: build ensemble residual signals and
  extract successive modes (Eqs. 12–14). Step 4: stop when the residual has fewer than 3 extreme
  points; final reconstruction $x(t)=\sum_{k=1}^{K}\widetilde{IMF_k}+r_K(t)$ (Eq. 15). Achieves
  nearly 0% reconstruction error with fewer averaging runs than EEMD. Small-amplitude noise suits
  high-frequency-dominated signals; large-amplitude noise suits low-frequency-dominated signals.

### 1b. Sliding-window segmentation (§3.3, §5.1)
- Design a window large enough to encompass the periodic and trend components of the load; sizing
  the window to the network input length would fail to separate trend from periodicity.
- Concrete setting: window spans **60 days**, moved at **step size 1**. After decomposing the data
  within each window, extract a fixed-length component segment from the **rear (posterior)** of the
  window (Figure 2 / evidence/figures/figure2.md).
- **Endpoint effects**: handled by **linearly extending the extreme points**.
- **Depth**: number of IMF components capped at **8** to prevent excessive components that would
  complicate later training; decomposition yields IMF1–IMF8 plus a residual RES.
- **Noise settings (experiment)**: white-noise amplitude = **0.1× the standard deviation** of the
  original data; **200 sets** of white noise added.

### 1c. Component roles (§5.1, Figure 7)
Empirically, for a representative user's hourly load: **IMF1–IMF3** are high-frequency with no
regular pattern (stochastic/random components); **IMF4–IMF7** show significant periodicity (periodic
components); **IMF8 and RES** show prominent trend (trend components). This maps the decomposition
onto the load-property characterization (random + periodic + trend).

## Stage 2 — Per-component LSTM forecasting and reconstruction (§4)
- Each IMF/residual component is forecast by its **own LSTM sub-model**; because the sub-models are
  independent, they can run **in parallel**.
- Each sub-model (see logic/solution/architecture.md): an LSTM layer whose **last-time-step output**
  summarizes the whole input sequence → **Batch Normalization** (placed after LSTM) → **Dropout** →
  **three fully connected (Dense) layers** → the predicted next component value.
- Preprocessing: **Batch Normalization** (Eqs. 16–19) normalizes each mini-batch (mean $\mu_P$,
  variance $\sigma_P^2$, normalized $\hat{x}_i$, scaled/shifted $y_i=\gamma\hat{x}_i+\beta$) to keep
  hidden-layer inputs in a common distribution and act partly as data augmentation against
  overfitting. **Dropout** (probability 0.5) randomly deactivates neurons to regularize.
- **Input protocol**: 48 historical IMF component values predict the next IMF component value
  (Table 2). The final overall load prediction is obtained by **overlaying (reconstructing)** the
  per-component predictions.

## Stage 3 — Evaluation (§5.2)
- Compare CEEMDAN-LSTM (experimental group) against RNN, LSTM, and EMD-LSTM (comparison group).
- Metrics: **RMSE** (Eq. 20, stability) and **MAE** (Eq. 21, accuracy), statistically analyzed over
  50 users, at both hourly and daily granularity.
- Results: evidence/tables/table3.md (hourly), evidence/tables/table4.md (daily),
  evidence/figures/figure9.md and figure10.md (prediction overlays).

## Pipeline summary
```
raw user load x(t)
   │  (data analysis: multi-scale, non-stationary)
   ▼
[Sliding window, 60-day span, step 1, rear-segment extraction, linear endpoint extension]
   ▼
[CEEMDAN decomposition]  →  IMF1..IMF8 + RES   (stochastic / periodic / trend)
   ▼
[per-component LSTM sub-model]  (BN → Dropout → 3× Dense),  48-in → 1-out,  run in parallel
   ▼
[overlay / reconstruct component forecasts]  →  final load prediction ŷ(t+1)
   ▼
[evaluate RMSE, MAE vs RNN / LSTM / EMD-LSTM]
```
