# Formulation — SEUC MIP Objective and Constraints

All equation numbers refer to the published paper. The model is a mixed-integer linear program (MILP) over a 24-hour horizon (T = 24 periods) for a TEBSA-like 5 × 2 CCGT plant (NC = 5 gas turbines, NS = 2 steam turbines).

## Nomenclature (from paper Nomenclature and §2)

**Indices:**
- t = 1…T (hours)
- i = 1…NC (gas turbines)
- j = 1…NS (steam turbines)

**Parameters (Table 1):**
- GCC = 800 MW (plant max capacity), GCC = 210 MW (plant min capacity)
- PAF = 15 MW (per-unit supplementary fire capacity)
- MUG = 2 (minimum gas units per steam turbine)
- STF = 0.613 (steam-to-gas factor, p.u.)
- KGC = 3 h (minimum gas operating hours for cold steam startup)
- KMH (governs hot-start window: steam turbine offline >9 h → cold start)
- t1 ≤ 16 h (hot → warm threshold), t2 16 < t ≤ 30 (warm → cold threshold), t3 > 30 h (cold)

**Unit parameters (Tables 3–4):**
- Gas turbines: G̅ = 100 MW, G̲ = 50 MW, TC = TD = 5 MW/min
- Steam turbines: S̅ = 170 MW, S̲ = 80 MW, GSTH = 80 MW (hot start output), GSTC = 30 MW (cold start output)

## 1. Objective function (Eq. 1, §2.1)

```
Min Σ_t [ Σ_i (c_i · u_{i,t} + s_0 · v_{i,t} + c_0 · w_{i,t}) + Σ_j (c_j · u_{j,t} + s_1 · v_{j,t} + c_1 · w_{j,t}) + DSC_penalty_t ]
```

Where:
- c_i, c_j: no-load costs of gas/steam turbines
- s_0, s_1: startup costs
- c_0, c_1: shutdown costs
- u_{i,t}, v_{i,t}, w_{i,t}: unit on/startup/shutdown binary variables
- DSC_penalty_t: load-distribution penalty term (Eqs. 41–46, see §6 below)

## 2. Power balance and plant output (Eqs. 2–4, §2.1)

```
Σ_i g_{i,t} + Σ_j s_{j,t} − a_{j,t} − σ_t = P^plant_t          (Eq. 2)
P^plant_t ≤ GCC                                            (Eq. 3)
P^plant_t ≥ GCC · δ_t                                      (Eq. 4)
```

Where:
- g_{i,t}: gas-turbine output (MW)
- s_{j,t}: steam-turbine output (MW)
- a_{j,t}: auxiliary consumption allocated to steam turbine j (MW)
- σ_t: steam waste (MW)
- P^plant_t: net plant output
- δ_t: plant commitment binary

## 3. Gas-turbine constraints (Eqs. 5–6, §2.2)

```
G̲ · u_{i,t} ≤ g_{i,t} ≤ G̅ · u_{i,t}                     (Eq. 5)
g_{i,t} − g_{i,t−1} ≤ TC · Δt; g_{i,t−1} − g_{i,t} ≤ TD · Δt   (Eq. 6)
```

Production limits (Eq. 5) and ramp-rate limits (Eq. 6) per gas turbine.

## 4. Gas–steam coupling and unit-count relation (Eqs. 7–10, §2.3.1)

```
Σ_j u_{j,t} ≤ Σ_i u_{i,t} − (MUG − 1)                     (Eq. 7)
Σ_j u_{j,t} ≤ Σ_i u_{i,t}                                 (Eq. 8)
Σ_j u_{j,t} ≥ 1 → Σ_i u_{i,t} ≥ MUG                       (Eq. 9)
Σ_i u_{i,t} ≥ MUG · Σ_j u_{j,t} — linearised form        (Eq. 10)
```

These enforce that at least MUG gas turbines must be online for any dispatched steam turbine; if no gas turbine is online, no steam turbine can run.

## 5. Steam-turbine constraints with supplementary firing (Eqs. 11–17, §2.3.2)

```
S̲ · u_{j,t} ≤ s_{j,t} ≤ S̅ · u_{j,t}                    (Eq. 11)
s_{j,t} = STF · ( Σ_i β_{j,t} · g_{i,t} + f_{j,t} ) − a_{j,t} − σ_{j,t}   (Eq. 12)
0 ≤ f_{j,t} ≤ PAF · u_{j,t}                                (Eq. 14/15)
0 ≤ σ_{j,t} ≤ σ_max · u_{j,t}                              (Eq. 16)
a_{j,t} = u_{j,t} · a_const                                 (Eq. 17)
```

Key: Eq. (12) links steam output s_{j,t} to gas-turbine output through the STF, with supplementary fire f_{j,t} providing an independent boost, steam waste σ_{j,t} and auxiliary consumption a_{j,t}.

Note: β_{j,t} allocates gas-turbine exhaust to steam turbines (Eq. 13 defines allocation per steam turbine).

## 6. Load-distribution constraint (Eqs. 41–46, §2.7)

```
d_{i,k,t} ≥ g_{i,t} − g_{k,t}                              (Eq. 42)
d_{i,k,t} ≥ g_{k,t} − g_{i,t}                              (Eq. 43)
d_{i,k,t} ≤ M · (2 − y_{i,k,t})                            (Eq. 45)
δ_{i,k,t} ≤ y_{i,k,t}                                      (Eq. 46)
DSC_penalty_t = DSC · Σ_{i<k} d_{i,k,t}                   (Eq. 1, part)
```

Where:
- d_{i,k,t}: absolute difference between gas turbines i and k
- y_{i,k,t}: indicator that both units are above technical minimum
- δ_{i,k,t}: additional binary (refining the both-above-minimum condition)
- DSC: penalty coefficient in the objective

Constraint only activates when both compared gas turbines are above their technical minimum output.

## 7. Startup ramp blocks (Eqs. 19–32, §2.5)

Sets of equations defining the energy blocks for hot/warm/cold startup profiles (Table 2). Each thermal state prescribes a block-wise ramp trajectory for the steam turbine that limits how much output can be brought online per hour, encoded through energy-block variables and sequencing constraints.

Formulation uses block variables b_{j,t,l} (block l of steam turbine j at hour t) with constraints:
```
s_{j,t} = Σ_l θ_{j,l} · b_{j,t,l}                         (Eq. 19)
0 ≤ b_{j,t,l} ≤ B_max(l) · x_{j,t,l}                      (Eq. 20–29)
Σ_l x_{j,t,l} = u_{j,t}                                    (Eq. 30)
```
(Simplified representation; paper has 12 distinct block equations.)

## 8. Minimum gas-hours gating for steam startup (Eqs. 33–37, §2.6)

The central novel constraint group. Steam-turbine hot/cold startup is gated by:
- **Hot-start window**: if the steam turbine has been off ≤ 9 h (KMH) it may start hot; otherwise cold start is forced.
- **Cold-start minimum**: for a cold startup, gas turbines must have been running for ≥ KGC = 3 h before the steam start.

Eqs. (33)–(37) encode these temporal-gating constraints through variables tracking the offline duration of each steam turbine and the cumulative online hours of the gas-turbine group.

## 9. Plant startup/shutdown sequencing (Eqs. 38–40, §2.4)

Additional logic for minimum up/down times and coordinated startup sequencing — steam turbines follow startup ramps only after enough gas turbines are online (MUG condition).
