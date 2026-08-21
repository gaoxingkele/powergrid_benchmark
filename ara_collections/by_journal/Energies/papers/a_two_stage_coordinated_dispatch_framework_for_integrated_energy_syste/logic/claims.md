# Claims

## C01: Coordinating PDR and V2G in a security-constrained power–gas co-optimization lowers total cost and flattens load curve beyond PDR alone
- **Statement**: In a coupled electricity–gas IES, price-based demand response (PDR) alone reduces total daily operating cost by approximately 3.2% and compresses the peak-to-valley load difference by approximately 15.0% relative to an uncoordinated baseline; adding bidirectional V2G deepens these gains to approximately 4.7% and 31.9%, respectively. The V2G layer contributes most of the additional peak-shaving while adding a smaller further cost saving.
- **Conditions**: Based on the IEEE 33-bus + 20-node gas test system with 1000 homogeneous EVs, under the three-case comparison (Case 1: baseline no PDR/no V2G; Case 2: PDR only; Case 3: PDR + V2G). System parameters in Appendix A.
- **Sources**: []
- **Status**: supported
- **Falsification criteria**: Show that on the same test system, either (a) PDR alone achieves a cost reduction above 4% (more than the reported PDR+V2G combined), or (b) adding V2G to PDR fails to reduce the peak-to-valley difference by at least 5 percentage points beyond PDR alone.
- **Proof**: [E01, E03]
- **Evidence basis**: §4.2, Table 3: Case 1 cost $4,873,632; Case 2 cost $4,718,301 (3.2%↓), peak-valley 203.5 MW (15.0%↓); Case 3 cost $4,644,496 (4.7%↓), peak-valley 163.1 MW (31.9%↓).
- **Tags**: PDR, V2G, cost reduction, peak shaving, load curve

## C02: P2G is the decisive enabler of renewable accommodation, eliminating curtailment
- **Statement**: In the co-optimized IES, the power-to-gas unit converts essentially all surplus wind energy into synthetic natural gas rather than spilling it. Removing P2G from the configuration raises wind curtailment from approximately 0% to approximately 14.5% of available wind, while total cost rises by only about 0.61%, because the additional gas must instead be procured from upstream supply.
- **Conditions**: Based on ablation study (Table 4). Wind curtailment is measured as the share of available day-ahead forecast wind that is neither injected nor converted. The P2G unit draws from curtailed wind only (Eq. 38).
- **Sources**: []
- **Status**: supported
- **Falsification criteria**: Show that with P2G active, a non-trivial fraction (>1%) of available wind is curtailed, or that the 14.5% curtailment figure without P2G can be reduced below 5% through alternative mechanisms within the same formulation.
- **Proof**: [E03]
- **Evidence basis**: §4.2.4, Table 4: Without P2G: ∆Total Cost +0.61%, ∆Wind Curtailment +14.5 pts.
- **Tags**: P2G, wind curtailment, renewable accommodation, ablation

## C03: Dispatch cost is governed primarily by wind availability, more than by any single flexibility mechanism
- **Statement**: Reducing wind resource availability by 30% increases total operating cost by approximately 9.17%, which is larger than the combined effect of all demand-side and storage flexibility mechanisms studied. Wind is the primary economic driver of the dispatch because it displaces costly thermal and gas-fired generation.
- **Conditions**: Based on ablation study (Table 4); wind penetration reduction simulated by scaling down the day-ahead wind forecast by 30%.
- **Sources**: []
- **Status**: supported
- **Falsification criteria**: Show that removing any other single mechanism (PDR, V2G, P2G, or LCOE) produces a cost impact larger than the 9.17% wind-reduction impact, or that the cost impact of 30% wind reduction can be fully offset by any combination of the other mechanisms.
- **Proof**: [E03]
- **Evidence basis**: §4.2.4, Table 4: Wind penetration −30%: ∆Total Cost +9.17%, ∆Wind Curtailment ≈0 pts.
- **Tags**: wind availability, cost sensitivity, renewable penetration, economic driver

