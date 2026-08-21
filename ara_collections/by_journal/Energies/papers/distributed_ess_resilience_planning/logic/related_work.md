# Related Work Dependency Graph

## RW01 — Cluster-Based DESS Planning

**Citations:** [9] Li et al. (2025) *J. Clean. Prod.*; [10] Shi et al. (2025) *Electr. Power Syst. Res.*

**Type:** bounds

**Delta:** Prior cluster-based methods partition the network into regions and optimize DESS within each region, but they do not use multi-dimensional demand indicators to rank nodes. The current paper imports the block-partitioning concept but extends it with a priority-index model that evaluates each node's storage demand using quality and efficiency criteria rather than relying solely on cluster-level optimization objectives.

---

## RW02 — DESS for Voltage Regulation

**Citations:** [11] Ma et al. (2025) *Electronics*; [12] Zhao et al. (2020) *Appl. Energy*; [13] Xu et al. (2025) *Appl. Energy*

**Type:** bounds

**Delta:** These works establish the technical capability of DESS for voltage and frequency regulation, which the current paper acknowledges as background. The current paper differs by focusing on planning-stage DESS deployment rather than real-time operational control, and by evaluating a broader set of resilience dimensions beyond voltage regulation.

---

## RW03 — Node Sensitivity-Based DESS Placement

**Citations:** [14] Shi et al. (2023) *Autom. Electr. Power Syst.*; [15] Su et al. (2019) *PESGM*; [16] Chen et al. (2024) *Int. J. Electr. Power Energy Syst.*; [17] Hong et al. (2021) *Int. Trans. Electr. Energy Syst.*; [18] Su et al. (2019) *Power Syst. Technol.*; [19] Du et al. (2019) *Power Syst. Prot. Control*; [20] Zhang et al. (2024) *Energies*

**Type:** baseline

**Delta:** The paper explicitly positions the proposed multi-dimensional priority index as an improvement over single-criterion sensitivity indices (voltage sensitivity [15,16,17], loss sensitivity variance [18,19,20], integrated power-flow sensitivity variance [20]). While sensitivity-based methods rely on deterministic or representative scenarios and limited functional objectives, the proposed approach incorporates renewable uncertainty via GMM, multi-objective optimization, and multi-scale resilience evaluation. Both similarity: sequential siting procedures are used in [16,17,18,20] and in the current paper — but the current paper adds priority-index recalculation between iterations.

---

## RW04 — Renewable Uncertainty Modeling (Scenario Generation)

**Citations:** [21] Zheng et al. (2025) *Energies*; [22] Peng et al. (2024) *J. Phys. Conf. Ser.*; [23] Ren et al. (2025) *Front. Phys.*

**Type:** imports

**Delta:** The paper imports the GMM methodology from [22] (PV prediction with GMM clustering) and the evaluation perspective from [23] (scenario quality assessment beyond basic statistical moments). The extension is the use of RV-coefficient-based K-means initialization for the GMM to preserve extreme operating scenarios better than random initialization.

---

## RW05 — CRITIC Objective Weighting Method

**Citations:** [35] Alkan (2024) *Sustain. Energy Grids Netw.*

**Type:** imports

**Delta:** The CRITIC method [35] is adopted directly for objective weight determination of quality indicators. The paper does not modify the CRITIC formulation but applies it in the novel context of DESS planning priority indices.

---

## RW06 — Distribution Network Planning Standards

**Citations:** [36] DL/T 5729-2023 (Chinese National Standard)

**Type:** bounds

**Delta:** The block partitioning methodology in the case study follows this standard. The paper does not modify or extend the partitioning method — it adopts existing planning outcomes as given.

---

## Summary Typology

| Type | Count | Citations |
|------|-------|-----------|
| **imports** | 3 | [22], [23], [35] |
| **bounds** | 6 | [9,10], [11,12,13], [36] |
| **baseline** | 7 | [14,15,16,17,18,19,20] |
| **extends** | 0 | — |
| **refutes** | 0 | — |
