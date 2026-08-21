# Constraints (Boundary Conditions, Assumptions, and Limitations)

## Modeling Assumptions
- A1: Load demand is inelastic with respect to price in DAM (no demand-side bidding).
- A2: DAM uses a zonal market structure; intra-zonal congestion is neglected.
- A3: ASM uses a nodal approach with DC load flow and PTDF sensitivity factors.
- A4: Distributed slack bus DCLF (all generation nodes as slack) for PTDF calculation.
- A5: DH units follow a fixed bidding strategy (90% DAM / 10% ASM base case).
- A6: ASM bid prices are derived from DAM bid prices via time-varying factors from Italian market data.
- A7: Secondary Reserve Requirement must be met exactly (equality constraint).
- A8: RES curtailment and load shedding are last-resort actions with high penalty costs.
- A9: DT unit SRH is 6% of P^max.
- A10: The optimization horizon is 24 h/d with inter-day MUT/MDT continuity enforced algorithmically.

## Technical Limitations
- L1: DC load flow approximation neglects reactive power and voltage constraints.
- L2: Zonal DAM model does not capture intra-zonal congestion; only interzonal limits are enforced.
- L3: Bid factors are derived from Italian market data and may not generalize to other markets.
- L4: The DH bidding strategy (fixed fraction) is a heuristic rather than an optimized decision.
- L5: The model does not yet include tertiary reserve services.
- L6: Stochastic/robust optimization for forecast uncertainty is not incorporated.
- L7: Energy storage systems and demand-side management are not included.
- L8: The computational burden (~2.5 min/day for ASM) may scale poorly with larger systems.

## Boundary Conditions
- BC1: Only dispatchable thermal (DT) and dispatchable hydro (DH) units participate in ASM.
- BC2: Non-dispatchable RES units are not redispatched; they follow forecast profiles.
- BC3: The model assumes perfect information within each day for RES/load updates.
- BC4: The MUT/MDT continuity between days assumes the previous day's optimal schedule is known.
- BC5: Yearly horizon uses a leap year (8784 h) for the NREL-118 dataset.
