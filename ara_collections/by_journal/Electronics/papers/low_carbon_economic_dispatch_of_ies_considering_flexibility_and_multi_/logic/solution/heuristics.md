# Heuristics — Improved-PSO Implementation Tricks

Only the tricks the paper actually states (§3.3.1). All are diversity/convergence mechanisms for the upper-level solver.

## H01: Nonlinearly decreasing inertia weight
- **Rationale**: A large inertia weight early gives strong global exploration; decreasing it over iterations shifts the swarm toward local refinement near high-quality solutions, reducing premature stalling (§3.3.1).
- **Sensitivity**: Not specified in paper (w_max/w_min values for Eq. 26 not given; a separate 0.9→0.4 linear schedule is reported in §4.1 for a parameter sanity check).
- **Bounds**: w ∈ [w_min, w_max]; concrete bounds Not specified in paper.
- **Code ref**: [src/execution/improved_pso.py]
- **Source**: §3.3.1, Eq. (26).

## H02: Sine-function learning factors
- **Rationale**: Coupling c1 (cognitive) and c2 (social) to sine functions of t/T lets the search emphasize global exploration early (large c1) and local exploitation late (large c2), balancing the two phases automatically (§3.3.1).
- **Sensitivity**: Not specified in paper. (Reported fixed sanity-check values c1=2, c2=1.5 in §4.1 differ from the adaptive Eq. 27 form.)
- **Bounds**: By construction c1, c2 ∈ [0, 2] (from Eq. 27's 2·√(·) with the sine term in [0,1]).
- **Code ref**: [src/execution/improved_pso.py]
- **Source**: §3.3.1, Eq. (27).

## H03: Four-subpopulation partition with distinct update rules
- **Rationale**: Splitting the swarm into four sub-populations — standard update, cognitive-only, social-only, and a sine positional perturbation — maintains search diversity so particles are less likely to collapse into a shared local optimum under the many equality (balance) constraints of the IES model (§3.3.1; motivation in §1/§3.3).
- **Sensitivity**: high — this is the paper's principal mechanism credited with the improved convergence/closeness/variance (Table 7, Figure 16); removing it reduces to plain PSO (the weaker baseline).
- **Bounds**: Four fixed sub-populations; partition sizes Not specified in paper. Sub-pop 4 uses a ∈ (0,1).
- **Code ref**: [src/execution/improved_pso.py]
- **Source**: §3.3.1, Eqs. (28)–(31).

## H04: DBO-tuned PSO parameters
- **Rationale**: The Dung Beetle Optimizer is used to tune the PSO parameters, further reducing the chance of falling into local optima (§3.3, "PSO algorithm with improved parameters by the Dung Beetle Optimizer (DBO)").
- **Sensitivity**: Not specified in paper.
- **Bounds**: Not specified in paper.
- **Code ref**: Not specified (DBO tuning procedure not detailed; DBO also used standalone as a baseline in §4.3).
- **Source**: §3.3 (paragraph after Eq. 25).

## H05: TOPSIS compromise selection from the Pareto front
- **Rationale**: The multi-objective solve yields a Pareto front, not one solution; TOPSIS picks the solution with highest relative closeness to the ideal, giving a single deployable compromise between operator profit and flexibility (§3.3).
- **Sensitivity**: Not specified in paper (also reused as the convergence/closeness metric in §4.3).
- **Bounds**: Closeness ∈ [0,1].
- **Code ref**: Not specified in paper (TOPSIS is standard; not reimplemented here).
- **Source**: §3.3, ref [24].
