# Concepts

Genuine technical terms defined in the survey (Sections 1–5). Notation follows the paper.

## Convex Hull Pricing (CHP)
- **Notation**: prices = slope of `z^{c*}(p*(D), u*(D), x*(D))` w.r.t. demand `D`; equivalently `λ*`
- **Definition**: A pricing mechanism in which convex hull prices are obtained as the slope of the convex envelope of the total cost function over the convex hull of a UC problem, taken with respect to the demand vector D. First introduced in [4]. The slope is non-decreasing in demand and avoids non-convex binary commitment variables.
- **Boundary conditions**: Defined for the UC problem; the survey focuses on UC (modeling/computation). Extends to AC OPF [22], smart-grid real-time pricing [23], demand response [24,25], but those are out of scope.
- **Related concepts**: Convex envelope, Convex hull, Uplift payment, Lagrangian dual multipliers.

## Convex Envelope
- **Notation**: `z^c` (system), `z_g^c(p_g, u_g, x_g)` (per unit)
- **Definition**: The "tightest" convex function that supports (under-estimates) the cost function from below; equivalently the double conjugate of the cost function over the convex hull. For CHP it is the convex envelope of the total UC cost function `z`.
- **Boundary conditions**: Over a specified convex hull `X^c`. Obtainable by integer relaxation iff the underlying (fuel) cost function is convex over that convex hull; otherwise a convexification (e.g., scaling by the commitment variable in [8]) is required.
- **Related concepts**: Convex hull, Double conjugate function, Fuel cost function.

## Convex Hull
- **Notation**: `X^c` (system), `X_g^c` (per unit)
- **Definition**: The smallest convex set that contains all feasible solutions of a UC problem (or per-unit formulation). The convexification of the unit-level constraint set X.
- **Boundary conditions**: For a "tight" unit formulation, integer relaxation of the formulation delineates the convex hull; when ramp-rate (or other time-dependent) constraints make the formulation non-tight, integer relaxation does not give the convex hull and the number of defining inequalities/vertices grows exponentially with the number of time slots.
- **Related concepts**: Tight formulation, Integer relaxation, Convex envelope.

## Unit Commitment (UC) problem
- **Notation**: UC-Orig: `min_{p,u,x} z(p,u,x)` s.t. `Ap = D`, `(p,u,x) ∈ X`
- **Definition**: The scheduling problem minimizing total fuel + commitment (start-up `c_g^s` and no-load `c_g^n`) costs over units G and time slots T, with binary start-up `u_{g,t}` and commitment `x_{g,t}` decisions and continuous generation `p_{g,t}`, subject to system-wide power balance and unit-level constraints (capacity, start-up logic, min up/down time, ramp rates). A mixed binary linear program; non-convex.
- **Boundary conditions**: Survey adopts a two-bin formulation without transmission constraints; only power-balance system constraints are modeled.
- **Related concepts**: Economic dispatch, Convexified UC (UC-Convex), Unit formulation.

## Economic Dispatch (ED)
- **Notation**: —
- **Definition**: The dispatch problem obtained by fixing UC commitment decisions; all variables continuous, hence a convex LP. Energy prices are the slope of its total cost with respect to demand and are monotonically non-decreasing.
- **Boundary conditions**: Does not consider commitment costs; therefore requires uplift payments to compensate units.
- **Related concepts**: Unit commitment, Uplift payment, Marginal cost.

## Uplift Payment
- **Notation**: —
- **Definition**: Supplementary payments to generators to compensate for costs not accounted for in the market price (e.g., start-up and no-load costs); includes lost opportunity costs and make-whole payments.
- **Boundary conditions**: Not uniform across units even on the same bus; not publicly disclosed (transparency issue). In the dual view, the standard duality gap equals the uplift payment.
- **Related concepts**: Convex hull pricing, Duality gap, Economic dispatch.

## Unit formulation (and Tightness)
- **Notation**: `X_g` (feasible region of unit g); tight ⇔ integer relaxation delineates `X_g^c`
- **Definition**: The per-unit feasible region defined by unit-level constraints. A unit formulation is "tight" when its integer (LP) relaxation delineates its convex hull. Basic constraints (3)–(9) without ramp rates give a tight formulation; adding ramp rates (10)–(11) makes it non-tight.
- **Boundary conditions**: Proved tight via network-flow integrality [7,9] and polyhedron argument [8] for the ramp-free basic constraints; non-tightness with ramp rates verified in [32].
- **Related concepts**: Integer relaxation, Network flow model, Convex hull.

## Integer relaxation
- **Notation**: relax `x_{g,t}, u_{g,t} ∈ {0,1}` to `≥ 0`
- **Definition**: Replacing binary restrictions with non-negativity (LP relaxation). For tight formulations it yields the convex hull without changing the optimal discrete values; combined with a convex cost it yields the convex envelope.
- **Boundary conditions**: Only yields the convex hull for tight formulations (no ramp rates for [7–9]).
- **Related concepts**: Tight formulation, LP, Convex hull, Convex envelope.

## Double conjugate function
- **Notation**: `z^c = (z)^{**}`
- **Definition**: The convex envelope of a function equals its double conjugate (Property 1). Additivity of conjugation (Property 2) lets the system convex envelope be written as a sum of per-unit convex envelopes. Underpins the per-unit decomposition of CHP. Relevant concepts in [29].
- **Boundary conditions**: Used to establish equivalence between UC-CHP (per-unit) and UC-Convex (system) and between the Lagrangian dual value and the convex envelope value.
- **Related concepts**: Convex envelope, Conjugate function, Lagrangian dual.

