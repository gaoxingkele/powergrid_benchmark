# MA-SQLGrid Round-1 manuscript revision report

Date: 2026-08-05  
Scope: `manuscript_applsci/` only  
Decision: **PASS for agent-resolvable Round-1 integration; external human/license/repository gates remain open.**

## Preserved author edits

- Title retained verbatim: **MA-SQLGrid: A Controlled Factorial Study of Context Grounding for Text-to-SQL over a Power-Grid Maintenance Database**.
- The revised abstract present at task start was retained verbatim.
- No author identity, affiliation, contribution, funding, conflict, acknowledgment, AI-use declaration, license, repository URL, or DOI was invented.

## Evidence integrated

- `canonical_v2_reanalysis/`: corrected common-target projected-column endpoint; unchanged 1440 execution outcomes; 70-cluster bootstrap; cluster sign-flip/Holm inference; prompt/context telemetry; factor-field and offline selector audits.
- `round1_revision_assets/`: executed Algorithm 1, prompt/factor invariance audit, GridDB data card, DKASQL qualitative comparator, and three reviewed framework figures.
- `public_baseline_protocol/`: BIRD Mini-Dev feasibility and protocol-freeze **draft** only; no BIRD database/model result is presented.
- Both independent Round-1 methods/statistics and domain/venue reviews were used as the revision checklist.

## Major corrections

1. Replaced the inaccurate isolated `schema scope` interpretation with the executed **bundled context-package factor**:
   - full package: complete eight-table DDL + global permitted-value dictionary;
   - compact/domain-grounded package: selected schema + retained joins + question-matched values + handcrafted normalization/predicate rules.
2. Replaced generic `answer-shape hint` language with **GridDB-tailored composite structural/SQL-operation hint** and disclosed its projected-column, row-granularity, ordering, aggregation, grouping/HAVING, exact-projection, and LIMIT content.
3. Replaced the condition-dependent structural endpoint with one **common-target projected-column diagnostic** applied identically in all cells and both backbones. The endpoint requires successful execution but does not validate row granularity, ordering, or semantics.
4. Replaced inferential question-level McNemar/Holm use with 100,000 cluster-unit sign flips and three prespecified eight-test Holm families. McNemar is retained only as descriptive sensitivity information.
5. Removed all former structural main-effect values and the erroneous Granite p-value transcription. A stale-pattern scan finds none of the old values or old table/figure references.
6. Added Algorithm 1 for the exact one-call executed path, including gold isolation, first-candidate parser boundary, safety validation, execution, ledger writing, and offline-only scoring.
7. Added a GridDB data-card narrative: 8 tables, 98 rows, split/difficulty, overlapping SQL features, 70 clusters, empty-result cases, exposure, and unresolved redistribution permission.
8. Added prompt excerpts and a factor audit describing invariant fields, bundled fields, corpus tailoring, and observed presence counts for matched values and normalization hints.
9. Added prompt-token and selector-coverage results: tokenizer-specific input counts, six selected tables, 16.68 mean selected columns, 0.9986 mean offline gold-table recall, and 0.9467 mean offline gold-column recall. These are explicitly diagnostic, not controlled latency or online selector claims.
10. Added a qualitative DKASQL comparison table. The manuscript states that no official implementation/environment lock was located and makes no reproduction, superiority, or same-environment numerical claim.
11. States explicitly that the BIRD plan is a draft freeze only: no database archive, preflight, or baseline model run has been completed.
12. Replaced the three framework diagrams with Round-1 reviewed versions and replaced the main results with the three canonical v2 figures and two corrected v2 tables.

## Revised quantitative interpretation

- Qwen composite-hint effect:
  - execution: +0.2306, cluster-bootstrap 95% CI [0.0573, 0.4343];
  - common projected columns: +0.4083 [0.2115, 0.6122].
- Granite composite-hint effect:
  - execution: +0.1583 [-0.0207, 0.3689];
  - common projected columns: +0.3556 [0.1352, 0.5793].
- Execution package--hint three-way modifier: +0.1889 [0.0088, 0.4286].
- Neither backbone supports an independently positive compact/domain-grounded package execution effect.
- The former apparent cross-backbone structural heterogeneity disappears under the common-target correction.

## Build and evidence verification

- Verifier: `python scripts/verify_manuscript.py` -> **PASS**.
- Verified v2 manifest: 26 files.
- Verified figures: 6 (three Round-1 framework PDFs and three byte-identical v2 result PDFs).
- Verified citation keys: 17; missing citations: 0.
- PDF: `build/paper_applsci.pdf`.
- PDF pages: 19.
- Extracted PDF token-like word count (front matter and references included): 8,798.
- PDF bytes: 481,855.
- PDF SHA-256: `ac63690458ee3f208500780cd6b19fbf0e49bc93ba2151a58b608fc87af8c9b8`.
- LaTeX final log: 0 overfull boxes, 0 undefined citations/references, 0 multiply defined labels, 0 LaTeX errors; four underfull boxes from long monospaced model/repository strings and two hyperref PDF-string warnings from the preserved abstract's math notation.
- Manual page-scale inspection covered Algorithm 1, framework figure, corrected cell/effect tables, and all three v2 result figures; no clipping or illegible main asset was observed.

## Open gates not resolvable by manuscript editing

- Author names, affiliations, e-mails, corresponding author, and CRediT approval.
- Funding, conflicts, acknowledgments, institutional-review wording, and final generative-AI disclosure.
- GridDB redistribution permission and source-specific review for derived RTS-GMLC/SimBench artifacts.
- License-filtered public archive and permanent DOI/URL.
- Two independent human reviews/adjudication of the 91 visible external candidates.
- A genuinely new sealed grid-domain confirmatory set.
- Prospectively signed and executed BIRD same-environment baselines; the current draft is not evidence.
- Controlled latency/memory/energy study and prospective value-grounding/validator experiments.

These gates remain explicit in the manuscript and must not be marked complete by an automated reviewer.
