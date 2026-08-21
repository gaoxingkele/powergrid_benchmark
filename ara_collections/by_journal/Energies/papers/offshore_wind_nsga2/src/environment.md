# Computational Environment

## Software
- **Programming language**: Python 3.8
- **Algorithm framework**: NSGA-II implemented via SYS module (implied custom implementation or geatpy/pymoo-based)
- **Libraries**: Standard Python scientific computing stack (assumed: numpy, matplotlib for visualization)

## Hardware
- Not specified in the paper

## Data Sources
- **Wind farm data**: Output power data from a 40 MW wind farm in Wan'an County, Jiangxi Province, China, for the full year 2023
- **Wind turbines**: 16 turbines, each 2.5 MW rated power
- **Spot electricity prices**: 2024 data published by the Energy Bureau of Guangdong Province, China
- **Cost parameters**: Derived from reference [24] (MeShengwei, 2022, "Energy Storage", China Machine Press)

## Parameter Values
### Cost Parameters (Table 2)
| Parameter | Value | Unit |
|-----------|-------|------|
| Power cost factor (k_p) | 5,000,000 | CNY/MW |
| Capacity cost factor (k_q) | 6,000,000 | CNY/MWh |
| O&M unit price (k_F) | 500 | CNY/MW |
| Discharge price (k_V) | 300 | CNY/MWh |
| Annual cost decline rate (alpha) | 5 | % |
| Battery replacements (tau) | 2 | times |
| Battery service life (a) | 10 | years |
| Battery cycle life (N) | 8000 | cycles |

### NSGA-II Parameters
| Parameter | Value |
|-----------|-------|
| Population size | 20 |
| Offspring per generation | 60 |
| Generations | 300 |
| Crossover probability | 0.5 |
| Mutation probability | 0.5 |
| P_es range | [0, 12] MW |
| S_es range | [0, 48] MWh |

### MOPSO Parameters (Table 4)
| Parameter | Value |
|-----------|-------|
| Population size (POP SIZE) | 50 |
| Archive size (ARCHIVE SIZE) | 100 |
| Generations (NGEN) | 300 |
| Inertia weight (W) | 0.4 |
| Cognitive coefficient (C1) | 1.5 |
| Social coefficient (C2) | 1.5 |

## Project Assumptions
- Energy storage battery does not experience performance degradation over individual charge-discharge cycles
- Battery replacement occurs immediately at end of service life with no downtime
- Constant discount rate i applied to replacement cost calculations
- Grid code requirements (Table 1) are mandatory constraints
