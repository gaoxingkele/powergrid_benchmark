# CGO Unified Optimization Algorithm

## Mathematical Formulation

### Global Multi-Objective Function

The optimization is guided by a composite objective function Ft that balances technical performance, economic benefit, and environmental impact:

Ft = min[W1(PLoss + QLoss) + W2 x VDI - W3 x CSaved Energy Loss + W4 x (1 / delta QCO2)]

where:
- PLoss = sum(I^2_s,i x Rs,i) for i=1..N-1 (active power loss, kW)
- QLoss = sum(I^2_s,i x Xs,i) for i=1..N-1 (reactive power loss, kVAR)
- VDI = sum((1 - Vi)^2) for i=1..N (voltage deviation index)
- CSaved Energy Loss = Ce x (Ploss,base - Ploss,new) x t (annual cost saving from reduced losses, USD/year)
  - Ce = 0.03 $/kWh, t = 8760 h/year
- delta QCO2 = fCO2 x delta Eslack (annual CO2 emission reduction, kg/year)
  - fCO2 ranges: Coal = 0.95, Oil = 0.75, Natural Gas = 0.45, Grid average = 0.5-0.9 kg CO2/kWh
- W1 = 0.4, W2 = 0.25, W3 = 0.1, W4 = 0.25 (weighting factors)

### Power Balance Constraints

PS,b = sum(Pld,i) + PLoss - sum(PDG,i) for i=2..N
QS,b = sum(Qld,i) + QLoss - sum(QCB,j) for i=2..N, j=1..mc

### DG and CB Constraints

PDG,min < PDG,i < PDG,max
sum(PDG,i) < 0.9 x sum(Pld,i)
sum(QCB,j) < 0.9 x sum(Qld,i)

### Voltage Constraint

0.95 <= Vi <= 1.05 for all buses i

### Thermal Capacity Constraint

|Sij| <= Sij,max where Sij = Vi x I*ij

### Capital Cost

CDG = sum(PDG,i x Cg)   (Cg = cost per kW of DG installed)
CCB = sum(QCB,j x Cc)   (Cc = cost per kVAR of CB installed)

### Payback Period

Payback = (CDG + CCB) / CSaved Energy Loss

## Unified Optimization Pseudocode

The proposed Classification-based Global Optimization (CGO) method merges EVCS, DG, and CB planning into a single structured routine.

```
Algorithm: CGO Unified Planning

Input: Network data (bus loads, line impedances, topology), EV_HF (30/40/50%)
Output: Optimal placement and sizing of EVCSs, DGs, CBs; minimized Ft

/* Stage 0: Base-case analysis */
1. Run power flow for base case (no DGs, CBs, or EVCSs)
2. Record: PLoss_base, QLoss_base, V_base, total active/reactive load

/* Stage 1: Bus classification */
3. Decompose radial network into branches
4. Rank branches by active power demand    (for EVCS and DG placement)
5. Rank branches by reactive power demand  (for CB placement)

/* Stage 2: EVCS planning */
6. Set total EVCS load = EV_HF x total system load
7. Select top-2 branches from active-power ranking for EVCS candidates
8. Initialize: split EV load equally between two stations
9. For each candidate location on selected branches:
     a. Assign EV load to candidate
     b. Run power flow
     c. Evaluate Ft
10. Iteratively adjust EVCS sizes (unequal split) to minimize Ft
11. Record optimal EVCS placement and sizing

/* Stage 3: DG planning */
12. Select top-2 branches from active-power ranking for DG candidates
    (branches may overlap with EVCS locations)
13. For each candidate location on selected branches:
     a. Initialize DG size = branch active power demand
     b. Run power flow
     c. Check constraints: voltage limits, thermal limits, DG capacity limits
     d. Evaluate Ft
14. Incrementally tune DG sizes subject to:
     sum(PDG,i) < 0.9 x sum(Pld,i)
     PDG,min < PDG,i < PDG,max
     |Sij| <= Sij,max for all branches
15. Record optimal DG placement and sizing

/* Stage 4: CB planning */
16. Select top-2 branches from reactive-power ranking for CB candidates
17. For each candidate location:
     a. Initialize CB size = branch reactive demand
     b. Run power flow
     c. Check all constraints
     d. Evaluate Ft
18. Incrementally tune CB sizes subject to:
     sum(QCB,j) < 0.9 x sum(Qld,i)
     |Sij| <= Sij,max for all branches
19. Record optimal CB placement and sizing

/* Stage 5: Final evaluation */
20. Run full-system power flow with optimal EVCS + DG + CB
21. Compute:
     - Active/reactive losses (PLoss, QLoss)
     - Voltage deviation index (VDI)
     - Minimum voltage (Vmin)
     - Substation power factor
     - Annual CO2 emission reduction (delta QCO2)
     - Capital costs (CDG, CCB)
     - Annual energy loss saving (CSaved Energy Loss)
     - Payback period
22. Return optimized configuration and performance metrics
```

## Step-by-Step Explanation

1. **Base-case power flow**: Captures initial operating conditions (losses, voltages, load) as the reference for improvement quantification.

2. **Bus classification**: The radial network is decomposed into branches from the radial tree. Each branch is ranked by active power demand (for EVCS and DG placement) and reactive power demand (for CB placement). This is the key innovation — resources are allocated only to branches with highest need, not searched across all N buses.

3. **Sequential component planning**: EVCSs are optimized first (since EV load is the new stressor), then DGs (to supply the active power deficit), then CBs (to provide reactive support). This ordering reflects causal dependency: EV load creates the need, DGs supply active power, CBs compensate reactive imbalance.

4. **Iterative sizing adjustment**: For each component type, candidate locations on the selected branches are evaluated, and sizes are incrementally adjusted while checking all operational constraints (voltage, thermal, capacity limits).

5. **Constraint enforcement**: At every step, thermal capacity limits |Sij| <= Sij,max, voltage limits 0.95-1.05 p.u., and component-specific limits are verified. The process terminates when Ft ceases to improve.

## Complexity Analysis

- **Not specified in paper**: The paper does not provide formal time or space complexity analysis.
- **Empirical observation**: CGO requires 18 iterations for IEEE 33-bus and 22 iterations for IEEE 69-bus, compared to 100 fixed iterations for PSO and GWO. Run time is 25 s (33-bus) and 28.5 s (69-bus). The reduction is attributed to the classification step that narrows the search space to only high-load branches.
