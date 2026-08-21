# Related Work

Typed dependency graph over the paper's 25 references. Works with a specific technical delta get
full RW blocks; the remainder are captured briefly to preserve the citation footprint.

## RW05: Albizu et al., 2018 — Adaptive Static Line Rating for HTLS Conductors
- **DOI**: 10.1109/TPWRD.2018.2822598
- **Type**: bounds
- **Delta**:
  - What changed: Adjusts the assumed wind speed in the rating calculation for higher-permissible-
    temperature conductors to reduce thermal-limit exceedance risk.
  - Why: Represents the conservative SLR baseline the paper argues DLR should replace.
- **Claims affected**: C01
- **Adopted elements**: Framing of SLR conservatism as the gap DLR closes.

## RW06: González-Cagigal et al., 2024 — Reliability of DLR via Conductor Temperature Estimation
- **DOI**: 10.1016/j.epsr.2024.110449
- **Type**: imports
- **Delta**:
  - What changed: DLR reliability assessment based on conductor temperature estimation.
  - Why: Supports the claim that DLR significantly enhances transmission capacity.
- **Claims affected**: C01
- **Adopted elements**: Evidence that DLR is a reliable enhancement over SLR.

## RW07: Bhattarai et al., 2018 — Weather-Based Dynamic Line Rating Ampacity Utilization
- **DOI**: 10.1109/TPWRD.2017.2779907
- **Type**: imports
- **Delta**:
  - What changed: Improves transmission-line ampacity utilization via weather-based DLR.
  - Why: Empirical basis that DLR raises usable transfer capability.
- **Claims affected**: C01
- **Adopted elements**: Weather-driven ampacity utilization concept.

## RW12: Zhang et al., 2021 — Hot-Spot Prediction / Dynamic Transformer Rating Scheduling
- **DOI**: 10.1109/ACCESS.2021.3056141
- **Type**: bounds
- **Delta**:
  - What changed: Scheduling model built on dynamic transformer ratings and lifetime-loss
    characteristics to mitigate aging.
  - Why: The paper cites it as prior art that "may become invalid under abnormal high-temperature
    conditions, where thermal stability parameters change drastically."
- **Claims affected**: C02
- **Adopted elements**: The idea of coupling transformer lifetime loss to scheduling; the paper
  addresses its extreme-heat breakdown.

## RW13: Bagheri et al., 2025 — MIQCP Multi-Objective Operation with Transformer Loss of Life
- **DOI**: 10.1016/j.epsr.2024.111252
- **Type**: bounds
- **Delta**:
  - What changed: MIQCP multi-objective operation for renewables-integrated distribution systems
    considering transformer loss of life and emissions; source of the ES ∈ [1.3, 1.5] loss-process
    factor range.
  - Why: Represents failure-probability/economic transformer-aging modeling the paper argues is
    inadequate for unexpected extreme-weather fault risk.
- **Claims affected**: C02, C05
- **Adopted elements**: Additional-loss process-factor range; multi-objective framing.

## RW14: Hosseinkhanloo et al., 2022 — Transformer Fleet Exploitation via Loss of Life & Failure Probability
- **DOI**: 10.1016/j.epsr.2022.108801
- **Type**: bounds
- **Delta**:
  - What changed: Optimal transformer-fleet exploitation using loss of life and failure-probability
    economic evaluation.
  - Why: Cited for the claim that transformer loading is the dominant factor determining hot-spot
    temperature and lifetime loss.
- **Claims affected**: C02
- **Adopted elements**: Loading-dominance premise motivating dispatch-side control.

## RW19: Frank et al., 2013 — Temperature-Dependent Power Flow
- **DOI**: 10.1109/TPWRS.2013.2266409
- **Type**: imports
- **Delta**:
  - What changed: Temperature-dependent power flow with the three-component conductor temperature
    decomposition (ambient/solar, resistive, higher-order radiative correction).
  - Why: Basis for Eqs. 5-8 (the β0/β1/β2 steady-state temperature model).
- **Claims affected**: C01
- **Adopted elements**: Conductor temperature-rise decomposition adopted directly.

## RW18: Ngoko et al., 2018 — Simplified Overhead Conductor Temperature Model (vs CIGRE)
- **DOI**: 10.1541/ieejpes.138.284
- **Type**: imports
- **Delta**:
  - What changed: Simplified DLR conductor-temperature estimation validated against CIGRE.
  - Why: Source of the empirical convective coefficients B1, n1 (Eq. 2).
- **Claims affected**: C01
- **Adopted elements**: Empirical convective-heat-transfer coefficient form.

