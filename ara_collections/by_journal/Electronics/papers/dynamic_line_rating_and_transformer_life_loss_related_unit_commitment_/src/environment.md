# Environment

- **Language/runtime**: Not specified in paper (development in PyCharm 2023.1 IDE). No source code
  released — "Data are contained within the article."
- **Framework**: Optimization solved with Gurobi 12.0.1 (mixed-integer program). Model development,
  debugging, monitoring performed with PyCharm 2023.1 debugging tools.
- **Hardware**: 24-core high-performance computer — Intel 13th Gen Core i9-13900 processor, 16 GB
  RAM.
- **Data sources**:
  - Ambient temperature: typical daily temperature of a region in southwest China, five regional
    24 h curves (Figure 2).
  - Load and wind power: day-ahead forecasts for the region (Figure 3), 24 h at 1 h resolution.
  - Network: standard IEEE 39-bus system data (10 synchronous generators, 39 buses; bus 31 slack;
    DFIG wind at buses 17 and 21 per the PSASP model). Generator parameters in Table 1.
- **Key dependencies**: Gurobi 12.0.1; PyCharm 2023.1. Exact Python/Gurobi API bindings and versions
  not specified in paper.
- **Protocols**: Day-ahead UC optimization over a 24 h horizon with 1 h time step; comparison of a
  conventional static-thermal-stability model against the proposed TL-TF model; sensitivity sweeps
  over wind-curtailment penalty, transformer investment cost, and temperature scaling factor λ.
- **Random seeds**: n/a (deterministic optimization; no stochastic sampling reported).
- **Data availability**: "Data are contained within the article. The original contributions
  presented in this study are included in the article. Further inquiries can be directed to the
  corresponding author." (§ Data Availability Statement).
