# Problem: Bi-Objective Resilient Backbone-Grid Planning

## Domain
Power Systems, Grid Planning, Resilience, Multi-Objective Optimization

## Problem Statement
Given a power transmission network with fixed pumped-storage connection locations and capacities, the goal is to select an optimal set of backbone transmission lines such that:
1. All critical buses (black-start, core-load, important power source) are connected
2. Edge connectivity >= 2 between core-load buses and pumped-storage buses (N-1 connectivity)
3. Power flow security is maintained under both pumped-storage generation and pumping scenarios
4. Total life-cycle costs (F1) are minimized
5. System resilience mismatch index (F2) is minimized

## Inputs
- Original grid topology with bus and line parameters
- Candidate line set E with impedance, reactance, and capacity data
- Core-load buses (V_core), black-start/pumped-storage buses (V_psh), important power source buses (V_imp)
- Conventional generator data and load data
- Pumped-storage unit ratings

## Decision Variables
- Binary vector Y = [y1, y2, ..., y|E|]^T where yi = 1 if candidate line i is selected for the backbone grid, 0 otherwise

## Objective Functions
- F1 (Economic): Normalized sum of impedance moduli of selected lines
- F2 (Resilience): System resilience mismatch index = F2_dist * (1 - alpha * BC_psh) where F2_dist is the normalized recovery-distance contribution and BC_psh is the capacity-weighted betweenness centrality of pumped-storage buses

## Constraints
1. **Connectivity**: All key buses must belong to the same connected component
2. **N-1 Connectivity**: Edge connectivity >= 2 between every pair (v in V_core, u in V_psh)
3. **Power Flow Safety**: Line flows and bus angle differences must stay within limits under both generation and pumping scenarios

## Output
Pareto-optimal set of backbone-grid configurations trading off economic cost (F1) and resilience (F2)

## Key Challenge
The problem is a high-dimensional, discrete, and heavily constrained multi-objective combinatorial optimization problem. Traditional mathematical programming suffers from combinatorial explosion, and standard evolutionary algorithms struggle with the rigid connectivity and N-1 constraints.
