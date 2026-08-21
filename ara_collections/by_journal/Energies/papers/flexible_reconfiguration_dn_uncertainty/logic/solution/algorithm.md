# Algorithm: Coati Optimization Algorithm (COA) for Dynamic Reconfiguration

## Overview

The Coati Optimization Algorithm (COA) is a population-based metaheuristic inspired by the natural behaviors of coatis (Nasua nasua). It is adapted in this paper to solve the hourly dynamic reconfiguration problem for distribution networks.

## Algorithm Structure

### Input Parameters
- N: Population size
- m: Number of decision variables (open switches per hour)
- Itermax: Maximum number of iterations
- LB, UB: Lower and upper bounds of decision variables
- Network data: Bus, branch, DG, load, and price data
- Uncertainty data: Wind speed, solar irradiance, load PDF parameters

### Decision Variables
- X = [SW1, SW2, ..., SW_N_SW]
- Each SWj = [SWj^1, SWj^2, ..., SWj^24] represents the status of the jth switch over 24 hours
- SWj^t = 1 (closed) or 0 (open) at time t

### Objective Function
```
Minimize Cost = sum_{t=1}^{24} [Closs_t + CVD_t + Cupn_t + CPV_t + CWind_t + CSW_t]
```
Subject to constraints (29)-(37).

### Phase 1: Hunting Strategy for Iguanas (Global Exploration)

1. **Population division**: Split N coatis into two equal groups: [N/2] and N-[N/2]
2. **First group (climbers)**: For i = 1 to [N/2]:
   - XP1_ij = x_ij + r * (iguana_j - I * x_ij)
   - The iguana position is the best member's position
   - I is a random integer {1, 2}; r is a random real [0, 1]
3. **Second group (ground hunters)**: For i = [N/2]+1 to N:
   - Randomly generate iguana position on ground: IGGround_j = LB_j + r * (UB_j - LB_j)
   - If IGGround is better than current position: XP1_ij = x_ij + r * (IGGround_j - I * x_ij)
   - Else: XP1_ij = x_ij + r * (x_ij - IGGround_j)
4. **Position update**: Accept new position if fitness improves

### Phase 2: Escape Strategy from Predators (Local Exploitation)

1. Define local bounds: LBlocal_j = LB_j / Iter, UBlocal_j = UB_j / Iter
2. For each coati i:
   - XP2_ij = x_ij + (1-2r) * (LBlocal_j + r * (UBlocal_j - LBlocal_j))
3. **Position update**: Accept new position if fitness improves

### Termination
- Repeat Phases 1 and 2 until Iter = Itermax
- Output the best solution found

## Pseudo-code (from Figure 1)

```
COA (N, m, I, Itermax, LB, UB)
1. Generate random population (N)
2. Evaluate objective functions for all N
3. Iter = 1
4. while Iter < Itermax do
5.   Select iguana position = best member position
6.   // Phase 1: Hunting
7.   for i = 1 to [N/2] do
8.     Generate I(1xm) with elements 1 or 2
9.     Determine new positions XP1 using Equation (39)
10.    Calculate objective functions for XP1
11.    Update Xi using Equation (42)
12.  end for
13.  for i = [N/2]+1 to N do
14.    Generate I(1xm) with elements 1 or 2
15.    Calculate random position for on-ground iguana by (40)
16.    Determine new positions XP1 using Equation (41)
17.    Calculate objective functions for XP1
18.    Update Xi using Equation (42)
19.  end for
20.  // Phase 2: Escape from predators
21.  for i = 1 to N do
22.    Determine new positions XP2 using Equations (43)-(44)
23.    Calculate objective functions for XP2
24.    Update Xi using Equation (45)
25.  end for
26.  Iter = Iter + 1
27.end while
28.output (best solution)
```

## Integration with Power Flow

The COA DR implementation embeds a Newton-Raphson power flow solver within the optimization loop:
1. For each candidate configuration (set of open switches), run load flow
2. Compute branch currents, bus voltages, and power losses
3. Evaluate objective function (Equation 20)
4. Check constraint violations (Equations 29-37)
5. Apply penalty for constraint violations
