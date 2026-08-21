# Formulation: Microgrid Economic-Environmental Dispatch

Source: §2 (device models) and §3 (objective + constraints).

## System
Single-bus multi-source microgrid (Figure 8) with distributed PV, wind turbines (WT), a small thermal generator (DG), an energy storage system (ESS), and a main-grid tie, serving residential and industrial loads. Case study: 10 PV units (10 kW each), WT (10 kW), one DG (1000 kW), 2 ESS units (10 kW each); 24-h horizon, 1-h steps.

## Device models (§2)

### PV output (Eq. 1)
```
P_PV = P_o * (G_INC / G_STC) * (1 + k (T_c - T_o))
```
- P_o: max power at Standard Test Conditions; G_INC: actual irradiance (kW/m^2); G_STC = 1 kW/m^2; k: temperature power coefficient; T_c: cell temperature; T_o: reference temp (typically 25 C). Higher temperature -> lower efficiency.

### Wind output (Eq. 2, piecewise)
```
P_WT = 0                                   for 0 <= V <= Vi
     = Prated * (V - Vi)/(Vr - Vi)         for Vi <= V <= Vr
     = Prated                              for Vr <= V <= Vc
     = 0                                   for Vc <= V
```
- V: wind speed; Vi: cut-in; Vr: rated; Vc: cut-out.

### Thermal generator fuel (Eq. 3)
```
VF(t) = a1 * P_DIE(t) + a2 * (P_DIE(t)/P_DG(t))^2
```
- VF: fuel consumption (L); P_DIE: actual output (kW); P_DG: rated output (kW); a1, a2: fuel-curve coefficients (L/kWh). Actual output fluctuates between 30% of rated and rated.

### Energy storage (Eqs. 4-5)
```
Charge:    SOC.1(t) = (1-delta) Soc(t-1) + Pc*dt*eta_c / Ec
Discharge: SOC.2(t) = (1-delta) Soc(t-1) - Pd*dt / (Ec*eta_d)
```
- delta: self-discharge rate; eta_c/eta_d: charge/discharge efficiency; Ec: rated capacity (kWh).

## Objective function (§3.1)
```
Min C_sun = C1 + C2     (Eq. 6)
```
### Operating cost C1 (Eqs. 7-11)
```
C1 = Σ_t Σ_i [ C_om_i(t) + C_DG_i(t) + C_DS_i + C_grid_i(t) ]                       (Eq. 7)
C_om_i(t) = K_PV P_PV + K_WT P_WT + K_DG P_DG + K_ESS P_ESS                          (Eq. 8)   (O&M)
C_DG_i(t) = Cr * P_DG_i(t) / eta_DG_i                                                (Eq. 9)   (fuel)
C_DS_i(t) = DS_i * P*_i(t) / (P_i,max * a * f_i)                                     (Eq. 10)  (depreciation)
C_grid_i(t) = Pci(t) * Cg(t)                                                         (Eq. 11)  (grid interaction)
```
- K_*: O&M cost coefficients; Cr: fuel price (CNY/L); eta_DG: thermal efficiency; DS_i: annual depreciation; a: constant; f_i: capacity factor; Pci: purchased/sold energy; Cg: electricity price.

### Environmental cost C2 (Eq. 12)
```
C2 = Σ_i Σ_j  l_{i,j} * lambda_j * P_DIE(t)
```
- l_{i,j}: amount of pollutant type j emitted per unit output of thermal generator i; lambda_j: treatment cost of pollutant j; P_DIE: thermal output. Pollutants: CO2, SO2, NOX (Table 2).

## Constraints (§3.2)
Power balance (Eq. 13); grid-interaction limits (Eq. 14); PV/WT/DG output and ESS SOC limits (Eqs. 15-18); ESS charge/discharge power caps (Eqs. 19-20); pollutant-emission cap (Eq. 21); DG ramp-rate limit (Eq. 22). See `constraints.md` for full list.

## Scheduling strategy (§3.3, Figure 1)
Merit order: (1) fully utilize PV and WT; (2) use ESS to buffer renewable variability (charge on surplus, discharge on deficit — peak-shaving/valley-filling); (3) add DG output as needed for baseload/large demand; (4) exchange with the main grid as the final balancing step (buy when short, sell when in surplus).

## Parameters (case study)
- Device operating parameters: Table 1 (lifespan, install/maintenance/depreciation cost, max power).
- Pollutant treatment costs and emission factors: Table 2.
- Time-of-use electricity prices: Table 4 (peak/standard/off-peak, purchase & sale).
- Input profiles: load (Figure 9), wind speed (Figure 10), temperature (Figure 11), irradiance (Figure 12).
