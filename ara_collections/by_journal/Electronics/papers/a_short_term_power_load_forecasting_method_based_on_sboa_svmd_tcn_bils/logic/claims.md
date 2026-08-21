# Claims

## C01: Optimizing a variational decomposition's compactness parameter toward minimum component-entropy yields more predictable sub-sequences
- **Statement**: When the mode-compactness parameter of a successive variational decomposition is chosen by a global optimizer that minimizes the permutation entropy of the resulting components — rather than fixed to an empirical value — the decomposition settles at a compactness that is neither over-dispersed nor over-concentrated, producing sub-sequences of lower complexity and higher predictability while avoiding mode mixing.
- **Conditions**: Non-stationary electricity load; compactness is the dominant SVMD parameter (others empirical); predictability judged by permutation entropy as proxy (Assumption A1). Untested boundary: whether the entropy-minimizing compactness also minimizes downstream forecast error is assumed, not directly optimized; only three compactness values were tabulated and one optimized value reported on one dataset.
- **Sources**: ["0.1245 ← evidence/tables/table2.md «19,990.25 (Optimized) | 0.1245» [result]", "19,990.25 ← evidence/tables/table1.md «compactness of mode | 19,990.25 |» [input]"]
- **Status**: supported
- **Falsification criteria**: Exhibit a compactness value (or an optimizer configuration) whose decomposed components have lower permutation entropy than the reported optimum yet the optimum still claimed, or show that lower component permutation entropy does not correspond to lower forecast error on held-out load.
- **Proof**: [E01]
- **Evidence basis**: Table 2 shows permutation entropy falling from 0.3462 (compactness 15,000) and 0.2857 (17,500) to 0.1245 at the optimized 19,990.25; Figure 9 shows the four resulting IMFs have clear, separated frequency structure. Numbers live in the evidence layer.
- **Tags**: decomposition, SVMD, permutation-entropy, optimization

## C02: Variational successive decomposition separates load frequency structure more cleanly than EMD-family decompositions, lowering downstream forecast error
- **Statement**: For non-stationary load, a variational successive decomposition front-end yields components with clearer periodicity and less mode mixing than empirical-mode-decomposition-family front-ends (noise-assisted EMD variants); because mode mixing produces components lacking distinct features and because adding more components compounds error, the cleaner separation propagates into lower forecast error when the same downstream forecaster is held fixed.
- **Conditions**: Same TCN-BiLSTM forecaster and evaluation protocol across decomposition methods; baselines = CEEMDAN and ICEEMDAN with the fixed settings of Table 3; single-region day-ahead load. Untested boundary: only two EMD-family baselines and one dataset; the mechanism is attributed to mode mixing but not independently measured for the baselines.
- **Sources**: ["219.7098 ← evidence/tables/table4.md «SBOA-SVMD-TCN-BiLSTM | 219.7098 | 309.2698 | 0.9273» [result]"]
- **Status**: supported
- **Falsification criteria**: On comparable load data with the forecaster held fixed, an EMD-family decomposition achieves equal-or-lower MAE/RMSE than the variational successive decomposition, or the variational method is shown to also suffer mode mixing on this data.
- **Proof**: [E02]
- **Evidence basis**: Table 4 (SVMD lowest MAE/RMSE, highest R² vs CEEMDAN/ICEEMDAN; stated reductions 29.01%/23.16% MAE, 17.76%/16.32% RMSE); Figure 11 shows the SVMD curve closest to measured.
- **Dependencies**: C01
- **Tags**: decomposition, SVMD, CEEMDAN, mode-mixing, baseline-comparison

## C03: A decompose-then-forecast pipeline outperforms forecasting the raw series with the same model
- **Statement**: Splitting a non-stationary load series into scale-separated components before forecasting, and reconstructing the component forecasts, gives lower error than applying the identical forecaster directly to the (pre-processed) raw series, because each component presents a simpler, more regular signal to the model than the superposed original.
- **Conditions**: Identical TCN-BiLSTM forecaster in both arms; the only difference is presence/absence of the SBOA-SVMD front-end; single-region day-ahead load. Untested boundary: benefit shown for this decomposition+forecaster pair; not isolated from the specific optimizer.
- **Sources**: ["337.4591 ← evidence/tables/table5.md «TCN-BiLSTM | 337.4591 | 464.9645 | 0.8346» [result]"]
- **Status**: supported
- **Falsification criteria**: A dataset/forecaster where adding the decomposition front-end leaves error unchanged or worse than the raw-input model.
- **Proof**: [E03]
- **Evidence basis**: Table 5 — proposed model vs plain TCN-BiLSTM (MAE −34.89%, RMSE −33.49%, R² +11.1%); Figure 12 shows the decomposition arm hugging measured load, the raw arm under-predicting peaks.
- **Dependencies**: C01, C02
- **Tags**: decomposition, ablation, necessity

