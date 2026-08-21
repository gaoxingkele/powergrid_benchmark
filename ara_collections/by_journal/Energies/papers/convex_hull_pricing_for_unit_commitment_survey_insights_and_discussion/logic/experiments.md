# Experiments

This is a **survey paper**. The "experiments" below are the survey's systematic comparison and synthesis exercises across the surveyed CHP literature, not new experiments run by the authors. Each experiment evaluates a family of approaches or analytical framework.

## E01: Taxonomy Construction — Primal vs Dual Categorization
- **Verifies**: C01, C02, C03, C04
- **Evidence**: evidence/figures/figure1.md; §2.1–§2.2
- **Run**: literature-based; no code
- **Setup**:
  - Source: 27 papers on convex hull pricing for UC (Web of Science)
  - Scope: two-bin UC formulation without transmission constraints
- **Procedure**:
  1. Survey the UC problem formulation (Section 2.1, Eqs. 1–14)
  2. Derive the convexified UC problem (Section 2.2, Eqs. 15–16)
  3. Establish the equivalence between the UC-CHP per-unit decomposition and UC-Convex via conjugate-function Properties 1 and 2
  4. Classify existing approaches into primal (UC-CHP) and dual (UC-Orig-Lagrangian-Dual)
- **Metrics**: classification coherence, cited-equivalence verification
- **Expected outcome**: The primal and dual routes yield identical convex hull prices; formulation dependence affects both.
- **Baselines**: None (survey synthesis)
- **Dependencies**: none

## E02: Tight-Formulation Comparison — Integer Relaxation Sufficiency
- **Verifies**: C05, C06
- **Evidence**: evidence/figures/figure2.md, evidence/figures/figure3.md, evidence/figures/figure4.md; §3.2
- **Run**: literature-based; no code
- **Setup**:
  - Methods compared: [7] network-flow (variable-as-node), [8] polyhedron, [9] state transition (edge-domain)
  - Unit formulation: basic constraints (3)–(9) without ramp rates
- **Procedure**:
  1. Verify tightness proofs for each method (network-flow integrality, polyhedron convex-combination, state-transition network-flow)
  2. Compare convex-envelope conditions: convex fuel cost vs non-convex fuel cost requiring x-scaling convexification
  3. Identify the common condition: integer relaxation yields the envelope iff the cost function is convex over the convexified domain
- **Metrics**: tightness proof validity, envelope-condition identification
- **Expected outcome**: All three methods rely on tightness of ramp-free constraints; the envelope condition reduces to convexity of fuel cost over the convexified domain.
- **Baselines**: [8] scaling convexification for non-convex fuel cost
- **Dependencies**: E01

## E03: Non-Tight and Approximate Hull Comparison
- **Verifies**: C06, C07, C08
- **Evidence**: evidence/figures/figure4.md, evidence/figures/figure5.md, evidence/figures/figure6.md; §3.3–§3.4
- **Run**: literature-based; no code
- **Setup**:
  - Methods compared: [10] disjunctive programming, [11] interval concept, [12,13] single-unit DP, [14] Dantzig–Wolfe column generation, [8,32,35] approximate hull
  - Unit formulation: with ramp-rate constraints (non-tight)
- **Procedure**:
  1. Compare exact convex-hull construction methods across computational burden (constraint count growth)
  2. Evaluate status-enumeration generality vs exponential constraint count tradeoff
  3. Assess the systematic formulation tightening approach: 4-step procedure (relax → drop fractional vertices → convert to constraints → parameterize)
  4. Compare exact vs approximate hull accuracy criterion (total uplift payments)
- **Metrics**: constraint-count growth pattern, enumeration burden, approximation accuracy criterion
- **Expected outcome**: Exact hull constructions grow exponentially; approximate hulls from short-window tightening provide scalable compromise.
- **Baselines**: Exact full-horizon hull vs approximate 2/3-slot window hull
- **Dependencies**: E02

## E04: Dual-Method Comparison — Convergence and Computational Burden
- **Verifies**: C03, C09, C10
- **Evidence**: evidence/figures/figure7.md, evidence/figures/figure8.md, evidence/figures/figure9.md; §4.1–§4.3
- **Run**: literature-based; no code
- **Setup**:
  - Methods compared: [15] subgradient simplex cutting plane, [16,17] extreme-point subdifferential, [18] level method, [36] Surrogate Lagrangian Relaxation
  - All methods solve the UC-Orig-Lagrangian-Dual problem
- **Procedure**:
  1. Compare subgradient zigzagging vs subdifferential smoothness vs level projection vs SLR surrogate direction quality
  2. Assess per-iteration computational effort for each method
  3. Evaluate the SLR three benefits: no exact subproblem solves, no q* guesstimate, zigzag-free directions
  4. Identify the SLR limitation: non-summable stepsizes give only linear convergence outside neighborhood of lambda*
- **Metrics**: convergence trajectory smoothness, per-iteration cost, requirement for q* estimate
- **Expected outcome**: Each remedy relocates rather than removes the difficulty; SLR resolves fundamental convergence issues but has iteration-wise speed limitation for large problems.
- **Baselines**: Standard subgradient method baseline vs each remedy
- **Dependencies**: E01

## E05: Quality Measure Comparison — SLR Upper Bound vs Standard Duality Gap
- **Verifies**: C08, C10
- **Evidence**: evidence/figures/figure9.md; §4.3, §5.1
- **Run**: literature-based; no code
- **Setup**:
  - Test system: IEEE 118-bus (from [41])
  - Quality measures compared: standard duality gap (= uplift) vs SLR-based upper-minus-lower bound on optimal dual value
- **Procedure**:
  1. Derive the novel SLR-based upper bound: using multiplier-oscillation concept in decision-based manner
  2. Compare accuracy: gap between upper and lower bounds on optimal dual value
  3. Compare computational effort required for each measure
- **Metrics**: accuracy of quality measure, computational effort
- **Expected outcome**: SLR-based quality measure is more accurate and computationally cheaper than standard duality gap.
- **Baselines**: Standard duality gap
- **Dependencies**: E04

## E06: Decarbonization Challenge Analysis
- **Verifies**: C11
- **Evidence**: §5.2
- **Run**: literature-based; no code
- **Setup**:
  - Scope: decarbonization-driven UC evolution
  - Sources: new binary variables (storage [45–47], stability constraints [48,49], reserve commitments [50]); renewable uncertainty [44,51]
- **Procedure**:
  1. Identify new binary variable categories entering UC (storage charge/discharge exclusivity, neural-network stability constraints, reserve commitment indicators)
  2. Identify renewable uncertainty modeling gap (CHP currently deterministic)
  3. Formulate three open questions for new binaries and four for renewable uncertainties
- **Metrics**: coverage of decarbonization challenges, open-problem formulation quality
- **Expected outcome**: Two challenge families with seven specific open questions identified; existing CHP approaches do not directly extend.
- **Baselines**: Existing CHP models (pumped hydro [46], CCUS [47], reserve [50], wind risk [51])
- **Dependencies**: E01
