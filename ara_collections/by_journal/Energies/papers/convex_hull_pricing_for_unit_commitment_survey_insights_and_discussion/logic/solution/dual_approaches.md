# Dual Approaches to Convex Hull Pricing

This file covers the dual route to convex hull prices: solving the Lagrangian dual of the original UC problem.

## Lagrangian Dual Problem (UC-Orig-Lagrangian-Dual, Eq. 22)

```
UC-Orig-Lagrangian-Dual: max_λ q(λ)
q(λ) ≡ min_{p,u,x ∈ X} { z(p,u,x) - λ^T(Ap - D) }
```

The optimal multipliers λ* equal the convex hull prices (the slope of the convex envelope w.r.t. demand D).

## Key Difficulty: Non-Smoothness

The dual function q(λ) is non-differentiable: subgradient directions are non-ascending, causing zigzagging and slow convergence.

## Method 1: Subgradient Simplex Cutting Plane [15]

- Generates cuts from subgradients at query points
- Adaptive three-level scheme for next-query computation
- Computes Extended Locational Marginal Prices (ELMPs, an approximation)
- Suffers from multiplier zigzagging

## Method 2: Extreme-Point Subdifferential [16,17]

- Steepest ascent direction by minimizing squared error between demand and generation while maximizing revenues
- Eliminates zigzagging and does not require q*
- High per-iteration cost: must explore all revenue-maximizing generation levels
- For large problems, many short ridges limit progress even with ascent directions

## Method 3: Level Method [18]

- Based on Kelley's cutting-plane algorithm
- Upper bound via supergradients; lower bound via best dual value
- Projects price iterate onto level set instead of taking cutting-plane optimum
- Level set: `q(λ) ≥ α·UB_k + (1-α)·LB_k`, α ∈ [0,1]
- Paper uses α = 0.2 (α = 0 recovers Kelley's algorithm)
- Multi-cut variant adds one cut per generator subproblem (more accurate, higher burden)

## Method 4: Surrogate Lagrangian Relaxation (SLR) [36]

### Surrogate Subgradient Update (Eq. 24)

```
λ^{k+1}_t = λ^k_t + s^k_{SLR} · \tilde{g}_e(p^k, r^k)
```

### Contraction-Mapping Step-Size Rule (Eq. 25)

```
s^k_{SLR} = (1 - 1/(M·k^{1-ρ})) · s^{k-1}_{SLR} · ||\tilde{g}_e(p^{k-1}, r^{k-1})|| / ||\tilde{g}_e(p^k, r^k)||
```

where M > 1 and 0 < ρ < 1.

### Surrogate Optimality Condition (Eq. 26)

```
\tilde{L}(λ^k, x^k, u^k, p^k, r^k) < \tilde{L}(λ^k, x^{k-1}, u^{k-1}, p^{k-1}, r^{k-1})
```

### Three Key Benefits

1. Subproblems not required to be solved optimally (only surrogate optimality needed)
2. No q* guesstimate needed (avoids slow convergence from heuristic adjustments)
3. Surrogate directions are smoother; zigzagging eliminated

### Remaining Limitation

The "non-summable" nature of step-sizes can only guarantee linear convergence outside the neighborhood of λ*, impeding fast iteration-wise convergence for large-scale problems.

### SLR-Based Quality Measure [41]

- Novel upper bound for the optimal dual value, derived from multiplier-oscillation concept
- Quality measure = difference between upper and lower bounds of optimal dual value
- Tested on IEEE 118-bus system; showed advantages over standard duality gap
- Lower bound: best available Lagrangian dual value
- Upper bound: decision-based (not heuristic) "level" inference
