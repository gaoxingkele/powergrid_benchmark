# Constraints (Boundary Conditions, Assumptions, and Limitations)

## Modeling Assumptions
- A1: Day-ahead horizon T = 24 h at hourly resolution.
- A2: DistFlow model for radial distribution network (linearized branch flow).
- A3: Weymouth gas flow equation piecewise-linearly approximated (12 segments/pipeline, <1% deviation).
- A4: Deterministic wind forecast (single day-ahead profile).
- A5: EV fleet modeled as homogeneous (battery capacity, power, efficiency).
- A6: P2G intake primarily coupled to curtailed wind (surplus only).
- A7: TOU price bands (peak/flat/valley) are predefined.
- A8: Quadratic generator cost curves used for CHP and gas-fired units.
- A9: The IESO has unified dispatch authority across all carriers.

## Technical Limitations
- L1: Reactive power and voltage constraints are simplified via DistFlow; full AC OPF is not used.
- L2: Wind uncertainty is modeled deterministically (no scenarios, chance constraints, or robust sets).
- L3: EV fleet homogeneity assumption provides optimistic estimate of dispatchable flexibility.
- L4: P2G coupling to curtailed wind only is a design choice; relaxing it would change economics.
- L5: The 12-segment Weymouth PWL approximation has <1% deviation but is not exact.
- L6: The model does not include intra-hour dynamics or real-time corrections.
- L7: Communication latency, metering accuracy, and real EV fleet diversity are not addressed.
- L8: The test system is small (33-bus, 20-node gas); scalability to multi-area systems would require decomposition.

## Boundary Conditions
- BC1: Only one EESS unit (Node 17) and one EV fleet (Node 11, 1000 vehicles).
- BC2: Wind farms at Nodes 15 and 29; P2G at Nodes 16 and 31.
- BC3: Gas turbines at Nodes 25 and 33; conventional thermal at Nodes 18 and 22.
- BC4: SOC bounds for EESS: [5%, 95%]; for EV: [10%, 90%].
- BC5: The LCOE discount rate is fixed at 8%.
