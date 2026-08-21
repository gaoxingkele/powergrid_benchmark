# Claims

## C01: Each added modeling stage — spatial graph convolution, then boosting, then uncertainty-aware weighting — removes a distinct, non-overlapping source of error on a temporal load forecaster
- **Statement**: When a bidirectional temporal forecaster is progressively augmented — first by prepending a graph-convolutional spatial encoder over inter-feature dependencies, then by boosting an ensemble of such encoders, then by attenuating ensemble weights with a per-learner uncertainty estimate — forecast error decreases monotonically at every stage, indicating the three mechanisms address complementary rather than redundant error sources.
- **Conditions**: Multivariate weather-driven hourly load, static feature graph, ensemble of ten base learners, evaluated on both a one-day and a one-week horizon; the monotone ordering is observed for one regional dataset and is not shown to hold across datasets or for arbitrary stage orderings.
- **Sources**: ["10 ← paper §2.4 (local_pdf p.8; mirrored in src/configs/model.md, src/environment.md) «The AdaBoost framework is introduced to integrate 10 such weak learners» [input]"]
- **Status**: supported
- **Falsification criteria**: On comparable weather-load data, adding the GCN spatial stage or the boosting stage or the uncertainty-weighting stage leaves MAE/MAPE/RMSE unchanged or worsens them on either horizon — i.e., a stage that contributes no separable error reduction.
- **Proof**: [E01, E02]
- **Evidence basis**: Table 4 shows MAE/MAPE/RMSE strictly decreasing across BiLSTM → GCN-BiLSTM → GCN-BiLSTM-Adaboost → proposed on both horizons; Figures 9–10 show the proposed model below all single-model baselines on every metric. Numbers live in `evidence/tables/table4.md`, `evidence/figures/figure9.md`, `evidence/figures/figure10.md`.
- **Dependencies**: none
- **Tags**: ablation, spatiotemporal, ensemble, hybrid-model

## C02: Down-weighting high-variance ensemble members preserves accuracy precisely where a static ensemble fails — at abrupt load transitions
- **Statement**: Scaling each base learner's ensemble weight inversely with its Monte-Carlo-Dropout predictive variance concentrates trust on locally stable learners, so the ensemble retains accuracy at load turning points and abrupt (e.g., weather-induced) transitions where uniformly or error-only weighted models degrade.
- **Conditions**: Non-stationary load segments containing turning points/mutations; uncertainty measured as sampling variance over stochastic dropout passes; demonstrated qualitatively at daily turning points and via a stagewise error drop, not quantified as an isolated variance-weighting ablation against a matched error-only-weighted ensemble.
- **Sources**: ["100 ← paper §2.5 (local_pdf p.10; mirrored in src/configs/model.md, src/environment.md) «each GCN-BiLSTM weak learner generates 100 stochastic predictions yn through Monte Carlo Dropout sampling» [input]"]
- **Status**: supported
- **Falsification criteria**: At load turning points, an ensemble whose weights ignore per-learner variance matches or beats the uncertainty-attenuated ensemble, or the attenuated ensemble shows no smaller error than the error-only-weighted (GCN-BiLSTM-Adaboost) variant during mutation windows.
- **Proof**: [E01, E04]
- **Evidence basis**: Figure 11 shows the proposed model tracking real load at daily turning points while BiLSTM/GCN-BiLSTM/GCN-BiLSTM-Adaboost deviate; Table 4 shows the proposed model's day/week errors below the GCN-BiLSTM-Adaboost (error-only) variant. See `evidence/figures/figure11.md`, `evidence/tables/table4.md`.
- **Dependencies**: C01
- **Tags**: robustness, uncertainty-weighting, Monte-Carlo-Dropout, non-stationarity

