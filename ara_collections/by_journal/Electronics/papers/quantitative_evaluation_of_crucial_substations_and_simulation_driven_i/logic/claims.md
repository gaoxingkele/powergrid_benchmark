# Claims

## C01: Served-load magnitude, not topological connectivity count, dominates a planned substation's systemic criticality
- **Statement**: When a substation's importance for multi-voltage grid development is decomposed into load-based and topology-based attributes, the aggregate served-load magnitude carries by far the largest decision weight, while the raw count of downstream low-voltage feeders it connects carries the least; spatial-extent measures fall in between. The physical criticality of a distribution node is therefore governed primarily by *how much load* it serves, not by *how many* lines emanate from it.
- **Conditions**: Holds for the five proposed indices under AHP pairwise weighting elicited for a rapidly-developing regional grid (220/110/10 kV). The ordinal dominance of the load-level attribute is asserted; the exact weight split is regime-specific to the elicited pairwise matrix and would shift under a different expert panel or a re-weighting method (entropy, coefficient-of-variation). Untested boundary: transfer to other regions/voltage classes or to data-driven weightings.
- **Sources**: [0.385 ← evidence/tables/table3.md / Table 3 «Weighting factor 0.385 0.043 0.120 0.226 0.226» [result]; 0.043 ← evidence/tables/table3.md / Table 3 «Weighting factor 0.385 0.043 0.120 0.226 0.226» [result]; 0.00726 ← §2.2 / p7 «the calculated consistency ratio (CR) for this weighting factor is 0.00726, which is significantly below the threshold value of 0.1» [result]]
- **Status**: supported
- **Falsification criteria**: Re-eliciting the pairwise comparison matrix from an independent planner panel (or deriving weights by an objective method) and finding that a connectivity-count attribute outranks the load-level attribute, or that the load-level attribute is not the single largest weight, would refute the dominance claim.
- **Proof**: [E01, E02]
- **Evidence basis**: Table 3 weights (load level 0.385 > spatial influence 0.226 = load density 0.226 > power supply coverage 0.120 > LV-grid influence / 10 kV line count 0.043); consistency ratio 0.00726 < 0.1 validates the pairwise judgments; §4.4/§5 discussion states load level is the primary factor and spatial influence / line-count a secondary one.
- **Tags**: AHP, criticality, weighting, indicator-ranking

## C02: A static composite importance score linearly predicts the simulation-derived incremental cost of delaying a substation
- **Statement**: A composite criticality score computed only from a substation's static load/topology attributes stands in a strong, positive, approximately linear (monotonic) relationship with the incremental multi-voltage construction investment that a dynamic grid-evolution simulation attributes to delaying that substation's commissioning. The cheap static screen thus recovers the ranking a costly what-if simulation would produce, so criticality can be pre-screened without simulating every candidate.
- **Conditions**: Demonstrated over six planned 110 kV substations in one regional grid, each deferred individually by one planning horizon (2020→2025), with cost accumulated to 2035 and discounted at 8%. The relationship is a fitted trend across six points, not a mechanistically exact law; monotonicity can be locally violated (the highest-cost substation is not the highest-scored one — see Evidence basis). Untested boundary: larger substation sets, simultaneous multi-substation delays, other regions.
- **Sources**: [8% ← §4.3 (p16) «the annual investments for each delayed commissioning scenario are discounted to the initial planning year using a discount rate of 8%» [input]]
- **Status**: supported
- **Falsification criteria**: Running the individual-deferral simulation over a larger or different substation population and finding no significant positive association (or a negative/flat regression) between importance score and incremental cost would refute the claim.
- **Proof**: [E05]
- **Evidence basis**: Table 7 pairs each substation's score with its incremental cost (e.g., score 0.2035→3.95%, 0.1905→4.24%, 0.1367→1.63%); Figure 7 shows the scatter and a positively-sloped fitted line; §4.4 reports "a significant linear relationship." Note the ordering is not perfectly monotonic (substation 5, score 0.1905, has the highest incremental cost 4.24%, above substation 1's 3.95% at score 0.2035) — the relationship is a strong trend, not a strict order.
- **Dependencies**: C01
- **Tags**: score-validation, regression, cross-method-concordance, incremental-cost

