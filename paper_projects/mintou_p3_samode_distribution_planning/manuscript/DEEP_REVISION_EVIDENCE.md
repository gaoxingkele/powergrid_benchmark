# Deep Revision Evidence Contract

**Identity decision.** The current evidence supports a SimBench-derived mixed-voltage portfolio-proxy optimizer study. It does not support action-aligned expansion planning, monetarily calibrated investment decisions, utility deployment, or optimizer-level electrical superiority.

## Title-to-Evidence Map

**Locked title:** *Power Distribution Network Planning Strategy Optimization based on Self-Adaption Multi-objective Differential Evolution Algorithm*

The title is retained verbatim as an approved identity constraint. It does not enlarge the evidence: the current study remains a SimBench-derived portfolio-proxy optimizer study, not action-aligned expansion planning or a demonstration that self-adaptation caused an improvement.

| Title element | Evidence | Claim boundary |
|---|---|---|
| Power Distribution Network Planning Strategy Optimization | `MANUSCRIPT.md`, the immutable P3 S3 archive, and the P3 S4 narrative manifest document optimization of SimBench-derived candidate-action portfolios under the stated proxy objectives. | "Planning" and "strategy optimization" refer to the portfolio proxy. They do not establish action-aligned siting, monetary calibration, AC-feasible final plans, or deployment evidence. |
| Self-Adaption Multi-objective Differential Evolution Algorithm | Section 4 and the read-only planning implementation define binary multi-objective DE, a joint adaptive controller, deterministic budget repair, and crowding selection; FixedDE, NoRepair, and NoDiversity are the available controls. | FixedDE disables parameter and strategy adaptation jointly. The present evidence neither identifies either adaptive subcomponent nor supports the causal wording that self-adaptation improves performance. |

The supported contribution is a reproducible constrained-search and diagnostic workflow with a demonstrated normalization limitation, not consistent optimizer or electrical superiority. This evidence boundary governs interpretation of the locked title.

## Primary Estimand and Analysis Unit

The archived primary estimand is the within-seed-block distribution of sampled-bound, clipped hypervolume for each stochastic method. The optimizer seed is the within-configuration analysis unit (`n = 30` per stochastic method and seed block). The archive contains six distinct deterministic configurations and seven seed blocks because `pareto_quality` independently replicates the base configuration. Two-sided Mann--Whitney U tests compare CARS-MODE with twelve stochastic opponents, with Holm correction within each seed block.

This stage makes configuration-specific effects primary. The two 30-run base seed blocks are pooled only for the base configuration's descriptive mean; the six configuration means then receive equal weight in cross-configuration summaries. Thus the deterministic planning configuration is the unit for cross-configuration generalization, while optimizer seeds remain the units for within-block inference. Because the six configurations are a fixed benchmark set rather than sampled grids, cross-configuration ranks and effects remain descriptive and receive no population-level p-value. Inferential results retain all seven seed blocks and their original Holm families. Three robustness estimands are evaluated on every preserved rerun front: unclipped analytic-bound hypervolume at reference 1.10, the same hypervolume at alternative reference 1.05, and common-reference IGD+ against the empirical non-dominated union within each seed block. The three metric definitions are robustness families; no multiplicity claim is made across them.

Weighted Sum has one effective deterministic output per seed block. Its 30 repeated archive rows per block preserve rectangular provenance and are not inferential replicates.

The AC layer addresses a different question. It contains one run-index-0 compromise composition per archived method from each of three selected seed blocks, deterministically mapped to four MV networks and six fixed cases. Its 72 rows per method share three compositions and are not optimizer replications. This stage retains AC as an illustrative composition diagnostic and does not compute seed-level or hierarchical optimizer uncertainty.

## Comparison Budget and Data Visibility

| Item | Evidence contract |
|---|---|
| Main optimizer archive | 14 methods x (6 configurations + 1 base replicate) x 30 rows = 2940; 2730 seeded stochastic runs and 210 deterministic Weighted Sum provenance rows. |
| Search horizon | 40 generations; population 40 except MOEA/D's 35 reference-direction members. Comparable pymoo evaluation counters were not archived. |
| Pareto-control fairness | GDE3 and NSDE match the Pareto-based DE search class, population 40, and 40-generation horizon. They are not claimed as strict equal-function-evaluation controls because comparable `n_eval` counters were not archived. |
| Legacy metric | Method-independent sampled reference set, 5% expanded sampled bounds, clipping to `[0,1]^5`, reference `1.10` in every coordinate. |
| Analytic metric | Equation-derived feasible envelopes, no clipping, references `1.10` and `1.05`; no optimizer output constructs the bounds. |
| Common-reference metric | IGD+ against the empirical non-dominated union of all methods and seeds within each seed block; complementary, not independent. |
| Inference | Seed-level Mann--Whitney U, Holm-corrected over twelve stochastic opponents within seed block and metric. |
| Narrative aggregation | Canonical manifest `evidence/runs/p3_s4_results_narrative_20260813/manifest.json`; base seed blocks pooled within the base row, followed by equal weight across six configurations. |
| Electrical inspection | Archived seed-0 compositions only; common No-Plan row matched by experiment/network/case; descriptive paired changes only. |

The immutable experiment evidence directory is `evidence/runs/p3_s3_planning_validation_20260813/`. It contains the run manifest, exact-reproduction comparison, all returned front objectives and their index, all-seed deterministic compromise compositions, sampled and analytic bounds, reference/clipping audit, per-run robustness metrics, seed-block inference, common reference fronts, the AC scope decision, and the matched No-Plan table. The P3 S4 canonical narrative manifest references those files by SHA-256 and deterministically regenerates the configuration tables and result figures. `ANALYSIS.md` and `VALIDATION_REPORT.md` record the Material Passport, warnings, reproducibility verdict, and 11-category statistical-fallacy scan.

