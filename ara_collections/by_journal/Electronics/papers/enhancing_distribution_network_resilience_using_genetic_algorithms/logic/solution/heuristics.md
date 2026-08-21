# Heuristics

Genuine design choices/tricks stated by the paper. Numeric values are from the paper; unspecified
sensitivities/bounds are marked "Not specified in paper".

## H01: Equal-priority voltage/loss weighting with a lighter resilience weight
- **Rationale**: The three objectives are combined into one scalar fitness; the authors weight the
  voltage-profile and loss terms equally (0.4 each) and give the resilience penalty a smaller weight
  (0.2), so that steady-state performance drives the search while resilience acts as a corrective
  penalty rather than dominating it.
- **Sensitivity**: Not specified in paper (no weight-sweep reported; a single fixed vector is used).
- **Bounds**: Weights (w1, w2, w3) = (0.4, 0.4, 0.2), summing to 1.0.
- **Code ref**: Not specified
- **Source**: §5 Objective Function, p.9.

## H02: Penalty-based handling of voltage/resilience constraints (soft constraints in the fitness)
- **Rationale**: Rather than enforcing voltage limits and contingency survivability as hard
  constraints, they are folded into the fitness as penalties — f3 penalizes configurations that lead
  to voltage collapse or overloads under DER faults, and the operational fitness adds "a penalty for
  voltage deviations outside the 0.95–1.05 pu range." This keeps infeasible-but-near candidates in
  the population and lets the GA gradient toward feasibility.
- **Sensitivity**: Not specified in paper (penalty magnitude/form not given).
- **Bounds**: Voltage band 0.95–1.05 pu; f3 functional form Not specified in paper.
- **Code ref**: Not specified
- **Source**: §5 Objective Function and results, p.9.

## H03: Binary chromosome encoding with elitist (best-Ps) survival
- **Rationale**: Control variables are binary-encoded and, each generation, only the Ps lowest-error
  individuals are retained from the expanded parent+offspring pool — an elitist truncation-selection
  scheme that guarantees monotonic non-worsening of the best solution and drives the smooth
  convergence observed in Figure 5.
- **Sensitivity**: Not specified in paper.
- **Bounds**: Population Ps = 50; crossover prob 0.8; mutation rate 0.05; ≤ 100 generations (or stop
  on stagnation in mean error e_e).
- **Code ref**: Not specified
- **Source**: §3 (pp.6), §5 (p.9).
