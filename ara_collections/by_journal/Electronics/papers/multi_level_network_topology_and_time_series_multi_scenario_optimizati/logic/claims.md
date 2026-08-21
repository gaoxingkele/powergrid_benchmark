# Claims

## C01: DC share of the cost-optimal topology tracks data-center DC-load penetration, above a converter-cost threshold
- **Statement**: When a distribution network absorbs data-center load, the cost-minimizing proportion of DC (versus AC) in the topology increases with the data-center DC-load penetration; below a threshold set by converter capital cost the all-AC topology stays optimal, because DC retrofit only reduces lifecycle cost once the conversion links it eliminates outweigh the converter investment it adds.
- **Conditions**: 13-node radial test network, single VSC unit cost, DG output and load represented as typical time-series scenarios, penetration grown in 10%-per-cycle steps; the no-retrofit regime is observed at/below 40% penetration and staged retrofit begins at 50%; behaviour above 80% penetration and for meshed networks or other converter-cost regimes is untested.
- **Sources**: [40% ← evidence/tables/table3.md «| I | 10%, 20%, 30%, 40% | N/A | N/A | N/A |» [result]; 50% ← evidence/tables/table3.md «| II | 50%, 60% | Bus6 | 5–6 | N/A |» [result]]
- **Status**: supported
- **Falsification criteria**: If an optimized hybrid topology delivered lower lifecycle cost than the all-AC topology even at negligible DC-load penetration (i.e. DC retrofit paid off with essentially no DC load present), the threshold mechanism would be false.
- **Proof**: [E01, E02]
- **Evidence basis**: Figure 7 shows Scenario 1 (real DC loads) becoming largely DC while Scenario 2 (same load as AC) stays largely AC; Figure 8 + Table 3 show no DC retrofit at 0-40% and progressively more DC structure at 50/60/70/80%.
- **Dependencies**: C06
- **Tags**: topology, penetration, converter-cost, threshold

## C02: The grid-connection and large-capacity AC-generator buses resist DC conversion under high penetration
- **Statement**: The highest-level grid-connection nodes and buses electrically tied to large-capacity AC generation remain AC even at high DC-load penetration, because converter cost scales with throughput capacity and becomes prohibitive precisely at these high-capacity interface points.
- **Conditions**: 13-node evolution example, penetration up to 80%; grid-connection buses 1, 2, 3 stay AC at 70-80% while the rest converts to DC; holds where the external grid interface and large generators are AC; not tested for a natively-DC grid interface.
- **Sources**: []
- **Status**: supported
- **Falsification criteria**: Observing the grid-connection buses (or large-capacity AC-generator buses) converted to DC in a cost-optimal plan at high penetration, despite their large converter capacity, would refute it.
- **Proof**: [E02]
- **Evidence basis**: Table 3 (buses 1, 2, 3 never appear in any retrofit phase); Figure 8d (80% case leaves only buses 1, 2, 3 AC); §5.1 text on high grid-connection converter cost.
- **Dependencies**: C01
- **Tags**: topology, grid-connection, converter-capacity

## C03: Cost-optimal DC conversion concentrates at feeder extremities
- **Statement**: Placing DC sub-systems and distributed generation at feeder ends (the low-throughput extremities) minimizes required converter capacity and converter loss, so cost-optimal plans locate DC lines and DG at line ends rather than on the high-flow trunk.
- **Conditions**: modified IEEE33 with per-node DC-load proportions and a fixed DG candidate set on branches; holds for radial topologies where end-of-line power flows are smallest; not tested on meshed networks.
- **Sources**: []
- **Status**: supported
- **Falsification criteria**: A cost-optimal plan that preferentially converts trunk / high-flow lines to DC while leaving low-flow feeder ends AC would refute the mechanism.
- **Proof**: [E03]
- **Evidence basis**: Table 5 (DC-modified lines and DG cluster at end nodes 13, 17, 23, 30, 31); Figure 10; §5.3 text ("most of the DC lines are at the end of the system, which reduces the converter capacity and saves investment").
- **Tags**: converter-placement, feeder-end, loss-reduction

## C04: Allowing line DC retrofit reallocates conversion from many per-unit converters to few shared ones, lowering total cost
- **Statement**: Permitting DC line reconstruction/new-build lets a plan replace many distributed per-DG and per-load converters with a smaller number of shared DC-subsystem converters, so total annual economic cost and network loss fall relative to a plan that forbids DC lines, even though a new DC-line converter cost appears.
- **Conditions**: modified IEEE33, VSC $170/kVA, fixed per-node DC-load proportions; the reallocation drives DG- and load-converter cost down while adding a DC-line converter cost; the net-saving magnitude is regime-specific.
- **Status**: supported
- **Falsification criteria**: If forbidding DC lines produced equal or lower total annual economic cost and network loss than allowing them, the reallocation benefit would be false.
- **Proof**: [E05]
- **Evidence basis**: Table 8 — annual economic cost 177.6870 vs 183.7880 $M; DG-grid converter 0.32 vs 23.34; load converter 3.102 vs 24.245; DC-line converter 26.6 vs 0; loss 884.12 vs 1223.45 MW·h.
- **Sources**: [177.6870 ← evidence/tables/table8.md «| Annual economic cost/($ million) | 177.6870 | 183.7880 |» [result]]
- **Dependencies**: C03
- **Tags**: converter-cost, cost-reallocation, network-loss

