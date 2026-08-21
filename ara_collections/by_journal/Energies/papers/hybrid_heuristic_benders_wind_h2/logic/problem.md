# Problem: Two-Stage Stochastic Wind-Hydrogen Investment Planning with Black-Box Costs

## Domain
Power systems planning under uncertainty — specifically, capacity sizing for a Wind-Hydrogen Integrated Energy System (WH-IES) comprising wind generation, electrolyzer, hydrogen storage tank, and fuel cell.

## Problem Type
Mixed-integer two-stage stochastic programming with a non-convex, non-analytical (black-box) first-stage cost function and a linear second-stage recourse.

## Formulation

### Stage I (Investment / Here-and-Now)
Minimize annualized investment cost + expected annual operating cost:

```
min_x   F = C_inv(x) + E_ξ[Q(x, ξ)]
```

where:
- `x = [x_WT, P_EL, E_H2, P_FC]^T`
  - `x_WT ∈ {0,1}` — binary wind farm construction decision
  - `P_EL ∈ R_+` — electrolyzer capacity (MW)
  - `E_H2 ∈ R_+` — hydrogen storage tank capacity (MWh)
  - `P_FC ∈ R_+` — fuel cell capacity (MW)
- `C_inv(x)` — annualized investment cost, includes:
  - Wind power: fixed turnkey cost (binary) — `C_WT(x_WT) = κ_WT · x_WT` ($75M for 50 MW farm)
  - Electrolyzer: linear — `C_EL(P_EL) = κ_EL · P_EL`
  - Fuel cell: linear — `C_FC(P_FC) = κ_FC · P_FC`
  - Hydrogen tank: non-convex black-box — `C_H2(E_H2) = max(C_min, C_base(E_H2) + C_cyc(E_H2))`
    - `C_base(E_H2)`: power-law (x^0.7) with step discount at 50 MWh
    - `C_cyc(E_H2)`: sinusoidal perturbation (stylized proxy for irregular pricing)
    - `C_min`: minimum investment threshold ($1M)
  - Annualization: `C_inv(x) = (1/L) * Σ C_i` with L = 10 years

### Stage II (Operation / Wait-and-See)
For each scenario s, solve LP:

```
Q(x, ξ_s) = 365 * min Σ_t [ λ_t_buy · P_grid_buy_{s,t} - λ_t_sell · P_grid_sell_{s,t} + ρ_shed · σ_load_{s,t} ]
```

Subject to:
1. Power balance
2. Hydrogen mass balance (with storage losses)
3. Investment capacity constraints
4. Cyclic storage boundary (S_H2_{s,0} = S_H2_{s,24})

## Difficulty
- The hydrogen-tank investment cost `C_H2(E_H2)` is non-convex, non-differentiable, and potentially available only through a black-box evaluator (supplier quotation logic, compiled simulation, neural network).
- The operational recourse model is a large-scale LP (500 scenarios × 24 hours) — solving it inside every metaheuristic function evaluation is computationally prohibitive.

## Key Parameters
- N = 500 scenarios (reduced from 1000 via Monte Carlo + scenario reduction)
- T = 24 hours (daily operation, annualized ×365)
- L = 10 years (economic recovery horizon)
- κ_WT = $75M (fixed wind farm cost)
- κ_H2 = $500 × 10^3 /MWh (tank cost coefficient)
- κ_cyc = $100 × 10^3 (sinusoidal perturbation amplitude)
- C_min = $1 × 10^6 (minimum tank investment)

## Why Not Standard Approaches?
- **Direct MINLP (Gurobi)**: Cannot process black-box/non-analytical functions
- **MILP reformulation**: Requires excessive binary variables for high-frequency sinusoidal components; impossible for true black-box evaluators
- **Pure heuristic (GSOA+Simulation)**: Computationally prohibitive (~4.86 hours)
- **C&CG / robust optimization**: The problem is stochastic (expectation), not robust (worst-case); and C&CG requires explicit master formulation
