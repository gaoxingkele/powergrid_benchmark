# Deep-Revision Claim Contract: SHIELD-MOEA

This contract records the evidence boundary for `mintou_p4_shield_resilience_planning`. It does not replace the manuscript or create new experimental evidence. The controlling sources are the current planning and AC configurations, implementation, run tables, corrected inference table, and manuscript. Deprecated proxy-method runs and the preserved weak-result history are not evidence for the current headline.

## Title-to-Evidence Map

Current title: **SHIELD-MOEA: Scenario Screening with Disjoint Evaluation for Distribution-Network Resilience Planning**.

| Title or contribution phrase | Direct support | Permitted reading | Excluded reading |
|---|---|---|---|
| **SHIELD-MOEA** | `src/powergrid_benchmark/mintou_real_planning.py` implements an NSGA-II-style binary search with GA/DE variation, budget repair, and worst-$K$ scenario screening; the current configuration fixes population 40, 40 generations, 16 search scenarios, $K=4$, and a five-generation screening period. | A named, evaluated optimization pipeline. | Evidence that every named operator is necessary or improves quality. Repair is resolved; hybrid variation and periodic re-screening are not. |
| **Scenario screening** | The full method uses the population's worst four of 16 search scenarios. The no-screening ablation uses all 16. Recorded search-phase plan--scenario calls are 17,920 versus 51,200 under the implemented accounting. | Selective scenario exposure reduces recorded objective calls by 65% in this implementation. | A wall-clock, energy, or deployment-efficiency claim. No mean-HV difference is detected against no screening, and equivalence was not tested. |
| **Disjoint evaluation** | Search scenarios use the fixed search draw and reported scores use a fixed full evaluation draw generated with a different seed. The unseen-stress experiment also uses non-overlapping search and evaluation ranges. | A protocol property preventing direct reuse of search realizations in final scoring. | A causal performance gain from disjoint evaluation; no same-draw versus disjoint-draw ablation estimates such a gain. |
| **Distribution-network resilience planning** | The optimization selects a budget-feasible binary portfolio from 72 SimBench-derived actions. The method-independent p4 objective vector is $(C,\mathbb{E}[L],\mathbb{E}[U],-R,-\mathbb{E}[S])$; the restoration-aware experiment substitutes the prespecified $L^e$ for $L$. | A resilience-framed planning proxy with explicit reliability and survivability coordinates under load, DER, and outage scenarios. | A utility-calibrated investment study, an element-level outage/restoration model, or a power-flow-embedded planning formulation. Costs are synthetic; $R$ and $S$ are engineering proxies. |
| **Electrical validation** | The AC layer maps seed-0 compromise *action-kind counts* from three planning experiments to six networks and six operating scenarios with fixed placement rules, producing 1296 cases. | A qualitative check of whether mapped portfolio compositions remain AC-feasible under the declared cases. | Nodal siting/sizing validation, a seeded replication of proxy comparisons, a causal mechanism estimate, or proof of AC superiority. SHIELD-MOEA reaches 0.685 AC feasibility and trails NSGA-II+Repair at 0.694. |

The paper's resilient-planning identity must therefore remain tied to the fixed proxy problem. The AC layer checks a downstream mapping of compositions; it does not convert the proxy objectives into AC objectives and does not validate restoration, islanding, or general resilience beyond the six-network, six-scenario screen.

## Primary Estimand and Analysis Unit

The primary performance outcome is standard five-dimensional hypervolume of the feasible non-dominated final front under fixed, method-independent normalization bounds and a reference point of 1.1 in each normalized dimension. For stochastic comparisons, the statistical analysis unit is one independently seeded optimizer run within a fixed experiment and method. Each stochastic method has 30 runs in each of eight experiments. The scored object for run $(m,e,r)$ is its final feasible front evaluated on the common 16-scenario evaluation draw, not on the scenarios used to guide search.

