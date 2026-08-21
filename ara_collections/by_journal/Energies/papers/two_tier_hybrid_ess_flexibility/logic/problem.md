# Problem: Flexibility Supply-Demand Balance in High-Renewable Penetration Power Grids

## Domain
Power systems operation and planning, energy storage configuration, grid flexibility.

## Context
As the penetration of renewable energy (wind and solar PV) into power grids increases, the spatio-temporal mismatch between renewable generation and load demand becomes increasingly prominent. This creates challenges including wind/solar curtailment and load shedding that threaten secure grid operation.

### Key Dimensions
- **Timescale span**: Renewable fluctuations range from seconds to days.
- **Voltage level**: The study focuses on 220 kV and above regional transmission grids.
- **Geographic scope**: A regional grid in Southwest China (12,735 km^2, 5.68 million people served).
- **Scale**: Installed thermal capacity 3500 MW, annual sales 31.41 billion kWh, peak-valley load difference 3091 MW.

## Core Problem Statement
**Flexibility supply-demand balance** — the extent to which the flexibility provided by various resources exceeds (or falls short of) the flexibility requirement, at any moment, over any timescale, and in any direction, relative to a permissible threshold.

### Specific Challenges Addressed

1. **Single-type energy storage temporal limitations**: Short-term storage (Li-ion) can safeguard instantaneous system security but cannot address sustained energy deficits; long-term storage (flow batteries) has slower response for high-frequency fluctuations.

2. **Subjectivity in VMD parameter selection**: Existing VMD-based power allocation methods exhibit significant subjectivity in selecting key algorithm parameters (mode number K, penalty factor alpha) and overlook the step of determining specific power allocation to different storage types after decomposition.

3. **Imperfect flexibility resource synergy**: Existing literature on flexibility resource coordination does not fully integrate the dynamic response characteristics of multi-dimensional resources (source, network, load, and storage).

4. **Excessive energy storage costs**: Over-configuring energy storage leads to unnecessary installation and operational costs; under-configuring leads to flexibility insufficiency penalties.

5. **Limited focus on large-scale centralized HESS**: Most existing work focuses on wind-storage or PV-storage integrated systems at farm level, with relatively limited attention to large-scale centralized energy storage in regional grids hosting both utility-scale PV and wind.

## Formulation (Succinct)

The problem is cast as a **mixed-integer nonlinear bi-level optimization**:

- **Upper level**: Determine storage location, rated capacity, and rated power to minimize annualized lifecycle costs.
- **Lower level**: Allocate storage power to optimize flexibility regulation and voltage stability, with VMD-PSO for frequency-based power decomposition into Li-ion (high-frequency) and flow battery (low-frequency) components.

### Objective Functions
1. Minimize total lifecycle cost (investment + O&M) — upper level
2. Minimize operational cost — lower level
3. Minimize flexibility deficiency penalty — lower level
4. Minimize voltage deviation — lower level
5. Minimize line losses — lower level

## Significance
This problem is critical because flexibility is becoming the core and defining characteristic of power system operations as renewable penetration continues to rise. The proposed HESS approach aims to overcome the temporal limitations of single-type storage and achieve flexibility supply-demand matching across critical timescales.
