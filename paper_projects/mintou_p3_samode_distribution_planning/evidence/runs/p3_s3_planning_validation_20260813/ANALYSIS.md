# P3 S3 Planning Validation Analysis

## Material Passport

- Origin Skill: experiment-agent
- Origin Mode: validate
- Origin Date: 2026-08-13
- Verification Status: VERIFIED
- Version Label: p3_s3_planning_validation_v1

## Reference-Point and Clipping Audit

The full 2940-row optimizer archive was rerun and the legacy hypervolume matched at eight decimals: `True` (maximum absolute serialized difference `0`).
Across `68248` returned front points, the sampled-bound implementation clipped `2189` points (`2281` coordinates). Before clipping, `0` points were not strictly dominated by the normalized 1.10 reference point; the smallest raw coordinate-wise reference margin was `0.145454545455`. All clipped coordinates were below zero (`1750` voltage-risk and `531` negative-reliability coordinates), and none exceeded one. Clipping was therefore unnecessary for reference-point dominance in these runs: it floored improvements beyond the sampled lower envelope and collapsed distinct values onto the zero boundary.
Under the analytic feasible envelopes, outside-envelope coordinate count was `0`. The alternative 1.05 reference point strictly dominated every rerun point; the smallest coordinate-wise margin was `0.05000000`.

The analytic envelopes are method-independent consequences of the implemented P3 equations: cost `[0,B]`, loss `[0.015, L_0 lambda]`, voltage `[0.005, U_0 lambda]`, negative hosting `[-1,0]`, and negative reliability `[-1,-0.35]`. No optimizer output is used to construct them, and no hypervolume input is clipped under this audit.

## Robustness Ranking

With analytic bounds and ref=1.05, CARS-MODE's pooled descriptive mean is `0.00043362`. The strongest implemented baseline is `NSGA-II+Repair` at `0.00043374`, a relative CARS-MODE margin of `-0.03%`. The combined FixedDE control remains `0.00043527` and therefore remains a joint negative/null result rather than evidence for adaptation.

| method | role | analytic HV r=1.10 | rank | analytic HV r=1.05 | rank | common-ref IGD+ | rank |
|---|---|---:|---:|---:|---:|---:|---:|
| Ablation-NoDER | ablation | 0.00269810 | 1 | 0.00057343 | 1 | 0.00771034 | 1 |
| Ablation-FixedDE | ablation | 0.00212414 | 3 | 0.00043527 | 2 | 0.02211203 | 4 |
| NSGA-II+Repair | baseline | 0.00213251 | 2 | 0.00043374 | 3 | 0.02133904 | 2 |
| CARS-MODE | proposed | 0.00211607 | 4 | 0.00043362 | 4 | 0.02231102 | 5 |
| NSGA-II | baseline | 0.00211578 | 5 | 0.00043044 | 5 | 0.02205899 | 3 |
| Ablation-NoRepair | ablation | 0.00208868 | 6 | 0.00042506 | 6 | 0.02246996 | 6 |
| GDE3 | baseline | 0.00208861 | 7 | 0.00042465 | 7 | 0.02301124 | 7 |
| NSDE | baseline | 0.00207191 | 8 | 0.00042107 | 8 | 0.02368155 | 8 |
| Ablation-NoDiversity | ablation | 0.00111108 | 9 | 0.00021810 | 9 | 0.10859249 | 9 |
| PSO | baseline | 0.00046218 | 10 | 0.00007950 | 10 | 0.20607965 | 10 |
| Standard DE | baseline | 0.00040698 | 11 | 0.00005600 | 11 | 0.22211507 | 11 |
| GA | baseline | 0.00036609 | 12 | 0.00004594 | 12 | 0.23452312 | 12 |
| Weighted Sum | baseline | 0.00015299 | 13 | 0.00002026 | 13 | 0.39271279 | 13 |
| MOEA/D | baseline | 0.00011000 | 14 | 0.00000656 | 14 | 0.46451462 | 14 |

The pooled ranks summarize heterogeneous experiments and are descriptive. Confirmatory comparisons retain the optimizer seed as the analysis unit and apply Holm correction within each experiment across twelve stochastic opponents. Weighted Sum remains one deterministic point per experiment.

- `analytic_hv_ref110`: favorable CARS-MODE mean in `63/84` experiment/opponent cells; `40/84` also Holm-significant in the favorable direction.
- `analytic_hv_ref105`: favorable CARS-MODE mean in `64/84` experiment/opponent cells; `40/84` also Holm-significant in the favorable direction.
- `igd_plus_common_reference`: favorable CARS-MODE mean in `54/84` experiment/opponent cells; `39/84` also Holm-significant in the favorable direction.

## Common-Reference Diagnostic

IGD+ is computed for every run against the empirical non-dominated union of all methods and seeds in the same planning experiment after analytic normalization. Lower is better. This common reference contains base_distribution_planning: 2555 points, constraint_repair: 1709 points, der_siting_sizing: 933 points, load_growth_expansion: 2653 points, pareto_quality: 2618 points, runtime_scalability: 3385 points, storage_allocation: 805 points. Because the reference front is empirical and includes the tested methods, IGD+ is complementary rather than an independent benchmark.

## Physical-Diagnostic Boundary

No new AC power-flow cases were run. The existing AC layer is retained as an illustrative composition diagnostic. The new matched common-panel table compares each archived method row with the same No-Plan experiment/network/case row, but it does not create optimizer-seed replication or hierarchical uncertainty. GDE3, NSDE, and NSGA-II+Repair have no archived AC rows and remain absent from electrical claims.

## Reproducibility Verdict

The legacy metric rerun is `REPRODUCIBLE` at the archive's eight-decimal precision. The analytic-bound/ref=1.10, analytic-bound/ref=1.05, and common-reference IGD+ columns are new deterministic evaluations of the preserved rerun fronts. Runtime is recorded for provenance but is not compared across environments.
