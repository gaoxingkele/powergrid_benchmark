# Computational Environment

## Language / Runtime

- **Solver**: Not explicitly stated but based on the use of C&CG algorithm with MILP subproblems, likely Gurobi, CPLEX, or MOSEK.
- **Modeling framework**: Not explicitly stated. Likely YALMIP (MATLAB), JuMP (Julia), or Pyomo (Python) given the academic convention for power system optimization.

## Framework

- **Optimization type**: Mixed-integer linear programming (MILP) for the C&CG master problem and subproblems, with linearized constraints (big-M formulation, auxiliary binary variables for absolute value linearization).
- **Solution algorithm**: Customized Column-and-Constraint Generation (C&CG) with:
  - Fault-state pruning (pre-processing step to reduce scenario count).
  - Endogenous cutting planes for DDU constraint tightening.
  - Convergence tolerance epsilon (not explicitly stated in the paper).
- **Sensitivity analysis**: Sobol' method with Monte Carlo sampling (or Saltelli sampling).

## Hardware

- **Not explicitly stated**. Simulation times reported:
  - IEEE 33-bus (no reduction): 2711 seconds (~45 minutes).
  - IEEE 33-bus (reduce 3 states): 726 seconds (~12 minutes).
  - IEEE 123-bus Case 5: 10.1 hours.
  - These suggest a standard workstation or server but specific CPU/RAM are not reported.

## Data Sources

- **Test systems**: IEEE 33-bus and IEEE 123-bus radial distribution networks (standard benchmark systems).
  - EV charging stations at buses 14, 30 (33-bus).
  - DGs at buses 14, 21, 24 (33-bus).
  - Five tie lines: 8-21, 9-15, 12-22, 18-33, 25-29 (33-bus).
  - MEG station at node 11 (33-bus).
  - 50 EVs in 5 groups, each 2 kW discharge, 10 kWh capacity (33-bus).
- **Wind-speed data**: Three representative typhoon wind-speed scenarios generated from historical typhoon path and wind-speed data. Probabilistic distributions via Monte Carlo simulation. Not explicitly identified (likely Chinese typhoon records).
- **Cost parameters**: Hardening costs in CNY:
  - Level 1: CNY 200,000
  - Level 2: CNY 300,000
  - Level 3: CNY 500,000
- **Total hardening budget**: CNY 1.2 million (base case).
- **Load and generation data**: Standard IEEE 33-bus and 123-bus load profiles.

## Key Dependencies

- **Type of model**: Tri-level distributionally robust optimization (min-max-min).
- **Key equations**:
  - Equation (5): Exponential failure probability model.
  - Equation (7): DDU-based availability coefficient.
  - Equation (8): Tri-level objective function.
  - Equations (49)-(55): Sobol' sensitivity indices.
- **Linearization techniques**:
  - Big-M constraints for power flow bounds (Equations 36-37, 40).
  - Auxiliary binary variables for absolute value linearization (Equation 2).
  - Pseudo power flow for radiality constraints (Equations 16-18).

## Protocols

- **Disaster modeling**: Typhoon wind field with attenuation algorithm -> time-series wind speed -> line failure probability via Equation (5) -> Bernoulli sampling for failure state (Equation 6).
- **Scenario generation**: Random wind-speed sampling -> wind field attenuation -> failure probability calculation -> Monte Carlo fault-state sampling -> fault-state pruning.
- **Sobol' sensitivity**: Define input variables -> generate samples (Monte Carlo/Latin Hypercube) -> evaluate model -> compute Sobol' indices.

## Random Seeds

- **Not explicitly stated**. The Monte Carlo sampling for wind speed scenarios and fault state generation (uniform [0,1] sampling for line failure determination) implies random seeds were used, but specific seed values are not reported in the paper. This affects reproducibility of the exact fault state sets.

## Version Information

- **Not available**: Software versions (solver version, modeling platform version, operating system) are not reported in the paper. This is a limitation for exact reproducibility.
