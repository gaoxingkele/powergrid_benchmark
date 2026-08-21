# Constraints: TSTG Paper

## Assumptions

- **A1 — Historical load stationarity**: The model assumes that temporal patterns observed in the historical window (daily, weekly, seasonal) remain sufficiently stationary to generalize to short-term forecast horizons (6--96 h). Extreme distribution shifts (e.g., new building occupancy schedules, energy policy changes, equipment retrofits) degrade performance.

- **A2 — Known physical topology**: A pre-defined physical adjacency matrix A_phy is required as input. In IES deployments where the physical network topology is unknown, unmeasured, or dynamically reconfigured, the model must rely entirely on the data-driven MI similarity component, reducing the benefit of the fusion mechanism.

- **A3 — Representative batch for MI estimation**: The mutual information estimator uses mini-batch representations. With very small batch sizes or highly noisy sensor data, the MI estimate becomes unreliable, potentially degrading attention quality and graph construction.

## Limitations

- **L1 — O(T^2 + D^2) per-layer attention complexity**: Multi-head spatio-temporal attention computes pairwise attention over T_hist time steps and D feature dimensions within each head. For very long historical windows (T_hist > 168) or a large number of energy types, this quadratic cost may become prohibitive. Optimization approaches (e.g., sparse attention, kernel approximation) could mitigate but are not explored.

- **L2 — O(N^2) graph similarity cost**: Computing the MI-based similarity graph for all N node pairs introduces an O(N^2) cost per layer. For very large networks (N > 10^3), this becomes a computational bottleneck that may outweigh the benefit of dynamic adaptation.

- **L3 — MI estimation bias**: The bilinear MI estimator (Eq. 2) is a lower-bound approximation of the true MI. Its accuracy depends on the richness of the learned projection and the nonlinear activation. With insufficient hidden dimension or poor optimization, the MI term may add noise rather than signal to the attention computation.

## Requirements

- **R1 — GPU memory for multi-head + graph storage**: The model stores attention matrices for H heads x 2 axes (time + feature), plus an N x N dynamic adjacency per layer, requiring O(H·(T^2 + D^2) + N^2) memory per layer. For the reported settings (N=20, T=24, D=3, H=4, depth=3), this is modest, but scaling up requires consideration.

- **R2 — Matching train and test feature spaces**: The auxiliary feature dimensions (calendar and meteorological) must be available for both training and inference. Missing meteorological data at inference time would reduce the model to Case 2 (calendar-only) performance.

## Trade-offs

- **Accuracy vs. compute**: The dynamic MI adaptivity introduces additional parameters (bilinear projection matrices W_mi, W_sim) and O(N^2) graph computation per layer. The accuracy gains (Table 1) are substantial enough to justify the overhead for short-term IES forecasting, but for latency-critical applications or resource-constrained edge deployment, lighter models (LightTS, TiDE) may be preferred.

- **Complexity vs. interpretability**: The combined attention + graph + MI modules make TSTG more complex than standard Transformers or GCNs, reducing interpretability. The MI-based graph does provide some inherent explainability (which loads/nodes have high mutual information), but the overall model remains largely a black box.
