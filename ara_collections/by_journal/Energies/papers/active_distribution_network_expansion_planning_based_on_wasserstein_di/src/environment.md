# Environment

## Test System

| Property | Value |
|----------|-------|
| Name | Portugal 54-node distribution system |
| Reference | [31] Miranda, Ranito, Proenca (IEEE Trans. Power Syst., 1994) |
| Substations | 4 (S1, S2, S3, S4) |
| Source-load nodes | 54 |
| Existing lines | Multiple (black in topology diagram) |
| Candidate (to-be-built) lines | Multiple (dashed in topology diagram) |
| SOP/switch candidate positions | Pre-selected tie positions between feeders (red in topology diagram) |
| DG nodes | 9 (1, 5, 9, 12, 14, 22, 30, 33, 47) |
| ESS nodes | 5 (8, 9, 13, 32, 50) |
| Voltage level | Not specified (distribution level) |

## Planning & Economic Parameters

| Parameter | Value |
|-----------|-------|
| Project period | 20 years |
| Discount rate | 0.03 |
| Line construction cost | 150,000 CNY/km |
| Line capacity | 7.27 MW |
| Line resistance | 0.307 Ohm/km |
| Line reactance | 0.38 Ohm/km |
| SOP unit capacity | 10 kW |
| SOP investment cost | 1000 CNY/kW |
| SOP loss coefficient | 0.02 |
| SOP O&M coefficient | 0.01 |
| SOP max capacity per line | 1 MW |
| Interconnection switch cost | 100,000 CNY each |
| Switch O&M coefficient | 0.05 |
| ESS annual O&M cost | 0.35 CNY/kW |
| ESS charging / discharging efficiency | 0.86 |
| ESS battery loss rate | 0.1 |
| DR incentive cost | 0.3 CNY/kW |
| DR max contract signing ratio | 50% |
| Purchase price (from grid) | 0.5 CNY/kW |
| Sale price (to grid) | 0.7 CNY/kW |
| DG penalty cost | 0.15 CNY/kW |
| DG max reduction ratio | 0.5 |

## Software & Solver

| Component | Specification |
|-----------|---------------|
| Optimization model | MISOCP (mixed-integer second-order cone programming) |
| Solver | CPLEX (version not specified) |
| Environment | Not specified (likely MATLAB + YALMIP or Python + Pyomo/CPLEX interface) |
| Model reformulation pipeline | SOCP relaxation (power flow) -> Lagrange duality (inner max) -> McCormick relaxation (bilinear terms) -> MISOCP |
| Nonconvex solver for comparison | IPOPT (Interior Point OPTimizer) |
| Machine | Not specified |
| Computation time (McCormick) | 2.52 hours |
| Computation time (Bilinear-Removed) | 1.59 hours |
| Computation time (IPOPT) | >5 hours (no solution found) |

## Data Sources

| Data | Source |
|------|--------|
| Network topology and line parameters | [31] |
| DG locations and maximum power | Table 1 |
| ESS locations and parameters | Table 2 |
| Scenario data (DG/load historical) | Not published (assumed from public datasets or simulation) |
| Cost parameters | Industry data and literature (citations [4], [9], [14]) |

## Claims Coverage
| Claim | E01 | E02 | E03 | E04 |
|-------|-----|-----|-----|-----|
| C01   | X   |     |     | X   |
| C02   |     | X   |     | X   |
| C03   |     |     | X   |     |
| C04   | X   |     |     |     |
| C05   |     |     | X   |     |
