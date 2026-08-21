# Concepts

## 1. NSGA-II (Non-dominated Sorting Genetic Algorithm II)
A multi-objective evolutionary algorithm that uses fast non-dominated sorting to rank solutions by Pareto dominance, crowding distance to maintain population diversity, and an explicit elite-preserving mechanism. In this study, NSGA-II optimizes two objectives (cost and volatility) over 300 generations with a population of 20 and offspring of 60.

## 2. State of Charge (SOC)
A parameter measuring the current energy level of an energy storage battery as a percentage of its rated capacity. SOC(t) evolves according to charging and discharging equations involving efficiency factors. SOC must remain within [SOC_min, SOC_max] for safe battery operation.

## 3. Pareto Frontier / Pareto Optimality
The set of non-dominated solutions in multi-objective optimization where no single objective can be improved without degrading another. In this paper, the Pareto frontier represents the trade-off between minimizing investment cost and minimizing power fluctuation rate.

## 4. Power Fluctuation Rate (sigma)
The relative standard deviation of wind farm output power, calculated as the standard deviation of power samples divided by rated wind farm power. A smaller sigma indicates a smoother wind power output curve after storage configuration.

## 5. Energy Storage System (ESS) Configuration
The decision variables of rated power (MW) and rated capacity (MWh) that define an energy storage system. These determine the system's capability to charge/discharge and its energy buffering capacity, directly affecting both cost and smoothing performance.

## 6. Electricity Spot Market
A market mechanism for real-time electricity trading where prices fluctuate based on supply and demand. This study uses 2024 Guangdong Province spot prices, with low-price periods (3-5 AM) and high-price periods (6-8 PM) for arbitrage strategies.

## 7. Peak-Valley Arbitrage
A strategy where energy storage batteries charge during low electricity price periods and discharge during high price periods to profit from the price differential. Implemented as Scheme 3 in this paper.

## 8. Crowding Distance
A density estimation metric in NSGA-II that measures the perimeter of the rectangle formed by neighboring solutions in objective space. Used to maintain population diversity by preferring solutions in less crowded regions.

## 9. MOPSO (Multi-Objective Particle Swarm Optimization)
A swarm-intelligence-based multi-objective optimization algorithm used as a benchmark comparator against NSGA-II. Uses particles with velocity updates guided by personal and global best positions, with an external archive for Pareto front storage.

## 10. Ideal Point Method (TOPSIS)
A multi-criteria decision-making technique that identifies optimal solutions by calculating the normalized distance from each candidate solution to an ideal point (the best possible values across all objectives). Used to select the final optimal configuration from Pareto frontier points.

## 11. Inflection Point Method
A selection technique based on identifying the point of maximum curvature on the Pareto frontier, beyond which further improvements in one objective require disproportionately large sacrifices in the other.

## 12. xi (Incremental Cost Metric)
A metric defined as the ratio of energy storage investment cost to volatility decline rate (xi = C_a / lambda), measuring the incremental cost required to achieve a 1% reduction in output volatility. Used to compare algorithm performance.
