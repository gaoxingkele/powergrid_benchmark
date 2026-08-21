# Problem Specification

This is a **survey/review paper**. The "problem" here is the state of knowledge the survey
organizes: why convex hull pricing (CHP) exists, what gaps in the literature the survey fills, and
what open challenges it identifies. Observations are drawn from the surveyed body of work, not from
new experiments run by the authors.

## Observations

### O1: Energy prices from economic dispatch omit commitment costs
- **Statement**: ISOs/RTOs set energy prices from the economic dispatch (ED) problem, defined as the slope of the total cost function with respect to demand. Because ED fixes commitment decisions and treats all variables as continuous, it is convex and prices are monotonically non-decreasing — but it ignores commitment (start-up and no-load) costs.
- **Evidence**: §1 (Introduction), page 1–2; citations [2,3].
- **Implication**: Generators must be compensated for uncovered commitment costs through supplementary uplift payments.

### O2: Uplift payments undermine market transparency
- **Statement**: Uplift payments (lost opportunity costs and make-whole payments) are not uniform across units even on the same bus and are not publicly disclosed, causing market-transparency issues; this has driven significant research toward reducing uplift.
- **Evidence**: §1, page 2; citations [4,5,6].
- **Implication**: A pricing mechanism that reduces or reflects uplift is desirable.

### O3: Unit commitment is non-convex, giving non-monotonic prices
- **Statement**: The UC problem has discrete (commitment) and continuous (generation) variables with a piecewise-linear objective and linear constraints — a mixed binary linear program that is non-convex, so prices derived from it may not increase monotonically with demand.
- **Evidence**: §1, page 1–2; citations [2,3,4].
- **Implication**: Directly pricing off UC is problematic; a convexification is needed.

### O4: Convex hull pricing is defined but scattered across a small literature
- **Statement**: Convex hull pricing — the slope of the convex envelope of the total cost function over the convex hull of the UC problem — was introduced in [4]; its slope is non-decreasing in demand and avoids binary variables. As per the Web of Science database there are 27 papers on convex hull pricing, developed by various groups [7–18], but no survey exists to organize them from a modeling standpoint.
- **Evidence**: §1, page 2; "As per the Web of Science database, there are 27 papers published on convex hull pricing"; citations [4,7–18].
- **Implication**: A systematic survey can link and compare the scattered approaches.

### O5: Two solution routes exist and are provably equivalent
- **Statement**: Current CHP-for-UC approaches split into (i) solving the convexified UC ("UC-CHP" primal) problem and (ii) solving the Lagrangian dual of the UC problem; the optimal dual multipliers of the second equal the convex hull prices computed by the first.
- **Evidence**: §1 bullet list (page 2); §2.2, §4.1.
- **Implication**: The survey can organize the field into a primal category and a dual category with a common price object.

## Gaps

### G1: No modeling-oriented survey of convex hull pricing for UC
- **Statement**: Despite active development, no survey links, compares, and organizes the various CHP approaches for UC from a modeling and computation standpoint.
- **Caused by**: O4.
- **Existing attempts**: Economic-analysis treatments exist [19–21] and CHP has been used beyond UC (AC OPF [22], smart-grid real-time pricing [23], demand response [24,25]), but none is a modeling survey of CHP for UC.
- **Why they fail**: They address economics or other applications, not a unified modeling taxonomy of the UC convex-hull-pricing computation.

### G2: Exact convex hull is hard to delineate under practical constraints
- **Statement**: The exact convex hull of each unit requires a facial description of a high-dimensional polytope with a number of inequalities/vertices that grows exponentially with the number of time slots, especially once ramp rates make the unit formulation non-tight.
- **Caused by**: O3, O5.
- **Existing attempts**: Network flow [7], polyhedron [8], state transition [9] (tight, but omit ramp rates); disjunctive [10], interval [11], single-unit [12,13], Dantzig–Wolfe [14] (handle ramp rates but enumerate statuses / many vertices).
- **Why they fail**: Tight-formulation methods assume no ramp rates (impractical); non-tight methods incur heavy computational burden from status enumeration or vertex count.

### G3: Dual approaches suffer non-smooth convergence problems
- **Statement**: The Lagrangian dual of the UC problem is non-differentiable; subgradient directions are non-ascending and zigzag along ridges, giving slow convergence, and traditional methods need a guesstimate of the optimal dual value q*.
- **Caused by**: O5.
- **Existing attempts**: Subgradient simplex cutting plane [15], extreme-point subdifferential [16,17], level method [18], and Surrogate Lagrangian Relaxation (SLR) [36].
- **Why they fail**: Subgradient methods zigzag; subdifferential/level methods reduce zigzagging but are computationally costly per iteration; SLR resolves convergence but its non-summable stepsize gives only linear convergence outside a neighborhood of λ*, limiting iteration-wise speed for large problems.

### G4: Decarbonization introduces new modeling challenges CHP does not yet address
- **Statement**: Power-system decarbonization introduces new binary variables (storage, stability constraints, reserve commitments) and renewable-generation uncertainty that current, largely deterministic CHP does not handle.
- **Caused by**: the broader energy transition [44].
- **Existing attempts**: CHP models for pumped-hydro storage [46] and CCUS [47]; a risk-mitigation use of CHP for wind uncertainty [51].
- **Why they fail**: Chemical battery storage models, uncertainty-aware CHP, and congestion effects remain open.

## Key Insight
- **Insight**: The entire landscape of convex-hull-pricing-for-UC approaches can be organized under one modeling lens: every approach either (a) constructs the per-unit convex envelope and convex hull and solves the convexified UC ("primal" UC-CHP), or (b) solves the Lagrangian dual whose optimal multipliers ARE the convex hull prices ("dual"); and the per-unit decomposition (via conjugate-function additivity) plus the notion of formulation "tightness" together explain when integer relaxation suffices and when it does not.
- **Derived from**: O4, O5; §2.2, §3.1.
- **Enables**: A two-category, three-case taxonomy (tight / non-tight / approximate for the primal; subgradient / subdifferential / level / SLR for the dual) that lets a reader place, compare, and identify the limitations of any CHP approach, and reveals concrete improvement directions.

## Assumptions
- A1: A two-bin UC formulation without transmission (network) constraints is adopted for exposition; only power-balance system-level constraints are considered (§2.1).
- A2: The fuel cost function is piecewise linear with monotonically non-decreasing slope within blocks, as required in current markets [26].
- A3: Strong duality holds for the convexified UC problem (used to equate primal optimal cost and dual optimal value) (§2.2).
- A4: The survey scope is CHP for UC modeling/computation; economic analysis and non-UC applications are explicitly out of scope (deferred to [19–25]).
