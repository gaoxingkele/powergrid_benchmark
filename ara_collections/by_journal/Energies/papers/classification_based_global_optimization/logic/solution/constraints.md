# Constraints

## Boundary Conditions
- **Network topology**: Radial distribution networks only. The method relies on branch decomposition from a radial tree structure.
- **Network scale**: Validated on IEEE 33-bus (32 branches) and IEEE 69-bus (68 branches) systems at 12.66 kV, 10 MVA base. Scalability to larger networks is claimed but not demonstrated.
- **Component count**: Fixed at 2 EVCSs, 2 DGs, and 2 CBs. The impact of different component counts is not studied.
- **EV penetration levels**: 30%, 40%, and 50% hosting factors. Lower penetration levels (<30%) or extreme levels (>50%) are not analyzed.
- **DG operation**: DGs operate at unity power factor. Reactive power support from inverter-based DGs is not utilized.

## Operational Constraints (from paper)

### Power Balance
- Active power: PS,b = sum(Pld,i) + PLoss - sum(PDG,i) for i=2..N
- Reactive power: QS,b = sum(Qld,i) + QLoss - sum(QCB,j) for i=2..N, j=1..mc
- Slack bus must supply the net demand after accounting for DG injection and CB compensation.

### DG Constraints
- Each DG output must be within min/max limits: PDG,min < PDG,i < PDG,max
- Total DG capacity must not exceed 90% of total active load: sum(PDG,i) < 0.9 x sum(Pld,i)

### CB Constraints
- Total CB reactive power must not exceed 90% of total reactive load: sum(QCB,j) < 0.9 x sum(Qld,i)

### Voltage Constraints
- All bus voltages must be within 0.95 p.u. <= Vi <= 1.05 p.u.
- VDI = sum((1 - Vi)^2) for i=1..N (minimized in objective)

### Thermal Capacity Limits
- Apparent power flow in each branch must not exceed its maximum allowable limit: |Sij| <= Sij,max

## Assumptions
- A1: Radial network topology with unidirectional power flow in the base case.
- A2: Two units of each component type (EVCS, DG, CB) are sufficient for optimal performance in the tested networks. Additional units would increase capital cost but may further improve performance.
- A3: DGs (solar PV) operate at unity power factor. Inverter capability for reactive power is not utilized, though acknowledged as a potential improvement.
- A4: EV charging load split between two stations is determined by the optimization; initial iteration assumes equal split.
- A5: Steady-state peak loading scenario is used. Annual energy loss is estimated by multiplying peak losses by 8760 hours/year.
- A6: Constant load power at each interval. No time-varying load profiles, daily load curves, or seasonal variations.
- A7: EV load is deterministic; stochastic EV charging behavior is not modeled.
- A8: DG generation is assumed constant; stochastic renewable generation profiles are not considered.
- A9: Bus classification based on known load values is assumed accurate; risk of misclassification is considered negligible.

## Known Limitations
- L1: Single operating condition (peak load) may not represent annual performance under variable loading and generation patterns.
- L2: Unity power factor operation of DGs misses potential benefits of smart inverter reactive support.
- L3: Fixed component count (2 each) may not be optimal for all network sizes or configurations.
- L4: Deterministic EV load model does not capture the stochastic nature of real EV charging behavior.
- L5: Capital cost calculation excludes operation and maintenance costs, time-of-use pricing, and PV degradation.
- L6: No consideration of unbalanced network operation or three-phase system asymmetries.
- L7: Energy storage integration is not addressed.
- L8: Payback period calculation uses simplified annual energy loss estimation (peak losses x 8760 h), which may overestimate actual savings under variable loading.
- L9: The approach is not validated on real-world feeder data; only IEEE benchmark networks are used.
