# Claims

Review takeaways. Each Statement is a mechanism/relationship the review synthesizes from the surveyed
evidence; supporting numbers live in `Evidence basis`/`Proof` and the surveyed tables, never in the
Statement. This is a review, so `Status` values reflect the strength of the surveyed evidence the
review cites, not an original experiment run by the authors.

## C01: Storage integration behaves as a coupled planning–control system, so decoupling the two layers converts forecast error and degradation into capital-efficiency loss
- **Statement**: When long-term techno-economic storage planning and short-term dynamic control are optimized as separate stages, errors and degradation incurred at the operational layer are not fed back into sizing/placement decisions, so the interaction between the layers — not either layer alone — governs achievable capital efficiency and reliability; treating storage integration as a single tightly coupled multidimensional optimization problem is therefore necessary for economically efficient, stable operation in low-inertia AC microgrids.
- **Conditions**: Holds for renewable-dominated AC microgrids where storage serves both an investment-deferral (planning) and a stability (control) role; argued at the level of framework structure, and the review deliberately does not attach system-wide monetary magnitudes to the coupling (untested boundary: the size of the coupling benefit across specific grids/tariffs is not quantified).
- **Sources**: ["5 percent ← §1.2 «Current studies demonstrate that prioritizing the State of Energy reduces capacity estimation errors by 5 percent» [result]"]
- **Status**: supported
- **Falsification criteria**: Evidence that a pipeline optimizing sizing and dispatch as independent stages achieves equal-or-better lifecycle cost and transient stability, versus a jointly coupled optimization, across representative renewable-dominated AC microgrids — i.e. no measurable degradation of capital efficiency or reliability from decoupling.
- **Proof**: [E04, E09, E10]
- **Evidence basis**: The review's central gap statement (§1, §1.2, O3/O4) plus Table 9's ([99]) reported 5% capacity-estimation-error reduction from SoE prioritization, offered as proof that the planning–control nexus is a direct driver of capital efficiency; Figure 2 embodies the coupled workflow with operational MATLAB/Simulink results updating planning constraints.
- **Dependencies**: C03, C08
- **Tags**: planning-control coupling, macro-micro gap, review thesis

## C02: Degradation-aware dispatch/sizing that separates calendar from cycle ageing is the dominant economic lever for storage, because static planning ignores the operating-strategy → lifetime feedback
- **Statement**: Because battery life-cycle cost is dominated by degradation that depends on operating strategy (depth-of-discharge, cycle vs calendar ageing), optimization frameworks that explicitly model and adapt to ageing extend usable life and lower lifecycle cost, whereas static planning that omits this feedback trades short-term dispatch gains for accelerated capacity fade and can be trapped in local optima.
- **Conditions**: Holds for lithium-ion-dominated storage where cycle/calendar ageing materially affects replacement cost; the review states the direction and cites representative reductions but does not establish a universal magnitude across chemistries (flow batteries decouple this differently).
- **Sources**: ["6.3 percent ← §1.2.1 «degradation-aware dispatch strategies can reduce total battery ageing by approximately 6.3 percent daily» [result]", "7 to 21 percent ← §1.2.1 «advanced algorithms achieve a 7 to 21 percent reduction in costs for hybrid microgrid sizing compared to traditional baseline models» [result]"]
- **Status**: supported
- **Falsification criteria**: Demonstration that dispatch/sizing which ignores calendar-vs-cycle ageing yields equal-or-lower lifecycle cost and equal battery lifetime as degradation-aware optimization under realistic renewable duty cycles.
- **Proof**: [E01, E08]
- **Evidence basis**: §1.2.1 (approx. 6.3% daily ageing reduction from degradation-aware dispatch; 7–21% sizing cost reduction by advanced algorithms) and §3.6 on calendar vs cycle ageing trade-offs; Table 1 lifespan ranges and Table 8 planning studies that cite health-index-aware deferral.
- **Dependencies**: C07
- **Tags**: degradation-aware, calendar vs cycle ageing, LCOS, techno-economics

