# Claims

## C01: FDB selection pressure inside a metaheuristic's position updates suppresses premature convergence and raises solution quality on high-dimensional multimodal search
- **Statement**: Replacing a candidate's own coordinate with a fitness-distance-balanced candidate at a position-update step re-aims the search toward under-explored regions, so the operator counteracts local-optimum trapping and improves the accuracy and robustness of the base optimizer across problem dimensions and population sizes.
- **Conditions**: Bound-constrained single-objective benchmark functions (CEC2020 dims 5–100; CEC2022 dims 10, 20; population sizes 30/50/100); the base optimizer is COA. Untested boundary: multi-objective or constrained-native problems, and other base optimizers beyond COA within this paper.
- **Sources**: ["FDB variants outrank base COA on mean Friedman score ← evidence/tables/table4.md «COA … 2.927998 4 | FDBCOA1 … 2.165434 1 | FDBCOA2 … 2.247728 2 | FDBCOA3 … 2.658841 3» [result]", "58.86% ← evidence/tables/table5.md / §III-B (p.35077) «win rate 58.86%, draw 39.01%, loss 2.13%» [result]"]
- **Status**: supported
- **Falsification criteria**: If, on the same benchmark suites, COA equalled or outranked all three FDB variants on mean Friedman score, or if Wilcoxon showed no net win advantage of the FDB variants over COA, the mechanism would be refuted.
- **Proof**: [E01, E02, E05]
- **Evidence basis**: Tables 2–4 (Friedman: all FDB variants rank above COA, COA rank 4/last), Tables 5–6 (Wilcoxon +/=/- vs COA), Table 7 (scalability), Figures 1–3 (radar/convergence/boxplots).
- **Tags**: fitness-distance-balance, premature-convergence, exploration-exploitation

## C02: The location of FDB injection inside the search operators sets the exploration/exploitation trade-off — steering the exploration update helps most, steering the exploitation update hurts scalability
- **Statement**: Applying the fitness-distance-balanced selection to the exploration-phase (tree-climbing) update yields the best joint accuracy-and-scalability profile, whereas pushing the same selection pressure into the second (ground/escape) update over-constrains diversity and degrades large-dimension scalability; i.e. selection pressure is beneficial where the algorithm should diversify and harmful where it should refine.
- **Conditions**: The three placement variants defined in Table 1 (FDBCOA1 = FDB in Eq. 17; FDBCOA2/FDBCOA3 = FDB in the Eq. 19 ground update); CEC2020/CEC2022 suites, dims up to 100. Untested boundary: intermediate/hybrid placements and placement in the exploitation Eq. 22 update were not evaluated.
- **Sources**: ["FDBCOA1 best mean rank, FDBCOA3 worst among FDB variants ← evidence/tables/table4.md «FDBCOA1 … 1 … FDBCOA3 … 3» [result]", "FDBCOA3 scalability weakest ← evidence/tables/table7.md «F1 Mean … FDBCOA3 9.11×10^10» [result]"]
- **Status**: supported
- **Falsification criteria**: If a placement of FDB in the exploitation/ground update (FDBCOA2 or FDBCOA3) had matched or beaten FDBCOA1 on both mean Friedman rank and the D=20→D=50 scalability trend, the placement-dependence mechanism would be refuted.
- **Proof**: [E01, E02]
- **Evidence basis**: Table 1 (variant definitions), Tables 2–4 (FDBCOA1 rank 1, FDBCOA2 rank 2, FDBCOA3 rank 3, COA 4), Table 7 (FDBCOA1 lowest/most-controlled std as D grows; FDBCOA3 "severe scalability problems").
- **Dependencies**: C01
- **Tags**: operator-placement, scalability, ablation

