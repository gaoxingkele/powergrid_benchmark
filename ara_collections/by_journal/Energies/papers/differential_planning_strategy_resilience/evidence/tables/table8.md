# Table 8: Comparison of Cost and Solve Time under Scenario Reduction

- **Source**: Page 20, Section 5.4
- **Screenshot**: `table8.png`
- **Claims supported**: C05
- **Data**:

| Reduction Scheme | Total Cost (10^4 CNY) | Error | Time (s) |
|-----------------|----------------------|-------|----------|
| No reduction | 2186.8 | / | 2711 |
| Reduce 2 states | 2172.3 | 0.67% | 1426 |
| Reduce 3 states | 2164.9 | 1.00% | 726 |
| Reduce 4 states | 1867.9 | 14.60% | 305 |

- **Key insight**: Reducing 3 fault states achieves an excellent trade-off: only 1.00% error in total cost while reducing computation time by 73.22% (from 2711s to 726s). Reducing 2 states yields even lower error (0.67%) with 47.4% time reduction. Reducing 4 states is unacceptable (14.60% error), indicating a threshold effect where too many important states are discarded. The pruning ratio alpha_cut = 0.95 effectively filters low-impact scenarios while preserving decision accuracy.
