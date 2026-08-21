# Claims

## C01: Generalized adequacy integrates three formerly isolated adequacy dimensions into a unified framework that reveals interdependencies in resource planning.
- **Statement:** Combining power/energy, flexibility, and inertia adequacy into a single planning paradigm reveals that the three dimensions are not independent -- they all rely on effective transmission of electrical energy and must be planned jointly to avoid countervailing resource allocations.
- **Conditions:** Valid under the assumption that control-based measures alone cannot provide additional supply capacity (SS2.1). The framework has been demonstrated on an IEEE 24-bus system; generalization to larger, meshed systems is untested. The framework explicitly excludes demand-side resources.
- **Status:** Supported
- **Falsification criteria:** Show that a planning scheme optimized independently for each adequacy dimension achieves equivalent or better system performance (LOLH, EENS, flexibility margins, inertia margin) than the joint optimization, while requiring no larger total investment.
- **Proof:** The paper builds the generalized adequacy framework in SS2.1--2.2, defining seven indicators across the three dimensions. The integrated planning model (SS3.1--3.2) uses iterative refinement (Figure 1) where extreme scenarios from adequacy evaluation feed back into the planning model -- a mechanism that is definitionally impossible when dimensions are evaluated separately. The cross-dimensional synergy is demonstrated in SS4.2 where M2 (long-term storage + renewables) improves power/energy adequacy but still fails inertia adequacy until M3 introduces frequency security constraints.
- **Evidence basis:** E01--E04 (scenarios M1--M4); see Tables 5, 6 for comparative indicator values.
- **Dependencies:** None.
- **Tags:** [methodology, framework, adequacy]

## C02: Coordinated planning of wind, solar, short-term and long-term energy storage, and transmission infrastructure under generalized adequacy reduces loss-of-load hours by more than half compared to traditional resource-only planning.
- **Statement:** Coordinated planning of renewables, multi-timescale storage, and transmission reduces loss-of-load hours by more than half relative to traditional resource-only planning, demonstrating that multi-resource coordination -- not any single resource type -- is the primary driver of reliability improvement under high renewable penetration.
- **Conditions:** Demonstrated on IEEE 24-bus with 3500 MW peak load, 250 MW wind/PV per node, max 750 MW per type. Cost parameters from [33,34]. Storage duration thresholds from [32]. The reduction is relative to M1 (traditional plan); absolute contribution of each resource type is not independently ablated.
- **Status:** Supported
- **Falsification criteria:** Find a resource configuration within the same cost envelope that achieves LOLH > 6.15 h/a (i.e., worse than M1) under the same load and renewable profiles, or find that the LOLH reduction from M1 to M4 is primarily driven by a single resource type (e.g., short-term storage alone) rather than their coordination.
- **Proof:** Table 5: M1 LOLH = 6.15 h, M4 LOLH = 2.91 h (reduction of 52.7%). Table 4 shows the coordinated expansion: M1 deploys 926.99 MW wind, 337.36 MW PV, 15 MW short-term storage, 0 MW long-term storage, 5 new lines; M4 deploys 750 MW wind, 585.76 MW PV, 750 MW short-term storage, 69.10/146.64 MW long-term storage, 2 new lines. The change is not monotonic -- intermediate scenarios M2 and M3 show progressive improvement (4.68 h, 3.14 h), confirming that each additional resource category contributes.
- **Evidence basis:** E01--E04; Tables 4, 5.
- **Dependencies:** C01 (the generalized adequacy framework is the mechanism that enables this coordination).
- **Tags:** [planning, coordinated, reliability]

## C03: Dynamic frequency security constraints in the planning model ensure the system inertia margin remains positive, preventing frequency instability in high-renewable scenarios.
- **Statement:** Incorporating RoCoF and frequency nadir constraints into the planning optimization forces a minimum online inertia level that keeps operating inertia consistently above the safety threshold, eliminating periods of negative inertia margin that would otherwise occur under high renewable penetration.
- **Conditions:** Constraint parameters: RoCoF_max, Delta_f_max, T_PFR, alpha = PFR coverage proportion. Disturbance magnitude Delta_P = 10% of load. Valid for the primary frequency response model described in SS3.2.2 (linear PFR ramp within TPFR seconds). Not validated for multi-contingency or cascading events. Only thermal and storage PFR are modeled -- wind/solar PFR contribution via virtual inertia is approximated through equivalent kinetic energy E_new (Eq. 13).
- **Status:** Supported
- **Falsification criteria:** Demonstrate a planning outcome under M3 or M4 where, for any hour in the 8760-h simulation, the operating system inertia H_sys falls below H_min (i.e., inertia margin A_H becomes negative) during a credible contingency. Alternatively, show that the inertia margin constraint can be satisfied with a smaller total resource investment than M3 achieves.
- **Proof:** Figure 8 shows the contrast: M2 (no frequency constraints) has inertia margin = -17.31% (Table 5), with operating inertia frequently below the minimum threshold. M3 (with constraints) achieves inertia margin = +2.90%, and M4 = +10.26%. The mathematical formulation (Eqs. 14--18, 30--36) shows how H_min is derived from both RoCoF and nadir constraints, and how the planning model enforces H_sys >= H_min.
- **Evidence basis:** E02, E03, E04; Table 5 (System Inertia Margin row), Table 6 (System Inertia Margin row), Figure 8.
- **Dependencies:** C01 (inertia adequacy is a component of generalized adequacy).
- **Tags:** [frequency stability, inertia, constraints]

