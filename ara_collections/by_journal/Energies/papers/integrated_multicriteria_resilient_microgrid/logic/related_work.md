# Related Work: Citation Footprint

## Core References (Directly Used in This Study)

The paper builds on 53 references spanning the following research areas:

### Microgrid Planning and Optimization
1. **Salehi et al. (2022)** — IEEE Access: Comprehensive review of control strategies and optimization methods for individual and community microgrids. Establishes the foundation for VRE-based microgrid planning. [Ref 1]
2. **Yang & Su (2021)** — Energy: Robust optimization of microgrid under renewable generation and load demand uncertainty. Motivates the uncertainty modeling approach. [Ref 2]
3. **Kiptoo et al. (2023)** — Energies: Previous work by the same group on optimal capacity and operational planning for renewable energy microgrid with different DSM strategies. Direct precursor to this study. [Ref 6]
4. **Kaluthanthrige & Rajapakse (2021)** — IJEPES: Demand response integrated day-ahead energy management for remote off-grid hybrid renewable systems. Framework basis for integrated DRP optimization. [Ref 12]

### Demand Response and DSM
5. **Kamwa et al. (2023)** — Energies: Review of integrated DRP programs in energy hubs. Context for DRP classification. [Ref 7]
6. **Shariatzadeh, Mandal & Srivastava (2015)** — RSER: Review of demand response for sustainable energy systems. Foundational DRP reference. [Ref 8]
7. **Kiptoo et al. (2019)** — Future Internet: Techno-economic benefits of flexible demand resources scheduling for renewable energy smart microgrids. Prior work on FDR modeling. [Ref 10]
8. **Cai et al. (2022)** — Energy: Dynamic pricing mechanism design for smart residential communities. Price elasticity modeling approach. [Ref 15]
9. **Yousefi et al. (2011)** — Energy: Optimal real-time pricing in agent-based retail markets. Price elasticity formulation basis. [Ref 18]

### LSTM and Forecasting
10. **Sagheer & Kotb (2019)** — Scientific Reports: Unsupervised pre-training of deep LSTM-based stacked autoencoder for multivariate time series forecasting. LSTM architecture reference. [Ref 25]
11. **Gu et al. (2021)** — Renewable Energy: Short-term forecasting of wind power using LSTM, cloud model, and non-parametric kernel density estimation. Wind forecasting methodology. [Ref 27]
12. **Huang et al. (2022)** — Energy: Time series forecasting for hourly PV power using conditional GAN and Bi-LSTM. PV forecasting reference. [Ref 28]

### Monte Carlo and Uncertainty Modeling
13. **Tavakoli & Karimi (2023)** — IET RPG: Monte-Carlo-based stochastic scenarios for optimal energy management of renewable energy hubs. MCS methodology. [Ref 31]
14. **Zhang et al. (2022)** — Applied Energy: Comprehensive wind speed prediction system based on Monte Carlo and AI. Uncertainty quantification approach. [Ref 32]
15. **Furukakoi et al. (2018)** — Applied Energy: Multi-objective unit commitment with PV uncertainty. Prior work on uncertainty in VRE systems. [Ref 43]
16. **Mo et al. (2019)** — Sustainability: Stochastic unit commitment with PV uncertainty. Scenario generation framework. [Ref 44]

### Multi-Objective Optimization
17. **Vaka & Matam (2022)** — Energy Storage: Optimal sizing of hybrid renewable energy systems using multi-objective technique. MOPSO application context. [Ref 33]
18. **Konneh et al. (2019)** — Sustainability: Multi-criteria decision maker for grid-connected hybrid renewable energy systems using MOPSO. Direct methodology reference for MOPSO implementation. [Ref 34]
19. **Yoon & Kim (2017)** — Expert Systems with Applications: The behavioral TOPSIS. TOPSIS methodology reference. [Ref 35]
20. **Tsou (2008)** — Expert Systems with Applications: Multi-objective inventory planning using MOPSO and TOPSIS. Combined MOPSO-TOPSIS approach. [Ref 36]

### Techno-Economic Parameters and Case Study Data
21. **Climate data**: Meteoblue weather data for Marsabit, Kenya. [Ref 45]
22. **Solar data**: PVGIS (European Commission Joint Research Centre). [Ref 46]
23. **Kenya power sector data**: Kenya Power Generation and Transmission Master Plan. [Ref 47]
24. **Kenya LCPDP**: Updated Least Cost Power Development Plan 2017-2037. [Ref 48]
25. **BESS cost data**: Dhundhara et al. (2018) — Energy Conversion and Management. [Ref 49]
26. **BESS levelized cost**: Perkins (2018) — Energy Conversion and Management. [Ref 50]
27. **DRP case study**: Singh & Kumar (2023) — Energy: Hybrid renewable energy with BESS and EV demand response. [Ref 51]
28. **Kenya tariff**: EPRA Kenya tariff setting. [Ref 52]
29. **Price elasticity**: Nayak et al. (2021) — SETA: Operational strategy for grid-connected AC microgrid under uncertainty. Elasticity coefficients. [Ref 53]

## Research Gaps Addressed

1. No prior study jointly optimized capacity sizing AND operational planning under uncertainty with advanced DRP + LSTM forecasting in a single integrated framework.
2. The SSAP (shortage/surplus adaptive pricing) DRP mechanism had not been proposed or evaluated against TOU-based approaches for VRE microgrids.
3. The synergistic effect of LSTM forecast accuracy on MCS uncertainty bounds for adaptive pricing DRP had not been quantified.
4. The three-way trade-off characterization (TLCC vs DPSP vs LPPP) under deterministic vs stochastic planning with and without DRP had not been systematically compared across six cases in a single location.
