# Related Work: TSTG Paper

## Typed Dependency Graph

### Transformers for IES Forecasting
- **Wang et al. (2022)** — Transformer-based multi-energy load forecasting; demonstrated self-attention captures temporal dependencies but did not model spatial structure.
- **Wu et al. (2020)** — Autoformer with decomposition architecture; seasonal-trend decomposition improves interpretability but no spatial modeling.
- **Zhou et al. (2021)** — Informer with ProbSparse self-attention; efficient for long sequences but univariate focus.
- **Zhou et al. (2022)** — FEDformer with Fourier-enhanced attention; frequency-domain approach captures periodicity but no cross-energy feature interaction.

### GNNs for Spatial Patterns in Energy
- **Guo et al. (2021)** — Graph convolutional network for building energy prediction; spatial structure improves accuracy but uses static adjacency.
- **Lin et al. (2022)** — Spatio-temporal graph convolutional network for multi-load; separate spatial and temporal modules, not jointly optimized.
- **Li et al. (2018)** — Diffusion convolutional recurrent network; combines GCN with GRU but sequential, not parallel spatio-temporal.

### LSTM/GRU Variants for Load Forecasting
- **Hochreiter & Schmidhuber (1997)** — LSTM foundational; widely used for short-term load forecasting but limited in capturing very long-range dependencies.
- **Cho et al. (2014)** — GRU; lighter than LSTM, used in hybrid models.
- **Kong et al. (2018)** — LSTM for residential load; good single-energy baseline but no cross-load or spatial modeling.

### Hybrid Approaches
- **ARIMA-LSTM (Zhang, 2003)** — Linear + nonlinear combination; improves over pure ARIMA but not designed for multi-energy.
- **CNN-LSTM (Kim & Cho, 2019)** — Convolutional feature extraction followed by LSTM; captures local patterns but no explicit spatial graph.
- **Attention-based GCN (Liu et al., 2023)** — Attention over graph nodes for energy; relates to TSTG but uses static graph and no MI.

### Gaps This Paper Addresses
- **No prior work jointly models** temporal long-range dependencies + nonlinear feature interactions + dynamic spatial adaptation in a single end-to-end framework.
- **No prior work uses MI** in a dual role (attention augmentation + graph construction) for multi-energy forecasting.
- **No prior work systematically ablates** calendar vs. meteorological auxiliary features in the multi-energy setting.

## Dependency Typing

| Reference | Type | Relation to TSTG |
|-----------|------|------------------|
| Transformers (general) | Background | TSTG extends Transformer with spatio-temporal attention and MI |
| Informer, Autoformer, FEDformer | Baseline (compared) | Outperformed by TSTG (Table 1) |
| GCN, GAT | Background | TSTG replaces static GCN with dynamic MI-based graph |
| Static GCN for energy | Background | TSTG's dynamic approach improves over static topology |
| LSTM/GRU | Baseline (compared) | Weaker than Transformer and TSTG baselines |
| ARIMA, Prophet | Baseline (compared) | Strong statistical baselines, outperformed |
| Hybrid CNN-LSTM | Baseline (compared) | Outperformed by TSTG end-to-end joint optimization |
