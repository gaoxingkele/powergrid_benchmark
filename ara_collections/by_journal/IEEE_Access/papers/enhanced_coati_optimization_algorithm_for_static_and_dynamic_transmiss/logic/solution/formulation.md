# TNEP Mathematical Formulation

The paper models both Static (STNEP) and Dynamic multistage (DTNEP) TNEP with a penalized fitness
function evaluated on a DC power-flow solution (MATPOWER). Transcribed from §II, Eqs. 1–15.

## Static TNEP (STNEP)

Fitness function (Eq. 1) and objective (Eq. 2):
```
FF_S(x) = OF_S(x) + ω₁ P₁(x) + P₂(x)
OF_S(x) = Σ_{(i,j)∈Ω} c_ij n_ij
```
- FF_S(x): STNEP fitness function
- OF_S(x): STNEP objective (total investment cost of added lines)
- Ω: set of all candidate lines
- c_ij: investment cost of a line added between bus i and bus j
- n_ij: number of lines added between bus i and bus j
- ω₁: penalty weight coefficient
- P₁(x): equality-constraint penalty; P₂(x): inequality-constraint penalty

Equality penalty — nodal power balance (Eq. 3):
```
P₁(x) = Σ_{k=1}^{nb} | d_k + B_k θ_k − g_k |
```
Inequality penalty (Eq. 4):
```
P₂(x) = Σ_{l=1}^{nc} λ_l
```
Inequality penalty coefficients (Eqs. 5–7):
```
λ₁ = 0 if |f_ij| ≤ (n_ij^0 + n_ij) f_ij^max, else λ₁        (line-flow limit)
λ₂ = 0 if g_i^min ≤ g_i ≤ g_i^max, else λ₂                   (generation limit)
λ₃ = 0 if 0 ≤ nt_ij ≤ n_ij^max, else λ₃                      (line-number limit)
```
Symbols: n_b = number of buses; n_c = number of inequality limits; d_k = demand at bus k;
g_k = generation at bus k; B_k = susceptance at bus k; θ_k = voltage angle at bus k;
f_ij = load flow between buses i,j; f_ij^max = max allowed flow; g_i^min/g_i^max = generation bounds;
nt_ij and n_ij^max = total (existing+added) and maximum allowed line number between buses i,j.

## Dynamic multistage TNEP (DTNEP)

Fitness (Eq. 8) and objective (Eq. 9):
```
FF_D(x) = OF_D(x) + ω₁ P₁(x) + P₂(x)
OF_D(x) = Σ_{t=1}^{T} [ δ_inv^t Σ_{(i,j)∈Ω} c_ij^t n_ij^t ]
```
- T: a specific planning stage in the planning horizon
- c_ij^t, n_ij^t: cost and number of lines added between buses i,j in planning stage t
- δ_inv^t: discount factor in planning stage t

Discount factor (Eq. 10):
```
δ_inv^t = (1 − I)^a
```
where I = annual interest rate and a = difference between the years covered by the planning stage.

Equality (Eq. 11) and inequality (Eq. 12) penalties, dynamic form:
```
P₁^t(x) = Σ_{k=1, t=1}^{nb, T} | d_k^t + B_k^t θ_k^t − g_k^t |
P₂^t(x) = Σ_{l=1}^{nc} λ_l
```
Dynamic inequality penalty coefficients (Eqs. 13–15):
```
λ₁ = 0 if |f_ij^t| ≤ (n_ij^0 + Σ_{t=1}^{T} n_ij^t) f_ij^max, else λ₁
λ₂ = 0 if g_i^{t,min} ≤ g_i^t ≤ g_i^{t,max}, else λ₂
λ₃ = 0 if 0 ≤ Σ_{t=1}^{T} nt_ij^t ≤ n_ij^max, else λ₃
```
Superscript t denotes the planning-phase quantity.

## Worked discounting (Colombian 93-bus, §IV)

Undiscounted stage costs: P1 = US$338,744,000; P2 = US$104,750,000; P3 = US$171,547,000. With base
year 2002 and I = 10%:
```
IC_P1 = δ_inv^t × c^t = (1 − 0.1)^{2002−2002} × 338744000 = US$ 338,744,000
IC_P2 = (1 − 0.1)^{2005−2002} × 104750000 = US$ 76,362,750
IC_P3 = (1 − 0.1)^{2009−2002} × 171547000 = US$ 82,050,398.3
```
Total discounted investment cost = US$ 497,157,143.3.

## Penalty coefficients per test system (§IV)
- Garver 6-bus: ω₁, λ₁, λ₂, λ₃ = 10^5, 10^6, 10^7, 10^5
- IEEE 25-bus: ω₁, λ₁, λ₂, λ₃ = 10^8, 10^9, 10^9, 10^7
- Colombian 93-bus: ω₁, λ₁, λ₂, λ₃ = 10^9, 5×10^8, 5×10^8, 5×10^6 (all three planning stages)
