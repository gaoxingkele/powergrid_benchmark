# Table 5: Probability of Each Scenario and Hardening Strategies with Different Budgets of Case 4 and Case 5

- **Source**: Page 17, Section 5.3
- **Screenshot**: `table5.png`
- **Claims supported**: C03
- **Data**:

| Budget (10^4 CNY) | Failure State Probabilities | Case 4 Strategy | Case 5 Strategy |
|-------------------|---------------------------|-----------------|-----------------|
| 12 | 0.17, 0.17, 0.17, 0.126, 0.126, 0.126 | 1-2^3, 2-3^2, 5-6^1, 31-32^1 | 1-2^3, 2-3^1, 5-6^1, 31-32^2 |
| 18 | 0.17, 0.17, 0.17, 0.126, 0.126, 0.126 | 1-2^3, 2-3^2, 3-4^2, 5-6^1, 3-23^1, 31-32^2 | 1-2^3, 2-3^2, 3-4^2, 5-6^1, 3-23^1, 23-24^1, 32-33^2 |
| 24 | 0.17, 0.17, 0.17, 0.126, 0.126, 0.126 | 1-2^3, 2-3^2, 3-4^2, 5-6^1, 3-23^1, 23-24^1, 24-25^3, 32-33^1 | 1-2^3, 2-3^2, 3-23^1, 5-6^1, 23-24^1, 24-25^3, 31-32^1, 32-33^2 |

- **Key insight**: Under DRO (Case 5), failure state probabilities shift toward more severe fault conditions (0.17 -> 0.153, 0.126 -> 0.164 for states 4-6) in the iterative process. The hardening strategies then prioritize lines that are most vulnerable in those severe states. For example, line 31-32 is hardened to level 2 in Case 5 at budget 12 (vs level 1 in Case 4) because it suffers longer outages in severe failure states.
