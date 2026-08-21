# Experiments

## E01: Weekly Energy Storage Configuration (Scheme 1)
- **Purpose**: Determine the baseline trade-off between investment cost and power fluctuation for a typical high-wind week, without spot market considerations.
- **Configuration**: Scheme 1 — only investment cost vs. output volatility.
- **Data**: 40 MW wind farm (16 x 2.5 MW turbines) in Wan'an County; output power data for 9-15 December 2023 (typical week with >80% wind power output proportion).
- **Method**: NSGA-II optimization with parameters: population=20, offspring=60, generations=300, crossover/mutation probability=0.5. Rated power range 0-12 MW, rated capacity range 0-48 MWh.
- **Results**: Baseline volatility without ESS: sigma_0 = 27.23%. Pareto frontier shows cost increasing from CNY 67.04M to CNY 520.45M, with volatility decreasing from 22.48% to 18.63%. Optimal point identified by inflection point method: 4 MW / 28 MWh, cost CNY 349.31M, volatility 18.92%.
- **Evidence links**: Figures 3, 4, 5; Tables 5, 7.

## E02: Battery Life Analysis and Correction
- **Purpose**: Model the relationship between ESS rated power/capacity and battery service life, and correct the Pareto frontier accordingly.
- **Data**: Cycle counts and expected service life for 11 Pareto front configurations (Table 3), ranging from (4,4) with 35 cycles/4.1 years to (10,40) with 12 cycles/12 years.
- **Method**: Multiple linear regression fitting battery life Y against rated power P_es and rated capacity S_es.
- **Results**: Regression model: Y = 3.73292 - 0.05076*P_es + 0.22835*S_es, R^2 = 0.96965. Rated capacity has strong positive correlation with battery life; rated power has weak negative correlation. Life correction shifts Pareto frontier, particularly for low-capacity configurations where actual cost exceeds NSGA-II simulation.
- **Evidence links**: Figure 6; Equation 14.

## E03: Annual Energy Storage Configuration Optimization
- **Purpose**: Extend the weekly analysis to full-year data to capture seasonal wind variation effects on optimal ESS configuration.
- **Configuration**: Scheme 1 applied to full 2023 dataset.
- **Method**: Life correction method from E02 applied to annual data; NSGA-II optimization on full year.
- **Results**: Annual Pareto frontier (Figure 11) provides basis for final optimal configuration selection. Optimal point: 4 MW / 28 MWh (consistent with weekly analysis for Scheme 1).
- **Evidence links**: Figure 11.

## E04: MOPSO Benchmark Comparison
- **Purpose**: Validate NSGA-II performance by comparing against MOPSO on the same optimization problem.
- **Configuration**: MOPSO parameters in Table 4 (population size=50, archive size=100, NGEN=300, W=0.4, C1=1.5, C2=1.5).
- **Results**: NSGA-II produces lower xi values than MOPSO, indicating more cost-effective volatility reduction. NSGA-II selected optimal point achieves 14.84% volatility decline vs. MOPSO's 7.48% at their respective inflection points.
- **Evidence links**: Figures 11, 12; Tables 5, 6, 7.

## E05: Spot Market Participation (Scheme 2)
- **Purpose**: Evaluate how electricity spot market revenue affects optimal ESS configuration by subtracting annual electricity sales revenue from investment cost.
- **Data**: 2024 Guangdong Province spot electricity prices.
- **Method**: NSGA-II optimization with net cost (investment minus revenue) as first objective; volatility as second objective.
- **Results**: When ESS configuration is below 8 MW/14 MWh, annual revenue can cover full lifecycle investment cost (negative cost). Optimal configuration by ideal point method: 8 MW / 37 MWh, cost CNY 242.77M, volatility 17.84%.
- **Evidence links**: Figure 14a; Table 8.

## E06: Peak-Valley Arbitrage Strategy (Scheme 3)
- **Purpose**: Evaluate enhanced economic performance by implementing a peak-valley arbitrage strategy — charging only during low-price periods (3-5 AM) and discharging only during high-price periods (6-8 PM).
- **Results**: Same configuration points as Scheme 2 but with lower costs. At (10 MW/26 MWh), Scheme 3 cost is CNY 2.73M lower than Scheme 2. Flexible switching between schemes allows balancing grid stability and economic returns.
- **Evidence links**: Figure 14b; Table 8; Figure 13.
