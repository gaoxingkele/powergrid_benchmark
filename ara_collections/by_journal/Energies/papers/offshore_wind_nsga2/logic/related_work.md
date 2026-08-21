# Related Work

## Energy Storage Sizing for Offshore Wind Farms

The paper builds upon prior work on electrochemical energy storage configuration for offshore wind farms. Paul et al. [10] proposed a multi-objective framework for BESS capacity optimization in large offshore wind farms considering battery cost, life, and turbine availability. Tian et al. [11] used hybrid hydrogen energy storage for smoothing offshore wind output volatility, finding that hydrogen systems significantly reduce economic viability. Wu et al. [12] proposed voltage control using reactive power coordination and electrochemical storage.

## Hybrid Energy Storage Approaches

Several studies examined hybrid storage combining batteries with supercapacitors or hydrogen. Lu et al. [16] applied wavelet decomposition to allocate high-frequency fluctuations to supercapacitors and low-frequency to batteries, reducing daily energy storage input costs by 2.79-3.84%. Lu et al. [17] evaluated a 2 MW wind farm with hybrid electrolytic cell, fuel cell, and supercapacitor system, achieving 41.1% annualized cost reduction. Li et al. [18] used deep reinforcement learning for electric-hydrogen hybrid storage control, reducing average daily fluctuation from 20.11 MW to 5.74 MW.

## Gap Addressed

The paper identifies two gaps in existing literature:
1. Few studies simultaneously address the relationship between output power volatility and investment cost for offshore wind farms with standalone battery storage.
2. Most existing studies do not consider the impact of electricity market participation and real-time spot trading on optimal storage configuration.

## Contribution Relative to Prior Work

This study uniquely combines:
- Multi-objective optimization (NSGA-II) for ESS sizing in offshore wind farms
- Battery life correction via multiple linear regression
- Three schemes progressing from basic cost-volatility trade-off to spot market arbitrage
- Systematic comparison with MOPSO as benchmark