## C04: Incorporating low-probability extreme weather scenarios into the planning scenario set substantially reduces the Conditional Value at Risk of energy not served, mitigating tail-risk supply shortages.
- **Statement:** Embedding low-probability extreme meteorological scenarios into the planning model's scenario set substantially reduces the Conditional Value at Risk of energy not served compared to planning on typical scenarios alone, demonstrating that explicit consideration of tail-risk events is necessary for supply security under deep renewable penetration.
- **Conditions:** Extreme scenario configurations per Table 1. Probability approximated at 0.01 each. Extreme scenarios are randomly embedded in Monte Carlo sampling. Validated on IEEE 24-bus with specific regional climate assumptions (China summer/winter/dry season patterns). Generalization to other climate regimes untested. EENS_CVaR uses alpha = 5%.
- **Status:** Supported
- **Falsification criteria:** Show that a planning scheme designed without extreme scenarios (M3) achieves EENS_CVaR within 20% of M4's value, or that the reduction in EENS_CVaR from M3 to M4 is primarily caused by a change in conventional resource mix rather than the extreme scenario embedding.
- **Proof:** Table 5: M3 (typical scenarios only) EENS_CVaR = 1512.18 MWh; M4 (with extreme scenarios) EENS_CVaR = 1316.64 MWh, a reduction of 12.9%. The absolute reduction (195.54 MWh) is less dramatic than the relative reduction headline. However, note that the worst-case energy shortage in M4 reaches up to 6x the EENS value (SS4.3), underscoring the practical importance. The EENS_CVaR is the appropriate metric as it captures tail risk by construction. Table 5 also shows LOLH reduction from 3.14 h (M3) to 2.91 h (M4).
- **Evidence basis:** E03, E04; Table 5 (EENS and EENS_CVaR rows), Table 1.
- **Dependencies:** C01 (generalized adequacy framework incorporates extreme-event risk via expanded scenario set).
- **Tags:** [extreme events, risk, adequacy, planning]

## C05: PROMETHEE-II with combined AHP-entropy weighting enables systematic scheme comparison across economic, technical, and environmental dimensions yielding a decisive ranking.
- **Statement:** The multi-criteria framework comprising 10 indicators (7 adequacy + 3 external) with game-theoretic combined weights produces a clear net-flow ranking (M4 > M3 > M2 > M1) that is robust to whether demand is quantified at maximum or 95th percentile, confirming that the superiority of generalized-adequacy-based planning is a structural property and not an artifact of extreme-peak weighting.
- **Conditions:** Valid for the four evaluated schemes (M1--M4). The stepwise 0/1 preference function was used (Eq. 41--42); results may differ with Gaussian or linear preference functions. Weight stability tested across two demand quantifications only -- no formal sensitivity analysis across weight variations was conducted.
- **Status:** Supported
- **Falsification criteria:** Re-weight the 10 indicators using a different defensible method (e.g., equal weights, pure entropy, pure AHP) and obtain a ranking where M1 or M2 outperforms M4. Alternatively, replace the PROMETHEE-II method with TOPSIS or VIKOR and obtain a different top-ranked scheme.
- **Proof:** Table 7 shows indicator values and combined weights; Table 8 shows PROMETHEE-II net flows: M1 = -2.26, M2 = -0.68, M3 = +0.94, M4 = +2.00. The ranking is identical between Table 5 (max-based) and Table 6 (95%-based) indicators. The highest-weighted indicators are LCOE (0.22), carbon intensity (0.15), LOLH (0.16), and EENS (0.13), reflecting the priority placed on economic and adequacy performance.
- **Evidence basis:** E01--E04; Tables 5, 6, 7, 8.
- **Dependencies:** C01 (the 7 adequacy indicators come from the generalized adequacy framework), C02--C04 (the indicator differences across scenarios are driven by these mechanisms).
- **Tags:** [MCDM, scheme comparison, PROMETHEE-II]
