# Cross-Paper Round 3 Final Methodology/Statistics Decision

## Final panel decision

| Manuscript | Method/statistics decision | Scientific blocker | Submission-operation blocker |
|---|---|---|---|
| C²GES | **Acceptable after minor editorial correction** | None for bounded proxy-corpus claims | Synchronize/tag/archive/fresh-clone verify exact repository |
| MA-SQLGrid | **Acceptable after submission-operation closure** | None for bounded software/finite-corpus claims | Synchronize/tag/archive/fresh-clone verify exact repository |

## Closed Round 2 blockers

- C²GES now discloses the unrenormalized no-CF estimand and its 17.6% relative redundancy-scale coupling; it no longer claims pure component isolation.
- C²GES's absolute-distance edge formula matches frozen code, and complexity now correctly states an `O(n^2)` ordered-pair scan with a local distance gate.
- MA-SQLGrid now shows all six component effects and paired denominators, explicitly identifies three two-member Holm families, distinguishes pointwise intervals from familywise decisions, and states weighting/exchangeability assumptions for factorial, component, formal-v5, and BIRD analyses.
- All recomputed totals, effects, intervals, exact/randomization values, Holm adjustments, rescue/harm counts, ties, and call/state counts match retained artifacts to printed precision.

## Remaining blocker categories

1. **Submission reproducibility — blocking before upload:** both GitHub repositories must match the final candidate through an immutable tag/commit or archive DOI and pass a fresh-clone build/test.
2. **External semantic validation — blocks only stronger claims:** neither paper has qualified domain-expert validation on title-concordant operational data. The manuscripts already limit their claims accordingly, so this is not a blocker for submitting the bounded studies.
3. **Editorial non-blockers:** C²GES may standardize “registered unrenormalized no-CF” terminology and label `t_boot` unadjusted. These changes require no new analysis.

## Integrity outcome

Across three rounds, no negative result was removed, no failed incident was converted into evidence, no LLM judgment was relabeled as expert gold, and no post hoc tuning result was promoted to confirmation. The final method/statistics audit finds no need to rerun either experiment suite.
