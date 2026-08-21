# Problem Definition: Integrated Multi-Criteria Planning for Resilient VRE-Based Microgrid

## Observations

1. **VRE uncertainty challenge**: Weather-driven uncertainties and the inherent variability of wind and solar generation make reliable microgrid operation increasingly difficult as reliance on VRE grows.

2. **BESS cost barrier**: While battery energy storage systems (BESS) can buffer VRE variability, their cost remains prohibitive for large-scale deployment, making it impractical to rely solely on BESS as a cost-effective solution.

3. **Demand-side flexibility underutilized**: Traditional planning approaches focus on supply-side solutions (oversizing generation/storage) without fully exploiting demand-side flexibility through advanced DRP mechanisms.

4. **Forecasting-integration gap**: Existing literature shows that comprehensive integrated planning combining forecasting, DRP, and joint sizing/operation under uncertainty remains insufficiently explored.

5. **Static pricing limitations**: Conventional time-of-use (TOU) pricing lacks sensitivity to real-time VRE and demand variations, limiting its effectiveness in mitigating power imbalances.

6. **Deterministic vs. stochastic trade-off**: Deterministic planning yields lower costs but fails to account for real-world uncertainty, while purely stochastic approaches lead to oversizing and excessive costs.

## Gaps

1. **Lack of integrated frameworks**: No existing study jointly optimizes capacity sizing and operational planning under uncertainty while incorporating advanced DRP, LSTM forecasting, and multi-objective optimization in a single framework.

2. **SSAP DRP not explored**: Shortage/surplus-based adaptive pricing (SSAP) as a dynamic DRP mechanism for VRE-based microgrids has not been thoroughly investigated or compared with traditional TOU-based approaches.

3. **Synergy of forecasting + adaptive pricing unstudied**: The combined effect of accurate LSTM forecasting with adaptive pricing DRP on microgrid resilience and cost-effectiveness has not been quantified in prior work.

4. **Multi-objective trade-off characterization**: The three-way trade-off between lifecycle cost (TLCC), reliability (DPSP), and VRE curtailment (LPPP) under uncertainty lacks systematic characterization.

5. **Real-world case study with 100% VRE target**: Limited studies validate integrated planning approaches using real isolated microgrid data targeting 100% VRE transition.

## Key Insight

The key insight is that by synergistically combining three elements — (1) accurate LSTM-based forecasting of VRE and load, (2) dynamic SSAP-based adaptive pricing that responds to real-time supply-demand imbalances, and (3) multi-objective optimization (MOPSO-TOPSIS) for joint capacity sizing and operational planning under Monte Carlo-simulated uncertainty — a microgrid can achieve superior cost-effectiveness (lower TLCC), higher reliability (lower DPSP), and reduced VRE curtailment (lower LPPP) compared to any subset of these strategies applied in isolation.

The SSAP VP-CPP DRP mechanism is the key innovation: it adjusts electricity prices dynamically based on the magnitude and direction of power imbalance, activating flexible demand resources proportionally, rather than relying on static TOU price bands.

## Assumptions

1. The community microgrid is isolated (not grid-connected) and targets 100% VRE-based generation.
2. Load demand, solar irradiance, and wind speed follow probability distributions suitable for Monte Carlo sampling.
3. Flexible demand resources (FDRs) constitute up to +/-10% of total system load at any time.
4. Consumers respond to price signals according to predefined price elasticity coefficients.
5. The BESS has a round-trip efficiency of 90% with SOC limits of 10%-90%.
6. LSTM one-hour-ahead forecasts provide sufficient lead time for DRP activation.
7. The project lifetime is 20 years with a 4% discount rate.
8. The Kenyan electricity tariff structure (reference price 15.80 US cents/kWh) is representative.
9. Critical events occur when SOC <= critical threshold AND total VRE generation <= 0.
10. The 50 MCS scenarios sufficiently capture the uncertainty space.
