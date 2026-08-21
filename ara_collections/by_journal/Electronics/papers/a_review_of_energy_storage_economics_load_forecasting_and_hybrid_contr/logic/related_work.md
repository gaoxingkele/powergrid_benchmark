# Related Work

Typed citation landscape. This review cites 102 references. Works with a specific technical delta
that the review builds on or bounds itself against get full `RW` blocks; the remaining citations are
captured in the grouped inventory below to preserve the full footprint.

## RW01: Hirsch, Parag & Guerrero, 2018 — Microgrids review
- **DOI**: 10.1016/j.rser.2018.03.040
- **Type**: bounds
- **Delta**:
  - What changed: Prior broad review of microgrid technologies, drivers, applications, ownership models, regulatory issues, and outstanding challenges.
  - Why: The review positions itself against [12] as covering microgrid development broadly but NOT providing the integrated economics + degradation + forecasting + optimization + offline-control synthesis this paper targets.
- **Claims affected**: C01
- **Adopted elements**: Framing of distributed energy resources' role in resilience and renewable integration.

## RW02: Ghosh, Mitra & Yemula, 2025 — Degradation-aware BESS allocation
- **DOI**: 10.1109/IAS62731.2025.11061398
- **Type**: bounds
- **Delta**:
  - What changed: Degradation-aware optimal BESS allocation for unbalanced active distribution networks.
  - Why: Cited (with [14]) as representative of prior degradation-aware planning that the review extends by linking it to forecasting, optimization-based EMS, and offline dynamic validation.
- **Claims affected**: C01, C02
- **Adopted elements**: Degradation-aware allocation and cycle/calendar-ageing importance.

## RW03: Lampsidis Tompros et al., 2026 — Green energy transition to European networks
- **DOI**: 10.3390/en19061400
- **Type**: bounds
- **Delta**:
  - What changed: Perspective on green-energy-transition opportunities/limitations for EU/Greece networks (planning, power quality, congestion, stability, performance indicators).
  - Why: Grouped with [12,13] as broad transition reviews the paper differentiates from by focusing on AC-microgrid storage economics-forecasting-control coupling.
- **Claims affected**: C01
- **Adopted elements**: Network-level transition challenge framing.

## RW04: Alshdaifat, Prasad, Al-Tameemi, Kilby & Lie, 2025 — GWO-PSO for grid-connected PV-battery
- **DOI**: 10.3390/en18226036
- **Type**: extends
- **Delta**:
  - What changed: The authors' own prior study proposing GWO-PSO for optimal energy-storage management in grid-connected PV-battery systems.
  - Why: The central control methodology (hybrid GWO-PSO), the offline time-domain state-tracking result, and Table 9's "Hybrid GWO-PSO" row (lowered Total NPC, reduced grid imports) derive from [63]; the review generalizes it into its multi-scale framework.
- **Claims affected**: C04, C09
- **Adopted elements**: GWO-explore/PSO-exploit hybridization; grid-aware dispatch objective.

## RW05: Wahid, El Rahman & Helmy, 2025 — External sizing optimization with HOMER
- **DOI**: 10.1109/ICEENG64546.2025.11031348
- **Type**: baseline
- **Delta**:
  - What changed: Uses an external (weighted-average) algorithm to optimize PV/diesel/battery capacity because HOMER's proprietary derivative-free optimizer converges to local optima.
  - Why: One of the two contrasted remedies in Table 3 (External Sizing Optimization); grounds C06's CAPEX-focused pole.
- **Claims affected**: C06
- **Adopted elements**: Diagnosis of HOMER local-optima traps; external capacity optimization.

## RW06: Pontes et al., 2025 — External dispatch control via HOMER + MATLAB Link
- **DOI**: 10.1109/INDUSCON66435.2025.11241688
- **Type**: baseline
- **Delta**:
  - What changed: Replaces HOMER's built-in dispatch strategies with a custom peak-aware control algorithm via MATLAB Link, reducing grid peak-demand costs without changing component sizes.
  - Why: The second contrasted remedy in Table 3 (External Dispatch Control); grounds C06's OPEX-focused pole.
