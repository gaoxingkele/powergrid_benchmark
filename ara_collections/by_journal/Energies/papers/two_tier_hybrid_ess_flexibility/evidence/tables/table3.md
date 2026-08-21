# Table 3: Solution Results of Five Algorithms

**Source**: Page 20 of the original paper

**Description**: Performance comparison of COOT, PSO, DE, WAA, and IWAA algorithms over 30 experimental trials for solving the HESS bi-level planning problem. Metrics include best (optimal), average (mean), and standard deviation values for penalty costs and total costs.

## Data

| Metric | COOT | PSO | DE | WAA | IWAA |
|--------|------|-----|----|-----|------|
| **Penalty Costs** | | | | | |
| Best | 2.67e6 | 2.41e6 | 2.53e6 | 2.49e6 | **2.16e6** |
| Avg | 3.12e7 | 2.74e7 | 2.85e7 | 2.86e6 | **2.43e6** |
| Std | 2.64e6 | 2.37e6 | 2.11e7 | 2.34e6 | **1.95e6** |
| **Total Costs** | | | | | |
| Best | 9.64e6 | 9.97e6 | 9.59e6 | 9.06e6 | **8.58e6** |
| Avg | 1.22e7 | 1.35e7 | 9.85e6 | 9.42e6 | **8.74e6** |
| Std | 3.09e6 | 2.63e6 | 2.08e6 | 2.57e6 | **2.48e6** |

*Bolded entries indicate optimal results.*

## Key Insights

1. **IWAA achieves best performance across all metrics** except total cost standard deviation (where IWAA is second-best, close to DE)
2. For penalty costs: IWAA best is 13.3% lower than suboptimal WAA; 19.1% lower than worst COOT
3. For total costs: IWAA best is 10.5% lower than suboptimal DE
4. IWAA average total cost is 7.2% lower than WAA
5. IWAA standard deviation for penalty costs is 17.7% lower than PSO
6. Results confirm IWAA's superiority in solution quality, stability, and convergence robustness