## C04: Prepending convolutional multi-scale feature extraction to a bidirectional recurrent forecaster beats the recurrent net alone and shallow learners
- **Statement**: On decomposed load components, feeding a dilated-causal-convolution feature extractor's output into a bidirectional recurrent network captures multi-scale local structure that a bidirectional recurrent net cannot extract on its own, so the combined forecaster is more accurate and stable than the recurrent net alone and markedly more accurate than shallow/unidirectional learners; the gain shrinks as the standalone forecaster already models more temporal context.
- **Conditions**: All forecasters consume the same SBOA-SVMD IMFs; compared against ELM, LSTM, BiLSTM; per-component then reconstructed. Untested boundary: single dataset; "stability" argued from curve fit, not a variance statistic.
- **Sources**: ["47.8% ← evidence/tables/table6.md «MAE reduced 47.8%, 32.8%, 11.5%» [result]", "11.5% ← evidence/tables/table6.md «MAE reduced 47.8%, 32.8%, 11.5%» [result]"]
- **Status**: supported
- **Falsification criteria**: On comparable decomposed load, adding the convolutional front-end to the bidirectional recurrent forecaster fails to reduce error versus the recurrent forecaster alone, or a shallow learner matches it.
- **Proof**: [E04]
- **Evidence basis**: Table 6 orders LSTM < ELM < BiLSTM < TCN-BiLSTM on MAE/RMSE/R²; the smallest improvement (11.5% MAE, 11.3% RMSE) is over BiLSTM (the strongest baseline), the largest over LSTM — consistent with the "gain shrinks as baseline captures more context" claim. Figure 13 shows TCN-BiLSTM tracking peaks/troughs best.
- **Dependencies**: C03
- **Tags**: TCN, BiLSTM, hybrid-model, ablation

## C05: The hybrid model's ranking advantage is season- and peak-time robust, but its absolute error tracks the load regime
- **Statement**: The accuracy ordering favoring the hybrid model holds across all four seasons and intra-day peak windows, yet the absolute error and the size of the margin over baselines are governed by the load regime — more volatile regimes (summer, winter; afternoon peaks) enlarge every model's error and compress or expand the margin — so a single aggregate error understates the model's regime dependence.
- **Conditions**: Per-season 5:1 train/test split; a representative day per season; peak windows 07:00–09:00 and 13:00–15:00. Untested boundary: one day per season, one region; seasons defined by the paper's month grouping.
- **Sources**: ["116.23 ← evidence/tables/table8.md «TCN-BiLSTM | 116.23 | 132.33 | 238.88 | 275.29 | 157.05 | 191.63 | 218.11 | 298.60 |» [result]"]
- **Status**: supported
- **Falsification criteria**: A season or peak window in which a baseline attains lower MAE/RMSE than the hybrid model, or in which the hybrid's error is invariant to regime volatility.
- **Proof**: [E05, E06]
- **Evidence basis**: Table 8 (hybrid lowest per-season MAE/RMSE; averages improved 63.2%/47.97%/41% MAE over baselines) with error highest in summer/winter; Table 9 (peak-period errors rise 13:00–15:00, winter most); Figure 14 (proposed model's errors concentrate within ±200 MW in spring/autumn, spread in summer/winter).
- **Dependencies**: C04
- **Tags**: seasonality, robustness, peak-load, error-distribution

## C06: Component-wise decomposition ensembles multiply training cost but keep inference latency negligible, so they remain deployable
- **Statement**: Training a separate forecaster per decomposed component multiplies training time roughly with the number of components, but because prediction is a single forward pass per component the aggregate inference latency stays orders of magnitude below training time; hence an offline-training / online-prediction deployment of a decomposition ensemble is not latency-bound in operation.
- **Conditions**: Four IMFs, four TCN-BiLSTM sub-models on the stated hardware; day-ahead operational use. Untested boundary: measured on one machine/dataset; scaling to many more components not tested.
- **Sources**: ["355.17 ← evidence/tables/table7.md «total training time 355.17 s; total testing time 0.89 s» [result]", "0.89 ← evidence/tables/table7.md «total training time 355.17 s; total testing time 0.89 s» [result]"]
- **Status**: supported
- **Falsification criteria**: A deployment where per-component inference latency becomes comparable to training time or violates the day-ahead timing budget.
- **Proof**: [E07]
- **Evidence basis**: Table 7 per-IMF training (84–99 s) vs testing (0.07–0.59 s) times; text totals 355.17 s train / 0.89 s test.
- **Tags**: efficiency, deployment, training-time

## C07: Optimizer choice materially affects decomposition-parameter tuning; late-iteration stability distinguishes metaheuristics on this landscape
- **Statement**: On the SVMD compactness-tuning landscape (objective = minimum component permutation entropy), the choice of population-based optimizer materially changes the attained optimum: an optimizer combining differential-evolution search, Brownian-motion exploitation and Lévy-flight attack phases reaches a lower, more stable late-stage objective than sparrow-search or grey-wolf optimizers, which either fluctuate or stagnate above it — so convergence stability, not just early descent speed, governs tuning quality.
- **Conditions**: Equal population size and iteration budget across optimizers; identical objective and SVMD setup; single tuning problem. Untested boundary: three optimizers, one landscape, one dataset; SBOA and GWO plotted on separate y-axes so absolute gaps are qualitative.
- **Sources**: []
- **Status**: supported
- **Falsification criteria**: Under matched budget on this tuning problem, SSA or GWO reaches an equal-or-lower stable objective than SBOA, or SBOA is shown to be unstable / stuck in local optima in late iterations.
- **Proof**: [E08]
- **Evidence basis**: Figure 10 — SBOA converges to the lowest fitness and stays stable; SSA descends fast then fluctuates and converges slower; GWO stays flat and never reaches the SBOA/SSA level.
- **Dependencies**: C01
- **Tags**: metaheuristic, SBOA, SSA, GWO, convergence
