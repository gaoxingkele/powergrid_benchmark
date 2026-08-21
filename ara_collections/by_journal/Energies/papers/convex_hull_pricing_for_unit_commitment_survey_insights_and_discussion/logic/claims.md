# Claims

This is a **survey paper**: claims are the survey's synthesizing conclusions about the convex hull
pricing (CHP) literature for unit commitment (UC), not results of new experiments by the authors.
Each claim distills a mechanism-level takeaway the surveyed evidence supports; "Proof" points to
the survey's comparison/synthesis exercises in `logic/experiments.md`.

## C01: Convexification restores price monotonicity that discreteness destroys
- **Statement**: When energy prices are defined as the slope of a cost function with respect to demand, non-convexity introduced by discrete commitment decisions is what permits non-monotonic prices; replacing the cost function by its convex envelope over the convex hull of the feasible set removes this failure structurally, because the slope of a convex envelope is non-decreasing in demand and the convex hull contains no binary restrictions.
- **Conditions**: Holds for mixed binary linear programming problems of UC type (piecewise-linear objective, linear constraints) where prices are defined as cost-slope w.r.t. the demand vector; the survey's exposition uses a two-bin formulation without transmission constraints. Behavior under full network (nodal) models is discussed only via [18,27].
- **Sources**: []
- **Status**: supported
- **Falsification criteria**: Exhibit a UC instance where the slope of the convex envelope of the total cost over the convex hull of the feasible set decreases as demand increases, or a convex (commitment-fixed) dispatch problem whose demand-slope prices are non-monotonic.
- **Proof**: [E01]
- **Evidence basis**: §1–§2 synthesis: ED is convex (prices monotone) but omits commitment costs; UC is non-convex (prices may not be monotone); Figure 1 (evidence/figures/figure1.md) defines the convex envelope/hull geometry; §2.2 shows the convex hull price is the slope of z^{c*} w.r.t. D.
- **Tags**: convex hull pricing, monotonicity, convexification, electricity markets

## C02: Excluding a cost category from the price signal forces opaque side payments
- **Statement**: A market price computed from a problem that excludes some incurred cost category (here, commitment costs excluded by economic dispatch) structurally requires supplementary uplift payments to keep units whole; because such payments are unit-specific and not publicly disclosed, the cost exclusion converts a pricing problem into a transparency problem.
- **Conditions**: US-style ISO/RTO day-ahead and real-time markets where prices come from ED with commitment fixed; uplift comprises lost opportunity costs and make-whole payments. Untested boundary: markets with different settlement/disclosure rules.
- **Sources**: []
- **Status**: supported
- **Falsification criteria**: Demonstrate an ED-priced market (commitment costs excluded from the price) in which all units recover commitment costs without any supplementary payment, or where uplift is uniform across units at a bus and fully disclosed without transparency concerns.
- **Proof**: [E01]
- **Evidence basis**: §1: ED omits start-up/no-load costs, so "significant uplift payments are often needed"; uplift "not uniform for different units even on the same bus, causing market transparency issues since they are not publicly disclosed" [4–6].
- **Tags**: uplift payments, market transparency, economic dispatch, pricing

