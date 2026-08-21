# Table 2: Comparison of Planning Results of Different Schemes

**Source**: Page 18-19 of the original paper

**Description**: Comparative results of five energy storage planning schemes (no storage, Li-ion only, flow battery only, single-node HESS, and proposed multi-node HESS) evaluated across voltage fluctuation, line loss, penalty cost, and total cost metrics.

## Data

| Scheme | Installation Location | Li-Ion Capacity (MWh) | Flow Battery Capacity (MWh) | Li-Ion Power (MW) | Flow Battery Power (MW) | Voltage Fluctuation (pu) | Line Loss (pu) | Penalization Cost (CNY) | Total Cost (CNY) |
|--------|---------------------|----------------------|---------------------------|-------------------|------------------------|-------------------------|---------------|------------------------|-----------------|
| Scheme 1 | - | - | - | - | - | 56.55 | 106.94 | 1.6042e7 | 1.6042e7 |
| Scheme 2 | 33 | 5370 | - | 3280 | - | 26.15 | 58.12 | 4.0281e6 | 1.1638e7 |
| Scheme 3 | 21 | - | 5700 | - | 4400 | 28.71 | 60.74 | 5.3612e6 | 1.0736e7 |
| Scheme 4 | 15 | 2410 | 4860 | 550 | 3880 | 24.05 | 50.63 | 2.9062e6 | 9.1448e6 |
| Scheme 5 | 21, 15 | 2600 | 5300 | 2160 | 4500 | 20.52 | 45.27 | 2.3960e6 | 8.7718e6 |

## Key Insights

1. **No storage baseline (Scheme 1)**: Highest voltage fluctuation, line losses, and costs — confirms need for ESS
2. **Single Li-ion (Scheme 2)**: Better than single FB in voltage and line loss due to rapid response, but higher total cost than FB
3. **Single Flow Battery (Scheme 3)**: Lower total cost than Li-ion but higher penalty costs due to slower response
4. **Single-node HESS (Scheme 4)**: Significant improvement over single-type storage — validates hybrid approach
5. **Multi-node HESS (Scheme 5, proposed)**: Best performance across all metrics — 4.1% total cost reduction over Scheme 4
