# Concepts

## NCUCER (Network-Constrained UC and Economic Redispatch)
- **Notation**: MILP formulation of the ASM optimization problem
- **Definition**: A mixed-integer linear programming problem that minimizes redispatching costs while simultaneously handling unit commitment constraints (MUT/MDT), secondary reserve procurement, network flow limits (via PTDF sensitivity factors), and RES/load forecast updates. The core contribution of the proposed ASM model.
- **Boundary conditions**: Solved daily over a 24 h horizon; uses DC load flow with distributed slack bus; assumes pay-as-bid settlement for ASM.
- **Related concepts**: DAM, Redispatch, PTDF, SCUC.

## Day-Ahead Market (DAM) model
- **Notation**: LP merit-order zonal market (Eqs. 2–9)
- **Definition**: A linear programming optimization that minimizes step-wise generator bid costs subject to zonal power flow limits, zonal active power balance, unit maximum bid steps, and generator maximum power. Does NOT include UC constraints. Uses a zonal (not nodal) network representation.
- **Boundary conditions**: Solved as an LP for each time step of the day; considers monthly escalators for thermal unit max power; DH units bid at 0 $/MWh with a strategic power reservation for ASM.
- **Related concepts**: Zonal market, Merit order, Market Clearing Price (MCP).

## Bid Adjustment Mechanism
- **Notation**: Time-varying factors applied to DAM bid prices for each ASM service
- **Definition**: A TSO-side process that translates DAM schedules into ASM-compatible bids for each dispatchable unit. Defines five operational cases (Figure 3) based on the unit's DAM schedule relative to its technical minimum, determining which services (SU, SD, UR, DR, USR, DSR) each unit can offer and in what order.
- **Boundary conditions**: DT units provide SU, SD, UR, DR, USR, DSR; DH units provide only UR and DR. Bid prices are DAM bid prices multiplied by time-varying factors derived from historical Italian market data.
- **Related concepts**: SU, SD, UR, DR, USR, DSR, Technical minimum.

## Power Transfer Distribution Factor (PTDF)
- **Notation**: S_{n,b}
- **Definition**: A sensitivity factor quantifying how an incremental change in nodal active power at node n affects the power flow on branch b. Used in the ASM to model redispatch impacts on branch flows without full AC power flow.
- **Boundary conditions**: Computed using distributed slack bus DCLF (all generation nodes considered as slack) for generality. Updated based on DAM schedules.
- **Related concepts**: DCLF, Redispatch, Slack bus.

## Secondary Reserve Requirement (SRR)
- **Notation**: SRR_t (MW)
- **Definition**: The amount of secondary reserve (upward and downward) that must be procured in each hour. Determined per [44] based on load demand, ranging from 94.4 MW to 302.5 MW in the case study.
- **Boundary conditions**: Must be met exactly as an equality constraint (44). Divided equally between upward and downward SR.
- **Related concepts**: USM, DSM, SRH, Secondary reserve.

## Upward/Downward Secondary Reserve Margin (USM/DSM)
- **Notation**: USM_t, DSM_t
- **Definition**: The total upward (resp. downward) margin available from cleared DT units after DAM, limited by the Secondary Reserve Half-bandwidth (SRH = 6% of P^max). USM insufficiency (741 hours/year) drives SU or DR clearance in ASM.
- **Boundary conditions**: USM < SRR triggers necessary SU or DR clearance. DSM is always sufficient year-round.
- **Related concepts**: SRR, SRH, SU, DR.

## Minimum Up/Down Time (MUT/MDT)
- **Notation**: MU_i, MD_i
- **Definition**: The minimum number of consecutive hours a DT unit must remain online (MUT) or offline (MDT) after a state change. Enforced via constraints (27)–(28) and inter-day continuity via Algorithms 1 and 2.
- **Boundary conditions**: Technology-dependent: CC NG MUT=2–6h, MDT=2–8h; ST NG MUT=8h, MDT=12h; CT NG MUT=1–8h, MDT=1–8h.
- **Related concepts**: DT unit, Unit commitment, Inter-temporal constraints.

## Dispatchable Hydro (DH) Unit
- **Notation**: i ∈ Ω_H
- **Definition**: Hydroelectric units with a storage basin that can be dispatched flexibly. They bid a portion (90% base case) of daily inlet energy to DAM at 0 $/MWh and hold the remainder for ASM. Can provide UR and DR services but not SU/SD.
- **Boundary conditions**: Subject to energy balance constraints (35), power limits (36), and basin energy limits (37)-(38).
- **Related concepts**: Reservoir, UR, DR, DAM bidding strategy.

## Net Forecast Error (NFE)
- **Notation**: NFE_t (MW)
- **Definition**: The difference between total load forecast error and total RES (PV + WF) forecast error between DAM and ASM timeframes. Ranges from −3667.76 MW to +3312.48 MW in the case study.
- **Boundary conditions**: Used to define the total imbalance that ASM redispatch must correct, in addition to network overload mitigation and SR procurement.
- **Related concepts**: Forecast error, Redispatch, Load shedding, RES curtailment.

## DCLF (DC Load Flow) with Distributed Slack Bus
- **Notation**: FD_{b,t}, ∆F_{b,t}
- **Definition**: A linearized power flow model used to compute branch flows from DAM schedules and redispatch actions. Uses a distributed slack bus formulation (all generation nodes as slack) for PTDF calculation, avoiding the single-reference-bus dependency.
- **Boundary conditions**: Applied after DAM for feasibility analysis and within ASM constraints (42)-(43) for redispatch impact evaluation.
- **Related concepts**: PTDF, Redispatch, Slack bus.
