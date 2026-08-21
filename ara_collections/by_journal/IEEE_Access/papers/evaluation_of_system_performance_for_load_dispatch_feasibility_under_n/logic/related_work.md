# Related Work

Typed dependency graph over the paper's 44 references. Works with a specific technical delta get full
`RW` blocks; the remaining citations are captured briefly to preserve the full footprint.

## RW01: Beyza, Garcia-Paricio & Yusta, 2019 — Ranking critical assets in interdependent energy transmission networks
- **DOI**: 10.1016/j.epsr.2019.03.014 (Electr. Power Syst. Res., vol. 172)
- **Type**: imports
- **Delta**:
  - What changed: Graph-theory ranking of critical assets from simulated cascading failures for integrated natural-gas and electricity infrastructures.
  - Why: Provides the criticality-ranking lineage this paper extends to individual thermal generators in DA UC.
- **Claims affected**: C02, C07
- **Adopted elements**: Criticality-ranking concept; IEEE RTS data source.

## RW02: Beyza, Ruiz-Paredes, Garcia-Paricio & Yusta, 2020 — Criticality of interdependent power and gas systems
- **DOI**: 10.1016/j.physa.2019.123169 (Phys. A, vol. 540)
- **Type**: imports
- **Delta**:
  - What changed: Geodesic vulnerability index for coupled gas-electricity criticality under simulated disruptions.
  - Why: Background for system-criticality assessment via state estimation / phasor measurements.
- **Claims affected**: C02
- **Adopted elements**: Criticality-analysis framing; IEEE RTS data reference.

## RW05: Khanabadi, Ghasemi & Doostizadeh, 2013 — Optimal transmission switching considering voltage security and N-1 contingency
- **DOI**: 10.1109/TPWRS.2012.2213097 (IEEE Trans. Power Syst., vol. 28, no. 1)
- **Type**: bounds
- **Delta**:
  - What changed: Transmission-line switching to enhance performance in OPF under N-1 contingencies.
  - Why: Contrast — prior N-1 work targets transmission switching, not DA-UC generator contingencies.
- **Claims affected**: C01
- **Adopted elements**: N-1 contingency problem setting.

## RW07: Nan, Liu, Wu & He, 2021 — Graph theory based N-1 transmission contingency selection in SCUC
- **DOI**: 10.35833/MPCE.2020.000895 (J. Modern Power Syst. Clean Energy, vol. 9, no. 6)
- **Type**: bounds
- **Delta**:
  - What changed: N-1 transmission-line contingency selection within security-constrained UC.
  - Why: Closest prior N-1-in-UC work, but on transmission lines rather than generators and without the four-metric performance framework.
- **Claims affected**: C01
- **Adopted elements**: N-1-contingency-based UC framing.

## RW09: Govardhan, Master & Roy, 2014 — Reliability-constrained unit commitment with demand response
- **DOI**: — (Power Res.-A J. CPRI, vol. 10, no. 3)
- **Type**: imports
- **Delta**:
  - What changed: Reliability metrics (LOLP, LOLE) established for UC reliability analysis.
  - Why: Source for using LOLP/LOLE as the reliability indices adopted here.
- **Claims affected**: C04, C08
- **Adopted elements**: LOLP/LOLE reliability-index basis.

## RW10: Billinton, 1996 — Reliability Evaluation of Power Systems (2nd ed.)
- **DOI**: — (Plenum Press book)
- **Type**: imports
- **Delta**:
  - What changed: Probabilistic reliability formulation (generation unavailability, COPT, LOLP).
  - Why: The LOLP/COPT probability calculations are referred to this and RW11.
- **Claims affected**: C04, C08
- **Adopted elements**: COPT and LOLP mathematical formulation; FR/MTTF data basis.

## RW11: Billinton & Allan, 1992 — Reliability Evaluation of Engineering Systems
- **DOI**: — (Plenum Press book, vol. 792)
- **Type**: imports
- **Delta**:
  - What changed: Engineering-reliability probability methods (failure/repair rate → unavailability).
  - Why: Co-source with RW10 for probability-of-load-loss and COPT computations.
- **Claims affected**: C04, C08
- **Adopted elements**: Failure-rate/repair-rate probability method.

## RW12: Wang, Kang & Liu, 2020 — Optimal scheduling for electric bus fleets by dynamic programming
- **DOI**: 10.1016/j.rser.2020.109978 (Renew. Sustain. Energy Rev., vol. 130)
- **Type**: imports
- **Delta**:
  - What changed: Argues DP yields the most optimal solution vs heuristic/metaheuristic approaches.
  - Why: Justification for choosing DP as the DA-UC optimizer.
- **Claims affected**: C01
- **Adopted elements**: DP-optimality rationale.

