# Real SimBench Planning Analysis - P3 CARS-MODE (real MOEA rewrite)

Status: `public_simbench_planning_v7_direct_moea_de_controls`.

## Why this version exists

The previous pipeline scored hand-shaped ranking heuristics per method (quality
constants, method-name-conditional weights) with deterministic repeats. It is
preserved as `*_proxy_methods_deprecated.*`. This version implements every method
as a real algorithm (pymoo NSGA-II/MOEA/D; real scalarized GA/PSO/DE; the proposed
method as a genuine self-contained MOEA), keeps the evaluation method-independent,
and runs 30 seeds per method/experiment with Mann-Whitney U + Holm tests.

## Headline results (pooled across experiments and seeds)

- Proposed method: `CARS-MODE`
- Proposed mean hypervolume: `0.04217835` (std `0.00380680`)
- Best baseline: `NSGA-II+Repair` with `0.03970671`
- Best ablation: `Ablation-FixedDE` with `0.04243314`
- Relative gain over best baseline: `6.22%`
- Relative gain over best ablation: `-0.60%`
- Holm-significant wins vs baselines: `62/63` (per-experiment comparisons)
- Holm-significant losses (any opponent): `2`
- Current value signal: `positive_but_partially_significant`

## Leaderboard (mean hypervolume, descending; worst-case HV = robustness readout)

| method | role | mean HV | std | worst-case HV | mean runtime (s) |
|---|---|---|---|---|---|
| Ablation-FixedDE | ablation | 0.04243314 | 0.00380846 | 0.04243314 | 0.118443 |
| Ablation-NoDER | ablation | 0.04222752 | 0.00381060 | 0.04222752 | 0.141673 |
| CARS-MODE | proposed | 0.04217835 | 0.00380680 | 0.04217835 | 0.121580 |
| NSGA-II+Repair | baseline | 0.03970671 | 0.00390207 | 0.03970671 | 0.079412 |
| NSGA-II | baseline | 0.03966261 | 0.00405090 | 0.03966261 | 0.079693 |
| Ablation-NoRepair | ablation | 0.03929326 | 0.00444244 | 0.03929326 | 0.080859 |
| NSDE | baseline | 0.03886633 | 0.00488881 | 0.03886633 | 0.051601 |
| GDE3 | baseline | 0.03884873 | 0.00479186 | 0.03884873 | 0.051543 |
| GA | baseline | 0.03088732 | 0.00068636 | 0.03088732 | 0.005310 |
| Standard DE | baseline | 0.03026524 | 0.00129071 | 0.03026524 | 0.012160 |
| Ablation-NoDiversity | ablation | 0.02802405 | 0.00977379 | 0.02802405 | 0.193231 |
| PSO | baseline | 0.01897728 | 0.00763435 | 0.01897728 | 0.005557 |
| Weighted Sum | baseline | 0.00584005 | 0.00261118 | 0.00584005 | 0.000299 |
| MOEA/D | baseline | 0.00047204 | 0.00000000 | 0.00047204 | 0.370512 |

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
