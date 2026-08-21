# Claims

## C01: DE achieves lowest operating cost in drought scenario
- **Statement**: The Differential Evolution (DE) algorithm achieved the lowest operating cost (USD 4.2897e5) under Scenario 1 (limited hydroelectric availability), outperforming PSO (USD 4.3536e5), GWO (USD 4.327e5), and CA (USD 4.3774e5).
- **Proof**: Table 11 reports best cost for each algorithm; DE shows minimum value.
- **Experiment**: E01

## C02: DE achieves lowest operating cost in high-water scenario
- **Statement**: Under Scenario 2 (high water availability), DE again achieved the lowest best cost (USD 5.6531e5) vs. PSO (USD 5.7356e5), GWO (USD 5.7139e5), and CA (USD 5.6868e5).
- **Proof**: Table 13 reports best cost for each algorithm; DE shows minimum value.
- **Experiment**: E02

## C03: DE shows highest robustness with low cost variance
- **Statement**: DE maintained cost variation below 3% across 100 Monte Carlo iterations, with less than 0.5% variation between the two repetitions in both scenarios.
- **Proof**: Section 6.3 states "negligible variation between repetitions (less than 0.5%)" for DE; Table 11 and Table 13 show small gap between best and worst costs for DE.
- **Experiment**: E01, E02

## C04: DE achieves 12.5% cost reduction over PSO in drought scenario
- **Statement**: In the drought scenario (Scenario 1), DE achieved a 12.5% cost reduction compared to PSO.
- **Proof**: Reported in the abstract and introduction (from the full text).
- **Experiment**: E01

## C05: PSO is fastest but least competitive in cost
- **Statement**: PSO had the shortest average execution time (9.40 s in Scenario 1, 12.29 s in Scenario 2) but delivered the least competitive cost among all algorithms.
- **Proof**: Table 11 and Table 13 show PSO lowest avg time but highest cost.
- **Experiment**: E01, E02

## C06: CA has highest computational cost
- **Statement**: Cultural Algorithm (CA) had the highest average runtime: 150.15 s in Scenario 1 and 156.05 s in Scenario 2.
- **Proof**: Table 11 and Table 13 show CA avg time values.
- **Experiment**: E01, E02

## C07: GWO offers balanced performance
- **Statement**: Grey Wolf Optimizer (GWO) offered a balanced compromise between cost and runtime in both scenarios.
- **Proof**: Table 11 and Table 13 show GWO costs and times between DE/PSO extremes; reinforced in Section 6.2 text.
- **Experiment**: E01, E02

## C08: Model is robust to +/-10% demand variation
- **Statement**: Sensitivity analysis with +/-10% demand variation showed DE maintained best performance with cost variations within +/-4%, confirming model robustness.
- **Proof**: Section 6.4 describes sensitivity analysis results.
- **Experiment**: E03

## C09: Weibull and GMM distributions adequately model stochastic resources
- **Statement**: Weibull distribution (for wind speed and solar radiation) and Gaussian Mixture Model (for temperature) were selected as the best-fitting PDFs based on Kolmogorov-Smirnov tests and visual histogram comparison.
- **Proof**: Section 2.3 describes PDF selection; Figure 1 shows fitted histograms.
- **Experiment**: E04

## C10: Renewable integration reduces operational costs
- **Statement**: Incorporating renewable energy sources into the generation mix enhances economic dispatch effectiveness, lowers costs, and reduces fossil fuel dependence.
- **Proof**: Sections 7 and 8 discuss the positive impact of renewable integration on costs and emissions.
- **Experiment**: E01, E02
