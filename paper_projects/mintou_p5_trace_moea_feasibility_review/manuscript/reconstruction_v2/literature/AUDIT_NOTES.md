# Literature Audit Notes

`LITERATURE_EVIDENCE_MATRIX.csv` binds each retained source to the exact manuscript paragraph and sentence it supports. `REFERENCE_VERIFICATION.csv` supplies the corresponding DOI or authoritative record and the source-level evidence location (metadata record, abstract, methods, or conclusions). Read together, those two files are the claim-to-source locator.

An independent candidate review on 2026-09-03 re-queried every DOI-bearing entry through the Crossref API and found no title, year, or author mismatch. That batch result verifies bibliographic identity only. It does not independently certify every full-text interpretation; the matrix therefore retains narrow claim language and the evidence locator used during the source-level audit.

## Corrections made

- Former `ref28`, an unpublished companion manuscript without a public identifier or independently verifiable record in this worktree, was removed from the bibliography. Companion-study statements remain explicitly internal shared-assets declarations and are not external literature evidence.
- `ref28` now identifies Liang et al.'s verified constrained-MOEA survey (DOI `10.1109/TEVC.2022.3155533`).
- The Related Work taxonomy no longer misclassifies NSGA-III as decomposition-based; NSGA-II, MOEA/D, and NSGA-III are described as dominance, decomposition, and reference-point families, respectively.
- The malformed proceedings markup for `ref27` was corrected without changing its bibliographic identity.
- `ref34` and `ref35` were added as bounded Energies comparators for physical validation and recent NSGA-II-based power-system planning.

## Evidence limitation

The literature establishes comparator designs and validation requirements. It supplies no TRACE-MOEA experiment run, expert label, audited project cost, AC-feasibility result, N-1 result, deployment observation, or evidence that the proxy ranking will survive later validation. The canonical `p5_s4` protocol remains `NO_RESULTS`.