## C03: Elite-guided opposition seeding of the initial population is the most effective opposition scheme because it derives opposites from the best incumbents
- **Statement**: Generating the opposition population from the elite (best) individuals rather than from arbitrary or purely random candidates concentrates the added diversity near promising regions, so it balances exploration and exploitation better than the other opposition schemes and gives the enhanced optimizer its most effective initialization; opposition seeding in general accelerates convergence and widens search coverage versus no opposition seeding.
- **Conditions**: Eight OBL schemes (Classical/Quasi-Reflection/Quasi/Super/Elite/Random/Dynamic/Probabilistic) seeding the FDBCOA1 initial population only (not the search phases); CEC2020/CEC2022 suites. Untested boundary: applying OBL during local/global search phases (named as future work), and OBL on base COA without FDB.
- **Sources**: ["Elite OBL (OBL5) best mean Friedman rank ← evidence/tables/table10.md «FDBCOA1-OBL5 … 5.17927750 | 1» [result]", "64.54% ← evidence/tables/table11.md / §III-C «64.54% win, 34.04% draw, 1.42% loss» [result]"]
- **Status**: supported
- **Falsification criteria**: If a non-elite OBL scheme (e.g. Random or Dynamic OBL) had achieved the best mean Friedman rank and highest Wilcoxon win rate, or if the OBL-seeded variants failed to outperform FDBCOA1-without-OBL, the elite-opposition mechanism would be refuted.
- **Proof**: [E03, E04, E05]
- **Evidence basis**: Tables 8–10 (FDBCOA1-OBL5 mean rank 1; FDBCOA1-without-OBL ranked 7th of 10), Tables 11–12 (Wilcoxon), Table 13 (scalability), Figures 4–6.
- **Dependencies**: C01, C02
- **Tags**: opposition-based-learning, elite-OBL, initialization, diversity

## C04: The two enhancements compose into a TNEP solver that reaches literature-optimal costs on tractable systems and competitive costs on a large dynamic system
- **Statement**: An optimizer carrying both the exploration-placed FDB selection and elite-opposition seeding converges to the known-optimal line-addition plan on small/medium static planning instances and to a low-cost multistage plan on a large dynamic instance, demonstrating that benchmark-derived operator choices transfer to a discrete, penalized, DC-power-flow planning objective.
- **Conditions**: Garver 6-bus and IEEE 25-bus (static, with/without generation resizing) and Colombian 93-bus (dynamic, 3 stages 2002–2012, I=10%); DC power flow via MATPOWER 6.0; 51 runs; penalty-weighted fitness. Untested boundary: AC power flow, N-1 security, and stochastic demand/renewables are not modeled.
- **Sources**: ["US$ 200,000 Garver optimal ← evidence/tables/table14.md «Best (US$) 200000» [result]", "US$ 111,466,000 IEEE-25 ← evidence/tables/table16.md «Best, 10^3 (US$) 111466» [result]", "US$ 497157143.3 Colombian total ← §IV «The total investment cost determined for the DTNEP problem of the Colombian 93-bus test system using the FDBCOA-OBL5 algorithm is US$ 497157143.3» [result]"]
- **Status**: supported
- **Falsification criteria**: If FDBCOA1-OBL5 failed to reach the documented optimal (US$200,000 Garver without resizing; US$110,000 with resizing) or produced a higher-cost/ infeasible plan than the compared literature methods on the same systems, the transfer claim would be refuted.
- **Proof**: [E06, E07, E08]
- **Evidence basis**: Tables 14–19 (cost comparisons vs SS, GAPSO, PLPSO, DEA, GBMO, MOX, CGA, HGA, EGA), Figures 8–15 (convergence curves + line diagrams).
- **Dependencies**: C01, C02, C03
- **Tags**: TNEP, static, dynamic-multistage, investment-cost, transfer

## C05: Benchmark-fitness advantage converts into reliable feasible-solution generation on constrained planning problems, not merely lower average error
- **Statement**: On constrained, penalty-shaped TNEP instances the enhanced optimizer produces feasible solutions across independent runs far more consistently than the base and other classic metaheuristics, showing that its exploration/exploitation balance yields stability (repeatable feasibility) — a distinct and practically decisive property beyond winning a fitness leaderboard.
- **Conditions**: Seven TNEP case studies (Garver ±resizing, IEEE-25 ±resizing, Colombian P1/P2/P3), 30 independent runs, stability metrics SR%/MIT/MST; compared against COA, FDBCOA1, GA, PSO. Untested boundary: success rate depends on the penalty weights and feasibility definition used; other constrained domains untested.
- **Sources**: ["SR% mean 74.2857 vs COA 4.2857 ← evidence/tables/table20.md «FDBCOA1-OBL5 74.2857 41.3564 18.9785 … COA 4.2857 2.1428 1.1336» [result]", "7 of 7 feasible scenarios ← §IV-B «generates practical solutions for 7 out of 7 test scenarios, while FDBCOA1 and PSO produce feasible results only for three scenarios» [result]"]
- **Status**: supported
- **Falsification criteria**: If a competing algorithm (COA/FDBCOA1/GA/PSO) matched or exceeded FDBCOA1-OBL5's mean success rate across the seven case studies, or if FDBCOA1-OBL5 failed to produce feasible solutions in a majority of the case studies, the stability-advantage claim would be refuted.
- **Proof**: [E09]
- **Evidence basis**: Table 20 (SR%/MIT/MST per case + means), Table 21 (min/mean/max/median/std costs).
- **Dependencies**: C04
- **Tags**: stability, success-rate, feasibility, real-world