The primary inferential estimand is the within-experiment difference in the distribution of held-out hypervolume between SHIELD-MOEA and a stochastic opponent. Two-sided Mann--Whitney U tests are Holm-corrected within each experiment. The 5.09% pooled mean margin over NSGA-II+Repair and 5.56% pooled margin over plain NSGA-II aggregate $8\times30$ records per stochastic method and are descriptive summaries across heterogeneous experiments, not a separate pooled hypothesis test. The corrected inference table records 32/32 Holm-significant wins against the four stochastic baselines. Weighted Sum and Deterministic Planning each have one effective result per experiment; their 16 gaps are descriptive and do not receive seed-level inference.

The screening-specific estimands are narrower:

1. the within-experiment held-out-HV contrast between SHIELD-MOEA and `Ablation-NoScenarioScreen`;
2. the deterministic difference in recorded plan--scenario objective calls under the declared implementation schedule; and
3. the within-experiment held-out-HV contrast between periodic re-screening and `Control-FixedWorstK`.

These estimands do not establish a screening quality gain: the first and third contrasts are unresolved in all eight experiments. They isolate SHIELD-MOEA's independent scientific question as whether selective scenario exposure, separated from final scoring, changes held-out front quality and evaluation workload, and whether repeated population-dependent updates add anything beyond a one-time worst-$K$ subset.

The AC analysis unit is different. It is one method/reference composition from one selected planning experiment, mapped to one network and one operating scenario. Twelve planning/reference configurations, three experiments, six networks, and six scenarios yield 1296 cases. The exported composition is the seed-0 compromise solution, and the mapping retains only counts of reinforcement, storage, DER, and automation actions. AC feasibility requires convergence, all bus voltages in $[0.95,1.05]$ pu, and all line loadings at or below 100%. These cases are descriptive repeated checks under common mappings and scenarios; they are not independent optimizer seeds and carry no p-values.

## Comparison Budget and Data Visibility

The main archive contains 2640 records: 11 methods $\times$ 8 experiments $\times$ 30 stored invocations. Inference treats the stochastic methods as $n=30$ per experiment and the two deterministic rules as $n=1$ per experiment despite their repeated provenance rows. The targeted mechanism archive adds 720 runs for GA-only, DE-only, and fixed-worst-$K$ controls over the same eight experiments and 30 seeds. The one-at-a-time sensitivity sweep uses 10 seeds per point and nominal, multiplicity-unadjusted p-values, so it is exploratory.

All methods receive the same fixed search scenario draw within an experiment. Full-scenario baselines use all 16 search scenarios; SHIELD-MOEA selects an active worst-$K$ subset from those 16. All methods are scored on the same fixed 16-scenario evaluation draw generated with a disjoint seed. The unseen-stress experiment additionally changes the evaluation ranges. Evaluation scenarios are never passed into search. Normalization bounds come from a separate fixed reference sample consisting of the empty plan, every single-action plan, and 2048 seeded budget-feasible random plans; method outputs do not set the scale.

The AC layer sees only exported seed-0 compromise compositions for `deterministic_vs_scenario`, `der_uncertainty`, and `outage_contingency`. Fixed method-independent rules place those action counts on four SimBench MV networks, CIGRE MV, and IEEE 33-bus. Reinforcement parallels the most-loaded lines, storage is assigned to weak-voltage load buses at the declared 3% net-load magnitude, DER is assigned to high-load buses at the declared 4% magnitude, and automation has no steady-state effect. No optimizer receives AC results, and no per-network tuning is performed.

Evidence used for this contract is the current `real_simbench_planning_results.csv`, `real_simbench_planning_inference_v2.csv`, main leaderboard, mechanism-control tables, sensitivity table, compromise-composition table, AC results/summary, source profile, and the corresponding JSON configurations under `papers/mintou/mintou_p4_shield_resilience_planning`. Historical weak and deprecated proxy-method artifacts remain provenance records only.

## Negative and Null Results

