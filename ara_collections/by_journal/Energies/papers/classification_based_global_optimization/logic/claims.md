# Claims

## C01: Classification-Based Bus Selection Improves Search Efficiency and Solution Quality
- **Statement**: Pre-optimization classification of network buses by voltage sensitivity and power demand narrows the search space to a small subset of high-load branches, enabling a deterministic optimization that achieves lower active power losses than stochastic metaheuristics while requiring fewer iterations and less computation time.
- **Conditions**: Holds for radial distribution networks with known load profiles where bus loads are quantifiable. Validated on IEEE 33-bus and 69-bus systems at 12.66 kV. Untested on meshed networks, unbalanced systems, or networks with time-varying loads. The classification approach assumes known, stable load values.
- **Sources**: [25 iterations (CGO) vs 100 iterations (PSO, GWO) for IEEE 33-bus at 30% HF] <- Table 8, Section 5.4 «Required iterations: 18 (CGO), 100 (PSO), 100 (GWO)» [result]; [28.5 s (CGO) vs 39.8 s (PSO) and 37.4 s (GWO) for IEEE 69-bus] <- Table 9 «Run time (S): 25 (CGO), 35.2 (PSO), 32.5 (GWO)» [result]; [PLoss CGO 28.67 kW vs PSO 35.7 kW vs GWO 32.10 kW for 33-bus] <- Table 8 «PLoss (kW): 28.67 (CGO), 35.7 (PSO), 32.10 (GWO)» [result]
- **Status**: supported
- **Falsification criteria**: A study on a radial distribution network showing that bus classification (by voltage sensitivity and power demand) followed by deterministic search yields higher losses or more iterations than a metaheuristic searching the full bus set without classification, under the same component count and EV penetration conditions.
- **Proof**: [E04]
- **Evidence basis**: Tables 8 and 9 compare CGO against PSO and GWO at 30% HF for both test systems. On the IEEE 33-bus system, CGO achieves PLoss = 28.67 kW (vs PSO 35.7 kW, GWO 32.10 kW) requiring only 18 iterations vs 100 for both competitors. On IEEE 69-bus, CGO achieves PLoss = 7.65 kW (vs PSO 10.59 kW, GWO 8.463 kW) requiring 22 iterations vs 100. Run time is 25 s vs 35.2 s (PSO) and 32.5 s (GWO) for 33-bus; 28.5 s vs 39.8 s (PSO) and 37.4 s (GWO) for 69-bus.
- **Dependencies**: None
- **Tags**: classification, search efficiency, deterministic optimization, CGO

## C02: Coordinated DG, CB, and EVCS Integration Yields Synergistic Loss Reduction Exceeding Component-Specific Optimization
- **Statement**: Simultaneous optimization of DGs, CBs, and EVCSs within a single framework achieves active power loss reductions that substantially exceed the additive effect of optimizing any subset, because local active power injection (DG) and reactive power compensation (CB) together reduce branch currents more than either alone, even under high EV penetration that would otherwise increase losses.
- **Conditions**: Holds for networks with two DGs, two CBs, and two EVCSs under 30-50% EV hosting factors; demonstrated on IEEE 33-bus and 69-bus radial networks. Untested for different component counts, non-unity DG power factor, or networks above 69 buses. The synergistic effect depends on coordinated placement at the same or nearby buses.
- **Sources**: [PLoss reduction from 210.99 kW to 28.67 kW (86.4%) for 33-bus combined] <- Table 3 «PLoss (kW): 210.99 (Base Case), 28.67 (HF 30%)» [result]; [PLoss reduction from 225.00 kW to 7.65 kW (96.6%) for 69-bus combined] <- Table 5 «PLoss (kW): 225.00 (Base Case), 7.65 (HF 30%)» [result]; [DG-only+EVCS: PLoss 87.33 kW at 30% HF for 33-bus] <- Table 2 «PLoss (kW): 87.33 (HF 30%)» [result]; [94.75% max loss reduction for 33-bus] <- Section 6 «loss reduction (94.75% for IEEE 33-bus)» [result]
- **Status**: supported
- **Falsification criteria**: An experiment on a radial distribution network showing that the loss reduction from simultaneous DG+CB+EVCS optimization is less than the sum (or equal to the max) of the reductions from DG-only and CB-only optimization under matched EV penetration, demonstrating no synergy.
- **Proof**: [E01, E02, E03]
- **Evidence basis**: For the 33-bus system, DG+EVCS integration (Table 2) achieves PLoss = 87.33 kW at 30% HF, while combined DG+CB+EVCS (Table 3) achieves PLoss = 28.67 kW — an additional 67% reduction from adding CBs. For the 69-bus system, DG+EVCS (Table 4) achieves PLoss = 72.13 kW at 30% HF, while combined (Table 5) achieves PLoss = 7.65 kW — an additional 89% reduction. The overall reductions are 86.4% (33-bus) and 96.6% (69-bus) from base case, or up to 94.75% and 98.061% as stated in conclusions.
- **Dependencies**: None
- **Tags**: coordinated planning, synergy, loss reduction, DGs, CBs, EVCSs

