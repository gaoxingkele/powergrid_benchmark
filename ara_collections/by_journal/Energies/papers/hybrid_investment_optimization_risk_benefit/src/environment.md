# Environment

## Language/Runtime
- MATLAB (for GA baseline implementation using built-in toolbox)
- ILA solver implementation (programming language not specified; algorithm from Ref. [59])

## Framework
- MATLAB GA toolbox (system default parameters for baseline comparison)
- ILA solver (parameters per Ref. [59])

## Hardware
- Not specified in the paper

## Data Sources
- **Primary data:** 10 projects from a power-grid company's investment project database
- **Qualitative risk indicators:** Expert scoring (1-9 scale) by 5-person expert group
- **Quantitative benefit indicators:** Project feasibility study reports (transmission volume, power supply reliability, load rate, debt service coverage ratio, internal rate of return, CO2 reduction, coal consumption reduction)
- **Investment amounts:** Project-specific AMO values (Table 9)
- **Expert group composition:** 1 government regulator, 1 regulatory department practitioner, 2 power-grid enterprise employees, 1 professor (Table 3)

## Key Dependencies
- **Bayesian BWM:** Implementation of the hierarchical Bayesian model for group weights (Section 3.1.1)
- **TOPSIS:** Euclidean distance computation for alternative ranking (Section 3.1.2)
- **ILA solver:** Three-stage metaheuristic optimization (Section 3.2.3)
- **MATLAB GA toolbox:** Baseline comparison optimization algorithm

## Protocols
- **Expert elicitation protocol:** Experts first agree on best/worst indicators, then provide BO and OW vectors using 1-9 scale
- **Qualitative indicator scoring:** Risk indicator performance scored 1-9 by expert judgment
- **Quantitative indicator measurement:** Benefit indicators use actual project data values (Table 4)
- **Optimization constraints:** Investment amount cap (AMO0 = 1500), power demand floor (D = 600), CO2 reduction floor (CER0 = 5000)
- **Sensitivity analysis:** Three constraint dimensions varied independently while holding others at default

## Random Seeds
- Not specified
- ILA uses random numbers with specified ranges: 1, 2 in [-1.5, 1.5]; 3, 6, 9 in [0,1]; 4, 5 in [-0.75, 0.75]; 7, 8 in [-0.25, 0.25]
- GA uses MATLAB toolbox defaults (seed not specified)
