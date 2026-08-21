# Experimental Environment

## Hardware
Not specified in paper. Standard computing environment assumed for power system optimization studies.

## Software
- TER-NSGA-II implementation (source code available at: https://github.com/ding-jin-xiu/TER-NSGA-II-backbone-grid-planning)
- Benchmark algorithms: NSGA-II and NSGA-III/NG implementations
- DC power flow solver (standard implementation)
- irace package for automatic algorithm configuration (Ref [41])

## Test Systems

### IEEE 118-Bus System (Main Validation)
- Core generation buses: 10, 69, 80, 89
- Core-load buses: 11, 16, 20, 29, 50
- Pumped-storage units: Buses 63 and 64, each 240 MW
- Candidate line set: Based on original IEEE 118-bus topology
- Edge connectivity constraint: lambda >= 2 between core loads and black-start units

### IEEE 300-Bus System (Scalability Validation)
- Same modeling framework as IEEE 118-bus case
- Used to assess algorithm scalability to larger networks
- 10 independent runs per algorithm

## Algorithm Configuration

| Parameter | IEEE 118-bus | IEEE 300-bus |
|-----------|-------------|-------------|
| Population size (M) | 50 | 50 |
| Max generations (T_max) | 200 | 200 |
| Stage I->II (T1) | 77 | Tuned |
| Stage II->III (T2) | 115 | Tuned |
| Reverse learning (Treverse) | 49 | Tuned |
| Independent runs | 50 | 10 |

## Comparison Protocol
- All algorithms (TER-NSGA-II, NSGA-II, NSGA-III/NG) use the same:
  - Decision encoding (binary line selection)
  - Population size
  - Termination criterion
  - Network data
  - Constraint-evaluation criteria
- Statistics reported from feasible runs only
- Metrics: F1, F2, feasible-run rate, IGD+, HV, Spread
