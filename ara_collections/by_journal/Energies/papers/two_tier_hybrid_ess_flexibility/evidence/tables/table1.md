# Table 1: Energy Storage Parameter Settings

**Source**: Page 18 of the original paper

**Description**: Economic and technical parameters for lithium-ion battery and flow battery energy storage systems used in the planning model. These parameters define the cost structure and operational limits for both storage types.

## Data

| Parameter | Lithium-Ion Battery | Flow Battery |
|-----------|-------------------|--------------|
| Unit capacity cost (CNY/KWh) | 3000 | 5000 |
| Unit power cost (CNY/KW) | 9000 | 3600 |
| Present value of funds discount factor | 6% | 6% |
| Expected operational life (years) | 20 | 30 |
| Annual maintenance cost factor (CNY/Wh) | 0.06 | 0.065 |
| System inflexibility unit penalty cost (CNY/KWh) | 1.5 | 1.5 |
| Energy storage SOC range (%) | [20, 80] | [10, 90] |

## Significance

These parameters drive the economic comparison between the two storage technologies. Notably:
- Li-ion has lower capacity cost but higher power cost
- Flow battery has longer expected life (30 vs 20 years)
- Li-ion has a narrower SOC operating range
- The flexibility penalty cost applies equally to both types
