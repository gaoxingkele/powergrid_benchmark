# SimBench AC Load-Flow Validation - P4 SHIELD-MOEA

Status: `public_simbench_ac_validation_v1`. pandapower AC power flow on real SimBench MV networks
(1-MV-rural--0-sw, 1-MV-semiurb--0-sw, 1-MV-urban--0-sw, 1-MV-comm--0-sw) across 6 stress scenarios,
validating the plan compositions produced by every method in the public
planning experiment (portfolios rebuilt deterministically, repeat=1).

## Headline

- No-Plan reference AC-feasible rate: `0.500000` (stress-only: `0.400000`)
- `SHIELD-MOEA` AC-feasible rate: `0.652778` (stress-only: `0.583333`)
- Best baseline: `MOEA/D` with `0.652778` (stress-only: `0.583333`)
- `SHIELD-MOEA` mean min voltage: `0.969869` pu vs No-Plan `0.961929` pu
- `SHIELD-MOEA` mean max line loading: `60.3370%` vs No-Plan `90.7705%`

## Summary Table

| method | role | AC-feasible rate | stress feasible | mean min vm (pu) | mean max loading (%) | mean losses (MW) |
|---|---|---|---|---|---|---|
| NoPlan | reference | 0.500000 | 0.400000 | 0.961929 | 90.7705 | 0.643324 |
| SHIELD-MOEA | proposed | 0.652778 | 0.583333 | 0.969869 | 60.3370 | 0.505649 |
| MOEA/D | baseline | 0.652778 | 0.583333 | 0.969885 | 64.7172 | 0.517050 |
| Ablation-NoOutage | ablation | 0.652778 | 0.583333 | 0.969711 | 65.0340 | 0.519052 |
| NSGA-II | baseline | 0.638889 | 0.566667 | 0.970035 | 67.5207 | 0.521040 |
| Ablation-NoRepair | ablation | 0.638889 | 0.566667 | 0.970696 | 64.7073 | 0.504012 |
| Ablation-NoResilienceObj | ablation | 0.625000 | 0.550000 | 0.970330 | 68.7924 | 0.522052 |
| GA | baseline | 0.611111 | 0.533333 | 0.971056 | 68.9767 | 0.510284 |
| Ablation-NoScenarioScreen | ablation | 0.597222 | 0.516667 | 0.970088 | 67.5632 | 0.520457 |
| Weighted Sum | baseline | 0.500000 | 0.450000 | 0.969783 | 85.6187 | 0.595516 |
| Deterministic Planning | baseline | 0.500000 | 0.450000 | 0.969783 | 85.6187 | 0.595516 |

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
