# UC Problem Formulation

This file transcribes the mathematical formulation of the UC problem and its convexified version used throughout the survey.

## Original UC Problem (UC-Orig)

### Objective Function (Eq. 1)

minimize total fuel + commitment costs:

```
min_{p_{g,t}, u_{g,t}, x_{g,t}} z = ∑_{g∈G} z_g = ∑_{g∈G,t∈T} [ f_g(p_{g,t}, x_{g,t}) + c^s_g u_{g,t} + c^n_g x_{g,t} ]
```

where:
- `f_g`: piecewise linear fuel cost function, slope monotonically non-decreasing within blocks
- `c^s_g`: start-up cost of unit g
- `c^n_g`: no-load cost of unit g

### System-Level Constraints (Eq. 2)

Power balance (the only system-wide constraint considered):

```
∑_{g∈G} p_{g,t} = D_t,  ∀t∈T
```

### Unit-Level Constraints (Eqs. 3–11)

**Generation capacities (Eq. 3):**
```
x_{g,t} P^{min}_g ≤ p_{g,t} ≤ x_{g,t} P^{max}_g,  ∀g,t
```

**Start-up logic (Eqs. 4–5):**
```
x_{g,t} - x_{g,t-1} ≤ u_{g,t},  u_{g,t} ≤ x_{g,t},  ∀g,t
x_{g,t-1} + u_{g,t} ≤ 1,  ∀g,t
```

**Minimum up/down time (Eqs. 6–9):**
```
∑_{i=t-L_g+1}^{t} u_{g,i} ≤ x_{g,t},  ∀g,t
∑_{i=t-l_g+1}^{t} u_{g,i} ≤ 1 - x_{g,t-l},  ∀g,t
```

Initial conditions (Eqs. 8–9): enforcement of remaining up/down time from initial state.

**Ramp rates (Eqs. 10–11):**
```
p_{g,t} - p_{g,t-1} ≤ R_g x_{g,t-1} + V_g (1 - x_{g,t-1}),  ∀g,t
p_{g,t-1} - p_{g,t} ≤ R_g x_{g,t} + V_g (1 - x_{g,t}),  ∀g,t
```

### Compact Form (Eqs. 12–14)

```
UC-Orig: min_{p,u,x} z(p,u,x)
s.t. Ap = D
(p,u,x) ∈ X
```

## Convexified UC Problem for CHP (UC-Convex, Eq. 15)

```
UC-Convex: min_{p,u,x} z^c(p,u,x)
s.t. [λ]: Ap = D
(p,u,x) ∈ X^c
```

where:
- `z^c`: convex envelope of total cost function z
- `X^c`: convex hull of unit-level constraint set X
- `λ`: dual multipliers (convex hull prices)

### UC-Convex-Dual (Eq. 16)

```
UC-Convex-Dual: max_λ q^c(λ)
q^c(λ) ≡ min_{p,u,x ∈ X^c} { z^c(p,u,x) - λ^T(Ap - D) }
```

## Per-Unit Decomposition (UC-CHP, Eq. 17)

```
UC-CHP: min ∑_{g∈G} z^c_g(p_g, u_g, x_g)
s.t. [λ]: Ap = D
(p_g, u_g, x_g) ∈ X^c_g, ∀g∈G
```

where `z^c_g` and `X^c_g` are the per-unit convex envelope and convex hull, respectively. The equivalence holds via conjugate-function Properties 1 and 2.

## Conjugate-Function Properties

- **Property 1**: The convex envelope of a function is the double conjugate of the function itself.
- **Property 2**: Additivity applies to a conjugate function.

These properties establish that `z^c(p,u,x) = ∑_g z^c_g(p_g, u_g, x_g)` over `X^c = ∏_g X^c_g`, enabling per-unit decomposition for convex hull pricing.
