# Uncertainty Modeling and Solving Method (§4)

## 1. Uncertainty models (§4.1)

### Wind
- Wind speed ~ Weibull distribution (Eq. 40):
  g_i(v) = (k_i/c_i)·(v_i/c_i)^{k_i−1}·exp[−(v_i/c_i)^{k_i}]
  with shape k_i and scale c_i estimated statistically from measured data.
- Turbine power curve (Eq. 41): P^wind_{i,t} = 0 for v_i ≤ v_c or v_i > v_d;
  P_{r,i}·(v_i − v_c)/(v_r − v_c) for v_c < v_i ≤ v_r; P_{r,i} for v_r < v_i < v_d
  (cut-in v_c, rated v_r, cut-out v_d).

### Photovoltaic
- PV prediction error ~ normal distribution; PV active-output density (Eq. 42):
  f(P^pv_{i,t}) = 1/(√(2π)·σ^pv_{i,t}) · exp[ −((P^pv_{i,t} − µ^pv_{i,t})/(√2·σ^pv_{i,t}))² ]
  with expected output µ^pv_{i,t} and standard deviation σ^pv_{i,t}.

## 2. Scenario generation (§4.2, §5.1)
- Latin hypercube sampling generates N output scenarios of wind/solar plants (case study: N = 500
  daily curves at 15-min resolution, 96 points/day), each superimposing Weibull/normal-derived
  randomness on a measured typical-day base profile (Hubei Province microgrid project data;
  JZ818 smart meter, precision level 1.0, error ≤ 1%).

## 3. Scenario reduction ("restoration") — K-means (§4.2)
1. Set cluster number K; randomly pick K cluster centers C_i. Distance metric (Eq. 46):
   d(X, C_i) = sqrt( Σ_{j=1}^{M} (X_j − C_{ij})² ).
2. Assign each scenario to its nearest center.
3. Recompute each center as its cluster mean; iterate.
4. Stop at the iteration cap or when centers stop changing → K representative scenarios (case
   study: K = 5).
5. Weight each representative scenario by its cluster size → ρ_i.

## 4. Extreme-scenario augmentation (Eq. 47)
Ψcom = Ψtyp ∪ { (P^wind_{i,max}, P^pv_{i,min}), (P^wind_{i,min}, P^pv_{i,max}) }
— the reduced typical set plus "max wind / min PV" and "min wind / max PV", to keep recovery
strategies resilient to fluctuations beyond the typical scenarios.

## 5. Second-order cone programming shell (§4.2)
- n-dimensional SOC (Eq. 43): C = {(u, t) : ‖u‖₂ ≤ t, t ≥ 0}, u ∈ R^{n−1}, t ∈ R.
- Feasible region (Eq. 44): ‖Ax + b‖₂ ≤ c′x + d, x ∈ R^n, b ∈ R^w, c ∈ R^n, d ∈ R, A ∈ R^{w×n}.
- Deterministic model (Eq. 45): min f(x) s.t. ‖Ax + b‖₂ ≤ c′x + d, g(x) = 0, h(x) ≤ 0 — both the
  islanding/operation model and the recovery model fit this form (via Eqs. 16–20).

## 6. Scenario-weighted stochastic model (Eq. 48)

min Σ_{s∈Ψcom} ρ_s · f(x, y_s)
s.t. ‖Ax + b‖₂ ≤ c′x + d, g(x, y_s) = 0, h(x, y_s) ≤ 0, ∀s ∈ Ψcom

Shared decisions x with per-scenario constraint satisfaction; objective weighted by scenario
probabilities ρ_s. Solved with the mature commercial software **CPLEX 12.10**.

**Source**: §4.1–§4.2, pp. 9–11; §5.1 pp. 11–13. Derivation notes:
[../../evidence/proofs/socp_relaxation.md](../../evidence/proofs/socp_relaxation.md).