## C03: State of Energy is the grid-aware dispatch metric of record over State of Charge, because releasable energy is a nonlinear function of terminal voltage and temperature that SoC does not capture
- **Statement**: Since usable/releasable battery energy varies nonlinearly with terminal voltage, internal parameters, and temperature, a charge-fraction metric (SoC, Coulomb-counting) systematically misrepresents deliverable energy, whereas an energy-integral metric (SoE) tracks it directly; prioritizing SoE for load-distribution and dispatch decisions therefore prevents capacity overestimation and unexpected power shortages, while SoC remains the appropriate metric for internal cell balancing.
- **Conditions**: Holds for islanded / NNS-like AC microgrids where the BMS makes grid-aware dispatch decisions; asserted under offline-simulation deterministic BMS modelling, and SoC/SoE are assumed co-estimated (states not directly measurable).
- **Sources**: ["5 percent ← Table 9 «Reduced capacity estimation error by 5 percent.» [result]", "3.1 percent ← Table 9 «Improved tracking performance by 3.1 percent.» [result]"]
- **Status**: supported
- **Falsification criteria**: Evidence that dispatch decisions driven by SoC alone deliver the same accuracy of releasable-energy estimation and no more frequent power shortages than SoE-prioritized dispatch, in a system with meaningful voltage/temperature variation.
- **Proof**: [E09]
- **Evidence basis**: BMS section Eqs (7)–(11) defining continuous-time SoC/SoE, operational ratios, and the SoE=a·SoC²+b·SoC+c correlation; Table 9 reports SoC tracking +3.1% ([66]) and SoE capacity-error −5% ([99]) with their economic effects (fewer cells; avoided shortages).
- **Dependencies**: —
- **Tags**: SoE, SoC, state estimation, BMS, co-estimation

## C04: Pairing a global-exploration metaheuristic with a local-exploitation metaheuristic resolves the exploration–exploitation dilemma that defeats standalone and rule-based controllers
- **Statement**: Multi-objective storage control/sizing under renewable uncertainty fails when a single search strategy must both scan the whole solution space and refine a local optimum; hybridizing a global explorer (Grey Wolf Optimizer) with a local exploiter (Particle Swarm Optimization) assigns each sub-task to the algorithm suited to it, giving a better robustness/efficiency balance for jointly meeting stability and economic objectives than standalone metaheuristics, rule-based controllers, or (at scale) MPC.
- **Conditions**: Holds for grid-connected / renewable-integrated PV–battery AC microgrids optimizing a weighted multi-objective function; evidence is drawn from cited hybrid-metaheuristic studies rather than a controlled head-to-head in this review (untested boundary: relative advantage vs other hybrids such as PSO-GA-LADRC or slime-mould is not quantified here).
- **Sources**: ["35 percent ← §1.2.3 «implementing advanced predictive controls achieves tracking response time improvements of 35 percent» [result]", "1.22 percent ← §1.2.3 «reduces Total Harmonic Distortion to exactly 1.22 percent» [result]", "3.1 percent ← §1.2.3 «improve steady state-of-charge tracking performance by 3.1 percent» [result]"]
- **Status**: supported
- **Falsification criteria**: A standalone metaheuristic or rule-based/MPC controller matching the hybrid GWO-PSO's transient-response and multi-objective (cost/emissions/losses/autonomy) balance at equal or lower computational cost on the same microgrid problem.
- **Proof**: [E05, E09, E11]
- **Evidence basis**: §1.2.3 and §4.2 describe the GWO-explore / PSO-exploit division (ref [63]); Figure 7 details the GWO-PSO workflow (top GWO solutions seed PSO particles); Table 9 links hybrid GWO-PSO to lowered Total Net Present Cost and reduced grid imports; reported control gains: +35% tracking response time, THD 1.22%, +3.1% SoC tracking.
- **Dependencies**: C03
- **Tags**: GWO-PSO, hybrid metaheuristic, exploration-exploitation, multi-objective control

