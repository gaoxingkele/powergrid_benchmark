# Constraints (Boundary Conditions, Assumptions, and Limitations)

This file captures the explicit and implicit boundaries of the survey's analysis.

## Assumptions (from the UC formulation)
- A1: Two-bin UC formulation without transmission (network) constraints is adopted for exposition; only power-balance system-level constraints are modeled (§2.1).
- A2: Fuel cost function is piecewise linear with monotonically non-decreasing slope within blocks (segments), as required in current markets [26].
- A3: Strong duality holds for the convexified UC problem (used to equate primal optimal cost and dual optimal value) (§2.2).
- A4: The survey scope is CHP for UC modeling/computation; economic analysis and non-UC applications are explicitly out of scope.

## Survey Boundary Conditions
- BC1: The survey covers 27 papers on convex hull pricing identified via Web of Science as of the writing date (2024).
- BC2: Only deterministic UC is covered in depth; stochastic/robust UC is discussed only in the decarbonization open challenges (§5.2).
- BC3: The survey does not include numerical benchmarking experiments; comparison is qualitative/structural across methods.
- BC4: The Lagrangian dual exposition dualizes the system-wide power-balance constraint only; network constraints are not dualized.
- BC5: The survey adopts a demand-balance (single system-wide) constraint as the coupling constraint; zonal/nodal formulations are discussed only via [27].

## Known Limitations of the Surveyed Approaches

### Primal Category Limitations (§5.1)
- L1: Tight-formulation methods [7–9] omit ramp-rate constraints, which is impractical for real power systems.
- L2: Non-tight-formulation methods [10–13] incur heavy computational burden from enumerating all commitment statuses.
- L3: The DW column generation approach [14] may require a large number of vertices (extreme points).
- L4: Exact convex hull description grows exponentially with the number of time slots [28].
- L5: Approximate hulls sacrifice pricing exactness; accuracy evaluation currently only at system-wide level (total uplift) rather than unit-level.

### Dual Category Limitations (continued in §5.1)
- L6: Subgradient methods [15] exhibit zigzagging and slow convergence.
- L7: Subdifferential methods [16,17] reduce zigzagging but have high per-iteration cost.
- L8: Level method [18] multi-cut variant adds considerable computational burden.
- L9: SLR [36] non-summable stepsizes guarantee only linear convergence outside the neighborhood of lambda*.
- L10: SLR convergence for large-scale problems may be impeded by iteration-wise speed.

## Open Challenge Boundaries (§5.2)
- O1: New binary variables from storage, stability constraints, and reserve commitments introduce additional complexity not handled by current CHP.
- O2: Chemical battery storage CHP models are not yet developed (pumped hydro [46] and CCUS [47] exist).
- O3: Renewable uncertainty impacts on convex hull pricing remain unclear.
- O4: Transmission congestion effects from remote renewable generation (e.g., Texas wind-west/load-east pattern) affect CHP.