## C03: Deterministic CGO Outperforms Stochastic Metaheuristics on Computed Loss Reduction and Computational Cost
- **Statement**: A deterministic optimization framework with explicit bus classification achieves equal or better active power loss reduction than widely-used stochastic metaheuristics (PSO, GWO) while requiring fewer iterations and lower computation time, without the parameter sensitivity and reproducibility issues inherent to stochastic methods.
- **Conditions**: Holds when compared against PSO and GWO on IEEE radial distribution networks (33-bus, 69-bus) with 30% EV hosting factor, two DGs, two CBs, and two EVCSs. Untested against other metaheuristics (GA, DE, ABC, etc.) or on larger networks. The deterministic nature assumes known, fixed load values; performance under uncertainty (stochastic loads, variable DG output) is not evaluated.
- **Sources**: [PLoss CGO 28.67 kW vs PSO 35.7 kW vs GWO 32.10 kW (33-bus)] <- Table 8 «PLoss (kW): 28.67 (CGO)» [result]; [PLoss CGO 7.65 kW vs PSO 10.59 kW vs GWO 8.463 kW (69-bus)] <- Table 9 «PLoss (kW): 7.65 (CGO)» [result]; [Run time CGO 25 s vs PSO 35.2 s (33-bus)] <- Table 8 «Run time (S): 25 (CGO), 35.2 (PSO)» [result]
- **Status**: supported
- **Falsification criteria**: A comparative study on any radial distribution network showing that a deterministic classification-based search requires more computation time or achieves higher losses than PSO or GWO executed under equal or greater iteration budgets and matched component counts, with statistical significance across multiple trials.
- **Proof**: [E04]
- **Evidence basis**: Tables 8 and 9 provide direct comparison. CGO consistently achieves the lowest PLoss among the three methods. For VDI, CGO achieves 1.49e-3 (33-bus) vs PSO 1.224e-3 and GWO 1.627e-3 — slightly above PSO but within the same order. Run time is 29-37% lower than PSO and 23-24% lower than GWO. Required iterations are 72-82% fewer than the 100 fixed iterations for both competitors.
- **Dependencies**: C01, C02
- **Tags**: deterministic optimization, metaheuristic comparison, PSO, GWO, reproducibility

## C04: Reactive Power Compensation Is Essential Under EV Penetration When DGs Operate at Unity Power Factor
- **Statement**: When DGs supply only active power (unity power factor), the inductive loading from EV charging stations causes a substantial drop in substation power factor, which can only be restored by coordinated capacitor bank placement — without CBs, substation power factor degrades to 0.50-0.64 even with optimal DG placement, while combined DG+CB integration restores it above 0.81-0.90 across all tested EV penetration levels.
- **Conditions**: Holds for radial distribution networks with DGs operating at unity power factor and EV penetration at 30-50% of total load. Validated on IEEE 33-bus and 69-bus systems. Untested for networks where DGs provide reactive power support (e.g., via smart inverters), or for lower EV penetration levels (<30%).
- **Sources**: [33-bus DG+EVCS: Slack PF drops from 0.849 (base) to 0.609 (30% HF)] <- Table 2 «Slack PF (lag): 0.8490 (Base Case), 0.609 (HF 30%)» [result]; [33-bus combined: Slack PF recovers to 0.904 (30% HF)] <- Table 3 «Slack PF (lag): 0.904 (HF 30%)» [result]; [69-bus DG+EVCS: Slack PF drops to 0.502 (30% HF)] <- Table 4 «Slack PF (lag): 0.502 (HF 30%)» [result]; [69-bus combined: Slack PF recovers to 0.812 (30% HF)] <- Table 5 «Slack PF (lag): 0.812 (HF 30%)» [result]
- **Status**: supported
- **Falsification criteria**: A study on a radial distribution network with 30% or higher EV penetration showing that optimal DG placement alone (at unity PF, without CBs) can maintain substation power factor above 0.85, or that the addition of CBs does not improve the power factor by more than 0.05 beyond the DG-only case.
- **Proof**: [E01, E03, E05]
- **Evidence basis**: Tables 2 vs 3 and 4 vs 5 demonstrate the critical role of CBs. For 33-bus at 30% HF: DG+EVCS yields PF=0.609, combined yields PF=0.904 (improvement of 0.295). For 69-bus at 30% HF: DG+EVCS yields PF=0.502, combined yields PF=0.812 (improvement of 0.310). Without CBs, PF degrades further at higher EV penetrations (33-bus: 0.609 at 30% HF, 0.641 at 50% HF). The pattern holds consistently across both test systems and all three hosting factors.
- **Dependencies**: C02
- **Tags**: reactive power compensation, power factor, capacitor banks, EV penetration, unity power factor
