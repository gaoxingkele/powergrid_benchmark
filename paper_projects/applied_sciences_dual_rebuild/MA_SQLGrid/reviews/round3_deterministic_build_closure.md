# MA-SQLGrid Deterministic-Build Superseding Closure

Date: 6 August 2026  
Auditor: `/root/ma_round3_closure_a`  
Decision: **SCIENTIFIC_CLOSED_HUMAN_GATES_OPEN**

## Supersession statement

This read-only audit is the authoritative Round-3 closure snapshot after deterministic rebuilding. It **supersedes only the PDF identity** recorded by `round3_closure_audit_a.md/json` and `round3_closure_audit_b_final.md/json`:

- historical PDF: 25 pages, 664,609 bytes, SHA-256 `1A2220381D18E2F5B037320B14377E6010A095F6A9AFAE834F0B3CF6C1FA7E4F`;
- current deterministic PDF: 25 pages, 664,597 bytes, SHA-256 `789696175B80A1CE2778524F0D293A54287233097F4F7235C7FBD5D2AD92A0A4`.

The old closure files remain unchanged as historical records. Their scientific findings are not reversed.

## Authoritative current identity

- TeX: 71,379 bytes; SHA-256 `E8FECF6C8D4223BA75B87FCDAE97EEE6A66035BE500CBD9B0B3991752644C420`.
- PDF: 25 pages, 664,597 bytes; SHA-256 `789696175B80A1CE2778524F0D293A54287233097F4F7235C7FBD5D2AD92A0A4`.
- `round3_author_response.md/json`, `round2_author_response.md/json`, and `W10_ASSEMBLY_REPORT.md` all record this current PDF identity and the unchanged TeX identity.

No manuscript source, experimental artifact, or build output was changed during this audit, and the manuscript was not recompiled.

## Deterministic-build evidence

`DETERMINISTIC_BUILD_AUDIT.json` (SHA-256 `03E92AD6D91EAF36B277EE484F01B28B58AD11D5C5D2602726DDF1E591F2A86F`) records:

- fixed `SOURCE_DATE_EPOCH=1785888000` (`2026-08-05T00:00:00Z`);
- `FORCE_SOURCE_DATE=1`;
- two separate MA-SQLGrid builds with the identical SHA-256 `789696175B80A1CE2778524F0D293A54287233097F4F7235C7FBD5D2AD92A0A4` and identical size 664,597 bytes;
- current PDF equality with that deterministic pair.

The current build script contains the same fixed-epoch settings. The retained final LaTeX log reports 25 pages and 664,597 bytes, with zero LaTeX errors, zero undefined references, and zero overfull boxes. Four underfull-box and two PDF-string warnings are non-blocking.

## Semantic and portable release closure

The deterministic PDF change did not alter the TeX or semantic evidence lineage:

- The 18-artifact portable manifest has SHA-256 `63C6E185678F03AD4C710CDB3AB20BA36F2E741A62BC5AE36BB09CB18534990A`.
- Read-only recomputation found zero missing, byte-mismatched, or hash-mismatched artifacts and a matching root marker.
- Local verification remains `PASS`, with 19 files including the root marker.
- The preserved clean-copy root exists; an independent read-only pass over its 19 files found zero hash or byte mismatches. Its recorded report remains `PASS` and binds the same manifest SHA.
- Registered invariants remain 25,920 atomic rows, 1,440 suite rows, 528 eligible predictions/7,920 primary semantic rows, 912 held predictions/16,416 diagnostic rows, 15 semantic states, three physical diagnostic states, nine Holm tests, and 1,440/1,440 T0 continuity.

No internal scientific or reproducibility blocker remains.

## Five human gates still open

All five items below are **HUMAN_GATE_OPEN**, not internal scientific failures:

1. Explicit human authorization and execution of the frozen 5,000-call BIRD comparator; it remains `FROZEN_NOT_RUN` with zero formal calls and no imported BIRD result.
2. Qualified dual review/adjudication of the external grid pairs and a sealed follow-up set; current automatic candidates remain diagnostic only.
3. Author identities, affiliations, correspondence, and CRediT approval.
4. Author-approved funding, conflicts, acknowledgments, ethics/consent, and AI-use declarations.
5. GridDB/derivative license review followed by an authorized permanent repository DOI or URL.

Therefore, scientific Round-3 closure remains valid under the deterministic PDF identity, while submission readiness remains false until these five human gates are completed.
