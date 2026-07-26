# SimBench AC Load-Flow Validation - P3 CARS-MODE

Status: `public_simbench_ac_validation_v2_real_moea_plans`. pandapower AC power flow on real SimBench MV networks
(1-MV-rural--0-sw, 1-MV-semiurb--0-sw, 1-MV-urban--0-sw, 1-MV-comm--0-sw) across 6 stress scenarios,
validating the compromise-plan compositions exported by the real-MOEA
planning pipeline (`real_simbench_planning_compromise_compositions.csv`,
seed-0 compromise solution per method/experiment).

## Headline

- No-Plan reference AC-feasible rate: `0.500000` (stress-only: `0.400000`)
- `CARS-MODE` AC-feasible rate: `0.611111` (stress-only: `0.566667`)
- Best baseline: `Standard DE` with `0.680556` (stress-only: `0.616667`)
- `CARS-MODE` mean min voltage: `0.972903` pu vs No-Plan `0.961929` pu
- `CARS-MODE` mean max line loading: `76.5615%` vs No-Plan `90.7705%`

## Summary Table

| method | role | AC-feasible rate | stress feasible | mean min vm (pu) | mean max loading (%) | mean losses (MW) |
|---|---|---|---|---|---|---|
| NoPlan | reference | 0.500000 | 0.400000 | 0.961929 | 90.7705 | 0.643324 |
| Standard DE | baseline | 0.680556 | 0.616667 | 0.973129 | 63.5423 | 0.483217 |
| NSGA-II | baseline | 0.666667 | 0.600000 | 0.973928 | 75.6122 | 0.522398 |
| Ablation-NoRepair | ablation | 0.666667 | 0.600000 | 0.973526 | 70.4723 | 0.499712 |
| Ablation-NoDER | ablation | 0.666667 | 0.600000 | 0.969715 | 56.7907 | 0.500178 |
| GA | baseline | 0.638889 | 0.566667 | 0.971984 | 66.7341 | 0.519633 |
| CARS-MODE | proposed | 0.611111 | 0.566667 | 0.972903 | 76.5615 | 0.546150 |
| PSO | baseline | 0.611111 | 0.533333 | 0.971559 | 75.6902 | 0.527960 |
| Ablation-FixedDE | ablation | 0.569444 | 0.516667 | 0.971959 | 73.6949 | 0.553252 |
| Ablation-NoDiversity | ablation | 0.569444 | 0.483333 | 0.968081 | 69.8574 | 0.539019 |
| MOEA/D | baseline | 0.500000 | 0.400000 | 0.961929 | 90.7705 | 0.643324 |
| Weighted Sum | baseline | 0.500000 | 0.400000 | 0.963618 | 88.4221 | 0.629353 |

## Mapping Assumptions (read before citing)

Planning candidates live on aggregated SimBench subnet statistics, so plan
*compositions* (action-kind counts) are mapped onto concrete MV networks with
fixed, method-independent rules: reinforcement adds a parallel conductor on the
most-loaded lines; storage connects at the weakest-voltage load buses
(+/-3% of net load, discharging under load stress and charging
under DER stress); DER adds PV at the highest-load buses (4% of net
load, scaled with the scenario DER factor); automation has no steady-state
electrical effect. This validates whether each method's plan mix restores or
preserves AC feasibility under stress; it is not a nodal siting/sizing study.

## Interpretation

- `ac_feasible` requires convergence, all bus voltages within [0.95, 1.05] pu,
  and no line above 100% loading.
- The peak_n1_outage scenario drops the highest-loaded line whose outage leaves
  all buses supplied (radial spurs are skipped).
- Scenario axis doubles as a sensitivity analysis over load growth and DER
  penetration; per-scenario rows are in the results CSV.
