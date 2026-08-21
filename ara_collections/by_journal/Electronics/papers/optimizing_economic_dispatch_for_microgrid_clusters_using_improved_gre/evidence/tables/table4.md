# Table 4 - Comparison of the effects of various chaotic mappings

**Source**: Table 4, Section 4.2 in "Optimizing Economic Dispatch for Microgrid Clusters Using Improved Grey Wolf Optimization" (Electronics 2024, 13, 3139)
**Caption**: "Comparison of the effects of various chaotic mappings."
**Screenshot**: table4.png
**Location on page**: Page 13 (PDF page 13), top of page.
**Extraction type**: raw_table

| Type of Chaotic Mapping | Optimal Fitness Value | Runtime/s |
| --- | --- | --- |
| Tent | 2.0920 × 10^3 | 9.1720009 |
| Sine | 2.0597 × 10^3 | 10.496083 |
| Chebyshev | 1.6895 × 10^3 | 11.616561 |
| Logistic | 1.7150 × 10^3 | 7.9097413 |
| Traditional GWO | 1.9030 × 10^3 | 10.534876 |

Notes: Chebyshev achieves the lowest (best) fitness value; Logistic achieves the lowest (best) runtime. The paper judges the fitness gap between Chebyshev and Logistic "negligible" and selects Logistic on the efficiency-precision trade-off.
