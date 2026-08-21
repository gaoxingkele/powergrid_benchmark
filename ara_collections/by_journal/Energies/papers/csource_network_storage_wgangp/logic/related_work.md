# Related Work

## RW1: ADN Planning with Uncertain Scenarios
- **Reference**: [2] Wang, S.; Luo, F.; Wang, C.; Lyu, Y.; Fo, J.; Ge, L. Collaborative Configuration Optimization of Soft Open Points and Distributed Multi-Energy Stations with Spatiotemporal Coordination and Complementarity. J. Mod. Power Syst. Clean Energy 2025, 13, 2086–2097.
- **Relevance**: Represents the clustering method based on historical data for scenario generation. Clusters actual wind and solar output profiles to obtain representative curves for optimization. Limitations: highly sensitive to sample set coverage and clustering criteria, limited number of scenarios struggle to capture high-volatility periods.
- **How Addressed**: The current paper uses WGAN-GP instead, which does not rely on distributional assumptions and generates more realistic and representative scenarios.

## RW2: SOP Technology and Applications
- **Reference**: [6] Jiang, X.; Zhou, Y.; Ming, W.; Yang, P.; Wu, J. An Overview of Soft Open Points in Electricity Distribution Networks. IEEE Trans. Smart Grid 2022, 13, 1899–1910.
- **Relevance**: Provides a comprehensive overview of SOP technology, establishing SOP as a key device for controllable bidirectional power flow between feeders and node voltage regulation in distribution networks.
- **How Addressed**: The current paper extends SOP by integrating BESS on its DC side to form E-SOP, achieving spatiotemporal coordinated control.

## RW3: BESS in Distribution Systems
- **Reference**: [7] Scrocca, A.; Pisani, R.; Andreotti, D.; Rancilio, G.; Delfanti, M.; Bovera, F. Optimal Spot Market Participation of PV + BESS: Impact of BESS Sizing in Utility-Scale and Distributed Configurations. Energies 2025, 18, 3791.
- **Relevance**: Represents work on BESS for temporal energy shifting through charging and discharging processes, contributing to peak shaving, valley filling, and smoothing renewable energy output.
- **How Addressed**: The current paper integrates BESS directly on the DC side of SOP to form E-SOP, rather than treating BESS as an independent resource.

## RW4: Scenario Analysis Methods
- **Reference**: [14] Ramadan, A.; Ebeed, M.; Kamel, S.; Abdelaziz, A.Y.; Haes Alhelou, H. Scenario-Based Stochastic Framework for Optimal Planning of Distribution Systems Including Renewable-Based DG Units. Sustainability 2021, 13, 3566.
- **Relevance**: Represents the scenario analysis method that generates representative operating scenarios based on probabilistic characteristics of uncertain variables, approximating stochastic fluctuations through deterministic operating conditions.
- **How Addressed**: The current paper identifies limitations of this approach (requires distribution assumptions, complex model construction, sensitive to assumptions) and proposes WGAN-GP as an alternative.

## RW5: Robust Optimization for Renewable-Dominated Systems
- **Reference**: [17] Liang, Z.; Chung, C.Y.; Wang, Q.; Chen, H.; Yang, H.; Wu, C. Fortifying Renewable-Dominant Hybrid Microgrids: A Bi-Directional Converter Based Interconnection Planning Approach. Engineering 2025, 51, 130–143.
- **Relevance**: Proposes a robust planning approach based on bidirectional converter-based interconnection structure to enhance operational reliability of hybrid microgrids with high renewable penetration under uncertain conditions.
- **How Addressed**: The current paper uses scenario-based stochastic programming with WGAN-GP generation instead of robust optimization, citing the different approach but acknowledging its promising performance.

## RW6: Fixed Topology Planning Models
- **Reference**: [13] Wang, C.; Song, G.; Li, P.; Ji, H.; Zhao, J.; Wu, J. Optimal Siting and Sizing of Soft Open Points in Active Electrical Distribution Networks. Appl. Energy 2017, 189, 301–309.
- **Relevance**: Represents existing planning studies based on fixed ADN topologies and predefined DG configurations, lacking an integrated modeling framework for DG–E-SOP–network structure.
- **How Addressed**: The current paper proposes a joint optimization framework for DG siting/sizing, E-SOP deployment, feeder layout, and substation construction/expansion.

## RW7: Radiality Constraints in Distribution Networks
- **Reference**: [18] Lavorato, M.; Franco, J.F.; Rider, M.J.; Romero, R. Imposing Radiality Constraints in Distribution System Optimization Problems. IEEE Trans. Power Syst. 2012, 27, 172–180.
- **Relevance**: Provides the specific modeling approach for ensuring network connectivity and radiality in distribution network optimization, referenced by the current paper for topology constraints.
- **How Addressed**: The current paper incorporates these radiality constraints in its network topology constraint formulation.

## RW8: SOCP in Distribution System Planning
- **Reference**: [19] Grover-Silva, E.; Girard, R.; Kariniotakis, G. Optimal Sizing and Placement of Distribution Grid Connected Battery Systems through an SOCP Optimal Power Flow Algorithm. Appl. Energy 2018, 219, 385–393.
- **Relevance**: Demonstrates the application of SOCP relaxation to distribution system optimal power flow problems, providing the basis for convex relaxation in the current paper.
- **How Addressed**: The current paper builds on SOCP relaxation and extends it with the SCCR iterative tightening mechanism.

## RW9: CCP for Flexibility Evaluation
- **Reference**: [22] Ji, H.; Wang, C.; Li, P.; Zhao, J.; Song, G.; Wu, J. Quantified Flexibility Evaluation of Soft Open Points to Improve Distributed Generator Penetration in Active Distribution Networks Based on Difference-of-Convex Programming. Appl. Energy 2018, 218, 338–348.
- **Relevance**: Uses convex–concave programming (CCP) approach for SOP-related problems in ADNs. Used as the baseline comparison algorithm in the current paper.
- **How Addressed**: The proposed SCCR algorithm is compared against CCP and shown to achieve identical solution accuracy with approximately twice the computational efficiency.

## RW10: Test System Source
- **Reference**: [21] Miranda, V.; Ranito, J.V.; Proenca, L.M. Genetic Algorithms in Optimal Multistage Distribution Network Planning. IEEE Trans. Power Syst. 1994, 9, 1927–1933.
- **Relevance**: Original source of the Portuguese 54-bus distribution network used as the test system.
- **How Addressed**: The current paper uses a modified version of this test system with source-load data from real operational measurements in northern China.
