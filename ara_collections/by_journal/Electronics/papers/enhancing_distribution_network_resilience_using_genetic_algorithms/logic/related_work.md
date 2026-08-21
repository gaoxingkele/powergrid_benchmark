# Related Work

Typed dependency graph. Full `RW` blocks for works with a specific technical delta; the remaining
citation footprint is captured briefly below.

## RW01: Christodoulou et al., 2011 — GA for metal-oxide surge-arrester model parameters
- **DOI**: 10.1016/j.epsr.2011.05.019 (Electr. Power Syst. Res. 2011, 81, 1881–1886) [ref 38]
- **Type**: imports
- **Delta**:
  - What changed: This paper reuses the same authors' "tailored genetic algorithm" methodology —
    originally applied to estimate arrester model parameters by minimizing residual-voltage error —
    and re-targets it at distribution-network control-variable optimization.
  - Why: Establishes GA as a proven engine for the group's power-system parameter-search problems.
- **Claims affected**: C01, C03
- **Adopted elements**: Binary-encoded GA loop (init → encode → selection → crossover → evaluate →
  replace → terminate); error-minimizing natural selection.

## RW02: Panteli & Mancarella, 2015 — power-system resilience conceptual framework
- **DOI**: 10.1109/MPE.2015.2397334 (IEEE Power Energy Mag. 2015, 13, 58–66) [ref 1]; also ref 15
- **Type**: imports
- **Delta**:
  - What changed: Provides the resilience framing (endure/adapt/recover, distinction from
    reliability) that this paper operationalizes as the f3 penalty term.
  - Why: Motivates treating resilience as an explicit design objective.
- **Claims affected**: C01, C04
- **Adopted elements**: Resilience-vs-reliability conceptual distinction; extreme-weather motivation.

## RW03: Vugrin et al., 2017 / Watson et al., 2014 — resilience metrics for the electric power system
- **DOI**: Sandia National Laboratories reports [refs 30, 31]
- **Type**: bounds
- **Delta**:
  - What changed: Supplies performance-based resilience metrics (min voltage, load served, structural
    robustness) that this paper adopts as its three assessment indicators in Table 6.
  - Why: Grounds the quantitative resilience assessment.
- **Claims affected**: C04
- **Adopted elements**: Min bus voltage, load-served ratio, overloaded-branch count as resilience KPIs.

## RW04: Trapezoidal resilience curve sources (IEA 2019 [21]; Christodoulou et al. 2011 [38])
- **DOI**: refs 21, 38
- **Type**: extends
- **Delta**:
  - What changed: Adopts the "trapezoidal" (rather than "triangular") resilience-curve variant to
    depict degradation/recovery stages, and maps the optimized-vs-base contingency results onto it.
  - Why: A more nuanced multi-stage representation of the disturbance response.
- **Claims affected**: C04
- **Adopted elements**: Trapezoidal functionality-vs-time model (Figure 1).

## RW05: Goulioti et al., 2025 — smart-grid tech for HIHF resilience
- **DOI**: 10.3390/en18112793 (Energies 2025, 18, 2793) [ref 29]
- **Type**: imports
- **Delta**:
  - What changed: Source of the HILF→HIHF threat-landscape framing and the Operational vs
    Infrastructure Resilience split used in §2.
  - Why: Justifies the climate-driven shift toward resilience-oriented design.
- **Claims affected**: C01
- **Adopted elements**: HIHF event framing; smart-grid/AI resilience strategies.

## RW06: Prior GA power-system applications (Gonos, Fotis, Evangelides et al.)
- **DOI**: refs 39–42 (ICLP 2010; IEE Proc. Gener. Transm. Distrib. 2002, 149; IEEE Trans. Power
  Deliv. 2005, 20; Meas. Sci. Technol. 2006, 17)
- **Type**: baseline
- **Delta**:
  - What changed: Cited as prior evidence of GA effectiveness on power-system estimation problems
    (surge-arrester model selection, polluted insulators, multi-layer soil parameters, ESD current
    equation).
  - Why: Supports the choice of GA as a general-purpose optimizer.
- **Claims affected**: C01
- **Adopted elements**: GA as the optimization technique of record.

## Broader citation footprint (brief)
- **Resilience definitions & distinctions [refs 1–13]**: reliability (N-1/N-2, LIHF), robustness,
  security/cyber, microgrids, worst-case outage identification — background for §1–§2 definitions.
- **Climate & hazard drivers [refs 14–26]**: temperature, drought, flooding/landslides, humidity/
  snow/ice, wind, sea-level rise, terrorism/cyberattacks, FERC resilience proceeding — motivate the
  resilience focus.
- **Resilience assessment & metrics [refs 27–36]**: metrics/strategies surveys, IPCC/FERC
  definitions, complex-network perspective, quantitative grid-resilience models, automation-on-
  resilience quantification, cyberphysical resilience testbed — background for the assessment approach.
- **AI/GA background [refs 37 (AlphaGo→Power System AI), 38–42]**: motivation and precedent for the
  GA method (ref 38 also RW01).