## C05: Replacing statistical forecasting with structured deterministic/ML forecasting compresses error enough to shift EMS operation from reactive to proactive
- **Statement**: Traditional statistical predictors (ARIMA/SARIMA) lose accuracy under non-stationary, volatile renewable/load conditions; structured deterministic and machine-learning forecasting frameworks capture the nonlinear temporal patterns well enough that the residual forecast error stops being the binding constraint, which lets the EMS pre-commit storage (proactive scheduling) instead of reacting, reducing load shedding and curtailment.
- **Conditions**: Holds for short-to-medium-horizon load and renewable-generation forecasting feeding EMS dispatch; the review scopes to deterministic (non-black-box) and structured ML models and reports representative accuracy gains rather than a benchmark it ran.
- **Sources**: ["0.8 percent and 2.6 percent ← §1.2.2 «reduces the Mean Absolute Percentage Error to between 0.8 percent and 2.6 percent for energy consumption forecasting» [result]", "3.85 percent ← §1.2.2 «high-fidelity demand prediction achieves Root Mean Square Error values of 3.85 percent for short-term horizons» [result]", "25 percent ← §1.2.2 «proactive scheduling that can decrease load shedding by 25 percent compared to traditional deterministic scheduling» [result]"]
- **Status**: supported
- **Falsification criteria**: Evidence that reducing forecast error below the statistical baseline produces no improvement in dispatch outcomes (load shedding, curtailment, storage overcommitment) — i.e. forecast accuracy is decoupled from operational/economic performance.
- **Proof**: [E05, E06]
- **Evidence basis**: §1.2.2 (MAPE 0.8–2.6%; RMSE 3.85% short-term; load shedding −25%), §4.1, and Table 5 forecasting synthesis (predictability coefficient 0.9821 [62]; MAE −14.00% [59]; MSE 0.012 household / 0.045 solar [58]); Table 6 preprocessing techniques that enable these gains.
- **Dependencies**: —
- **Tags**: deterministic forecasting, MAPE/RMSE, proactive dispatch, machine learning

## C06: Neither external sizing optimization nor external dispatch control is universally superior; the operating environment selects the winner
- **Statement**: The two remedies for HOMER's sizing/dispatch rigidity — externally optimizing component capacity vs externally replacing dispatch logic — target different cost drivers (CAPEX vs OPEX), so their relative economic value is conditional: sizing optimization dominates in isolated, high-CAPEX, tariff-static networks where avoiding local optima sets feasibility, while dispatch control dominates in grid-integrated systems with dynamic pricing and peak-demand penalties where real-time load/SoC shifting captures most of the value.
- **Conditions**: Holds for HOMER-Pro-based techno-economic studies of hybrid microgrids; the review contrasts two representative studies ([39] sizing, [40] dispatch) and generalizes the environment-dependence rather than measuring a crossover point.
- **Sources**: []
- **Status**: supported
- **Falsification criteria**: A demonstration that one approach yields lower system cost than the other across both isolated/static-tariff and grid-connected/dynamic-tariff environments alike, contradicting the claimed context dependence.
- **Proof**: [E03]
- **Evidence basis**: §3.4 and Table 3 contrast External Sizing Optimization [39] (CAPEX focus, avoids local-optima traps, lower global LCOE) against External Dispatch Control [40] (OPEX focus, reduces peak-demand charges); §3.4 text states which dominates in isolated vs grid-integrated environments.
- **Dependencies**: C02
- **Tags**: sizing vs dispatch, HOMER Pro, LCOE, context dependence

