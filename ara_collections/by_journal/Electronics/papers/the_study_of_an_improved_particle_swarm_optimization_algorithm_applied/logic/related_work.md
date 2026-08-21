# Related Work

Typed dependency graph of the paper's citation footprint (26 references). Works with a specific technical delta get full RW blocks; the remainder are captured briefly to preserve the full footprint.

## RW03: Duan et al., 2023 — initialization-free distributed dynamic economic dispatch
- **DOI**: 10.1016/j.segan.2023.101004
- **Type**: baseline / imports
- **Delta**:
  - What changed: This paper adopts the same broad problem (dynamic economic dispatch in a microgrid, minimize generation cost, supply-demand and capacity constraints) but replaces the distributed convex/Lyapunov-analysis solver with a metaheuristic (SCMPSO) and adds environmental cost and more device types.
  - Why: to handle a more comprehensive, non-convex multi-device cost model.
- **Claims affected**: C03
- **Adopted elements**: economic-dispatch framing, supply-demand and capacity constraints.

## RW04: Abdelghany et al., 2024 — coordinated optimal operation of grid-connected wind-solar microgrid with hybrid storage
- **DOI**: 10.1109/TSTE.2023.3281390
- **Type**: bounds / imports
- **Delta**:
  - What changed: Shares the grid-connected wind-solar-plus-storage microgrid setting and economic operating-cost objective, but uses model predictive control over a mixed-logic dynamic framework rather than a swarm metaheuristic.
  - Why: alternative control paradigm for the same storage-coordination problem.
- **Claims affected**: C03
- **Adopted elements**: hybrid energy-storage coordination, economic-efficiency objective.

## RW16: Zhao et al., 2020 — economic-environmental dispatch via improved quantum PSO (QPSO)
- **DOI**: — (Energy 2020, 195, 117014)
- **Type**: baseline / extends
- **Delta**:
  - What changed: Directly comparable — improved QPSO for microgrid economic-environmental dispatch. This paper uses QPSO as one of the three comparison baselines and reports SCMPSO achieving lower cost and emissions.
  - Why: to demonstrate SCMPSO's superiority over an existing improved-PSO dispatch method.
- **Claims affected**: C04, C05, C06
- **Adopted elements**: economic-environmental dispatch objective; QPSO as a comparison algorithm.

## RW14: Xiong et al., 2022 — improved bare-bones multi-objective PSO for combined heat-power emission dispatch
- **DOI**: 10.1016/j.energy.2022.123108
- **Type**: baseline / imports
- **Delta**:
  - What changed: Prior improved-PSO for economic-emission dispatch; motivates the PSO-improvement + emission-cost direction. This paper adds chaotic init + second-order oscillation instead of a bare-bones scheme.
  - Why: positions SCMPSO within the improved-PSO-for-emission-dispatch line.
- **Claims affected**: C01, C06
- **Adopted elements**: joint economic-emission objective for PSO dispatch.

## RW23: Liu et al., 2018 — multi-agent microgrid optimization via dynamic guiding chaotic search PSO
- **DOI**: 10.3390/en11123286
- **Type**: imports / extends
- **Delta**:
  - What changed: Precedent for combining chaotic search with PSO for microgrid operation; SCMPSO uses Henon chaotic mapping specifically for initialization plus a distinct second-order oscillation update.
  - Why: grounds the chaotic-mapping component (Eq. 25).
- **Claims affected**: C01
- **Adopted elements**: chaotic-search-enhanced PSO for microgrid dispatch (cited at Eq. 23 / §4.1 for PSO basics too).

## RW12: Zhao et al., 2024 — hierarchical parallel search with automatic parameter configuration for PSO
- **DOI**: 10.1016/j.asoc.2023.111126
- **Type**: bounds
- **Delta**:
  - What changed: One of [12-14] documenting PSO's local-optima / slow-convergence weaknesses that motivate the improvements.
  - Why: establishes the gap G2.
