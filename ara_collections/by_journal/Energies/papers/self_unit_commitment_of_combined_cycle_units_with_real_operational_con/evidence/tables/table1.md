# Table 1: CCGT parameters

- **Source**: Table 1, Section 3 (Results and Discussion), pages 10–11
- **Caption**: "CCGT parameters." (table continues as "Table 1. Cont." on page 11)
- **Screenshot**: table1.png (page 10, first part) + table1_cont.png (page 11, continuation)
- **Extraction type**: raw_table
- **Object location**: Table 1 begins at the bottom of page 10 and continues at the top of page 11 ("Table 1. Cont.").

| Variable | Value | Unit |
|----------|-------|------|
| GCC (max, GĈC̄) | 800 | MW |
| GCC (min, G_CC) | 210 | MW |
| PAF | 15 | MW |
| AUXCC | 5 | MW |
| AUXGT | 0.45 | MW |
| AUXST | 2 | MW |
| RD/RU | 335 | MWh |
| PCC | 120 | USD/MWh |
| PBC | 500 | USD/MWh |
| CSC | 15,000 | USD |
| MUG | 2 | p.u. |
| STF | 0.613 | p.u. |
| NC | 5 | p.u. |
| NS | 2 | p.u. |
| t1 | t <= 16 | Hours |
| t2 | 16 < t <= 30 | Hours |
| t3 | t > 30 | Hours |
| KGC | 3 | Hours |

Notes:
- GCC max/min are the combined-cycle plant output bounds (overbar = max, underbar = min in the paper).
- MUG = minimum number of gas units to start up one steam unit.
- STF = steam-to-gas output relation (constant assumed by the model).
- t1/t2/t3 = thermal-state time windows (hot/warm/cold) governing startup ramp selection.
- KGC = hours the steam turbine is in a cold state / gas-turbine hours required for a cold startup.
