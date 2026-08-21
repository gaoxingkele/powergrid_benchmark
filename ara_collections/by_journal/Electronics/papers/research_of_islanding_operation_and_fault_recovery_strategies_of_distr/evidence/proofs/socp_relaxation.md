# Second-order cone relaxation of the branch power flow + scenario-weighted stochastic form

- **Source**: Section 2.2 (Eqs. 16-20), Section 4.2 (Eqs. 43-48)
- **Statement**: The nonconvex distribution-network islanding/operation and fault-recovery models are
  cast as (mixed-integer) second-order cone programs (SOCP), then extended to a scenario-weighted
  stochastic SOCP to handle wind/PV uncertainty.
- **Assumptions used**: radial (tree) island topology (A: radiality enforced by Eqs. 3-12);
  branch power flow (DistFlow) model; Weibull wind and normal-error PV distributions.

## Derivation sketch

**1. Branch flow with conic relaxation.**
The exact branch-flow coupling U_{i,t}^2 I_{ij,t}^2 = P_{ij,t}^2 + Q_{ij,t}^2 is relaxed to the
rotated second-order cone inequality (Eq. 16):

    U_{i,t}^2 * I_{ij,t}^2 ≥ P_{ij,t}^2 + Q_{ij,t}^2 ,  ∀ ij ∈ E, t ∈ T

Nodal active/reactive balance (Eqs. 17-18) and the big-M voltage-drop equalities (Eqs. 19-20, with
M_v = U_max^2 to relax lines that are disconnected, y_{ij,t}=0) complete the convex model. The paper
states this relaxation is exact for radial distribution networks.

**2. Standard SOC form.**
The n-dimensional second-order cone (Eq. 43): C = { (u, t) | ||u||_2 ≤ t, t ≥ 0 }.
Constraint feasible region (Eq. 44): ||A x + b||_2 ≤ c' x + d, with x∈R^n, b∈R^w, c∈R^n, d∈R,
A∈R^{w×n}. Deterministic model (Eq. 45): min f(x) s.t. ||Ax+b||_2 ≤ c'x+d, g(x)=0, h(x)≤0.

**3. Scenario-weighted stochastic extension.**
Wind/PV uncertainty is represented by scenario generation (Latin hypercube sampling of N=500 curves
from the Weibull/normal models) + K-means scenario reduction to K=5 typical scenarios with weights
ρ_s (Eqs. 46). Two extreme scenarios are appended (max-wind/min-PV and min-wind/max-PV) to form the
expanded set Ψ_com (Eq. 47). The uncertainty-aware model (Eq. 48):

    min  Σ_{s∈Ψ_com} ρ_s f(x, y_s)
    s.t. ||A x + b||_2 ≤ c' x + d,  g(x, y_s) = 0,  h(x, y_s) ≤ 0,  ∀ s ∈ Ψ_com

Here x = here-and-now decisions, y_s = scenario-dependent recourse. Solved with CPLEX 12.10.

## Note
The paper does not provide a formal exactness proof of the SOC relaxation; it asserts accuracy for
radial networks (standard DistFlow-SOCP result). Treated here as a reconstructed derivation of the
paper's stated modeling steps, not an original theorem.
