# Table 4: Resilience Improvement Strategies with Different Budgets

- **Source**: Pages 16-17, Section 5.2
- **Screenshots**: `table4a.png` (page 16), `table4b.png` (page 17)
- **Claims supported**: C02, C04
- **Data**:

| Reinforcement Cost (10^4 CNY) | Total Cost (10^4 CNY) | Resilience Improvement Strategies | MEG Nodes |
|------------------------------|----------------------|----------------------------------|-----------|
| 0 | 2711.7 | / | 25, 32 |
| 12 | 2367.6 | 1-2^3, 2-3^1, 5-6^1, 31-32^2 | 25, 32 |
| 15 | 2317.9 | 1-2^3, 2-3^2, 5-6^1, 3-23^1, 32-33^2 | 25, 33 |
| 18 | 2237.8 | 1-2^3, 2-3^2, 3-4^2, 23-24^1, 32-33^2 | 25, 33 |
| 21 | 2211.3 | 1-2^3, 2-3^2, 3-23^1, 5-6^1, 23-24^1, 24-25^3, 31-32^1 | 25, 32 |
| 24 | 2154.8 | 1-2^3, 2-3^2, 3-23^1, 5-6^1, 23-24^1, 24-25^3, 31-32^1, 32-33^2 | 25, 32 |

- **Key insight**: As reinforcement budget increases, the number of reinforced lines increases and strategies concentrate near critical loads. Lines 1-2 and 2-3 are reinforced in all non-zero-budget cases because they are the core power supply section near the upper-level grid. At higher budgets, the strategy expands to secondary lines near critical load nodes (23, 24, 25, 31, 32). The total cost decreases monotonically with budget as expected.
