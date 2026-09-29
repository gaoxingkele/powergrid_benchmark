# Meta skill applied: review → revision → rescore

Skill: paper-meta-review v1.0; Information profile 2026-09-12.1 plus new router.
Date: 2026-09-13. Source SHA after:
`2261d07bb8fc23cd134dcb0cc11fb16703a2026c3387fbbb90b900a25a5f07a8`.
This is same-agent consultation. Scores are ordinal judgments with a transparent
weighted arithmetic, not empirically calibrated acceptance probabilities.

## Same-scale scores

| Dimension | Before /4 | After /4 | Reason |
|---|---:|---:|---|
| I1 Contribution | 3 | 3 | Clear bounded diagnosis, no additional contribution evidence |
| I2 Theory/mechanism | 2 | 2 | Elementary properties unchanged |
| I3 Data/validity | 1 | 1 | No new cross-pool execution or expert validation |
| I4 Comparisons | 2 | 2 | Controlled diagnostics retained; external replication open |
| I5 Statistics | 3 | 3 | Finite-pool/Appendix caveats retained; no new statistics |
| I6 Narrative/prose | 3 | 3 | Local alignment improved, insufficient to claim a whole-band change |
| I7 Reproducibility | 2 | 2 | New source is built; old R3 ZIP does not contain this revision |
| I8 Presentation | 3 | 3 | 30-page build, changed text pages visually inspected; full fresh visual audit not claimed |
| I9 Author readiness | 1 | 1 | Current author/portal approvals still absent |

Total **56.25 → 56.25 /100**; scientific subtotal **48.75/85**;
technical/author subtotal **7.50/15**. Weights and initial ratings were saved
before the edit in BEFORE_REVIEW.md. Unchanged score is intentional: wording
alone cannot remove the principal scientific weaknesses.

## Actual meta interface map (scoped, not whole-text coverage)

| Unit/locator | Rhetorical function / atomic claim | Evidence link | Cross-section edge | Status |
|---|---|---|---|---|
| Abstract | Separate candidate absence from selection failure | tab:failure-partition | RQ1→Results | Supported within retained pool |
| Introduction RQ1 | Ask where correct answers are lost | candidate/eligibility/top-score sets | Methods→failure decomposition | Supported, external scope limited |
| eq:poolbound / propositions | Define finite-pool limits | algebraic definitions | Method→diagnostic categories | Basic deductive property, not new general theory |
| Results reading guide | Prioritize availability/scoring/ties | tab:failure-partition; tab:offline | Abstract→RQ1→Results | META-01 closed by this edit |
| BIRD supporting results | Generation portability, not selector replication | retained BIRD aggregates | RQ3→Discussion boundary | Explicitly limited; META-02 open |
| Conclusion | Diagnose before adding complexity | counts 42/0/6/33–32 | Results→design implication | Conditional lesson, not demonstrated deployment gain |

Unassessed here: full natural-paragraph lengths, all sentence-level edges,
211-field completion and fresh full reference-truth verification. Existing
Information atlas itself has incomplete third-paper paragraph coverage; this
loop does not silently upgrade it to a complete journal model.

## Revision and verification

Changed only the two paragraphs in Results/Evidence Summary and Reading Guide.
The new opening follows candidate availability→scoring→tie ambiguity; it keeps
the strongest fixed source and distinguishes 130 slot ties from 51 mixed-
correctness top sets. Supporting generation results now follow the main
diagnosis. No experiment, equation, table, figure, author or citation changed.

Final verification: `final/verification.json`, `final/revision.patch`.
All table/equation/figure blocks are byte-equivalent as decoded source;
outside the reading-guide subsection text is unchanged. Two LaTeX builds
passed without unresolved references or overfull boxes. The first longer
candidate produced 31 pages; it was tightened for concision, final 30 pages.
Final pages 14 and 15 were visually inspected and are legible, with no detected
overlap/clipping. Earlier intermediate verification is retained, not current.

## Outstanding review advice

- META-02: authorize and execute the proposed reference-free BIRD replay to
  test cross-pool transfer; do not count existing generation results as that test.
- META-03: bind the eventually approved source, supplement and release; the R3
  ZIP remains an unchanged older candidate, not a package for this new SHA.
- META-04: obtain version-bound author approval/exclusivity before submission.

Recommendation remains substantial strengthening, not immediate submission.
