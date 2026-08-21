# Related Work Typed Dependency Graph

## RW01: Decision-Dependent Uncertainty Modeling

- **Type**: imports
- **Delta**: This paper adopts the DDU concept from [17,18] and extends it to multi-level line hardening for distribution networks under extreme weather. Prior work [19] applied DDU to network expansion planning; [20] combined DRO with DDU for wildfire risk. This paper is the first to integrate DDU with multi-level distributionally robust hardening for typhoon-induced failures.
- **Source references**: [17] Giannelos et al. 2018 (Option Value of Demand-Side Response Schemes Under Decision-Dependent Uncertainty); [18] Giannelos et al. 2018 (Endogenously Stochastic Demand Side Response); [19] Giannelos et al. 2025 (A stochastic optimization model for network expansion planning under exogenous and endogenous uncertainty); [20] Pianco et al. 2025 (Decision-Dependent Uncertainty-Aware Distribution System Planning Under Wildfire Risk)

## RW02: Transmission Defense Hardening Under DDU

- **Type**: imports
- **Delta**: Reference [14] (Zhang et al. 2023) proposed DDU-based hardening for transmission networks against typhoons. This paper extends the DDU hardening concept to distribution networks, which have different topology (radial vs meshed), operational constraints (distflow, voltage limits), and additional resilience resources (EVs, MEGs, demand response).
- **Source references**: [14] Zhang, W.; Shao, C.; Hu, B.; Xie, K.; Siano, P.; Li, M.; Cao, M. Transmission Defense Hardening Against Typhoon Disasters Under Decision-Dependent Uncertainty. IEEE Trans. Power Syst. 2023, 38, 2653-2665.

## RW03: Single-Level vs Multi-Level Line Hardening

- **Type**: extends
- **Delta**: References [6,7] used single-level (binary) hardening where a line is either hardened or not. This paper extends to three discrete hardening levels with graduated costs and failure-probability coefficients, enabling differential (targeted) resource allocation.
- **Source references**: [6] Tian et al. 2024 (Line hardening strategies for resilient power systems); [7] He et al. 2018 (Robust Network Hardening Strategy for Enhancing Resilience)

## RW04: Robust and Stochastic Planning Baselines

- **Type**: baseline
- **Delta**: References [9] (two-stage robust optimization) and [10] (stochastic pre-disaster planning) serve as baselines that this paper improves upon by combining distributionally robust optimization with DDU. Compared to pure robust optimization, DRO avoids excessive conservatism; compared to pure stochastic programming, DRO handles distributional ambiguity.
- **Source references**: [9] Yang et al. 2022 (Two stage affinely adjustable robust optimal scheduling); [10] Hou et al. 2023 (Stochastic pre-disaster planning and post-disaster restoration)

## RW05: Coupled Power-Transportation Planning

- **Type**: extends
- **Delta**: Reference [11] (Gan et al. 2022) modeled coupled power distribution and transportation systems. This paper focuses solely on the distribution network but integrates additional resilience measures (EV-V2G, MEG, demand response) that the coupled model does not address.
- **Source references**: [11] Gan et al. 2022 (A Tri-Level Planning Approach to Resilient Expansion and Hardening of Coupled Power Distribution and Transportation Systems)

## RW06: Differential Planning (Author's Prior Work)

- **Type**: imports
- **Delta**: Reference [12] (Chen et al. 2025, the authors' own ICPST paper) introduced the differential pre-event planning concept. This paper operationalizes it through a rigorous DRO-DDU mathematical framework with Sobol' interpretability analysis.
- **Source references**: [12] Chen, X.; Liu, L.; Kang, X.; Li, S.; Huang, X.; Ma, Y.; Ma, Y.; Qin, W. Differential pre-event planning for power-transportation network resilience against cascading disruption. ICPST 2025.

## RW07: DRO with DDU in Power Systems

- **Type**: imports
- **Delta**: References [22,23] applied DRO with DDU to generation dispatch and renewable integration. This paper adapts the DRO-DDU framework to the different context of distribution network hardening, where the decision-dependent variable is line failure probability rather than generation output.
- **Source references**: [22] Huang et al. 2023 (A multistage distributionally robust optimization approach for generation dispatch); [23] Zhang et al. 2025 (On Decision-Dependent Uncertainties in Power Systems with High-Share Renewables)

## RW08: Multi-Energy and Mobile Resource Resilience

- **Type**: baseline
- **Delta**: Reference [13] (Li et al. 2023) considered multi-energy distribution network hardening; [8] (Pan et al. 2025) studied mobile energy storage for port distribution networks. This paper compares against these approaches and shows that coordinated optimization of MEG + EV + DR + reconfiguration + hardening outperforms individual measures.
- **Source references**: [13] Li et al. 2023 (Robust expansion planning and hardening strategy of meshed multi-energy distribution networks); [8] Pan et al. 2025 (Resilience enhancement strategy for port distribution networks considering mobile energy storage)

## Dependency Graph Summary

```
 [17,18] ---> [19] ----> This  <--- [20]
   (DDU)       (DDU)     paper      (DRO+DDU)
                            |
                            v
                       [14] (transmission DDU hardening -> extended to distribution)
                            |
               +------------+------------+
               |            |            |
              [6,7]       [9,10]       [11]
          (single-level)  (baselines)  (coupled systems)
               |            |            |
               v            v            v
           extended      improved     extended
```

Edge key:
- **imports**: This paper adopts/buids on the concept from the cited work
- **extends**: This paper broadens the scope beyond the cited work
- **baseline**: The cited work serves as a comparison baseline
- **refutes**: This paper shows a limitation of the cited approach
