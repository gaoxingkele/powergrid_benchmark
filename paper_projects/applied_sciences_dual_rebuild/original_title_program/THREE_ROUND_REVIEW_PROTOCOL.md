# Three-Round Independent Review and Revision Protocol

## Scope

This protocol applies separately to the original-title versions of C2GES and
MA-SQLGrid.  A manuscript advances only when its PDF, source, evidence ledger,
figures, tables, and reproducibility package are frozen together for the round.
Reviewers assess the frozen round; later edits are recorded in a response
matrix and a new round directory.  Earlier rounds remain immutable.

## Independent reviewer roles

Each round uses three fresh review assignments.  Reviewers must not edit the
manuscript they review.

1. **Methods and statistics reviewer**: experimental units, splits, baselines,
   ablations, multiplicity, uncertainty intervals, denominator consistency,
   leakage, negative results, and reproducibility.
2. **Power-grid application reviewer**: domain terminology, operational scope,
   data representativeness, safety boundaries, engineering value, and whether
   the conclusions exceed the evidence.
3. **Applied Sciences and integrity reviewer**: journal fit, novelty, section
   balance, figure/table legibility, citation support, authorship/back matter,
   data availability, title--abstract--conclusion consistency, and unsupported
   or misleading claims.

## Required review output

Every reviewer reports:

- recommendation: reject / major revision / minor revision / ready for final audit;
- five most serious issues, ordered by decision impact;
- a claim--evidence audit with exact section or line locations;
- an experiment audit identifying required, desirable, and unjustified reruns;
- a figure/table audit;
- reproducibility and ethics findings;
- concrete revision instructions and acceptance tests.

Reviewers must distinguish a blocking defect from an optional improvement.  A
review may not invent missing results or request that diagnostic, silver, or
post-hoc evidence be relabeled as gold or prospective evidence.

## Round gates

### Round 1 to Round 2

- Both manuscripts compile without fatal errors, unresolved citations, or
  unresolved cross-references.
- All quantitative claims appear in the evidence ledger and trace to retained
  artifacts.
- Unsupported claims inherited from the source DOCX are absent.
- Every blocking reviewer item has an owner and a planned resolution.

### Round 2 to Round 3

- Blocking Round 1 items are resolved or explicitly declined with evidence.
- Added experiments have frozen protocols, immutable outputs, and independent
  recomputation where feasible.
- Figures and tables have provenance records and match the text numerically.
- The abstract and conclusion make no stronger claim than the results section.

### Round 3 to submission candidate

- Three reviewers find no unresolved blocking integrity, evidence, or build
  defect.
- A final response matrix closes every Round 3 item.
- PDF text, LaTeX source, bibliography, code, data manifests, and package hashes
  are mutually consistent.
- Corresponding-author email remains an explicit manual placeholder until the
  authors supply it; the package is labelled not ready for portal upload while
  any required manual field remains incomplete.

## Revision records

For each manuscript and round, retain:

- `reviews/reviewer_methods_statistics.md`;
- `reviews/reviewer_power_grid_application.md`;
- `reviews/reviewer_journal_integrity.md`;
- `REVISION_RESPONSE_MATRIX.md` with item, decision, change, file/line, and
  verification columns;
- `ROUND_AUDIT.json` containing manuscript, PDF, figure, table, bibliography,
  and evidence-manifest SHA-256 values.

The final audit reports limitations and unresolved manual actions.  “Three
rounds completed” means three frozen review--revision cycles, not three passes
over the same draft.
