# Constraints / Boundary Conditions

## Boundary Conditions
- The optimization is formulated for a distribution network with PV generation, wind generation, battery ESS, micro-gas turbines, and temperature-controlled building loads.
- The objective is bi-objective: F1 (grid operating costs) and F2 (ESS configuration costs) — both minimized simultaneously via scalarization / metaheuristic Pareto approach.
- The power flow constraints are convexified via SOCR; exactness depends on the radial network topology assumption.
- Scheduling horizon is 24 hours with 1-hour intervals.

## Assumptions
- A1: Temperature-controlled loads follow a first-order ETP model (single-zone lumped capacitance) — no multi-zone thermal coupling.
- A2: ESS lifetime is fixed at 10.5 years with deterministic replacement cycles — calendar-aging and cycle-aging degradation beyond self-discharge are not modeled.
- A3: Renewable energy (PV, wind) forecasts are deterministic — no stochastic or uncertainty modeling.
- A4: Time-of-use electricity tariffs are fixed and known in advance — no real-time pricing.
- A5: Indoor comfort temperature range is static and user-defined — no adaptive comfort or occupancy variation.
- A6: SOCR relaxation gap is assumed to converge sufficiently for the SOCP solution to approximate the true optimal solution.

## Known Limitations
- L1: The case study uses data from a single summer day in one region (Shanxi Province) — seasonal and geographic generalizability is unvalidated.
- L2: No validation on benchmark distribution network test cases (e.g., IEEE 13/33/123-bus systems) — only the specific Shanxi data configuration.
- L3: The hybrid algorithm's hyperparameters (population size, inertia weight bounds, crossover probabilities) are not systematically tuned or ablated — sensitivity analysis is absent.
- L4: The POA-GWO-CSO convergence proof is empirical only (Figure 9) — no theoretical convergence guarantee.
- L5: The SOCR error gap (\(\Delta_{diff,t}\)) is described but the actual achieved gap values for the case study are not reported.
- L6: Scenario 2 and 3 both achieve 100% RE consumption — the model cannot show further improvement in RE integration beyond this ceiling, potentially masking trade-offs under higher RE penetration.
- L7: The building load model considers only air conditioning (cooling) — heating loads and other temperature-controlled appliances (heat pumps, electric water heaters) are excluded.
- L8: No uncertainty or robustness analysis — all inputs (RE generation, load, temperature, tariffs) are deterministic.
- L9: The ESS configuration cost model does not consider degradation-dependent capacity fade or second-life battery applications.
- L10: Computational cost (run time, memory) of the POA-GWO-CSO algorithm is not reported relative to the baselines.
