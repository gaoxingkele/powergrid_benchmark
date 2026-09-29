# Manual Candidate Review, Round 1

Candidate branch head reviewed: `c49e16412e56`

## Summary

- Stage-2 verdict: PASS.
- Full-manuscript readiness: NOT READY.
- CRITICAL: 0 within the literature stage.
- MAJOR: 2 deferred.
- MINOR: 1.

Top fixes: keep generic optimizer citations separate from engineering validation, avoid treating transmission/economic-dispatch analogues as distribution-planning proof, and isolate parameter adaptation from strategy adaptation experimentally.

## Dimension 1: Macro logic

| # | Finding | Severity | Suggested fix |
|---|---|---|---|
| 1 | The map states that refs 18 and 19 are “transmission-expansion and economic-dispatch analogues”. This is the correct evidence boundary. | PASS | Preserve the analogue label in every manuscript version. |
| 2 | The manuscript admits that the AC panel uses “one run-index-0 compromise per method and selected seed block”. | MAJOR, deferred | Later evidence work needs seed-replicated, action-aligned nodal mapping before any optimizer-level physical-validity claim. |
| 3 | The FixedDE control changes parameter and strategy adaptation together. | MAJOR, deferred | Add separate controls for parameter-only adaptation and strategy-only adaptation, with a declared estimand and common seeds. |

## Dimension 2: Writing details

The Related Work now closes with an evidence-bounded gap rather than claiming direct engineering validation. Several paragraphs are dense source catalogues and should be split during prose polish.

## Dimension 3: English grammar

No new blocking grammar defect was introduced. Long multi-clause sentences in Section 2 should be split under G4. Related-work tense is acceptable under G3.

## Dimension 4: LaTeX format

Three `pdflatex` passes produced a 29-page A4 PDF with zero undefined citations or references. The log contains 20 overfull boxes. Final layout repair remains required.

## Dimension 5: Figure quality

Figure review is deferred. Current graphics are PNG, so effective resolution and label legibility must be checked at final artifact review.

## Banned-vocabulary and em-dash scan

The full source was scanned. Unicode em-dash count: 0. “Innovative” occurs once and should be neutralized in the final polish pass; “superiority” occurs in explicit boundary statements.

## Citation integrity

All DOI-bearing P3 citations were independently re-queried with no title, year, or author mismatch. The map-only arXiv source was resolved through the arXiv API. The search log now states that these checks establish identity only and do not validate engineering claims.

## Final score

Stage 2: 8/10.

## Submission recommendation

- Accept Stage 2.
- Require the two-factor adaptation controls and stronger physical validation before a submission-ready verdict.
