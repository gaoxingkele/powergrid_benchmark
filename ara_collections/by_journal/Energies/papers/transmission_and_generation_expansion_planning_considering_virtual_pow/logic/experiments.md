# Experiments

## E01: Garver 6-Node — VPL Impact (Scenarios S1.1 vs S1.2)
- **Objective**: Evaluate the capability of VPL to replace or defer transmission line investments in a small test system.
- **Method**: Compare expansion plans with no VPL (S1.1) vs with VPL at current ESS costs (S1.2).
- **Configuration**: Garver 6-node network; 15 right-of-ways; 760 MW load; 1140 MW generation; candidate ESS: 50 MW, 85% efficiency, 75 MWh; current ESS costs [75,76].
- **Direction**: When VPL is available, some new transmission line circuits are replaced by VPL infrastructure, resulting in a lower total cost compared to the base case without VPL.
- **Verifies**: C01
- **Metrics**: Number of new line circuits; number of VPL; total cost [M$].

## E02: Garver 6-Node — ESS Cost Sensitivity (Scenarios S1.2 vs S1.3)
- **Objective**: Quantify the impact of ESS cost reduction on VPL adoption rate.
- **Method**: Compare VPL deployment at current ESS costs (S1.2) vs projected lower ESS costs (S1.3).
- **Configuration**: Garver 6-node network; same candidate ESS specs; projected cost reduction from [75].
- **Direction**: With projected lower ESS costs, more transmission line circuits are replaced by VPL, further reducing total cost compared to current ESS costs.
- **Verifies**: C02
- **Metrics**: Number of line circuits replaced by VPL; total cost [M$]; cost reduction delta.

## E03: IEEE RTS-GMLC — VPL Impact (Scenarios S2.1 vs S2.2)
- **Objective**: Validate VPL effectiveness in a medium/large test system.
- **Method**: Compare expansion plans with no VPL (S2.1) vs with VPL at current ESS costs (S2.2).
- **Configuration**: IEEE RTS-GMLC; 104 right-of-ways; three-year planning horizon; candidate ESS: 50 MW, 85% efficiency, 75 MWh.
- **Direction**: VPL replaces some transmission line circuits, yielding a measurable reduction in total expansion cost compared to the base case.
- **Verifies**: C01, C05
- **Metrics**: Number of new line circuits; number of VPL; total cost [M$].

## E04: IEEE RTS-GMLC — ESS Cost Sensitivity (Scenarios S2.2 vs S2.3)
- **Objective**: Analyze ESS cost reduction impact on VPL deployment in a larger system.
- **Method**: Compare VPL adoption at current costs (S2.2) vs projected costs (S2.3).
- **Configuration**: IEEE RTS-GMLC; same candidate ESS specs; projected cost reduction.
- **Direction**: Lower ESS costs increase VPL adoption, replacing an additional transmission line circuit and further reducing total cost.
- **Verifies**: C02
- **Metrics**: Number of VPL; total cost [M$].

## E05: IEEE RTS-GMLC — Full Model with Flexibility (Scenarios S2.2 vs S2.4)
- **Objective**: Evaluate the combined impact of VRE generation investment, demand response, and TSO-DSO flexibility on total expansion cost.
- **Method**: Compare S2.2 (VPL only) with S2.4 (VPL + VRE + demand response + flexibility).
- **Configuration**: IEEE RTS-GMLC; three-year horizon; 4.5% annual growth; 25% demand response participation; 30% upward/downward flexibility.
- **Direction**: Adding VRE, demand response, and TSO-DSO flexibility further reduces total cost relative to VPL-only scenarios.
- **Verifies**: C03, C05
- **Metrics**: Total cost [M$]; dispatchable generation [GW]; non-dispatchable generation [GW]; demand response [GW]; flexibility [GW].

## E06: DDDRO Ambiguity Set Construction
- **Objective**: Validate the DDDRO ambiguity set formulation using dual norms (L1 and L∞).
- **Method**: Partition historical data into MD bins; compute E-PDF; construct confidence uncertainty set with tolerance coefficients δ1 and δ∞ derived from confidence levels α1, α2.
- **Configuration**: Historical data: ENTSO-E Spain 2015-2023; MD=6 bins; confidence levels α1, α2.
- **Direction**: The ambiguity set shrinks as historical data increases; the E-PDF converges to the T-PDF as N → ∞.
- **Verifies**: C04
- **Metrics**: Tolerance coefficients δ1, δ∞; convergence as N → ∞.

## E07: Duality-Free Decomposition for DDDRO
- **Objective**: Test the computational efficiency of duality-free decomposition for the max-min subproblem.
- **Method**: Decompose M08 into independent subproblems; exploit disjoint feasible regions.
- **Configuration**: Both Garver 6-node and IEEE RTS-GMLC test systems.
- **Direction**: The duality-free approach solves the bi-level problem without computing dual information, preserving tractability as scenario count grows.
- **Verifies**: C04
- **Metrics**: Computational time; convergence iterations; solution quality vs. exact duality.

## E08: Transmission System Utilization and LMP Indicators
- **Objective**: Quantify the impact of VPL and flexibility on line usage, losses, and LMP.
- **Method**: Compare average line usage [p.u.], line losses [p.u.·h], and average LMP [$] across scenarios S2.1 through S2.4.
- **Configuration**: IEEE RTS-GMLC system; all four scenarios.
- **Direction**: Average line usage increases, line losses decrease, and average LMP decreases progressively from S2.1 to S2.4 as VPL and flexibility are added.
- **Verifies**: C06, C07
- **Metrics**: Average line usage [p.u.]; line losses [p.u.·h]; LMP average [$].

## E09: Computational Scalability
- **Objective**: Assess the computational tractability of the proposed model for medium-to-large systems.
- **Method**: Measure processing time for IEEE RTS-GMLC scenarios.
- **Configuration**: Apple Studio M1 64 GB; Python 3.11.0; Spyder 5.4.3; Pyomo 6.5.0; Gurobi 10.
- **Direction**: Processing times are within reasonable bounds for planning applications, scaling adequately with problem size.
- **Verifies**: C08
- **Metrics**: Processing time [minutes]; number of integer/binary variables.
