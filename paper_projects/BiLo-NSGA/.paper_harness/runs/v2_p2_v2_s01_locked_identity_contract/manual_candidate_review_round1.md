# P2 v2 Stage 1 Candidate Review — Round 1

**Scope:** candidate commit `bd504a58` plus review-fix commit `e4af0da9`, compared with approved baseline `8a274c64`.

**Paradigm / venue:** STEM multi-objective optimization and power-grid investment screening; MDPI Applied Sciences.

**Decision scope:** acceptance of the locked-identity and claim-contract stage only. This review does not certify the full manuscript for submission.

## Summary

- Candidate-introduced CRITICAL: 0.
- Candidate-introduced MAJOR: 0 after review fix.
- Candidate-introduced MINOR: 0 after review fix.
- The candidate preserves the exact locked title, confirmed author order and corresponding-author role, Applied Sciences route, all adverse NSGA-II evidence, and the distinction between stage-local atomic substitution and unproved component benefit.
- Downstream submission blockers remain: unverified item-level references, incomplete bidirectional-mechanism identification, no second independent task family, PNG-first figure inclusion, stale checked-in PDFs, and unresolved layout warnings.

## Dimension 1: Macro logic

| # | Finding | Severity | Suggested fix |
|---|---|---|---|
| 1 | The candidate binds the exact title to three bounded meanings: the stage-local non-dominated-sorting implementation, inspected forward and paired delete--insert passes, and proxy effectiveness screening. | PASS | Preserve these boundaries until the orthogonal ablation and independent task-family evidence license stronger wording. |
| 2 | The protected result states that all eight BiLo-NSGA scenario means are below NSGA-II, with zero significant wins and four significant losses. Direct parsing of `matched_summary.csv` and `matched_inference.csv` reproduces 8/8 negative means, 0 significant wins, and 4 significant losses. | PASS | Retain this result in every later manuscript version, even if a new task family is favorable. |
| 3 | The title foregrounds bidirectional local search, while P2-C04 correctly remains `UNRESOLVED` and P2-C08 remains `FUTURE_HYPOTHESIS`. | CRITICAL for submission; not introduced by this candidate | Complete the frozen NDS-only, forward-only, backward-only, and bidirectional matrix on two independently generated action-aligned task families. If that gate fails, keep the route at NO-GO under the locked title. |

## Dimension 2: Writing details

| # | Finding | Severity | Suggested fix |
|---|---|---|---|
| 1 | The initial verification note said that “Affiliation, correspondence, funding, and CRediT confirmation remain separate human gates”, contradicting the confirmed authorship record. | RESOLVED | Commit `e4af0da9` now locks the common affiliation and Yubin Lin's first- and corresponding-author roles, while leaving only funding, CRediT, and final all-author approval open. |
| 2 | The claim register consistently separates implementation facts from outcome claims, for example: “This is an implementation statement, not evidence that bidirectionality improves accuracy”. | PASS | Keep the implementation/effect distinction in the later Abstract, Introduction, Results, and Conclusion. |

## Dimension 3: English grammar

| # | Finding | Severity | Suggested fix |
|---|---|---|---|
| 1 | No article, agreement, tense, which/that, or comma-splice regression was introduced by the candidate. | PASS | Apply Rule G4 during the later full-manuscript rewrite, especially to long Results and Discussion sentences. |

## Dimension 4: LaTeX format

