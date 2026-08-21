# Related Work

## RW01: Keshavarzzadeh and Ahmadi, 2019
- **DOI**: 10.1016/j.enconman.2019.05.061
- **Type**: baseline
- **Delta**:
  - What changed: Proposed a multi-objective techno-economic optimization of a solar-based IES using mixed-integer linear programming; the present paper handles non-linearities through GA rather than MILP.
  - Why: MILP approaches struggle with non-convexities introduced by tiered pricing structures.
- **Claims affected**: C01, C02
- **Adopted elements**: IES modeling framework with CHP and renewable integration.

## RW02: Yang et al., 2023
- **DOI**: 10.1016/j.ijepes.2022.108902
- **Type**: baseline
- **Delta**:
  - What changed: Proposed IES coordinated scheduling considering demand response and carbon trading; used multi-objective optimization but without the GA enhancements proposed in the present work.
  - Why: Standard MOEA approaches may not handle constraint satisfaction as effectively as the proposed IGA.
- **Claims affected**: C03
- **Adopted elements**: Multi-objective optimization framework for IES scheduling.

## RW03: Wang et al., 2022
- **DOI**: 10.1016/j.egyr.2022.01.246
- **Type**: baseline
- **Delta**:
  - What changed: Applied NSGA-II with dynamic crowding distance for rural IES multi-objective optimization. The present work builds on NSGA-II but adds cyclic crossover and polynomial mutation.
  - Why: Dynamic crowding distance alone does not address the crossover/mutation limitations that the IGA targets.
- **Claims affected**: C01, C02
- **Adopted elements**: NSGA-II fast non-dominated sorting and crowding distance concepts.

## RW04: Deb et al., 2002 (NSGA-II)
- **DOI**: 10.1109/4235.996017
- **Type**: extends
- **Delta**:
  - What changed: The IGA extends NSGA-II by replacing the standard crossover and mutation operators with cyclic crossover and polynomial mutation, and embedding a constraint-prioritizing parent selection mechanism.
  - Why: Standard NSGA-II operators may not preserve beneficial genetic structure or handle equality constraints as effectively.
- **Claims affected**: C01, C02, C03
- **Adopted elements**: Fast non-dominated sorting, crowding distance, and the overall elitist multi-objective framework.

## RW05: Michalewicz and Schoenauer, 1996
- **DOI**: 10.1162/evco.1996.4.1.1
- **Type**: baseline
- **Delta**:
  - What changed: Foundational work on evolutionary algorithms for constrained optimization. The SGA baseline in this paper follows the classical GA framework described here.
  - Why: Standard GA methods face exploration/exploitation trade-offs that the IGA aims to improve.
- **Claims affected**: C01, C04
- **Adopted elements**: Standard GA chromosome representation, selection, crossover, and mutation concepts (for the SGA baseline).

## RW06: Coello and Lechuga, 2002 (MOPSO)
- **DOI**: Not provided (conference paper)
- **Type**: baseline
- **Delta**:
  - What changed: MOPSO is used as a multi-objective baseline for comparison; it employs penalty function methods for constraint handling rather than the IGA's constraint-elitist approach.
  - Why: Penalty functions treat equality constraints as soft objectives, leading to higher violations as shown in the comparison results.
- **Claims affected**: C05
- **Adopted elements**: Used as a comparative benchmark only.

## RW07: Akbari et al., 2012 (MOABC)
- **DOI**: 10.1016/j.swevo.2011.08.002
- **Type**: baseline
- **Delta**:
  - What changed: MOABC is used as a multi-objective baseline; also employs penalty function methods for constraint handling.
  - Why: Similar penalty-function limitation as MOPSO.
- **Claims affected**: C05
- **Adopted elements**: Used as a comparative benchmark only.

## RW08: Lv et al., 2023
- **DOI**: 10.1016/j.egyr.2023.04.116
- **Type**: imports
- **Delta**:
  - What changed: Proposed bi-directional tiered-pricing carbon trading for electricity-heat-gas systems, which informed the tiered carbon pricing model in the present work.
  - Why: Tiered carbon pricing is an important real-world mechanism that IES optimization should consider.
- **Claims affected**: C03
- **Adopted elements**: Bi-directional tiered-pricing carbon trading concept adapted as a three-tier carbon emission pricing mechanism.

## Additional Background References

The paper also cites the following works for context and infrastructure:
- Wang et al. (2017) — Review of residential tiered electricity pricing in China (Ref. [6])
- Kuang and Lin (2021) — Performance of tiered natural gas pricing in China (Ref. [8])
- Song et al. (2022) — Critical survey of integrated energy systems (Ref. [4])
- Berjawi et al. (2021) — Evaluation framework for future IESs (Ref. [5])
- Zhong et al. (2020) — Stochastic optimization of IES (Ref. [13])
- Li et al. (2021) — Operation optimization of IES (Ref. [14])
- Zhang et al. (2019) — Optimal planning of IES (Ref. [15])
- Carvalho et al. (2017) — Adaptive penalty scheme for constrained optimization (Ref. [16])
- Jia et al. (2024) — DRL-based energy management (Ref. [1])
- Jiang et al. (2024, 2025) — Short-term load forecasting methods (Refs. [2, 3])
- Wang et al. (2022) — Flexible solar power generation (Ref. [17])
- Niu et al. (2024) — Thermal risks in EV chargers (Ref. [18])
- Li and Wang (2024) — Swing contract market design (Ref. [19])
- Yang et al. (2023) — PMSM drive nonlinear friction identification (Ref. [20])
- Hong Kong Electric Company (2023) — Residential electricity price list (Ref. [21])
- Zhang and Yao (2024) — Multi-user IES service sharing (Ref. [24])
