# HyG-LoadFormer Neural Upgrade Analysis - P2

Status: `public_data_benchmark_v6_hyg_neural`. The proposed method is now a genuine neural
implementation (Poincare-ball series embeddings, target-adaptive curvature
hyperbolic graph attention, shared temporal MLP encoder at MLP-baseline
parameter budget). Protocol identical to the neural baselines: same splits,
full test sets, Adam/MSE, temporal early stopping, 3 seeds
(median-MAPE seed reported; per-seed rows preserved in
`real_*_hyg_neural_results.csv`). The five ablations are real mechanism
switches on this model. The previous ridge implementation stays in the
leaderboards as `HyG-LoadFormer` (stdlib family) for transparency.

## OPSD (ranking metric: MAPE)

### Horizon 1h

- HyG-LoadFormer (neural) MAPE: `0.01054869` (rank 3/24, seed-std MAPE `0.00013111`)
- Best baseline: `MLP` (neural) with `0.00995841`
- Margin over best baseline: `-5.60%` (baseline_beats_proposed)
- Best neural ablation: `Ablation-EqualNeighbors (neural)` with `0.01048105` (margin `-0.64%`)

| rank | method | family | MAPE | normalized MAE |
|---|---|---|---|---|
| 1 | MLP | neural | 0.00995841 | 0.00397258 |
| 2 | Ablation-EqualNeighbors (neural) | neural | 0.01048105 | 0.00417275 |
| 3 | HyG-LoadFormer (neural) | neural | 0.01054869 | 0.00425617 |
| 4 | Ablation-FixedCurvature (neural) | neural | 0.01056156 | 0.00419935 |
| 5 | Ablation-EuclideanGraph (neural) | neural | 0.01058669 | 0.00421001 |
| 6 | Ablation-NoCalendar (neural) | neural | 0.01062862 | 0.00424401 |
| 7 | Ablation-TemporalOnly (neural) | neural | 0.01116096 | 0.00449667 |
| 8 | PatchTST-lite | neural | 0.01119052 | 0.00455152 |
| 9 | TCN | neural | 0.01182458 | 0.00481027 |
| 10 | DLinear | neural | 0.01251062 | 0.00494342 |
| 11 | Ablation-NoCalendar | stdlib | 0.02068559 | 0.00842894 |
| 12 | LSTM | neural | 0.02172846 | 0.00912920 |

### Horizon 24h

- HyG-LoadFormer (neural) MAPE: `0.03326563` (rank 5/24, seed-std MAPE `0.00149816`)
- Best baseline: `MLP` (neural) with `0.03394443`
- Margin over best baseline: `2.04%` (proposed_beats_all_baselines)
- Best neural ablation: `Ablation-NoCalendar (neural)` with `0.03157770` (margin `-5.07%`)

| rank | method | family | MAPE | normalized MAE |
|---|---|---|---|---|
| 1 | Ablation-NoCalendar (neural) | neural | 0.03157770 | 0.01258442 |
| 2 | Ablation-EqualNeighbors (neural) | neural | 0.03262645 | 0.01321988 |
| 3 | Ablation-FixedCurvature (neural) | neural | 0.03290447 | 0.01334890 |
| 4 | Ablation-EuclideanGraph (neural) | neural | 0.03295993 | 0.01330470 |
| 5 | HyG-LoadFormer (neural) | neural | 0.03326563 | 0.01346076 |
| 6 | MLP | neural | 0.03394443 | 0.01375767 |
| 7 | Ablation-TemporalOnly (neural) | neural | 0.03453514 | 0.01408967 |
| 8 | TCN | neural | 0.03611025 | 0.01470160 |
| 9 | PatchTST-lite | neural | 0.03777387 | 0.01520306 |
| 10 | HyG-LoadFormer | stdlib | 0.03972575 | 0.01621211 |
| 11 | DLinear | neural | 0.04084048 | 0.01700381 |
| 12 | LSTM | neural | 0.05273086 | 0.02121039 |

## SIMBENCH (ranking metric: normalized MAE)

### Horizon 1h

- HyG-LoadFormer (neural) normalized MAE: `0.03325591` (rank 1/24, seed-std MAPE `0.00242133`)
- Best baseline: `MLP` (neural) with `0.03403137`
- Margin over best baseline: `2.33%` (proposed_beats_all_baselines)
- Best neural ablation: `Ablation-EuclideanGraph (neural)` with `0.03326713` (margin `0.03%`)

| rank | method | family | MAPE | normalized MAE |
|---|---|---|---|---|
| 1 | HyG-LoadFormer (neural) | neural | 0.17526892 | 0.03325591 |
| 2 | Ablation-EuclideanGraph (neural) | neural | 0.17356467 | 0.03326713 |
| 3 | Ablation-FixedCurvature (neural) | neural | 0.17493626 | 0.03330374 |
| 4 | Ablation-EqualNeighbors (neural) | neural | 0.17388739 | 0.03338756 |
| 5 | Ablation-NoCalendar (neural) | neural | 0.17550518 | 0.03341392 |
| 6 | MLP | neural | 0.17957017 | 0.03403137 |
| 7 | Ablation-TemporalOnly (neural) | neural | 0.18497825 | 0.03492706 |
| 8 | TCN | neural | 0.22451650 | 0.03811722 |
| 9 | PatchTST-lite | neural | 0.27392203 | 0.04124449 |
| 10 | DLinear | neural | 0.28068178 | 0.04133336 |
| 11 | Persistence | stdlib | 0.14812336 | 0.04316202 |
| 12 | HyG-LoadFormer | stdlib | 0.14812336 | 0.04316202 |

### Horizon 24h

- HyG-LoadFormer (neural) normalized MAE: `0.05853985` (rank 2/24, seed-std MAPE `0.02458132`)
- Best baseline: `MLP` (neural) with `0.05979284`
- Margin over best baseline: `2.14%` (proposed_beats_all_baselines)
- Best neural ablation: `Ablation-TemporalOnly (neural)` with `0.05745835` (margin `-1.85%`)

| rank | method | family | MAPE | normalized MAE |
|---|---|---|---|---|
| 1 | Ablation-TemporalOnly (neural) | neural | 0.34509578 | 0.05745835 |
| 2 | HyG-LoadFormer (neural) | neural | 0.35695735 | 0.05853985 |
| 3 | Ablation-FixedCurvature (neural) | neural | 0.36123129 | 0.05864915 |
| 4 | Ablation-EqualNeighbors (neural) | neural | 0.35966381 | 0.05871606 |
| 5 | Ablation-NoCalendar (neural) | neural | 0.36723236 | 0.05964616 |
| 6 | MLP | neural | 0.34851375 | 0.05979284 |
| 7 | Ablation-EuclideanGraph (neural) | neural | 0.39369412 | 0.06317142 |
| 8 | TCN | neural | 0.40324111 | 0.06325750 |
| 9 | PatchTST-lite | neural | 0.44478652 | 0.06649389 |
| 10 | DLinear | neural | 0.53373145 | 0.07820647 |
| 11 | HyG-LoadFormer | stdlib | 0.48224558 | 0.07822078 |
| 12 | Persistence | stdlib | 0.46003461 | 0.08103131 |

## Interpretation Boundary

All neural models (proposed, ablations, baselines) share the same CPU training
budget class, optimizer, early-stopping rule, and test sets, so rankings are
internally fair; absolute numbers are not GPU-tuned SOTA. Per-seed variance is
preserved. The ridge-based rows remain visible as the stdlib family.
