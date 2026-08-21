# Related Work

This survey organizes 27 papers on convex hull pricing for unit commitment. The full reference list (51 entries) is in the original paper. Below is the typed dependency graph for the core CHP literature.

## Foundational Works

### RW01: Gribik, Hogan & Pope, 2007
- **DOI**: — (Cambridge, MA working paper)
- **Type**: baseline
- **Delta**: Introduced the convex hull pricing concept: prices defined as slope of the convex envelope of total cost over the convex hull of the UC problem.
- **Claims affected**: C01, C02, C03
- **Adopted elements**: Definition of convex hull prices; relationship to uplift (duality gap = uplift).

### RW02: Falk, 1969
- **DOI**: 10.1137/0107035
- **Type**: baseline
- **Delta**: Established conjugate-function properties (double conjugate = convex envelope; additivity of conjugation) underpinning per-unit decomposition of CHP.
- **Claims affected**: C03
- **Adopted elements**: Properties 1 and 2 used to prove UC-CHP ↔ UC-Convex equivalence.

### RW03: Balas, 1998
- **DOI**: 10.1016/S0166-218X(97)00141-0
- **Type**: baseline
- **Delta**: Disjunctive programming theorem expressing convex hull as convex combination of per-status feasible regions.
- **Claims affected**: C07
- **Adopted elements**: Theoretical foundation for the disjunctive approach [10].

## Primal-Route Methods (Case 1: Tight Formulation)

### RW04: Chao, 2019 (Ref. [7])
- **DOI**: 10.1007/s11149-019-09388-x
- **Type**: extends
- **Delta**: Network-flow model (variable-as-node) of basic UC constraints; tightness via integrality theorem; integer relaxation yields convex hull.
- **Claims affected**: C05, C06
- **Adopted elements**: Network-flow representation of UC; tightness proof for ramp-free constraints.

### RW05: Hua & Baldick, 2016 (Ref. [8])
- **DOI**: 10.1109/TPWRS.2016.2636746
- **Type**: extends
- **Delta**: Polyhedron tightness proof; x-scaling convexification for non-convex fuel cost; general convex-envelope framework; approximate hull via 2/3-slot tightening.
- **Claims affected**: C05, C06, C08
- **Adopted elements**: Cost convexification via commitment-variable scaling; systematic formulation tightening procedure.

### RW06: Alvarez et al., 2019 (Ref. [9])
- **DOI**: 10.1109/TPWRS.2019.2952703
- **Type**: extends
- **Delta**: State-transition diagram (edge-domain xe, ye) reformulation; cost linear in enumeration variables; Bienstock–Zuckerberg decomposition for large-scale LP.
- **Claims affected**: C06, C07
- **Adopted elements**: State-transition enumeration; edge-based cost linearization.

## Primal-Route Methods (Case 2: Non-Tight Formulation)

### RW07: Schiro et al., 2015 (Ref. [10])
- **DOI**: 10.1109/TPWRS.2015.2505876
- **Type**: extends
- **Delta**: Disjunctive programming convex-hull formulation for ramp-rate-constrained UC; general linear-constraint framework; many constraints from status enumeration.
- **Claims affected**: C07
- **Adopted elements**: Disjunctive convex-hull for non-tight unit formulations.

### RW08: Knueven et al., 2022 (Ref. [11])
- **DOI**: 10.1016/j.cie.2021.107806
- **Type**: extends
- **Delta**: Time-interval concept for convex hull; Benders decomposition for computational performance.
- **Claims affected**: C07
- **Adopted elements**: Interval-based enumeration; Benders decomposition.

### RW09: Guan et al., 2018 (Ref. [12,13])
- **DOI**: 10.1080/24725854.2017.1405900
- **Type**: extends
- **Delta**: Single-unit commitment DP-to-dual mapping; convex hull in dual-variable domain; handles time-dependent costs naturally.
- **Claims affected**: C07
- **Adopted elements**: DP-based convex hull; dual-variable domain mapping.

### RW10: Andrianesis et al., 2021 (Ref. [14])
- **DOI**: 10.1109/TPWRS.2021.3126541
- **Type**: extends
- **Delta**: Dantzig–Wolfe column generation builds convex hull iteratively via extreme points; no cost-function reformulation needed; finitely convergent.
- **Claims affected**: C07
- **Adopted elements**: Column generation for convex hull pricing; extreme-point construction.

## Dual-Route Methods

### RW11: Wang et al., 2013 (Ref. [15])
- **DOI**: 10.1109/TPWRS.2013.2242506
- **Type**: extends
- **Delta**: Subgradient simplex cutting plane for ELMPs; foundation for subdifferential methods.
- **Claims affected**: C09
- **Adopted elements**: Subgradient approach; adaptive three-level scheme.

