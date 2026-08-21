# Figure 1: Model flow chart

- **Source**: Figure 1, §2.1 (page 4, middle of page)
- **Caption**: "Model flow chart."
- **Screenshot**: figure1.png
- **Figure type**: diagram
- **Extraction method**: visual_description
- **Reading confidence**: high

## Visual description
- **Components** (three colored sub-blocks):
  - *Data preparation model* (pink): Start → Get historical data → Fill missing values with column
    average → split into Training Data / Test Data.
  - *Feature correlation analysis model* (blue): Use Spearman correlation coefficient → decision
    "Correlation coefficient > 0.8?" → Yes: connection = 1 / No: connection = 0 → Generate adjacency matrix.
  - *Prediction and evaluation model* (yellow): Normalization → "Adaboost: GCN-BiLSTM model × 10" →
    Monte Carlo Dropout Sampling → decision "Training completed or not?" (No loops back) → Yes: Load
    forecasting and uncertainty estimation → Adaboost integration → "GCN-BiLSTM-Adaboost (Bayesian
    version) model" → End.
- **Connections**: Data-prep feeds both the feature-correlation branch (adjacency) and the
  prediction branch (train/test data); the adjacency matrix feeds the GCN in the prediction block; a
  training-loop back-edge iterates until convergence.
- **Annotations**: dashed colored boundaries group the three functional models; a diamond decision node
  encodes the |ρ|>0.8 edge rule and another the training-completion check.
- **What it conveys**: the end-to-end pipeline and, in particular, that the Bayesian (MC-Dropout)
  sampling and the AdaBoost ensemble of 10 GCN-BiLSTM learners sit inside a single training/evaluation
  loop. Mirrored into `logic/solution/architecture.md`.
