# Environment

- **Language/runtime**: MATLAB R2024a (Matlab2024a)
- **Framework**: MATLAB deep-learning toolbox (TCN, BiLSTM, Adam optimizer); SVMD and SBOA implemented per §2 (no library named). Optimizer comparison also implements SSA and GWO.
- **Hardware**: Intel Core i9-13900HX CPU; 16 GB RAM; NVIDIA GeForce RTX 4070 GPU (training GPU-accelerated).
- **Data sources**: Regional electricity load, a region in Belgium, 1 Jan 2018 – 31 Dec 2018, 15-min sampling, 35,040 points. "Dataset available on request from the authors." No public link.
- **Key dependencies**: Not enumerated in the paper beyond MATLAB R2024a.
- **Protocols**:
  - Preprocessing: quartile outlier detection → missing → interpolation upsampling; min–max normalization to [0,1] (Eq. 33) with inverse (Eq. 34).
  - Split: 5:1 train/test; whole-year experiment uses first 10 months for training, remainder for testing; per-season experiments split each season 5:1. Day-ahead forecasting, 96 points/day, each day predicted from the previous day.
  - Model config (§5.2): TCN 10 filters, filter size 2, 1 residual block, dropout 0.02; BiLSTM 60 hidden units, max 100 epochs, ReLU; Adam optimizer, initial lr 0.005 halved every 2 epochs via callback.
  - SVMD/SBOA config (Table 1): compactness (maxAlpha) optimized = 19,990.25; SBOA pop 30, max_iteration 60; stopping-criteria type 4; dual-ascent time step 0; convergence tolerance 1×10⁻⁶.
  - Decomposition baselines (Table 3): CEEMDAN/ICEEMDAN with Nstd 0.2, NR 100, MaxIter 1000, SNRFlag 2.
- **Random seeds**: Not specified in paper.

## Implementation note
The paper describes SVMD, SBOA, TCN and BiLSTM via equations (Eqs. 1–37) and flowcharts (Figures 1, 2, 8) but prints no source code and no algorithm-listing pseudocode, and releases no repository. Per ARA Rule 14(a), no `src/execution/` code stub is manufactured from the prose method — the algorithmic content lives in `logic/solution/algorithm.md` and `architecture.md`. If the authors' MATLAB code is later obtained, transcribe it into `src/execution/` (grounded: transcribed).