## C05: Eliminating converter links via DC sub-systems raises distributed-generation hosting capacity
- **Statement**: Because DC sub-systems remove converter links and thereby cut per-unit DG loss and investment, a DC-enabled plan accommodates more distributed generation than a DC-forbidden plan optimized under the same objective.
- **Conditions**: modified IEEE33; DG installed in 60 kVA increments; hosting gain observed for the DC-enabled optimum over the DC-forbidden optimum; not generalized to thermally- or congestion-limited networks.
- **Status**: supported
- **Falsification criteria**: A DC-enabled optimum that hosted less or equal DG capacity than the DC-forbidden optimum would refute the claim.
- **Proof**: [E03, E04]
- **Evidence basis**: Table 5 total DG capacity 1500 kVA (WT 840 + PV 660) versus Table 7 total 1080 kVA (WT 600 + PV 480).
- **Sources**: [1500 ← evidence/tables/table5.md «WT: 840; PV: 660; Total capacity: 1500» [result]; 1080 ← evidence/tables/table7.md «WT: 600; PV: 480; Total capacity: 1080» [result]]
- **Dependencies**: C04
- **Tags**: DG-hosting, converter-elimination

## C06: Probability-weighted time-series multi-scenario embedding makes the optimal topology scenario-dependent
- **Statement**: Embedding distributed-generation output and load as probability-weighted typical time-series scenarios inside the planning objective couples one-time topology/DG investment to operational variability, which is what makes the cost-optimal topology depend on the operating scenario rather than being fixed.
- **Conditions**: 12 typical time-series scenarios each spanning 48 daily time slots, with scenario probabilities; objective sums cost, loss and stability over all scenarios; demonstrated on the studied radial cases only.
- **Sources**: []
- **Status**: supported
- **Falsification criteria**: If an optimum computed on a single time-averaged scenario matched the multi-scenario optimum across penetration levels, the scenario embedding would add nothing and the claim would be false.
- **Proof**: [E01, E02]
- **Evidence basis**: Objective Eqs. 2, 5, 6 (sums over scenarios j, s and time t); procedure loops t<48 and n<12 (§4.2 steps 5-6); Figure 6 flowchart; Table 2 input categories.
- **Tags**: time-series, multi-scenario, formulation

## C07: Reliability tier, not electrical load alone, sets the redundancy of the DC supply architecture
- **Statement**: A data center's reliability tier maps monotonically onto the redundancy of its flexible-DC supply architecture — fault-tolerant tiers require dual independent DC buses with mutually hot-standby paths that share load equally and can each carry the whole load, redundant tiers a single path with parallel-redundant equipment, and basic tiers a single non-redundant path — so the topology's redundancy is dictated by the required availability rather than by the electrical load.
- **Conditions**: 750V DC bus design fed from 10kV DC mains with diesel backup; qualitative architecture-to-tier mapping (GB50174 A/B/C ↔ Uptime I-IV); no quantitative availability figure computed.
- **Sources**: []
- **Status**: supported
- **Falsification criteria**: A fault-tolerant (Tier IV/A) design shown to meet its availability target with a single non-redundant DC path would refute the tier→redundancy mapping.
- **Proof**: [E07]
- **Evidence basis**: Table 1 tier correspondence; Figures 1-5 (dual-bus fault-tolerant → single-path redundant → single-path basic architectures).
- **Tags**: reliability-tier, architecture, redundancy

## C08: Converting a branch to DC removes it from the AC voltage-stability drop mechanism
- **Statement**: Converting a branch to DC operation removes its AC-type voltage-stability constraint (its stability index becomes zero) and lowers the network's average branch stability index, so hybridization improves voltage stability chiefly by shrinking the set of AC branches exposed to the voltage-drop mechanism rather than by re-tuning AC branches.
- **Conditions**: voltage-stability index defined by Eq. 6 for AC branches only; DC branches assigned index 0 by construction; holds under the paper's index definition and the studied IEEE33 case.
- **Status**: supported
- **Falsification criteria**: If DC-converted branches exhibited nonzero AC-style voltage-drop instability under the same operating flows, or the hybrid network's average index exceeded the pure-AC index, it would refute the claim.
- **Proof**: [E05]
- **Evidence basis**: Figure 11 (consider-DC index at or below exclude-DC on nearly every branch; converted/new DC branches at 0); Table 8 average index 0.062 vs 0.091.
- **Sources**: [0.062 ← evidence/tables/table8.md «| Annual average voltage stability index | 0.062 | 0.091 |» [result]]
- **Dependencies**: C04
- **Tags**: voltage-stability, DC-branch

## C09: Feeder pairs with unbalanced load rates are the practical DC-interconnection candidates
- **Statement**: In a real regional network, feeder/link line pairs whose maximum annual load rates are markedly unbalanced (poor mutual transfer reliability) are the practical candidates for DC interconnection, because DC soft-connection equalizes transfer capability across the pair without requiring AC phase, frequency, or amplitude matching.
- **Conditions**: single regional case study (4 substations, 9 lines); qualitative engineering evaluation with no post-retrofit metric; lines already using soft-straightening (707, 717) cited as an operating precedent.
- **Sources**: []
- **Status**: hypothesis
- **Falsification criteria**: A regional deployment in which balanced-load-rate feeders gained more from DC interconnection than unbalanced ones would weaken the candidacy rule.
- **Proof**: [E06]
- **Evidence basis**: Table 9 (feeder vs link maximum annual load rates differ substantially on the flagged lines; soft-straightening precedent noted).
- **Tags**: practical-engineering, DC-interconnection, transfer-reliability
