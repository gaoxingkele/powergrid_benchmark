# Reproducibility Information

## Software Environment
- **Python**: 3.11.0
- **IDE**: Spyder 5.4.3
- **Optimization Modeling**: Pyomo 6.5.0
- **Solver**: Gurobi 10
- **OS**: macOS (Apple Studio M1 64 GB)

## Solution Method
- **Deterministic**: Column and Constraint Generation (CCG) decomposition
- **Uncertainty**: DDDRO with duality-free decomposition (bi-level max-min transformed into independent subproblems)
- **Model Type**: Mixed-integer linear programming (MILP) / Mixed-integer second-order cone programming (MISOCP) due to AC linearized constraints with SOC constraint

## Data Sources
- **Historical demand and VRE generation**: ENTSO-E Transparency Platform (Spain, 01/2015 to 12/2023) [70]
- **Test system - Garver 6-node**: Derived from [72]
- **Test system - IEEE RTS-GMLC**: From [73] (https://github.com/GridMod/RTS-GMLC)
- **ESS costs (current)**: [75,76]
- **ESS costs (projected)**: [75] (IRENA projections)
- **Implementation data repository**: https://github.com/Falferreira/Phd_Files.git [71]

## Parameters
- **ESS**: Max charge/discharge: 50 MW; round-trip efficiency: 85%; usable capacity: 75 MWh
- **Planning horizon**: 3 years (IEEE RTS-GMLC)
- **Annual growth rate**: 4.5% (demand and VRE)
- **Demand stages**: 4 per day (S1: 0.05, S2: 0.2, S3: 0.2, S4: 0.55 duration fractions)
- **Data bins (DDDRO)**: 6 clusters via K-means
- **Demand response participation**: 25% (S2.4)
- **Flexibility contracting**: 30% upward and downward (S2.4)

## Hardware
- **Processor**: Apple Studio M1
- **RAM**: 64 GB
- **Processing time**: ~10 min average; ~30 min max (IEEE RTS-GMLC)

## Not Specified
- Solver termination criteria (optimality gap tolerance) not specified
- DDDRO confidence levels α1 and α2 not specified
- Discount rate dr not specified
- Specific values for investment costs IC_TL, IC_D, IC_ND, IC_ST, IC_VL not provided (referenced to GitHub repository [71])
- Operating costs OC_* values not specified (referenced to [71])
