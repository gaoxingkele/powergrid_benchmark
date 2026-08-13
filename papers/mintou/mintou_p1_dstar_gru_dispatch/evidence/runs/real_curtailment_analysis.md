# Real Curtailment Forecasting Analysis - P1 DSTAR-GRU (v4 pivot)

Status: `public_rts_curtailment_v6_modern_temporal_controls`.

## Why v4 exists

The v3 dispatch experiment scored hand-parameterized method proxies, and
DSTAR-GRU carried an exclusive renewable-bias formula that manufactured most
of the curtailment gap highlighted in the round-2 review. v4 redefines the
task honestly: curtailment under a FIXED reference dispatch policy is the
method-independent target, every method is a real forecasting model, and
DSTAR-GRU's Siamese retrieval operates in a genuinely learned embedding
space. v3 artifacts remain as historical evidence.

## Headline (per horizon)

### Horizon 1h

- DSTAR-GRU MAE `0.00769850` (std `0.00026278`, rank 4/14)
- Best baseline: `Persistence` MAE `0.00690531`
- Margin over best baseline: `-10.30%`
- Event F1: `0.674076` vs best baseline `0.769737`
- ONSET F1 (validation-calibrated detection): `0.176114` vs best baseline `LSTM` `0.173514`
- ONSET MAE: `0.04875569` vs best baseline `0.04035899`

| rank | method | role | MAE | onset F1 | onset MAE | event F1 | stress MAE |
|---|---|---|---|---|---|---|---|
| 1 | Persistence | baseline | 0.00690531 | 0.042458 | 0.06753225 | 0.769737 | 0.01994194 |
| 2 | Ablation-NoTopology | ablation | 0.00750717 | 0.184597 | 0.04743546 | 0.659461 | 0.02165156 |
| 3 | Ablation-LSTMEncoder | ablation | 0.00762671 | 0.185409 | 0.04678222 | 0.680522 | 0.02197200 |
| 4 | DSTAR-GRU | proposed | 0.00769850 | 0.176114 | 0.04875569 | 0.674076 | 0.02218815 |
| 5 | TCN | baseline | 0.00833791 | 0.165169 | 0.04874025 | 0.700966 | 0.02224085 |
| 6 | LSTM | baseline | 0.00966282 | 0.173514 | 0.04379054 | 0.724201 | 0.02503223 |
| 7 | Ablation-NoRetrievalBank | ablation | 0.01240724 | 0.163099 | 0.04190934 | 0.696107 | 0.03114757 |
| 8 | Ablation-NoSiamese | ablation | 0.01281050 | 0.089172 | 0.04880844 | 0.541833 | 0.03528196 |
| 9 | kNN-RawFeature | baseline | 0.01281050 | 0.089172 | 0.04880844 | 0.541833 | 0.03528196 |
| 10 | MLP | baseline | 0.01294264 | 0.162302 | 0.04866386 | 0.631467 | 0.02911240 |
| 11 | Ablation-SmallBank | ablation | 0.01534389 | 0.042458 | 0.06937456 | 0.000000 | 0.04431182 |
| 12 | Ridge | baseline | 0.01984423 | 0.143426 | 0.04455398 | 0.434783 | 0.05038428 |
| 13 | Seasonal-24h | baseline | 0.02035887 | 0.076271 | 0.07043567 | 0.342105 | 0.04886620 |
| 14 | DLinear | baseline | 0.02201935 | 0.122143 | 0.04035899 | 0.265595 | 0.04982051 |

### Horizon 24h

- DSTAR-GRU MAE `0.02054281` (std `0.00025532`, rank 8/14)
- Best baseline: `kNN-RawFeature` MAE `0.01946336`
- Margin over best baseline: `-5.25%`
- Event F1: `0.034290` vs best baseline `0.131737`
- ONSET F1 (validation-calibrated detection): `0.176789` vs best baseline `Ridge` `0.235602`
- ONSET MAE: `0.11082187` vs best baseline `0.10131713`

| rank | method | role | MAE | onset F1 | onset MAE | event F1 | stress MAE |
|---|---|---|---|---|---|---|---|
| 1 | Ablation-SmallBank | ablation | 0.01534389 | 0.122857 | 0.13239732 | 0.000000 | 0.04431182 |
| 2 | Ablation-NoSiamese | ablation | 0.01946336 | 0.224913 | 0.10675782 | 0.131737 | 0.04350381 |
| 3 | kNN-RawFeature | baseline | 0.01946336 | 0.226415 | 0.10675782 | 0.131737 | 0.04350381 |
| 4 | Ablation-LSTMEncoder | ablation | 0.02032465 | 0.168747 | 0.11111369 | 0.068417 | 0.04567292 |
| 5 | Ablation-NoTopology | ablation | 0.02034663 | 0.175247 | 0.11088351 | 0.061635 | 0.04579518 |
| 6 | Persistence | baseline | 0.02035887 | 0.122857 | 0.13228327 | 0.340000 | 0.04886620 |
| 7 | Seasonal-24h | baseline | 0.02035887 | 0.122857 | 0.13228327 | 0.340000 | 0.04886620 |
| 8 | DSTAR-GRU | proposed | 0.02054281 | 0.176789 | 0.11082187 | 0.034290 | 0.04625580 |
| 9 | Ablation-NoRetrievalBank | ablation | 0.02195273 | 0.206973 | 0.10981972 | 0.000000 | 0.04613928 |
| 10 | LSTM | baseline | 0.02196195 | 0.210796 | 0.10902063 | 0.018598 | 0.04583260 |
| 11 | TCN | baseline | 0.02219860 | 0.182822 | 0.11122535 | 0.021807 | 0.04606279 |
| 12 | Ridge | baseline | 0.02427802 | 0.235602 | 0.10648650 | 0.025157 | 0.04949261 |
| 13 | MLP | baseline | 0.02664181 | 0.206373 | 0.10226666 | 0.167563 | 0.04885908 |
| 14 | DLinear | baseline | 0.02822760 | 0.164984 | 0.10131713 | 0.044185 | 0.05012421 |

## Interpretation Boundary

The target is curtailment under one fixed reference policy, i.e. a proxy
for operational curtailment risk, not an OPF/UC-validated quantity; the
dispatch-advisory story requires the (still open) DC-OPF layer. Learned
methods share the training regime and temporal splits; deterministic
methods have single rows. Significance: Mann-Whitney U + Holm on
curtailment MAE, seeded methods only.
