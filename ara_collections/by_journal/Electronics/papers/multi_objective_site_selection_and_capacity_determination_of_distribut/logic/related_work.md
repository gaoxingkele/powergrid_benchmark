# Related Work

Typed dependency graph over the paper's 35-reference footprint. Works with a specific technical delta get full `RW` blocks; the remaining citations are listed briefly to preserve the footprint.

## RW18: Zhang, R. et al., 2023 — Dynamic reactive power optimization considering load uncertainty
- **DOI**: Not specified in paper (Proc. 2023 IEEE ITNEC, pp. 1710–1714)
- **Type**: imports / baseline
- **Delta**:
  - What changed: Source of the K-means wind/solar output scenario model this paper builds on, AND the source of the "detailed parameters" of the IEEE 33-node test system used in the case study ("the detailed parameters are shown in Reference [18]").
  - Why: Provides the benchmark system and a prior scenario-planning approach the copula method is meant to improve on.
- **Claims affected**: C03, C01, C02, C05
- **Adopted elements**: IEEE 33-node parameterization; scenario-based planning framing.

## RW29: Zhu, L.J. et al., 2021 — Short-term power load forecasting based on CNN-BiLSTM
- **DOI**: Not specified in paper (Power Syst. Technol. 45, 4532–4539)
- **Type**: imports
- **Delta**:
  - What changed: Origin of the CNN-BiLSTM architecture adopted here for EV-cluster state prediction; this paper repurposes it from load forecasting to EV arrival/departure/SOC prediction.
  - Why: Bidirectional temporal modeling reduces prediction error.
- **Claims affected**: C04
- **Adopted elements**: CNN-BiLSTM model structure.

## RW30: Wang, K. et al., 2022 — Short-term interval probability prediction of PV via QR-CNN-BiLSTM
- **DOI**: Not specified in paper (High Volt. Eng. 48, 4372–4384)
- **Type**: imports
- **Delta**:
  - What changed: Prior CNN-BiLSTM application to PV probabilistic prediction and similar-day clustering; cited in the scenario/EV data processing step.
  - Why: Supports the choice of CNN-BiLSTM for renewable/EV time-series.
- **Claims affected**: C04, C03
- **Adopted elements**: CNN-BiLSTM for renewable time-series.

## RW28: Ding, M. et al., 2018 — Cluster partition of high-penetration DGs via comprehensive performance index
- **DOI**: Not specified in paper (Autom. Electr. Power Syst. 42, 47–52)
- **Type**: imports
- **Delta**:
  - What changed: Cited for the copula/correlation treatment of DG ("Frank copula can work with both non-negative and negative correlations of variables [28]").
  - Why: Justifies Frank-copula choice for wind–solar correlation.
- **Claims affected**: C03
- **Adopted elements**: copula-based correlation handling for DG.

## RW31: Gao, S.; Dai, R., 2023 — Charging control strategy for EV cluster in frequency regulation market
- **DOI**: Not specified in paper (Autom. Electr. Power Syst. 47, 60–67)
- **Type**: imports
- **Delta**:
  - What changed: Source of the EV SOC and charge/discharge power constraints (Eqs. 6–9) formalizing the EVS cluster as dispatchable storage (cited [31,32]).
  - Why: Provides the aggregate SOC dynamics used in the storage model.
- **Claims affected**: C01, C02
- **Adopted elements**: EV-cluster SOC/charge-discharge constraint set.

## RW33: Zhang, P.Z. et al., 2022 — Multi-player two-stage low-carbon operation with EV cluster schedulability
- **DOI**: Not specified in paper (Power Syst. Technol. 46, 4809–4825)
- **Type**: imports
- **Delta**:
  - What changed: Cited [33] for the allowable ranges of EVS SOC and charge/discharge power in the schedulable-potential model.
  - Why: Bounds the dispatchable storage model.
- **Claims affected**: C01
- **Adopted elements**: EVS power/SOC bounds.

## RW21: Huang, Z. et al., 2020 — Multi-objective optimization with V2G-enabled EVs in building integrated energy system
- **DOI**: 10.1186/s41601-020-... (Prot. Control Mod. Power Syst. 5, 1–8) — full DOI not printed
- **Type**: baseline / extends
- **Delta**:
  - What changed: Prior use of EV clusters as energy-storage participants in ADN scheduling; this paper adds DG-uncertainty scenario modeling and joint siting/capacity determination.
  - Why: Positions EV-as-storage within multi-objective distribution planning.
- **Claims affected**: C01, C05
- **Adopted elements**: EV cluster as ADN storage participant.

## RW16: Ghiani, E.; Pilo, F., 2015 — Smart inverter operation in distribution networks with high PV penetration
- **DOI**: Not specified in paper (J. Mod. Power Syst. Clean Energy 3, 504–511)
- **Type**: bounds
- **Delta**:
  - What changed: Inline-cited [16] as prior work on wind–PV correlation / two-layer chance-constraint OPF that this paper argues does not handle storage siting under uncertainty (note: the paper's inline description and the reference-list entry appear mismatched).
  - Why: Motivates the gap (uncertainty + storage siting not jointly handled).
- **Claims affected**: C05
- **Adopted elements**: none (contrast/bounds).

## Briefer citations (footprint preserved)
- **[1–3] Wang/Heidari/Wan (IEEE Trans. 2016–2018)**: DG hosting capacity, distribution automation planning, DG uncertainty boundary — background on DG in ADNs.
- **[4–6] Fang/Zhang/Elkadeem (2019–2021)**: DG output uncertainty sources and renewable-integrated planning under uncertainty — background.
- **[7,8] Li/Zhang (2020–2021)**: RIES modeling, KPI-based situational awareness — DG combined with ADN.
- **[9–11] Chen/Sun/Shi (2020–2023)**: multi-time-scale scheduling, virtual power plant, robust dispatch — multi-timescale scheduling context; [10] cited as the voltage-stability-indicator basis for objective f1.
- **[12,13] Sun/Xing (2020–2023)**: Elbow + K-means wind-speed typical scenarios; EV-PV charging strategy — prior scenario clustering.
- **[14,15] Li/Gao (2019–2020)**: SVG/black-start and SOC-based energy management — reactive-power/voltage regulation prior art.
- **[17] Sudipta/Sukumar (2016)**: energy-function control for DFIG-flywheel; cited for Bi-LSTM/history-future data connection rationale.
- **[19,20] Lu/Zhan (2021–2024)**: EV aggregator frequency/voltage regulation; two-stage charging-station bidding — EV dispatchable-potential prior art.
- **[22–24] Goswami/Qin/Dong (1992–2024)**: feeder reconfiguration for loss minimization, low-carbon multi-objective dispatch, China grid security — power-quality/network-loss and multi-objective background.
- **[25–27] Zhou/Li/Zhang (2022–2024)**: grid-cell distribution planning, UHVDC stochastic planning, AC/DC energy-storage planning under high renewables — DG uncertainty planning background.
- **[32] You et al., 2024**: EV-cluster charging-load calculation — cited with [31] for EV constraints.
- **[34,35] Zhou/Zhao (2021–2024)**: copula-shuffle two-stage stochastic optimization; improved K-means + SBR wind-power scenario reduction — cited for the scenario reduction step.
