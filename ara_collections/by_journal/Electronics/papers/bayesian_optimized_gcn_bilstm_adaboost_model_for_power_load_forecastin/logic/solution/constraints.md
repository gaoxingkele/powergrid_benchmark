# Constraints — Boundary Conditions, Assumptions, Limitations

## Boundary conditions
- **Single regional dataset, one year**: hourly load + weather for one region, 1 Jan 2018 – 28 Dec 2018.
  No cross-region or multi-year generalization is tested.
- **Static graph**: the adjacency is built once from Spearman correlations over the whole series and is
  not updated over time (§5 limitation 1: may miss dynamic feature interactions during extreme events).
- **Fixed horizon primitive**: a 24-h window predicts one hour ahead; multi-step (one-day/one-week)
  curves are produced by rolling this one-step model.
- **Fixed ensemble size and sample count**: K = 10 weak learners, 100 MC-Dropout passes.

## Assumptions
- **A1** Spearman |ρ| ≥ 0.8 marks a genuine, physically meaningful monotonic edge (chosen over KNN /
  learned / MI graphs).
- **A2** MC-Dropout sampling variance is a valid reliability proxy for a weak learner.
- **A3** The 0.3 absolute error threshold separates hard/mutation samples from noise; the paper
  explicitly states it "should be adjusted based on error tolerance criteria and data characteristics
  in practical applications" (§2.4).
- **A4** Min-max normalization to [0,1] is adequate scaling; predictions are de-normalized (Eq 21).
- **A5** Mean-of-column imputation is acceptable for the missing values present.

## Known limitations (stated by the authors, §5)
1. **Static graph construction** may not capture dynamic feature interactions during extreme events.
2. **Computational overhead increases linearly** with the number of weak predictors (K = 10) and Monte
   Carlo samples (100).

### Additional limitations surfaced during extraction
3. **Terminology / method inconsistency**: the Introduction promises MCMC-based Bayesian *hyperparameter
   optimization*; the Method implements MC-Dropout *uncertainty quantification/weighting*. No MCMC search
   space or tuning procedure is reported. (See `algorithm.md` scope note.)
4. **Internal numeric inconsistency**: the Abstract reports the proposed model's MAE/MAPE/RMSE as
   1.86 / 3.13% / 2.26 — values that coincide with the *BiLSTM* "A Day" row of Table 4 (1.86 / 3.12% /
   2.26), whereas Table 4 lists the proposed model's "A Day" errors as 0.19 / 0.33% / 0.26. The abstract
   figures appear to be a transcription error; Table 4 is treated as authoritative here.
5. **Data anomaly in the correlation matrix**: Figure 2 shows a Wind Speed–Pressure Spearman value of
   1.17 (> 1), which is not a valid correlation coefficient and is unexplained.
6. **Feature-count ambiguity**: the input is described as "9 feature columns" (§2.1) and the model input
   tensor as 24×8 (Table 3); the GCN "nodes ... represent the 8-dimensional feature vectors" (§2.2).
   The load column is a target/feature depending on context; the paper does not fully reconcile 8 vs 9.
7. **No released code or public data**: data is restricted ("not publicly available due to privacy
   restrictions"); reproduction depends on printed equations only.
8. **Uncertainty band not calibration-tested**: the 95% interval is asserted from construction, not
   validated against empirical coverage.
9. **No threshold/ensemble-size/sample-count sensitivity study**: τ=0.3, K=10, T=100 are fixed, not swept.
10. **Missing CNN-BiLSTM baseline results**: §4 names CNN-BiLSTM among the comparison baselines,
   but Figures 9–10 contain no CNN-BiLSTM series and the §4.3 delta narrative gives only four
   baseline pairs (LSTM, CNN-LSTM, GCN-LSTM, GRU) — CNN-BiLSTM results are never reported. One
   narrative delta also disagrees slightly with the figure labels (§4.3 states the one-week RMSE
   improvement over CNN-LSTM as 1.27; Figure 10's labels give 1.75 − 0.43 = 1.32).

## Future work (authors, §5)
- Dynamic graph neural networks (DGNN) / temporal attention for an adaptive adjacency.
- Replace MC Dropout with Bayesian neural networks via Laplace approximation (no iterative sampling).
- Surrogate models (e.g., Gaussian processes) to approximate the weak-predictor posterior.
- Quantization-aware training to compress the ensemble for edge deployment.
- Multi-modal data fusion (e.g., grid topology maps) for robustness under complex weather.
