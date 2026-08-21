# Table 7: Performance comparison of three methods

- **Source**: Table 7, Section 5.6 (Validity Analysis of The McCormick Relaxation Method)
- **Caption**: "Performance comparison of three methods."
- **Screenshot**: table7.png
- **Extraction type**: raw_table

Relaxation / solution-method comparison. Net profit in CNY 10^7. IPOPT = Interior Point Optimizer applied to the nonconvex model; Bilinear-Removed = the bilinear-term removal method of ref [30]; McCormick = the method proposed in this paper.

| Metric | IPOPT | Bilinear-Removed | McCormick |
|--------|-------|------------------|-----------|
| Annual Net Profit (CNY 10^7) | -- | 3.75 | 4.93 |
| Computing Time (h) | >5 | 1.59 | 2.52 |

Reported (Section 5.6): IPOPT could not obtain an optimal solution within 5 h. The bilinear-removed method is fastest but its result is "only 76% of that of McCormick method" (3.75 / 4.93 ≈ 0.76).
