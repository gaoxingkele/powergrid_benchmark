# Table 1 - Comparison of Different Algorithms

- **Source**: Table 1, Section 4.5
- **Caption**: "Comparison of different algorithms."
- **Screenshot**: table1.png
- **Extraction type**: raw_table

| Algorithm | Scenario 1 |  |  | Scenario 2 |  |  | Scenario 3 |  |  |
|-----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|
| | V | o1 | o2 | V | o1 | o2 | V | o1 | o2 |
| IGA | 0.20 | 3202.13 | 4216.66 | 0.29 | 8094.54 | 5246.46 | 0.30 | 3381.65 | 4948.82 |
| MGA | 0.23 | 3290.70 | 4330.03 | 0.33 | 8156.91 | 5333.16 | 0.32 | 3447.34 | 4957.79 |
| MPSO | 17.6 | 3365.40 | 4524.81 | 13.4 | 8107.57 | 5348.40 | 10.91 | 3478.29 | 4965.16 |
| SGA | 0.18 | 3468.18 | 4463.21 | 0.32 | 8295.44 | 5453.69 | 0.30 | 3486.24 | 4975.41 |
| MABC | 2.5 | 3234.07 | 4253.31 | 4.8 | 8120.60 | 5309.64 | 3.74 | 3397.34 | 4955.38 |

*V: maximum equality constraint violation (kW); o1: total operating cost (CNY); o2: total carbon emissions (m3)*

**Notes**:
- IGA achieves the lowest o1 and o2 values in all three scenarios compared to all other algorithms.
- IGA constraint violations are 0.20, 0.29, 0.30 kW across scenarios, consistently below 0.3 kW.
- All GA variants (IGA, MGA, SGA) show violations <0.33 kW, while penalty-function-based methods (MPSO, MABC) show violations orders of magnitude higher.
- SGA (single-objective) shows competitive constraint violations but higher o2 (carbon emissions) than multi-objective algorithms.
- IGA outperforms MGA in both objectives in all scenarios, validating the cyclic crossover and polynomial mutation enhancements.
