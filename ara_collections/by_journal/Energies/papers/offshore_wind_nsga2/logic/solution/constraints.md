# Constraints

## State of Charge (SOC) Constraints
The battery must operate within safe charge/discharge limits to prevent damage:

```
SOC_min <= SOC(t) <= SOC_max
```

where SOC_min and SOC_max represent the minimum and maximum allowable state of charge, respectively.

## Power Constraints
The charging and discharging power must not exceed maximum limits to avoid system overheating:

```
0 <= P_c(t) <= P_c_max     (charging power)
0 <= P_dc(t) <= P_dc_max   (discharging power)
```

## Grid Code Constraints (Wind Farm Power Change Limits)
Based on Table 1, wind farm active power change must comply with:

| Installed Capacity P_N | Max 10-min Change | Max 1-min Change |
|------------------------|-------------------|------------------|
| P_N < 30 MW            | 10 MW             | 3 MW             |
| 30 <= P_N <= 150 MW    | P_N/3 MW          | P_N/10 MW        |
| P_N > 150 MW           | 50 MW             | 15 MW            |

For the 40 MW wind farm in this study: Max 10-min change = 13.33 MW, Max 1-min change = 4 MW.

## Decision Variable Ranges
- Rated power (P_es): 0 to 12 MW
- Rated capacity (S_es): 0 to 48 MWh
- Continuous working time range: 1 to 4 hours (implicitly constrains S_es/P_es ratio)

## Project Lifespan Constraints
- Total project lifespan: 25 years
- Battery cycle life: ~8000 cycles
- Battery service life: ~10 years
- Number of battery replacements over project lifespan: 2 (tau = 2)
