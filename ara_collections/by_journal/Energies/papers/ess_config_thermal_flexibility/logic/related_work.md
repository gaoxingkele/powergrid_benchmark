# Related Work

## RW01: Li et al., 2024
- **DOI**: 10.35833/MPCE.2023.000716
- **Type**: baseline
- **Delta**: Proposed optimal operation with dynamic partitioning for centralized shared ESS with large-scale RE integration. Provides background on ESS operational strategies that the current work extends by adding TCL flexibility.
- **Claims affected**: C01, C03
- **Adopted elements**: ESS operational framework concept

## RW02: Abomazid et al., 2022
- **DOI**: 10.1109/TSTE.2021.3137832
- **Type**: baseline
- **Delta**: Optimal energy management for hydrogen energy facility with battery ESS and PV. Shows the cost/reliability framing for hybrid energy storage that motivates the need for better configuration methods.
- **Claims affected**: C03
- **Adopted elements**: ESS cost modeling approach

## RW03: Hou et al., 2021
- **DOI**: 10.1109/TIA.2021.3130707
- **Type**: baseline
- **Delta**: Multisource ESS optimal dispatch among electricity, hydrogen, and heat networks. Provides multi-energy context but does not address TCL flexibility.
- **Claims affected**: C01
- **Adopted elements**: Multi-energy coordination perspective

## RW04: Hossain et al., 2024
- **DOI**: 10.1109/TIA.2024.3481934
- **Type**: baseline
- **Delta**: Component sizing for supercapacitor-hydrogen hybrid ESS for wind dispatch. Establishes the ESS sizing optimization framing.
- **Claims affected**: C03
- **Adopted elements**: Sizing optimization methodology

## RW05: Zhuang et al., 2024
- **DOI**: 10.35833/MPCE.2023.000192
- **Type**: baseline
- **Delta**: Multi-timescale resource allocation with long-term contracts and real-time rental for shared ESS. Provides economic models for ESS operation.
- **Claims affected**: C01
- **Adopted elements**: ESS economic analysis framework

## RW06: Islam et al., 2024
- **DOI**: 10.1109/ACCESS.2024.3456251
- **Type**: baseline
- **Delta**: Comprehensive review on ESS role in improving power system reliability and stability. Contextualizes the importance of ESS for frequency stability.
- **Claims affected**: C03
- **Adopted elements**: Frequency stability motivation

## RW07: Han et al., 2024
- **DOI**: 10.1109/TSG.2024.3472298
- **Type**: baseline
- **Delta**: Optimal planning of multi-microgrid with shared ESS based on capacity leasing and energy sharing. Addresses multi-actor ESS planning without TCL integration.
- **Claims affected**: C01
- **Adopted elements**: Multi-microgrid ESS planning perspective

## RW08: Kong et al., 2025
- **DOI**: 10.35833/MPCE.2024.000241
- **Type**: baseline
- **Delta**: Two-stage optimal scheduling with hydrogen storage considering operation sequences. Represents ESS scheduling approaches the current work builds on.
- **Claims affected**: C03
- **Adopted elements**: Scheduling framework

## RW09: Guo et al., 2022
- **DOI**: 10.1109/TSTE.2022.3219525
- **Type**: baseline
- **Delta**: Two-timescale dynamic energy and reserve dispatch with wind power and ESS. Addresses ESS-wind coordination without load flexibility.
- **Claims affected**: C03
- **Adopted elements**: Dispatch modeling techniques

## RW10: Zhang et al., 2024
- **DOI**: 10.1109/TCE.2024.3408270
- **Type**: bounds
- **Delta**: Stochastic bi-level optimal allocation of intelligent buildings considering ESS sharing services. Most closely related to the current work as it addresses building energy management with ESS, but uses a stochastic bi-level approach rather than multi-objective optimization with TCL flexibility explicitly modeled.
- **Claims affected**: C01, C04
- **Adopted elements**: Building-ESS coordination concept; stochastic approach superseded by explicit TCL modeling in the current work

## RW11: Zhai et al., 2025
- **DOI**: 10.1016/j.apenergy.2025.125271
- **Type**: extends
- **Delta**: Risk-averse energy management for integrated electricity and heat systems with building heating vertical imbalance. Uses building thermal dynamics for energy management, which the current work extends to cooling (air conditioning) in the ESS configuration context.
- **Claims affected**: C01, C04
- **Adopted elements**: Building thermal dynamic modeling approach

