# Constraints

This file documents all constraints from the ADN expansion planning model defined in Sections 3.3 and 4 of the paper.

## E-SOP Power Balance Constraint
The power at the two AC terminals of the E-SOP and the DC-side BESS must remain balanced:
```
P_SOP_AC_i,t + P_SOP_AC_j,t + P_SOP_AC_k,t = P_BESS_dc,t + P_E-SOP_L,ij,t
```
Positive when flowing outwards. P_BESS_dc,t positive when discharging.

SOP power loss:
```
P_E-SOP_L,ij,t = A_E-SOP × sqrt(P_E-SOP_AC,ij,t^2 + Q_E-SOP_AC,ij,t^2)
```
where A_E-SOP is the SOP power loss coefficient.

## Capacity Constraints of AC Terminals in E-SOP
The active and reactive power of each AC terminal are limited by its rated capacity:
```
(P_SOP_AC,it)^2 + (Q_SOP_AC,it)^2 ≤ (S_SOP_max,n)^2
```

## Power and Energy Constraints of BESS in E-SOP
Charging/discharging power limits:
```
-P_BESS_max ≤ P_BESS_dc,t ≤ P_BESS_max
```

Energy state transition:
```
E_BESS_t = E_BESS_t-1 + P_BESS_ch_dc,t × η_ch × Δt - (P_BESS_dis_dc,t / η_dis) × Δt
```

Energy state limits:
```
0.2 × E_BESS_m ≤ E_BESS_t ≤ E_BESS_m
```

## DG Capacity Constraints
Wind and PV installed capacities at each node must not exceed upper limits:
```
0 ≤ S_Wind_j ≤ Z_WTG_max,j, ∀j ∈ Ω_WTG
0 ≤ S_PV_j ≤ Z_PVG_max,j, ∀j ∈ Ω_PVG
```

## Network Topology Constraints
The distribution network must maintain connectivity and radiality. Specific modeling approaches referenced from [18] (Lavorato et al., 2012).

## Voltage and Current Constraints
Voltage limits:
```
U_i_min^2 ≤ v_i,t ≤ U_i_max^2, ∀i ∈ Ω_N
```

Current limits:
```
I_ij,t^2 ≤ I_ij_max^2, ∀(i,j) ∈ Ω_line
```

## Power Flow Constraints
Active power balance at each node:
```
∑P_ij,t - ∑(P_ni,t - R_ni × I_ni,t^2) = P_inj,i,t, ∀i ∈ Ω_N
```

Reactive power balance at each node:
```
∑Q_ij,t - ∑(Q_ni,t - X_ni × I_ni,t^2) = Q_inj,i,t, ∀i ∈ Ω_N
```

Nodal power injection composition:
```
P_inj,it = P_WT,it + P_PV,it + P_E-SOP_AC,it - P_L,it
Q_inj,it = Q_WT,it + Q_PV,it + Q_E-SOP_AC,it + Q_SVC,it - Q_L,it
```

Voltage–power flow relationship (relaxed form):
```
v_i,t^2 - v_j,t^2 ≥ 2(R_ij×P_ij,t + X_ij×Q_ij,t) - (R_ij^2 + X_ij^2)×I_ij,t^2 - M×(1 - x_line_ij)
v_i,t^2 - v_j,t^2 ≤ 2(R_ij×P_ij,t + X_ij×Q_ij,t) + (R_ij^2 + X_ij^2)×I_ij,t^2 + M×(1 - x_line_ij)
I_ij,t^2 × v_i,t^2 - (P_ij,t^2 + Q_ij,t^2) = 0
```
where M is a sufficiently large constant and x_line_ij is a binary variable for line existence.

## Relaxation Gap Constraints (SCCR)
Branch relaxation gap:
```
g^flow_t = (P_ijt^2 + Q_ijt^2) / (I_ijt^2 × v_it^2) - 1
```

E-SOP relaxation gap:
```
g^E-SOP_t = (P_E-SOP_AC,ijt^2 + Q_E-SOP_AC,ijt^2) / (A_E-SOP × P_E-SOP_L,ijt) - 1
```

## Linear Cutting-Plane Constraints (SCCR)
```
(P_ijt^2 + Q_ijt^2) / v_it^2 - I_ij_max^2 ≤ 0
P_E-SOP_L,ijt - A_E-SOP × sqrt(P_E-SOP_AC,ijt^2 + Q_E-SOP_AC,ijt^2) ≤ 0
```
