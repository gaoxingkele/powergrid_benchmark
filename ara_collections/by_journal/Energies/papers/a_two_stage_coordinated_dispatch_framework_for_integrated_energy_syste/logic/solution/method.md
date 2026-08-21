# Method: Two-Stage Coordinated Dispatch Framework

## Overview

The proposed framework is organized as two sequentially coupled decision stages sharing the same 24 h day-ahead horizon at hourly resolution, assembled and solved as a single MILP instance.

## Stage 1: Retail Pricing and Demand Shaping

The IESO determines the TOU retail price vector (peak, flat, valley blocks) subject to market-stability constraints:
- Tariff ordering (valley < flat < peak)
- Peak-to-valley ratio bounds (γ ∈ [2, 5])
- Per-block tariff limits

Through the cross-price elasticity matrix (Eq. 4), this price vector yields price-responsive load:
- Fixed load (Eq. 5)
- Shiftable load with daily energy conservation (Eqs. 6–8)
- Interruptible load with max curtailment (Eqs. 9–10)

The post-PDR total load (Eq. 11) is passed as boundary condition to Stage 2.

## Stage 2: Security-Constrained Dispatch

Given the reshaped load, the operator co-optimizes:
- Conventional and gas-fired units (quadratic cost, capacity, ramping, UC constraints)
- CHP units and P2G plants (with curtailed-wind coupling)
- EESS (with LCOE degradation cost, SOC tracking, cycle limits)
- Bidirectional V2G fleet (stochastic mobility, charge/discharge exclusivity)
- Coupled electricity–gas network constraints (DistFlow, Weymouth PWL)

The objective minimizes total cost = upstream procurement (C1) + equipment O&M (C2) + EESS lifecycle depreciation (C3).

## Single-Instance Assembly

The two stages share the same day-ahead time scale and are assembled as a single MILP/MISOCP rather than an iterative master–subproblem decomposition. This preserves global optimality while retaining the conceptual two-stage decision logic. The second stage plays the role of the recourse-like dispatch layer that realizes the price decision.

## Case Study Design

Three comparative scenarios:
- Case 1 (Baseline): No PDR, no V2G
- Case 2 (PDR Only): PDR active, V2G unidirectional charging only
- Case 3 (Coordinated): PDR + bidirectional V2G

Ablation study removes individual mechanisms from Case 3 to isolate marginal contributions.
