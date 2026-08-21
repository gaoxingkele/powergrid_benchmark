# Constraints for Economic Dispatch in Hybrid Generation Systems

## 1. Power Balance (Equality Constraint)
Sum of all generation equals demand at each hour:
- PTix + PHjx + PEkx + PFlx = PDx
- Single-node model; transmission losses ignored.

## 2. Generation Limits (Inequality Constraint)
Each unit operates within its established bounds:
- Pmin <= Pgen <= Pmax

## 3. Hydroelectric Power Output
PHjx = C1j(Vjx)^2 + C2j(Qjx)^2 + C3j(Vjx * Qjx) + C4j(Vjx) + C5j(Qjx) + C6j
- Power is a quadratic function of reservoir volume Vjx and water discharge Qjx.

## 4. Water Discharge Limits
Qmin <= Qjx <= Qmax

## 5. Reservoir Volume Limits
Vmin <= Vjx <= Vmax

## 6. Reservoir Volume Balance
Vjx = Vj(x-1) + In_jx - Qjx - Sjx
- Volume depends on previous volume, inflow, discharge, and spillage.

## 7. Coupled Hydroelectric Reservoirs
Vjx = Vj(x-1) + In_jx - Qjx - Sjx + sum(Qlx + Slx)
- For cascaded reservoirs, volume also depends on upstream discharges and spillages.

## Constraint Enforcement
Penalty-based mechanism:
- Power balance tolerance: 0.0001 MW
- Water balance tolerance: 0.001 hm^3
- Penalty factors (Table 6): pen1 (power) = 20-30, pen2 (water) = 360 across algorithms