## RW20: Luo et al., 2025 — FBG Hot-Spot Dynamic Temperature Rise Sensing
- **DOI**: 10.1109/JSEN.2025.xxxx
- **Type**: imports
- **Delta**:
  - What changed: Hot-spot dynamic temperature rise of oil-immersed transformers via FBG sensing.
  - Why: Basis for the ultimate hot-spot temperature decomposition TH = Ta + ∆TM + ∆Tu (Eq. 17).
- **Claims affected**: C02
- **Adopted elements**: Hot-spot temperature superposition formula.

## RW21: Hashmi et al., 2013 — Climate Change Effect on Transformer Loading
- **DOI**: 10.4236/ojapps.2013.31B1005
- **Type**: imports
- **Delta**:
  - What changed: IEC-based aging rule (98 C rated hot-spot; +6 C doubles aging rate).
  - Why: Directly underpins the life-loss cost model threshold.
- **Claims affected**: C02, C04
- **Adopted elements**: 98 C / 6 C-doubling aging rule.

## RW22: Li et al., 2023 — Miner's-Rule / Sequential Rule Mining (cited for damage accumulation)
- **DOI**: 10.1109/TKDE.2022.3161580
- **Type**: imports
- **Delta**:
  - What changed: Cited alongside IEEE/ANSI C57.91 for the linear (miner's-rule) damage-accumulation
    basis of the life-loss cost (Eq. 20).
  - Why: Formal basis for additive life-loss accumulation.
- **Claims affected**: C02, C04
- **Adopted elements**: Linear damage accumulation principle.

## RW23: Djamali & Tenbohlen, 2017 — Cooling-System Malfunction Detection / OA-ONAN Parameters
- **DOI**: 10.1109/TPWRD.2016.2578322
- **Type**: imports
- **Delta**:
  - What changed: Empirical OA/ONAN cooling parameters.
  - Why: Source of FT = 1.4, n = 0.9, m = 0.8 used in the hot-spot model.
- **Claims affected**: C02
- **Adopted elements**: OA/ONAN empirical exponents/factor.

## RW24: GB/T 38969-2020 — Guide on Technology for Power System
- **DOI**: n/a (Chinese national standard)
- **Type**: imports
- **Delta**:
  - What changed: Technical guideline fixing the spinning-reserve margin factor α = 0.02.
  - Why: Sets the reserve constraint parameter (Eq. 27).
- **Claims affected**: C03
- **Adopted elements**: Reserve margin factor.

## RW25: Zhou et al., 2016 — Probabilistic Equivalent Model of DFIG Wind Farms
- **DOI**: 10.1007/s40565-016-0208-5
- **Type**: imports
- **Delta**:
  - What changed: DFIG/PSASP wind-turbine equivalent model.
  - Why: Basis for modeling the equivalent wind turbines at buses 17 and 21.
- **Claims affected**: C03
- **Adopted elements**: DFIG equivalent wind-farm model.

## Brief citations (background / infrastructure, no distinct technical delta)
- **RW01 Qin et al., 2022** (10.1109/TPWRS.2021.3123531) — coordination of preventive/emergency/
  restorative dispatch in extreme weather; motivates operational-risk framing.
- **RW02 Trakas & Hatziargyriou, 2022** (10.1109/TPWRS.2021.3116821) — resilience via undergrounding
  lines; extreme-weather resilience context.
- **RW03 Zhou et al., 2025** — testing-temperature effects on transformer oil-paper insulation;
  insulation-aging context.
- **RW04 Ilunga et al., 2024** (10.1109/ACCESS.2024.xxxx) — conductor temperature effect on corona
  performance; transmission-side heating context.
- **RW08 Gezegin et al., 2021** — monitoring winding/hot-spot temperatures of oil-immersed
  transformers; sensing background.
- **RW09 Wang et al., 2024** — transformer fatigue life/damage under short-circuit; failure-context.
- **RW10 Paramane et al., 2014** — CFD radiator thermal performance; cooling-enhancement background.
- **RW11 Fathi et al., 2025** (10.1016/j.applthermaleng.2025.125775) — heat-pipe transformer cooling;
  also cited for the 0.8/3.5/0.7 top-oil regression constants.
- **RW15 Shaker et al., 2012** — fuzzy dynamic thermal rating of transmission lines; thermal-rating
  definition.
- **RW16 Wang et al., 2018** — contingency analysis with transient thermal behavior of lines;
  overheating/sag failure background.
- **RW17 Davidzon, 2012** — Newton's law of cooling interpretation; basis for convective-loss Eq. 1.
