# Constraints, Assumptions, and Limitations

## Boundary Conditions

### Problem Definition Boundaries
1. **Time horizon**: 24-hour day-ahead operation planning
2. **Network types**: Radial distribution networks (IEEE 33-bus, TPC 83-bus)
3. **Voltage level**: 12.66 kV (IEEE 33-bus), 11.4 kV (TPC 83-bus)
4. **Base values**: Sbase = 10 MVA, Vbase per system
5. **DG types**: Wind turbines (Weibull-based), PV arrays (Beta-based)

### Algorithmic Boundaries
1. **Optimization algorithm**: COA (Coati Optimization Algorithm)
2. **Uncertainty modeling**: Scenario-based with discretized PDFs
3. **Power flow**: Newton-Raphson or similar load flow integrated into solution process
4. **Implementation platform**: MATLAB R2016b

## Formal Constraints

### Power Balance (Equations 29-30)
- Active and reactive power must balance at each bus for every time period and scenario
- Load flow equations must be satisfied exactly

### Voltage Limits (Equation 31)
- Vmin = 0.95 p.u. ≤ Vt,i ≤ Vmax = 1.05 p.u. for all buses at all times

### Line Thermal Limits (Equation 32)
- Apparent power flow on each feeder must not exceed the feeder's maximum rated capacity

### DG Output Limits (Equations 33-34)
- 0 ≤ PDG,t,i ≤ Pmax_DG,t,i and 0 ≤ QDG,t,i ≤ Qmax_DG,t,i

### Radial Topology (Equation 35)
- Nb,t = NBt - Nsub: number of closed branches = number of buses - number of substations
- No closed loops permitted in network topology

### Switching Limits (Equations 36-37)
- Each RCS limited to NSWmax = 4 switching operations in 24-hour period
- NSWRCSj = sum of |SWj,t - SWj,t-1| over t=1..24

## Assumptions

### Modeling Assumptions
1. **PDF parameters known a priori**: Shape and scale parameters for Weibull, Beta, and Normal distributions are known from historical data
2. **Scenario independence**: Load, wind, and PV uncertainties are independent; combined probability is product of individual probabilities
3. **Fixed power factor**: Wind-DG at 0.85 lagging, PV at unity power factor
4. **Constant DG locations**: DG locations and sizes are predetermined (not optimized in this work)
5. **Known energy prices**: Energy price profiles are predetermined and fixed for the scheduling horizon
6. **Deterministic switching cost**: Each switching operation costs USD 1 regardless of which switch is operated

### Operational Assumptions
1. All switches are remote-controlled and can operate at any hour boundary
2. Network reconfiguration occurs at the beginning of each hour
3. Load and generation are constant within each hourly interval
4. The upstream network can supply unlimited power at the specified price
5. No islanding operation considered
6. No network expansion or planning decisions included

## Limitations

1. **Single-objective formulation**: The weighted-sum approach combines multiple objectives (losses, VD, switching, etc.) into a single cost function. Multi-objective Pareto optimization could provide richer trade-off information.

2. **Metaheuristic optimality gap**: COA, as a metaheuristic, does not guarantee global optimality. Solution quality depends on population size, number of iterations, and random initialization.

3. **Scenario count fixed**: The number of scenarios (3 load, 5 wind, 3 PV) is fixed. The sensitivity of results to scenario count is not analyzed.

4. **Limited validation scenarios**: The method is tested on only two systems (33-bus and 83-bus). Scalability to larger systems (1000+ buses) is not demonstrated.

5. **No storage coordination**: Battery energy storage systems are not considered, which could further reduce operational costs when coordinated with DR.

6. **Deterministic switching cost**: Switching costs may vary by switch type, location, and operational context in practice.

7. **Single-run results**: No statistical analysis (multiple runs with different random seeds) is provided to assess the robustness of COA's solutions.

8. **No demand response integration**: Demand response programs that could shift load are not considered alongside DR.

9. **Reactive power optimization limited**: DG reactive power is fixed by power factor, not independently optimized.

10. **Computational requirements not fully characterized**: The paper does not report solution time, convergence characteristics, or scalability to larger systems for the COA.
