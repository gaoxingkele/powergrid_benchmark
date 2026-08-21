# Model / Training Configuration

Values from Table 3 (§4.2) and the §4.2 hyperparameter narrative. Sources cited per parameter.

## Input layer
- **Value**: input dimension 24 × 8 (24 time steps × 8 feature dimensions); no output listed
- **Rationale**: 24-h sliding window over 8 feature dimensions for one-step-ahead prediction
- **Search range**: Not specified in paper
- **Sensitivity**: Not specified in paper
- **Source**: Table 3; §4.2 "raw time-series data consisting of 24 time steps and 8 feature dimensions (24 × 8)"

## GCN layer
- **Value**: input 24 × 8 → output 24 × 128
- **Rationale**: Spatial feature extraction over the feature graph; lifts 8 feature channels to 128
- **Search range**: Not specified in paper
- **Sensitivity**: Not specified in paper
- **Source**: Table 3

## Dropout
- **Value**: rate 0.2; 24 × 128 → 24 × 128
- **Rationale**: Mitigate overfitting during training; stochasticity reused for MC-Dropout at inference
- **Search range**: Not specified in paper
- **Sensitivity**: Not specified in paper
- **Source**: Table 3; §4.2 "a Dropout rate of 0.2 was applied to mitigate overfitting"

## BiLSTM layer
- **Value**: input 24 × 128 → output 1 × 512
- **Rationale**: Bidirectional temporal feature extraction; collapses sequence to a 512-d embedding
- **Search range**: Not specified in paper
- **Sensitivity**: Not specified in paper
- **Source**: Table 3

## Output layer
- **Value**: input 1 × 512 → output 1 × 1 (next-hour load)
- **Rationale**: Regression head producing the scalar load forecast
- **Search range**: Not specified in paper
- **Sensitivity**: Not specified in paper
- **Source**: Table 3

## Optimizer
- **Value**: Adam
- **Rationale**: Network parameter updates
- **Source**: §4.2

## Initial learning rate
- **Value**: 0.001
- **Rationale**: Not specified in paper
- **Source**: §4.2 "an initial learning rate set to 0.001"

## Training epochs
- **Value**: 1800
- **Rationale**: Not specified in paper
- **Source**: §4.2 "trained over 1800 epochs"

## Ensemble size (K)
- **Value**: 10 weak learners
- **Rationale**: AdaBoost integration of GCN-BiLSTM base learners
- **Source**: §2.4 "The AdaBoost framework is introduced to integrate 10 such weak learners"

## AdaBoost error threshold (τ)
- **Value**: 0.3 (normalized scale)
- **Rationale**: Only above-threshold-error samples up-weighted; must be tuned per application
- **Search range**: Not specified in paper (stated tunable)
- **Sensitivity**: high (paper flags it as application-dependent) — not quantified
- **Source**: §2.4 "only increases the weights of samples with prediction errors exceeding 0.3"

## MC-Dropout samples (T)
- **Value**: 100 stochastic passes per weak learner
- **Rationale**: Estimate predictive variance (uncertainty)
- **Source**: §2.5 "each GCN-BiLSTM weak learner generates 100 stochastic predictions"

## Training-sample count (m)
- **Value**: 1200
- **Rationale**: Denominator of initial sample weight D_1(i)=1/m
- **Source**: §2.4 "where m is the number of training samples (1200)"
