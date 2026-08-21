# Environment

## Model type
Mixed-Integer Linear Program (MILP) — a single-plant self-unit-commitment formulation for a 5 × 2 CCGT.

## Data provenance

| Data | Source | Details |
|------|--------|---------|
| CCGT plant parameters (GCC, PAF, MUG, STF, KGC, startup windows) | TEBSA-like plant, Colombian system | Table 1; based on published TEBSA plant data and Colombian grid-code declarations |
| Gas turbine characteristics (G̅, G̲, TC, TD) | Table 3 | Specified per-unit values (100 MW max, 50 MW min, 5 MW/min ramps) |
| Steam turbine characteristics (S̅, S̲, GSTH, GSTC) | Table 4 | Specified per-unit values (170 MW max, 80 MW min, hot/cold start outputs) |
| Startup ramp blocks (hot/warm/cold) | Colombian grid code | Table 2; official startup and shutdown energy block declarations |
| Initial conditions — Case I | Table 5 | Hot-start scenario: GT1, GT5, ST1 online at t=0 |
| Initial conditions — Case II | Table 6 | Warm-start scenario: all units offline at t=0 |
| Deviation penalty price | Colombian market [25] | PCC price used to compute USD/MWh penalty |
| Equipment damage evidence | Figure 1, refs [4–7] | Blade erosion photographs from TEBSA operational experience |

## Solver / software

The paper does not specify the solver software (e.g., Gurobi, CPLEX) or version used to solve the MILP. Solution times and optimality gaps are not reported. The model is described as an MILP; no custom algorithm or decomposition technique is presented.

## Code status

No public code repository is referenced in the paper. No author-provided replication code has been located. The SEUC formulation (Eqs. 1–46) is described in sufficient detail for independent reimplementation, but the heuristic simulation code against which the model is compared is not published.