The rerun used the existing planning source read-only. No shared P3/P4 source, configuration, or P4 evidence was edited. Runtime is retained only as provenance because the rerun environment differs from the archive environment.

## Negative and Null Results

- **External-control ordering is normalization-sensitive.** With equal weight across six configurations, sampled-bound/clipped HV gives CARS-MODE 0.04240014 versus 0.03997622 for NSGA-II+Repair. With analytic bounds and reference 1.05, the values are 0.00043464 versus 0.00043530, and CARS-MODE ranks fourth overall. Common-reference IGD+ ranks CARS-MODE fifth (0.02218917 versus 0.02117209; lower is better). A consistent-superiority claim is not supported.
- **Clipping is material.** Among 68,248 returned front points, 2189 points contain 2281 sampled-normalized coordinates below zero: 1750 voltage-risk and 531 negative-reliability coordinates. None exceeds one. The un-clipped 1.10 reference already strictly dominates every point, with minimum coordinate-wise margin 0.14545, so clipping is not required for reference dominance and instead floors distinct improvements.
- **Adaptation bundle unresolved.** FixedDE is nominally higher than CARS-MODE under all equal-configuration summaries: 0.60% for sampled-bound/clipped HV, 0.52% for analytic HV at reference 1.05, and 1.31% for common-reference IGD+. The joint control does not establish a benefit from parameter-and-strategy adaptation and cannot separate its two parts.
- **NoDER is a problem variant.** It ranks first under the analytic and common-reference diagnostics, but it removes DER/storage decisions and cannot support algorithmic component attribution.
- **Direct-control evidence weakens under robustness metrics.** Sampled-bound/clipped HV favors CARS-MODE over GDE3 and NSDE in all seven seed blocks spanning six configurations. Under analytic HV only one of seven contrasts against each is Holm-significant in the favorable direction; common-reference IGD+ favors CARS-MODE by mean in four of seven against each, with one significant favorable contrast.
- **AC remains illustrative.** CARS-MODE has an archived AC-feasible case fraction of 0.611 versus 0.500 for No-Plan and 0.667 for NSGA-II. In the matched common panel it changes 11 rows from infeasible to feasible and 3 in the reverse direction, but these are dependent fixed-case rows from seed-0 compositions. GDE3, NSDE, and NSGA-II+Repair have no archived AC rows.
- **Mapped high-DER reversal and MOEA/D failure retain narrow scopes.** The No-Plan reversal in one high-DER case is a composition-mapping artifact. The tested penalty-based MOEA/D configuration returns the empty plan; neither observation generalizes to the algorithm family or deployed planning.
- **Configuration labels required correction without changing evidence.** The `der_siting_sizing` block excludes storage but retains reinforcement and automation, and `storage_allocation` excludes DER but retains reinforcement and automation. P3 S5 replaced the misleading "DER-only"/"Storage-only" display labels with storage-excluded/DER-excluded labels; no run, number, or ordering changed.

## Shared Assets and Independent Contribution

The companion project is explicitly named **`mintou_p4_shield_resilience_planning`**. It shares SimBench-derived generators with this project. Shared generators are common infrastructure, not an independent dataset replication, and evidence from one project is not counted for the other.

The independent P3 contribution is the implementation and audit of the constrained-search workflow on its fixed portfolio proxy: exact seeded rerun, front preservation, reference-dominance and clipping audit, method-independent analytic bounds, alternative-reference sensitivity, common-reference IGD+, joint ablations, and an explicitly illustrative proxy-to-AC composition check. P4 evidence and claims remain untouched.

## New or Rerun Experiments

The upstream P3 S3 stage reran all 2940 optimizer rows using the declared source-derived seeds. All archived sampled-bound hypervolumes match at eight decimals; the maximum absolute serialized difference is 0. The rerun preserves 68,248 returned front points and exports a deterministic normalized-sum compromise for every optimizer seed.

That upstream stage added deterministic evaluations of those fronts:

- pre-clipping reference dominance and clipping-direction counts;
- unclipped hypervolume under equation-derived feasible envelopes at references 1.10 and 1.05;
- IGD+ against one empirical common reference front per seed block; and
- seed-level Mann--Whitney/Holm tables for each robustness metric.

P3 S4 runs no new optimizer or AC experiment. It adds only a deterministic narrative aggregation: six configuration means, an internal-replication rule for the two base seed blocks, equal-configuration summaries, configuration-specific effect tables, and figures regenerated from one hashed manifest. The all-seed compromise compositions remain non-AC evidence. No method, parameter, seed, bound, reference, or result was selected to improve CARS-MODE's apparent ranking; the unfavorable and null findings are retained.

P3 S5 likewise runs no optimizer or AC experiment. It performs logic, methodology--statistics, and theory--innovation closure reviews; corrects configuration and NoDER descriptions against the hashed source; makes the two analysis-unit levels explicit; narrows the innovation claim; and regenerates tables/figures from the existing canonical manifest. The review and disposition ledger is `manuscript/P3_S5_THREE_ROUND_CLOSURE.md`.

## Unresolved Human Blockers

- **AUTHOR INPUT REQUIRED:** obtain approval for the CRediT role assignment for every listed author. No roles are inferred in this stage.
- **AUTHOR INPUT REQUIRED:** provide the verified funder, grant number, and APC funder, or approve the statement that the research received no external funding. No funding statement is inferred in this stage.
- Confirm the corresponding-author supplementary package and final public archive/DOI before publication. No repository URL or DOI is invented here.
- Multi-seed AC power flow with hierarchical uncertainty, action-aligned nodal siting, monetary calibration, a second benchmark family, parameter-only and strategy-only controls, and additional multi-objective DE implementations remain future work, not current evidence.
