# C2GES Round-3 Author-Metadata Superseding Closure

Date: 2026-08-06 (Asia/Shanghai)  
Audit mode: independent, read-only metadata provenance and post-migration identity verification  
Decision: **SCIENTIFIC_CLOSED_HUMAN_GATES_OPEN**

## Scope and supersession

This record supersedes only the **build and bundle identities** in `round3_deterministic_build_closure.md/json` and the earlier `round3_final_closure_confirmation.md/json`. It does not supersede or reopen their scientific, statistical, artifact, or visual conclusions. The identity change is fully explained by the user-authorized migration of author names, affiliations, and corresponding-author information from the paired CMC manuscript.

No manuscript, experiment, figure, table, manifest, or PDF was modified or regenerated during this closure audit. The audit read the CMC source, the author-metadata migration record, the current Applied Sciences TeX/PDF, the v2 deterministic-build audit, the current bundle manifest, and the existing verifier evidence.

## Author-metadata provenance

The authoritative migration record is `AUTHOR_METADATA_MIGRATION_2026-08-06.json`, 1,372 bytes, SHA-256 `731A55617261FCEBA0E21746A55F94B3020AA86F6AEEA0759D424AD99600D94D`. It records the user's explicit authorization to reuse metadata from the corresponding CMC manuscript.

The C2GES source is `paper_projects/2026_c2ges_engineeringletters/source/manuscript_cmc/paper_cmc.tex`, 17,697 bytes, SHA-256 `83E8DAA68DC46BD20916B4D801C277BF22F4F1D19464CB0A73A0020B1EE62848`. Direct comparison confirms:

| Field | CMC source | Current Applied Sciences TeX | Result |
|---|---|---|---|
| Authors and order | Bijing Liu; Yong Yang | Bijing Liu; Yong Yang | Match |
| Affiliation indices | Both authors: 1, 2 | Both authors: 1, 2 | Match |
| Affiliation 1 | NARI Group Corporation (State Grid Electric Power Research Institute), Nanjing 211106, Jiangsu Province, China | Same | Match |
| Affiliation 2 | Beijing Kedong Electric Power Control System Co., Ltd., Beijing 100080, China | Same | Match |
| Corresponding author | Yong Yang | Yong Yang | Match |
| Corresponding e-mail | `yangyong1@sgepri.sgcc.com.cn` | `yangyong1@sgepri.sgcc.com.cn` | Match |

No non-corresponding-author e-mail, ORCID, funding grant, CRediT allocation, conflict statement, acknowledgment, ethics confirmation, or AI-use declaration was inferred. The author identity/affiliation/correspondence gate is therefore resolved within the explicit authorization, while the remaining author-attestation gates stay open.

## Current deterministic manuscript identity

| Artifact | Bytes | Pages | SHA-256 |
|---|---:|---:|---|
| `manuscript_applsci/paper_applsci.tex` | 58,318 | -- | `4875F4251C43C2A6395DB36E0EDA4E10CEF25EEEB2CA4DD7E6DD62F559A95D7D` |
| `manuscript_applsci/build/paper_applsci.pdf` | 763,005 | 22 A4 | `2694417B9D48F14C83CE0F54532DC14A05783BBA534BFAA3E5D2D0B7CA7C90CF` |

`DETERMINISTIC_BUILD_AUDIT.json` is the authoritative v2 author-metadata build record: 1,656 bytes, SHA-256 `B21E8194D772AC6E6B9499ADAF62564F2FEFC72B185CD94FCDFC0195A55245C2`. With `SOURCE_DATE_EPOCH=1785888000` forced, both C2GES builds produced the exact PDF identity above; status is `PASS`.

The current build log is 62,118 bytes, SHA-256 `D0973D0759D751CA372876B2F1DFB7AFA0A5B2761384546A4E6982669D3F4249`; its read-only scan reports zero LaTeX errors, undefined references/citations, overfull boxes, and underfull boxes. Pagination remains 22 pages, so the prior all-page visual conclusion is retained.

## Current bundle identity and verifier evidence

The authoritative manifest is `manuscript_applsci/reproducibility/bundle_manifest.json`:

- SHA-256: `7FD1C0F60FE751071491FD9C6D5C4565E31109AC1AB64542413EF0CF2DAC1F5A`
- size: 3,076,681 bytes
- status: `complete_local_manifest_generated_and_verified_after_manuscript_build`
- artifacts: **11,378**
- total bytes: **1,110,025,006**

Its unique TeX and PDF entries exactly match the direct identities above. The v2 deterministic-build audit records the corresponding bundle verifier status as `PASS`, with 11,378 artifacts, 1,110,025,006 bytes, and all five gzip checks passing. This closure uses that existing post-migration verifier evidence and does not rerun or rewrite the bundle.

## Scientific closure continuity

All three review rounds, response matrices, Round-3 closure review, and the prior zero-open-issue final confirmation remain present. The author-only metadata migration and the associated cleanup of obsolete author-identity wording do not alter experiments, statistics, claims, figures, tables, bibliography, gzip provenance, or the prospective “toward power-grid NERC” evidence boundary. Accordingly:

- scientific recomputation required: **no**;
- local scientific blockers: **0**;
- prior scientific closure: **retained**;
- build/bundle identity: **superseded by this record**.

`W7_ASSEMBLY_REPORT.md` still describes the historical 18-page assembly and its then-unresolved author fields; `round1_response_matrix.md` likewise preserves the Round-1-era partial-resolution status and original smaller bundle count. These are provenance records, not current identity authorities. They should either remain explicitly historical or receive a clearly labeled current-status addendum; their stale current-tense author/build wording must not be used for submission-state claims. The current authority is the migration record, v2 deterministic-build audit, current manifest, and this superseding closure.

## Remaining human gates

Eight `W7_FRONT_MATTER` markers remain, all outside the now-resolved author identity/affiliation/correspondence fields:

1. Author-approved CRediT contributions and initials.
2. Funding organization, grant number, and funder-role statement.
3. Author confirmation of ethics and informed-consent wording.
4. Author-approved acknowledgments, if any.
5. Each author's conflict-of-interest disclosure.
6. Final author-approved generative-AI-use disclosure.
7. License and redistribution review; the irrecoverable historical Hugging Face revision must remain disclosed and must not be invented.
8. Authorized public deposit and a permanent repository URL/DOI.

Non-corresponding-author e-mail addresses and ORCID identifiers were not present in the source and were not fabricated; authors may add them if required or desired. Independent NERC expert annotation remains conditional: it is not required for the current prospective claim boundary, but it is required before any stronger validated quantitative power-grid/NERC performance claim.

## Final determination

The CMC source, explicit migration record, Applied Sciences author block, deterministic two-build identity, current bundle manifest, and existing verifier evidence agree. The metadata migration is traceable and introduces no scientific change. Decision: **SCIENTIFIC_CLOSED_HUMAN_GATES_OPEN**; local scientific blockers: **0**; submission-ready: **no**.
