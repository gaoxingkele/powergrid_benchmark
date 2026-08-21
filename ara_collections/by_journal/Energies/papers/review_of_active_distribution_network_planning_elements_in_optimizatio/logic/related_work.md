# Related Work

This is a review paper. The "related work" corresponds to the body of literature reviewed and synthesized. The dependency graph maps the relationships between the review and the references it surveys.

## Typed Dependency Graph

### Reviews and Surveys (meta-sources that this review builds upon)

| ID | Reference | Relationship | Coverage |
|----|-----------|-------------|----------|
| [3] | Rastgou, 2024, "Distribution network expansion planning: An updated review" | Foundation — provides DNP background | Section 2 (constraints), Section 3 |
| [9] | Li et al., 2017, "A review of optimal planning active distribution system" | Foundation — ADN planning review | Sections 2.2, 2.4 |
| [40] | Ehsan and Yang, 2019, "State-of-the-art techniques for modelling of uncertainties in ADN planning" | Foundation — uncertainty modeling | Section 2.6 |
| [41] | Aien et al., 2016, "A comprehensive review on uncertainty modeling techniques in power system studies" | Foundation — uncertainty techniques | Section 2.6 |
| [42] | Aien et al., 2014, "On possibilistic and probabilistic uncertainty assessment" | Support — probabilistic methods | Section 2.6 |
| [43] | Singh et al., 2022, "Uncertainty handling techniques in power systems: A critical review" | Support — uncertainty comparison | Section 2.6 |
| [45] | Khator and Leung, 1997, "Power distribution planning: A review of models and issues" | Foundation — LP planning models | Section 3.1 |
| [46] | Temraz and Quintana, 1993, "Distribution system expansion planning models: An overview" | Support — LP expansion models | Section 3.1 |
| [31] | Verma et al., 2020, "Constraints for effective distribution network expansion planning: An ample review" | Support — constraint classification | Section 2.4 |

### ADN Planning Optimization Studies (primary research papers on planning elements)

| ID | Reference | Relationship | Coverage |
|----|-----------|-------------|----------|
| [6] | Anadon Martinez et al., 2025, "Planning fast-charging stations along highways" | Example — short-term/EV planning | Section 2.1 |
| [7] | Saldana-Gonzalez et al., 2024, "Distribution network planning method: Integration of a RNN" | Example — hybrid planning | Section 2.1 |
| [8] | Nordic Energy Research, 2022, "Distributed Flexibility: Lessons Learned in the Nordics" | Example — short-term flexibility | Section 2.1 |
| [10] | Borousan and Hamidan, 2023, "Distributed power generation planning using chimp optimization" | Example — economic objective | Section 2.2 |
| [11] | de Lima et al., 2023, "A risk-based planning approach for sustainable distribution systems" | Example — economic + EV | Section 2.2 |
| [13] | Hou et al., 2023, "Resilience enhancement of distribution network under typhoon" | Example — technical objective | Section 2.2 |
| [14] | Zhou et al., 2023, "A multiple uncertainty-based bi-level expansion planning" | Example — technical + ESS | Section 2.2 |
| [17] | Ahmadi et al., 2023, "Multi-objective stochastic techno-economic-environmental optimization" | Example — environmental objective | Section 2.2 |
| [21] | Ganguly et al., 2011, "Mono-and multi-objective planning using PSO" | Example — substation decision variables | Section 2.3 |
| [23] | Xing et al., 2015, "Second-order cone model for ADN expansion planning" | Example — SOC for ADN | Sections 2.3, 3.4 |
| [27] | Lin et al., 2014, "Distribution network planning integrating charging stations of EV with V2G" | Example — EVCS decision variable | Section 2.3 |
| [28] | Wu et al., 2020, "AC/DC hybrid distribution system expansion planning" | Example — flexible strategies | Section 2.3.2 |
| [29] | Ramirez et al., 2016, "Co-Optimization of Generation Expansion Planning and EVs Flexibility" | Example — EV flexibility | Section 2.3.2 |
| [30] | Hamidpour et al., 2019, "Flexible, reliable, and renewable power system resource expansion planning" | Example — stochastic with flexible sources | Section 2.3.2 |
| [32] | Xie et al., 2020, "Expansion planning of active distribution system" | Example — technical constraints | Section 2.4 |

