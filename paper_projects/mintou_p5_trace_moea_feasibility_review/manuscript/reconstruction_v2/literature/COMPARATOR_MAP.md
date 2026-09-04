# Verified Literature and Energies Comparator Map

This map records what each comparator can and cannot support. It does not transfer another study's numerical findings, datasets, engineering validity, or deployment claims to TRACE-MOEA.

| Unresolved problem | Retained sources | What the sources establish | What remains unsupported here |
|---|---|---|---|
| Project-queue selection versus network/asset planning | refs 1, 2, 10, 11, 29--33 | Transmission, storage, reliability-cost, and investment models provide established planning formulations and application-specific validation examples. | The TRACE-MOEA proxy objectives are not audited utility costs, AC-feasible plans, N-1-secure plans, or realized returns. |
| Physical validation | ref34 | Losses and N-1 contingencies can alter expansion plans in a specialized planning model. | No AC/power-flow or N-1 validation has been run for the present candidate portfolios. |
| Recent Energies MOEA comparator | ref35 | An improved NSGA-II has been applied to IEEE-33-bus investment-cost, reliability, and network-loss objectives; that paper explicitly leaves scenario and N-1 checks for later work. | It is not a matched implementation-level baseline for this binary project queue and supplies no result about TRACE-MOEA. |
| Constraint handling | ref28, with algorithm families refs 8, 9, 12 | Constrained-MOEA work treats feasibility handling as a distinct design dimension; NSGA-II, MOEA/D, and NSGA-III represent different baseline families. | The current combined objective-hiding controls do not isolate every constraint-handling component, and no new matched CMOEA run was performed in this literature stage. |
| Preference guidance | refs 13--20 | Reference points, scalarizing functions, dominance modifications, and adaptive vectors are established; preference guidance is not uniformly beneficial. | The 0.17% direct ablation difference does not establish an independent preference-adaptation benefit. |
| Traceability and audit | refs 21--27 | XAI, provenance, and audit literature define stronger requirements than aggregate event counts. | Current run summaries do not establish chronology, lineage, replay, explanation quality, or human-review value. |

## Comparator decisions

- `ref34` was added as the physical-validation comparator because its losses and N-1 analysis directly supports the manuscript's limitation that electrical checks are load-bearing.
- `ref35` was added as a recent Energies NSGA-II application comparator. It is cited only for its formulation and disclosed validation boundary, not for cross-study performance ranking.
- `ref28` now denotes the verified 2023 constrained-MOEA survey. The former unpublished companion citation was removed from the bibliography because it lacked an independently verifiable record.
- The 2020 BESS transmission-planning paper found during screening was not added: it is relevant but older and redundant with the retained physical-validation role. Its exclusion is recorded in `SEARCH_LOG.json`.

## Scope gate

The literature supports the need for cost, electrical, constraint-handling, preference, and audit checks. It does not show that the current proxy ranking will survive any of those checks. The canonical validation protocol remains `NO_RESULTS`.
