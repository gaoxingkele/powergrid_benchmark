# Related Work Dependency Graph

## RW01: Luo et al. (2024) — Dynamic reconfiguration with wind/solar uncertainty modeling

**Type:** baseline
**Delta:** The current paper extends dynamic reconfiguration by incorporating a two-layer framework with DRO and flexibility metrics, going beyond interval prediction.
**Source:** "Luo et al. proposed a dynamic reconfiguration strategy that models wind and solar uncertainties through interval prediction and scenario generation." [Page 2]

## RW02: Gong and Wu (2021) — Risk assessment with stochastic power flow

**Type:** baseline
**Delta:** The current paper adds reconfiguration optimization and a two-layer architecture on top of uncertainty quantification.
**Source:** "Gong and Wu introduced a risk assessment model combining stochastic power flow and failure probability to quantify operational risk." [Page 2]

## RW03: Herath et al. (2023) — Flexibility enhancement with Normalized Flexibility Index

**Type:** baseline
**Delta:** The current paper adapts the flexibility metric concept from planning-level to branch-level operational flexibility within a reconfiguration framework.
**Source:** "Herath et al. proposed a flexibility enhancement process using a Normalized Flexibility Index and Violation Probability metric to guide planning." [Page 2]

## RW04: Huang et al. (2025) — Multi-scale flexibility quantification in district heating

**Type:** bounds
**Delta:** Different application domain (heating networks vs. power distribution), but similar multi-scale flexibility quantification concept informs the current paper's approach.
**Source:** "Huang et al. developed a multi-scale flexibility quantification approach in district heating networks to support EPS scheduling." [Page 2]

## RW05: Yi et al. (2018) — Multiobjective robust dispatch with demand response uncertainty

**Type:** baseline
**Delta:** The current paper extends to DRO (rather than robust) with a two-layer architecture incorporating topology optimization. Reference performance: "achieving 4.2% cost reduction in IEEE 33-bus system under 200 scenarios." [Page 14]
**Source:** "Yi et al. developed a multiobjective robust dispatch framework incorporating demand response uncertainty." [Page 2]

## RW06: Liao et al. (2022) — Affine adjustable robust strategy for active distribution networks

**Type:** baseline
**Delta:** The current paper claims improved performance through two-layer architecture with topology co-optimization rather than purely operational robust control.
**Source:** "Liao et al. proposed an affine adjustable robust strategy coordinating PV, load, and storage under distribution network uncertainty." [Page 2]

## RW07: Huang et al. (2024) — Web-of-cells two-layer optimization with flexibility metrics

**Type:** baseline | imports
**Delta:** Most closely related architecture. The web-of-cells two-layer model inspired the current paper's architecture. The current paper adds DRO and equipment maintenance considerations, while addressing the limitation that the prior work had "higher average cost due to lack of loss minimization." [Page 14]
**Source:** "Huang et al. designed a web-of-cells two-layer model incorporating supply-demand flexibility metrics." [Page 2]

## RW08: Hao et al. (2024) — Two-layer optimization with EV scheduling

**Type:** baseline
**Delta:** Similar two-layer structure but focused specifically on EV scheduling; the current paper generalizes to multi-resource coordination including multiple DG types, storage, and flexible loads.
**Source:** "Hao et al. proposed a similar structure integrating EV scheduling with distribution network loss minimization." [Page 2]

## RW09: Zhao et al. (2024) — Electrode configuration for alkaline water electrolyzer

**Type:** bounds
**Delta:** Demonstrates device-level optimization impact on system-level energy performance, motivating hardware-software co-optimization as a broader principle.
**Source:** "Zhao et al. investigated the optimal electrode configuration for a compactly assembled industrial alkaline water electrolyzer, whose result highlights the importance of coupling hardware optimization with system-level scheduling and control." [Page 2]

## RW10: Baran and Wu — Disflow power flow model

**Type:** imports
**Delta:** The Disflow model is the foundational power flow formulation used and adapted in this paper with big-M relaxation for reconfiguration.
**Source:** "The traditional Disflow power flow model is a simplified power flow calculation method widely used in distribution network analysis, proposed by Baran and Wu." [Page 3]

## RW11: Del Pizzo et al. (2024) — Italian TSO operational adjustments

**Type:** bounds
**Delta:** Provides real-world context for high RES penetration challenges. Not directly used in the optimization model but motivates the problem.
**Source:** "Del Pizzo et al. analyzed the operational adjustments made by the Italian TSO to manage high RES penetration during low-load seasons." [Page 1]

## RW12: Wang et al. (2025) — Capacity adequacy and pricing

**Type:** bounds
**Delta:** Market/regulatory perspective on dispatchable capacity under high renewables; provides motivation for flexibility assessment.
**Source:** "Wang et al. emphasized the risk of insufficient dispatchable capacity under high renewable conditions, advocating for new capacity pricing strategies." [Page 1]

## Summary Graph

```
[10] Baran & Wu Disflow ──imports──> Upper-layer power flow constraints
[7]  Huang web-of-cells  ──imports──> Two-layer architecture
[3]  Herath flexibility index ──baseline──> FBF index in upper layer
[5]  Yi robust dispatch  ──baseline──> Lower-layer DRO formulation
[6]  Liao affine robust  ──baseline──> (improved upon)
[1]  Luo dynamic reconfiguration ──baseline──> Reconfiguration strategy
[2]  Gong risk assessment ──baseline──> Uncertainty quantification
[8]  Hao EV two-layer    ──baseline──> (similar but narrower scope)
[9]  Zhao electrolyzer   ──bounds──> Hardware-software co-optimization motivation
[4]  Huang multi-scale flexibility ──bounds──> Flexibility quantification concept
[11] Del Pizzo Italian TSO ──bounds──> Real-world RES integration context
[12] Wang capacity pricing  ──bounds──> Market adequacy motivation
```
