# Table 1 - Versions of the COA algorithm created using the FDB method

**Source**: Table 1 in "Enhanced Coati Optimization Algorithm for Static and Dynamic Transmission Network Expansion Planning Problems", §III-B (p.35076)
**Caption**: "Versions of the COA algorithm created using the FDB method."
**Screenshot**: table1.png (top of page; the table sits above Algorithm 1)
**Extraction type**: raw_table

This is a definitional table specifying where the FDB selection replaces a term (`x_{i,j}` → `x_{FDB,j}`) in COA's update equations to create each variant.

| Equation | Region where FDB selection is applied | Variation |
|----------|----------------------------------------|-----------|
| Equation (17) | `X_i^{P1} : x_ij^{P1} = x_{FDB,j} + r·(Iguana_j − I·x_{i,j})`, i=1..N/2, j=1..m (FDB in the exploration tree-climbing update) | FDBCOA1 |
| Equation (19) | `x_{i,j}^{P1} = x_{i,j} + r·(Iguana_j^G − I·x_{i,j})` if F_{Iguana^G} < F_i ; else `x_{i,j} + r·(x_{FDB,j} − Iguana_j^G)`, i=N/2+1..N (FDB in the *else* branch of the ground update) | FDBCOA2 |
| Equation (19) | `x_{i,j}^{P1} = x_{FDB,j} + r·(Iguana_j^G − I·x_{i,j})` if F_{Iguana^G} < F_i ; else `x_{i,j} + r·(x_{i,j} − Iguana_j^G)`, i=N/2+1..N (FDB in the *if* branch base term) | FDBCOA3 |

**Note**: Table 1 is paired with Algorithm 1 (Pseudo-Code of Fitness Distance Balance Based Coati Optimization Algorithm) on the same page; the pseudocode is transcribed in `logic/solution/algorithm.md`.
