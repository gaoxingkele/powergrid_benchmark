# Related Work

Typed dependency graph for Yang et al., Electronics 2023, 12, 4230. Reference numbers are the
paper's own [N]. Full RW blocks for works with a specific technical delta; the remaining citation
footprint is preserved briefly at the end.

## RW01: Pang et al., 2022 (ref [14])
- **DOI**: Not specified in paper (Power Syst. Autom. 2022, 46, 13–24)
- **Type**: imports
- **Delta**:
  - What changed: [14] introduced a rolling optimization model for real-time operation of
    distribution-network islands (multi-DG output characteristics, AC flow, radial and steady-state
    safety constraints). This paper adopts the rolling scheme but extends it across BOTH the
    islanding stage and the fault recovery stage, adds the Eq. (2) threshold that avoids
    re-partitioning on every period, and embeds wind/PV uncertainty via scenarios.
  - Why: troubleshooting time is variable; fixed-horizon plans based on pre-fault predictions are
    suboptimal.
- **Claims affected**: C03, C05
- **Adopted elements**: rolling optimization with per-period feedback correction; radial/safety
  constraint structure

## RW02: Liu & Cui, 2020 (ref [19])
- **DOI**: Not specified in paper (Huadian Technol. 2020, 42, 29–34)
- **Type**: extends
- **Delta**:
  - What changed: [19] melded islanding with network reconstruction for fault recovery to tackle
    partial load non-recovery in DG-integrated networks. This paper additionally couples the two
    stages through the recovery-stage load weight β_{i,k} (Eq. 36), which [19]-style approaches
    lack, and drives both stages by rolling optimization under uncertainty.
  - Why: island-stage supply history (membership churn, no-power periods) affects user electricity
    satisfaction and should shape recovery priorities.
- **Claims affected**: C04, C05
- **Adopted elements**: joint islanding + reconstruction view of fault recovery

## RW03: Ma et al., 2019 (ref [23])
- **DOI**: Not specified in paper (Power Syst. Prot. Control 2019, 47, 48–57)
- **Type**: imports
- **Delta**:
  - What changed: [23] used second-order cone relaxation to turn a fault-reconstruction model with
    adjustable DGs/capacitor banks into a mixed-integer SOCP keeping voltages in range. This paper
    reuses the SOC relaxation of the branch-flow model (Eqs. 16–20, 43–45) but layers a
    scenario-weighted stochastic extension (Eq. 48) on top.
  - Why: tractable convex formulation of the nonconvex distribution power flow.
- **Claims affected**: C04
- **Adopted elements**: mixed-integer SOCP formulation of reconstruction; big-M line-status relaxation

## RW04: Wang et al., 2023 (ref [26])
- **DOI**: Not specified in paper (Proc. CSEE 2023, 45, 1–19)
- **Type**: imports
- **Delta**:
  - What changed: the weighted multi-objective form of the fault-recovery objective (Eq. 35 —
    restored load minus loss term minus switching term) is adopted "in the form of (35) [26]".
  - Why: standard scalarization for load-recovery/loss/switching trade-offs.
- **Claims affected**: C04, C05
- **Adopted elements**: weighted-sum objective structure

