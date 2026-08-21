# Table A1 - Sampling parameters of EV

**Source**: Table A1, Appendix A, page 13
**Caption**: "Sampling parameters of EV."
**Screenshot**: tableA1.png (table at top of page 13, above the References list)
**Extraction type**: raw_table

Notation: `N(µ, σ)` = normal distribution (arrival/departure hour, initial SOC); `U(a, b)` = uniform distribution (SOC bounds and EV counts). `T_arrive`/`T_leave` are arrival/departure times (hours); `S0` is initial state of charge. Remaining columns give the number of EVs assigned within charging stations 1–4 (0 = none of that EV type at that station).

| EV | T_arrive | T_leave | S0 | # EVs within 1 charging station | # EVs within 2 charging stations | # EVs within 3 charging stations | # EVs within 4 charging stations |
|----|----------|---------|-----|------|------|------|------|
| 1 | N (18, 4) | N (8, 4) | U (0.4, 0.6) | U (180, 210) | U (180, 210) | 0 | U (380, 400) |
| 2 | N (21, 1) | N (7, 1) | U (0.2, 0.4) | U (190, 220) | U (90, 120) | U (90, 120) | 0 |
| 3 | N (9, 2) | N (17, 2) | U (0.4, 0.6) | 0 | U (380, 400) | U (380, 400) | 0 |