## RW13: Espiritu, Coit & Prakash, 2007 — Component criticality importance measures for the power industry
- **DOI**: 10.1016/j.epsr.2006.03.007 (Electr. Power Syst. Res., vol. 77, nos. 5–6)
- **Type**: bounds
- **Delta**:
  - What changed: Birnbaum, Fussell-Vesely, RAW, RRW, Criticality Importance (CI) metrics via FMEA for transmission criticality.
  - Why: Establishes component-level criticality metrics that do NOT address generator-level DA-UC criticality (Gap G2).
- **Claims affected**: C02, C07
- **Adopted elements**: Criticality-metric vocabulary (contrast).

## RW27: Jain & Kanwar, 2025 — Optimized unit commitment for peak load management with solar PV and storage
- **DOI**: — (Sci. Rep., vol. 15, no. 1)
- **Type**: extends
- **Delta**:
  - What changed: The DA-UC constraint set (shutdown cost, min up/down time, active-power limits, ramp rates) and CM definition are referred from this prior work by the same authors.
  - Why: Supplies the UC constraint formulations reused in Eq. 3–8 and the CM concept.
- **Claims affected**: C01, C04, C06
- **Adopted elements**: UC constraints; contingency-margin / spinning-reserve modeling.

## RW28: Jain & Kanwar, 2019 — Day-ahead optimal scheduling of generators using dynamic programming method
- **DOI**: — (Proc. 8th Int. Conf. Power Syst. (ICPS))
- **Type**: extends
- **Delta**:
  - What changed: The DP method for DA UC used here.
  - Why: Prior authors' DP-based DA-UC methodology that this paper builds the contingency analysis on.
- **Claims affected**: C01
- **Adopted elements**: DP DA-UC solver.

## RW29: Jain, Pachar & Gidwani, 2020 — Reliability-constrained day-ahead UC with optimal spinning reserve for solar-integrated system
- **DOI**: — (Proc. 5th IEEE Int. Conf. Recent Adv. Innov. Eng. (ICRAIE))
- **Type**: extends
- **Delta**:
  - What changed: Reliability-constrained DA UC with optimal spinning-reserve allocation.
  - Why: Prior authors' work linking spinning reserve, reliability, and DA UC — the lineage of the reserve-vs-reliability trade-off.
- **Claims affected**: C04
- **Adopted elements**: Spinning-reserve / reliability DA-UC modeling.

## RW30: Albrecht et al., 1979 — IEEE Reliability Test System (RTS-79)
- **DOI**: 10.1109/TPAS.1979.319398 (IEEE Trans. Power Appar. Syst., vol. PAS-98, no. 6)
- **Type**: baseline
- **Delta**:
  - What changed: Defines the original IEEE RTS used as the test system.
  - Why: Source of the 24-bus, 26-generator test system and its data.
- **Claims affected**: C02, C03, C06, C07, C08
- **Adopted elements**: Test-system topology and generator data.

## RW32: Grigg et al., 1999 — IEEE RTS-96 (Reliability Test System update)
- **DOI**: 10.1109/59.780914 (IEEE Trans. Power Syst., vol. 14, no. 3)
- **Type**: baseline
- **Delta**:
  - What changed: Updated IEEE RTS data.
  - Why: Co-source for the generator data (fuel coefficients, limits, ramp/startup, up/down times).
- **Claims affected**: C02, C06
- **Adopted elements**: Generator dataset.

## RW34: Central Electricity Authority (India), 2022 — Draft Guidelines for Resource Adequacy Planning Framework for India
- **DOI**: — (Government guideline, cea.nic.in)
- **Type**: imports
- **Delta**:
  - What changed: Specifies LOLP_max = 0.05 for India.
  - Why: Provides the LOLP_max threshold used to compute the operating margin.
- **Claims affected**: C05
- **Adopted elements**: LOLP_max = 0.05 value.

