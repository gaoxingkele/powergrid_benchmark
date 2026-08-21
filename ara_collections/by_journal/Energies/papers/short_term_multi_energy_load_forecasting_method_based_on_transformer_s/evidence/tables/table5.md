# Table 5: Ablation Experiments for Each Module

**Source:** `evidence/tables/table5.png`

**Caption:** "Ablation experiments for each module."

**Extraction:** Ablations at 96 h prediction horizon, comparing variants of the spatial and attention modules. Table shows electric and cooling loads (heating not reported in this ablation).

## Transcription

| Variant | Electric MAE | Electric RMSE | Electric R2 | Cooling MAE | Cooling RMSE | Cooling R2 |
|---------|-------------|---------------|-------------|-------------|---------------|-------------|
| -StaticGCN | 0.152 | 0.208 | 0.932 | 0.081 | 0.112 | 0.987 |
| -GAT | 0.148 | 0.201 | 0.938 | 0.078 | 0.108 | 0.990 |
| -DynamicGCN | 0.142 | 0.195 | 0.942 | 0.075 | 0.106 | 0.991 |
| -WO-MSA | 0.146 | 0.199 | 0.940 | 0.077 | 0.109 | 0.988 |
| -SA | 0.144 | 0.197 | 0.941 | 0.076 | 0.107 | 0.989 |
| -MSA | 0.141 | 0.193 | 0.943 | 0.075 | 0.106 | 0.991 |
| **TSTG (full)** | **0.139** | **0.192** | **0.945** | **0.074** | **0.105** | **0.992** |

## Variant descriptions
- **-StaticGCN**: Dynamic adaptive graph convolution replaced with static physical adjacency only
- **-GAT**: Graph convolution replaced with Graph Attention Network (GAT)
- **-DynamicGCN**: Dynamic adaptive graph convolution module removed entirely
- **-WO-MSA**: Multi-head spatio-temporal attention module removed entirely
- **-SA**: MI-augmented multi-head attention replaced with single-head standard attention
- **-MSA**: MI-augmented multi-head attention replaced with standard multi-head attention (no MI)

## Key observations
- Removing either module degrades performance; using both yields the best results.
- The full model outperforms all ablation variants, confirming both modules' contributions (C01, C02).
- TSTG MAE/RMSE are 2.11%/1.54% lower than -DynamicGCN; 1.42%/0.52% lower than -MSA, confirming synergy (C05).
