# Related Work

## RW01: Ahmed & Salama, 2019 — Energy management of AC-DC hybrid distribution considering reconfiguration
- **DOI**: 10.1109/TPWRS.2019.2921358 (IEEE Trans. Power Syst. 34:4583-4594)
- **Type**: bounds
- **Delta**:
  - What changed: This paper plans investment (line DC retrofit, DG siting) rather than operational two-stage energy management with reconfiguration.
  - Why: Data-center DC-load penetration requires topology-design and planning decisions, not just EMS.
- **Claims affected**: C01, C04
- **Adopted elements**: The idea that AC/DC hybrid structure and reconfiguration are jointly optimizable.

## RW02: Yang, Zhang & Li, 2019 — Two-stage robust reactive-voltage control for hybrid AC/DC networks
- **DOI**: — (Proc. CSEE 39:4764-4774)
- **Type**: bounds
- **Delta**:
  - What changed: Robust reactive-voltage control coordinates AC/DC converter stations for uncertainty; this paper instead optimizes topology/planning under time-series multi-scenarios.
  - Why: Planning-stage siting vs operation-stage control are complementary.
- **Claims affected**: C08
- **Adopted elements**: Coordination of AC/DC converter stations for voltage performance.

## RW03: Fang, Yang & Fan, 2018 — AC/DC distribution network planning based on flexibility time series
- **DOI**: — (Electr. Energy Manag. Technol. 15:17-24)
- **Type**: extends
- **Delta**:
  - What changed: This paper adopts the flexibility/time-series planning idea and extends the voltage-stability index (Eq. 6) to a data-center multi-scenario, DG-aware setting.
  - Why: Data-center DC loads need penetration-driven topology evolution.
- **Claims affected**: C06, C08
- **Adopted elements**: Time-series-based planning framing; voltage-stability index reference [22].

## RW04: Jing et al., 2019 — Review of DC distribution network topology and fault diagnosis
- **DOI**: — (2019 IEEE ICIEA, pp. 1681-1685)
- **Type**: baseline
- **Delta**:
  - What changed: Provides the chain / ring / double-ended topology taxonomy that this paper's multi-level tier-aware design goes beyond.
  - Why: Generic topologies are not data-center-tier-specific.
- **Claims affected**: C07
- **Adopted elements**: The topology taxonomy as design starting point (ref [7]).

## RW05: Yang, Liu & Su, 2021; Liu et al., 2022 — Suzhou Tongli ±10kV flexible DC distribution
- **DOI**: — (Power Eng. Technol. 40:113-120; 2022 CICED pp.1217-1221)
- **Type**: imports
- **Delta**:
  - What changed: Real ±10kV dual-supply flexible-DC demonstration informs the physical-level DC architectures.
  - Why: Grounds the DC bus / converter design in a demonstration project.
- **Claims affected**: C07
- **Adopted elements**: Dual-supply flexible-DC topology (refs [8,9]).

## Additional citations (brief)
- **[1] Yu et al., 2021** — New-infrastructure impact on power-system planning (14th Five-Year); motivates data-center growth.
- **[2] Feng et al., 2020** — Review of data-center energy management in energy internet; background.
- **[3] Wu, 2018** — HVDC UPS in data centers; background on DC UPS.
- **[4,5] Zou et al., 2022; Zu et al., 2020** — Flexible DC transmission status and simulation; DC efficiency motivation.
- **[6] Ren & Yang, 2022** — Data-management framework for nuclear plants; new-infrastructure context.
- **[10] Ahmed & Salama** — see RW01.
- **[11] Yang et al.** — see RW02.
- **[12] Wawrzola, 2016** — DC data-center protection / zone selectivity; fault-location background.
- **[13] Kang et al., 2021** — LVDC superconducting distribution for data centers; power quality/loss.
- **[14] Yu et al., 2022** — New electric-power data center on DC supply/distribution; control scheme.
- **[15] Haro-Larrode et al., 2021** — Fractional-order resonant controller tuning for VSC in weak AC grid.
- **[16] Wang et al., 2024** — Data-center integrated energy system (DC-IES) review.
- **[17] Chen et al., 2023** — Data-center power supply from grid edge to point-of-load.
- **[18] Han et al., 2024** — Construction/evaluation of a full DC power supply system in data centers.
- **[19] Ahmed et al., 2020; [20] Singh et al., 2002** — Sigma converter / eServer z900 power-packaging; medium-voltage AC supply context.
- **[21] Al-Obaidi et al.** — Review of non-isolated bidirectional DC-DC converters for hybrid storage; DC interface background.
- **[22] Fang, Yang & Fan, 2018** — see RW03 (voltage-stability index source).
