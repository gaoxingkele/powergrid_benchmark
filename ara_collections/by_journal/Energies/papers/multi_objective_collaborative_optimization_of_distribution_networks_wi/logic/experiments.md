# Experiments

## Experiment 1: Comparison between Improved NSGA-II and PSO
**Setup**: IEEE 33-bus distribution system. Crossover and mutation factors = 0.8, population size = 250, maximum generations = 100. Penalty factors: w1,w2,w3 = 6.0e-3; w4,w5 = 1.0e-3; w6,w7 = 7.0e-3; w8 = 1.0e-3.
**Baseline/comparator**: PSO algorithm applied to same test system.
**Metrics**: Convergence generations, investment cost (Fm), expected load loss (Em), network loss (Floss).
**Key results**: Improved NSGA-II converges in 40 generations vs. PSO 75; Fm = 167 vs. 190; Em = 51 vs. 65; Floss = 2.5 vs. 3.1 (all in 10^-4 yuan).
**Evidence**: Table 3, Figure 4

## Experiment 2: Comparison between Improved NSGA-II and Standard NSGA-II
**Setup**: Same IEEE 33-bus system and parameters as Experiment 1.
**Baseline/comparator**: Standard NSGA-II algorithm.
**Metrics**: Convergence generations, Fm, Em, Floss.
**Key results**: Improved NSGA-II converges in 40 generations vs. standard NSGA-II 60; improved version provides lower investment cost, lower expected loss, and reduced network loss.
**Evidence**: Section 5.2(1), paragraph 4

## Experiment 3: Comparison of Four Power-Supply Schemes
**Setup**: IEEE 33-bus system with four schemes: (1) DG direct to grid; (2) ES + dispatchable EVs only; (3) Em prioritized; (4) multi-objective coordinated optimization.
**Metrics**: Distribution network capacity, Fm, Em, Floss.
**Key results**: Scheme 4 achieves lowest network capacity (1.1501 MW), intermediate Fm (167), intermediate Em (51), and lowest Floss (2.5). Scheme 1 has lowest Fm (80) but highest Em (100).
**Evidence**: Table 4

## Experiment 4: Energy Storage Cost Sensitivity
**Setup**: IEEE 33-bus system, varying ES cost from 110 to 130 million yuan/MW.
**Metrics**: ES placement and quantity, on-net load/DG capacity, off-net load/DG capacity.
**Key results**: ES configuration decreases from 0.2468 MW (at 110) to 0.1998 MW (at 130). On-net load decreases from 0.7901 to 0.5812 MW. Off-net load increases from 0.2097 to 0.4197 MW.
**Evidence**: Table 5, Figures 5 and 6

## Experiment 5: Post-Evaluation Sensitivity Analysis
**Setup**: Fixed optimal configuration from Table 2, varying operating conditions: S0 (baseline), S1 (cloudy PV), S2 (winter PV), S3 (high wind), S4 (low wind), S5 (fixed-period ES), S6 (real-time ES).
**Metrics**: Finv (fixed at 1175e4 CNY), Em, Floss.
**Key results**: Em ranges from 48.0 (S3, high wind) to 61.0 (S4, low wind). Floss ranges from 2.30 (S3) to 3.20 (S4). Real-time ES (S6) outperforms fixed-period (S5).
**Evidence**: Table 6

## Experiment 6: Re-Optimization Sensitivity (ES Access Location)
**Setup**: IEEE 33-bus system, varying ES access location: Bus 10 (trunk), Bus 16 (end), Bus 6 (mid).
**Metrics**: ES/MW, PV/MW, WT/MW, Finv, Em, Floss.
**Key results**: Trunk access (Bus 10) yields lowest ES size (0.200 MW), Finv (1175e4), Em (51.0), and Floss (2.50). End access (Bus 16) yields highest values across all metrics.
**Evidence**: Table 7