- Removing scenario screening is nominally 0.48% lower in pooled mean HV than SHIELD-MOEA, but no significant difference is detected in any of eight experiments. This is a null difference test, not evidence of equivalence.
- Periodic re-screening is statistically inseparable from a worst-$K$ subset fixed after generation 1 in all eight experiments. Dynamic adaptation is not established as necessary.
- Hybrid GA/DE variation is statistically inseparable from DE-only in all eight experiments. The hybrid is a motivated default, not a resolved source of the headline gain.
- Hiding the survivability objective during search produces pooled mean HV 0.27467 versus 0.27396 for the full method, a nominal 0.26% advantage, with no significant difference in any experiment. The resilience objective is retained as a decision-support coordinate, not a performance-improving mechanism.
- The screening call reduction does not produce a wall-clock advantage on the current closed-form proxy. Mean runtime is 0.0889 s for SHIELD-MOEA and 0.0792 s without screening.
- At population 60, the exploratory sensitivity comparison with NSGA-II is unresolved ($p=0.104$). Sensitivity p-values are nominal and uncorrected.
- SHIELD-MOEA does not lead the AC composition check: aggregate feasibility is 0.685 versus 0.694 for NSGA-II+Repair. On IEEE 33-bus both reach 0.333, showing limited transfer of the fixed composition mapping.
- Removing outage exposure during search yields 0.574 AC feasibility versus 0.685 for SHIELD-MOEA and higher mean maximum loading (67.0% versus 52.7%). This is composition-level differential evidence under one fixed export/mapping protocol, not a seeded causal estimate.
- Sampled worst-envelope HV uses the worst values among 16 evaluation scenarios. It is a finite-sample diagnostic, not a bound on unobserved tail behavior.

## Shared Assets and Independent Contribution

The named companion is `mintou_p3_samode_distribution_planning`, identified in the current p4 manuscript by its method/manuscript name CARS-MODE. The shared-infrastructure disclosure must be symmetric in both projects and must not be reduced to "candidate generation only." Source inspection shows that p3 and p4 use:

- the same `mintou_real_planning.py` runner, SimBench subnet extraction, and 72-action candidate builder;
- the same binary-plan data structures, budget-feasibility representation, fixed-bound hypervolume helpers, seeded run/archive machinery, and statistical table generation, with paper-specific branches;
- four common proxy coordinates (cost, loss, voltage risk, and reliability), while p3 uses hosting capacity as its fifth objective and p4 uses survivability; and
- the same `mintou_pandapower_validation.py` infrastructure, six-network/six-scenario AC suite, and fixed composition-to-network mapping, applied to separately exported paper-specific compositions and experiment selections.

This is shared research and evaluation infrastructure, not shared evidence for the two algorithms. The reciprocal disclosure should state the same boundary in `mintou_p3_samode_distribution_planning` and this project: common code, public source data, benchmark construction, evaluation utilities, and AC mapping are shared; the research questions, method-specific search mechanisms, configurations, run archives, comparisons, and conclusions are paper-specific.

SHIELD-MOEA's independent contribution is the scenario-exposure question: worst-$K$ search-phase screening, separation of search and scoring draws, and the direct test of periodic re-screening against no-screening and fixed-worst-$K$ controls in a load/DER/outage proxy setting. The companion's operator/strategy self-adaptation question cannot be used as evidence for screening, and SHIELD-MOEA's results cannot be used as evidence for the companion. The shared AC validator likewise supplies separate composition checks, not a joint algorithm comparison.

## New or Rerun Experiments

No experiment was run or rerun for this narrative stage. No configuration, evidence CSV, table, figure, p-value, or numerical result was changed. This document reconciles claims against existing evidence only.

Broader claims would require new evidence rather than prose changes: independently optimized candidate pools on another network family, nodal siting/sizing with AC power flow in the optimization loop, element-level outage and post-event recovery modeling, and monetary calibration. Until such work exists, the proxy and composition-level qualifiers remain mandatory.

## Unresolved Human Blockers

- **AUTHOR INPUT REQUIRED:** final author list, ORCIDs, affiliations, correspondence details, and author-approved CRediT roles.
- **AUTHOR INPUT REQUIRED:** verified funding and grant information, including whether the correct statement is no external funding and who will cover any APC.
- The authors must confirm the final bibliographic identity and status of the companion: project `mintou_p3_samode_distribution_planning`, currently named CARS-MODE in this manuscript's citation and prose.
- The authors or portfolio owner must place the same full shared-infrastructure disclosure in the companion manuscript. That manuscript is not present in this isolated project worktree, so reciprocal insertion cannot be verified here.
- A persistent public archive URL/DOI and source-data terms remain to be supplied before publication.
