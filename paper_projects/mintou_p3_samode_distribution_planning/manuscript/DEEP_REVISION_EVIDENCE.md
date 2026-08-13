# Deep Revision Evidence Contract

**Identity decision.** The current assets support a **SimBench-derived mixed-voltage portfolio proxy study**, not an action-aligned distribution expansion study. The benchmark generates costs and benefits from subnet statistics, spans EHV--LV source data, and evaluates selected action counts through a separate composition-to-MV-network mapping. It does not optimize nodal construction actions, monetarily calibrated investments, or utility deployment decisions.

## Title-to-Evidence Map

**Aligned title:** *CARS-MODE: Constraint-Aware Repair and Strategy-Pool Multi-Objective Differential Evolution on a SimBench-Derived Mixed-Voltage Portfolio Proxy*

| Title element | Evidence in the current assets | Claim boundary |
|---|---|---|
| CARS-MODE | `MANUSCRIPT.md`, Section 4, defines the binary multi-objective DE, parameter control, strategy pool, repair, and crowding selection. | Names the implemented optimizer only; it is not deployment evidence. |
| Constraint-aware repair and strategy pool | Sections 4.2--4.4 and the FixedDE/NoRepair controls in Sections 5.1 and 6.2. | FixedDE changes parameter and strategy adaptation jointly, so the evidence cannot identify either adaptive subcomponent separately. |
| SimBench-derived | Section 3.2 derives aggregate inputs from the public SimBench complete mixed dataset. | The objectives are analytic indices of those statistics, not AC power-flow objectives. |
| Mixed-voltage portfolio proxy | Table 2 spans EHV--LV source subnets; Sections 3.2 and 5.4 state that the separate AC check uses four MV networks and maps portfolio compositions rather than nodal actions. | The voltage tiers and candidate actions are not an action-aligned engineering expansion model. |

The former title ending, "for Distribution Network Expansion Planning," was broader than the analysis supports because it could imply that the optimizer selected and validated concrete expansion actions. The aligned title names the proxy as the experimental object.

## Primary Estimand and Analysis Unit

The primary reporting target is the within-scenario distribution of standard hypervolume for each stochastic method on the fixed proxy objective. Between-method magnitude is reported as mean hypervolume difference or relative mean margin; inference uses two-sided Mann--Whitney U tests with Holm correction within each scenario. The seeded optimizer run is the analysis unit (`n = 30` per stochastic method and scenario). Pooled means over seven heterogeneous scenarios are descriptive summaries, not a separate replicated estimand.

The deterministic Weighted Sum method has one effective output per scenario. Its repeated archive invocations are provenance rows, not independent observations, so its seven comparisons are descriptive and receive no seed-level p-values.

The AC stage answers a different, secondary question: whether one seed-0 compromise composition per method and selected planning experiment remains feasible after a deterministic mapping onto four MV networks and six operating/stress cases. Its 72 binary cases per method are generated from three plan compositions rather than 72 independent optimizer runs. This stage supports descriptive transfer and failure-pattern statements, not a powered causal or method-superiority estimand.

## Comparison Budget and Data Visibility

| Item | Contract recorded in the manuscript |
|---|---|
| Stochastic repetition | 30 independently derived seeds per method and proxy scenario. |
| Population budget | Population 40 and 40 generations for population-based methods. |
| Objective visibility | Identical five-objective proxy and budget definition across methods; fixed, method-independent hypervolume normalization. |
| Confirmatory comparison family | Twelve stochastic opponents within each scenario, Holm-corrected at 0.05. |
| Deterministic comparator | Weighted Sum is an `n = 1` point comparison per scenario. |
| Sensitivity sweep | 10 seeds per point; displayed p-values are nominal and multiplicity-unadjusted, so the sweep is exploratory. |
| Electrical inspection | One seed-0 compromise composition for each of three experiments, mapped to four networks and six cases; descriptive only. |

