# Method

## Main Algorithm

`HyG-LoadFormer`: Hyperbolic Graph Load Forecasting Transformer

## Innovation Handles

- Uses hyperbolic geometry to model load and grid hierarchy.
- Separates hierarchy benefit from generic GCN/Transformer capacity by ablation.
- Links forecast accuracy to dispatch sensitivity metrics.

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