### RW12: Wang et al., 2013 (Ref. [16,17])
- **DOI**: 10.1109/TPWRS.2013.2245391 / 10.1109/TPWRS.2013.2245395
- **Type**: extends
- **Delta**: Extreme-point subdifferential method for steepest ascent directions; alleviates zigzagging but high per-iteration cost.
- **Claims affected**: C09
- **Adopted elements**: Steepest-ascent subdifferential; convergence trajectory comparison.

### RW13: Stevens & Papavasiliou, 2022 (Ref. [18])
- **DOI**: 10.1109/TPWRS.2021.3139009
- **Type**: extends
- **Delta**: Level method (Kelley-based) with projection onto level set; multi-cut variant; alpha = 0.2 parameter.
- **Claims affected**: C09
- **Adopted elements**: Level-set projection; supergradient upper bound.

## SLR and Convergence Works

### RW14: Bragin et al., 2015 (Ref. [36])
- **DOI**: 10.1007/s10957-014-0617-3
- **Type**: extends
- **Delta**: Surrogate Lagrangian Relaxation with contraction-mapping step-size rule; surrogate optimality condition eliminates need for full minimization and q* guesstimate.
- **Claims affected**: C10
- **Adopted elements**: Surrogate subgradient; contraction-mapping step-size (Eq. 25); surrogate optimality condition (Eq. 26).

### RW15: Bragin et al., 2023 (Ref. [41])
- **DOI**: — (arXiv:2304.07990)
- **Type**: extends
- **Delta**: Novel SLR-based quality measure (upper-minus-lower bound on optimal dual value); more accurate and cheaper than standard duality gap.
- **Claims affected**: C10
- **Adopted elements**: SLR-based upper bound; IEEE 118-bus testing.

### RW16: Bragin, 2024 (Ref. [42]); Bragin & Tucker, 2022 (Ref. [43])
- **DOI**: 10.1007/s10479-023-05308-z / 10.1038/s41598-022-28209-6
- **Type**: bounds
- **Delta**: Linear convergence potential for SLR; surrogate "level-based" Lagrangian relaxation; proposed as acceleration route for CHP.
- **Claims affected**: C10
- **Adopted elements**: Linear convergence analysis; potential acceleration for large-scale CHP.

## Related Application Areas

### RW17: Garcia et al., 2020 (Ref. [22])
- **DOI**: 10.1109/TCNS.2020.2988899
- **Type**: bounds
- **Delta**: Generalized CHP for AC OPF; extends convex hull pricing beyond DC UC.
- **Claims affected**: C01
- **Adopted elements**: CHP application beyond UC scope.

### RW18: Dominguez et al., 2019 (Ref. [6])
- **DOI**: 10.1016/j.ijepes.2019.05.064
- **Type**: bounds
- **Delta**: Reserve procurement and flexibility in renewable-dominated systems with different market designs.
- **Claims affected**: C11
- **Adopted elements**: RES impact on market design.

## Tightness and Formulation Works

### RW19: Yan et al., 2019 (Ref. [32])
- **DOI**: 10.1109/TPWRS.2019.2933651
- **Type**: extends
- **Delta**: Systematic formulation tightening for UC; general procedure for 2/3-slot convex hulls; non-tightness of ramp-rate-constrained formulations.
- **Claims affected**: C06, C08
- **Adopted elements**: 4-step formulation tightening procedure; ramp-rate non-tightness verification.

### RW20: Damci-Kurt et al., 2016 (Ref. [28])
- **DOI**: 10.1007/s10107-015-0941-5
- **Type**: bounds
- **Delta**: Polyhedral study of production ramping; exponential growth of convex hull description with time slots.
- **Claims affected**: C08
- **Adopted elements**: Exponential growth motivation for approximate hulls.

### RW21: Zhao et al., 2023 (Ref. [27])
- **DOI**: 10.1109/TEMPR.2023.3265590
- **Type**: refutes
- **Delta**: Shows convex hull prices depend on UC formulation; formulation tightening and constraint screening change prices even with identical primal optima; sufficient conditions for price preservation.
- **Claims affected**: C04
- **Adopted elements**: Formulation-dependence analysis; price-preservation conditions.

## Decarbonization-Related Works

### RW22: Guo et al., 2021 (Ref. [45]); Qu et al., 2022 (Ref. [46]); Lu et al., 2024 (Ref. [47])
- **DOI**: various
- **Type**: bounds
- **Delta**: CHP models for energy storage (pumped hydro, CCUS); binary variables for storage charge/discharge exclusivity.
- **Claims affected**: C11
- **Adopted elements**: Storage CHP modeling as starting point for open problems.

### RW23: Akhundov et al., 2023 (Ref. [51])
- **DOI**: 10.1007/s10669-023-09937-0
- **Type**: bounds
- **Delta**: CHP for risk mitigation under wind uncertainty; transforms stochastic UC into deterministic problem via CHP.
- **Claims affected**: C11
- **Adopted elements**: Uncertainty-aware CHP as starting point for renewable integration.
