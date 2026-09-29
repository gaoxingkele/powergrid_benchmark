# Method

## Main Algorithm

`CSA-LoadNet`: Cross-Series Attention Load Forecasting Network (working name before v7: `HyG-LoadFormer`)

## Naming note (2026-07-14)

Renamed from `HyG-LoadFormer` to `CSA-LoadNet` under Route A (claim downgrade). Reason: the v7 10-seed Mann-Whitney/Holm analysis (`evidence/runs/real_p2_v7_significance_analysis.md`, `evidence/tables/real_p2_v7_significance.csv`) shows the hyperbolic weighting is statistically inseparable from Euclidean, equal-weight, and fixed-curvature variants in all five dataset/horizon settings, while cross-series aggregation itself is a significant contributor on OPSD 24h (vs TemporalOnly, p=0.0011) and the full model significantly beats MLP there (p_holm=0.0085). The contribution claim is therefore cross-series attention aggregation, not hyperbolic geometry. The implementation retains the Poincare-ball embedding as one weight-parameterization option; it is no longer a claimed contribution. Evidence files and CSV row names keep the historical `HyG-LoadFormer (neural)` label unchanged.

## Innovation Handles

- Cross-series attention aggregation over the multi-region load pool feeding a shared temporal encoder (the significance-backed contribution; OPSD 24h).
- Weight parameterization is pluggable (Poincare-ball hyperbolic distance, Euclidean distance, equal-weight); v7 shows these forms are inseparable — reported as an honest component finding, not a contribution claim.
- Separates aggregation benefit from temporal-encoder capacity by the TemporalOnly ablation and 10-seed significance testing.

## Baseline Coverage

- ARIMA
- XGBoost
- LSTM
- BiLSTM
- TCN
- Transformer
- Euclidean GCN
- GCN-Transformer
- CNN-LSTM

## Ablation Coverage

- euclidean_gcn
- fixed_curvature
- temporal_only
- no_weather_features
- physical_edges_only
- poincare_only
- short_horizon_only
