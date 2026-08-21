# Uncertainty-Handling Methods: DG Scenario Generation and EV-Cluster Prediction

Two data-side methods feed the multi-objective planning model (see formulation.md):
(1) a KDE + Frank-copula scenario generator for wind/PV output (§3), and
(2) a CNN-BiLSTM predictor for EV-cluster state (§4.1).

## 1. DG output scenario generation (KDE + Frank copula), §3

### Why not the standard alternatives (dead ends the paper argues against)
The paper reviews two mainstream schemes and rejects both (§3):
1. **Weibull (wind speed) / Beta (light intensity) distribution assumption** — "this scheme only
   carries out reliability evaluation and analysis, which cannot be applied to calculate the annual
   cost because it ignores the time scale of DG data."
2. **Day-ahead prediction-error sampling** — "the prediction limitations of this scheme are
   obvious; further processing is needed for the predicted steps."

### Step 1 — Non-parametric marginals via kernel density estimation (Eq. 4)

$$\hat{f}(x) = \frac{1}{nh} \sum_{t=i}^{T} K\!\left(\frac{x - X_i}{h}\right)$$

- $n$: sample size; $h$: window width; $K(\cdot)$: kernel function; $x$: hourly PV/WT output;
  $X_i$: hourly PV/WT output of the i-th day.
- Advantage stated in §3: "This method does not need to assume the distribution of historical
  data" — DG output data can be directly processed to obtain the output probability density
  function of DG units in each period of the day.

### Step 2 — Joint wind–solar distribution via the Frank copula (Eq. 5)

$$F^n(x^i, y^i) = C\big(F_{X_i}(x^i),\, F_{Y_i}(y^i)\big)$$

- $C(\cdot)$: copula connection function; $F_{X_i}(x^i)$, $F_{Y_i}(y^i)$: probability functions
  for wind turbines and photovoltaics, respectively.
- Copula choice rationale (§3): "Since the output of DG usually has a negative correlation and
  complementarity, the Frank copula function is selected to describe the wind–solar correlation.
  ... Frank copula can work with both non-negative and negative correlations of variables [28]."
  (Goodness of fit should in general be used to select among copula types; the paper selects Frank
  a priori on this correlation argument.)

### Step 3 — Sampling and daily-curve reconstruction (Figure 1)
Per period, the Frank copula is sampled to obtain correlated uniforms
$[u^1 \dots u^{24}; v^1 \dots v^{24}]$; each variable is passed through the inverse marginal CDF
($x^i = F_x^{-1}(u^i)$, $y^i = F_y^{-1}(v^i)$) to reconstruct the 24-hour wind (x) and PV (y)
output matrix — "Finally, a typical daily curve is generated considering DG correlation and
randomness." (§3; pipeline diagram: evidence/figures/figure1.md.)

### Step 4 — Scenario generation and reduction (§5)
In the case study, "500 wind–solar complementary scenarios are generated. Then, the generated new
energy output scenarios can be reduced, and the corresponding probability of each scenario can be
calculated." The reduced sets shown are 5 wind scenarios (probabilities 0.214, 0.196, 0.222,
0.198, 0.17 — Figure 4) and 5 PV scenarios (Figure 5). The specific reduction algorithm is cited
to Refs. [30,34,35] (similar-day clustering / COPULA-SHUFLE / improved K-means + SBR) but the
paper does not state which is used — Not specified in paper.

## 2. EV-cluster data processing via CNN-BiLSTM, §4.1

### Problem
Cluster processing of EVs largely eliminates prediction error, "however, the historical data bias
of EVs is still one of the reasons for the error."

### Architecture (Figures 2–3)
- **CNN front-end** (Figure 2: Input layer → Convolutional layer → Pooling layer → Fully
  connected layer → Output): "CNN processes the initial data through local connection and weight
  sharing, which effectively reflects the data characteristics. At the same time, the number of
  parameters in the training process is greatly reduced" [30].
- **Bi-LSTM back-end** (Figure 3: forward LSTM + reverse LSTM between input and output layers):
  "Compared with traditional LSTM, Bi-LSTM displays a reverse LSTM process, which can better
  connect historical data with future data [17]."
- **Combination**: "CNN-Bi-LSTM can further explore the relationship between the current data and
  the data at each time point to improve the prediction accuracy."

### Protocol
After knowing the maximum charge/discharge power of EVs and the historical SOC data, "the data
are divided into training groups and test groups" — the training group is used to explore the
internal connection, the test group to verify accuracy. Predicted quantities: EV inbound (arrival)
time, outbound (departure) time, and initial SOC (Figure 6; 40 test samples shown per panel).
Hyperparameters, layer sizes, and training details: Not specified in paper.

### Outcome linkage
The predicted EV-cluster data parameterize the EVS dispatchable-storage model (Eqs. 6–9,
formulation.md); reported error reductions vs standalone CNN / Bi-LSTM are filed in
evidence/figures/figure6.md and claimed in C04.
