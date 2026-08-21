# Heuristics

Practical tuning heuristics the paper explicitly states for SCMPSO.

## H01: Keep the iteration budget well above the convergence floor (>=500; use 2000)
- **Rationale**: The four PSO variants all approach zero around 500 iterations; to avoid under-validating the algorithm's effectiveness with too few iterations, the budget must not fall below that floor, and a comfortable margin (2000) is used as the standard.
- **Sensitivity**: medium — below ~500 iterations reliability drops sharply; above the floor the final value is flat, so extra iterations mainly cost compute.
- **Bounds**: floor = 500 iterations «it is crucial that the number of iterations does not fall below 500»; chosen standard = 2000 «2000 iterations were chosen as the standard in this paper» (both §4.2.5).
- **Code ref**: Not specified (no released code; MATLAB 2020a).
- **Source**: §4.2.5 (Testing of the Improved Particle Swarm Algorithm), Figure 6.

## H02: Bound the inertia weight in [0.4, 0.9]
- **Rationale**: A large w over-explores (slow convergence, oscillation/instability); a small w over-exploits (local-optima trapping). Bounding between a fixed max and min, then scheduling nonlinearly, balances global and local search.
- **Sensitivity**: high — the text frames both extremes as failure modes (instability vs local-optima trapping).
- **Bounds**: wmin = 0.4, wmax = 0.9 «wmax is the maximum weight factor, set to 0.9, and wmin is the minimum weight factor, set to 0.4» (§4.2.2).
- **Code ref**: Not specified.
- **Source**: §4.2.2 (Adaptive Weight Iteration Improvement), Eqs. 26-27.

## H03: Choose Henon chaotic-map parameters with a in [1,2] and small b in [0,1]
- **Rationale**: Parameter a controls the population's nonlinearity (higher a = more chaotic/diverse); b controls symmetry and coupling strength affecting the overall trajectory, with smaller values typically used to keep the trajectory well-behaved.
- **Sensitivity**: medium — a governs diversity/chaos level; b governs trajectory stability.
- **Bounds**: a in [1,2], b in [0,1] «The value range for a is [1, 2], and for b, it is [0, 1]» (§4.2.1); smaller b usually used.
- **Code ref**: Not specified.
- **Source**: §4.2.1 (Chaotic Mapping Population), Eq. 25.

## H04: Switch oscillation vs progressive convergence at the half-way iteration (Tmax/2)
- **Rationale**: Early in the run, larger oscillation factors (two-sided perturbation) widen exploration and help escape local minima; later, smaller factors give a one-sided damped approach for stable refinement. The midpoint of the run is used as the switch.
- **Sensitivity**: Not specified in paper (only the midpoint threshold is shown; no scan of alternative thresholds).
- **Bounds**: threshold at t = Tmax/2; lambda bounded by (2 sqrt(c r) - 1)/(c r) — lower bound for t <= Tmax/2, upper bound for t > Tmax/2 «When the iteration count t ≤ Tmax/2, the algorithm exhibits oscillation convergence» / «When the iteration count t > Tmax/2, the algorithm exhibits progressive convergence» (§4.2.4).
- **Code ref**: Not specified.
- **Source**: §4.2.4 (Improvement in Algorithm Iteration), Eqs. 30-34.
