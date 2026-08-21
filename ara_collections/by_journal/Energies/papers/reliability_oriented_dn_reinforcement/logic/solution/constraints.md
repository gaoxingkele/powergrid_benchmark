# Constraints

## Reliability Constraints
- **SAIDI Constraint** (Equation 12): SAIDI_i,t <= SAIDI_targeted_i. The System Average Interruption Duration Index at each bus i in each stage t must not exceed the regulatory threshold (2.5 h/year).
- **ENS Constraint** (Equation 13): ENS_i,t <= ENS_targeted_i. The Energy Not Supplied at each bus i in each stage t must not exceed the regulatory threshold (5 MWh/year per bus).

## Operational Constraints (Restoration -- Success Mode 1)
- **Restoration Path Existence**: At least one restoration path must reconnect the isolated island to the main source.
- **Feeder Thermal Limit** (Equation 14): I_f <= I_M_f. The current on receiving feeder f must not exceed its maximum thermal limit.
- **Substation Capacity** (Equation 15): S_sub <= S_Max_sub. The substation receiving transferred loads must not be overloaded.
- **Voltage Limits** (Equation 16): V_Min_i <= V_i <= V_Max_i. Bus voltages along the restoration path must remain within permissible limits.
- **Power Balance** (Equations 17-18): Active and reactive power balance must be maintained: sum(P_Gi) + sum(P_DGi) - sum(P_Di) - sum(P_loss_f) = 0 and similarly for reactive power.

## Operational Constraints (Islanding -- Success Mode 2)
- **DG Adequacy** (Equation 19): P_DGI >= P_DI + P_LossI. Total DG power inside the island must meet or exceed total load plus losses within the island.
- **Island Loss Assumption**: System losses during islanded operation are assumed to be 5% of the islanded load.

## System Topology Constraints
- **Radial Configuration**: The distribution system operates in a radial configuration; protection devices isolate faulty sections for contingency management.
- **N-1 Principle**: Only single-component failures (substations and lines) are considered; the system must be capable of supplying demand under any single component outage.
- **Customer-Owned DG**: The utility does not control DG size or location but manages reliability through strategic placement and operation of tie lines and sectionalizing switches.

## Objective Function Structure
- **Total Cost Minimization** (Equation 7): Minimize Z = sum over t of [CENS(t) + CLT(t) + CNOS(t) + CUPG(t)] / (1+tau)^((t-1)K) + Pf * sum(mu_c).
  - CENS(t): Cost of energy not supplied at stage t (Equation 8)
  - CLT(t): Cost of tie line investments at stage t (Equation 9)
  - CNOS(t): Cost of NO switch investments at stage t (Equation 10)
  - CUPG(t): Cost of feeder and substation upgrades at stage t (Equation 11)
  - Pf: Penalty factor for reliability constraint violations (mu_c = 1 if violated, 0 otherwise)

## Time/Cost Parameters
- Planning horizon: 15 years (3 stages of 5 years each)
- Annual load growth rate: 3%
- Interest rate: 10%
- Interruption cost penalty: $2,000/MWh
- NO switch installation cost: $4,700
- Tie line construction cost: $2x10^6 per km
- Substation upgrade: 13.3 MVA unit at $8x10^6, 16.7 MVA unit at $10x10^6
- Feeder upgrade options: 250 A at $3.5x10^5/km, 450 A at $4.6x10^5/km, 900 A at $9.2x10^5/km
