# Table 4: Energy Storage Capacity Under Different Penalty Factors

**Source**: Page 22 of the original paper

**Description**: Sensitivity analysis showing how the planned energy storage capacity and power change under different flexibility penalty coefficients (ranging from 0.1 to 0.5 times the baseline lambda_0). This analysis helps grid operators understand the trade-off between flexibility tolerance and storage investment.

## Data

| Penalty Factor | Li-Ion Capacity (MWh) | Li-Ion Power (MW) | Flow Battery Capacity (MWh) | Flow Battery Power (MW) |
|----------------|----------------------|-------------------|---------------------------|------------------------|
| 0.1*lambda_0 | 3068 | 2484 | 6254 | 5175 |
| 0.2*lambda_0 | 2860 | 2333 | 5830 | 4860 |
| 0.3*lambda_0 | 2600 | 2160 | 5300 | 4500 |
| 0.4*lambda_0 | 2236 | 1901 | 4558 | 3960 |
| 0.5*lambda_0 | 1950 | 1685 | 3675 | 3110 |

## Key Insights

1. **Monotonic decrease**: Both Li-ion and flow battery capacity and power decrease as the penalty coefficient increases (i.e., as tolerance for flexibility shortfall decreases)
2. **Flow battery dominance**: Across all scenarios, FB capacity and power are significantly higher than Li-ion, highlighting the need for large-scale FB to balance low-frequency energy fluctuations
3. **Recommended range**: For grid operators prioritizing stability, penalty coefficient in range 0.2-0.3 lambda_0 is recommended to maintain higher redundancy
4. **Trade-off**: Lower penalty coefficient (stricter flexibility requirement) -> higher storage investment; higher penalty coefficient -> lower investment but increased operational risk
