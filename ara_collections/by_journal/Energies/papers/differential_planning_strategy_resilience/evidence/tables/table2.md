# Table 2: Resilience Improvement Strategies and Cost with Different Cases

- **Source**: Page 15, Section 5.2
- **Screenshot**: `table2.png`
- **Claims supported**: C01, C02
- **Data**:

| Case | Reinforcement Strategy | Total Cost (10^4 CNY) | MEG Nodes |
|------|----------------------|----------------------|-----------|
| 1 | 1-2^2, 2-3^2, 3-23^2, 23-24^2 | 2551.2 | / |
| 2 | 1-2^3, 2-3^2, 3-23^1, 23-24^1 | 3222.9 | / |
| 3 | 1-2^3, 2-3^1, 3-4^2, 5-6^1 | 2962.7 | / |
| 4 | 1-2^3, 2-3^2, 5-6^1, 31-32^1 | 2319.3 | 25, 32 |
| 5 | 1-2^3, 2-3^1, 5-6^1, 31-32^2 | 2367.6 | 25, 32 |

Superscript indicates reinforcement level (1, 2, or 3).

- **Key insight**: Case 1 (non-DDU) uses only level-2 hardening on four lines. Case 2 (DDU) assigns level 3 to critical line 1-2 but only level 1 to 3-23 and 23-24, demonstrating graduated allocation. Case 4 achieves lowest total cost (2319.3) by adding MEGs at nodes 25 and 32. Case 5 (DRO) has slightly higher total cost than Case 4.
