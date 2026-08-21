# Solution Constraints

## Boundary Conditions

1. **Grid-based network partition is a prerequisite.** The method assumes the distribution network is pre-partitioned into functional grid blocks following utility planning standards (DL/T 5729-2023). The paper does not propose or evaluate a partitioning algorithm.

2. **Planning horizon and investment budget are externally given.** The budget (B_AEV) and planning horizon are specified by the utility or system owner. The number of DESS units is implicitly determined by the budget constraint, not optimized.

3. **Node–block–grid evaluation uses planning-stage data.** All indicators are calculated from typical daily load curves (96-point, 15-minute resolution) and annual statistical records, not from high-resolution full-year time-series simulations.

## Assumptions

1. **Stationary renewable generation patterns.** The GMM is fitted to historical data, and the extracted scenarios are assumed representative of future operating conditions. No temporal non-stationarity or climate-change-induced shifts are considered.

2. **Uniform DG power output characteristics.** All DG units of the same type (PV, wind) within the grid share the same normalized output profile, differing only in installed capacity.

3. **Fixed demand response participation.** Reducible load is set at 10–20% of nodal load, and critical sectors (administrative, medical, educational) are excluded from DR programs. These parameters are not varied or optimized.

4. **Single composite objective via weighted-sum.** The multi-objective optimization problem is solved by normalized weighted-sum aggregation, which yields a single solution per iteration. No Pareto front exploration or multi-solution analysis is performed.

5. **Sequential planning does not revisit previous decisions.** Once a DESS is sited and sized at a node, its configuration is fixed and not revised in subsequent iterations.

6. **Network topology is static.** The distribution network topology is assumed unchanged throughout the planning process. No network reconfiguration, expansion, or dynamic topology scenarios are considered.

## Known Limitations

1. **Scalability to very large networks.** The sequential iteration process requires re-solving the optimization model per DESS unit. For networks requiring many DESS units (e.g., >20), the computational burden may become significant.

2. **No explicit extreme event modeling.** The resilience assessment focuses on day-to-day operational resilience under uncertainty, not on resilience to extreme weather events (e.g., hurricanes, floods) or N−k contingency scenarios.

3. **Single test system.** The method is validated on one real distribution grid in Zhejiang Province. Generalizability to other grid configurations, voltage levels, or regulatory environments is not demonstrated.

4. **No comparison with deep generative methods for scenario generation.** The GMM approach is compared against simpler statistical baselines but not against deep learning-based scenario generation methods (e.g., GANs, VAEs).

5. **Weighted-sum optimization limitations.** The weighted-sum method may miss solutions in non-convex regions of the Pareto front, potentially overlooking configurations that better balance competing objectives.

6. **No operational validation.** The planning results are evaluated using planning-stage metrics (O1–G2) but not validated through detailed operational simulation or real-time control emulation.

7. **Simplified time-of-use pricing model.** The electricity pricing structure is static (fixed peak/flat/off-peak rates). Dynamic pricing or real-time market prices are not considered.

8. **Data availability requirement.** The method requires node-level quality indicators (I1–I7), which may not be available in all distribution networks. The paper notes that feeder- or area-level indicators are allocated proportionally when node-level data are unavailable, which introduces approximation error.
