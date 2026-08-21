# Algorithm — Modified AdaBoost + Bayesian (MC-Dropout) Uncertainty Weighting

This is the paper's core methodological contribution: a boosting loop over ten GCN-BiLSTM weak
learners, whose per-learner combination weights are then refined by a Monte Carlo Dropout uncertainty
estimate. (The paper's title says "Bayesian-Optimized"; in the *Method* the Bayesian component is
realized as MC-Dropout uncertainty quantification/weighting and dropout-based regularization — see the
scope note at the end.)

## Mathematical formulation

**Base learner output (GCN then BiLSTM):**
$$H^{(1)} = \sigma\!\left(\tilde{D}^{-\frac12}\tilde{A}\tilde{D}^{-\frac12}H^{(0)}W^{(0)}\right)\quad(\text{Eq. 1})$$
$$h_t = [\overrightarrow{h}_t,\ \overleftarrow{h}_t]\quad(\text{Eq. 8, BiLSTM concat})$$

**AdaBoost training phase** (m = 1200 training samples, K = 10 learners):
- Init: $D_1(i) = \tfrac{1}{m}$
- Per-sample error: $e_i = |\hat{y}_i - y_i|$ (Eq. 11)
- Hard-sample weight mass: $\text{weight\_sum} = \sum_{i\,|\,e_i>0.3} D_k(i)$ (Eq. 12)
- Learner weight (exponential decay): $\alpha_k = \dfrac{0.5}{\exp(\text{weight\_sum})}$ (Eq. 13)
- Sample-weight update: $D_{k+1}(i) = D_k(i)\times 1.1$ if $e_i>0.3$ (Eq. 14), else $D_{k+1}(i)=D_k(i)$ (Eq. 15)
- Normalize sample weights: $D_{k+1}(i) \leftarrow \dfrac{D_{k+1}(i)}{\sum_i D_{k+1}(i)}$ (Eq. 16)
- Learner weights $W_m$ are **not** normalized yet (deferred to the Bayesian phase).

**Bayesian (MC-Dropout) testing phase:**
- Per learner, 100 stochastic dropout passes → mean $\bar{y}$ and
  $$\text{Uncertainty} = \tfrac{1}{100}\sum_{n=1}^{100}(y_n-\bar{y})^2\quad(\text{Eq. 17})$$
- Attenuate: $W'_m = \dfrac{W_m}{1+\text{Uncertainty}}$ (Eq. 18)
- Normalize: $W''_m = \dfrac{W'_m}{\sum_{m=1}^{10} W'_m}$ (Eq. 19)
- Final prediction = weighted sum of the 10 learners' predictions using $W''_m$; a 95% interval is
  formed from the dropout-sample spread.

## Pseudocode (reconstructed from Steps 1–4 and Eqs 11–19, §2.4–2.5)

```
Input:  training set (X, y), m samples; K = 10; error threshold τ = 0.3; T = 100 MC samples
Output: final ensemble weights W'' and forecast function

# ---- AdaBoost training phase ----
D_1(i) = 1/m  for all i
for k = 1..K:
    train weak learner L_k (GCN-BiLSTM) on (X, y) weighted by D_k
    e_i = |ŷ_i - y_i|                              # Eq 11
    weight_sum = sum( D_k(i) for i where e_i > τ ) # Eq 12
    α_k = 0.5 / exp(weight_sum)                    # Eq 13  -> stored as W_k
    for each i:                                    # Eq 14/15
        D_{k+1}(i) = D_k(i) * 1.1 if e_i > τ else D_k(i)
    D_{k+1} = D_{k+1} / sum(D_{k+1})               # Eq 16 (normalize samples only)

# ---- Bayesian (MC-Dropout) testing phase ----
for m = 1..K:
    {y_1..y_T} = T stochastic dropout passes of L_m
    ȳ = mean(y_1..y_T)
    U_m = (1/T) * sum( (y_n - ȳ)^2 )               # Eq 17
    W'_m = W_m / (1 + U_m)                          # Eq 18
W'' = W' / sum(W')                                  # Eq 19
forecast(x) = sum_m W''_m * mean_dropout_pass(L_m, x)
CI_95(x)   = 95% band from pooled dropout samples
```

## Step-by-step explanation
1. **Equal start**: every training sample begins with weight 1/m.
2. **Train + score**: each weak learner is fit under current sample weights; absolute errors computed.
3. **Selective hard-sample focus**: only samples exceeding τ=0.3 accumulate into `weight_sum` and get
   their weights multiplied by 1.1 — subsequent learners focus on peaks/mutations, ignoring small
   (possibly noisy) errors.
4. **Learner weight**: `α_k` shrinks as more hard-sample mass persists (exponential decay), rewarding
   learners that leave little hard-sample residual.
5. **Uncertainty refinement**: at test time, dropout stays on; each learner's prediction variance over
   100 passes measures its instability; unstable learners are down-weighted before the final normalized
   weighted sum.
6. **Output**: point forecast + 95% predictive interval.

## Complexity analysis
- The paper states computational overhead **increases linearly with the number of weak predictors
  (K = 10) and Monte Carlo samples (100)** (§5 limitations). No formal big-O is given otherwise.
- Empirically, a full run is reported at 5 min 56 s on the stated workstation (§4.4).

## Scope / consistency note (dead end preserved)
- The Introduction (contribution 3) describes "a Bayesian optimization method based on Markov Chain
  Monte Carlo (MCMC) sampling ... probabilistic hyperparameter tuning." The Method (§2.5) instead
  implements **Monte Carlo Dropout** for uncertainty quantification and weight attenuation, and dropout
  for regularization — there is **no explicit MCMC hyperparameter-search procedure or search space
  reported**. This ARA documents the implemented MC-Dropout algorithm; the MCMC-hyperparameter-tuning
  framing appears to be an unrealized/loosely-worded claim and is flagged in `constraints.md` and the
  exploration trace.
