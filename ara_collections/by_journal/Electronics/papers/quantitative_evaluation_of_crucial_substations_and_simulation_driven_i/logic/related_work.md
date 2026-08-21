# Related Work

Typed dependency graph over the paper's 19 references. Full blocks for works with a specific technical delta; brief entries for background/infrastructure citations.

## RW07: Han et al., 2023 — Deep-learning joint DG–substation siting/sizing
- **DOI**: 10.3389/fenrg.2022.1089921
- **Type**: bounds
- **Delta**:
  - What changed: Uses LSTM forecasting inside a two-stage stochastic mixed-integer bilinear program for siting/capacity under uncertain load.
  - Why: Represents the load-uncertainty-focused planning line this paper contrasts against.
- **Claims affected**: (motivates G1)
- **Adopted elements**: none (positioned as prior focus on plan generation, not delay-impact quantification).

## RW08: Abedi et al., 2020 — Fuzzy sub-transmission substation expansion planning
- **DOI**: 10.1002/2050-7038.12421
- **Type**: bounds
- **Delta**:
  - What changed: Fuzzy load functions + clustering to site substations/MV feeders under load-distribution uncertainty.
  - Why: Load-uncertainty planning contrast.
- **Claims affected**: (motivates G1)
- **Adopted elements**: none.

## RW09: Mohaghegh et al., 2019 — Fuzzy-logic DG/substation expansion under uncertainty
- **DOI**: 10.3906/elk-2005-56
- **Type**: bounds
- **Delta**:
  - What changed: Fuzzy modeling of load and energy-price uncertainty for siting/capacity/feeder expansion.
  - Why: Load/price uncertainty contrast.
- **Claims affected**: (motivates G1)
- **Adopted elements**: none.

## RW10: Yang et al., 2022 — Multi-agent game + robust optimization planning
- **DOI**: 10.3389/fenrg.2022.803716
- **Type**: bounds
- **Delta**:
  - What changed: Game theory + robust optimization over multiple stakeholders (DG operators, DSOs, consumers, storage).
  - Why: Stakeholder-uncertainty planning contrast.
- **Claims affected**: (motivates G1)
- **Adopted elements**: none.

## RW11: Zhang et al., 2017 — Distribution substation planning period under forecast error
- **DOI**: 10.17775/CSEEJPES.2017.0036
- **Type**: bounds
- **Delta**:
  - What changed: Robust optimization addressing load-forecast-error impact on substation planning cycles.
  - Why: Highlights forecast error but not delay-induced investment cascades.
- **Claims affected**: (motivates G1)
- **Adopted elements**: none.

## RW12: Cajas et al., 2022 — Multi-voltage transmission expansion planning
- **DOI**: (IEEE ISGT-Europe 2022; CrossRef)
- **Type**: bounds
- **Delta**:
  - What changed: Hybrid meta-heuristic (differential evolution + PBIL) for multi-voltage transmission expansion.
  - Why: Multi-voltage joint planning line; optimizes the plan, ignores deviation cost.
- **Claims affected**: (motivates G1)
- **Adopted elements**: multi-voltage joint-planning framing.

## RW13: Klein et al., 2017 — Integrated multi-voltage network expansion
- **DOI**: (IEEE ISGT-Europe 2017; CrossRef)
- **Type**: bounds
- **Delta**:
  - What changed: Heuristic minimization of total multi-voltage cost over lines/transformers/substations.
  - Why: Closest in objective (total-cost minimization) but no delay/deviation analysis.
- **Claims affected**: (motivates G1); parallels the Eq. 8 cost objective.
- **Adopted elements**: total-cost minimization objective for multi-voltage grids.

## RW14: Zheng et al., 2019 — Coordinated transmission–distribution planning
- **DOI**: (RPG 2019 proceedings)
- **Type**: bounds
- **Delta**:
  - What changed: Joint model over transmission/distribution substations and feeders with a holistic evaluation system.
  - Why: Joint planning + evaluation, but not delay-impact quantification.
- **Claims affected**: (motivates G1, G2)
- **Adopted elements**: comprehensive evaluation-system framing.

## RW15: Müller et al., 2019 — eGo 100 integrated techno-economic planning
- **DOI**: 10.3390/en12112091
- **Type**: bounds
- **Delta**:
  - What changed: Open-source top-down tool scaling the grid across all voltage levels via nonlinear-power-flow heuristic optimization.
  - Why: Multi-voltage optimization tool; overlooks financial impact of deviations from the plan.
- **Claims affected**: (motivates G1)
- **Adopted elements**: cross-voltage-level optimization framing.

## RW16: Lv & Yang, 2020 — Demand-guided multi-dimensional investment index
- **DOI**: (IEEE ITAIC 2020; CrossRef)
- **Type**: bounds
- **Delta**:
  - What changed: Investment-effect evaluation index system using electricity demand + economic/social factors.
  - Why: Evaluation-index line lacking empirical outcome validation.
- **Claims affected**: (motivates G2)
- **Adopted elements**: multi-dimensional index-system concept.

## RW17: Liu C. et al., 2022 — CoV + fuzzy substation project evaluation
- **DOI**: (IEEE CEECT 2022; CrossRef)
- **Type**: bounds
- **Delta**:
  - What changed: Coefficient-of-variation combination weighting + fuzzy comprehensive scoring across four project dimensions.
  - Why: Alternative weighting/evaluation; still not validated against realized cost.
- **Claims affected**: (motivates G2); alternative to AHP weighting.
- **Adopted elements**: none (this paper uses AHP instead).

## RW18: Liu Z. et al., 2022 — AHP-entropy distribution-network evaluation
- **DOI**: 10.3389/fenrg.2022.975462
- **Type**: extends
- **Delta**:
  - What changed: AHP-entropy weighting balancing expert judgment with data to reduce AHP subjectivity/instability.
  - Why: Directly relevant precedent; this paper uses plain AHP (no entropy cross-check — see constraints limitations).
- **Claims affected**: C01
- **Adopted elements**: AHP weighting for a distribution-network evaluation index system.

## RW19: Dash et al., 2024 — MCDM + self-organizing maps for energy systems
- **DOI**: 10.3390/technologies12030042
- **Type**: imports
- **Delta**:
  - What changed: Cited as the methodological reference for AHP as a multi-criteria decision-analysis framework.
  - Why: Grounds the choice of AHP.
- **Claims affected**: C01
- **Adopted elements**: AHP as MCDA method.

## Brief citations (background / infrastructure)
- **RW01 — Li et al., 2018** (IEEE TPWRS, 10.1109/TPWRS.2017.2687318): robust coordinated transmission/generation expansion with ramping and construction periods — background on construction-period-aware planning.
- **RW02 — Wang et al., 2021** (CIEEC): technical-loss analysis of the Hubei grid — background on China grid loss/coordination challenges.
- **RW03 — Ayokunle et al., 2020** (ICISMS): technical vs non-technical losses in Nigeria — background on developing-region losses.
- **RW04 — Chorshanbiev et al., 2020** (EIConRus): power-loss assessment in 0.4–500 kV Tajik networks — background on multi-level network losses.
- **RW05 — Gao et al., 2021** (Front. Energy Res., 10.3389/fenrg.2021.697959): cyber-physical coordinated distribution planning — motivates investment-risk mitigation.
- **RW06 — Vahid et al., 2020** (IEEE Access, 10.1109/ACCESS.2020.2973525): overview of distribution-network expansion planning — background survey.
