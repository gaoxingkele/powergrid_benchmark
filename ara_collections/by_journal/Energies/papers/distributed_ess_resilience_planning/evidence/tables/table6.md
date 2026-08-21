# Table 6: System-Level Electrical Performance Comparison

**Source:** Section 4.3, p.22 of the paper.
**Screenshot:** ![Table 6](tables/table6.png)

**Description:** Electrical performance metrics at energy storage nodes before and after DESS planning across the three cases. Reports peak-to-valley difference (%), frequency nonconformance rate (%), and voltage deviation (%) for each configured node.

**Claims supported:** C02, C03

**Results:**

| Case | Block | Load Type | Node | Original P-V (%) | Current P-V (%) | Freq. Violation (%) | Voltage Deviation (%) |
|------|-------|-----------|------|-----------------|-----------------|-------------------|---------------------|
| 1 | 7 | Residential | 20 | | | | |
| | 20 | Residential | 41 | 70.9 | 21.9 | 7.960 | 3.490 |
| | 32 | Residential | 70 | 75.2 | 24.1 | 1.900 | 7.810 |
| 2 | 26 | Residential | 49 | 72.0 | 30.6 | 6.950 | 9.490 |
| | 21 | Industrial | 121 | 74.9 | 36.9 | 9.700 | 6.330 |
| | 21 | Commercial | 157 | 79.2 | 43.0 | 5.340 | 8.230 |
| 3 | 26 | Residential | 49 | 77.3 | 34.0 | 5.410 | 8.140 |
| | 21 | Industrial | 121 | 74.9 | 36.9 | 9.700 | 6.330 |
| | 15 | Commercial | 147 | 75.1 | 38.2 | 6.030 | 8.540 |

**Key observation:** All cases significantly reduce the original peak-to-valley difference (from ~70–80% down to ~20–40%), demonstrating the effectiveness of DESS in load smoothing. Frequency violation rates and voltage deviations also show improvement after DESS deployment.

![Table 6](tables/table6.png)
