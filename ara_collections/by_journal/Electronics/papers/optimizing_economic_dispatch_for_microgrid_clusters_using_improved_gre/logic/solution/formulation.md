# Economic Dispatch Problem Formulation (MGC)

Decision horizon: one day, 24 hourly intervals (t = 1..24). System: 3 microgrids (MG1, MG2, MG3),
each with WT, PV, one dispatchable non-renewable unit (MT for MG2; DG for MG1, MG3), an ESS, and AC
load, coordinated by an EMC that trades with the main grid. All equations are transcribed from §2 of
the paper (Eqs. 1-15).

## Objective (minimize)

Eq. (8):
```
F_MGC = C_Operation + C_Pollution + C_ESS + F_Main-MGC + F_ESS
```
- `C_Operation` — operational cost; `C_Pollution` — pollution control cost; `C_ESS` — ESS loss cost.
- `F_Main-MGC`, `F_ESS` — penalty terms (power-exchange excursion; ESS start/end energy discrepancy).

### Operational cost — Eq. (9), (10)
```
F_Operation = C_grid1 + C_grid2 + C_grid3 + C_ex1-2 + C_ex2-3 + C_ex3-1
              + Σ_{i=1..3} C_WTi + Σ_{i=1..3} C_PVi + Σ_{i=1..3} C_non-renew-i
C_gridi = C_buyi − C_selli      (i = 1, 2, 3)
```
Net main-grid trade per MG + inter-MG trade + WT/PV maintenance + non-renewable generation cost.

### Pollution control cost — Eq. (11)
```
F_Pollution = ∫_0^24 Σ_{i=1..M} ( c_DG·λ_i·P_DG(t) + c_MT·λ_i·P_MT(t) ) dt
```
`c_DG`, `c_MT` = unit pollution-control costs for DG/MT; `λ_i` = pollutant emission coefficient.
Only MT and DG emit (WT/PV emission-free; ESS pollutants neglected).

### ESS loss cost — Eq. (12)
```
F_ESS(loss) = m_ESS · Σ_{i=1..3} ∫_0^24 |P_SCi(t)| · f(SOC_SCi(t)) dt
m_ESS = C_Investment / Q_ESS
```
`m_ESS` = unit loss coefficient = investment cost / lifecycle throughput; `f(SOC)` = SOC-dependent loss function; supercapacitor-based model.

### Penalty 1 — main-grid/MGC exchange excursion — Eq. (13), (14)
```
F_Main-MGi = δ · Σ_{t=1..24} ( P_MG,i(t) − P_MI,i(t) )     (i = 1, 2, 3)
F_Main-MGC = Σ_{i=1..3} F_Main-MGi
```
`δ` = penalty coefficient; `P_MG,i`, `P_MI,i` = equivalent generation / equivalent load power between MGi and the distribution network.

### Penalty 2 — ESS start/end energy discrepancy — Eq. (15)
```
F_ESS = γ · | Σ_{t, P_dis(t)>0} P_dis(t)·η_dis + Σ_{t, P_ch(t)>0} P_ch(t)/η_ch |
```
`γ` = battery constraint penalty factor; `η_dis`, `η_ch` = discharge/charge efficiencies.

## Constraints (see also constraints.md)
- Power balance — Eq. (1): `Σ_{i=1..N} P_gen,i(t) + P_import(t) = P_load(t)`
- Per-MG load composition — Eq. (2): `P_loadi(t) = P_WTi + P_PVi + P_MTi + P_ESSi + P_buyi − P_selli + P_exi-j + P_exi-j` (symbols in Table 1)
- MT/DG output & ramp limits — Eqs. (3), (4)
- ESS charge/discharge power, capacity, SOC — Eqs. (5), (6), (7); SOC ∈ [30%, 90%] in this study

## Notes / unspecified quantities
- Numerical values of penalty coefficients δ and γ, emission coefficients λ_i, unit pollution costs
  c_DG/c_MT, m_ESS, ramp limits r_MT/r_DG, and generator/ESS capacity bounds are **not specified in
  the paper** (only the SOC window [30%, 90%] is given).
- The fitness value minimized by the optimizer includes the penalty terms and therefore differs
  numerically from the "actual daily cost" reported in Table A1 (which excludes penalties). See C01.
