# Applied Sciences Comparator Map

## Audit boundary

This map uses the 33-item frozen manuscript bibliography and the worktree's recorded 2026-07-17 Crossref re-verification (`manuscript/WAVE1_CHANGELOG.md`). Live Crossref and AnySearch access was unavailable on 2026-09-03, so no new search lead is promoted to a citation. Bibliographic verification and sentence support are separated in `REFERENCE_VERIFICATION.csv` and `LITERATURE_EVIDENCE_MATRIX.csv`.

## Target-journal neighbors

| Source | Applied Sciences topic | Supported comparison | Boundary |
|---|---|---|---|
| ref10 | Coordinated transmission and storage planning | Multi-stage grid-planning formulation under renewable integration | Does not validate this paper's heterogeneous 120-item proxy or local operators |
| ref11 | Reliability investment valuation | Interruption-cost estimation for value-based reliability investment | Not a portfolio-search or algorithm-comparison study |
| ref12 | Grid-side storage planning and return analysis | Storage planning under multiple grid-security requirements | Asset-specific comparator; not evidence of project-vocabulary substitution |
| ref13 | Battery configuration | Multi-objective battery configuration for peak shaving and valley filling | Asset-specific comparator; not evidence of portfolio-scale behavior |
| ref17 | Power-plant site selection review | Review context for multi-objective optimization-based site selection | Review scope differs from project portfolio search |

The target-journal set supports topical fit in planning, investment valuation, and multi-objective decision problems. It does not support an accuracy, deployment, electrical-feasibility, or practical-review claim for BiLo-NSGA.

## Cross-thread comparator map

| Thread | Sources | What can be claimed | What remains outside evidence |
|---|---|---|---|
| Non-dominated sorting and canonical MOEAs | ref1, ref22, ref24; ref23 as decomposition comparator | Pareto-based evolutionary comparison, NSGA-II, NSGA-III, and MOEA/D are established method lineages | No source establishes BiLo-NSGA superiority |
| Knapsack and portfolio selection | ref2--ref9, ref31, ref32 | Multi-objective knapsack, portfolio selection, dependencies, and constrained memetic search are relevant neighboring problem classes | No exhaustive claim that these literatures lack atomic substitution |
| Neighborhood and local search | ref2, ref20, ref21, ref25, ref31, ref32 | Genetic local search, Pareto-archived search, memetic search, and Pareto local search are legitimate comparators | A verified variable-neighborhood-search citation was not recovered in this environment |
| Power-grid planning and investment | ref8, ref10--ref13, ref18, ref19, ref26--ref30 | Risk--benefit investment, reliability valuation, storage, transmission, distribution, and grid-planning studies establish application adjacency | They do not provide expert labels, calibrated costs, load-flow validation, or evidence for the paper's run summaries |
| Matched-compute evaluation | local protocol and matched archive | The paper may describe its exact 3200-unit budget and separate 0.20-s deadline as its own disclosed design | No external source was verified here for a field-wide matched-compute standard |

## Move-semantics guard

In this paper, **atomic substitution** is a single evaluated proposal: one selected project is tentatively deleted, one affordable unselected project is inserted, and the pair is either accepted together or rolled back together. A method with separately evaluated or separately committed deletion and insertion moves is not equivalent, even if both move types occur during one run. References ref31 and ref32 remain nearby portfolio/local-search comparators, but the accessible evidence does not justify labeling their operators atomic or claiming that no earlier atomic operator exists.

## Claim-language guard

- Use “project-vocabulary move” only for the inspected BiLo-NSGA implementation.
- Use “run-level accepted-event summaries” rather than audit trail, lineage, replay, provenance, or explanation quality.
- Use “heuristic group-label bonus” rather than dependency model or dependency synergy.
- Keep matched-evaluation results, matched-time results, and historical/proxy checks in their declared evidence layers.
- Do not relabel grid reliability, event records, or optimization monitoring as cybersecurity evidence.

## Unfilled search cells

Variable-neighborhood search and external matched-compute methodology remain unfilled cells because live discovery failed and the local corpus contained no verified source suitable for import. This limitation is recorded rather than repaired with title-only or remembered citations.
