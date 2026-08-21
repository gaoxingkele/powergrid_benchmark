# Constraints

This document catalogs all mathematical constraints defined in the optimization model.

## 1. Energy Storage State of Charge (SOC) Constraints

```
SOC_i,min <= SOC_i(n) <= SOC_i,max
```
Where SOC_i,min and SOC_i,max represent the upper and lower limits of remaining power for the i-th type of energy storage.

**Values from Table 1:**
- Li-ion battery SOC range: [20%, 80%]
- Flow battery SOC range: [10%, 90%]

## 2. Energy Storage Rated Power and Capacity Constraints

```
E_ESS,min_i <= E_ESS_i <= E_ESS,max_i
P_ESS,min_i <= P_ESS_i <= P_ESS,max_i
```

Where:
- E_ESS,min_i, E_ESS,max_i: upper/lower limits of rated capacity at node i
- P_ESS,min_i, P_ESS,max_i: upper/lower limits of rated power at node i

## 3. Charge-Discharge Mutual Exclusion Constraint

```
X_ch_a_r + X_di_s_r <= 1
```

Energy storage devices of the same type at time t cannot be simultaneously charged and discharged. X_ch and X_di are binary (0-1) variables representing charging and discharging states.

Where r in {1: Li-ion Battery, 2: Vanadium Flow Battery}

## 4. Power Balance Constraint (Flexibility Supply-Demand)

```
P_TH(t) + P_wind/PV(t) + P_ESS(t) + P_aban(t) + P_grid(t) = P_load(t) + P_cl(t)
```

Where:
- P_TH(t): Thermal power output at time t
- P_wind/PV(t): Wind and PV joint output
- P_ESS(t): HESS charging/discharging power
- P_aban(t): Wind and PV curtailment power
- P_grid(t): Tie-line power with main grid (positive = import, negative = export)
- P_load(t): Total load demand
- P_cl(t): Load shedding power

## 5. Grid Operation Security Constraints

```
U_i,min <= U_i,t <= U_i,max
I_ij,min <= I_ij,t <= I_ij,max
```

Where:
- U_i,min, U_i,max: voltage limits at node i
- I_ij,min, I_ij,max: branch current limits for branch ij

## 6. Nodal Power Balance Constraints

**Active power:**
```
P_i(t) + sum(P_kj(t)) - sum(P_ij(t)) - r_ij * I_ij(t)^2 = 0
```

**Reactive power:**
```
Q_i(t) + sum(Q_kj(t)) - sum(Q_ij(t)) - x_ij * I_ij(t)^2 = 0
```

## 7. Branch Current Constraint

```
P_ij(t)^2 + Q_ij(t)^2 = U_i(t)^2 * I_ij(t)^2
```

## 8. Node Voltage Balance Constraint

```
U_j(t)^2 = U_i(t)^2 - 2(P_ij(t)*r_ij + Q_ij(t)*x_ij) + (r_ij^2 + x_ij^2) * I_ij(t)^2
```

## 9. Node-Level Resource Balance

**Active power at node i:**
```
P_i,load(t) - P_i,WD/PV(t) - P_i,ESS(t) - P_i,aban(t) - P_i,grid(t) - v_i(t) - P_i,cl(t) - P_i,TPP(t) = 0
```

**Reactive power at node i:**
```
Q_i,load(t) - Q_i,WD/PV(t) - Q_i,grid(t) - v_i(t) - Q_i,cl(t) - Q_i,TPP(t) = 0
```

Variables for resources not connected to a node are set to zero.

## 10. VMD Decomposition Constraints

```
sum(u_k(t)) = f(t)  for k = 1 to K
```

Where u_k(t) are the K modal components and f(t) is the original ESS target power signal. This ensures lossless decomposition of the total energy storage target output.
