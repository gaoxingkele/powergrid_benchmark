# Claims

## C01 — Priority index model enables quantitative discrimination of DESS demand across distribution nodes

**Statement:** The Critic-weighted multi-indicator priority index (combining quality indicators I1–I7 and efficiency indicators) provides a quantitative ranking of energy storage deployment urgency across nodes within a grid-based distribution network, discriminating between load-dominant and generation-dominant blocks.

**Conditions:**
- The distribution network must be partitioned into grid blocks with known load-type composition.
- Node-level quality indicators (I1–I7) and efficiency indicators (matching degree) must be available from planning-stage data.
- The Critic method objectively assigns weights based on indicator variability and inter-indicator correlation.

**Sources:**
> "The priority index measures the intensity of energy storage demand in distribution networks, based on a multi-criteria assessment of demand indicators." (Section 3.3, p. 11)
> "The Critic approach, an objective weighting technique, allocates weights in a multi-indicator comprehensive evaluation by analysing the correlation and disparities among indicators, thus scientifically assessing the significance of each indicator." (Section 3.3, p. 11)
> "Through the proposed Critic method, the weights of the quality indicators I1 to I7 are obtained as 0.05, 0.19, 0.15, 0.08, 0.18, 0.17, and 0.19, respectively." (Section 3.4.3, p. 15)

**Status:** Supported by evidence.
**Falsification:** A distribution grid where the priority index ranking fails to correlate with observed outage frequency, voltage violation rate, or peak-to-valley stress across nodes would falsify this claim.
**Proof:** E02 (priority index construction and weighting), E04 (multi-dimensional evaluation showing Case 2/3 improvements over Case 1)
**Evidence basis:** Table 2 (quality indicator definitions), Table 4 (equipment parameters), Figure 14 (node-level priority indices), Figure 15 (demand indicators of selected nodes)
**Dependencies:** O3, O4, G1
**Tags:** priority index, Critic method, demand assessment

---

## C02 — Sequential priority-index updating prevents spatial over-concentration of DESS compared to one-shot priority ranking

**Statement:** Recalculating the priority index after each DESS installation iteration (sequential planning) leads to a more spatially balanced distribution of energy storage across heterogeneous grid blocks, avoiding the excessive concentration that occurs when all sites are selected from a single priority ranking.

**Conditions:**
- Multiple candidate blocks with different source–load characteristics exist within the same distribution network.
- The budget constraint limits the total number of DESS installations (here, three units).
- The sequential process updates the generalized load curve after each deployment.

**Sources:**
> "By sequentially updating the priority index, Case 3 adaptively adjusts the siting decision after each installation and finally selects nodes 49, 121, and 147 (733, 1166, and 1176 kWh), which avoids excessive concentration and achieves a more balanced configuration." (Section 4.3, p. 22)
> "Case 3 avoids the excessive spatial concentration observed in Case 2 while achieving the highest economic return among all cases." (Section 4.3, p. 22)
> "Case 2 selects nodes 49, 121, and 157 (733, 1166, and 1076 kWh) based on a one-time priority ranking and exhibits local concentration because nodes 121 and 157 both belong to Block 21." (Section 4.3, p. 22)

**Status:** Supported by evidence.
**Falsification:** A distribution network where sequential priority-index updating selects nodes that are more concentrated within a single block than one-shot priority ranking would falsify this claim.
**Proof:** E03 (sequential planning comparison across Cases 1–3)
**Evidence basis:** Table 5 (storage planning results), Figure 14 (priority indices per iteration), Figure 15 (demand indicator profiles)
**Dependencies:** C01, G4
**Tags:** sequential planning, spatial concentration, priority index

---

## C03 — Priority-guided DESS planning improves node-level stability and economic return compared to global traversal

**Statement:** Using the priority index for site selection (either one-shot or sequential) produces DESS configurations with superior node optimization potential (O1), economic efficiency (O2), and renewable integration (O3) compared to exhaustive global traversal that searches all nodes without demand-based prioritization.

