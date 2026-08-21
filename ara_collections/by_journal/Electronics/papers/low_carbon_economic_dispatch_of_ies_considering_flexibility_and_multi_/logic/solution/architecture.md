# Architecture — Bi-level IES Dispatch System

Mirrors Figure 1 (bi-level model) and Figure 2 (IES physical structure).

## A. Optimization architecture (Figure 1)

### Upper layer — IES operator (leader)
- **Purpose**: Maximize operator revenue (F1, Eq. 7) AND system flexibility (F2, Eq. 11).
- **Inputs**: Purchased quantities and EV charge/discharge + SoC fed up from the lower layer.
- **Outputs (decision vars)**: Outputs of the various devices; energy prices (electricity/heat/cooling, EV price) sent down.
- **Solver**: Improved PSO (multi-objective) → Pareto front → TOPSIS compromise.
- **Key design choice**: Two objectives kept explicit (not scalarized to a single cost) so an economy–flexibility Pareto front exists.

### Lower layer — followers
- **User aggregator**: minimize total cost F^L (Eq. 21). Decision var: power purchased by users (demand response: shift/curtail/substitute).
- **EV clusters**: maximize self-utility F_EV (Eq. 19). Decision var: EV charge/discharge power.
- **Solver**: CPLEX 12.10.

### Coupling
- Down (upper→lower): energy prices.
- Up (lower→upper): purchased quantities + EV state.
- Iterated to global optimum (Figure 3 loop).

## B. Physical architecture (Figure 2)

- **Sources**: Wind Turbine, Photovoltaic, Power Grid.
- **Conversion/storage**: Gas Turbine (electricity+heat CHP), Electric Boiler (elec→heat), Absorption Chiller (heat→cooling), Electric Chiller (elec→cooling), Storage Battery, Heat Storage Tank, Electric Vehicles (bidirectional).
- **Loads**: Electric, Thermal, Cooling.
- **Buses / couplings**:
  - Electric bus balances WT+PV+grid+GT+BT.dis+EV.dis against elec load + EC + EH + BT.chr + EV.chr (Eq. 12).
  - Thermal bus balances GT+EB+HST.dis against heat load + AC + HST.chr (Eq. 13).
  - Cooling bus balances AC+EC against cooling load (Eq. 14).
- **Multi-energy coupling nodes**: Gas Turbine (elec↔heat), Electric Boiler (elec→heat), Electric/Absorption Chillers (→cooling) — these couplings are what make cross-carrier flexibility and energy substitution possible.

## C. Data-flow summary
Forecast data (Figure 4) + device params (Table 1) + EV params (Table 4) + prices (Tables 2,3) → bi-level solve (Figure 3) → per-carrier optimized power schedules (Figures 5–7), DR + prices (Figures 9–12), EV schedules (Figures 13–14), flexibility profiles (Figures 8,15), and scenario/algorithm results (Tables 5–7, Figure 16).
