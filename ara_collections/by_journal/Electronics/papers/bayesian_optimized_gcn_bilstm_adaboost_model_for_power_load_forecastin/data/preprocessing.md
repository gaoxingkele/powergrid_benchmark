# Preprocessing

## 1. Missing-value imputation
- Missing cells are filled with the **mean of the respective column** containing the missing data
  (§2.1, Figure 1: "Fill in the missing values with the missing values column average").

## 2. Normalization (min-max)
- Each feature is linearly mapped to [0,1] via min-max scaling (Eq 20):
  $X_i^* = \dfrac{X_i - X_{\min}}{X_{\max} - X_{\min}}$
- Rationale: eliminate inter-feature dimensional discrepancies; accelerate convergence; stabilize
  numerics (§3.2).
- Predictions are de-normalized back to the load scale (Eq 21):
  $x^* = y^*(x_{\max}-x_{\min}) + x_{\min}$.

## 3. Windowing
- A **24-hour sliding window** is constructed to predict the load value for the **subsequent hour**
  (one-step-ahead). Model input tensor: 24 × 8.

## 4. Adjacency-matrix construction (GCN graph)
- Compute pairwise **Spearman rank correlation** among input features (chosen over Pearson because
  features lack normality/linear correlation; §2.2).
- Edge rule: if a correlation's absolute value **≥ 0.8**, set an edge (connection weight **1**);
  otherwise weight **0** (§2.1, §2.2).
- The resulting binary adjacency is used (with self-loops, symmetric normalization) inside every GCN
  layer (Eq 1).
- Reported correlation values are in Figure 2; note the anomalous Wind Speed–Pressure = 1.17 (> 1),
  see `evidence/figures/figure2.md`.
- Edges implied by the ≥0.8 rule (from Figure 2, absolute values): Temperature–Pressure (0.86),
  Temperature–Water Vapor (0.89), Temperature–Apparent Temp (0.99), Wind Speed–Pressure (1.17),
  Pressure–Water Vapor (0.85), Pressure–Apparent Temp (0.87), Water Vapor–Apparent Temp (0.92).

## 5. Train/test split
- m = 1200 training samples (§2.4). Test-set size not explicitly stated; evaluation reported over
  one-day and one-week horizons.

## Source
§2.1 (Figure 1 flow), §2.2 (Spearman/adjacency), §3.2 (normalization), §4.1 (graph comparison).
