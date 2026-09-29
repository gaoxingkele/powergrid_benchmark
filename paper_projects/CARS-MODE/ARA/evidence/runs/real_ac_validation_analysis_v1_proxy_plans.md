# SimBench AC Load-Flow Validation - P3 CARS-MODE

Status: `public_simbench_ac_validation_v1`. pandapower AC power flow on real SimBench MV networks
(1-MV-rural--0-sw, 1-MV-semiurb--0-sw, 1-MV-urban--0-sw, 1-MV-comm--0-sw) across 6 stress scenarios,
validating the plan compositions produced by every method in the public
planning experiment (portfolios rebuilt deterministically, repeat=1).

## Headline

- No-Plan reference AC-feasible rate: `0.500000` (stress-only: `0.400000`)
- `CARS-MODE` AC-feasible rate: `0.625000` (stress-only: `0.550000`)
- Best baseline: `GA` with `0.638889` (stress-only: `0.566667`)
- `CARS-MODE` mean min voltage: `0.972263` pu vs No-Plan `0.961929` pu
- `CARS-MODE` mean max line loading: `75.8268%` vs No-Plan `90.7705%`

## Summary Table

| method | role | AC-feasible rate | stress feasible | mean min vm (pu) | mean max loading (%) | mean losses (MW) |
|---|---|---|---|---|---|---|
| NoPlan | reference | 0.500000 | 0.400000 | 0.961929 | 90.7705 | 0.643324 |
| Ablation-NoDER | ablation | 0.666667 | 0.600000 | 0.968996 | 59.6059 | 0.511151 |
| GA | baseline | 0.638889 | 0.566667 | 0.972235 | 73.3833 | 0.503969 |
| CARS-MODE | proposed | 0.625000 | 0.550000 | 0.972263 | 75.8268 | 0.517248 |
| NSGA-II | baseline | 0.625000 | 0.550000 | 0.972263 | 75.8268 | 0.517248 |
| MOEA/D | baseline | 0.625000 | 0.550000 | 0.972263 | 75.8268 | 0.517248 |
| Standard DE | baseline | 0.625000 | 0.550000 | 0.971352 | 70.8562 | 0.513739 |
| Ablation-NoRepair | ablation | 0.625000 | 0.550000 | 0.973211 | 71.0949 | 0.486698 |
| Ablation-FixedDE | ablation | 0.625000 | 0.550000 | 0.971862 | 75.2354 | 0.524982 |
| PSO | baseline | 0.611111 | 0.533333 | 0.970780 | 72.7919 | 0.522950 |
| Weighted Sum | baseline | 0.500000 | 0.450000 | 0.969783 | 85.6187 | 0.595516 |
| Ablation-NoDiversity | ablation | 0.500000 | 0.450000 | 0.969783 | 85.6187 | 0.595516 |

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