## Additional citations (brief)
- **[3] Liu, Pan, Liu & Zhu, 2021** — Contingencies-based distributionally robust co-risk operation for combined electricity & heat (IEEE Access, vol. 9). *Type: bounds* — combined heat/electricity flexibility under uncertain component states.
- **[4] Mazumdar & Kapoor, 1995** — Stochastic models for power generation production costs (Electric Power Syst. Res., vol. 35, no. 2). *Type: imports* — probability distribution of uncertain generator outages affecting UC cost.
- **[6] Faraji, Hashemi-Dezaki & Ketabi, 2021** — Stochastic operation/scheduling of energy hub with renewable uncertainty and N-1 (Sustain. Cities Soc., vol. 65). *Type: bounds* — integrated renewable sources for reliability under N-1.
- **[8] Oliveira et al., 2017** — Power system security assessment for multiple contingencies via multiway decision tree (Electric Power Syst. Res., vol. 148). *Type: bounds* — multi-contingency security assessment.
- **[14] Mei, Ni, Wang & Wu, 2008** — Self-organized criticality of power system via AC-OPF with voltage stability margin (IEEE Trans. Power Syst., vol. 23, no. 4). *Type: bounds* — SOC criticality under cascading failures; IEEE RTS data source.
- **[15] David & Sansavini, 2018** — Identification of critical states by limit-state surface reconstruction (Int. J. Electr. Power Energy Syst., vol. 101). *Type: bounds* — criticality index via distance from limit surface; data source.
- **[16] Göl & Abur, 2013** — Observability and criticality analyses measured by phasor measurements (IEEE Trans. Power Syst., vol. 28, no. 3). *Type: bounds* — PMU-based criticality.
- **[17] Espinoza et al., 2016** — Risk and resilience assessment with component criticality ranking under earthquakes (IEEE Syst. J., vol. 14, no. 2). *Type: bounds* — seismic criticality.
- **[18] Zheng, Okamura, Pang & Dohi, 2021** — Availability importance measures in smart grid (Rel. Eng. Syst. Saf., vol. 205). *Type: bounds* — component criticality in smart grid.
- **[19] Peng, Coit & Feng, 2012** — Component reliability criticality/importance for degrading systems (IEEE Trans. Rel., vol. 61, no. 1). *Type: bounds* — criticality for individual/correlated outages.
- **[20] Benjamin, Tan & Razon, 2015** — Criticality analysis in integrated energy systems (Clean Technol. Environ. Policy, vol. 17, no. 4). *Type: bounds* — integrated-system criticality.
- **[21] Chan & Athans, 1984** — Robustness theory applied to power system models (IEEE Trans. Autom. Control, vol. AC-29, no. 1). *Type: bounds* — early frequency-domain robustness margins (SMIB/MIMO).
- **[22] Zhang & Yağan, 2016** — Optimizing robustness against cascading failures (Sci. Rep., vol. 6, no. 1). *Type: bounds* — robustness to cascading line failures.
- **[23] Xiang, Wang & Liu, 2018** — Robustness-oriented grid operation considering attacks (IEEE Trans. Smart Grid, vol. 9, no. 5). *Type: bounds* — SCOPF robustness under cyber/physical attacks.
- **[24] Tu, Xia, Iu & Chen, 2019** — Optimal robustness in power grids from network science (IEEE Trans. Circuits Syst. II, vol. 66, no. 1). *Type: bounds* — topological robustness metrics.
- **[25] Hong, Wu, Hsiao & Lin, 2021** — Reliability with high renewable penetration: scenario-based study (IEEE Access, vol. 9). *Type: bounds* — functional robustness of dynamics under faults.
- **[26] Rios, Hadjsaid, Feuillet & Torres, 1999** — Power system stability robustness via μ-analysis (IEEE Trans. Power Syst., vol. 14, no. 2). *Type: bounds* — SVC robustness evaluation.
- **[31] Allan, Billinton & Abdel-Gawad, 1986** — IEEE RTS extensions to the generating system (IEEE Trans. Power Syst., vol. PS-1, no. 4). *Type: baseline* — RTS generator-data extension.
- **[33] Barrows et al., 2020** — IEEE RTS: a proposed 2019 update (IEEE Trans. Power Syst., vol. 35, no. 1). *Type: baseline* — RTS update; data source.
- **[35] Chaiamarit & Nuchprayoon, 2013** — Modeling renewable resources for generation reliability evaluation (Renew. Sustain. Energy Rev., vol. 26). *Type: imports* — US DOE LOLP_max 0.002 reference.
- **[36] European Standards, 2025** — (cencenelec.eu). *Type: imports* — EU LOLP_max 0.008 reference.
- **[37] Brown & Smith, 2025** — UC without commitment: DP for integrated energy system under uncertainty (Oper. Res., vol. 73, no. 4). *Type: imports* — future-work DP/stochastic scenario modeling.
- **[38] Greenough et al., 2025** — Wildfire-resilient unit commitment under uncertain demand (IEEE Trans. Power Syst., vol. 40, no. 4). *Type: imports* — future-work extension basis.
- **[39] Mohan et al., 2025** — Real-time congestion control using cascaded LSTM deep neural networks (Sci. Rep., vol. 15, no. 1). *Type: imports* — future-work LSTM-based control.
- **[40] Qu & Yang, 2025** — Infeasibility cutting plane for unit commitment (CSEE J. Power Energy Syst.). *Type: imports* — future-work infeasibility-aware optimization.
- **[41] Huang et al., 2025** — Consensus-based distributed quantum decomposition for SCUC with optimal transmission switching (Adv. Quantum Technol., vol. 1). *Type: imports* — future-work quantum/distributed optimization.
- **[42] Hamadneh et al., 2025** — Rabbit and Turtle Algorithm (Int. J. Intell. Eng. Syst., vol. 18, no. 6). *Type: imports* — future-work metaheuristic.
- **[43] Hamadneh et al., 2025** — Farmer and Seasons Algorithm (Int. J. Intell. Eng. Syst., vol. 18, no. 6). *Type: imports* — future-work metaheuristic.
- **[44] Hamadneh et al., 2025** — Negotiators Algorithm (Int. J. Intell. Eng. Syst., vol. 18, no. 6). *Type: imports* — future-work metaheuristic.
