# Table 6: Result Comparison under Different Confidence Sets

- **Source**: Page 18, Section 5.3
- **Screenshot**: `table6.png`
- **Claims supported**: C03
- **Data**:

| alpha_1 | alpha_infinity = 0.5 | alpha_infinity = 0.9 | alpha_infinity = 0.99 |
|---------|---------------------|---------------------|----------------------|
| 0.2 | 2337.9 | 2350.4 | 2366.3 |
| 0.5 | 2338.1 | 2350.6 | 2367.2 |
| 0.9 | 2338.1 | 2352.5 | 2368.3 |

Values are total cost (10^4 CNY).

- **Key insight**: Higher confidence levels (larger ambiguity sets) increase total cost. alpha_infinity has a stronger effect on cost than alpha_1: at alpha_1=0.2, cost goes from 2337.9 to 2366.3 (+28.4) when alpha_infinity rises from 0.5 to 0.99; at alpha_infinity=0.5, cost goes from 2337.9 to 2338.1 (+0.2) when alpha_1 rises from 0.2 to 0.9. This indicates that the l-infinity norm (maximum per-scenario deviation) is the binding constraint.
