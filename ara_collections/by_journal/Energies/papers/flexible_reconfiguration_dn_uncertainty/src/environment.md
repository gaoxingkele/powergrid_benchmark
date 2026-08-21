# Computational Environment

## Hardware
- **CPU**: Intel Core i3, 1.9 GHz
- **RAM**: 4 GB

## Software
- **OS**: Not specified (assumed Windows)
- **Programming Language**: MATLAB R2016b
- **Optimization Framework**: Custom implementation of Coati Optimization Algorithm (COA)
- **Power Flow Solver**: Newton-Raphson (integrated within the COA solution loop)
- **Load Flow Base**: Per-unit system (Sbase = 10 MVA)

## Implementation Details
- **Uncertainty Modeling**: Scenario-based using discretized PDFs implemented in MATLAB
- **Scenario Generation**: Weibull (wind), Beta (solar), and Normal (load) PDFs parameterized with mean and standard deviation from historical data
- **Scenario Count**: 3 load scenarios x 5 wind scenarios x 3 PV scenarios = 45 combined scenarios per time segment
- **Time Segments**: 24 hourly periods
- **Total Scenarios per Run**: 45 x 24 = 1080 scenario evaluations

## Notes
- The paper does not specify the COA population size or maximum iteration count
- No parallel computing or GPU acceleration is mentioned
- Single-run results are reported without statistical analysis across multiple runs
- Solution time and convergence characteristics are not reported
