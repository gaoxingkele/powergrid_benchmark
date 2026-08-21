# Environment

- **Language/runtime**: Python (version not specified in paper)
- **Framework**: PyTorch (version not specified in paper)
- **Hardware**: NVIDIA GeForce RTX 4060Ti GPU; 13th-Generation Intel Core i7 CPU; 32 GB RAM (workstation)
- **Data sources**: Hourly electricity-load data from a specific region, 00:00 on 1 January 2018 to
  23:00 on 28 December 2018, plus 8 weather features. **Not publicly available** (privacy restrictions);
  available on reasonable request from the corresponding author.
- **Key dependencies**: PyTorch; standard scientific stack (implied — pandas/numpy; versions not stated).
- **Training / optimization protocol**:
  - Optimizer: Adam
  - Initial learning rate: 0.001
  - Epochs: 1800
  - Dropout rate: 0.2 (also reused at inference for Monte Carlo Dropout)
  - Ensemble: AdaBoost over K = 10 GCN-BiLSTM weak learners
  - MC-Dropout samples: 100 stochastic passes per weak learner at test time
  - AdaBoost error threshold τ: 0.3 (normalized scale)
  - Training samples: m = 1200
  - Reported full-run wall time: 5 min 56 s
- **Preprocessing**: mean-of-column imputation; min-max normalization to [0,1]; 24-h sliding window →
  next-hour target; Spearman-threshold (|ρ|≥0.8) adjacency.
- **Random seeds**: Not specified in paper.

## Reproducibility note
No source code was released. The implementation-layer file
`execution/adaboost_bayesian_weighting.py` is a **reconstructed** stub grounded only in the paper's
printed equations (11–19) and Steps 1–4; the GCN-BiLSTM base-learner internals and exact tensor
plumbing are not fully specified in the paper and are left as `NotImplementedError`.