**Conditions:**
- The global traversal method (Case 1) selects DESS locations by sorting all nodes by objective function value without demand-based pre-filtering.
- Node-level evaluation metrics O1, O2, and O3 are measured after DESS deployment.

**Sources:**
> "In terms of O1, the indicator value of Case 2 increased from 0.548 in Case 1 to 0.684 (+25%), demonstrating that the priority index method can more effectively harness the potential to improve power supply quality at nodes." (Section 5, p. 25)
> "For O2, the metric value rose from 0.308 to 0.622 (+102%), demonstrating that the DESS configuration delivers superior economic benefits while maintaining stronger operational resilience." (Section 5, p. 25–26)
> "In O3, Case 2 overcame Case 1's limitation in renewable utilization (O3 = 0) through improved renewable-load coordination." (Section 5, p. 26)

**Status:** Supported by evidence.
**Falsification:** A distribution network where global traversal yields higher or equal O1, O2, and O3 values compared to priority-index-based siting would falsify this claim.
**Proof:** E03 (sequential planning comparison), E04 (multi-dimensional evaluation)
**Evidence basis:** Figure 16 (comparison of evaluation indicators), Table 5 (economic comparison), Table 6 (electrical performance)
**Dependencies:** C01
**Tags:** priority vs. traversal, node-level metrics, economic efficiency

---

## C04 — Priority-index-based DESS planning improves block-level source-load matching and quality-demand satisfaction

**Statement:** DESS deployment guided by priority indices significantly increases block-level source-load matching rate (L1) and high-quality demand satisfaction (L2) compared to global traversal, because DESS is placed where demand is highest rather than where the raw optimization objective is best.

**Conditions:**
- Block-level evaluation metrics L1 and L2 are defined as per Formulas (34)–(35).
- Blocks have heterogeneous source–load characteristics (some load-dominant, some generation-dominant).

**Sources:**
> "In L1, the indicator value increased from 0.043 to 0.079 (+82%), demonstrating that Case 2 achieves more effective power distribution balancing within the block." (Section 5, p. 26)
> "The L2 rose from 0.0464 to 0.787 (+70%), demonstrating the effectiveness of the prioritized index method in optimizing regional power supply quality and load-balancing." (Section 5, p. 26)

**Status:** Supported by evidence.
**Falsification:** A grid where global traversal achieves L1 or L2 values comparable to or higher than priority-index-based planning would falsify this claim.
**Proof:** E04 (multi-dimensional evaluation)
**Evidence basis:** Figure 16 (evaluation indicators comparison), Figure 10 (matching degree per block)
**Dependencies:** C01, C02, O1, O4
**Tags:** block-level matching, source-load coordination, quality demand

---

## C05 — Priority-index-based DESS planning with sequential updating improves grid-wide coordination uniformity

**Statement:** The combination of priority-index guidance and sequential updating yields the highest grid-level coordination uniformity (G2) and high-quality demand improvement (G1) compared to either global traversal or one-shot priority ranking, because the sequential process distributes resilience resources more equitably across the grid.

**Conditions:**
- Grid-level metrics G1 and G2 are evaluated using Formulas (36)–(37).
- The grid contains multiple blocks with diverse load types and source–load characteristics.

**Sources:**
> "G1 increased from 0.017 to 0.021 (+25%), and G2 surged from 0.003 to 0.014 (+324%)." (Section 5, p. 26)
> "Among the three cases presented in Figure 12, Case 3 has the highest evaluation index value, signifying that it is the most rational option." (Section 5, p. 26)
> "The disparity in source-load coordination among various grid blocks has diminished, leading to a more equitable distribution of overall resilience." (Section 5, p. 26)

**Status:** Supported by evidence.
**Falsification:** A grid where Case 1 or Case 2 achieves G1 or G2 values equal to or higher than Case 3 would falsify this claim.
**Proof:** E04 (multi-dimensional evaluation)
**Evidence basis:** Figure 16 (all indicators comparison across cases)
**Dependencies:** C02, C03, C04
**Tags:** grid-level coordination, uniformity, resilience distribution
