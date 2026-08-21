# Problem Specification

## Observations

### O1: Renewable energy variability challenges grid operation
- **Statement**: The continuous incorporation of wind and photovoltaic systems increases the share of variable and unpredictable RE in the power system, creating challenges for power supply stability and grid scheduling.
- **Evidence**: Section 1 (Introduction); references [1,2]
- **Implication**: Energy storage is needed as a buffering and regulatory mechanism to stabilize RE output and ensure orderly grid scheduling.

### O2: Energy storage systems have high life-cycle costs
- **Statement**: ESS construction requires expensive core components, complex installation and commissioning, and high ongoing maintenance costs, leading to prolonged investment return cycles.
- **Evidence**: Section 1 (Introduction)
- **Implication**: Optimal ESS configuration is critical to improve economic feasibility and investor confidence.

### O3: Air conditioning accounts for >50% of building energy use
- **Statement**: Air conditioning energy consumption accounts for more than 50% of total building energy use, providing substantial flexibility potential for demand-side management.
- **Evidence**: Section 1 (Introduction), citing reference [10]
- **Implication**: Temperature-controlled loads offer significant untapped flexibility that could reduce ESS configuration costs.

### O4: Existing approaches neglect demand-side load flexibility
- **Statement**: Prior research on optimal energy storage configuration has overlooked the substantial flexibility potential of the load side in microgrid systems, focusing predominantly on the supply side.
- **Evidence**: Section 1 (Introduction), review of references [6,7,8,9]
- **Implication**: Full exploitation of load-side flexibility could significantly lower ESS configuration costs and improve overall system economics.

### O5: Existing multi-objective algorithms face convergence and parameter sensitivity issues
- **Statement**: Multi-objective PSO tends to converge to local optima and is highly dependent on parameter selection; improved genetic simulated annealing is computationally complex for large-scale grids and depends on empirical parameter debugging.
- **Evidence**: Section 1 (Introduction), discussion of references [14,15]
- **Implication**: A more efficient algorithm with better global search capability and faster convergence is needed.

## Gaps

### G1: Temperature-controlled load model not systematically incorporated into ESS optimization
- **Statement**: Existing studies have not systematically incorporated temperature-controlled load models into system modeling and optimization processes, thereby neglecting the substantial potential for flexible regulation from building thermal dynamics.
- **Caused by**: O4
- **Existing attempts**: References [11,12,13] applied temperature-controlled load flexibility to hybrid microgrids and cogeneration systems but did not jointly optimize with ESS configuration.
- **Why they fail**: They address load flexibility in isolation without integrating it with ESS sizing/siting decisions under a unified multi-objective framework.

### G2: Existing optimization algorithms lack both computational efficiency and global search capability
- **Statement**: Current algorithms for multi-objective ESS configuration suffer from either premature convergence to local optima (PSO variants) or excessive computational complexity (genetic simulated annealing), with no single algorithm providing fast convergence, good parameter adaptability, and high engineering practicality simultaneously.
- **Caused by**: O5
- **Existing attempts**: The improved pelican optimization algorithm [16] showed strong global search but suffered from relatively long convergence time and low computational efficiency.
- **Why they fail**: They balance exploration and exploitation sub-optimally — the POA lacks a leader-guided search mechanism and sufficient crossover diversity to escape local optima efficiently.

### G3: Coordinated minimization of microgrid and ESS operation costs not achieved
- **Statement**: The role of ESS in reducing grid operation costs and the exploitation of temperature-controlled load flexibility have not been sufficiently addressed in a coordinated manner, resulting in failure to achieve simultaneous minimization of both cost objectives.
- **Caused by**: O2, O4
- **Existing attempts**: Individual cost minimization has been attempted (e.g., reference [9] on life-cycle costs), but multi-objective coordination between grid operating costs and ESS configuration costs is absent.
- **Why they fail**: Single-objective approaches optimize one cost at the expense of the other, and prior multi-objective formulations omit the load-side flexibility that changes the Pareto frontier.

## Key Insight
- **Insight**: By incorporating temperature-controlled load flexibility (building thermal inertia and user comfort range) into a multi-objective ESS configuration optimization, the system can pre-cool buildings during off-peak hours to shift air conditioning load away from peak tariff periods, simultaneously reducing grid operating costs through demand-side flexibility and improving ESS revenue through more efficient charging/discharge scheduling. A hybrid metaheuristic combining POA (exploration), GWO leader strategy (guided convergence), and CSO crossover operators (dimension-level diversity) can solve the resulting non-convex multi-objective problem more efficiently than any single algorithm.
- **Derived from**: O1, O2, O3, O4, O5; G1, G2, G3
- **Enables**: A unified optimization framework that (a) models building thermal dynamics alongside ESS constraints, (b) solves the bi-objective problem (grid operating costs + ESS configuration costs) with a tailored hybrid algorithm, and (c) demonstrates quantitative improvements through three-scenario comparative case analysis.

## Assumptions
- A1: The temperature-controlled load model uses a first-order equivalent thermal parameter (ETP) representation of building thermal dynamics (single-zone lumped capacitance) — simplifies multi-zone thermal behavior.
- A2: The ESS uses battery energy storage technology (most mature and widely deployed).
- A3: ESS lifetime is fixed at 10.5 years per reference [27]; no calendar-aging degradation model beyond the self-discharge rate.
- A4: Renewable energy (PV and wind) forecasts are treated as deterministic maximum forecasted outputs — no stochastic/uncertainty modeling in the current formulation.
- A5: Time-of-use electricity tariffs are fixed and known a priori — no real-time pricing or demand response interaction beyond pre-cooling.
- A6: Indoor comfort temperature range is user-defined and static — no adaptive comfort model or occupancy variation.
- A7: The second-order cone relaxation (SOCR) gap is assumed to converge to an acceptable accuracy for the optimal solution to be equivalent to the actual optimal solution.
