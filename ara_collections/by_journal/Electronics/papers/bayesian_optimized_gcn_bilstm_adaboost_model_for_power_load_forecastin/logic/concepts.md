# Concepts

## Graph Convolutional Network (GCN) over meteorological factors
- **Notation**: $H^{(1)} = \sigma\!\left(\tilde{D}^{-\frac12}\tilde{A}\tilde{D}^{-\frac12}H^{(0)}W^{(0)}\right)$ (Eq. 1)
- **Definition**: A spectral graph convolution that aggregates each node's features with its neighbors' via the symmetrically normalized adjacency $\tilde{A}$ (with self-loops) and degree matrix $\tilde{D}$. Here nodes are the meteorological/load feature vectors at a time step and edges encode their pairwise dependency, so the GCN extracts inter-feature (spatial) correlations.
- **Boundary conditions**: Requires a predefined adjacency; in this work the graph is static across the whole series (built once from Spearman correlations, not re-estimated over time).
- **Related concepts**: Spearman-threshold adjacency construction; BiLSTM temporal extractor.

## Bidirectional LSTM (BiLSTM)
- **Notation**: $h_t = [\overrightarrow{h}_t, \overleftarrow{h}_t]$ (Eq. 8); LSTM gates Eqs. 2–7
- **Definition**: Two LSTMs run over the sequence in opposite directions; their hidden states are concatenated so each step's representation depends on both past and future context, capturing long-range temporal dependencies more comprehensively than a unidirectional LSTM.
- **Boundary conditions**: Full-sequence bidirectionality assumes the whole input window is available at inference (offline/window forecasting), not strictly causal streaming.
- **Related concepts**: LSTM gating (forget/input/output); GCN output feeds BiLSTM.

## Modified AdaBoost ensemble (selective sample re-weighting)
- **Notation**: $e_i=|\hat{y}_i-y_i|$ (Eq. 11); $\text{weight\_sum}=\sum_{i|e_i>0.3}D_k(i)$ (Eq. 12); $\alpha_k=\frac{0.5}{\exp(\text{weight\_sum})}$ (Eq. 13); $D_{k+1}(i)=D_k(i)\times1.1$ for $e_i>0.3$ (Eq. 14)
- **Definition**: A boosting ensemble of ten GCN-BiLSTM weak learners in which, unlike classic AdaBoost, only samples with error above a fixed absolute threshold (0.3) have their weights raised (×1.1), and the learner weight uses an exponential-decay form. Sample weights are normalized to sum to 1; learner weights are left for the later Bayesian step.
- **Boundary conditions**: Threshold 0.3 is on the normalized scale and stated to require per-application tuning; weak learner here is a deep spatiotemporal net rather than a shallow tree.
- **Related concepts**: Uncertainty-based weight attenuation; GCN-BiLSTM base learner.

## Monte Carlo Dropout (Bayesian approximation)
- **Notation**: $\text{Uncertainty}=\frac{1}{100}\sum_{n=1}^{100}(y_n-\bar{y})^2$ (Eq. 17)
- **Definition**: Dropout kept active at inference; repeated stochastic forward passes approximate sampling from the posterior over model parameters, so the mean of the passes is the point prediction and their variance is an uncertainty estimate. Used both to prevent overfitting (training) and to quantify per-learner predictive variance (testing).
- **Boundary conditions**: An approximation to Bayesian inference, not exact posterior inference; quality depends on dropout rate (0.2 here) and sample count (100).
- **Related concepts**: Bayesian uncertainty; uncertainty-based weight attenuation; 95% predictive interval.

## Uncertainty-based weight attenuation
- **Notation**: $W'_m=\frac{W_m}{1+\text{uncertainty}}$ (Eq. 18); $W''_m=\frac{W'_m}{\sum_{m=1}^{10}W'_m}$ (Eq. 19)
- **Definition**: Each weak learner's AdaBoost-derived weight $W_m$ is divided by $1+$ its predictive variance, then all weights are normalized; higher-variance (less reliable) learners are down-weighted before the final weighted-sum prediction.
- **Boundary conditions**: Assumes dropout-sampling variance is a faithful reliability proxy; applied once, after AdaBoost training, at the testing phase.
- **Related concepts**: Monte Carlo Dropout; modified AdaBoost ensemble.

## Spearman-threshold adjacency construction
- **Notation**: edge iff $|\rho_{\text{Spearman}}| \ge 0.8$ (weight 1), else 0
- **Definition**: The GCN adjacency matrix is built by computing pairwise Spearman rank correlations among input features; an absolute value ≥ 0.8 becomes an edge (weight 1), all else weight 0. Chosen because features lack normality/linear correlation and rank statistics capture monotonic relations robustly and training-free.
- **Boundary conditions**: Static graph; sensitive to the 0.8 cutoff; one reported correlation exceeds 1.0 (Wind Speed–Pressure = 1.17), an apparent data/computation anomaly.
- **Related concepts**: GCN; alternative graph builders (KNN, learned graphs, mutual information).

## 24-hour sliding window (one-step-ahead forecasting)
- **Notation**: input $24\times 8$ → output $1\times 1$
- **Definition**: A sliding window of 24 hourly steps over 8 feature dimensions is used to predict the load value of the subsequent hour; the window slides forward across the series to generate training/test samples.
- **Boundary conditions**: Fixed 24-h context and single-hour horizon per prediction; multi-step horizons (one-day/one-week plots) are formed by rolling this one-step model.
- **Related concepts**: Min-max normalization; GCN-BiLSTM input tensor.

## Prediction uncertainty (predictive variance / 95% confidence interval)
- **Notation**: variance of MC-Dropout passes; 95% CI band
- **Definition**: In this paper "prediction uncertainty" is specifically the variance of predictions from each GCN-BiLSTM weak learner obtained via MC Dropout; visualized as a 95% confidence interval around the forecast, interpreted as the range within which the true value lies with 95% probability under repeated sampling.
- **Boundary conditions**: Interval is model-derived (approximate), asserted rather than empirically calibration-validated.
- **Related concepts**: Monte Carlo Dropout; uncertainty-based weight attenuation.
