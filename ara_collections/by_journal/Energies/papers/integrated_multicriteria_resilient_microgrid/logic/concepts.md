# Concepts: Integrated Multi-Criteria Planning for Resilient VRE-Based Microgrid

## 1. SSAP VP-CPP DRP (Shortage/Surplus Adaptive Pricing with Variable Peak Critical Peak Pricing Demand Response Program)

A hybrid demand response mechanism with two operating modes. In non-critical mode, electricity prices adjust dynamically based on the magnitude of power imbalance between VRE generation and load demand: when generation exceeds demand, prices decrease (proportionally to surplus) to encourage consumption; when demand exceeds generation, prices increase (proportionally to shortage) to discourage consumption. In critical mode (SOC below critical threshold AND total VRE generation at or near zero), an extreme high price is enforced to curtail non-essential load and prevent system collapse. The pricing equation (Equation 12 in the paper) defines three regimes: critical price, surplus-responsive price, and shortage-responsive price, with the baseline reference price being 15.80 US cents/kWh and bounds of 50%-200% of reference.

## 2. DPSP (Deficiency of Power Supply Probability)

A reliability metric defined as the ratio of total curtailed (unserved) load demand to total load demand over the entire operational planning period (8760 hours). DPSP = sum(S_curtailed_load) / sum(S_load) * 100%. A lower DPSP indicates higher reliability. The objective is to minimize DPSP alongside TLCC and LPPP. In the results, DPSP values range from 0.00% (perfect reliability) to 3.52% (compromised reliability for cost savings). This metric directly corresponds to loss of load expectation in traditional power system reliability analysis.

## 3. LPPP (Loss of Produced Power Probability)

A VRE utilization efficiency metric defined as the proportion of total curtailed/wasted VRE power to the total power that all VRE sources could potentially generate over the entire operation period. LPPP = sum(S_curtailed_VRE) / sum(S_total_VRE) * 100%. A high LPPP indicates substantial waste of renewable energy potential due to BESS saturation, demand-supply mismatches, or operational constraints. This metric captures the environmental and efficiency dimension of the multi-objective optimization, complementing the economic (TLCC) and reliability (DPSP) perspectives.

## 4. TOPSIS (Technique for Order Preference by Similarity to Ideal Solution)

A multi-criteria decision-making method used as the ranking mechanism after MOPSO generates the Pareto front of non-dominated solutions. TOPSIS identifies the best compromise solution as the one closest to the positive-ideal solution (best values across all objectives) and farthest from the negative-ideal solution (worst values). The procedure involves: normalizing the decision matrix (Equation 19), computing weighted normalized values (Equation 20), determining positive/negative ideal solutions (Equations 21-22), calculating Euclidean distances (Equations 23-24), and computing relative closeness scores (Equation 25). This converts the 3D Pareto front into a ranked list of alternatives.

## 5. Flexible Demand Resource (FDR)

A category of electrical load that can be adjusted in response to price signals, comprising elastic loads (shiftable operation times, e.g., dishwashers, water pumps) and adjustable inelastic loads (e.g., HVAC systems). FDR capacity is bounded at +/-10% of total system load at any given time. FDRs are distinct from curtailable loads (which are only used in emergencies). The FDR model uses price elasticity coefficients (self-elasticity and cross-elasticity) to determine load response to price changes. This concept enables demand-side flexibility without compromising essential load service.

## 6. MOPSO (Multi-Objective Particle Swarm Optimization)

A swarm intelligence algorithm adapted for multi-objective optimization, inspired by natural swarm behaviors. Each particle represents a candidate solution with position (decision variables: PV, WT, BESS capacities) and velocity vectors. The algorithm maintains a repository of non-dominated solutions and applies mutation (similar to NSGA-II) for diversity. The velocity update equation considers personal best (Pbest) and global best (Gbest) positions with inertia weight w that decreases linearly with iterations. MOPSO generates the Pareto front of optimal trade-off solutions for the three conflicting objectives (TLCC, DPSP, LPPP).

## 7. LSTM (Long Short-Term Memory) Forecasting

A recurrent neural network architecture designed for sequence-to-sequence time series prediction, featuring cell state and three gating mechanisms (forget, input, output gates) that control information flow. Used in this paper for one-hour-ahead point forecasting of solar irradiance, wind speed, and load demand. The gates (Equations 15-18) enable the network to retain long-term dependencies while avoiding vanishing gradient problems. Forecast accuracy (measured by MAE) is used both for operational DRP activation and as the basis for MCS uncertainty scenario generation within +/-25% of the MAE range.
