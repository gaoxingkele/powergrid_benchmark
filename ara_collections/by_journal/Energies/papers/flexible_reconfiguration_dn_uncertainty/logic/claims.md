# Claims

## Claim C01: Dynamic reconfiguration under uncertainty reduces total operational cost compared to static reconfiguration

| Field | Value |
|-------|-------|
| **Statement** | A flexible dynamic reconfiguration model that accounts for load and renewable generation uncertainty via scenario-based probabilistic modeling achieves lower total operational cost (sum of power loss, voltage deviation, switching, upstream purchase, PV, and wind costs) than static reconfiguration approaches, under equivalent network and economic conditions. |
| **Conditions** | (1) Network is equipped with remote-controlled switches; (2) 24-hour time horizon with hourly reconfiguration decisions; (3) Uncertainty described by Weibull (wind), Beta (solar), and Normal (load) PDFs; (4) Scenario-based approach with 3 load, 5 wind, and 3 PV scenarios; (5) Maximum 4 switching operations per RCS per day. |
| **Sources** | Tables 4, 12; Figures 8, 10, 16 |
| **Status** | Supported by evidence |
| **Falsification** | This claim is falsified if the total operational cost of dynamic reconfiguration (Case 4) is not lower than static reconfiguration (Cases 2 and 3) on both the IEEE 33-bus and TPC 83-bus test systems under the same uncertainty characterization and parameter settings. |
| **Proof** | Experiment E01 compares the total cost across four cases. In the IEEE 33-bus system, Case 4 achieves USD 2626.39 vs USD 2635.45 (Case 2) and USD 2649.57 (Case 3), representing savings of 0.34% and 0.88%, respectively. In the TPC 83-bus system, Case 4 achieves USD 18,378.23 vs USD 18,455.35 (Case 2) and USD 18,574.61 (Case 3). |
| **Evidence basis** | Table 4 (Evidence E01) shows cost breakdown for all cases on IEEE 33-bus; Table 12 (Evidence E12) shows similar breakdown for TPC 83-bus. Power loss reductions of 26.31% (vs Case 1), 2.14% (vs Case 2), and 4.66% (vs Case 3) are documented. |

---

## Claim C02: The Coati Optimization Algorithm (COA) outperforms Particle Swarm Optimization (PSO) for dynamic reconfiguration

| Field | Value |
|-------|-------|
| **Statement** | The Coati Optimization Algorithm produces a lower total operational cost solution for the DR problem than Particle Swarm Optimization under identical problem formulation, network configuration, and computational budget, due to its two-phase search (global iguana hunting and local predator escape). |
| **Conditions** | (1) Same objective function and constraints; (2) Same number of iterations and population size; (3) Same IEEE 33-bus test system; (4) Same scenario-based uncertainty modeling; (5) Same MATLAB R2016b implementation environment. |
| **Sources** | Table 8; Figure 13 |
| **Status** | Supported by evidence |
| **Falsification** | This claim is falsified if PSO achieves a total operational cost equal to or lower than COA on the IEEE 33-bus dynamic reconfiguration problem under identical conditions, or if the cost difference is within the stochastic variation margin of the algorithms. |
| **Proof** | Experiment E02 compares COA and PSO. COA achieves a total cost of USD 2626.39 with switching cost of USD 10, while PSO achieves USD 2634.58 with switching cost of USD 18. COA's cost is USD 8.19 (0.31%) lower than PSO. COA also achieves lower Closs (USD 466.73 vs USD 466.85) and Cupn (USD 1857.53 vs USD 1857.63). |
| **Evidence basis** | Table 8 (Evidence E08) provides side-by-side comparison of COA and PSO performance metrics. Minimum bus voltage profiles are comparable (Figure 13, Evidence F13). |

---

## Claim C03: Scenario-based probabilistic modeling captures the operational impact of renewable and load uncertainty on DR decisions

