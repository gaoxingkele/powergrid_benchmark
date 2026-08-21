# Claims

## C01: Per-modality encoding with late fusion beats a single shared encoder for heterogeneous STLF
- **Statement**: In multi-source short-term load forecasting, routing each heterogeneous input modality through its own recurrent encoder and deferring their combination to a late convolutional fusion stage preserves modality-specific dynamics (strict periodicity, delayed weather response, trend-plus-noise) that a single shared encoder entangles; this independent-encode-then-fuse structure lowers forecast error relative to forcing all modalities through one input channel.
- **Conditions**: Demonstrated on two distribution-network datasets (Tétouan 2017; Electrician Cup) with three modalities — time codes, meteorology, historical load — and a two-layer Conv1D late-fusion head; the fusion improvement is observed as a consistent ranking (single-channel baselines < three-channel) rather than a proven universal law. Untested for other modality sets, multi-step horizons beyond next-day, or transfer to unseen grids.
- **Sources**: ["1.367% and 0.974% ← Abstract, p1 «its average absolute percentage error on the two datasets is reduced to 1.367% and 0.974%, respectively» [result]", "MAPE decreased by 0.566%, 0.465% and 0.104% ← §4(1), p11 «MAPE decreased by 0.566%, 0.465% and 0.104%, respectively» [result]", "MAPE decreased by 0.548%, 0.272%, and 0.109% ← §4(2), p12 «The MAPE decreased by 0.548%, 0.272%, and 0.109%, respectively» [result]"]
- **Status**: supported
- **Falsification criteria**: On a dataset whose modalities are near-homogeneous or only weakly heterogeneous, the multi-channel independent-encode design would show no error reduction (or a regression) versus a matched single-channel encoder with equal capacity and tuning; or a matched single-channel model matching the three-channel MAPE on these datasets.
- **Proof**: [E04, E05]
- **Evidence basis**: Table 4 (Tétouan: three-channel MAPE 1.367% vs LSTM 1.942%, CNN-LSTM 1.823%, TCN 1.471%) and Table 5 (Electrician Cup: three-channel MAPE 0.974% vs LSTM 1.522%, CNN-LSTM 1.246%, TCN 1.083%); prediction curves Figures 9 and 11. Numbers are in the cited evidence files, not restated here as the claim.
- **Dependencies**: C02
- **Tags**: architecture, multi-source-fusion, late-fusion, STLF

## C02: Convolutional feature extraction after recurrent encoding recovers cross-feature correlation LSTM alone misses
- **Statement**: Appending convolutional (local-perception, weight-sharing) feature extraction after recurrent temporal encoding captures cross-feature correlation structure that a recurrent-only model leaves unexploited, so a CNN-augmented LSTM improves forecast accuracy over an LSTM of comparable configuration even before any multi-channel modality separation is introduced.
- **Conditions**: Observed on both STLF datasets with the LSTM, CNN-LSTM, and three-channel models sharing consistent hyperparameters; increment appears as a monotone ordering LSTM < CNN-LSTM < three-channel on all three metrics. Untested outside these datasets/configuration.
- **Sources**: []
- **Status**: supported
- **Falsification criteria**: A CNN-LSTM failing to beat a matched-capacity LSTM (equal tuning) on these datasets, i.e. the convolutional stage adding no accuracy over recurrent encoding alone.
- **Proof**: [E04, E05]
- **Evidence basis**: In Table 4 and Table 5, CNN-LSTM outranks plain LSTM on RMSE/MAE/MAPE, and the three-channel model outranks both; the paper attributes this to the CNN "better capturing the characteristic information of power load." Exact cells live in the evidence tables.
- **Dependencies**: (none)
- **Tags**: cnn, lstm, hybrid, feature-extraction

## C03: A leaky rectifier avoids both dead-unit and saturation gradient pathologies for this recurrent-convolutional stack
- **Statement**: For a stacked recurrent-convolutional load forecaster, a rectifier with a nonzero negative slope outperforms both saturating activations — which lose gradient in their saturation regions — and the hard rectifier — whose zero negative branch stalls weight updates during backpropagation — because the leaky variant escapes the dead-unit and saturation gradient pathologies simultaneously.
- **Conditions**: Measured on the tuned three-channel model (Electrician-Cup configuration); the observed ranking is Leaky ReLU > Sigmoid > Tanh > ReLU by MAPE. The mechanism is inferred from the paper's gradient-pathology explanation, not from gradient measurements. Untested on other stacks/datasets.
- **Sources**: ["MAPE decreased by 0.181%, 0.299%, and 1.244% ← §3, p9 «the performance of the Leaky ReLU activation function in MAPE decreased by 0.181%, 0.299%, and 1.244%, respectively» [result]"]
- **Status**: supported
- **Falsification criteria**: An activation ablation on the same architecture where ReLU (or a saturating activation) matches or beats Leaky ReLU on held-out MAPE, contradicting the claimed gradient-pathology advantage.
- **Proof**: [E01]
- **Evidence basis**: Table 1 — MAPE: Leaky ReLU 0.974%, Sigmoid 1.155%, Tanh 1.273%, ReLU 2.218% (ReLU worst; Leaky ReLU best). Values are in the table, not the Statement.
- **Dependencies**: (none)
- **Tags**: activation-function, leaky-relu, gradient, ablation