| # | Finding | Severity | Suggested fix |
|---|---|---|---|
| 1 | `\Title{Multi-objective Evolution Algorithm based on Non-Dominated Sorting and Bidirectional Local Search for Investment Effectiveness Strategy Optimization}` is byte-for-byte consistent with the approved title; the canonical `paper.tex` is unchanged from baseline in this stage. | PASS | Keep the title immutable. |
| 2 | The full source has 33 unique citation keys and 33 matching `\bibitem` keys, but item existence, metadata, and sentence support have not yet been independently verified. | MAJOR for submission; pre-existing | Complete Stage 2 reference verification before revising Related Work or novelty positioning. |
| 3 | Thirty-four of 36 `\cite{}` commands lack the non-breaking tilde required by reviewer Rule L1, and 38 of 61 labels contain a hyphen or space under Rule L4. | MAJOR for final format; pre-existing | Normalize citation spacing and labels only after the evidence-first content reconstruction, then recompile and check every reference. |
| 4 | An isolated three-pass `pdflatex` build of the canonical source succeeds as a 29-page A4 PDF with the locked title and author metadata and no undefined citations or references. Retained checked-in PDFs still display superseded titles, and the build log includes material overfull boxes, including one of approximately 146.26 pt. | MAJOR for final artifact consistency and layout; pre-existing | After scientific reconstruction, rebuild both PDFs from accepted sources, replace stale artifacts, correct overfull material, and visually inspect the rendered title, authors, equations, tables, and figures. |

## Dimension 5: Figure quality

| # | Finding | Severity | Suggested fix |
|---|---|---|---|
| 1 | The canonical source includes nine PNG figures, although all nine have PDF vector counterparts in the journal figure directory. | CRITICAL for final submission; pre-existing | Switch accepted figure includes to the corresponding PDFs and visually verify fonts, legends, captions, and clipping after compilation. |
| 2 | This stage changes no figure, caption, table value, or data source. | PASS for this candidate | Perform the formal figure-to-data and visual audit at the evidence and final-integrity gates. |

## Banned-vocabulary and em-dash scan

- The full canonical LaTeX source was scanned, not sampled.
- Unicode em dash: 0.
- `yet`: 3 occurrences, which reaches the reviewer skill's MAJOR threshold; all are pre-existing and should be replaced during the final prose pass.
- `excel`: 1 occurrence and `reveal`: 1 occurrence; both are pre-existing and require neutral alternatives.
- Eight `superior*` matches occur only in explicit negative or bounded statements such as “not superiority over NSGA-II”. They are evidential guardrails rather than promotional claims, but their contexts must remain negative.

## Integrity observations

- Direct data audit reproduces scenario-balanced means of 0.1627660679 for BiLo-NSGA, 0.1721313353375 for NSGA-II, and 0.1162593786625 for Pareto Local Search.
- Inspection of `local_improve` confirms that the stage-local paired delete--insert proposal modifies a copy, evaluates the pair once, and commits both changes only after acceptance. This supports atomicity for that implementation only; it does not support an accuracy gain.
- The reconstruction contract gate passes, all four reconstruction acceptance tests pass, narrative structure passes with a 183-word abstract against the 220-word limit, manuscript hygiene passes, and `git diff --check` passes after the review fix.
- No experiment was added, rerun, removed, retuned, or selectively suppressed in this stage.

## Final score

- Stage-1 candidate quality: **9/10**.
- Full-manuscript submission readiness: **not ready**; the scientific, literature, figure, artifact-consistency, layout, and later multi-round review gates remain mandatory.

## Supplemental compilation/style audit

- Three-pass `pdflatex`: PASS; 29 A4 pages; zero undefined citations/references.
- Build log: 34 overfull boxes; maximum approximately 146.26 pt.
- Raw ChkTeX findings: 182 total, comprising 115 before the bibliography and 67 in bibliography formatting. The dominant body signals are dash-length warnings (40), missing nonbreaking citation spaces (34), and intersentence-spacing warnings (17).
- ChkTeX counts are triage signals, not automatically confirmed defects; template macros, mathematics, and literal bibliographic titles require manual adjudication during the final LaTeX pass.

## Recommendation

**Accept the P2 Stage-1 candidate and continue the planned scientific reconstruction.** The candidate makes the locked identity and evidence boundaries explicit without hiding the adverse NSGA-II result or treating implemented atomicity as demonstrated effectiveness.
