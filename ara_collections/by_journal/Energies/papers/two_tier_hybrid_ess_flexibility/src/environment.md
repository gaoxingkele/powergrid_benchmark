# Environment

## Computational Platform
| Component | Specification |
|-----------|---------------|
| OS | Windows 10 |
| CPU | Intel Core i7-11800H |
| RAM | 16 GB |
| Simulation Platform | MATLAB R2024b |

## Test System
- **Network**: Modified IEEE 39-bus transmission system (220 kV)
- **Reference bus**: Node 1 (upstream grid connection via substation)
- **Thermal generation**: Nodes 31 and 33 (3500 MW total)
- **PV generation**: Node 30
- **Wind generation**: Nodes 36, 37, 38

## Data Sources
| Data Type | Source |
|-----------|--------|
| Load profiles | Real operational data from Southwest China power grid company (2023) |
| Wind generation | Historical data from regional wind farms |
| PV generation | Historical data from regional PV plants |
| Grid parameters | IEEE 39-bus standard data with regional modifications |
| ESS cost parameters | Table 1 (from industry sources [24]) |

## Geographical Context
| Parameter | Value |
|-----------|-------|
| Supply area | 12,735 km^2 |
| Population served | 5.68 million |
| Customers | 2.33466 million |
| Annual sales (2023) | 31.41 billion kWh |
| Daily peak supply | 106 million kWh |
| Peak-valley load difference | 3091 MW |

## Key Parameters
| Parameter | Value |
|-----------|-------|
| Li-ion unit capacity cost | 3000 CNY/KWh |
| Li-ion unit power cost | 9000 CNY/KW |
| Flow battery unit capacity cost | 5000 CNY/KWh |
| Flow battery unit power cost | 3600 CNY/KW |
| Discount factor | 6% |
| Li-ion expected life | 20 years |
| Flow battery expected life | 30 years |
| Li-ion annual O&M factor | 0.06 CNY/Wh |
| Flow battery annual O&M factor | 0.065 CNY/Wh |
| Flexibility penalty cost | 1.5 CNY/KWh |

## Reproducibility Notes
- The paper uses real operational data from a specific Chinese regional grid that is not publicly available due to confidentiality.
- The modified IEEE 39-bus network parameters are standard, but specific modifications (thermal/PV/wind node assignments) are described.
- MATLAB R2024b was used; the IWAA algorithm code, PSO-VMD implementation, and all optimization routines would require custom implementation from the mathematical descriptions provided.
- Data availability: Contact corresponding author (jxg@kust.edu.cn) for datasets.
