---
title: "Multi-Objective Optimization of Offshore Wind Farm Configuration for Energy Storage Based on NSGA-II"
authors:
  - name: "Xin Lin"
    affiliation: "Power Grid Planning Research Center, Guangxi Power Grid, Nanning, China"
  - name: "Wenchuan Meng"
    affiliation: "Energy Development Research Institute, China Southern Power Grid, Guangzhou, China"
  - name: "Ming Yu"
    affiliation: "Power Grid Planning Research Center, Guangxi Power Grid, Nanning, China"
  - name: "Zaimin Yang"
    affiliation: "Energy Development Research Institute, China Southern Power Grid, Guangzhou, China; College of Electrical Engineering, Zhejiang University, Hangzhou, China"
  - name: "Qideng Luo"
    affiliation: "Power Grid Planning Research Center, Guangxi Power Grid, Nanning, China"
  - name: "Zhi Rao"
    affiliation: "Energy Development Research Institute, China Southern Power Grid, Guangzhou, China"
  - name: "Jingkang Peng"
    affiliation: "School of Energy and Power Engineering, Huazhong University of Science and Technology, Wuhan, China"
  - name: "Yingquan Chen"
    affiliation: "School of Energy and Power Engineering, Huazhong University of Science and Technology, Wuhan, China"
year: 2025
venue: "Energies"
doi: "10.3390/en18123061"
ara_version: "1.0"
domain: "Energy Systems, Wind Power, Multi-Objective Optimization"
keywords:
  - "offshore wind power"
  - "multi-objective optimization"
  - "NSGA-II"
  - "power fluctuation suppression"
  - "energy storage configuration"
  - "electricity spot market"
  - "Pareto optimization"
  - "battery energy storage system"
  - "state of charge"
  - "peak-valley arbitrage"
claims_summary:
  - "NSGA-II effectively balances energy storage investment cost against wind power output fluctuation suppression in offshore wind farms."
  - "Energy storage battery life is primarily determined by rated capacity (positive correlation), not rated power."
  - "Optimal configuration under pure investment-volatility consideration is 4 MW rated power and 28 MWh rated capacity."
  - "Optimal configuration under spot market participation is 8 MW rated power and 37 MWh rated capacity."
  - "NSGA-II outperforms MOPSO in this multi-objective energy storage sizing problem, producing lower volatility per unit cost."
  - "Peak-valley arbitrage (Scheme 3) provides additional economic benefits over simple spot market participation (Scheme 2)."
  - "Battery life correction significantly alters the Pareto frontier, making it essential for realistic economic evaluation."
abstract: "The configuration of energy storage systems in offshore wind farms can effectively suppress fluctuations in wind power and enhance the stability of the power grid. However, the economic balance between the cost of energy storage systems and the fluctuations in wind power remains an urgent challenge to be addressed, especially against the backdrop of widespread spot trading in the electricity market. How to achieve effective wind power stabilization at the lowest cost has become a key issue. This paper proposes three different energy storage configuration strategies and adopts the non-dominated sorting genetic algorithm (NSGA-II) to conduct multi-objective optimization of the system. NSGA-II performed stably in dual-objective scenarios and effectively balanced the relationship between the investment cost of the energy storage system and power fluctuations through the explicit elite strategy. Furthermore, this study analyzed the correlation between the rated power and rated capacity of the energy storage system and the battery life, and corrected the battery life of the Pareto frontier solution obtained by NSGA-II. The research results show that when only considering the investment cost of the energy storage, the optimal configuration was a rated power of 4 MW and a rated capacity of 28 MWh, which could better balance the investment economy and power fluctuation. When further considering the participation of energy storage systems in the electricity spot market, the economic efficiency of the energy storage systems could be significantly improved through the fixed-period electricity price arbitrage method. At this point, the optimal configuration was a rated power of 8 MW and a rated capacity of 37 MWh. The corresponding project investment cost was CNY 242.77 million, and the annual fluctuation rate of the wind power output decreased to 17.84%."
collection: by_journal
journal: Energies
ownership_status: external_published_paper_not_project_original
local_pdf: "papers/literature/target_journal_related/pdfs/p6_nsga_bls_feasibility_review/p6_nsga_bls_feasibility_review__01__multi_objective_optimization_of_offshore_wind_farm_configura__84ad7c978c.pdf"
paper_type: research
page_count: 20
references_count: 30
---

