# Real SimBench Planning Analysis - P4 SHIELD-MOEA (real MOEA rewrite)

Status: `public_simbench_planning_v2_real_moea`.

## Why this version exists

The previous pipeline scored hand-shaped ranking heuristics per method (quality
constants, method-name-conditional weights) with deterministic repeats. It is
preserved as `*_proxy_methods_deprecated.*`. This version implements every method
as a real algorithm (pymoo NSGA-II/MOEA/D; real scalarized GA/PSO/DE; the proposed
method as a genuine self-contained MOEA), keeps the evaluation method-independent,
and runs 30 seeds per method/experiment with Mann-Whitney U + Holm tests.
Scenario uncertainty is now a real mechanism: each experiment carries a fixed
seeded set of 16 (load, DER, outage) scenarios; SHIELD-MOEA screens the
worst-K scenarios during search, while the final evaluation always uses a
disjoint-seed full scenario set (so screening cannot leak into scoring).

## Headline results (pooled across experiments and seeds)

- Proposed method: `SHIELD-MOEA`
- Proposed mean hypervolume: `0.27396193` (std `0.02699979`)
- Best baseline: `NSGA-II+Repair` with `0.26069954`
- Best ablation: `Ablation-NoResilienceObj` with `0.27466880`
- Relative gain over best baseline: `5.09%`
- Relative gain over best ablation: `-0.26%`
- Holm-significant wins vs baselines: `48/48` (per-experiment comparisons)
- Holm-significant losses (any opponent): `0`
- Current value signal: `significant_public_signal`

## Leaderboard (mean hypervolume, descending; worst-case HV = robustness readout)

| method | role | mean HV | std | worst-case HV | mean runtime (s) |
|---|---|---|---|---|---|
| Ablation-NoResilienceObj | ablation | 0.27466880 | 0.02666770 | 0.26976259 | 0.088949 |
| SHIELD-MOEA | proposed | 0.27396193 | 0.02699979 | 0.26911449 | 0.088926 |
| Ablation-NoScenarioScreen | ablation | 0.27265741 | 0.02627099 | 0.26804374 | 0.079205 |
| Ablation-NoOutage | ablation | 0.27124763 | 0.02511029 | 0.26610234 | 0.086895 |
| NSGA-II+Repair | baseline | 0.26069954 | 0.02696441 | 0.25654491 | 0.091147 |
| NSGA-II | baseline | 0.25952923 | 0.02816385 | 0.25541209 | 0.092437 |
| Ablation-NoRepair | ablation | 0.25176243 | 0.02919398 | 0.24649258 | 0.058331 |
| GA | baseline | 0.21987273 | 0.02811458 | 0.22106743 | 0.007151 |
| Deterministic Planning | baseline | 0.02386880 | 0.00124267 | 0.02281648 | 0.000385 |
| Weighted Sum | baseline | 0.01962865 | 0.00146482 | 0.01804840 | 0.000392 |
| MOEA/D | baseline | 0.00047321 | 0.00001812 | 0.00047318 | 0.450272 |

## Interpretation Boundary

Objectives are engineering proxies computed from SimBench subnet statistics;
electrical claims are backed separately by the pandapower AC validation stage
(`real_ac_validation_*`), which should be re-run against the compromise
compositions exported by this pipeline
(`tables/real_simbench_planning_compromise_compositions.csv`).

## Remaining Compliant Optimization Path

- Nodal siting/sizing experiments on concrete pandapower networks for method
  differentiation at the electrical level.
- Monetary calibration of cost coefficients.
- Keep deprecated proxy-method artifacts and all weak seeds in the evidence trail.
