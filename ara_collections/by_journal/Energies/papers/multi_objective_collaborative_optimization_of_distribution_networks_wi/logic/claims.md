# Claims

## Claim 1: Improved NSGA-II Converges Faster than PSO
**Statement**: The improved NSGA-II algorithm achieves convergence within approximately 40 generations, while PSO requires about 75 generations on the same IEEE 33-bus test system.
**Evidence**: Table 3; Experiment 1 (Comparison against PSO)
**Proof**: Table 3 reports "Convergence Generations" of 40 for improved NSGA-II versus 75 for PSO. Figure 4 visually confirms the convergence trajectory difference.

## Claim 2: Improved NSGA-II Converges Faster than Standard NSGA-II
**Statement**: The improved NSGA-II achieves convergence within 40 generations, while standard NSGA-II requires about 60 generations.
**Evidence**: Section 5.2(1), paragraph 4
**Proof**: The paper explicitly states "the improved NSGA-II achieves convergence within 40 generations, while the standard NSGA-II requires about 60 generations to reach a similar level of stability."

## Claim 3: Improved NSGA-II Achieves Lower Investment Cost than PSO
**Statement**: The improved NSGA-II obtains a lower investment cost (Fm) of 167e-4 yuan compared to 190e-4 yuan for PSO.
**Evidence**: Table 3
**Proof**: Table 3 column "Fm (10^-4 Yuan)" shows Improved NSGA-II = 167, PSO = 190.

## Claim 4: Improved NSGA-II Achieves Lower Expected Load Loss than PSO
**Statement**: The improved NSGA-II obtains an expected load loss (Em) of 51e-4 yuan compared to 65e-4 yuan for PSO.
**Evidence**: Table 3
**Proof**: Table 3 column "Em (10^-4 Yuan)" shows Improved NSGA-II = 51, PSO = 65.

## Claim 5: Improved NSGA-II Achieves Lower Network Loss than PSO
**Statement**: The improved NSGA-II obtains a network loss (Floss) of 2.5e-4 yuan compared to 3.1e-4 yuan for PSO.
**Evidence**: Table 3
**Proof**: Table 3 column "Floss (10^-4 Yuan)" shows Improved NSGA-II = 2.5, PSO = 3.1.

## Claim 6: Coordinated Optimization (Scheme 4) Reduces Expected Load Loss by ~49%
**Statement**: Scheme 4 (multi-objective coordinated optimization) reduces expected load loss from 100e-4 yuan (Scheme 1) to 51e-4 yuan.
**Evidence**: Table 4
**Proof**: Table 4 shows Scheme 1 Em = 100, Scheme 4 Em = 51.

## Claim 7: Coordinated Optimization (Scheme 4) Reduces Network Loss by ~7.4%
**Statement**: Scheme 4 reduces network losses from 2.7e-4 yuan (Scheme 1) to 2.5e-4 yuan.
**Evidence**: Table 4
**Proof**: Table 4 shows Scheme 1 Floss = 2.7, Scheme 4 Floss = 2.5.

## Claim 8: Energy Storage Costs Exhibit Bidirectional Coupling with Configuration Capacity
**Statement**: A 10% increase in energy storage costs causes synchronized contraction of system configuration capacity and planning scale, forming a bidirectional coupling relationship.
**Evidence**: Table 5; Figures 5 and 6; Section 5.2(2)
**Proof**: Table 5 shows ES configuration at 0.2468 MW (110 million yuan/MW) decreasing to 0.1998 MW (130 million yuan/MW), with corresponding shifts in on-net/off-net load and DG capacity distributions.

## Claim 9: Real-Time ES Strategy Outperforms Fixed-Period Strategy
**Statement**: The real-time ES scheduling strategy reduces Em by approximately 5-6% and Floss by approximately 8% relative to the fixed-period (night-charge/day-discharge) strategy.
**Evidence**: Table 6, scenarios S5 and S6
**Proof**: Table 6 shows S5 (fixed-period) Em = 52.5, Floss = 2.55; S6 (real-time) Em = 49.5, Floss = 2.35.

## Claim 10: Pareto Solution Set Shows Good Diversity and Convergence
**Statement**: The Pareto solution set obtained by improved NSGA-II is relatively evenly and continuously distributed in the target space, covering the trade-off relationships between different objectives.
**Evidence**: Figure 3; Section 5.2(1)
**Proof**: The paper states "the Pareto solution set is relatively evenly and continuously distributed in the target space and can better cover the trade-off relationship between different objectives."

## Claim 11: Feasibility-Priority Mechanism Improves Solution Validity
**Statement**: The improved NSGA-II incorporates a binary feasibility indicator for DER deployment, ensuring only eligible buses (with sufficient area, short-circuit headroom, and connection interfaces) are considered for installation.
**Evidence**: Equations (24); Section 4.1; Section 3.2
**Proof**: Equation (24) formalizes the constraint PDER_i <= delta_feas_i * Pmax_i, where delta_feas_i in {0,1}.

## Claim 12: End-of-Feeder ES Access Requires Larger Capacity and Yields Higher Losses
**Statement**: ES access at the end bus (Bus 16) requires larger ES capacity (0.240 MW) and results in higher Finv (1190e4 yuan) and Floss (2.90e-4 yuan) compared to trunk access (Bus 10, 0.200 MW, 1175e4 yuan, 2.50e-4 yuan).
**Evidence**: Table 7
**Proof**: Table 7 compares ES at Bus 10 (trunk), Bus 16 (end), and Bus 6 (mid), showing monotonic increases in ES size, Finv, Em, and Floss from trunk to end.
