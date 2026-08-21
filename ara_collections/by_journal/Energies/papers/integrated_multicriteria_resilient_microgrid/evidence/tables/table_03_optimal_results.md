# Table 3: Optimal Component Capacities, DPSP, LPPP, and TLCC

**Source**: Pages 18-19 of the published PDF.

**Caption**: The optimal component capacities, DPSP and LPPP, and their corresponding TLCCs for the first four best-ranked non-dominated solutions for each of the six considered cases.

**Content summary (top-ranked solutions only)**:

| Case | DPSP (%) | TLCC (US$) | LPPP (%) | PV (kW) | WT (kW) | BESS (kWh) |
|------|----------|------------|---------|---------|---------|------------|
| #1 (Base) | 0.48 | 10,377,384.54 | 6.26 | 1440 | 1850 | 4800 |
| #2 (TOU-VP) | 0.57 | 10,314,687.16 | 4.35 | 1530 | 1830 | 4200 |
| #3 (SSAP) | 0.06 | 9,649,293.00 | 1.33 | 1270 | 1840 | 3500 |
| #4 (Stoch) | 0.12 | 10,576,185.15 | 10.31 | 1480 | 2000 | 4900 |
| #5 (LSTM+TOU) | 0.36 | 10,378,836.97 | 5.05 | 1430 | 1930 | 3600 |
| #6 (LSTM+SSAP) | 0.04 | 10,066,405.65 | 2.05 | 1420 | 1920 | 3200 |

**Key findings from Table 3**:
- Case 3 (deterministic SSAP) achieves the lowest TLCC overall ($9.65M)
- Case 6 (stochastic LSTM+SSAP) achieves the best reliability (DPSP 0.04%) with the smallest BESS (3200 kWh)
- Case 4 (stochastic only) has the highest TLCC ($10.58M) and highest VRE curtailment (LPPP 10.31%)
- BESS capacity ranges from 3200 kWh (Case 6) to 4900 kWh (Case 4)

**Evidence file**: `tables/table_03_optimal_results.png`
