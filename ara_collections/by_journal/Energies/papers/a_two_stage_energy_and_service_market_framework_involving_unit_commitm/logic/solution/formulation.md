# Mathematical Formulation

## DAM Model (Eqs. 2–9)

### Objective (Eq. 2)
```
min τ · ∑_{i∈Ω_G} ∑_{s∈Ω_i^S} c_{i,s} P_{i,s,t}
```

### Constraints

**Generator dispatch (Eq. 3–4):**
```
P^D_{i,t} = ∑_s P_{i,s,t}, ∀i
0 ≤ P_{i,s,t} ≤ ∆P^max_{i,s,t}, ∀i,s
```

**Thermal unit max power (Eq. 5):**
```
0 ≤ P^D_{i,t} ≤ P^max_{i,t}, ∀i∈Ω_DT ∪ Ω_ND
```

**RES max power (Eq. 6):**
```
0 ≤ P^D_{i,t} ≤ P^{da}_{i,t}, ∀i∈Ω_R
```

**DH max power (Eq. 7):**
```
0 ≤ P^D_{i,t} ≤ k_H P^{H,max}_{i,t}, ∀i∈Ω_H
```

**Zonal power balance (Eq. 8):**
```
∑_i α^G_{i,z} P^D_{i,t} − ∑_l α^F_{z,l} F_{l,t} = D^{da}_{z,t}, ∀z
```

**Interzonal flow limits (Eq. 9):**
```
F^{lb}_l ≤ F_{l,t} ≤ F^{ub}_l, ∀l
```

**Monthly escalator (Eqs. 1, 10):**
```
P^max_{i,t} = P^max_i · e_{i,t} · a_{i,t}
∆P^max_{i,s,t} = ∆P^max_{i,s} · e_{i,t}
```

## ASM Model: NCUCER (Eqs. 11–44)

### Objective (Eq. 11)
```
f_d = τ · ∑_{t=1}^{N_T} (C^R_t + C^{UD}_t + C^{SR}_t + C^{LS}_t + C^{RC}_t)
```

where:
- C^R_t: redispatching cost (UR costs + DR revenues) — Eq. 12
- C^{UD}_t: SU/SD costs — Eq. 13
- C^{SR}_t: secondary reserve cost — Eq. 14
- C^{LS}_t: load shedding penalty — Eq. 15
- C^{RC}_t: RES curtailment penalty — Eq. 16

### Redispatch Constraints (Eqs. 17–19)
```
∆P↓_{i,s,t} ≤ ∆P↓_{i,s,t} z↓_{i,t}  (per-step DR limit)
∆P↑_{i,s,t} ≤ ∆P↑_{i,s,t} z↑_{i,t}  (per-step UR limit)
z↑_{i,t} + z↓_{i,t} ≤ 1  (no simultaneous UR and DR)
```

### DT Net Redispatch (Eq. 20)
```
∆P^A_{i,t} = ∑_s ∆P↑_{i,s,t} − ∑_s ∆P↓_{i,s,t} + P^{su}_{i,t} z^{su}_{i,t} − P^{sd}_{i,t} z^{sd}_{i,t}
```

### DT Unit-State Constraints (Eqs. 21–28, 30–34)

These encode the five-case bid adjustment logic from Figure 3:
- State limited by availability (Eq. 21)
- Min/max power with SR margins (Eqs. 22–23)
- SR only when unit online (Eqs. 24–25)
- SU/SD consistency (Eq. 26)
- MUT/MDT via Eqs. 27–28 with duration parameters Eq. 29
- Case-specific ordering (Eqs. 30–34): SU before UR if P^D < P^min; mandatory SU or SD if 0 < P^D < P^min; no SU if P^D >= P^min; no SD if P^D = 0

### DH Unit Constraints (Eqs. 35–38)
Energy balance (Eq. 35), power limits (Eq. 36), non-stored energy (Eq. 37), available energy update (Eq. 38)

### RES Curtailment and Load Shedding (Eqs. 39–40)
```
0 ≤ P^{rc}_{i,t} ≤ P^{rt}_{i,t}, ∀i∈Ω_R
0 ≤ D^{ls}_{n,t} ≤ D^{rt}_{n,t}, ∀n∈Ω_N
```

### Network Constraints (Eqs. 41–43)
- Nodal power balance (Eq. 41)
- Branch flow bounds (Eq. 42)
- Flow variation via PTDF (Eq. 43): ∆F_{b,t} = ∑_n S_{n,b} [ ∑_i β_{i,n} ∆P^A_{i,t} + ∑_i β_{i,n} ∆P^R_{i,t} − ∆D^L_{n,t} + D^{ls}_{n,t} − ∑_i β_{i,n} P^{rc}_{i,t} ]

### Secondary Reserve (Eq. 44)
```
∑_{i∈Ω_DT} P^{sr↓}_{i,t} = SRR_t ∧ ∑_{i∈Ω_DT} P^{sr↑}_{i,t} = SRR_t
```

## Benchmark Model (Appendix A, Eqs. A1–A16)

Standard DAM model with UC and reserve constraints based on [32,33]. Includes MUT/MDT, SU/SD costs, SR constraints, zonal power balance. Used for comparison with the proposed sequential approach.
