# Problem Specification

## Observations

### O1: IES faces high complexity from multi-energy coupling and renewable penetration
- **Statement**: The Integrated Energy System (IES) ties electricity, natural gas, heat, and cooling into one framework, but high renewable penetration creates supply–demand imbalances, and strong nonlinear carrier coupling poses significant challenges to secure and economic operation.
- **Evidence**: §1, pages 1–2; citations [1–4].
- **Implication**: A coordinated co-optimization scheduling framework is needed.

### O2: Demand-side flexibility (PDR, V2G) is underexploited in coupled power–gas IES
- **Statement**: Existing PDR and V2G studies stay almost entirely within the electrical subsystem and seldom ask how V2G flexibility travels into a coupled carrier (gas network). The demand side is underexplored in IES scheduling — in particular, how PDR and V2G act together to relax stress between power and gas networks.
- **Evidence**: §1, pages 2–3; citations [8–12,15–19].
- **Implication**: The synergistic interaction between PDR and V2G across power–gas systems must be studied.

### O3: Existing TOU pricing models lack market-stability constraints
- **Statement**: Most TOU-based PDR formulations bound the price vector but rarely include explicit constraints on the peak-to-valley ratio or enforce the ordering of peak/flat/valley tariffs, which are precisely the limits that protect social welfare and prevent clearing failures.
- **Evidence**: §1, page 2; citations [8–12].
- **Implication**: A PDR framework with built-in market-stability constraints (peak-to-valley ratio bound, tariff ordering) is needed.

### O4: Storage degradation is neglected in conventional dispatch models
- **Statement**: Conventional dispatch models consider only short-term operational expenditures while neglecting lifecycle degradation of capital-intensive assets such as electrochemical energy storage systems (EESS), leading to overly optimistic charging–discharging schedules.
- **Evidence**: §1, page 3; references [28,29].
- **Implication**: An LCOE-based degradation term is needed to discourage aggressive cycling.

### O5: The coupled IEEE 33-bus + 20-node gas test system provides a controlled evaluation
- **Statement**: The paper uses a modified IEEE 33-node distribution network (12.66 kV) coupled with a 20-node natural gas grid, with 2 wind farms, 5 generators, 1 EESS, 1 EV fleet (1000 vehicles), and P2G units.
- **Evidence**: §4.1, Figure 3; Tables A1–A6.
- **Implication**: The test system is small but sufficient to validate the proposed mechanisms.

## Gaps

### G1: No unified IES framework combines PDR, V2G, P2G, and LCOE degradation with market-stability constraints
- **Statement**: Existing studies treat PDR, V2G, P2G, and storage degradation in isolation or pairwise. No single security-constrained electricity–gas co-optimization embeds all four mechanisms with distribution-network power flow, gas Weymouth dynamics, and retail market-stability limits.
- **Caused by**: O2, O3, O4.
- **Existing attempts**: [8] TOU with elasticity; [15–19] V2G; [20–25] P2G–IES; [29] LCOE for EESS.
- **Why they fail**: They address each mechanism separately or in pairs; none combine all four.

### G2: DR mechanisms not evaluated for cross-carrier propagation effects
- **Statement**: The impact of electrical-side demand flexibility (PDR, V2G) on the coupled gas network (ramping stress, pressure stability) is not quantified in existing IES studies.
- **Caused by**: O2.
- **Existing attempts**: [15–19] evaluate V2G for power system only.
- **Why they fail**: They do not model gas network effects of electricity-side flexibility.

## Key Insight
- **Insight**: The four flexibility mechanisms — PDR with market-stability-constrained TOU, bidirectional V2G, P2G coupling, and LCOE storage degradation — can be assembled as a two-stage (pricing/dispatch) single-instance MILP that simultaneously enforces DistFlow power flow, Weymouth gas dynamics, and retail market limits, preserving global optimality while capturing the cross-carrier propagation of demand-side flexibility.
- **Derived from**: O2, O3, O4.
- **Enables**: A unified framework that quantifies marginal contributions of each mechanism via ablation.

## Assumptions
- A1: The day-ahead horizon (T = 24 h) at hourly resolution is used for all scheduling.
- A2: DistFlow model for radial distribution network (linearized).
- A3: Weymouth gas flow equation approximated by piecewise linearization (12 segments/pipeline).
- A4: Wind power forecast is deterministic (single day-ahead profile).
- A5: EV fleet is treated as homogeneous in battery capacity, charge/discharge power, and efficiency.
- A6: The P2G intake is coupled primarily to curtailed wind (economic rationale).
- A7: TOU price bands (peak/flat/valley) are predefined time intervals.