## C03: The primal and dual routes to convex hull prices compute the same object
- **Statement**: Convex hull prices can be reached by two formally equivalent routes — solving the convexified UC problem (whose system-constraint dual multipliers are the prices) or solving the Lagrangian dual of the original UC problem (whose optimal multipliers equal those prices) — because strong duality plus the double-conjugacy identity make the optimal dual value equal the convex envelope value, and additivity of conjugation decomposes the system envelope into per-unit envelopes.
- **Conditions**: Requires strong duality of the convexified UC problem and the conjugate-function properties (Properties 1 and 2, §3.1) over the convex hull of the unit-level constraint set; stated for the demand-balance (system-wide) constraint being the dualized coupling constraint.
- **Sources**: []
- **Status**: supported
- **Falsification criteria**: Produce a UC instance (satisfying the survey's assumptions) where the optimal multipliers of UC-Orig-Lagrangian-Dual differ from the slope of the convex envelope of total cost over the convex hull w.r.t. demand.
- **Proof**: [E01, E04]
- **Evidence basis**: §2.2 (UC-Convex, Eq. (15)–(16)): z^{c*} = q^{c*} by strong duality; §3.1 Properties 1–2 give per-unit decomposition (UC-CHP, Eq. (17)); §4.1 (Eq. (22)): optimal Lagrangian dual multipliers λ* of UC-Orig give the convex hull prices.
- **Tags**: Lagrangian duality, strong duality, conjugate function, equivalence

## C04: Convex hull prices are properties of the formulation, not just the feasible set
- **Statement**: Because convex hull prices derive from the dual function of the primal formulation, two UC formulations that yield identical primal optimal solutions can yield different convex hull prices; computational reformulations (formulation tightening, contingency-constraint screening) therefore change the priced object unless preservation conditions are verified, and even non-binding constraints can move prices.
- **Conditions**: Reported for formulation variations ISOs use to speed UC solution (tightening, security-constraint screening) per [27]; sufficient conditions for price preservation exist (e.g., for multiple representations of nodal balance constraints) but must be checked case by case.
- **Sources**: []
- **Status**: supported
- **Falsification criteria**: Show that for all UC formulation variants with the same primal optimum, the dual-function-derived convex hull prices necessarily coincide (i.e., prices depend only on the primal solution set), contradicting the reported formulation dependence.
- **Proof**: [E01]
- **Evidence basis**: §2.2 end: [27] reports convex hull prices "might not be the same" across formulations with identical primal optima; "numerical testing shows that convex hull prices can be affected by non-binding security constraints"; conclusion that "any change in the UC formulation must be carefully examined before implementation for convex hull pricing".
- **Tags**: formulation dependence, dual function, formulation tightening, constraint screening

## C05: Integer relaxation delivers the convex envelope exactly when cost convexity survives domain convexification
- **Statement**: Under a tight unit formulation, relaxing integrality convexifies the per-unit domain (the off-state point joins the generation interval), so integer relaxation yields the convex envelope of the unit cost if and only if the fuel cost remains convex over that convexified domain; when the domain convexification breaks convexity (the slope below minimum generation exceeds the first-block slope), scaling the cost function by the commitment variable — an under-estimator since the variable is at most one — restores a valid convex envelope.
- **Conditions**: Tight (ramp-free) unit formulations with piecewise-linear fuel cost whose slope is non-decreasing within blocks; start-up and no-load cost terms are linear (hence convex) and never the obstacle. Untested boundary: cost families beyond piecewise-linear/quadratic treated in [7,8].
- **Sources**: []
- **Status**: supported
- **Falsification criteria**: Exhibit a tight unit formulation with fuel cost convex over the convexified domain whose integer relaxation fails to produce the convex envelope, or show the commitment-variable-scaled cost of [8] failing to under-estimate the original cost somewhere on the convex hull.
- **Proof**: [E02]
- **Evidence basis**: §3.2: envelope-by-relaxation "if and only if the fuel cost function f_g is convex over the convex hull X_g^c"; Figure 2 (convex case) vs Figure 3 (non-convex case, x_{g,t}-scaling convexification of [8]); domain convexification {0 ∪ [P^min, P^max]} → [0, P^max].
- **Tags**: convex envelope, integer relaxation, fuel cost, convexification, tight formulation

## C06: Formulation tightness is the single property deciding whether relaxation suffices
- **Statement**: Whether the cheap route to a per-unit convex hull — integer (LP) relaxation — works is decided entirely by tightness of the unit formulation: constraints expressible as a network-flow model with integral capacities (or provably integral polyhedra) are tight, so relaxation delineates the hull; adding inter-temporal coupling such as ramp-rate constraints breaks that structure, and relaxation no longer yields the hull, forcing explicit hull constructions whose size grows exponentially with the number of time slots.
- **Conditions**: Shown for the two-bin UC unit formulation: basic constraints (capacity, start-up logic, min up/down time) are tight [7–9,30]; non-tightness with ramp rates verified in [32]; exponential growth of exact-hull descriptions per [28]. Other time-dependent constraints are asserted to have the same effect.
- **Sources**: []
- **Status**: supported
- **Falsification criteria**: Exhibit integer relaxation of a ramp-constrained two-bin unit formulation that delineates its convex hull in general, or a fractional vertex of the LP relaxation of the basic (ramp-free) constraints (3)–(9).
- **Proof**: [E02, E03]
- **Evidence basis**: §3.2 (tightness proofs: polyhedron [8], network flow [7,9], integrality theorem [30]); §3.3 (non-tightness with ramp rates [32]); §3.4 / [28]: exact-hull constraint count "grows exponentially as the number of time slots increases"; Figures 2–5.
- **Tags**: tightness, network flow, integrality, ramp rates, convex hull

## C07: Status enumeration buys generality by linearizing cost, and pays in constraint count
- **Statement**: Reformulating a unit's feasible set over enumerated commitment statuses (state-transition edges, disjunctive status unions, time-interval indicators, DP-derived dual variables) makes the cost function linear in the new variables, so integer relaxation recovers the convex envelope regardless of fuel-cost convexity or time-dependence of cost coefficients — but the enumeration itself produces a substantial-to-exponential number of constraints, so these exact methods are only practical when paired with decomposition schemes; column generation avoids reformulating cost by generating hull vertices instead, trading constraint count for potentially many extreme points.
- **Conditions**: Applies to the exact non-tight-case approaches surveyed in §3.2(3)–§3.3 ([9–14]); the decomposition pairings observed are Bienstock–Zuckerberg [9], Benders [11], and Dantzig–Wolfe column generation [14]; ramp rates break the network-flow structure of the state-transition reformulation just as in the original variables.
- **Sources**: []
- **Status**: supported
- **Falsification criteria**: Show a status-enumeration reformulation of the surveyed type whose cost is not linear in the enumeration variables (so relaxation fails to yield the envelope), or an exact hull construction from status enumeration whose constraint count does not grow with enumerated statuses/time slots.
- **Proof**: [E03]
- **Evidence basis**: §3.2(3): state-transition cost "linear with x_e and y_e", envelope by relaxation for convex or non-convex fuel cost and time-dependent commitment costs; §3.3: disjunctive (Eq. (20)–(21)) and interval approaches need "a large/significant number of constraints"; DP approach [12,13] handles time-dependent costs but yields many constraints; DW [14] "does not necessitate a reformulation of the cost function" but "may require a large number of vertices"; Figures 4–5.
- **Tags**: state transition, disjunctive programming, column generation, decomposition, computational burden

## C08: Few-slot exact hulls parameterize into scalable approximate hulls
- **Statement**: Because exact convex hull descriptions grow exponentially with the horizon, a systematic compromise is to derive exact (tight) constraints over short windows of consecutive time slots — relax integrality, enumerate vertices, drop fractional ones, convert back to constraints, then parameterize coefficients in unit parameters — and reuse those tightened constraints across arbitrarily long horizons as an approximate convex hull; this trades exactness of the resulting prices for a controlled, horizon-independent constraint budget, with approximation accuracy conventionally scored by total uplift payments (lower is more accurate).
- **Conditions**: Stated for non-tight unit formulations (ramp rates or other time-dependent constraints); the surveyed instantiations derive windows of two or three consecutive slots ([8] using [34]; general procedure [32], applied in [35]). Unit-level accuracy evaluation beyond total uplift is proposed but not yet standard.
- **Sources**:
  - "two or three" ← PDF p.12 (§3.4) «the above systematic formulation tightening approach is typically applied for two or three intervals» [result]
- **Status**: supported
- **Falsification criteria**: Show that constraints exact for short windows, parameterized and applied across all slots, systematically fail to tighten the relaxation (uplift no lower than plain integer relaxation), or that exact full-horizon hulls are computable with horizon-independent effort, removing the need for approximation.
- **Proof**: [E03, E05]
- **Evidence basis**: §3.4 and Figure 6 (evidence/figures/figure6.md): 4-step procedure (relax → drop fractional vertices → re-derive tight constraints → parameterize); [28] exponential growth motivation; §5.1: approximation accuracy "usually evaluated by the total uplift payments, i.e., the lower the value, the higher the accuracy".
- **Tags**: approximate convex hull, formulation tightening, uplift evaluation, scalability

## C09: Dual-route difficulty is non-smoothness, and every remedy relocates the cost rather than removing it
- **Statement**: Solving for convex hull prices via the Lagrangian dual is hard because the dual function is non-differentiable: subgradient directions are typically non-ascending, iterates zigzag along ridges, and classical step-size rules need an estimate of the unknown optimal dual value; the surveyed remedies (steepest-ascent extreme-point subdifferentials, level-set projection of iterates) smooth the trajectory but relocate the effort into each iteration — computing steepest-ascent directions requires exploring all revenue-maximizing generation levels per iteration, and multi-cut level variants gain accuracy at considerably more computational burden — while on large problems with many short ridges even ascent directions make little progress.
- **Conditions**: Applies to non-smooth Lagrangian duals of UC-type problems solved with subgradient-family methods [15–18,36–38]; the trajectory comparison is the survey's reading of [17] (Figure 7) and the level projection of [18] (Figure 8, Eq. (23)).
- **Sources**:
  - "α = 0.2" ← PDF p.14 (§4.2) «Ref. [ 18] reports that α = 0.2 is chosen for all experiments presented in the paper.» [result]
- **Status**: supported
- **Falsification criteria**: Demonstrate a plain subgradient method (no smoothing device, no q* knowledge) whose iterates provably do not zigzag and converge fast on non-smooth UC duals, or a smoothing device that reduces zigzag with no added per-iteration cost relative to plain subgradients.
- **Proof**: [E04]
- **Evidence basis**: §4.1–§4.2; Figure 7 (subdifferential trajectory smooth vs subgradient zigzag), Figure 8 (level-set projection); [15] slow convergence from zigzag; [16,17] "computations of ascending directions come at a price"; [18] multi-cut "adds a considerably more computational burden"; level parameter α ∈ [0,1] with α = 0 recovering Kelley's algorithm.
- **Tags**: non-smooth optimization, subgradient, zigzagging, level method, subdifferential

## C10: Decoupling multiplier updates from exact subproblem optimality resolves dual convergence, up to a stepsize-rate limit
- **Statement**: Requiring only a surrogate optimality condition — that the surrogate dual value strictly improve on the previous iterate — instead of full Lagrangian minimization yields valid, smoother update directions at reduced subproblem effort, eliminates both the optimal-dual-value guesstimate and zigzagging, and additionally supports a decision-based (rather than heuristic) upper bound on the optimal dual value whose gap to the best lower bound measures price quality more accurately and cheaply than the standard duality gap; the remaining barrier is that the non-summable step sizes guarantee only linear convergence outside a neighborhood of the optimal multipliers, limiting iteration-wise speed on large-scale problems.
- **Conditions**: Stated for the Surrogate Lagrangian Relaxation method [36] with contraction-mapping step-size rule (Eq. (25), parameters M > 1, 0 < ρ < 1) and surrogate optimality condition (Eq. (26)); quality-measure evidence is from testing reported in [41]; the acceleration route via linear-convergence potential [42,43] is a suggested improvement, not yet demonstrated for CHP.
- **Sources**:
  - "IEEE 118-bus" ← PDF p.16 (§4.3) «Testing this novel quality measure on the IEEE 118-bus system shows its advantages over the standard duality gap in terms of accuracy and computational efforts needed.» [result]
- **Status**: supported
- **Falsification criteria**: Show that iterates satisfying only the surrogate optimality condition with the contraction-mapping stepsize fail to converge to the optimal multipliers on UC duals, that zigzagging persists under SLR comparably to subgradient methods, or that the SLR-based upper/lower-bound gap is less accurate or more expensive than the standard duality gap on benchmark systems.
- **Proof**: [E04, E05]
- **Evidence basis**: §4.3: Eqs. (24)–(26); the three enumerated SLR benefits (no exact subproblem solves; no q* guesstimate; smoother zigzag-free directions); Figure 9 (novel quality measure: upper-minus-lower bound on optimal dual value vs standard duality gap = uplift); §5.1: "the 'non-summable' nature of stepsizes can only guarantee the linear convergence outside of the neighborhood of λ*".
- **Dependencies**: C09
- **Tags**: surrogate Lagrangian relaxation, surrogate optimality, quality measure, convergence rate

## C11: Decarbonization moves UC outside the regime current convex hull pricing covers
- **Statement**: The decarbonization-driven evolution of UC introduces exactly the two ingredients current CHP theory does not handle: new classes of binary variables (storage charge/discharge exclusivity, machine-learning-encoded stability constraints, reserve-commitment indicators) that reshape the convex hulls to be priced, and renewable-generation uncertainty that the predominantly deterministic CHP framework does not model — so extending CHP requires re-answering how prices, hulls, and envelopes change under these additions rather than reusing existing constructions.
- **Conditions**: A forward-looking synthesis (§5.2): grounded in existing CHP models for pumped-hydro storage [46], CCUS [47], reserve commitments [50], and one risk-mitigation use of CHP under wind uncertainty [51]; chemical battery storage, uncertainty-aware CHP, and congestion effects (e.g., the Texas wind-west/load-east pattern) remain open.
- **Sources**: []
- **Status**: hypothesis
- **Falsification criteria**: Demonstrate that existing CHP constructions apply unchanged (prices, hulls, and envelopes preserved) to UC with storage/stability/reserve binaries, or that deterministic CHP prices remain valid (no systematic mispricing) under variable renewable uncertainty and the induced congestion.
- **Proof**: [E06]
- **Evidence basis**: §5.2: two challenge families with the survey's explicit open questions (three for new binaries; four for renewable uncertainties); citations [44–51].
- **Tags**: decarbonization, energy storage, renewable uncertainty, open problems
