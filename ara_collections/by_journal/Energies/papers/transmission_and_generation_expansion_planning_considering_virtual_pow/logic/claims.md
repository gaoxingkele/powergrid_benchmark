# Claims

## C01: Virtual Power Lines Defer or Replace Transmission Line Investments
- **Statement**: Battery energy storage deployed as virtual power lines can substitute for or postpone investments in new physical transmission line circuits by shifting energy flow from high-demand to low-demand periods (peak shaving equivalent).
- **Conditions**: ESS round-trip efficiency of 85%; max charge/discharge rate 50 MW; usable energy capacity 75 MWh; four net demand stages per day.
- **Status**: Supported by case study results.
- **Falsification**: If, in scenarios where VPL is available, the optimal expansion plan installs the same number of new transmission line circuits as the base case without VPL, then the claim is falsified.
- **Proof**: E01 (Scenario S1.1 vs S1.2), E03 (Scenario S2.1 vs S2.2).

## C02: ESS Cost Reduction Increases VPL Adoption and Transmission Deferral
- **Statement**: As ESS investment and operating costs decline, virtual power lines become economically preferable over a larger number of new transmission line circuits, further reducing total expansion cost.
- **Conditions**: Projected ESS cost reduction based on IRENA data [75]; ESS round-trip efficiency 85%; max charge/discharge 50 MW; usable capacity 75 MWh.
- **Status**: Supported by sensitivity analysis results.
- **Falsification**: If the number of transmission line circuits replaced by VPL does not increase when ESS costs are reduced (comparing current-cost vs. projected-cost scenarios), the claim is falsified.
- **Proof**: E02 (Scenario S1.2 vs S1.3), E04 (Scenario S2.2 vs S2.3).

## C03: TSO-DSO Flexibility Services Reduce Total Expansion Cost
- **Statement**: Contracting upward and downward flexibility from the TSO-DSO interconnection reduces total system expansion costs by enabling demand response and distributed generation to substitute for generation and transmission investments.
- **Conditions**: 25% of demand participates in demand response; upward and downward flexibility contracted at 30%; three-year expansion plan with 4.5% annual growth.
- **Status**: Supported by scenario S2.4 results.
- **Falsification**: If the total cost of scenario S2.4 (with flexibility and VRE) is greater than or equal to scenario S2.2 (with VPL only), the claim is falsified.
- **Proof**: E05 (Scenario S2.2 vs S2.4).

## C04: DDDRO with Dual Norm Ambiguity Set Provides Tractable Uncertainty Handling
- **Statement**: The data-driven distributionally robust optimization approach using L1 and L∞ norm-based confidence uncertainty sets converges to the true probability distribution as historical data increases, producing less conservative solutions than traditional robust optimization while maintaining computational tractability via duality-free decomposition.
- **Conditions**: Historical data from ENTSO-E Spain 2015-2023; six data bins; confidence levels α1 and α2; N historical data points; MD bins.
- **Status**: Theoretically supported based on [10,60,61,68].
- **Falsification**: If increasing historical data does not shrink the ambiguity set or if the duality-free decomposition fails to produce feasible solutions for known test systems, the claim is falsified.
- **Proof**: E06, E07.

## C05: Integrated TGEP Model with VPL, VPP, and Flexibility Reduces Total Cost
- **Statement**: Integrating virtual power lines, virtual power plants, TSO-DSO flexibility, and VRE into a unified TGEP model achieves lower total expansion and operational costs by enabling substitution between transmission, generation, and flexibility investments.
- **Conditions**: IEEE RTS-GMLC test system; three-year planning horizon; 4.5% annual growth; all flexibility mechanisms available.
- **Status**: Supported.
- **Falsification**: If the total cost of the full model (with VPL+VRE+DR+flexibility) is not lower than the base case (conventional planning), the claim is falsified.
- **Proof**: E03 (conventional vs VPL-only), E05 (VPL-only vs full model).

## C06: VPL and Flexibility Improve Transmission System Utilization
- **Statement**: The deployment of virtual power lines and flexibility services increases average line occupancy and reduces losses, indicating more rational and efficient use of the transmission system by shifting energy flow from high-demand to low-demand periods.
- **Conditions**: IEEE RTS-GMLC test system; average line usage metric; line losses metric.
- **Status**: Supported.
- **Falsification**: If average line usage does not increase and line losses do not decrease when VPL and flexibility are deployed, the claim is falsified.
- **Proof**: E08 (Table 10: S2.1 through S2.4 line usage and loss metrics).

## C07: VPL and Flexibility Improve Locational Marginal Pricing Indicators
- **Statement**: The implementation of VPLs and flexibility services reduces average LMP by alleviating transmission congestion.
- **Conditions**: IEEE RTS-GMLC test system; LMP average across transmission nodes.
- **Status**: Supported.
- **Falsification**: If the average LMP does not decrease when VPL and flexibility are added, the claim is falsified.
- **Proof**: E08 (Table 10: LMP Average values across scenarios S2.1 through S2.4).

## C08: Column and Constraint Generation (CCG) Enables Scalable Solution for Medium-to-Large Systems
- **Statement**: The CCG decomposition method, combined with duality-free decomposition, makes the proposed TGEP model computationally tractable for medium-to-large-scale power systems by solving the two-stage robust optimization problem in manageable processing time.
- **Conditions**: IEEE RTS-GMLC; Apple Studio M1 64 GB; Python 3.11.0, Pyomo 6.5.0, Gurobi 10.
- **Status**: Supported.
- **Falsification**: If the model fails to converge within reasonable time (e.g., > 2 hours) for the IEEE RTS-GMLC cases, the scalability claim is falsified.
- **Proof**: E09.