## C06: No metaheuristic dominates universally — the enhanced variants still lose on a minority of problems, concentrated at low dimensions and large populations
- **Statement**: Consistent with the No Free Lunch principle, adding FDB/OBL structure buys a large but non-total advantage: the enhanced variants tie or lose on a residual set of problems, and the losses/ties concentrate at the largest population size and lowest dimensions, indicating the enhancements trade some performance on those regimes for gains elsewhere.
- **Conditions**: CEC2020/CEC2022 Wilcoxon pairwise vs COA across dims and pop sizes 30/50/100; the residual losses cluster at P=100 and Dim=5. Untested boundary: the precise problems lost are suite-specific.
- **Sources**: ["lost 6, tied 110, won 166 (FDBCOA1) ← §III-B «the FDBCOA1 algorithm lost 6 out of 282 problems across population sizes of 30, 50, and 100, drew 110 problems, and won 166 problems» [result]", "loss 2.13% / 1.42% ← §III-B/§III-C «a loss rate of 2.13%» / «1.42% loss percentage» [result]"]
- **Status**: supported
- **Falsification criteria**: If Wilcoxon showed zero losses/ties for the enhanced variants across all 282 problems (universal domination), the NFL-bounded claim would be refuted.
- **Proof**: [E01, E03]
- **Evidence basis**: Tables 5–6 and 11–12 (per-cell +/=/- showing losses e.g. FDBCOA1 2/5/3 at P=100 Dim=5; §III-B/§III-C aggregate win/draw/loss rates), §III NFL discussion [62].
- **Dependencies**: C01, C03
- **Tags**: no-free-lunch, honesty, limits

## C07: Among the FDB variants, raw accuracy and stability are separable axes — the base is accurate-but-unstable while a well-placed operator delivers balance
- **Statement**: The comparison across COA and its FDB variants reveals that highest average accuracy (base COA in low dimensions) coincides with the highest variance, whereas the best-placed variant trades a little peak accuracy for markedly lower and more controlled variance as dimensionality grows; performance and stability are therefore distinct design targets that a selection operator can rebalance.
- **Conditions**: Scalability comparison D=20→D=50, functions F1–F10, P=100. Untested boundary: only two dimension points define the scalability trend.
- **Sources**: ["COA highest mean but highest std on F1 ← evidence/tables/table7.md «F1 Mean COA 1.0096×10^11 Std 9.82814×10^9 … FDBCOA1 Mean 6.41×10^10 Std 9.95×10^9» [result]"]
- **Status**: supported
- **Falsification criteria**: If base COA had shown both the highest average performance and the lowest standard deviation as dimension increased, the accuracy-vs-stability separation would be refuted.
- **Proof**: [E02]
- **Evidence basis**: Table 7 (mean and std per function at D=20 and D=50), §III-B narrative ("high variance … coefficient of variation rose sharply").
- **Dependencies**: C01, C02
- **Tags**: variance, scalability, stability, coefficient-of-variation

## C08: Generation re-planning (resizing) coupled to line planning changes the optimal expansion plan and lowers investment cost
- **Statement**: Allowing generator output to be re-optimized jointly with line additions expands the feasible decision space so the planner reaches a cheaper line-addition plan than fixed-generation planning, showing that generation and transmission decisions are economically coupled in TNEP.
- **Conditions**: Garver 6-bus (fixed: US$200,000, 9 params; resizing: US$110,000, 11 params) and IEEE 25-bus (fixed 36 params; resizing 46 params). Untested boundary: coupling demonstrated on these two static systems only.
- **Sources**: ["Garver 200000 vs 110000 ← evidence/tables/table14.md «Best (US$) 200000» and evidence/tables/table15.md «Best (US$) 110000» [result]", "IEEE-25 111466 vs 9780 (×10^3) ← evidence/tables/table16.md «Best, 10^3 (US$) 111466» and evidence/tables/table17.md «Best, 10^3 (US$) 9780» [result]"]
- **Status**: supported
- **Falsification criteria**: If enabling generation resizing produced an equal or higher optimal investment cost than fixed-generation planning on the same system, the coupling/cost-reduction claim would be refuted.
- **Proof**: [E06, E07]
- **Evidence basis**: Tables 14 vs 15 (Garver), Tables 16 vs 17 (IEEE-25); Fig. 8 vs 9, Fig. 11 vs 12 convergence curves.
- **Tags**: generation-resizing, transmission-generation-coupling, investment-cost
