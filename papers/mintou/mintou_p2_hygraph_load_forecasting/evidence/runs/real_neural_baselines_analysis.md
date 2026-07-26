# Neural Baseline Analysis - P2 HyG-LoadFormer

Status: `public_data_benchmark_v5_neural_baselines`. Real neural baselines (MLP, LSTM, TCN, DLinear,
PatchTST-lite) trained on exactly the same data, 70% temporal split, and full
test sets as the stdlib benchmark; per-series z-normalization, Adam/MSE,
temporal early stopping, train-sample stride 3 (test never strided),
3 seeds per model with the median-MAPE seed reported and per-seed
variance preserved in `real_*_neural_results.csv`.

## OPSD (ranking metric: MAPE)

### Horizon 1h

- HyG-LoadFormer MAPE: `0.02244670` (rank 7/18)
- Best neural baseline: `MLP` with `0.00995841` (seed-std MAPE `0.00017252`)
- HyG-LoadFormer margin over best neural baseline: `-55.64%` (neural_baseline_beats_proposed)

| rank | method | family | MAPE | normalized MAE |
|---|---|---|---|---|
| 1 | MLP | neural | 0.00995841 | 0.00397258 |
| 2 | PatchTST-lite | neural | 0.01119052 | 0.00455152 |
| 3 | TCN | neural | 0.01182458 | 0.00481027 |
| 4 | DLinear | neural | 0.01251062 | 0.00494342 |
| 5 | Ablation-NoCalendar | stdlib | 0.02068559 | 0.00842894 |
| 6 | LSTM | neural | 0.02172846 | 0.00912920 |
| 7 | HyG-LoadFormer | stdlib | 0.02244670 | 0.00887378 |
| 8 | Ablation-FixedCurvature | stdlib | 0.02248453 | 0.00888278 |
| 9 | Euclidean-GCN Ridge | stdlib | 0.02250389 | 0.00888464 |
| 10 | GCN-Temporal Ridge | stdlib | 0.02250389 | 0.00888464 |

### Horizon 24h

- HyG-LoadFormer MAPE: `0.03972575` (rank 4/18)
- Best neural baseline: `MLP` with `0.03394443` (seed-std MAPE `0.00058834`)
- HyG-LoadFormer margin over best neural baseline: `-14.55%` (neural_baseline_beats_proposed)

| rank | method | family | MAPE | normalized MAE |
|---|---|---|---|---|
| 1 | MLP | neural | 0.03394443 | 0.01375767 |
| 2 | TCN | neural | 0.03611025 | 0.01470160 |
| 3 | PatchTST-lite | neural | 0.03777387 | 0.01520306 |
| 4 | HyG-LoadFormer | stdlib | 0.03972575 | 0.01621211 |
| 5 | DLinear | neural | 0.04084048 | 0.01700381 |
| 6 | LSTM | neural | 0.05273086 | 0.02121039 |
| 7 | Weekly-168h | stdlib | 0.05632632 | 0.02405159 |
| 8 | Ablation-FixedCurvature | stdlib | 0.06915059 | 0.02588285 |
| 9 | AR-Calendar Ridge | stdlib | 0.06925376 | 0.02598398 |
| 10 | Ablation-TemporalOnly | stdlib | 0.06925376 | 0.02598398 |

## SIMBENCH (ranking metric: normalized MAE)

### Horizon 1h

- HyG-LoadFormer normalized MAE: `0.04316202` (rank 6/18)
- Best neural baseline: `MLP` with `0.03403137` (seed-std MAPE `0.01140072`)
- HyG-LoadFormer margin over best neural baseline: `-21.15%` (neural_baseline_beats_proposed)

| rank | method | family | MAPE | normalized MAE |
|---|---|---|---|---|
| 1 | MLP | neural | 0.17957017 | 0.03403137 |
| 2 | TCN | neural | 0.22451650 | 0.03811722 |
| 3 | PatchTST-lite | neural | 0.27392203 | 0.04124449 |
| 4 | DLinear | neural | 0.28068178 | 0.04133336 |
| 5 | Persistence | stdlib | 0.14812336 | 0.04316202 |
| 6 | HyG-LoadFormer | stdlib | 0.14812336 | 0.04316202 |
| 7 | Ablation-NoCalendar | stdlib | 0.19855467 | 0.04331806 |
| 8 | Ablation-FixedCurvature | stdlib | 0.23474454 | 0.04471369 |
| 9 | Euclidean-GCN Ridge | stdlib | 0.23451101 | 0.04471764 |
| 10 | GCN-Temporal Ridge | stdlib | 0.23451101 | 0.04471764 |

### Horizon 24h

- HyG-LoadFormer normalized MAE: `0.07822078` (rank 5/18)
- Best neural baseline: `MLP` with `0.05979284` (seed-std MAPE `0.01529006`)
- HyG-LoadFormer margin over best neural baseline: `-23.56%` (neural_baseline_beats_proposed)

| rank | method | family | MAPE | normalized MAE |
|---|---|---|---|---|
| 1 | MLP | neural | 0.34851375 | 0.05979284 |
| 2 | TCN | neural | 0.40324111 | 0.06325750 |
| 3 | PatchTST-lite | neural | 0.44478652 | 0.06649389 |
| 4 | DLinear | neural | 0.53373145 | 0.07820647 |
| 5 | HyG-LoadFormer | stdlib | 0.48224558 | 0.07822078 |
| 6 | Persistence | stdlib | 0.46003461 | 0.08103131 |
| 7 | Weekly-168h | stdlib | 0.41451949 | 0.09253661 |
| 8 | Ablation-NoCalendar | stdlib | 0.69330349 | 0.09513336 |
| 9 | AR-Calendar Ridge | stdlib | 0.69531841 | 0.09658434 |
| 10 | Ablation-TemporalOnly | stdlib | 0.69531841 | 0.09658434 |

## Interpretation Boundary

Neural baselines are compact CPU-trained models (bounded epochs, strided
training samples); a GPU-tuned version of each could be somewhat stronger, and
this is stated as a limitation rather than hidden. Test sets are identical to
the stdlib benchmark rows, so the combined leaderboards are directly
comparable. Rolling-split neural evidence is limited to what these budgets
allow and remains an open extension.

## Consequence for the manuscript claim

If HyG-LoadFormer (currently a ridge-based implementation) does not beat the
neural baselines on the 24h day-ahead task, the manuscript must either (a)
upgrade the proposed method to a genuine neural implementation before claiming
state-of-the-art-adjacent performance, or (b) reframe the contribution as an
interpretable lightweight method and report the neural baselines honestly as
an upper reference. Silent omission is not an option.
