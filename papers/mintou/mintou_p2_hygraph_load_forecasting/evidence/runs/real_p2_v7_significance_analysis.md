# P2 Seed-Significance and Ausgrid Hierarchical Analysis (v7)

Status: `public_data_benchmark_v7_seed_significance_ausgrid`. 10 seeds for the decision-relevant set (6 neural
HyG variants + MLP) on OPSD and SimBench (3 original + 7 new seeds, identical
protocol), plus the new Ausgrid solar-home hierarchical benchmark (hourly GC:
12 top-energy complete customers + 4 postcode-region
aggregates + system total; 2010-07..2013-06; 24h day-ahead; 10 seeds for the
HyG set and MLP/DLinear, 3 seeds for TCN/PatchTST/LSTM). Mann-Whitney U
two-sided with Holm correction per dataset/horizon on the dataset's primary
metric (OPSD: MAPE; SimBench/Ausgrid: normalized MAE).

## Verdict tables (proposed vs opponents)

### opsd_h1 (n_seeds=10, proposed mean `0.010689` std `0.000314`)

| opponent | role | mean opponent | proposed better? | p (Holm) | significant |
|---|---|---|---|---|---|
| Ablation-EqualNeighbors (neural) | ablation | 0.01063205 | False | 1 | False |
| Ablation-EuclideanGraph (neural) | ablation | 0.01064340 | False | 1 | False |
| Ablation-FixedCurvature (neural) | ablation | 0.01070693 | True | 1 | False |
| Ablation-NoCalendar (neural) | ablation | 0.01061739 | False | 1 | False |
| Ablation-TemporalOnly (neural) | ablation | 0.01098055 | True | 0.188177 | False |
| MLP | baseline | 0.01015548 | False | 0.0347722 | True |

### opsd_h24 (n_seeds=10, proposed mean `0.032345` std `0.000817`)

| opponent | role | mean opponent | proposed better? | p (Holm) | significant |
|---|---|---|---|---|---|
| Ablation-EqualNeighbors (neural) | ablation | 0.03246871 | True | 1 | False |
| Ablation-EuclideanGraph (neural) | ablation | 0.03225675 | False | 1 | False |
| Ablation-FixedCurvature (neural) | ablation | 0.03230191 | False | 1 | False |
| Ablation-NoCalendar (neural) | ablation | 0.03187295 | False | 0.484898 | False |
| Ablation-TemporalOnly (neural) | ablation | 0.03459125 | True | 0.00109603 | True |
| MLP | baseline | 0.03371542 | True | 0.00853125 | True |

### simbench_h1 (n_seeds=10, proposed mean `0.033349` std `0.000385`)

| opponent | role | mean opponent | proposed better? | p (Holm) | significant |
|---|---|---|---|---|---|
| Ablation-EqualNeighbors (neural) | ablation | 0.03346122 | True | 1 | False |
| Ablation-EuclideanGraph (neural) | ablation | 0.03342401 | True | 1 | False |
| Ablation-FixedCurvature (neural) | ablation | 0.03330872 | False | 1 | False |
| Ablation-NoCalendar (neural) | ablation | 0.03362727 | True | 0.702325 | False |
| Ablation-TemporalOnly (neural) | ablation | 0.03389225 | True | 0.270927 | False |
| MLP | baseline | 0.03338473 | True | 1 | False |

### simbench_h24 (n_seeds=10, proposed mean `0.060662` std `0.002064`)

| opponent | role | mean opponent | proposed better? | p (Holm) | significant |
|---|---|---|---|---|---|
| Ablation-EqualNeighbors (neural) | ablation | 0.06017905 | False | 1 | False |
| Ablation-EuclideanGraph (neural) | ablation | 0.06085380 | True | 1 | False |
| Ablation-FixedCurvature (neural) | ablation | 0.06060326 | False | 1 | False |
| Ablation-NoCalendar (neural) | ablation | 0.06211447 | True | 1 | False |
| Ablation-TemporalOnly (neural) | ablation | 0.06019859 | False | 1 | False |
| MLP | baseline | 0.05859118 | False | 0.0841157 | False |

### ausgrid_h24 (n_seeds=10, proposed mean `0.323613` std `0.006152`)

| opponent | role | mean opponent | proposed better? | p (Holm) | significant |
|---|---|---|---|---|---|
| Ablation-EqualNeighbors (neural) | ablation | 0.32216576 | False | 1 | False |
| Ablation-EuclideanGraph (neural) | ablation | 0.32272363 | False | 1 | False |
| Ablation-FixedCurvature (neural) | ablation | 0.32203797 | False | 1 | False |
| Ablation-NoCalendar (neural) | ablation | 0.32994356 | True | 0.848572 | False |
| Ablation-TemporalOnly (neural) | ablation | 0.32415393 | True | 1 | False |
| DLinear | baseline | 0.31324440 | False | 0.00439639 | True |
| LSTM | baseline | 0.35270924 | True | 0.0629371 | False |
| MLP | baseline | 0.32283336 | False | 1 | False |
| PatchTST-lite | baseline | 0.31462955 | False | 0.111888 | False |
| TCN | baseline | 0.31677132 | False | 0.965035 | False |

## Component verdict

- **opsd_h1**: significant wins: none; significant losses: MLP; not separable: Ablation-EqualNeighbors (neural), Ablation-EuclideanGraph (neural), Ablation-FixedCurvature (neural), Ablation-NoCalendar (neural), Ablation-TemporalOnly (neural)
- **opsd_h24**: significant wins: Ablation-TemporalOnly (neural), MLP; significant losses: none; not separable: Ablation-EqualNeighbors (neural), Ablation-EuclideanGraph (neural), Ablation-FixedCurvature (neural), Ablation-NoCalendar (neural)
- **simbench_h1**: significant wins: none; significant losses: none; not separable: Ablation-EqualNeighbors (neural), Ablation-EuclideanGraph (neural), Ablation-FixedCurvature (neural), Ablation-NoCalendar (neural), Ablation-TemporalOnly (neural), MLP
- **simbench_h24**: significant wins: none; significant losses: none; not separable: Ablation-EqualNeighbors (neural), Ablation-EuclideanGraph (neural), Ablation-FixedCurvature (neural), Ablation-NoCalendar (neural), Ablation-TemporalOnly (neural), MLP
- **ausgrid_h24**: significant wins: none; significant losses: DLinear; not separable: Ablation-EqualNeighbors (neural), Ablation-EuclideanGraph (neural), Ablation-FixedCurvature (neural), Ablation-NoCalendar (neural), Ablation-TemporalOnly (neural), LSTM, MLP, PatchTST-lite, TCN

## Interpretation Boundary

Every model in a comparison shares the training regime, splits, and test
sets. OPSD/SimBench rows merge the original v5/v6 3-seed runs with 7 new
seeds under an identical code path. Ausgrid uses lazy window gathering,
stride 6, 10 epochs (documented budget). If the
hyperbolic components are still not separable from Euclidean/equal-weight
ablations here, the manuscript's contribution claim must be downgraded
accordingly (cross-series attention rather than hyperbolic geometry).