## Lagrangian dual problem (of UC)
- **Notation**: `UC-Orig-Lagrangian-Dual: max_λ q(λ)`, `q(λ) ≡ min_{(p,u,x)∈X} { z(p,u,x) − λ^T(Ap − D) }`
- **Definition**: The dual obtained by relaxing the system-wide constraint `Ap = D` with multipliers λ. At optimum the dual value equals the convex envelope value; the optimal multipliers λ* (the coefficient prior to D) give the convex hull prices.
- **Boundary conditions**: Non-differentiable ("non-smooth") dual function; subgradient directions non-ascending, causing zigzagging and slow convergence; naive methods require a guesstimate of the optimal dual value q*.
- **Related concepts**: Convex hull pricing, Subgradient, Surrogate Lagrangian Relaxation, Duality gap.

## Extended Locational Marginal Price (ELMP)
- **Notation**: —
- **Definition**: An approximation of convex hull prices computed by the subgradient simplex cutting plane approach [15].
- **Boundary conditions**: Approximate (not exact) convex hull prices; foundation for the subdifferential approaches [16,17].
- **Related concepts**: Convex hull pricing, Subgradient method, Locational marginal price.

## Surrogate Lagrangian Relaxation (SLR)
- **Notation**: `λ_t^{k+1} = λ_t^k + s_{SLR}^k · g̃_e(p^k, r^k)`; step rule Eq. (25); surrogate optimality condition Eq. (26)
- **Definition**: A decomposition-and-coordination method [36] updating multipliers with surrogate subgradients that require only the surrogate optimality condition (not full minimization of the Lagrangian), with a contraction-mapping step-size rule. Fundamentally resolves Lagrangian-relaxation convergence issues; outperforms ALR and ADMM [39,40].
- **Boundary conditions**: Three benefits — subproblems need not be solved optimally, no q* guesstimate, smoother/zigzag-free directions. Limitation: non-summable stepsizes guarantee only linear convergence outside a neighborhood of λ*, impeding iteration-wise convergence for large-scale problems.
- **Related concepts**: Surrogate subgradient, Lagrangian dual, Level method, Convex hull pricing.

## Surrogate subgradient
- **Notation**: `g̃_e(p^k, r^k)`
- **Definition**: A search direction under SLR that need not fully minimize the Lagrangian; only the surrogate optimality condition (26) — the surrogate dual value strictly decreases relative to the previous iterate's — must hold. Gives smoother directions than subgradients.
- **Boundary conditions**: Requires the contraction-mapping step-size rule (25) with parameters M > 1, 0 < ρ < 1.
- **Related concepts**: SLR, Subgradient, Contraction mapping.

## Level method
- **Notation**: level set: `q(λ) ≥ α·UB_k + (1−α)·LB_k`, α ∈ [0,1]
- **Definition**: A cutting-plane method [18] based on Kelley's algorithm that constructs an upper bound of the dual via supergradients and a lower bound via the best dual value, stopping on their relative difference. It stabilizes updates by projecting the price iterate onto a level set rather than taking the cutting-plane optimum (α = 0 recovers Kelley's algorithm; the paper uses α = 0.2). A multi-cut variant adds a cut per generator subproblem.
- **Boundary conditions**: Multi-cut gives more accurate solutions at higher computational burden.
- **Related concepts**: Kelley's algorithm, Cutting plane, Supergradient, Lagrangian dual.

## Network flow model (integral capacities)
- **Notation**: constraints g(p,u,x) = H with integral vertices
- **Definition**: A representation of the basic UC constraints (3)–(9) as a unimodular network-flow model with integral capacities; by the integrality theorem [30] its LP relaxation has integral vertices, so integer relaxation yields the convex hull. Used in [7] (variable-as-node) and [9] (edge domain (x_e, y_e)).
- **Boundary conditions**: Only valid without ramp rates; ramp constraints break the network-flow structure.
- **Related concepts**: Tight formulation, State transition diagram, Convex hull.

## State transition diagram
- **Notation**: edges e with binary `x_e`, continuous `y_e`
- **Definition**: A graph enumerating commitment statuses of a unit across time slots; binary x_e activates a transition edge, continuous y_e is generation above P_g^min on that edge. The cost function becomes linear in (x_e, y_e), so integer relaxation yields the convex envelope regardless of fuel-cost convexity or time-dependent costs. Basis of [9].
- **Boundary conditions**: Enumeration causes many constraints (heavy burden), addressed by Bienstock–Zuckerberg decomposition; breaks down with ramp rates.
- **Related concepts**: Network flow model, Bienstock–Zuckerberg algorithm, Dynamic programming.

## Disjunctive programming (convex-hull via status enumeration)
- **Notation**: `X_g = ∪_{j∈J_g} X_g^j`; convex hull via convex combination (Eq. 20–21)
- **Definition**: Formulating the convex hull as a convex combination of the per-status feasible regions [10], from Balas' disjunctive programming [33]. General (handles any linear, time-dependent constraints) but requires many constraints over all statuses.
- **Boundary conditions**: General framework; heavy computational burden.
- **Related concepts**: Interval concept, Convex hull, Benders decomposition.

## Dantzig–Wolfe (DW) decomposition / column generation
- **Notation**: —
- **Definition**: Constructs the convex hull of the overall UC iteratively by generating extreme points (feasible schedules) with negative reduced cost in a restricted master problem; converges finitely and gives exact convex hull prices from the dual without reformulating the cost function [14].
- **Boundary conditions**: May require a large number of vertices (extreme points).
- **Related concepts**: Column generation, Extreme point, Convex hull.
