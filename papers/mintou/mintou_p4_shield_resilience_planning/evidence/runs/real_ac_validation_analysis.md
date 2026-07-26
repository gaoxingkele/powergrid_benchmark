# SimBench AC Load-Flow Validation - P4 SHIELD-MOEA

Status: `public_simbench_ac_validation_v2_real_moea_plans`. pandapower AC power flow on real SimBench MV networks
(1-MV-rural--0-sw, 1-MV-semiurb--0-sw, 1-MV-urban--0-sw, 1-MV-comm--0-sw) across 6 stress scenarios,
validating the compromise-plan compositions exported by the real-MOEA
planning pipeline (`real_simbench_planning_compromise_compositions.csv`,
seed-0 compromise solution per method/experiment).

## Headline

- No-Plan reference AC-feasible rate: `0.500000` (stress-only: `0.400000`)
- `SHIELD-MOEA` AC-feasible rate: `0.708333` (stress-only: `0.650000`)
- Best baseline: `GA` with `0.708333` (stress-only: `0.650000`)
- `SHIELD-MOEA` mean min voltage: `0.973656` pu vs No-Plan `0.961929` pu
- `SHIELD-MOEA` mean max line loading: `68.7531%` vs No-Plan `90.7705%`

## Summary Table

| method | role | AC-feasible rate | stress feasible | mean min vm (pu) | mean max loading (%) | mean losses (MW) |
|---|---|---|---|---|---|---|
| NoPlan | reference | 0.500000 | 0.400000 | 0.961929 | 90.7705 | 0.643324 |
| SHIELD-MOEA | proposed | 0.708333 | 0.650000 | 0.973656 | 68.7531 | 0.484187 |
| GA | baseline | 0.708333 | 0.650000 | 0.974046 | 63.9211 | 0.466181 |
| Ablation-NoRepair | ablation | 0.708333 | 0.650000 | 0.974096 | 70.7278 | 0.491981 |
| Ablation-NoResilienceObj | ablation | 0.708333 | 0.650000 | 0.974225 | 71.2802 | 0.488204 |
| NSGA-II | baseline | 0.694444 | 0.633333 | 0.973732 | 69.6426 | 0.480895 |
| Ablation-NoScenarioScreen | ablation | 0.694444 | 0.633333 | 0.972319 | 65.5529 | 0.493379 |
| Ablation-NoOutage | ablation | 0.625000 | 0.583333 | 0.973213 | 82.3339 | 0.567231 |
| Deterministic Planning | baseline | 0.541667 | 0.550000 | 0.980021 | 103.6272 | 0.780180 |
| MOEA/D | baseline | 0.500000 | 0.400000 | 0.961929 | 90.7705 | 0.643324 |
| Weighted Sum | baseline | 0.500000 | 0.400000 | 0.962705 | 84.7985 | 0.624380 |

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
