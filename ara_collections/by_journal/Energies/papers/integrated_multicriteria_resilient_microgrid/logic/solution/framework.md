# Framework: Integrated Planning Framework for VRE-Based Community Microgrid

## Overview

The integrated planning framework (Figure 2 in the paper) combines four key components: (1) LSTM-based forecasting, (2) Monte Carlo uncertainty modeling, (3) demand response (SSAP VP-CPP or TOU VP-CPP), and (4) multi-objective optimization (MOPSO-TOPSIS). The framework operates in two modes: deterministic (Cases 1-3) and stochastic (Cases 4-6).

## Operational Modes

### Normal (Non-Critical) Mode
- System is in optimal state when VRE generation equals load demand
- Price remains at previously determined level
- FDRs remain unadjusted
- If imbalance detected, DRP activates price adjustments to incentivize FDR participation
- BESS charging/discharging activated after DRP capacity exhausted

### Critical (Emergency) Mode
- Triggered when SOC <= SOC_critical AND total VRE generation <= 0
- VP-CPP enforces extreme high electricity price (200% of reference)
- Non-essential load curtailment authorized
- Goal: prevent total system collapse while maintaining critical load supply

## Six Simulation Cases

| Case | Type | DRP | Forecasting | Uncertainty |
|------|------|-----|-------------|-------------|
| 1 | Deterministic | None (flat pricing) | No | No |
| 2 | Deterministic | TOU VP-CPP | No | No |
| 3 | Deterministic | SSAP VP-CPP | No | No |
| 4 | Stochastic | None (flat pricing) | No | Yes (MCS) |
| 5 | Stochastic | TOU VP-CPP | Yes (LSTM) | Yes (MCS) |
| 6 | Stochastic | SSAP VP-CPP | Yes (LSTM) | Yes (MCS) |

## Decision Variables
- PV rated capacity (Scp_pv)
- WT rated capacity (Scp_w)
- BESS rated capacity (Scp_b)

## Objective Functions
1. Minimize TLCC (Total Lifecycle Cost) — Equation 26
2. Minimize DPSP (Deficiency of Power Supply Probability) — Equation 27
3. Minimize LPPP (Loss of Produced Power Probability) — Equation 28

## Key Constraints
- Power balance (Equation 29)
- BESS SOC limits (Equation 4)
- BESS charge/discharge power limits (Equation 30)
- FDR capacity limits (Equation 31)
- Electricity price bounds (Equation 32)
- VRE power output limits (Equations 33-34)

## Performance Summary

| Metric | Case 1 | Case 2 | Case 3 | Case 4 | Case 5 | Case 6 |
|--------|--------|--------|--------|--------|--------|--------|
| TLCC (rank 1) | $10.38M | $10.31M | $9.65M | $10.58M | $10.38M | $10.07M |
| DPSP (rank 1) | 0.48% | 0.57% | 0.06% | 0.12% | 0.36% | 0.04% |
| LPPP (rank 1) | 6.26% | 4.35% | 1.33% | 10.31% | 5.05% | 2.05% |
| BESS (rank 1) | 4800 kWh | 4200 kWh | 3500 kWh | 4900 kWh | 3600 kWh | 3200 kWh |

Case 6 (LSTM + SSAP VP-CPP + stochastic) provides the best overall balance of cost, reliability, and VRE utilization under uncertainty.