| Field | Value |
|-------|-------|
| **Statement** | A scenario-based approach using Weibull, Beta, and Normal probability density functions to model wind, solar, and load uncertainty, combined through independent scenario multiplication, captures the stochastic nature of distribution network operation and informs optimal hourly reconfiguration decisions. |
| **Conditions** | (1) Probability distributions are parameterized from historical data; (2) Scenarios are discretized into finite intervals; (3) 3 load scenarios, 5 wind scenarios, and 3 PV scenarios per time segment (45 combined scenarios); (4) Scenario probabilities are used to weight cost contributions in the expected-value objective function. |
| **Sources** | Sections 2.1.1-2.1.3; Equations (1)-(19); Figures 4, 5 |
| **Status** | Supported by evidence |
| **Falsification** | This claim is falsified if: (a) the scenario-based optimization yields the same configuration as a deterministic approach using only mean values, indicating no benefit from uncertainty modeling; or (b) the scenario probabilities do not sum appropriately, violating the probability axioms. |
| **Proof** | Experiment E03 evaluates the impact of uncertainty modeling through four-case comparison. Case 3 (static with DG at nominal power) assumes no uncertainty and achieves USD 2649.57, while Case 4 (dynamic with uncertainty) achieves USD 2626.39, showing that accounting for uncertainty enables cost savings. The combined scenario probability model (Equation 19) correctly multiplies independent scenario probabilities. |
| **Evidence basis** | The probabilistic models are mathematically defined in Equations (1)-(18). Figures 4 (Evidence F04) and 5 (Evidence F05) show the wind speed, solar irradiance, and load profiles used for scenario generation. |

---

## Claim C04: Dynamic reconfiguration improves distribution network reliability (reduces EENS) compared to static configurations

| Field | Value |
|-------|-------|
| **Statement** | Dynamic reconfiguration (Case 4) reduces the Expected Energy Not Supplied (EENS) compared to both the initial configuration (Case 1) and static reconfiguration approaches (Cases 2 and 3), because the hourly topology optimization reroutes power to reduce the impact of branch outages. |
| **Conditions** | (1) EENS is calculated using Equations (46)-(47) with branch failure rates and durations from [34]; (2) IEEE 33-bus test system; (3) Same load profile and DG placement across all cases. |
| **Sources** | Table 9; Figure 14 |
| **Status** | Supported by evidence |
| **Falsification** | This claim is falsified if the total or average EENS for Case 4 is not lower than for Cases 1, 2, and 3 on the IEEE 33-bus system under identical failure rate assumptions. |
| **Proof** | Table 9 (Evidence E09) shows EENS values: Average EENS values are Case 1: 0.6192, Case 2: 0.5106, Case 3: 0.6245, Case 4: 0.5037 MWh/year. Total EENS values are Case 1: 14.8602, Case 2: 12.2543, Case 3: 14.9887, Case 4: 12.0879 MWh/year. Case 4 achieves the lowest EENS in both metrics. |
| **Evidence basis** | Table 9 shows average and total EENS for all cases. Figure 14 (Evidence F14) shows hourly EENS variation. The reliability improvement is consistent across all 24 hours. |

---

## Claim C05: Dynamic reconfiguration reduces upstream power purchase by optimizing hourly topology in response to generation and load variation

| Field | Value |
|-------|-------|
| **Statement** | Hourly dynamic reconfiguration reduces the total energy purchased from the upstream network by adapting the distribution network topology to match the time-varying profiles of renewable generation and load demand. |
| **Conditions** | (1) IEEE 33-bus and TPC 83-bus test systems; (2) Same energy price profiles (Figure 6); (3) Four-case comparison framework; (4) 24-hour time horizon. |
| **Sources** | Tables 5, 6; Figures 7, 8, 16 |
| **Status** | Supported by evidence |
| **Falsification** | This claim is falsified if the total upstream power purchase (Cupn) in Case 4 is not lower than Cases 1, 2, and 3 on both test systems. |
| **Proof** | On IEEE 33-bus, Case 4 Cupn = USD 1857.53 vs Case 1: USD 1873.28, Case 2: USD 1858.42, Case 3: USD 1859.75. On TPC 83-bus, Case 4 Cupn = USD 15,825.3 vs Case 1: USD 15,861.9, Case 2: USD 15,835.1, Case 3: USD 15,846.1. Case 4 achieves the lowest purchase cost in both systems. |
| **Evidence basis** | Table 5 (Evidence E05) shows hourly power procurement. Table 6 (Evidence E06) shows hourly procurement costs. Figure 7 (Evidence F07) and Figure 8 (Evidence F08) visualize the reduction. |
