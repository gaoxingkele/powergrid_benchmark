# Concepts

## Core Concepts

### 1. Hybrid Energy Storage System (HESS)
- **Definition**: Combined deployment of flow batteries (vanadium redox flow battery, long-duration) and lithium-ion batteries (short-duration) to leverage complementary characteristics.
- **Rationale**: Flow batteries offer long lifespan, rapid response, adjustable capacity; Li-ion batteries offer high energy density and millisecond response time.
- **Role**: The flow battery handles low-frequency/large-energy fluctuations; the Li-ion battery handles high-frequency/small-energy fluctuations.

### 2. Flexibility Supply-Demand Balance
- **Definition**: The extent to which flexibility supply exceeds flexibility demand at any moment, over any timescale, and in any direction, beyond a permissible threshold.
- **Components**: 
  - Supply resources: renewable output, thermal power, energy storage, main grid exchange
  - Demand: load demand
  - Gap: flexibility deficiency when supply cannot meet demand

### 3. Variational Mode Decomposition (VMD)
- **Origin**: Non-recursive signal decomposition method originating from Empirical Mode Decomposition (EMD)
- **Advantage over EMD**: Built on optimization theory, unique decomposition results, strong adaptability for non-stationary signals, mitigates mode mixing and endpoint effects
- **Key parameters**: Mode number K, penalty factor alpha
- **Process**: Decomposes total ESS target power into K Intrinsic Mode Functions (IMFs) with specific bandwidths and center frequencies

### 4. Particle Swarm Optimization Variational Mode Decomposition (PSO-VMD)
- **Purpose**: Adaptive optimization of VMD parameters (K, alpha)
- **Objective function**: Composite loss = full-band reconstruction MSE + lambda * (K / N) for modal redundancy penalty
- **Innovation**: Eliminates subjectivity in selecting VMD parameters for HESS power allocation

### 5. Weighted Average Algorithm (WAA)
- **Type**: Metaheuristic optimization algorithm
- **Core idea**: Uses weighted average position of the population to guide search, preventing individuals from trapping in local optima
- **Phases**: 
  - Exploitation (3 strategies): global + personal best guided, personal best guided, global best guided
  - Exploration (2 strategies): Levy flight, random repositioning
- **Switching**: Based on sinusoidal function f(it) with 0.5 threshold

### 6. Improved Weighted Average Algorithm (IWAA)
- **Refraction Opposition-based Learning**: Enhances exploration phase by generating opposition solutions based on light refraction principles
- **Dynamic Crowding Distance**: Sequential removal method for Pareto solution maintenance — iteratively removes the solution with smallest crowding distance, recalculates, and repeats until target set size is reached
- **Purpose**: Overcomes WAA limitations: premature convergence to local optima, insufficient Pareto diversity

### 7. Bi-Level (Two-Tier) Optimization
- **Upper level**: Capacity and power planning — determines storage location, rated capacity, rated power to minimize lifecycle costs
- **Lower level**: Operational optimization — allocates storage power in real-time to optimize flexibility, voltage, and line losses
- **Coupling**: Lower-level results feed back to upper level for iterative refinement (closed-loop)

### 8. Flexibility Insufficiency Penalty
- **Purpose**: Penalize situations where energy storage output power cannot fully cover the system flexibility power shortage
- **Enforcement**: Unit penalty cost Q_penal applied to flexibility gap magnitude
- **Advantage**: Drives the optimization toward configurations that provide adequate flexibility

## Supporting Concepts

### 9. Refraction Opposition-based Learning
- **Inspiration**: Law of light refraction in physics
- **Mechanism**: Generates opposite solutions using a refraction formula, enabling algorithm to jump out of current optimization region/direction
- **Application**: Applied to the second exploration strategy of WAA

### 10. Dynamic Crowding Distance
- **Standard crowding distance**: Measures density around a Pareto solution based on objective function distances to neighbors
- **Improved method**: Sequential removal — sort by crowding distance, remove smallest, recalculate, repeat until target size N reached
- **Benefit**: Better uniformity and diversity of Pareto solutions compared to single-pass selection

### 11. Median Frequency Threshold
- **Definition**: Median of all IMF center frequencies used as the decision boundary for high/low frequency separation
- **Role**: IMFs with center frequency > median -> high-frequency (assigned to Li-ion); <= median -> low-frequency (assigned to flow battery)

### 12. Scenario Clustering
- **Purpose**: Reduce the dimensionality of annual wind/PV/load time series data
- **Method**: k-means or similar clustering to identify representative daily patterns
- **Output**: Clustering centers with 95% confidence intervals (Figures 3-5)