### OPF Formulation Studies

| ID | Reference | Relationship | Coverage |
|----|-----------|-------------|----------|
| [47] | Kabirifar et al., 2021, "A bi-level framework for expansion planning in active power distribution networks" | Example — MILP bi-level | Section 3.2 |
| [48] | Qin et al., 2021, "Many-objective interactive optimization for DNP" | Example — MILP multi-objective | Section 3.2 |
| [49] | Abdi-Siab and Lesani, 2020, "Distribution expansion planning in the presence of PEV" | Example — MILP with PEV | Section 3.2 |
| [50] | Yao et al., 2024, "Optimal planning of distribution systems and charging stations" | Example — MINLP with PV-grid-EV | Section 3.3 |
| [51] | Wang et al., 2022, "Distribution network expansion planning approach for large scale EVs" | Example — MINLP scalability | Section 3.3 |
| [55] | Swaminathan et al., 2017, "Short-term ADN operation with convex formulations" | Example — SOC relaxation | Section 3.4 |
| [56] | Luo et al., 2018, "Optimal planning of EVCS comprising multi-types of charging facilities" | Example — SOC for EVCS | Section 3.4 |
| [57] | Gholizadeh-Roshanagh et al., 2020, "Multi-objective method for MILP-based DNP" | Example — metaheuristic | Section 3.5 |
| [58] | Ahmadian et al., 2019, "Hybrid PSO and tabu search for expansion planning" | Example — metaheuristic hybrid | Section 3.5 |

### Dynamic OPF Planning Tools

| ID | Reference | Relationship | Coverage |
|----|-----------|-------------|----------|
| [59] | Bodal et al., 2022, "Demand flexibility modelling for long term optimal distribution grid planning" | Example — flexibility tool | Section 3.6 |
| [60] | Rossini et al., 2023, "FlexPlan.jl — An open-source Julia tool" | Example — stochastic planning tool | Section 3.6 |
| [61] | Muller et al., 2019, "Integrated techno-economic power system planning" (eGo) | Example — open-source planning | Section 3.6 |
| [62] | Scheidler et al., 2018, "Heuristic optimisation for automated distribution system planning" (Pandapower) | Example — automated planning framework | Section 3.6 |

### Generative AI Studies for Power Systems

| ID | Reference | Relationship | Coverage |
|----|-----------|-------------|----------|
| [63] | Yuan et al., 2022, "Conditional style-based GAN for renewable scenario generation" | Example — GAN scenario | Section 4 |
| [64] | Kang et al., 2023, "A cross-modal GAN for scenarios generation of renewable energy" | Example — GAN cross-modal | Section 4 |
| [65] | Wang and Hong, 2020, "Generating realistic building electrical load profiles through GAN" | Example — GAN load profiles | Section 4 |
| [69] | Li et al., 2024, "Diffcharge: Generating EV charging scenarios via a denoising diffusion model" | Example — diffusion EV | Section 4 |
| [70] | Wang and Zhang, 2024, "Customized load profiles synthesis based on conditional diffusion models" | Example — diffusion load | Section 4 |
| [74] | Razghandi et al., 2022, "VAE-GAN for synthetic data generation in smart home" | Example — VAE hybrid | Section 4 |
| [78] | Hu et al., 2021, "Scenario forecasting for wind power using flow-based generative networks" | Example — flow-based wind | Section 4 |
| [85] | Choi et al., 2024, "eGridGPT: Trustworthy AI in the Control Room" | Example — transformer LLM | Section 4 |
| [100] | Yin et al., 2024, "PowerPulse: Power energy chat model with LLaMA" | Example — transformer LLM | Section 4 |
| [102] | Wang et al., 2024, "Cooperative planning of renewable energy generation and multi-timescale flexible resources" | Example — GAN in ADN planning | Section 4 |
| [103] | Xu et al., 2023, "GAN-assisted stochastic PV planning" | Example — GAN in ADN planning | Section 4 |