- **Claims affected**: C06
- **Adopted elements**: Diagnosis that HOMER's limitation is operational flexibility, not sizing accuracy.

## RW07: Santos et al., 2024 — Joint sizing/operation of unbalanced three-phase AC microgrids (HOMER + MILP)
- **DOI**: 10.1007/s40313-023-01059-5
- **Type**: extends
- **Delta**:
  - What changed: Couples HOMER Pro with Mixed-Integer Linear Programming for joint optimal sizing and operation of unbalanced three-phase AC microgrids; also the GWO minimize-SoC-error study anchor (Table 8 ref [66]).
  - Why: Exemplifies the macro-sizing + high-fidelity-dynamic coupling the review advocates (C08) and the SoC-error minimization result in Table 9.
- **Claims affected**: C03, C08
- **Adopted elements**: Coupled macro-economic + physical three-phase modelling; SoC tracking improvement.

## RW08: Ramadan, Alhelou & Ahmed, 2025 — GWO near-optimal control/sizing for hybrid battery systems
- **DOI**: 10.1049/rpg2.12423
- **Type**: baseline
- **Delta**:
  - What changed: GWO for near-optimal control and sizing of lead-acid and lithium-ion hybrid energy systems, minimizing initial-to-final SoC error.
  - Why: Grounds the review's claim that metaheuristics (GWO) determine optimal sizing/control to minimize SoC error (§5, Table 8 ref [67]).
- **Claims affected**: C04, C07
- **Adopted elements**: GWO optimal sizing/control; multi-chemistry hybrid balancing.

## RW09: Sharma et al., 2022 — Combined SoC/SoE estimation via feedforward neural network
- **DOI**: 10.1109/PEDES56012.2022.10080110
- **Type**: imports
- **Delta**:
  - What changed: Multi-layer feedforward neural network for combined SoC/SoE estimation.
  - Why: Table 9 ref [99] — source of the "SoE prioritization reduces capacity estimation error by 5%" result that grounds C01/C03.
- **Claims affected**: C01, C03
- **Adopted elements**: Joint SoC/SoE estimation; capacity-error reduction.

## RW10: Liu, Liu, Peng, Meng & Gao, 2024 — SoE recovery with primary frequency control
- **DOI**: 10.1109/TTE.2024.3477921
- **Type**: imports
- **Delta**:
  - What changed: State-of-Energy recovery for BESS with primary frequency control for ageing mitigation.
  - Why: Cited for SoC's limitation (ignores nonlinear terminal-voltage dynamics) and health-aware control motivation (§BMS ref [50], §3.6 ref [50]).
- **Claims affected**: C03
- **Adopted elements**: SoC limitation; ageing-mitigating frequency-control operation.

## RW11: Chen et al., 2025 — SoC/SoE estimation via meta-learning + square-root UKF
- **DOI**: 10.1109/TTE.2025.3590916
- **Type**: imports
- **Delta**:
  - What changed: Meta-learning + square-root unscented Kalman filter for SoC/SoE estimation; establishes the stable quadratic SoC–SoE correlation.
  - Why: Grounds Eq (11) SoE = a·SoC² + b·SoC + c (§BMS ref [92]).
- **Claims affected**: C03
- **Adopted elements**: Quadratic SoC–SoE correlation model.

## RW12: Shrivastav & Dutta, 2025 — Slime Mould multi-objective hybrid microgrid optimization
- **DOI**: 10.1038/s41598-025-15207-1
- **Type**: baseline
- **Delta**:
  - What changed: Slime Mould Algorithm (and GA) for multi-objective energy-trilemma optimization of hybrid microgrids.
  - Why: Cited as an alternative evolutionary approach to GWO-PSO (§4.2 ref [16]); bounds C04's claim to a family of metaheuristics.
