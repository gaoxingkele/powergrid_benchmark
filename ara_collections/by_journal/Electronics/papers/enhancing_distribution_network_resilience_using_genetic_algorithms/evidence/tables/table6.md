# Table 6 - Resilience Assessment

**Source**: Table 6, Section 6 (Results), page 11
**Caption**: "Resilience Assessment."
**Screenshot**: table6.png (second table on page 11, below the paragraph on the fault-induced DER trip at bus 3)
**Extraction type**: raw_table

| Metric              | Base Case | Optimized |
|---------------------|-----------|-----------|
| Min Voltage (pu)    | 0.88 | 0.94 |
| Overloaded Branches | 2    | 0    |
| Load Served (%)     | 89%  | 100% |

Notes: Contingency scenario — a fault-induced DER trip at bus 3. Three resilience metrics: minimum
bus voltage (depth of service degradation), number of overloaded branches (structural robustness),
and load-served ratio (continuity of supply). Under the DER outage the base case drops to 0.88 pu
min voltage, 2 overloaded branches, and 89% load served; the GA-optimized configuration holds
0.94 pu, 0 overloads, and 100% load served. Note these min-voltage figures (0.88→0.94) are the
contingency case and differ from the steady-state min voltage in Table 3 (0.92→0.97).
