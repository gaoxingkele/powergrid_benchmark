# Stage 2 Batch Acceptance Packet

Date: 2026-09-04
Scope: verified literature maps for the four locked-title manuscripts
Decision requested: accept or reject each Stage-2 candidate branch

## Candidate heads

| Paper | Stage | Candidate branch head | Stage contract |
|---|---|---|---|
| P1 | `p1_v2_s02_verified_literature_map` | `d76ee394f6a0` | PASS |
| P2 | `p2_v2_s02_verified_literature_map` | `68cd1f233f9f` | PASS |
| P3 | `p3_v2_s02_verified_literature_map` | `c49e16412e56` | PASS |
| P4 | `p4_v2_s02_verified_literature_map` | `c138f7228c9e` | PASS |

These are branch-head commits after independent review fixes. The Paper Harness runtime records the original candidate commits, but `accept` merges the current candidate branch head.

## Independent evidence checks

- All four locked titles remain byte-for-byte present in both `MANUSCRIPT.md` and canonical `journal_submission/paper.tex`.
- The current inventories contain 131 DOI-bearing rows and 114 unique DOIs.
- The initial 130 DOI rows were independently queried through Crossref; normalized title/year comparison and author-token comparison found no mismatch.
- P2 ref34 was added during review and separately verified through Crossref plus the Universitat Autònoma de Barcelona institutional publication record.
- Four P4 arXiv map records were resolved directly through the arXiv API.
- Metadata identity is explicitly separated from abstract/method/full-text sentence support in the revised audit notes.

## Reviewer-driven changes

### P1

- Removed the unverifiable unpublished companion citation as external literature evidence.
- Corrected the NSGA-III taxonomy and bounded all comparator claims.
- Added two recent power-system planning comparators without transferring their results to the proxy benchmark.
- Added an explicit note that DOI matching does not certify full-text interpretation.

### P2

- Removed exhaustive absence claims about atomic substitution.
- Defined atomic substitution as one accepted-or-rolled-back delete-insert proposal.
- Added Panadero et al. (2020), DOI `10.1007/s10732-018-9367-z`, as a scope-limited VNS project-portfolio neighbor.
- Synchronized the main manuscript, canonical LaTeX, submission preview, standalone Related Work, evidence matrix, reference inventory, search log, and comparator map.

### P3

- Separated optimizer-method citations from engineering-validation evidence.
- Marked transmission-expansion and economic-dispatch sources as analogues rather than direct distribution-planning validation.
- Preserved the unresolved requirement to separate parameter adaptation from strategy adaptation.
- Recorded the independent metadata audit without upgrading it to engineering evidence.

### P4

- Added foundational GCN/HNN/HGCN and nearby learned-graph/evaluation sources.
- Removed priority and field-wide absence claims.
- Preserved the critical boundary that the current baseline is not yet the locked-title GCN/HGCN method.
- Recorded independent DOI and arXiv identity checks.

## Compile evidence

Canonical Stage-2 LaTeX sources compiled successfully with three `pdflatex` passes:

| Paper | Pages | Undefined citations/references | Overfull boxes |
|---|---:|---:|---:|
| P1 | 28 | 0 | 32 |
| P2 | 29 | 0 | 34 |
| P3 | 29 | 0 | 20 |
| P4 | 25 | 0 | 1 |

The overfull-box counts are deferred to the final layout gate; they do not invalidate the Stage-2 literature artifacts.

## Stage-scoped reviewer recommendation

All four Stage-2 candidates are recommended for acceptance. This recommendation does not mean the manuscripts are ready to submit. The main deferred scientific risks are:

- P1: proxy objectives still require action-aligned electrical validation or strict claim scoping.
- P2: the negative NSGA-II result must remain visible; later work cannot reframe it as superiority.
- P3: parameter and strategy adaptation need separate controls; AC mapping needs seed-replicated, action-aligned evidence.
- P4: the locked title remains unsupported until a genuine hyperbolic graph-convolutional forecaster and matched controls are implemented and evaluated.

After explicit acceptance, the next runnable stages are the four Stage-3 method/data/implementation contracts.
