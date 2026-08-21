# Environment

- **Language/runtime**: MATLAB 2024a
- **Framework**: CPLEX 12.7.1 (MILP/MISOCP solver)
- **Hardware**: Standard desktop workstation (not further specified)
- **Data sources**:
  - Modified IEEE 33-node distribution network (12.66 kV) coupled with 20-node natural gas grid
  - Generator data: Tables A1–A3 (capacity, constraints, costs)
  - Gas network node data: Table A4
  - Gas source data: Table A5
  - EV parameters: Table A6
  - Wind forecast: deterministic day-ahead profiles for two wind farms
  - TOU price bands: peak/flat/valley predefined hourly blocks
  - Cross-price elasticity matrix: adopted from established DR literature
- **Key dependencies**: CPLEX 12.7.1
- **Protocols**: Single-instance MILP/MISOCP assembly (two-stage logic, solved as one model). 12-segment piecewise-linear Weymouth approximation. Homogeneous EV fleet aggregation.
- **Computational performance**: Converges to <0.01% optimality gap within seconds per configuration
- **Random seeds**: Not specified in paper
- **Code location**: Not released publicly; case study data in Appendix A