- **Claims affected**: C04
- **Adopted elements**: Multi-objective evolutionary optimization for the trilemma.

## Grouped citation inventory (full footprint)

- **Transition / DER-integration context (imports/background)**: [1] Oladigbolu et al. 2025 (transport+power planning, EV/ESS/DER); [2] Zhang et al. 2024 (high-RE power planning, flexible resources); [3] Liu et al. 2025 (distributed BESS grid support); [4] Galea et al. 2025 (LV power-quality with BESS); [5] Vaziri Rad et al. 2023 (excess-electricity off-grid review); [6] Zhao et al. 2020 (tri-level robust planning-operation DES co-optimization); [18] Assaad et al. 2025 (utility-scale hybrid plant technology mixes); [26] Yang et al. 2018 (BESS sizing review).
- **Microgrid control / topology (imports)**: [7] Al-Ismail 2021 (DC microgrid review); [8] Supian et al. 2025 (ESS resilient-grid science map); [9] Naima et al. 2025 (MPPT hybrid predictive+P&O); [10] Kalaivani et al. 2023 (hybrid microgrid power management); [11] Undre et al. 2024 (BESS synchronization circuit, DFIM hydro); [20] Benosenko et al. 2025 (DC-coupled storage PV park); [21] Wang et al. 2025 (DC vs AC-coupled fast charging techno-economics); [22] Sharida et al. 2025 (hierarchical control DC fast EV charging); [23] Nguyen & Nguyen 2025 (PSO-GWO smart-grid reconfiguration); [24] Ibrahim et al. 2024 (PSO-GA-LADRC autonomous DC microgrid); [25] Rathod & Subramanian 2025 (HRES advanced algorithms rural).
- **Techno-economic / HOMER studies (baseline)**: [27] Kumar et al. 2025 (HOMER Pro green energy/storage); [28] Halmous et al. 2024 (grid-connected HRES HOMER, feed-in-tariff sensitivity); [29] Alvarez et al. 2025 (groundwater pumping PV-battery Ecuador, LCOE vs diesel); [30] Kumar et al. 2025 (campus microgrid HOMER, 72% RE fraction); [31] Shaswati et al. 2025 (HRES HOMER); [32] Yasmeena et al. 2024 (EV-fleet microgrid HOMER); [33] Sun et al. 2025 (hybrid microgrid + EV charging HOMER); [34] Swain et al. 2025 (PV/fuel-cell/battery HOMER, hydrogen high LCOE); [35] Ong et al. 2025 (solar+wind into hydropower, HOMER+GIS); [36] Nguyen et al. 2025 (solar-biogas-BESS Vietnam); [37] Karadeniz et al. 2025 (offshore wind site selection HOMER); [38] Lauredo et al. 2025 (GIS rooftop PV HOMER); [41] Arnoos et al. 2024 (BIPV Helioscope+HOMER); [42] Sulistyono et al. 2025 (HRES HOMER Pro).
- **Battery degradation / 100%-renewable feasibility (bounds)**: [43] Gumbrell 2020 (storage in 100% RE NZ 2050); [44] Boretti 2023 (flow batteries net-zero NZ); [45] McIntosh 2025 (hydrogen storage NZ micro-grids); [46] Vaidya et al. 2025 (rooftop-solar EV charging impact); [47] Cavus et al. 2026 (net-load+EV GRU forecasting); [48] Wamalwa & Ishimwe 2024 (grid-tied PV-battery demand response); [49] Chakir et al. 2020 (grid-connected PV-battery EMS).
- **Forecasting / AI reviews (imports)**: [15] Zahari et al. 2024 (PV+storage+DR peak shaving review); [51] Wang et al. 2019 (deep learning RE forecasting review); [52] Benti et al. 2023 (ML/DL RE forecasting); [53] Devaraj et al. 2021 (big-data+DL energy forecasting); [54] Ukoba et al. 2024 (AI RE optimization review); [55] Aslam et al. 2021 (DL power-load/RE forecasting survey); [56] Habbak et al. 2023 (load forecasting techniques); [57] Alkahtani et al. 2023 (AI solar-radiation prediction); [58] Khan et al. 2023 (hybrid DL building consumption/generation — Table 5); [59] Hu et al. 2025 (clustering-enhanced DL load forecasting — Table 5); [60] Wang et al. 2024 (AI smart-energy load/anomaly/DR); [61] Yousef et al. 2023 (AI variable-RE review — Table 5); [62] Baseer et al. 2023 (AI power-generation forecasting — Table 5); [64] Liu & Chen 2019 (wind forecasting data processing); [65] Mawson & Hughes 2020 (DL forecasting/condition monitoring); [17] Jain et al. 2023 (hybrid GA-grey-wolf global optimization).
- **Expansion planning / NNS (extends/baseline)**: [68] de Lima et al. 2024 (distribution expansion planning, new market designs — Table 8 [67]); [69] Borozan & Strbac 2025 (multi-stage T&D expansion, smart investment — Table 8 [68]); [70] Abeygunawardana et al. 2015 (cost-reflective network pricing — Table 8 [69]); [71] Wang et al. 2022 (integrated-energy multi-level planning — Table 8 [70]); [72] Zhou et al. 2020 (health-index + NNS expansion planning — Table 8 [71]); [73] Xing et al. 2018 (optimal siting/sizing distributed RE); [74] Liu et al. 2020 (STATCOM+UVLS voltage-stability NNS, wind); [75] Meng et al. 2019 (offshore AC vs DC transmission planning); [76] Jain & Varshney 2024 (group-key-management for NNS communications); [19] Benitez et al. 2026 (AI RE optimization); [16] Shrivastav & Dutta 2025 (see RW12); [66] Santos et al. 2024 (see RW07); [67] Ramadan et al. 2025 (see RW08).
- **BMS / state estimation (imports)**: [77] Gabbar et al. 2021 (BMS development/standards); [78] Sagar et al. 2022 (BMS in sustainable transport); [79] Krishna et al. 2024 (advanced BMS for EVs); [80] Stecca et al. 2020 (BESS integration into distribution networks); [81] Hu 2024 (BMS simulation platform); [82] Jayasekara et al. 2014 (distributed-storage management high-PV); [83] Raj et al. 2023 (FLC solar charging + BMS); [84] Saidulu et al. 2024 (smart BMS EV); [85] Fan et al. 2022 (battery-pack consistency GAN); [86] Bhuvaneswari et al. 2024 (intelligent BMS EV); [87] Vanlalchhuanawmi et al. 2024 (EMS with EV+BESS review); [88] Sarda et al. 2023 (SoC estimation methods review); [89] Bhattacharya & Bauer 2012 (SoP/SoE charging requirements); [90] Geetha et al. 2024 (IoT sensor-based BMS); [91] Feng et al. 2024 (SoE super-twisting sliding-mode observer); [92] Chen et al. 2025 (see RW11); [93] Sharma & Panigrahi 2025 (S-QRNN SoC/SoE); [94] Liu et al. 2024 (KNN joint SoC/SoE); [95] Zheng et al. 2024 (sliding-mode SoC/SoE observation); [96] Chen et al. 2024 (bidirectional-GRU SoC/SoE); [97] He et al. 2025 (TimesNet + MoE SoC/SoE); [98] Zeng et al. 2024 (PatchTST SoC/SoE co-estimation); [99] Sharma et al. 2022 (see RW09); [100] Safder et al. 2022 (SoE-based islanded DC-grid EMS); [101] Naseri et al. 2020 (supercapacitor SoE/SoH estimation); [102] Gupta et al. 2022 (two-layer grid-aware MPC dispatch validation).