## C03: Cost-scaling with criticality makes "defer the least-critical substation" the loss-minimizing sequencing rule
- **Statement**: Because delay-induced incremental cost increases with a substation's criticality, when some commissioning delay is unavoidable under land/investment constraints, sequencing that postpones the lowest-criticality substations first bounds the total economic loss, while critical substations should be protected on schedule. The reusable principle: under a positive cost-criticality gradient, the optimal deferral target is the least-critical unit.
- **Conditions**: Follows from the positive score–cost relationship (C02) within the same regional-grid regime and one-horizon deferrals; assumes delays are mutually substitutable choices among candidate substations. Untested boundary: cases where operational feasibility (not cost) forces a specific substation's delay, or where interaction effects between simultaneous delays dominate.
- **Sources**: []
- **Status**: supported
- **Falsification criteria**: Finding a regime where deferring a lower-scored substation produces a *larger* total incremental cost than deferring a higher-scored one (a reversal of the cost gradient) would refute the sequencing rule.
- **Proof**: [E04, E05]
- **Evidence basis**: §4.3 paired comparison (delaying low-importance No. 6 costs 1.63% vs high-importance No. 1 at 3.95%); §4.4/§5 recommend prioritizing deferral of lower-importance substations; Conclusion (2)(3).
- **Dependencies**: C02
- **Tags**: decision-rule, construction-sequencing, prioritization

## C04: Commissioning-delay cost concentrates in and persists within the low-voltage layer across the whole horizon
- **Statement**: Delaying a substation shifts its load onto distant substations through additional low-voltage (10 kV) feeders; the induced over-investment is concentrated in the 10 kV layer and does not dissipate once the delayed unit is later commissioned — it persists across subsequent planning horizons. Counter-intuitively, a high-criticality delay can *reduce* near-term upper-voltage (110 kV) investment while still raising total multi-voltage cost, because the excess sits in the distribution layer.
- **Conditions**: Observed for one-horizon deferrals of a high-density-area substation (No. 1) in the case grid, with cost tracked to 2035. The persistence and layer-concentration are asserted for delays into high-load-density service areas; a delay into a sparse area produces the same pattern at smaller magnitude. Untested boundary: grids where spare 110 kV capacity is unavailable so cost surfaces at the upper layer.
- **Sources**: []
- **Status**: supported
- **Falsification criteria**: A delay scenario in which the incremental cost surfaces predominantly in the 220/110 kV layers (not the 10 kV layer), or fully reverts after the delayed substation is commissioned, would refute the concentration/persistence mechanism.
- **Proof**: [E03, E04]
- **Evidence basis**: Table 6 per-layer cost breakdown (No. 1 delay: 10 kV line cost rises 722.089→774.9868 in 2020 and stays elevated through 2035; 110 kV substation investment in 2025 not increased) ; §4.3 narrative: "the total investment across the multi-voltage level grid is highest due to excessive investment in the 10 kV grid" and the impact "persists through 2035."
- **Dependencies**: C02
- **Tags**: cascade, temporal-persistence, layer-concentration, 10kV

## C05: Local load density is the operative physical driver of the transfer/feeder cost incurred by a delay
- **Statement**: The incremental cost a delay causes is governed by the local load density of the affected service area: in a dense area, existing feeders already run near capacity, so serving the displaced load requires building many additional feeders over short but numerous paths; in a sparse area, fewer/shorter transfers suffice. Load concentration — not merely total served load — is what converts a delay into feeder construction cost.
- **Conditions**: Demonstrated by contrasting a high-density substation (No. 1) against a low-density one (No. 6) in the case grid, one-horizon deferral. The mechanism links the load-density index to realized 10 kV cost; magnitude depends on the pre-delay feeder utilization. Untested boundary: areas with ample idle feeder headroom, where density would matter less.
- **Sources**: []
- **Status**: supported
- **Falsification criteria**: Observing that a delay in a low-load-density area produces equal or greater incremental 10 kV feeder cost than an otherwise-comparable delay in a high-density area would refute the density-driver mechanism.
- **Proof**: [E03]
- **Evidence basis**: §4.3: No. 1 is in a high-load-density region where "most existing 10 kV feeders already operate at relatively high-capacity factors; therefore, additional 10 kV feeders are required"; No. 6 "generates a smaller incremental demand for the 10 kV feeders due to its low load density and limited power supply coverage area." Table 4 load-density values (No. 1 = 2.80 vs No. 6 = 1.83, km).
- **Dependencies**: C04
- **Tags**: load-density, feeder-transfer, physical-mechanism