## RW12: Lu et al., 2024
- **DOI**: 10.1109/ACCESS.2024.3355260
- **Type**: baseline
- **Delta**: Optimizing grid-connected multi-microgrid with shared ESS. Provides ESS-sharing optimization that the current work extends by adding load flexibility.
- **Claims affected**: C01
- **Adopted elements**: Shared ESS optimization framework

## RW13: Zhang et al., 2022
- **DOI**: Not specified
- **Type**: baseline
- **Delta**: Optimal operation of micro-energy grids considering shared ESS and balanced profit allocations. Provides the micro-energy grid context.
- **Claims affected**: C01
- **Adopted elements**: Profit allocation methodology

## RW14: Wang et al., 2024
- **DOI**: 10.1109/TIA.2024.3369846
- **Type**: baseline
- **Delta**: Day-ahead and intraday joint optimal dispatch in active distribution network with centralized/distributed ESS coordination.
- **Claims affected**: C03
- **Adopted elements**: ESS dispatch coordination

## RW15: Qi et al., 2017
- **DOI**: 10.1109/TSG.2017.2742045
- **Type**: baseline
- **Delta**: Decentralized optimal operation of AC/DC hybrid distribution grids.
- **Claims affected**: C01
- **Adopted elements**: Grid modeling framework

## RW16: Lu et al., 2024
- **DOI**: 10.1016/j.renene.2024.120898
- **Type**: bounds
- **Delta**: Optimization method for multi-port AC/DC flexible integrated systems based on improved pelican optimization algorithm. Direct precursor to the current work's algorithm development — showed strong global search but suffered from long convergence time, motivating the hybrid POA-GWO-CSO approach.
- **Claims affected**: C02
- **Adopted elements**: POA baseline algorithm; GWO and CSO additions are the novel extensions in the current work

## RW17: Gan & Low, 2014
- **DOI**: 10.1109/TPWRS.2014.2313511
- **Type**: baseline
- **Delta**: Optimal power flow in DC networks. Foundational for power flow modeling used in the grid constraints.
- **Claims affected**: C01
- **Adopted elements**: Power flow constraint formulation

## RW18–RW21: Nagpal et al., 2022; Yang & Song, 2024; Yan & Chen, 2023; Xia et al., 2024
- **Type**: baseline
- **Delta**: Each addresses hierarchical ESS management, energy sharing, charging station coordination, or agricultural load flexibility in distribution networks. Collectively provide the broader ESS operational background.
- **Claims affected**: C01
- **Adopted elements**: Operational and coordination concepts

## RW22: Wang et al., 2020
- **DOI**: 10.1109/TSG.2020.2968301
- **Type**: baseline
- **Delta**: Flexibility estimation and control of thermostatically controlled loads with lock time for regulation service. Provides the TCL modeling baseline.
- **Claims affected**: C04
- **Adopted elements**: TCL flexibility concept; the current work applies it within ESS optimization rather than standalone regulation service

## RW23: Hao et al., 2017
- **DOI**: 10.1109/TSG.2017.2716944
- **Type**: baseline
- **Delta**: Optimal coordination of building loads and ESS for power grid and end-user services. Directly related — coordinates building loads with ESS — but does not formulate as multi-objective configuration optimization.
- **Claims affected**: C01, C04
- **Adopted elements**: Building load-ESS coordination concept

## RW24: Chen et al., 2023
- **DOI**: 10.1109/TPWRD.2023.3344343
- **Type**: baseline
- **Delta**: Two-stage stochastic programming for resilience enhancement with mobile ESS.
- **Claims affected**: C03
- **Adopted elements**: ESS investment cost modeling components (installation, residual value)

## RW25: Bai et al., 2023
- **DOI**: 10.1109/OAJPE.2023.3277274
- **Type**: baseline
- **Delta**: Online multi-level EMS for commercial building microgrids with multiple generation and storage.
- **Claims affected**: C01
- **Adopted elements**: Multi-level optimization concept

## RW26: Wu et al., 2021
- **DOI**: Not specified (Power System Technology, Chinese)
- **Type**: baseline
- **Delta**: Bi-level optimal configuration for combined cooling, heating, and power multi-microgrids based on ESS service. Source of the Shanxi Province summer day dataset.
- **Claims affected**: E01
- **Adopted elements**: Dataset (Shanxi Province typical summer day data)

## RW27: Wen et al., 2019
- **DOI**: Not specified (High Voltage Engineering, Chinese)
- **Type**: baseline
- **Delta**: Deployment optimization with control for battery ESS participating in primary frequency regulation considering calendar life. Source for ESS lifetime assumption (10.5 years).
- **Claims affected**: E01
- **Adopted elements**: ESS lifetime parameter