## C04: LCOE storage-degradation term reprices cycling but does not alter dispatch
- **Statement**: Adding the LCOE-based EESS degradation cost term affects cost accounting (reduces reported cost by approximately 0.42% when removed) but does not change the dispatch itself, because the storage operates at its cycle-count limit in every configuration. The penalty term therefore affects the cost accounting rather than the operational schedule.
- **Conditions**: Based on ablation removing the LCOE term from Case 3. Storage cycle limit K^max_i constrains operation regardless of degradation cost.
- **Sources**: []
- **Status**: supported
- **Falsification criteria**: Show that removing the LCOE degradation term changes the storage dispatch profile (charging/discharging pattern or total daily throughput) by more than 5%, or that the cost impact exceeds 2% of total operating cost.
- **Proof**: [E03]
- **Evidence basis**: §4.2.4, Table 4: Without LCOE degradation: ∆Total Cost −0.42%, ∆Wind Curtailment ≈0 pts.
- **Tags**: LCOE, storage degradation, cycling cost, dispatch impact

## C05: Electrical-side demand flexibility propagates across carriers, relaxing gas network stress
- **Statement**: When PDR and V2G reduce electrical peak demand in the IES, the coupled gas network experiences reduced ramping stress: gas-fired units require less peaking fuel, gas sources (especially S4) operate at lower stress-free levels, and the gas production profile becomes more uniform. This confirms that demand-side flexibility in the power sector can be strategically leveraged to optimize the coupled gas network.
- **Conditions**: Based on the three-case comparison (Figures 8–10). Gas source S4 functions as the marginal peaking supplier. The effect is maximized in Case 3 (PDR + V2G).
- **Sources**: []
- **Status**: supported
- **Falsification criteria**: Show that the gas source production profiles are identical across all three cases (no cross-carrier propagation), or that the gas network stress increases when PDR and V2G are added.
- **Proof**: [E01]
- **Evidence basis**: §4.2.2, Figures 8–10. Gas sources operate at reduced stress in Cases 2 and 3 vs Case 1; the marginal source S4 is significantly lower in Case 3.
- **Tags**: cross-carrier propagation, gas network, flexibility, PDR, V2G

## C06: Adding V2G lifts the valley price and damps peak-price anomalies that demand-only pricing cannot resolve
- **Statement**: In the PDR-only scenario (Case 2), local levelized cost remains high and the peak price still spikes because no storage changes total energy drawn. When V2G is added (Case 3), V2G discharge adds local capacity through peaks to hold peak prices down, while coordinated overnight charging adds load that lifts the valley price above its PDR-only level. This flattens the price curve and spares generators some ramping wear.
- **Conditions**: Based on daily demand electricity price distribution comparison across three cases (Figure 12). The price curves show the operating cost rather than market-clearing prices.
- **Sources**: []
- **Status**: supported
- **Falsification criteria**: Show that the daily price distribution in Case 3 has a higher peak price than Case 2 (indicating V2G does not damp peak anomalies), or that the valley price in Case 3 is lower than Case 2.
- **Proof**: [E01]
- **Evidence basis**: §4.2.3, Figure 12: Case 1 shows flat baseline; Case 2 narrows peak-valley gap but peak still spikes; Case 3 smooths anomalies with V2G discharge and coordinated charging.
- **Tags**: V2G, valley price, peak price, market impact, price smoothing

## C07: The two-stage single-instance MILP stays computationally lightweight at this scale
- **Statement**: The complete model (mixed-integer SOCP over 24 h, ~15,000 decision variables, ~4,000 binary) converges to a relative optimality gap below 0.01% within seconds on a standard desktop workstation using CPLEX 12.7.1. Solution time grows mainly with the number of Weymouth segments and EV aggregation granularity.
- **Conditions**: Tested on the IEEE 33-bus + 20-node gas system; 12-segment piecewise-linear Weymouth approximation; homogeneous EV fleet aggregation. Larger multi-area systems would require decomposition.
- **Sources**: []
- **Status**: supported
- **Falsification criteria**: Show that the model requires more than 60 seconds to reach 0.01% gap on the same hardware and test system, or that the model fails to converge within 1% gap within 5 minutes.
- **Proof**: [E02]
- **Evidence basis**: §4.2.4: "each configuration converges to a relative optimality gap below 0.01% within a few seconds of wall-clock time."
- **Tags**: computational performance, MILP, optimality gap, scalability
