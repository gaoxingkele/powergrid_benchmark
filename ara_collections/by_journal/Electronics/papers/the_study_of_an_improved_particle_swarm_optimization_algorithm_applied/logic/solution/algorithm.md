# Algorithm: SCMPSO (Improved Second-Order Oscillation Chaotic-Mapping PSO)

The paper's proposed solver. Baseline PSO plus four coordinated modifications. Source: §4.

## 1. Baseline PSO (§4.1)

Standard velocity/position update:

```
V_i^{k+1} = w V_i^k + r1 c1 (Xpbest_i^k - x_i^k) + r2 c2 (Xgbest_i^k - x_i^k)     (Eq. 23)
X_i^{k+1} = X_i^k + V_i^{k+1}                                                     (Eq. 24)
```
- w: inertia weight; c1: individual (cognitive) learning factor; c2: group (social) learning factor.
- r1, r2: random numbers in [0,1]; Xpbest: individual best; Xgbest: global best at iteration k.
- Weakness (§4.1): local optima, premature convergence, uneven particle distribution.

## 2. Modification 1 — Henon chaotic-mapping initialization (§4.2.1)

```
X_{i+1}^k = F(x,r) = 1 - a * (X_i^k)^2 + b * X_i^k     (Eq. 25)
```
- a in [1,2] controls nonlinearity/chaos; b in [0,1] controls symmetry/coupling (smaller b typical).
- Purpose: replace random init to spread particles diversely, expand global search range, speed convergence.
- Steps: (1) define the Henon function producing a D-dimensional vector; (2) map population positions through it.

## 3. Modification 2 — Adaptive nonlinear inertia weight (§4.2.2)

```
b = (fit_i - fit_gbest) / (fit_0 - fit_gbest)                       (Eq. 26)
w = wmax + (wmax - wmin)(1 - 1/b),   if b >= 1                       (Eq. 27, upper)
w = wmin + b (wmax - wmin),          if b < 1                        (Eq. 27, lower)
```
- fit_i: current particle fitness; fit_gbest: best population fitness; fit_0: critical fitness.
- wmax = 0.9, wmin = 0.4.
- Purpose: large w early (global search), nonlinearly decreased later (local search).

## 4. Modification 3 — Dynamic learning factors (§4.2.3)

```
c1 = 2 * sin^2[(pi/2)(1 - t/Tmax)]     (Eq. 28)   -> monotonically decreasing
c2 = 2 * sin^2(pi t / (2 Tmax))        (Eq. 29)   -> monotonically increasing
```
- t: current iteration; Tmax: max iterations. Both bounded in [0,2], crossing at t = Tmax/2.
- Purpose: cognitive emphasis early (diversity), social emphasis late (convergence).

## 5. Modification 4 — Second-order oscillation velocity update (§4.2.4)

```
V_i^{k+1} = w v_i^k
          + u1 [ Xpbest_i^k - (1+lambda1) Xgbest_i^k + lambda1 Xgbest_i^{k-1} ]
          + u2 [ Xpbest_i^k - (1+lambda2) Xgbest_i^k + lambda2 Xgbest_i^{k-1} ]     (Eq. 30)

u1 = c1 * r1,  c1 = 2 sin^2[(pi/2)(1 - t/Tmax)],  r1 = random     (Eq. 31)
u2 = c2 * r2,  c2 = 2 sin^2(pi t / (2 Tmax)),     r2 = random     (Eq. 32)
```
Regime switching by iteration threshold:
```
t <= Tmax/2 (oscillation convergence):   lambda1 >= (2 sqrt(c1 r1) - 1)/(c1 r1),  lambda2 >= (2 sqrt(c2 r2) - 1)/(c2 r2)   (Eq. 33)
t >  Tmax/2 (progressive convergence):   lambda1 <= (2 sqrt(c1 r1) - 1)/(c1 r1),  lambda2 <= (2 sqrt(c2 r2) - 1)/(c2 r2)   (Eq. 34)
```
- lambda1, lambda2: progressive-convergence and oscillation-convergence factors.
- Uses both current (Xgbest^k) and previous (Xgbest^{k-1}) global best — the "second-order" aspect — to inject controllable perturbation near the optimum and escape local minima.

## 6. Pseudocode — model-solution procedure (§4.3 Steps 1-8; matches Figure 7 flowchart)

Reconstructed from the paper's enumerated Steps 1-8 (prose, not printed code):

```
Step 1: Initialize SCMPSO parameters: 100 particles, 50 dimensions/particle, 2000 iterations;
        current iteration = 0; scheduling period = 24 h.
Step 2: Input load data, electricity-price data, and PV/WT/DG/ESS parameters.
Step 3: Initialize particle population (Henon chaotic mapping) and assign dimension values.
Step 4: Using the scheduling strategy and constraints, adjust operating states of PV, WT, DG, ESS.
Step 5: If max iterations reached -> output scheduling strategy, optimal particle fitness,
        and minimum operating cost.
Step 6: Else -> update particle positions and velocities (Eqs. 27-34) and the global best;
        compute current individual and global best fitness.
Step 7: Revise scheduling strategy from individual/global best positions and their fitness;
        compute current minimum operating cost.
Step 8: If max iterations reached -> output results; else repeat Steps 6-7.
```

## 7. Complexity
- Not specified in paper. (Only fixed budget is given: population 100, dimension 50, 2000 iterations.)

## 8. Validation summary
- Benchmarks: Sum of Different Powers, Schwefel, Rastrigin, Rosenbrock, Levy (dimension 50, acceptance 0.01, optimum 0; Table 3).
- Comparators: PSO, CPSO, QPSO under identical settings (Figures 5-6).
- Convergence mechanism illustrated by Figure 2 (learning factors), Figure 3 (oscillation regime), Figure 4 (progressive regime).
