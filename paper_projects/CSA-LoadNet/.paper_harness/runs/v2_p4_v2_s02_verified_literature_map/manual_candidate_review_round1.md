# Manual Candidate Review, Round 1

Candidate branch head reviewed: `c138f7228c9e`

## Summary

- Stage-2 verdict: PASS.
- Full-manuscript readiness: NOT READY.
- CRITICAL: 1 deferred to the title-method reconstruction stages.
- MAJOR: 1 deferred.
- MINOR: 1.

Top fixes: implement and test the locked-title GCN/hyperbolic method, retain the matched rolling-origin null result, and separate graph benefit from graph-parameterization benefit.

## Dimension 1: Macro logic

| # | Finding | Severity | Suggested fix |
|---|---|---|---|
| 1 | The abstract says, “The current CSA-LoadNet is a baseline for the locked-title rebuild, not a GCN or HGCN” and “No GCN or HGCN experiment or result is reported.” This directly conflicts with the locked title. | CRITICAL, deferred | Later method/protocol/evidence stages must add an actual graph-convolutional model in hyperbolic space and matched Euclidean/no-graph controls, or the locked title cannot be supported. |
| 2 | The literature map now includes foundational GCN, hyperbolic neural network, and HGCN sources but correctly notes that they are graph-task foundations rather than load-forecasting evidence. | PASS | Preserve this boundary. |
| 3 | The rolling-origin matched target-self result is unresolved at Holm-adjusted p = 0.984. | MAJOR, deferred | Do not let fixed-split gains override the matched temporal estimand; design the new GCN/HGCN tests around rolling origins and common seeds. |

## Dimension 2: Writing details

The revised Related Work removes field-wide frequency and priority claims and states a concrete comparison need. This materially improves scientific tone. A few paragraphs remain long and should be split during final polish.

## Dimension 3: English grammar

No new blocking grammar defect was introduced. Long sentences with multiple qualification clauses should be split under G4. Related-work tense is acceptable under G3.

## Dimension 4: LaTeX format

Three `pdflatex` passes produced a 25-page A4 PDF with zero undefined citations or references. Only one overfull box remains, the best layout status in the batch.

## Dimension 5: Figure quality

The architecture figure still depicts CSA-LoadNet rather than the locked-title GCN/HGCN method. That is part of the deferred CRITICAL reconstruction. Current figures are PNG and require effective-resolution inspection at release.

## Banned-vocabulary and em-dash scan

The full canonical source was scanned. Unicode em-dash count: 0. “Superior/superiority” occurs primarily in null or negative boundary statements. One “innovative” occurrence should be replaced with a neutral descriptor during final polish.

## Citation integrity

All DOI-bearing P4 records were independently re-queried with no title, year, or author mismatch. Four arXiv map records were resolved directly through the arXiv API. Metadata identity remains separate from sentence-level support.

## Final score

Stage 2: 8.5/10. Overall manuscript cannot receive a submission-ready score while the title-method contradiction remains.

## Submission recommendation

- Accept Stage 2.
- Do not submit until the GCN/hyperbolic reconstruction and matched controls are complete.
