# Manual Candidate Review, Round 1

Candidate branch head reviewed: `68cd1f233f9f`

## Summary

- Stage-2 verdict: PASS after one reviewer-driven literature addition.
- Full-manuscript readiness: NOT READY; later experimental and release gates remain mandatory.
- CRITICAL: 0 within the literature stage.
- MAJOR: 1 deferred.
- MINOR: 1.

Top fixes completed: removed literature-wide absence claims, distinguished atomic substitution from separate edits, and filled the missing VNS portfolio cell with verified ref34.

## Dimension 1: Macro logic

| # | Finding | Severity | Suggested fix |
|---|---|---|---|
| 1 | The revised gap says, “the present audit does not establish an exhaustive absence claim for atomic project substitution”. This correctly converts novelty rhetoric into implementation positioning. | PASS | Preserve the scoped claim. |
| 2 | Ref34 now shows that variable-neighborhood search has been applied to uncertain project portfolio selection. Its stochastic NPV/risk setting is not a matched multi-objective grid benchmark. | PASS | Cite it as a neighboring method only, as currently written. |
| 3 | The paper reports that the proposed method loses four of eight corrected NSGA-II contrasts and wins none. | MAJOR, deferred | Later narrative/evidence stages must retain the negative result and frame the contribution around operator semantics and bounded comparator evidence, not performance superiority. |

## Dimension 2: Writing details

The main Related Work and standalone `related_work.md` now use the same cautious taxonomy. One generated submission-preview copy remains structurally different from the canonical source, so the final artifact stage must regenerate it rather than hand-maintain it.

## Dimension 3: English grammar

No new article, agreement, or tense error was found in the added Panadero sentence. It contains several clauses and should be reconsidered under G4 during the final prose pass, but it is currently readable.

## Dimension 4: LaTeX format

After adding ref34, three `pdflatex` passes produced a 29-page A4 PDF with zero undefined citations or references. The log contains 34 overfull boxes, including long scenario identifiers and a raw URL; these are a final-layout MAJOR if still present at release.

## Dimension 5: Figure quality

Figure content was not changed. Current figures are PNG; the release gate must inspect effective DPI, font size, and grayscale/color-blind legibility.

## Banned-vocabulary and em-dash scan

The full canonical source was scanned. Unicode em-dash count: 0. “Superior/superiority” occurrences are mostly explicit denials, not promotional claims. No Stage-2 AI-tone violation.

## Citation integrity

The original DOI inventory was independently re-queried with no title, year, or author mismatch. Ref34 was verified through Crossref and the Universitat Autònoma de Barcelona institutional record before import. Its abstract supports VNS plus Monte Carlo simulation for uncertain project portfolio selection; it does not support atomicity or matched performance.

## Final score

Stage 2: 8.5/10.

## Submission recommendation

- Accept Stage 2.
- Continue to protocol and evidence strengthening before submission.