## RW05: Xu et al., 2021 (ref [27])
- **DOI**: Not specified in paper (Autom. Electr. Power Syst. 2021, 45, 38–46)
- **Type**: imports
- **Delta**:
  - What changed: adopts the Weibull description of wind speed ("The existing literature mostly
    uses Weibull distribution to describe wind speed [27]") as the wind uncertainty model (Eq. 40).
  - Why: established parametric wind-speed model.
- **Claims affected**: C02
- **Adopted elements**: Weibull wind-speed probability density function

## RW06: Baran & Wu, 1989 (ref [28])
- **DOI**: 10.1109/61.25627 (IEEE Trans. Power Deliv. 1989, 4, 1401–1407; CrossRef in paper)
- **Type**: imports
- **Delta**:
  - What changed: supplies the IEEE 33-node benchmark; this paper improves it by adding 4 DGs
    (wind/PV at node 6, storage at node 13, diesel at nodes 24 and 31).
  - Why: standard, widely recognized distribution test system.
- **Claims affected**: C01, C03, C04 (test-bed validity)
- **Adopted elements**: 33-node radial network topology and branch-flow context

## RW07: Zhang et al., 2019 (ref [7])
- **DOI**: Not specified in paper (Electr. Meas. Instrum. 2019, 56, 63–68+75)
- **Type**: baseline
- **Delta**:
  - What changed: [7] maximized power-supply restoration, user satisfaction, and minimized demand
    response cost for island division. This paper keeps satisfaction as a driver but locates it in
    the recovery weight β rather than the island-division objective, and treats division jointly
    with recovery.
  - Why: [7]-style methods optimize island division alone, neglecting stage correlation (Gap G1).
- **Claims affected**: C01, C05
- **Adopted elements**: user-satisfaction motive for weighting loads

## RW08: Ying et al., 2021 (ref [8])
- **DOI**: Not specified in paper (Power Syst. Clean Energy 2021, 37, 91–97)
- **Type**: imports
- **Delta**:
  - What changed: [8] built island division on comprehensive load weights (multiple attributes and
    user preferences). This paper uses a simpler three-level static weight (Table 2) but makes the
    weight dynamic at recovery time via Eq. (36).
  - Why: overcome single-attribute load importance.
- **Claims affected**: C01, C05
- **Adopted elements**: load-weight-based island division

## RW09: Wang et al., 2019 (ref [15])
- **DOI**: 10.1109/TSG.2018.2803141 (IEEE Trans. Smart Grid 2019, 10, 2507–2522; CrossRef in paper)
- **Type**: bounds
- **Delta**:
  - What changed: [15] evaluated wind/PV uncertainty impact on distribution-network resilience via
    risk-limiting, multi-stage scheduling. This paper instead handles uncertainty by scenario
    generation/reduction inside a single scenario-weighted SOCP per rolling step.
  - Why: integrate uncertainty directly with the islanding+recovery formulation (Gap G3).
- **Claims affected**: C02, C03
- **Adopted elements**: framing of uncertainty-aware island operation flexibility

## RW10: Tang et al., 2020 (ref [22])
- **DOI**: Not specified in paper (Power Syst. Technol. 2020, 44, 2731–2740)
- **Type**: baseline
- **Delta**:
  - What changed: [22] handled recovery under new-energy randomness with uncertain bilevel
    programming. This paper replaces the bilevel machinery with scenario-weighted SOCP plus rolling
    feedback, and adds the stage-coupling weight.
  - Why: tractability (mature CPLEX SOCP solving) and stage correlation.
- **Claims affected**: C04
- **Adopted elements**: recovery-under-uncertainty problem framing

## RW11: Chen et al., 2019 (ref [24])
- **DOI**: Not specified in paper (Electr. Meas. Instrum. 2019, 56, 46–51)
- **Type**: bounds
- **Delta**:
  - What changed: [24] combined reconstruction and island partitioning with black-start capability,
    fault recovery time, and maintenance sequence on SOCP basis. This paper does not model
    black-start/maintenance sequencing but adds renewable uncertainty and the satisfaction-aware
    weight.
  - Why: different slice of the joint problem; delineates what this paper does not cover.
- **Claims affected**: C04, C05
- **Adopted elements**: comprehensive reconstruction + islanding recovery viewpoint

## Remaining citation footprint (brief)

- [1] Han et al., IEEE Trans. Sustain. Energy 2023 — background: communication/control optimization
  for wind farms with storage (new-energy development context).
- [2] Li et al., Autom. Electr. Power Syst. 2018 — background: dynamic reconfiguration with EVs and
  DGs; motivates DG-induced complexity.
- [3] Wang et al., Power Syst. Technol. 2022 — background: reconstruction strategies for fault
  recovery under DG uncertainty (reliability significance).
- [4] Liang et al., Power Syst. Technol. 2021 — background: CPS fault simulation with network
  information security.
- [5] Ye et al., Power Syst. Technol. 2022 — background: knowledge graph for fault handling.
- [6] Osama et al., IEEE Syst. J. 2020 — background: planning framework for optimal partitioning
  into microgrids (islanding-division prerequisite).
- [9] El-Sayed et al., IEEE Trans. Power Syst. 2022 — inline comparison: droop-based islanded
  microgrids with optimum loadability (maximize island load capacity, resist local interference).
- [10] Wang et al., IEEE Access 2022 — inline: fault reconfiguration under uncertainty for maximum
  supply capacity (uncertainty-aware division).
- [11] Zhu et al., J. Mod. Power Syst. Clean Energy 2018 — inline: integrated island partition and
  power dispatch.
- [12] Yang et al., Smart Grid 2019 — inline: real-time dynamic islanding detection considering
  source–network–load interaction.
- [13] Wu et al., Electr. Power Autom. Equip. 2023 — inline: post-disaster islanding detection with
  information–energy coupling nodes.
- [16] Bian et al., Autom. Electr. Power Syst. 2013 — inline: uncertainty reconfiguration with
  demand response (time-of-use price moderation).
- [17] Zheng et al., Smart Power 2019 — inline: reactive power optimization + reconstruction via
  mixed-integer SOCP.
- [18] Liu et al., Electr. Meas. Instrum. 2018 — inline: multi-objective fault restoration under DG
  output randomness (use all network resources in recovery).
- [20] Huang et al., Power Syst. Prot. Control 2022 — inline: reconstruction with demand-side
  response under high clean-energy penetration.
- [21] Yan et al., Autom. Electr. Power Syst. 2022 — inline: post-disaster restoration using
  multiple DGs/storage based on outage-loss assessment.
- [25] Yun et al., CSEE J. Power Energy Syst. 2020 — inline: multi-period collaborative restoration
  for electric–gas systems, two-stage solving, rolling optimization.
- [29] Fang et al., Electr. Meas. Instrum. 2023 — infrastructure: outage probability from real-time
  equipment failure rate (source of DG parameters, with [30,31]).
- [30] Li et al., Electr. Meas. Instrum. 2022 — infrastructure: micro-grid fault recovery via
  improved BPSO (DG parameter source).
- [31] Wei et al., Electr. Meas. Instrum. 2022 — infrastructure: fault location via Lambda
  algorithm (DG parameter source).
