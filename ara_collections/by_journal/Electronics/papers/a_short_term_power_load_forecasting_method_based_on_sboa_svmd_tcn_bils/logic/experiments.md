# Experiments

All experiments use the Belgian 2018 regional load dataset (35,040 points at 15-min sampling) unless a per-season split is stated. No exact numbers here — see evidence/ for values.

## E01: SVMD compactness optimization by minimum permutation entropy
- **Verifies**: C01
- **Evidence**: evidence/tables/table2.md, evidence/tables/table1.md, evidence/figures/figure9.md
- **Run**: SBOA optimizing SVMD maxAlpha (src/environment.md; method in logic/solution/algorithm.md). No released code.
- **Setup**:
  - Model: SVMD decomposition; SBOA optimizer (pop=30, max_iter=60 per Table 1)
  - Hardware: Intel Core i9-13900HX, 16 GB RAM, RTX 4070; MATLAB R2024a
  - Dataset: normalized Belgian load, 7 days × selected months across seasons (6720 points)
  - System: objective = minimum permutation entropy of decomposed components
- **Procedure**:
  1. For candidate compactness values, run SVMD and compute component permutation entropy.
  2. Let SBOA search compactness to minimize permutation entropy.
  3. Compare entropy at optimized vs non-optimized compactness; inspect the IMFs.
- **Metrics**: permutation entropy (dimensionless, 0–1); qualitative IMF frequency separation.
- **Expected outcome**:
  - The optimized compactness attains the lowest permutation entropy among tested values.
  - Decomposition yields distinct, non-mixed IMFs (trend + periodic + high-frequency).
- **Baselines**: non-optimized (empirical) compactness values.
- **Dependencies**: none

## E02: Decomposition-method comparison with a fixed forecaster
- **Verifies**: C02
- **Evidence**: evidence/tables/table4.md, evidence/figures/figure11.md, evidence/tables/table3.md
- **Run**: SBOA-SVMD vs CEEMDAN vs ICEEMDAN front-ends, each + TCN-BiLSTM.
- **Setup**:
  - Model: TCN-BiLSTM forecaster held fixed; decomposition front-end varied
  - Dataset: last week of the test set; a specific day compared in the figure
  - System: CEEMDAN/ICEEMDAN with Table 3 settings (Nstd 0.2, NR 100, MaxIter 1000, SNRFlag 2)
- **Procedure**:
  1. Decompose with each method; forecast each component with TCN-BiLSTM; reconstruct.
  2. Overlay forecast vs measured; compute error metrics.
- **Metrics**: MAE (MW), RMSE (MW), R².
- **Expected outcome**:
  - The variational successive decomposition gives the lowest MAE/RMSE and the forecast curve closest to measured.
- **Baselines**: CEEMDAN-TCN-BiLSTM, ICEEMDAN-TCN-BiLSTM.
- **Dependencies**: E01

## E03: With vs without decomposition (ablation of the SBOA-SVMD front-end)
- **Verifies**: C03
- **Evidence**: evidence/tables/table5.md, evidence/figures/figure12.md
- **Run**: SBOA-SVMD-TCN-BiLSTM vs plain TCN-BiLSTM (raw processed load input).
- **Setup**:
  - Model: identical TCN-BiLSTM; input = IMFs vs raw load
  - Dataset: last two weeks of the test set; a specific day compared
- **Procedure**:
  1. Train/predict with decomposed inputs; train/predict with raw inputs.
  2. Compare error metrics and forecast curves.
- **Metrics**: MAE (MW), RMSE (MW), R².
- **Expected outcome**:
  - The decomposition arm has materially lower MAE/RMSE and higher R².
- **Baselines**: plain TCN-BiLSTM.
- **Dependencies**: E01, E02

