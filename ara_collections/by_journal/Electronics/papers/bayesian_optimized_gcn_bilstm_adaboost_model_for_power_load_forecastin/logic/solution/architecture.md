# Architecture — GCN-BiLSTM-AB Ensemble Pipeline

The pipeline (Figure 1) has three functional blocks: a **data-preparation model**, a **feature-correlation
/ adjacency model**, and a **prediction-and-evaluation model** that runs an AdaBoost ensemble of ten
GCN-BiLSTM base learners with Monte Carlo Dropout uncertainty weighting.

## Component graph (data flow)

```
Historical data ─► mean-imputation ─► min-max normalization ─► 24-h sliding window
       │                                                             │
       └─► Spearman correlation ─► threshold |ρ|≥0.8 ─► adjacency A ──┤
                                                                      ▼
                              ┌─────────── GCN-BiLSTM base learner (×10) ───────────┐
   input 24×8 ─►  GCN layer (24×8 → 24×128) ─► Dropout(0.2) (24×128) ─► BiLSTM (24×128 → 1×512) ─► FC out (1×512 → 1×1)
                              └─────────────────────────────────────────────────────┘
                                                                      ▼
   AdaBoost: sample re-weighting (error>0.3) + learner weight α_k ─► training-phase weights W_m
                                                                      ▼
   MC-Dropout testing: 100 stochastic passes/learner ─► mean ȳ + variance (uncertainty)
                                                                      ▼
   Weight attenuation W'_m = W_m/(1+uncertainty) ─► normalize ─► W''_m
                                                                      ▼
   Weighted sum of 10 learners ─► point forecast + 95% predictive interval
```

## Components

### 1. Data-preparation model
- **Purpose**: Clean and shape raw hourly load + weather into model tensors.
- **Inputs**: 10-column table (date + load + 8 weather features); missing cells.
- **Outputs**: Normalized `24×8` windows, each mapped to the next-hour load target; train/test split.
- **Key choices**: Mean-of-column imputation; min-max scaling to [0,1] (Eq 20); 24-h window → 1-hour-ahead target.

### 2. Feature-correlation / adjacency model
- **Purpose**: Build the static GCN graph over features.
- **Inputs**: Feature matrix.
- **Outputs**: Binary adjacency `A` (edge iff Spearman |ρ| ≥ 0.8, else 0), symmetrically normalized with self-loops inside the GCN.
- **Interactions**: `A` is consumed by every GCN layer in every base learner.
- **Key choices**: Spearman rank correlation (chosen over KNN/learned/MI) for robustness to non-normal, non-linear, monotonic feature relations.

### 3. GCN spatial encoder (per base learner)
- **Purpose**: Aggregate inter-feature (spatial) dependencies. Eq 1.
- **Inputs**: `24×8` window + adjacency `A`.
- **Outputs**: `24×128` spatially-enriched feature sequence.
- **Interactions**: Output → Dropout → BiLSTM.

### 4. Dropout layer
- **Purpose**: Regularization during training; the stochasticity reused at inference for MC-Dropout uncertainty.
- **Inputs/Outputs**: `24×128` → `24×128`, rate 0.2.

### 5. BiLSTM temporal encoder (per base learner)
- **Purpose**: Extract bidirectional long-range temporal dependencies. Eqs 2–10.
- **Inputs**: `24×128`.
- **Outputs**: `1×512` sequence embedding → fully-connected output `1×1` (next-hour load).

### 6. AdaBoost ensemble controller
- **Purpose**: Train and combine 10 GCN-BiLSTM weak learners; concentrate later learners on hard samples.
- **Inputs**: Per-sample errors `e_i`; sample weights `D_k`.
- **Outputs**: Per-learner training weight `W_m` (= α_k form), normalized sample weights.
- **Key choices**: Only samples with `e_i > 0.3` are up-weighted (×1.1); learner weight `α_k = 0.5/exp(weight_sum)`; deep base learner instead of shallow tree.

### 7. Bayesian (MC-Dropout) uncertainty & weighting head
- **Purpose**: Quantify each learner's predictive variance and attenuate unreliable learners; emit interval.
- **Inputs**: 100 stochastic dropout passes per learner (Eq 17); training weights `W_m`.
- **Outputs**: Attenuated normalized weights `W''_m` (Eqs 18–19); final weighted-sum forecast; 95% confidence interval.

## What the diagram (Figure 1) conveys
The novelty is not in any single block but in the **feedback of per-learner uncertainty into the
boosting weights**: AdaBoost sets `W_m` from training error, then MC-Dropout variance divides it down
so unstable learners contribute less to the final weighted sum — coupling accuracy (boosting on hard
samples) with robustness (discounting high-variance learners) in one pipeline.
