# Environment

- **Language/runtime**: Optimization model and algorithm implemented in an unspecified environment (code not provided in the paper). Mathematical formulation is presented in standard algebraic form.
- **Framework**: Not specified in paper. The SOCP relaxation suggests a convex optimization solver (e.g., Gurobi, CPLEX, MOSEK) or a custom metaheuristic implementation.
- **Hardware**: Not specified in paper.
- **Data sources**:
  - Typical summer day data from a selected region of Shanxi Province, China [reference 26]
  - Outdoor solar irradiance and ambient temperature profiles (Figure 3)
  - PV and wind maximum forecasted output curves (Figure 4)
  - Conventional load profile (Figure 4)
  - Time-of-use electricity tariff structure (described qualitatively in Section 6.2)
  - ESS parameters: lifetime 10.5 years [reference 27]; AC rated power upper limit 1.6 kW; AC energy efficiency ratio 3.0
  - No public dataset identifier or repository URL is provided
- **Key dependencies**: Not specified in paper. The model requires a solver capable of handling: (a) mixed-integer or continuous nonlinear optimization for the metaheuristic, (b) SOCP constraints for the power flow relaxation. Candidate tools: MATLAB with YALMIP, Python with Pyomo/Gurobi, or similar.
- **Protocols**: The three-scenario comparative protocol described in Section 6.2 is the primary analysis protocol. Algorithm parameters (population size, max iterations = 500, weight bounds) are stated qualitatively but exact numeric values are not specified.
- **Random seeds**: Not specified in paper. Metaheuristic reproducibility is not addressed.
