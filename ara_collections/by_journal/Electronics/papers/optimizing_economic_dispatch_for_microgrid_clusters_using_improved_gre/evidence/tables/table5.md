# Table 5 - Comparison of improved GWO (CDGWO) with common intelligent optimization algorithms

**Source**: Table 5, Section 4.3.1 in "Optimizing Economic Dispatch for Microgrid Clusters Using Improved Grey Wolf Optimization" (Electronics 2024, 13, 3139)
**Caption**: "Comparison of improved GWO (CDGWO) with common intelligent optimization algorithms."
**Screenshot**: table5.png
**Location on page**: Page 14 (PDF page 14), top of page.
**Extraction type**: raw_table

| Intelligent Optimization Algorithm | Optimal Fitness Value | Runtime/s | Number of Iterations at Convergence | Convergence Variance |
| --- | --- | --- | --- | --- |
| FA | 1.425 × 10^3 | 1100.305307 | 70 | 132.656897 |
| PSO | 2.147 × 10^3 | 27.753490 | 90 | 213.926534 |
| WOA | 3.045 × 10^3 | 26.265349 | 350 | 587.452367 |
| GWO | 1.903 × 10^3 | 10.534876 | 93 | 196.567398 |
| GA | 1.576 × 10^3 | 103.635457 | 56 | 206.875623 |
| SA | 2.803 × 10^3 | 52.786543 | 130 | 670.246676 |
| CDGWO | 1.044 × 10^3 | 6.906439 | 65 | 48.678354 |

Notes: CDGWO attains the lowest optimal fitness value, the lowest runtime, and the lowest convergence variance of the seven algorithms. GA reaches convergence in the fewest iterations (56) but at higher fitness/variance and much higher runtime; CDGWO converges in 65 iterations. CDGWO runtime is 3.6 s shorter than traditional GWO (10.534876 − 6.906439 = 3.628437 s).