## C03: Building the GCN adjacency from a rank-correlation threshold beats similarity-, learning-, and information-based graph builders because it admits only monotone physical dependencies
- **Statement**: Deriving the feature graph from a Spearman rank-correlation threshold selects edges that reflect genuine monotonic co-variation among weather factors, avoiding the spurious edges of raw-similarity (KNN) graphs, the overfitting of learned graphs, and the small-sample estimation bias of mutual-information graphs — and this cleaner spatial prior lowers downstream forecast error.
- **Conditions**: Static, training-free adjacency over ~8–9 weather/load features on one regional dataset; superiority shown only on a one-week horizon and only against KNN, learned-graph, and mutual-information baselines; edge threshold fixed at |ρ| ≥ 0.8.
- **Sources**: ["0.8 ← paper §2.1 (local_pdf p.4; mirrored in data/preprocessing.md) «a correlation coefficient exceeding 0.8 is defined as an edge (i.e., a connection weight of 1) between two features» [input]"]
- **Status**: supported
- **Falsification criteria**: On comparable multivariate weather-load data, a KNN, learned, or mutual-information adjacency produces equal or lower MAE/MAPE/RMSE than the Spearman-threshold adjacency with the same downstream model.
- **Proof**: [E03]
- **Evidence basis**: Table 2 reports Spearman below KNN, learned graphs, and mutual information on MAE/MAPE/RMSE at the one-week horizon. See `evidence/tables/table2.md`.
- **Dependencies**: none
- **Tags**: graph-construction, Spearman, adjacency, ablation

## C04: Boosting only on above-threshold-error samples steers capacity toward hard/mutation cases without amplifying noise
- **Statement**: Restricting AdaBoost's sample re-weighting to instances whose error exceeds a fixed tolerance (rather than re-weighting all misclassified samples) makes successive weak learners specialize on the rare hard-to-predict regimes — peaks and load mutations — while leaving near-correct, possibly-noisy samples untouched, trading a tunable threshold for reduced sensitivity to non-significant fluctuations.
- **Conditions**: Error tolerance is a single fixed absolute threshold on the normalized scale that the paper states must be re-tuned per application; the benefit is argued mechanistically and reflected in the ensemble's turning-point behavior, but the threshold itself is not swept, so its optimum and sensitivity are untested.
- **Sources**: ["0.3 ← paper §2.4 (local_pdf p.9; mirrored in src/execution/adaboost_bayesian_weighting.py) «this study only increases the weights of samples with prediction errors exceeding 0.3» [input]"]
- **Status**: hypothesis
- **Falsification criteria**: An ensemble that re-weights all misclassified samples (traditional AdaBoost) matches the selective-threshold variant's accuracy on hard/mutation windows, or varying the threshold shows no regime where selective re-weighting helps.
- **Proof**: [E01, E04]
- **Evidence basis**: §2.4 states the modification and its rationale; Figure 11 and Table 4 show improved turning-point tracking of the full model over the plain-Adaboost variant. Threshold is never ablated (dead end noted in trace). See `evidence/figures/figure11.md`.
- **Dependencies**: C02
- **Tags**: AdaBoost-modification, selective-reweighting, hard-samples, hypothesis

## C05: Monte Carlo Dropout turns the point forecaster into a risk-quantifying forecaster by emitting a calibrated predictive interval alongside the mean
- **Statement**: Repeated stochastic dropout passes at inference approximate a posterior predictive distribution, so the same ensemble that produces a point load forecast also produces a 95% predictive interval — converting the model output from a single number into a risk-quantification signal usable for dispatch, at a sampling cost that scales linearly with the number of passes and learners.
- **Conditions**: Uncertainty is defined as the sampling variance of dropout passes (an approximate, not exact, Bayesian posterior); interval coverage is asserted from the construction, not empirically calibration-tested; runtime cost grows with samples × learners.
- **Sources**: ["100 ← paper §2.5 (local_pdf p.10; mirrored in src/configs/model.md, src/environment.md) «each GCN-BiLSTM weak learner generates 100 stochastic predictions yn through Monte Carlo Dropout sampling» [input]", "95% ← paper §4.4 (local_pdf p.16; mirrored in evidence/figures/figure12.md) «under repeated sampling conditions, the true value has a 95% probability of falling within this interval range» [input]"]
- **Status**: supported
- **Falsification criteria**: Empirical coverage of the reported 95% interval departs materially from 95% on held-out load, or the dropout-sampling variance shows no correspondence to realized error — i.e., the band does not bound true values at its stated rate.
- **Proof**: [E05]
- **Evidence basis**: Figure 12 overlays the predicted mean, actual load, and a shaded 95% confidence interval over a one-week horizon; §2.5/§4.4 define the interval and its intended statistical meaning; §4.4 reports a full-run wall time. See `evidence/figures/figure12.md`.
- **Dependencies**: none
- **Tags**: uncertainty-quantification, Monte-Carlo-Dropout, predictive-interval, reliability