- **Claims affected**: C01
- **Adopted elements**: characterization of PSO limitations.

## Additional citations (brief footprint)
- **RW01** Yao et al., 2023, *Energy Policy* 183:113769 — background: bibliometric overview of energy policy (motivates fossil-fuel/environment framing). Type: background.
- **RW02** Feng & Liao, 2020, *J. Clean. Prod.* 258:120630 — background: "Energy + Internet" in China (microgrid context). Type: background.
- **RW05** Gholami et al., 2016, *IEEE Trans. Smart Grid* 7:2849 — model development: microgrid scheduling under uncertainty/resilience. Type: baseline (model line).
- **RW06** Correa-Posada & Sanchez-Martin, 2014, *IEEE Trans. Power Syst.* 29:18 — coordinated power/natural-gas dispatch to minimize fuel cost. Type: baseline (model line).
- **RW07** Sadeghian & Ardehali, 2016, *Energy* 102:10 — economic dispatch with max profit / min emissions via Benders decomposition. Type: baseline (dual-objective model).
- **RW08** Shen et al., 2016, *J. Electron. Meas. Instrum.* 30:568 — coordinated multi-microgrid scheduling / economic operation. Type: baseline (model line).
- **RW09** Yin & Cai, 2024, *Energy* 295:130996 — multimodal multi-objective economic dispatch (penalty-function line [9-11]). Type: imports (multi-to-single objective).
- **RW10** Rezaei et al., 2018, *IEEE Trans. Ind. Inf.* 15:1532 — IGDT normal-boundary-intersection bidding for smart microgrids. Type: imports (multi-objective handling).
- **RW11** Huang et al., 2024, *Int. J. Hydrogen Energy* 69:927 — multi-objective energy-hub optimization. Type: imports (multi-objective handling).
- **RW13** Wang, 2022, Master's thesis, CUMT Beijing — improved PSO for combined cooling/heating/power microgrid (PSO-limitation line [12-14]). Type: bounds.
- **RW15** Jakubik et al., 2021, *Eur. J. Oper. Res.* 295:157 — directed PSO with Gaussian-process forecasting (PSO-hybrid line [15-18]). Type: extends.
- **RW17** Kacimi et al., 2020, *Eng. Appl. Artif. Intell.* 89:103417 — mixed-coding PSO for fuzzy-rule cleaning (PSO-hybrid line). Type: extends.
- **RW18** Wang et al., 2019, *Swarm Evol. Comput.* 49:114 — CPSO-CNN hyperparameter tuning (PSO-hybrid line; CPSO relates to a comparison baseline). Type: extends.
- **RW19** Roudbari et al., 2024, *Sol. Energy Mater. Sol. Cells* 276:113070 — PV/thermal systems review (grounds PV temperature effect, Eq. 1). Type: imports.
- **RW20** Teferra et al., 2023, *Heliyon* 9:e12802 — fuzzy PV/wind forecasting with PSO (grounds wind model, Eq. 2). Type: imports.
- **RW21** Ding et al., 2013, *Power Syst. Technol.* 37:575 — capacity optimization of standalone PV-wind-diesel-battery microgrid (grounds thermal model 30%-rated bound, Eq. 3). Type: imports.
- **RW22** Zhang et al., 2011, *Power Syst. Technol.* 35:24 — microgrid energy management and control strategy (grounds ESS model, Eqs. 4-5). Type: imports.
- **RW24** Chu et al., 2024, *Appl. Soft Comput.* 162:11187 — surrogate-assisted social-learning PSO (chaotic-init line [24,25]). Type: imports.
- **RW25** Priya & Ganguly, 2024, *Appl. Soft Comput.* 159:111616 — multi-swarm surrogate PSO for distribution-network loss minimization (chaotic-init line [24,25]). Type: imports.
- **RW26** Tantu & Biramo, 2024, *Heliyon* 10:e36668 — adaptive-PSO network reconfiguration (grounds adaptive-weight idea, Eq. 26/§4.2.2). Type: imports.