## C07: Storage technology and integration topology impose upstream constraints that bound achievable control performance and degradation
- **Statement**: The physical properties of the chosen storage medium (energy vs power density, response time, cycle life) and the electrical integration topology (AC-coupled vs DC-coupled vs hybrid) set the ceiling on control bandwidth, conversion efficiency, and degradation behaviour before any EMS algorithm acts; consequently, matching technology and topology to the application — e.g. a battery+supercapacitor HESS that assigns slow energy balancing to batteries and fast transients to supercapacitors — is what makes low-degradation, high-bandwidth control physically attainable.
- **Conditions**: Holds across AC-microgrid storage deployments; comparative direction is asserted qualitatively from surveyed characteristics (Table 1/Table 2) with one quantified topology datapoint (DC coupling efficiency gain), not a controlled benchmark.
- **Sources**: ["approximately 3% ← §2.2.2 «implementing DC distribution for commercial fleets can result in significant reductions in CAPEX and OPEX while increasing system efficiency by approximately 3% compared to AC distribution» [result]"]
- **Status**: supported
- **Falsification criteria**: Evidence that control bandwidth, efficiency, and degradation outcomes are insensitive to storage-technology and topology choice — i.e. an EMS achieves the same performance regardless of medium (battery vs supercapacitor) and coupling (AC vs DC vs HESS).
- **Proof**: [E01, E02]
- **Evidence basis**: §2 (technology–architecture co-design constrains control), Table 1 (energy density/response/lifespan/application per technology), Table 2 (battery-only vs SC-only vs HESS: HESS gives multi-scale response and reduced degradation stress), §2.2.2 (DC coupling ~3% efficiency gain vs AC), §2.3 (topology sets control bandwidth/optimization timeframe).
- **Dependencies**: —
- **Tags**: storage technology, integration topology, HESS, technology-architecture co-design

## C08: Coupling macro-economic sizing tools with meso-scale physical and micro-scale dynamic simulators closes the fidelity gap that static economic models leave open
- **Statement**: Macro-economic sizing software (HOMER Pro) optimizes NPC/LCOE but cannot represent shading, thermal loss, electrochemical degradation, three-phase imbalance, or transient stability; layering it with meso-scale physical modelling (PVsyst/Helioscope) and micro-scale dynamic simulation (MATLAB/Simulink) grounds the economic model in realistic yield and degradation data and validates operational constraints against transient behaviour, so investment decisions remain robust to both financial and physical grid disturbances.
- **Conditions**: Holds for offline (non-real-time) co-simulation workflows for AC-microgrid storage planning; presented as the review's proposed framework, validated conceptually against surveyed integration studies rather than by an end-to-end run in this paper.
- **Sources**: []
- **Status**: supported
- **Falsification criteria**: Evidence that a purely macro-economic sizing model, without meso-scale physical or micro-scale dynamic coupling, yields investment decisions equally robust to real shading/degradation and transient-stability outcomes.
- **Proof**: [E04, E10]
- **Evidence basis**: §3.5 and Table 4 align PVsyst/Helioscope (physical yield, electrochemical degradation) with HOMER Pro 3.18.4 (NPC minimization, replacement forecasting); §4.4 on coupling macro-sizing with MILP/MATLAB dynamic simulators and three-phase modelling; Figure 2 is the multi-layer framework.
- **Dependencies**: C01, C02
- **Tags**: multi-scale, co-simulation, HOMER Pro, PVsyst, MATLAB/Simulink, framework

## C09: BESS acting as a coordinated non-network solution defers capital-intensive network reinforcement at fixed investment cost
- **Statement**: Strategically sized and placed distributed battery storage, operated as a non-network solution and coordinated with dynamic reactive-power devices (e.g. STATCOMs) and health-index-aware planning, manages peak loads and voltage stability well enough to postpone or eliminate pole-and-wire upgrades, so storage investment substitutes for network-reinforcement capital while preserving reliability in renewable-heavy AC microgrids.
- **Conditions**: Holds where storage siting/sizing is optimized against an expansion-cost objective (Eq 6) and where reactive-power coordination is available; the review synthesizes planning studies (Table 8) and does not attach a universal deferral value.
- **Sources**: []
- **Status**: supported
- **Falsification criteria**: Evidence that deploying optimally sized/placed BESS as an NNS does not defer or reduce required network-reinforcement expenditure while maintaining voltage/frequency reliability — i.e. storage cannot substitute for pole-and-wire upgrades at comparable cost.
- **Proof**: [E07, E08]
- **Evidence basis**: §5, Table 7 (NNS integration factors: techno-economic feasibility, health index, voltage stability, metaheuristic optimization, cost-reflective pricing), Table 8 (GWO reduces installation costs and grid dependence; multi-stage planning defers capital expenditure; health-index incorporation extends asset lifespan), Eq (6) expansion-cost objective, and STATCOM coordination (§5, refs [72,74]).
- **Dependencies**: C02, C07
- **Tags**: non-network solution, infrastructure deferral, STATCOM, expansion planning, grid resilience