## C04: Plain Adam's first-moment estimate fits multi-channel LSTM-CNN gradients better than adaptive/momentum variants
- **Statement**: For a multi-channel LSTM-CNN, plain Adam's first-moment (momentum) estimation aligns with the architecture's gradient patterns better than plain stochastic descent, an RMS-scaled optimizer, or Nesterov-augmented Adam; adding Nesterov look-ahead or dropping adaptivity degrades final accuracy, and an optimizer's faster early convergence does not translate into better final accuracy on coupled temporal-meteorological features.
- **Conditions**: Same tuned three-channel model; observed MAPE ordering Adam > Nadam > RMSprop > SGD. The alignment explanation is the authors' interpretation, not a measured decomposition. Untested on other architectures/datasets.
- **Sources**: ["MAPE has improved by 0.519% ← §3, p10 «its prediction accuracy in MAPE has improved by 0.519%» [result]", "MAPE increased by 6.2% ← §3, p10 «its MAPE increased by 6.2% compared to Adam in our task» [result]"]
- **Status**: supported
- **Falsification criteria**: Under equal tuning on this architecture, Nadam, RMSprop, or SGD matching or beating Adam's held-out MAPE, or RMSprop's faster early convergence yielding the best final accuracy.
- **Proof**: [E02]
- **Evidence basis**: Table 2 — MAPE: Adam 0.974%, Nadam 1.038%, RMSprop 1.102%, SGD 1.493%. Cell values live in the table.
- **Dependencies**: (none)
- **Tags**: optimizer, adam, training-dynamics, ablation

## C05: Under same-hour target alignment, the shortest historical lookback matches the target best; longer lookbacks inject noise
- **Statement**: When the historical-load channel is aligned to the same hour as the forecast target, the shortest lookback (previous day) best corresponds to the target and extending the lookback adds loosely-correlated history that degrades accuracy, with degradation accelerating sharply beyond a few days.
- **Conditions**: Same-time-next-day single-step design; lookbacks of 1–4 prior days tested; degradation is gradual from 1→3 days and abrupt at 4 days. Untested for multi-day-averaged inputs or other alignment schemes.
- **Sources**: ["MAPE ... decreased by 0.156%, 0.562%, and 3.564% ← §3, p10 «the MAPE of the model compared with other historical load input lengths has decreased by 0.156%, 0.562%, and 3.564%, respectively» [result]"]
- **Status**: supported
- **Falsification criteria**: Under the same same-hour alignment, a lookback longer than one day yielding lower held-out MAPE than the one-day lookback.
- **Proof**: [E03]
- **Evidence basis**: Table 3 — MAPE by input length (days): 1 → 0.974%, 2 → 1.130%, 3 → 1.536%, 4 → 4.520% (monotone worsening, jump at 4). Values in the table.
- **Dependencies**: (none)
- **Tags**: input-length, historical-load, lookback, ablation

## C06: Independent-encode-then-fuse gives the gentlest residuals, most so at abrupt load transitions
- **Statement**: The independent-encode-then-fuse design produces the smallest and most stable prediction residuals across the daily load cycle, and its advantage over recurrent-only and single-channel-hybrid baselines is largest at abrupt load transitions, where those baselines overshoot the true load.
- **Conditions**: Qualitative residual comparison against LSTM, CNN-LSTM, and TCN on both datasets; "gentlest residual fluctuation" and "best at sudden changes" are read from residual plots, not a single scalar. Untested for rare extreme events outside the test windows.
- **Sources**: []
- **Status**: supported
- **Falsification criteria**: A baseline exhibiting lower or more stable residuals than the three-channel model at sudden-change points, or larger baseline overshoot not being observed.
- **Proof**: [E04, E05]
- **Evidence basis**: Figures 9 & 11 (prediction curves: three-channel tracks actual through sudden changes; LSTM worst) and Figures 10 & 12 (residual magnitudes: three-channel residuals lowest/most gentle; most < 1000 kW on Tétouan per §4). Directional reading only.
- **Dependencies**: C01
- **Tags**: residual-analysis, robustness, sudden-change, qualitative
</content>
