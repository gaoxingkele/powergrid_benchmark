# Constraints

## Equality Constraints

### 1. Power-Flow Equations
Active power balance at node i:
```
Pi = Vi * sum_j(Vj * (Gij*cos(theta_ij) + Bij*sin(theta_ij)))
```

Reactive power balance at node i:
```
Qi = Vi * sum_j(Vj * (Gij*sin(theta_ij) - Bij*cos(theta_ij)))
```

### 2. Capacity Constraints for DG and Loads
Total PV capacity: sum(Ppv_i) = PTPV
Total wind capacity: sum(Pwind_j) = PTW
Total load capacity: sum(PL_d) = PTL

## Inequality Constraints

### 1. Branch-Power Limits
```
Sk <= Sk_max   for k in [1, Nb]
```
where Sk is apparent power on branch k, Sk_max is branch capacity limit.

### 2. Output Limits for Distributed Generators
```
Pmin_DGi <= PDGi <= Pmax_DGi
Qmin_DGi <= QDGi <= Qmax_DGi
```

### 3. Energy Storage and Dispatchable EV Constraints
SOC limits: SOCmin <= SOC(t) <= SOCmax
Charging power limits: Pes_cmin <= Pes_c <= Pes_cmax
Discharging power limits: Pes_fmin <= Pes_f <= Pes_fmax

### 4. Practical DER Deployment Constraints
Spatial availability: Only buses with sufficient installation area considered.
Short-circuit capacity limits: Maximum DER injection limited by switchgear ratings.
Grid connection feasibility: DERs at buses with pre-existing connection interfaces.
Formalized as: PDER_i <= delta_feas_i * Pmax_i, where delta_feas_i in {0,1}.

### 5. Energy Balance (ES/Dispatchable EV)
Charging: Ees(t) = Ees(t-dt) + eta * Pes_c * dt
Discharging: Ees(t) = Ees(t-dt) - Pes_f * dt / eta

## Optimization Model Formulation
```
min f(xc, xs) = min{f1(xc,xs), f2(xc,xs), f3(xc,xs)}
s.t. hi(xc, xs) = 0, i = 1,2
     gi(xc, xs) <= 0, i = 1,2,...,7
```
where xc are control variables, xs are state variables, f1 is investment cost, f2 is expected energy shortage, f3 is network loss.
