# Dual Applied Sciences Rebuild: Author-Metadata Completion Audit

Audit snapshot: 2026-08-06 00:48 Asia/Shanghai  
Decision: **both papers are internally scientifically closed for their bounded claims; neither is submission-ready**

This audit supersedes the previous dual audit's build identities. The user authorized reuse of author and affiliation information from the paired CMC manuscripts; names, ordering, both affiliations, corresponding-author identity and the available corresponding email are now integrated. Earlier review and closure records remain historical evidence.

## Current authoritative snapshots

| Paper | TeX | Deterministic PDF | Independent closure | Submission-ready |
|---|---|---|---|---|
| MA-SQLGrid | 71,708 bytes; `2724D78D...0EC3` | 25 pages; 664,506 bytes; `CF67243F...F96F` | `SCIENTIFIC_CLOSED_HUMAN_GATES_OPEN`; identity gate closed; 0 local scientific blockers | No |
| C2GES | 58,318 bytes; `4875F425...5D7D` | 22 pages; 763,005 bytes; `2694417B...90CF` | `SCIENTIFIC_CLOSED_HUMAN_GATES_OPEN`; identity gate closed; 0 local scientific blockers | No |

Both build scripts now set `SOURCE_DATE_EPOCH=1785888000` and `FORCE_SOURCE_DATE=1`. Two consecutive builds of each paper produced byte-identical PDFs. Full identities are recorded in `DETERMINISTIC_BUILD_AUDIT.json`.

## MA-SQLGrid

The current bounded manuscript is internally complete. Its evidence includes the 1,440-prediction factorial study, prospective component experiment, 25,920-row multi-state SQL reliability study, fixed nine-contrast family, exact and resampling-based inference, two independent post-score audits, and a portable 19-file verified release. Three review rounds and a new independent post-determinism closure are complete.

The current authoritative closure is `MA_SQLGrid/reviews/round3_author_metadata_closure.json` (SHA-256 `2563C22A...EE56`). It confirms exact CMC-to-Applied-Sciences metadata matching and supersedes only prior build identities, not scientific findings.

Open gates remain:

- BIRD is `FROZEN_NOT_RUN`: 500/500 gold preflight, 5,000 planned generation calls, 0 formal calls. Running it requires explicit human authorization.
- The 91 external grid candidates still require qualified dual review, disagreement adjudication, and a genuinely sealed follow-up set before stronger external-domain claims.
- CRediT, funding, conflicts, acknowledgments, ethics/consent and final AI-use declarations still require author approval; identity, affiliations and correspondence are resolved.
- GridDB/derivative redistribution requires a human license decision.
- A permanent public repository URL or DOI is absent.

## C2GES

The current prospective “toward power-grid NERC” manuscript is internally complete without claiming validated quantitative NERC deployment performance. Its five-seed three-protocol study, canonical predictions, exploratory extraction, genuine ablations, cross-encoder add-on, multiplicity-controlled statistics, framework/result assets, three review rounds, and visual audit are present.

The current reproducibility bundle contains 11,378 artifacts totaling 1,110,025,006 bytes. Every manifest SHA-256 and all five canonical gzip checks pass; the manifest SHA-256 is `7FD1C0F6...1F5A`. The authoritative closure is `C2GES/reviews/round3_author_metadata_closure.json` (SHA-256 `39A611E0...8427`).

Open gates remain:

- Approved CRediT, funding, conflicts, ethics/consent, acknowledgments, and final AI-use disclosure; identity, affiliations and correspondence are resolved.
- FEVER/NERC-derived artifact redistribution and attribution review.
- A permanent public repository URL or DOI.
- Independent NERC expert annotation is conditional on promoting the present prospective claim into a validated power-grid performance claim.

## Ten-paper Applied Sciences benchmark

The local reference corpus contains 10 PDFs and 10 JATS XML files. Verified medians are 24 pages, 7,098 body words, 5 top-level sections, 26 numbered formulas, 1 evaluation dataset, 9 figures, 5 tables, and 2 framework diagrams. Both rebuilt papers are structurally within this observed range while retaining topic-specific experimental depth.

## Final determination

The deterministic source/PDF identities, migrated author metadata, experiment ledgers, figures, statistics, three-round review chains, and independent superseding closures now agree. No local scientific blocker remains for either manuscript's present bounded claims. Submission is still blocked because BIRD and qualified external validation remain incomplete for MA-SQLGrid, and both manuscripts still require remaining author attestations, license clearance, and permanent deposit identifiers.