The isolated worktree contains the manuscript, figures, figure-generation source, and the derived summaries `p3_pooled_efficiency.csv` and `p3_ac_margin_diagnostics.csv`. The master manuscript points to a larger evidence tree and machine-readable configurations in the source project, but the raw 2940-run archive, inference tables, and configurations are not copied into this worktree. This narrative stage therefore records the claim contract from the available assets and does not claim a fresh audit of every run or p-value. Before submission, the supplementary evidence package named in the Data Availability Statement must be checked against the final manuscript.

## Negative and Null Results

- **Adaptation bundle unresolved:** Ablation-FixedDE is nominally 0.60% higher in pooled proxy hypervolume, and the contrast is unresolved in all seven scenarios. The paper cannot claim that parameter-and-strategy adaptation improves proxy accuracy.
- **No component-level causal separation:** FixedDE disables parameter adaptation and the strategy pool together. It supports only a joint conclusion and cannot identify either subcomponent as helpful or harmful.
- **NoDER near-null/problem-variant result:** Ablation-NoDER is nominally 0.12% higher in pooled proxy hypervolume and changes the candidate pool rather than one algorithmic operator; it is not component attribution.
- **Proxy--physics disagreement:** CARS-MODE leads the implemented external controls on proxy hypervolume but is mid-pack in the descriptive AC-feasibility ranking (0.611 versus 0.667 for NSGA-II and 0.681 for Standard DE).
- **Mapped high-DER reversal:** No-Plan exceeds several methods in one high-DER stress setting. The manuscript identifies this as a deterministic mapping-rule artifact, not evidence that no planning is preferable.
- **Configuration-specific failure:** The tested MOEA/D penalty configuration collapses to the empty plan; no claim is made about MOEA/D generally.
- **Residual comparison null:** The NSGA-II+Repair contrast in `storage_allocation` is the one unresolved stochastic-baseline cell among the 56 reported cells.
- **AC stage not statistically powered:** The full-versus-FixedDE AC rates (0.611 versus 0.569) are descriptive and do not overturn the unresolved proxy contrast.

## Shared Assets and Independent Contribution

The companion project is explicitly named **`mintou_p4_shield_resilience_planning`**. It and this CARS-MODE study share the generators used to derive SimBench-based benchmark inputs. Those shared generators are common infrastructure; they do not provide an independent dataset replication and do not allow a result from one project to be counted as evidence for the other.

The independent CARS-MODE question is: **under a fixed SimBench-derived proxy benchmark, comparison budget, and evaluation protocol, does the complete constrained-search framework improve proxy-front quality relative to the implemented controls, and which mechanism groups survive ablation?** The companion project instead addresses resilience-oriented stress-scenario screening in the evaluation layer. The present contribution is restricted to the CARS-MODE optimizer question, its own comparisons, and the reported proxy-to-AC validity check.

## New or Rerun Experiments

No experiment was added, rerun, filtered, or retuned in this stage. No numerical result, p-value, seed count, effect direction, or AC-feasibility rate was changed. The work is a narrative identity and disclosure revision based on the current manuscript, derived tables, and figure source.

Future experiments named in the manuscript remain future work: nodal action-aligned siting and sizing, multi-seed AC mapping, monetary calibration, a second benchmark family, parameter-only and strategy-only controls, and additional multi-objective DE controls. They are not evidence for the current claims.

## Unresolved Human Blockers

- **AUTHOR INPUT REQUIRED:** obtain approval for the CRediT role assignment for every listed author. No roles are inferred in this stage.
- **AUTHOR INPUT REQUIRED:** provide the verified funder, grant number, and APC funder, or approve the statement that the research received no external funding. No funding statement is inferred in this stage.
- Confirm that the corresponding-author-held supplementary package contains the raw run archive, corrected inference tables, configurations, and AC cases described by the final Data Availability Statement, and retain the shared-generator provenance alongside that package or in internal records.
- Approve the final public archive location or DOI before publication; the current manuscript states that a persistent archive can be supplied but does not provide one.
