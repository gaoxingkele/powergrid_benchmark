# Environment

This is a simulation/analytical modeling study. No source code, repository, or executable artifact is released (the underlying dataset is classified — see Data Availability). The method is described in prose + equations only; no pseudocode is printed, so no code stub is reconstructed here (it would only duplicate `logic/solution/`).

- **Language/runtime**: Not specified in paper. (Figures 3–7 rendered in a MATLAB-style plotting environment — inferred from axis/legend styling, not stated.)
- **Framework**: Custom genetic-algorithm implementation for the multi-voltage grid-evolution model; AHP computed analytically. Specific library/toolbox: Not specified in paper.
- **Hardware**: Not specified in paper.
- **Data sources**:
  - Regional power grid, base year 2020: 220 equivalent load nodes; aggregate base demand 2013.74 MW.
  - Planning-phase (2017–2020) grid construction program; medium-to-long-term (2021–2035) load forecast.
  - 2020 baseline topology: 5 × 220 kV substations, 12 × 110 kV substations, 18 × 110 kV transmission lines, 516 × 10 kV distribution feeders; six new 110 kV substations (labeled 1–6) commissioned during 2017–2020.
  - Load forecast: 2734.83 MW (2025), 3316.22 MW (2035).
  - **Access**: dataset cannot be released — contains classified information (trade secrets, sensitive technical details). Not reproducible externally.
- **Key dependencies**: Not specified in paper.
- **Protocols / model configuration**:
  - Genetic algorithm: max generations 200, population size (INDIVIDUAL_NUM) 800, crossover probability (CROSS_RATE) 0.5, mutation probability (UPTATE_RATE) 0.5.
  - Operational constraints: max substation loading factor 75%; max safe operating current 552 A (10 kV feeders), 718 A (110 kV lines); discount rate 8%.
  - AHP consistency threshold 0.1; achieved CR = 0.00726.
  - Planning horizons: 2020 base → 2025 → 2035 (rolling optimization).
- **Random seeds**: Not specified in paper.
- **Funding**: Key Planning Project of Guangdong Power Grid Corporation, grant 0300002023030201GH00091.
