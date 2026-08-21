# Problem Specification

## Observations

### O1: Data-center equipment is predominantly DC-driven load
- **Statement**: Most servers, network, and other equipment in data centers are DC-driven loads; accessing DC supply via voltage-source-converter (VSC) distribution improves energy efficiency and reduces carbon emissions.
- **Evidence**: Introduction (§1), refs [4,5]
- **Implication**: A DC or hybrid AC/DC distribution form is a natural fit for data-center power supply.

### O2: DC distribution offers footprint, loss, and reliability advantages
- **Statement**: A DC electrical-equipment room is about one-third the footprint of an AC one (≈50% footprint reduction, ≈40% equipment/engineering saving); DC line loss is much lower with a loss saving of about 5-8%; medium-voltage DC convergence is more economical when the convergence radius exceeds 5 km and capacity is at least 10 MW.
- **Evidence**: §2.1 (technical/economic impact)
- **Implication**: DC introduction can lower both capital footprint and operating loss, but the equipment (converters, DC breakers) carries higher one-time cost.

### O3: Existing DC-distribution topology work does not address data-center network design
- **Statement**: Prior literature enumerates chain / ring / double-ended DC topologies and studies reconfiguration, robust voltage control, protection, and superconducting LVDC, but multi-level network-topology design specifically for data-center AC/DC access is still under exploration.
- **Evidence**: §1 refs [7-18], §3 opening
- **Implication**: A physical-level, tier-aware topology-design method for data centers is missing.

### O4: DG and rising DC-load density increase planning uncertainty
- **Statement**: Infiltration of distributed generation and growing data-center DC-load density change node structure and operating mode, raising planning/operation uncertainty across time-series scenarios.
- **Evidence**: §1 (traditional planning discussion)
- **Implication**: Planning must account for multiple time-series operating scenarios, not a single load forecast.

## Gaps

### G1: No multi-level physical topology design for data-center AC/DC access
- **Statement**: There is no systematic, reliability-tier-aware physical-level topology design for hybrid AC/DC distribution in data centers.
- **Caused by**: O1, O3
- **Existing attempts**: Generic DC topologies (chain/ring/double-ended) and reconfiguration/robust-control schemes.
- **Why they fail**: They are not tied to data-center tiers (A/B/C ↔ Uptime I-IV), DC-load dominance, and hot-standby requirements.

### G2: No time-series multi-scenario planning method coupling DG and DC-load penetration
- **Statement**: Planning methods that jointly decide DC line retrofit, DG siting/sizing, and converter placement under time-series multi-scenario DG/load variation are lacking.
- **Caused by**: O2, O4
- **Existing attempts**: Traditional single-forecast planning; two-stage EMS/robust control.
- **Why they fail**: They do not couple investment decisions to scenario-dependent operation, so they cannot track how the cost-optimal topology shifts as DC-load penetration grows.

## Key Insight
- **Insight**: Because converter cost scales with throughput capacity, DC retrofit is only cost-effective once the DC-load / new-energy share is high enough that eliminated conversion links outweigh converter capex; embedding time-series multi-scenario operation in the objective lets the optimizer place DC exactly where (feeder ends, high-DC-density nodes) and when (penetration stage) it pays off.
- **Derived from**: O1, O2, O4
- **Enables**: A staged, penetration-driven DC-retrofit plan (multi-level topology design + bi-level time-series multi-scenario optimization).

## Assumptions
- A1: DG output and load can be represented by a finite set of probability-weighted typical time-series scenarios (12 scenarios × 48 daily slots).
- A2: Converter cost is proportional to active capacity; DC branches carry no AC-type voltage-stability constraint (index set to 0).
- A3: The test networks (13-node, IEEE33) and their assigned per-node DC-load proportions are representative of data-center-penetrated distribution feeders.
- A4: Economic parameters (discount rate 7.5%, VSC $170/kVA, 15-year life, etc.) hold over the planning horizon.