# Multi-Objective Optimization of Offshore Wind Farm Configuration for Energy Storage Based on NSGA-II

## Overview

This paper addresses the multi-objective optimization problem of configuring battery energy storage systems (BESS) in offshore wind farms to simultaneously minimize investment cost and suppress wind power output fluctuations. The study employs NSGA-II (Non-dominated Sorting Genetic Algorithm II) to generate Pareto-optimal configurations of energy storage rated power and capacity. Three schemes are compared: (1) considering only investment cost vs. power fluctuation, (2) incorporating spot market electricity sales revenue, and (3) applying a peak-valley arbitrage strategy. The analysis includes battery life correction through multiple linear regression, and uses MOPSO as a benchmark algorithm. A 40 MW wind farm in Wan'an County, China serves as the case study, using 2023 operational data and 2024 Guangdong Province spot electricity prices.

## Layer Index

### Logic Layer
- `logic/problem.md` - Problem domain, scope, and formulation
- `logic/claims.md` - All claims (C01-C07) with full evidence bindings
- `logic/concepts.md` - Key technical concepts (10 entries)
- `logic/experiments.md` - Experiments (E01-E06)
- `logic/related_work.md` - Related work positioning
- `logic/solution/constraints.md` - Optimization constraints
- `logic/solution/algorithm.md` - NSGA-II algorithm description
- `logic/solution/methodology.md` - Three scheme configurations

### Source Layer
- `src/environment.md` - Computational and data environment

### Trace Layer
- `trace/exploration_tree.yaml` - Exploration tree of the paper's reasoning

### Evidence Layer
- `evidence/README.md` - Evidence directory guide
- `evidence/figures/figure1.png` - Figure 1: System structure diagram
- `evidence/figures/figure2.png` - Figure 2: NSGA-II flowchart
- `evidence/figures/figure3.png` - Figure 3: Pareto frontier (NSGA-II)
- `evidence/figures/figure4.png` - Figure 4: Influence of rated power/capacity on cost
- `evidence/figures/figure5.png` - Figure 5: Influence on output power fluctuation
- `evidence/figures/figure6.png` - Figure 6: Pareto front after life correction
- `evidence/figures/figure7.png` - Figure 7: Output power comparison (4MW/4MWh)
- `evidence/figures/figure8.png` - Figure 8: Output power comparison (10MW/40MWh)
- `evidence/figures/figure9.png` - Figure 9: SOC change curve (4MW)
- `evidence/figures/figure10.png` - Figure 10: SOC change curve (10MW)
- `evidence/figures/figure11.png` - Figure 11: Annual Pareto frontier by NSGA-II
- `evidence/figures/figure12.png` - Figure 12: Annual Pareto frontier by MOPSO
- `evidence/figures/figure13.png` - Figure 13: Spot electricity price on a typical day
- `evidence/figures/figure14.png` - Figure 14: Pareto frontiers of Scheme 2 and 3
- `evidence/tables/table1.md` - Table 1: Wind farm power change constraints
- `evidence/tables/table2.md` - Table 2: Cost parameters
- `evidence/tables/table3.md` - Table 3: Battery cycle times and service life
- `evidence/tables/table4.md` - Table 4: MOPSO parameters
- `evidence/tables/table5.md` - Table 5: xi values for NSGA-II
- `evidence/tables/table6.md` - Table 6: xi values for MOPSO
- `evidence/tables/table7.md` - Table 7: Optimal configuration comparison
- `evidence/tables/table8.md` - Table 8: Frontier comparison Scheme 2 vs 3
