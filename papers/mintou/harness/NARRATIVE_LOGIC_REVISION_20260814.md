# Mintou Six-Paper Narrative Logic Revision Record

Date: 2026-08-14
Scope: the six `manuscript/journal_submission/paper.tex` files and independently built `paper_narrative_revision.pdf` artifacts.

## Revision objective

The revision aligns each manuscript's title, research object, contribution claims, empirical evidence, discussion, limitations, and conclusion. It does not add experiments, alter archived numerical results, or invent author, funding, expert-label, or citation information.

## Paper-level changes

1. **P1 (GRU-LSR dispatch forecasting).** Replaced evaluative uses of “fair” with “matched” where the phrase denotes comparison quality, while retaining `fair run` where it is the archived protocol name. Statistical claims continue to distinguish the retrieval-versus-head result from Persistence and from the unsupported onset analysis.
2. **P2 (HyGraph forecasting).** Standardized null-result language to “no statistically distinguishable difference under the declared tests” and aligned the abstract, discussion, and conclusion with the reported testing design.
3. **P3 (CARS-MODE).** Recast the manuscript as a constraint-aware multi-objective DE framework with metric-sensitivity diagnostics. The main result now distinguishes favorable archived hypervolume from order changes under analytic normalization and IGD+. Repair/diversity evidence is separated from the unresolved adaptation bundle. Discussion and conclusion connect proxy optimization to the illustrative AC layer without claiming physical superiority.
4. **P4 (SHIELD-MOEA).** Reframed the contribution around disjoint search/evaluation scenarios, resolved repair evidence, and a measured screening workload--quality trade-off. The main comparison precedes pooled archive summaries; replicated labels and the 32/32 count are demoted to interpretation limits. Screening row reduction is not described as a quality or wall-clock gain, and AC mapping is not used to claim electrical superiority.
5. **P5 (TRACE-MOEA).** Separated complete-framework performance from the unresolved direct contribution of preference adaptation. The 98.6% event statistic is consistently defined as run-level set overlap rather than lineage or replay. Normalization sensitivity and the implemented R-NSGA-II boundary are carried through Results, Discussion, Limitations, and Conclusions.
6. **P6 (BiLo-NSGA).** Made the exact 3200-unit matched-effort comparison the primary result. The paper now states consistently that BiLo-NSGA does not outperform NSGA-II under that protocol, while retaining the bounded result against the disclosed Pareto Local Search. The earlier fixed-generation margin is treated as an unmatched quality--compute trade-off. Run-level accepted-move summaries are not presented as lineage.

## Cross-paper narrative edits

- P3--P6 contributions were reduced to three evidence-backed items where separate framework and mechanism claims had previously been conflated.
- Results lead with the strongest design-appropriate comparison rather than execution or archive inventory.
- Discussion follows the order: main finding, mechanism interpretation, practical meaning, and evidence boundary.
- Conclusions answer the research object directly and avoid turning unresolved component effects into system-wide failure or superiority claims.
- Long audit-style limitation inventories in P3--P6 were consolidated into five or six thematic groups without removing facts that materially bound interpretation.
- High-risk terms such as superiority, lineage, replay, robustness, and fairness are now qualified by the corresponding experimental design.

## Build and static verification

| Paper | PDF | Pages | Fatal LaTeX errors | Undefined citations/references |
|---|---|---:|---:|---:|
| P1 | `paper_narrative_revision.pdf` | 12 | 0 | 0 |
| P2 | `paper_narrative_revision.pdf` | 25 | 0 | 0 |
| P3 | `paper_narrative_revision.pdf` | 29 | 0 | 0 |
| P4 | `paper_narrative_revision.pdf` | 28 | 0 | 0 |
| P5 | `paper_narrative_revision.pdf` | 28 | 0 | 0 |
| P6 | `paper_narrative_revision.pdf` | 29 | 0 | 0 |

`git diff --check` passes for all six source files. MiKTeX reports a local maintenance warning that updates have not recently been checked, but all six PDFs were produced and the logs contain no fatal LaTeX, undefined-control-sequence, undefined-citation, or undefined-reference condition.

## Remaining author-only submission gates

The source files still contain explicit `AUTHOR INPUT REQUIRED` placeholders for verified author contributions, funding, correspondence, or related declarations. These fields were deliberately not inferred. They do not affect the narrative revision, but they must be completed and approved by the authors before submission.
