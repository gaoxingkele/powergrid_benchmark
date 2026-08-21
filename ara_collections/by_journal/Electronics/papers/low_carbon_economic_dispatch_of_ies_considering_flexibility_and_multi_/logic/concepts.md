# Concepts

## Integrated Energy System (IES)
- **Notation**: —
- **Definition**: A system that unifies production, transmission, conversion, and consumption of multiple energy forms (electricity, heat, gas, cooling). Here a park-level IES coupling electricity/heat/cooling via gas turbine, electric boiler, absorption/electric chillers, battery, heat-storage tank, WT, PV, grid, and EVs (Figure 2).
- **Boundary conditions**: Park-level scope; extendable to regional level as future work (§5).
- **Related concepts**: Flexibility resource, Multi-energy coupling.

## Flexibility demand / supply margin
- **Notation**: P_u^t, P_d^t (demand, Eq. 1); F_u^t, F_d^t (supply, Eq. 5)
- **Definition**: Upward/downward flexibility demand is the positive/negative part of the net-load increment between consecutive periods (Eq. 1). Upward/downward flexibility supply is the sum of margins from energy-conversion equipment (Eq. 2), storage (Eq. 3), load demand response (Eq. 4), and EVs (Eq. 18).
- **Boundary conditions**: Directional (up vs down); evaluated per time step t.
- **Related concepts**: Flexibility evaluation indicator, Ramping constraint.

## Flexibility evaluation indicator (F_e, F_h, F_q)
- **Notation**: F_e = (F_u^e + F_d^e)/(2 P_L^e), likewise F_h, F_q (Eq. 6)
- **Definition**: Dimensionless index measuring the IES's response capability to net-load fluctuation for electrical/thermal/cooling energy: average of up+down supply margins normalized by supplied power. Larger = more flexible.
- **Boundary conditions**: Per energy carrier; combined into the flexibility objective F2 with weights ω (Eq. 11).
- **Related concepts**: System flexibility, Flexibility supply margin.

## Bi-level (Stackelberg) dispatch model
- **Notation**: Upper max F1 (Eq. 7) + max F2 (Eq. 11); lower min F^L (Eq. 21) & max F_EV (Eq. 19)
- **Definition**: A leader–follower optimization: the IES operator (leader, upper) sets energy prices and device outputs to maximize revenue and flexibility; user aggregator and EVs (followers, lower) respond via demand response and charge/discharge plans. Coupled by prices (down) and purchased quantities / EV state (up); iterated to a global solution.
- **Boundary conditions**: Two levels with independent objectives, constraints, and decision variables (§3.3).
- **Related concepts**: Multi-entity participation, TOPSIS.

## Green Certificate–Carbon Trading (GCT-CET) mechanism
- **Notation**: F_GCT = λ_GCT(Q_gs − Q_gd); F_CET = λ_CET(E_O − E_C) (Eq. 8, 9, 10)
- **Definition**: A combined market mechanism in the operator's objective. Green-certificate cost is the price times the gap between quota obligation (Q_gs, from load) and certificates earned from renewables (Q_gd). Carbon cost is the carbon price times the gap between actual emissions (E_O) and the initial quota (E_C), each computed from grid purchases and gas-turbine gas use.
- **Boundary conditions**: Coefficients α_GCT, κ_GCT, σ1–σ4 taken from ref [29]; concrete values not specified in this paper.
- **Related concepts**: Low-carbon economic dispatch.

## Improved PSO (IPSO)
- **Notation**: Eq. 26 (inertia weight w), Eq. 27 (learning factors c1, c2), Eqs. 28–31 (four sub-population updates)
- **Definition**: A PSO variant with (i) nonlinearly decreasing inertia weight, (ii) sine-function learning factors that trade global vs local search over iterations, and (iii) the swarm split into four sub-populations each with a distinct position-update rule, to reduce the chance of falling into local optima. Parameters are tuned via the Dung Beetle Optimizer (DBO) per §3.3.
- **Boundary conditions**: Applied to the upper-level model only; lower level solved by CPLEX.
- **Related concepts**: Dung Beetle Optimizer, Pareto front, Local optima.

## TOPSIS (Technique for Order Preference by Similarity to Ideal Solution)
- **Notation**: relative closeness ∈ [0,1]
- **Definition**: Multi-attribute decision method used to pick one compromise dispatch scheme from the Pareto front, by computing each solution's relative closeness to the positive- and negative-ideal solutions (using operator profit and flexibility index as criteria); the highest-closeness solution is selected (§3.3, ref [24]).
- **Boundary conditions**: Applied post-optimization to the Pareto set; also serves as the convergence metric in §4.3.
- **Related concepts**: Pareto front, Bi-level dispatch model.

## Multi-entity participation
- **Notation**: —
- **Definition**: Explicit modeling of three distinct stakeholder classes with their own objectives — IES operator (revenue + flexibility), user aggregator (min cost), EV clusters (max self-utility) — whose interactions are resolved within the bi-level framework.
- **Boundary conditions**: Three modeled entity classes; excludes gas-network operators and others.
- **Related concepts**: Bi-level dispatch model, Demand response.
