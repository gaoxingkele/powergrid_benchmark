# Mathematical Formalization

## Notation

| Symbol | Meaning |
|--------|---------|
| X = [x_ij] | Raw decision matrix (n countries x m criteria) |
| n | Number of countries (n = 36) |
| m | Number of criteria (m = 18) |
| r_ij | Normalized performance value of country i on criterion j |
| w_j | Weight assigned to criterion j |
| S_i | Baseline readiness score of country i |
| S_i^(p) | Persona-specific readiness score of country i for persona p |
| C_ij | Criterion-level contribution of criterion j to country i's score |
| L_i, M_i, U_i | Lower, modal, upper fuzzy bounds for country i |
| S_i^(def) | Defuzzified score using centroid method |

## 1. Normalization

### Benefit criterion (higher value = stronger readiness):
```
r_ij = (x_ij - min(x_j)) / (max(x_j) - min(x_j))
```

### Cost criterion (higher value = weaker readiness):
```
r_ij = (max(x_j) - x_ij) / (max(x_j) - min(x_j))
```

Where min(x_j) and max(x_j) are the minimum and maximum observed values of criterion j across all countries.

**Result**: r_ij in [0, 1]; higher always indicates stronger investment readiness.

## 2. Baseline Readiness Score

### Equal-weight model:
```
S_i = sum_{j=1}^{m} w_j * r_ij
```
where w_j = 1/m for all j (equal-weight baseline).

### Fuzzy extension (when panel data available):
```
~S_i = sum_{j=1}^{m} w_j * ~r_ij
```
Defuzzification via centroid method:
```
S_i^(def) = (L_i + M_i + U_i) / 3
```

## 3. Persona-Specific Scoring

Persona-specific weight vector:
```
W^(p) = (w_1^(p), w_2^(p), ..., w_m^(p))
```
with constraints: w_j^(p) >= 0 for all j, and sum_j w_j^(p) = 1.

Persona-specific score:
```
S_i^(p) = sum_{j=1}^{m} w_j^(p) * r_ij
```

## 4. Criterion Contribution Decomposition

```
C_ij = w_j * r_ij
```

Total score for country i:
```
S_i = sum_{j=1}^{m} C_ij
```

Dimension-level aggregation:
```
D_i^(d) = (1 / |J_d|) * sum_{j in J_d} C_ij
```
where J_d is the set of criterion indices belonging to dimension d.

## 5. Objective Weighting Methods

### Entropy weighting:
1. Compute normalized proportion: p_ij = r_ij / sum_i r_ij
2. Compute entropy: e_j = -k * sum_i p_ij * ln(p_ij) where k = 1/ln(n)
3. Compute dispersion: d_j = 1 - e_j
4. Compute weight: w_j^(entropy) = d_j / sum_j d_j

### CRITIC weighting:
1. Compute criterion standard deviations: sigma_j
2. Compute inter-criterion conflict: sum_k (1 - rho_jk) where rho_jk is Pearson correlation between criteria j and k
3. Compute information: I_j = sigma_j * sum_k (1 - rho_jk)
4. Compute weight: w_j^(critic) = I_j / sum_j I_j

### Hybrid weighting:
```
w_j^(hybrid) = (w_j^(entropy) + w_j^(critic)) / 2
```

## 6. Robustness Metrics

### Spearman rank correlation:
```
rho = 1 - (6 * sum_i d_i^2) / (n * (n^2 - 1))
```
where d_i is the rank difference for country i between two ranking scenarios.

### Top-k overlap:
Number of countries appearing in both top-k sets divided by k.

### Largest rank change:
```
max_i |rank_i^(scenario) - rank_i^(baseline)|
```
