# Algorithm: Successive Contraction of Convex Relaxation (SCCR)

## Overview
The SCCR algorithm solves the non-convex ADN expansion planning model by iteratively tightening SOCP relaxation constraints through penalty terms and linear cutting-plane constraints, progressively approximating the feasible region of the original problem.

## Algorithm Pseudocode

```
Algorithm: Successive Contraction of Convex Relaxation (SCCR)
────────────────────────────────────────────────────────────
Input:  ε (convergence threshold), χ0 (initial penalty weight), ω (step-size factor)
Output: Optimal planning scheme (substation/feeder/DG/E-SOP configuration)

 1:  Initialize: k ← 0, χ(k) ← χ0
 2:  Solve SOCP-relaxed model with objective F' = F + χ(k) × F_χ
 3:  Obtain initial solution S(0)
 4:  Compute relaxation gaps g^flow_t and g^E-SOP_t for all t
 5:
 6:  repeat
 7:      k ← k + 1
 8:      χ(k) ← χ(k-1) × ω           ▷ Increase penalty coefficient
 9:
10:      Add linear cutting-plane constraints:
11:          (P_ijt^2 + Q_ijt^2)/v_it^2 - I_ij_max^2 ≤ 0,   ∀(i,j) ∈ Ω_line
12:          P_E-SOP_L,ijt - A_E-SOP·√(P_AC,ijt² + Q_AC,ijt²) ≤ 0, ∀(i,j) ∈ Ω_SOP
13:
14:      Solve modified SOCP model with updated χ(k) and cutting-plane constraints
15:      Obtain solution S(k)
16:      Compute relaxation gaps g^flow_t and g^E-SOP_t
17:
18:  until max(g^flow_t, g^E-SOP_t) < ε,  ∀t, ∀scenarios
19:
20:  return S(k)
```

## Mathematical Formulation

### Relaxation Gap Metrics

**Branch relaxation gap:**
```
g^flow_t = (P_ijt^2 + Q_ijt^2) / (I_ijt^2 × v_it^2) - 1
```

**E-SOP relaxation gap:**
```
g^E-SOP_t = (P_E-SOP_AC,ijt^2 + Q_E-SOP_AC,ijt^2) / (A_E-SOP × P_E-SOP_L,ijt) - 1
```

When g^flow_t → 0 and g^E-SOP_t → 0, the relaxation accuracy in the corresponding components is high.

### Modified Objective Function
```
min F' = F + χ(k) × F_χ
```

where:
- F = original objective function (annualized comprehensive cost)
- χ(k) = contraction coefficient at iteration k
- F_χ = penalty function = Σ_t Σ_(i,j)∈Ω_line I_ijt^2 + Σ_t Σ_i∈Ω_SOP P_E-SOP_L,ijt

The penalty term F_χ reflects the additional losses caused by line flows and flexible devices.

### Linear Cutting-Plane Constraints

After each iteration, the following linear constraints are added:
```
(P_ijt^2 + Q_ijt^2) / v_it^2 - I_ij_max^2 ≤ 0
P_E-SOP_L,ijt - A_E-SOP × sqrt(P_E-SOP_AC,ijt^2 + Q_E-SOP_AC,ijt^2) ≤ 0
```

## Convergence Criterion
The algorithm converges when the relaxation gaps in all scenarios satisfy:
```
max(g^flow_t, g^E-SOP_t) < ε
```

## Performance
- Number of iterations to convergence: 3
- Computation time: approximately 3.12 h
- Final relaxation gap: below approximately 10^(-5)
- Solution accuracy: identical to CCP (annual total cost = 148.97 × 10^4 CNY)
- Computational efficiency: approximately twice that of CCP (8 iterations, 8.32 h)