## E04: Forecaster comparison on the same decomposed inputs
- **Verifies**: C04
- **Evidence**: evidence/tables/table6.md, evidence/figures/figure13.md
- **Run**: ELM, LSTM, BiLSTM, TCN-BiLSTM each on SBOA-SVMD IMFs.
- **Setup**:
  - Model: four forecasters; TCN = 10 filters, size 2, 1 residual block, dropout 0.02; BiLSTM = 60 hidden units, 100 epochs, ReLU; Adam, lr 0.005 halved every 2 epochs
  - Dataset: test set; three randomly selected days per month shown in figure
- **Procedure**:
  1. Forecast each IMF with each model; reconstruct; compare to measured.
  2. Compute error metrics; inspect peak/trough tracking.
- **Metrics**: MAE (MW), RMSE (MW), R².
- **Expected outcome**:
  - Ordering LSTM < ELM < BiLSTM < TCN-BiLSTM; the hybrid best; smallest margin over BiLSTM.
- **Baselines**: ELM, LSTM, BiLSTM.
- **Dependencies**: E03

## E05: Seasonal accuracy comparison
- **Verifies**: C05
- **Evidence**: evidence/tables/table8.md, evidence/figures/figure14.md
- **Run**: four forecasters per season.
- **Setup**:
  - Model: LSTM, ELM, BiLSTM, TCN-BiLSTM
  - Dataset: each season split 5:1 train/test; one representative day per season
- **Procedure**:
  1. Train/test per season; compute per-season MAE/RMSE.
  2. Plot relative-error distributions per model per season.
- **Metrics**: MAE (MW), RMSE (MW); relative-error histograms.
- **Expected outcome**:
  - Hybrid lowest error every season; all models worse in summer/winter; hybrid's errors more concentrated at low magnitudes.
- **Baselines**: ELM, LSTM, BiLSTM.
- **Dependencies**: E04

## E06: Peak-period error analysis
- **Verifies**: C05
- **Evidence**: evidence/tables/table9.md
- **Run**: proposed model on peak windows.
- **Setup**:
  - Model: SBOA-SVMD-TCN-BiLSTM
  - Dataset: four selected days (one per season); windows 07:00–09:00 and 13:00–15:00
- **Procedure**:
  1. Compute MAE/RMSE within each peak window per day.
  2. Compare morning vs afternoon peak, across seasons.
- **Metrics**: MAE (MW), RMSE (MW).
- **Expected outcome**:
  - Morning-peak errors generally lower; afternoon-peak errors rise; winter highest.
- **Baselines**: none (single-model peak-behavior analysis).
- **Dependencies**: E05

## E07: Training/testing time measurement per IMF
- **Verifies**: C06
- **Evidence**: evidence/tables/table7.md
- **Run**: per-IMF TCN-BiLSTM timing.
- **Setup**:
  - Model: four TCN-BiLSTM sub-models (one per IMF)
  - Hardware: i9-13900HX, RTX 4070, MATLAB R2024a
- **Procedure**:
  1. Record training and testing wall-clock time per IMF; sum totals.
- **Metrics**: training time (s), testing time (s).
- **Expected outcome**:
  - Per-IMF and total testing time orders of magnitude below training time.
- **Baselines**: none.
- **Dependencies**: E04

## E08: Optimizer comparison (SBOA vs SSA vs GWO)
- **Verifies**: C07
- **Evidence**: evidence/figures/figure10.md
- **Run**: three metaheuristics on the SVMD compactness-tuning objective.
- **Setup**:
  - Model: SBOA, SSA, GWO
  - System: pop = 30, max 60 iterations each; objective = minimum permutation entropy
- **Procedure**:
  1. Run each optimizer; record fitness (permutation entropy) per iteration.
  2. Compare convergence value and late-stage stability.
- **Metrics**: fitness = permutation entropy; convergence/stability (qualitative).
- **Expected outcome**:
  - SBOA converges lowest and stays stable; SSA fluctuates; GWO stagnates above.
- **Baselines**: SSA, GWO.
- **Dependencies**: E01
