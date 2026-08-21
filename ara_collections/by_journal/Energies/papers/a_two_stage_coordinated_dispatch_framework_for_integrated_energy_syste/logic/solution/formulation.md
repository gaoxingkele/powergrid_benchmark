# Mathematical Formulation

## Objective Function (Eq. 12)

```
min C = C1 + C2 + C3
```

**Upstream procurement cost C1:**
```
C1 = ∑_t (λ^t_{e,spot} P^t_{grid} + λ^t_{g,spot} V^t_{gas})
```

**Equipment O&M cost C2:**
```
C2 = ∑_t [ ∑_h (a_h P^2_{h,t} + b_h P_{h,t} + c_h) + ∑_u (a_u P^2_{u,t} + b_u P_{u,t} + c_u) + ∑_p C_p P_{p,t} ]
```

**EESS lifecycle cost C3:**
```
C3 = C_{LCOE} ∑_t P^{out}_{EESS,t} ∆t
```

## Constraints

### TOU Pricing and Market Stability (Eqs. 13–17)
- Peak tariff bounds: λ^min_peak ≤ λ^t_e ≤ λ^max_peak (Eq. 13)
- Valley tariff bounds: λ^min_valley ≤ λ^t_e ≤ λ^max_valley (Eq. 14)
- Tariff ordering: max(λ_valley) < λ_flat < min(λ_peak) (Eq. 15)
- Peak-to-valley ratio: γ = λ_peak/λ_valley, γ^min ≤ γ ≤ γ^max, [2, 5] (Eqs. 16–17)

### PDR Load Model (Eqs. 5–11)
- Fixed load: P^t_{fixed} = C_{fixed} (Eq. 5)
- Shiftable load: Eq. 6 with daily energy conservation (Eq. 7) and bounds (Eq. 8)
- Interruptible load: Eq. 9 with bounds (Eq. 10)
- Total load: P^t_{total} = P^t_{fixed} + P^t_{shift} + P^t_{inter} (Eq. 11)

### DistFlow Power Flow (Eqs. 18–21)
- Active power balance (Eq. 18), reactive power balance (Eq. 19)
- Voltage drop (Eq. 20), current-voltage relation (Eq. 21)

### Line Thermal Limits (Eqs. 22–23)
Active/reactive power bounds with safety margin coefficient.

### Voltage/Current Security (Eqs. 24–25)
Squared voltage and current bounds.

### Generation Constraints (Eqs. 26–31)
Capacity limits (26), start-up/shut-down ramping (27–28), ramp rates (29), min up/down time (30–31).

### Spinning Reserve (Eq. 32)
```
∑_i (u_{i,t} P^max_i − P_{i,t}) ≥ R^req_t
```

### Gas Network Constraints (Eqs. 33–36)
- Nodal gas mass balance (Eq. 33)
- Gas source limits (Eq. 34)
- Nodal pressure bounds (Eq. 35)
- Weymouth pipeline flow (Eq. 36, piecewise-linearized)

### Wind and P2G Coupling (Eqs. 37–39)
- Wind output: 0 ≤ P^{act}_{w,i,t} ≤ P^{pre}_{w,i,t} (Eq. 37)
- P2G-wind coupling: P^{elec}_{P2G,j,t} ≤ ∑_w (P^{pre}_{w,w,t} − P^{act}_{w,w,t}) (Eq. 38)
- P2G power limits (Eq. 39)

### EESS Constraints (Eqs. 40–47)
- Charging/discharging power with mutual exclusivity (Eqs. 40–42)
- SOC limits (Eqs. 43–44)
- Energy balance with self-discharge (Eq. 45)
- Daily cycle conservation (Eq. 46)
- Max cycle limit (Eq. 47)

### V2G Constraints (Eqs. 48–56)
- Arrival/departure times via normal distributions (Eqs. 48–49)
- Uncoordinated charging window (Eq. 50)
- Aggregated baseline (Eq. 51)
- SOC tracking (Eq. 52), SOC bounds (Eq. 53)
- Power limits with mutual exclusivity (Eqs. 54–55)
- Aggregate grid-side power (Eq. 56)

### LCOE (Eqs. 57–59)
- LCOE calculation: CAPEX + ∑ OPEX_y/(1+r)^y divided by ∑ E^out_y/(1+r)^y (Eq. 57)
- CAPEX decomposition (Eq. 58), OPEX decomposition (Eq. 59)

### P2G Coupling (Eqs. 60–61)
- Gas output: G^{P2G}_{i,t} = η_{P2G} · HGV · P^{P2G,elec}_{i,t} (Eq. 60)
- Power limits (Eq. 61)

### Gas-Fired Unit (Eq. 62)
- Power output: P^{GF}_{i,t} = η^{GF}_i · HGV · G^{GF}_{i,t}

### Conventional Unit Cost (Eq. 63)
- C_i(P_{g,i,t}) = a_i P^2_{g,i,t} + b_i P_{g,i,t} + c_i
