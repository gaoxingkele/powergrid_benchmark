# Method: Two-Stage DAM-ASM Framework

## Overview

The proposed method models the sequential interaction between a zonal Day-Ahead Market (DAM) and a nodal Ancillary Service Market (ASM) in the European context. It consists of four stages solved sequentially for each day d.

## Stage 1: DAM Model (Section 2.1)

A merit-order zonal market optimization (LP) that clears generation at marginal cost, subject to:
- Generator step-wise bid costs
- Zonal active power balance
- Interzonal connection power flow limits
- Unit technical limits (max power, monthly escalators, availability)
- DH strategic bidding (power reservation for ASM)

Output: preliminary generation schedules P^D_{i,t} and zonal Market Clearing Prices.

## Stage 2: Bid Adjustment Mechanism (Section 2.2)

TSO-side adjustment of ASM bids based on DAM results:

1. **DT unit services**: SU, SD, UR, DR, USR, DSR
2. **DH unit services**: UR, DR only
3. **Five operational cases** (Figure 3):
   - (a) Unit not cleared in DAM → SU first, then UR, USR
   - (b) Unit cleared below P^min → mandatory SU or SD
   - (c) Unit at P^min → SD or upward services
   - (d) Unit between limits → UR or DR + SR bids
   - (e) Unit at P^max → DR first, then DSR
4. **Time-varying bid factors**: ASM price = DAM price × hourly factor (selling > 1, buying < 1)
5. **Gaussian variation**: 99.7% confidence interval at 10% of mean factor

## Stage 3: DCLF and Sensitivity Factors (Section 2.2)

- DC load flow from DAM schedules → identifies overloaded branches (FD_{b,t})
- PTDF computation with distributed slack bus (S_{n,b})
- Each PTDF captures how nodal power injection change affects branch flow

## Stage 4: ASM Optimization — NCUCER (Section 2.3)

A daily MILP that minimizes redispatching costs while enforcing:

1. **Unit commitment**: MUT/MDT (Eqs. 27–28), inter-day continuity (Algorithms 1–2)
2. **DT state constraints**: min/max power with SR margins, case-dependent bid ordering (Eqs. 30–34)
3. **DH constraints**: energy balance, power limits, basin limits (Eqs. 35–38)
4. **Network constraints**: nodal power balance (Eq. 41), branch flow bounds (Eq. 42), PTDF-based flow variation (Eq. 43)
5. **Secondary reserve**: exact SRR procurement (Eq. 44)
6. **Penalty terms**: RES curtailment and load shedding (Eqs. 15–16, 39–40)

### Algorithms

**Algorithm 1 — MUT/MDT Continuity**: Ensures inter-day unit state continuity from day d−1 to day d based on t^{on}_{i,d-1} and t^{off}_{i,d-1} parameters.

**Algorithm 2 — MUT & Availability Continuity**: Ensures consistency between MUT at the end of day d and unit availability at day d+1.
