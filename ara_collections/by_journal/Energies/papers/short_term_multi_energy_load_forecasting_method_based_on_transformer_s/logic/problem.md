# Problem Statement: Short-Term Multi-Energy Load Forecasting

## Observations

- **O1 — Traditional univariate forecasting models cannot jointly model temporal long-term dependencies and nonlinear feature interactions.** Single-energy models (e.g., ARIMA, Prophet) treat electric, cooling, and heating loads independently, ignoring cross-energy coupling. Even multivariate extensions fail to capture the nonlinear, asymmetric dependencies between different energy types that arise from physical conversion and complementary operation in IES.

- **O2 — GNNs capture spatial dependencies but miss temporal dynamics; Transformers capture long-range temporal patterns but miss nonlinear feature interactions.** Static GCN-based approaches rely on a fixed physical adjacency matrix that does not adapt to real-time load shifts. Standard Transformer self-attention operates along the temporal axis and models pairwise linear dependencies via dot-product, but offers no explicit mechanism for nonlinear, higher-order interactions across the feature (energy-type) dimension.

- **O3 — Mutual information (MI) provides a principled way to capture nonlinear and asymmetric dependencies that linear correlation (Pearson) or dot-product similarity cannot.** MI measures any statistical dependence (linear or nonlinear) and is asymmetric, making it suitable for detecting directional influence between energy loads (e.g., heating load influencing electric load differently than the reverse).

- **O4 — Calendar features (hour of day, day of week, month) dominate meteorological features (temperature, humidity) for multi-energy load forecasting.** Multi-energy loads exhibit strong temporal周期性 (periodicity) tied to human activity patterns (occupancy schedules, operational routines), which calendar features capture. Meteorological conditions provide secondary corrections but are less predictive overall.

## Gaps

- **G1 — No existing method jointly addresses nonlinear cross-energy coupling and dynamic spatial adaptation in a single end-to-end framework.** Prior work either (a) uses static GCN with fixed physical topology, (b) uses Transformer on univariate or stacked-univariate loads, or (c) applies attention and GCN sequentially without joint optimization. The combination of MI-augmented spatio-temporal attention and dynamic graph convolution has not been explored.

- **G2 — The relative contribution of calendar vs. meteorological auxiliary features for multi-energy load forecasting is not systematically benchmarked.** Existing studies fuse both types without ablation, leaving unclear which source carries greater predictive value and whether both are necessary.

## Key Insight

Mutual information can serve as a differentiable augmentation to the standard scaled dot-product attention, enabling the model to capture nonlinear/asymmetric dependencies across both temporal and feature dimensions. Simultaneously, MI computed from real-time load representations provides a natural similarity measure for dynamically updating the spatial adjacency matrix, fusing physical topology with data-driven feature relations. This dual role of MI — as an attention augmenter and a graph constructor — creates a unified framework where the two modules reinforce each other: better feature representations from MI-augmented attention yield better MI-based adjacency matrices, which in turn improve spatial message passing.

## Assumptions

- **A1 — Historical load patterns (daily, weekly, seasonal) are sufficient to generalize to future short-term horizons (6--96 h).** The model assumes stationarity in the underlying temporal dynamics of multi-energy consumption; extreme distribution shifts (e.g., new building occupancy, policy changes) may violate this assumption.

- **A2 — The physical topology of the energy network is known and fixed.** The model requires a pre-defined physical adjacency matrix (e.g., pipe/duct connections between buildings or substations); this may not be available in all IES deployments.

- **A3 — Mutual information estimated from mini-batch representations is a reliable approximation of true statistical dependence.** The MI estimator uses a bilinear projection layer and operates on d_model-dimensional embeddings from a batch of T_hist time steps; its accuracy degrades with very small batch sizes or extremely noisy sensor data.
