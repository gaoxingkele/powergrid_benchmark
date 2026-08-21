# MA-SQLGrid Round-3 Closure Audit B

Date: 5 August 2026  
Role: second independent closure auditor  
Mode: read-only evidence audit; no manuscript, result, or author-response source was edited  
Decision: **BLOCK_CLOSURE**

## Outcome

The scientific Round-3 revision is internally closed and the remaining substantive gates are correctly restricted to human/author-controlled work. However, the byte identity asserted by the Round-3 author response is no longer the identity of the current compiled PDF. Closure is therefore blocked on one local snapshot-synchronization defect, not on a scientific contradiction.

## Independent checks

- `scripts/verify_manuscript.py`: **PASS**, reporting 26 v2, 15 v3, and 4 component-analysis manifest outputs, 9 figures, and 23 citation keys.
- Full independent LaTeX/BibTeX build: **PASS**, 25 pages and 664,609 bytes. The final log has zero LaTeX errors, zero undefined citations/references, and zero overfull boxes (four underfull warnings only).
- TeX SHA-256: `E8FECF6C8D4223BA75B87FCDAE97EEE6A66035BE500CBD9B0B3991752644C420`, matching the response.
- Current PDF SHA-256 after the independent rebuild: `1A2220381D18E2F5B037320B14377E6010A095F6A9AFAE834F0B3CF6C1FA7E4F`.
- Response-bound PDF identity: `E5C5B26801205ADB1D27B76724595E44A0B8088550C9C9651ABCD8D8BCAC68CF`. Page and byte counts match, but the byte hash does not. The same-length drift produced by recompilation is consistent with PDF build metadata, but the response's exact-identity claim is nevertheless false for the current file.
- Displayed Tables 3, 4, and 8 use composition-sensitivity terminology (`Exec. sensitivity interval`/`Cols. sensitivity interval`, `Sens. low`/`Sens. high`, and `95% comp.-sens. interval`) rather than population-CI labels. Stale CI wording exists only in unused legacy table files and is not input by the manuscript.
- Figure 6 is the semantic-reliability figure. Its manuscript caption states the common exact Holm result once, and the SVG contains one common `Exact enumeration: all Holm p = 1.000` annotation rather than nine repeated right-edge labels. Figure/table hashes agree with the semantic figure-lineage manifest.
- The abstract explicitly says “two blinded agent technical reviewers”, defines the 15-state logical-AND execution-agreement rate, and denies human semantic-audit status. The response records 197 token-like words; the revised abstract is visibly within the journal's approximately 200-word target and preserves the limitation boundary.
- Exact enumeration is bound to 12 clusters and all `2^12 = 4096` sign assignments per test. The nine raw values in the manuscript match the exact-analysis report, and all nine Holm-adjusted values equal 1.0000.
- Portable verification independently passes both the live repository root and the recorded clean copied root: 19 checked files including the root marker; 18 manifest artifacts; invariant denominators include 25,920 atomic rows, 7920 primary semantic rows, and 16,416 held diagnostic rows.
- The response matrix covers 26 unique review findings with no missing or extra IDs. Status totals independently reproduce `resolved=18`, `resolved_internal_only=2`, `pending_bird_formal_run=1`, and `deferred_human=5`. Three severity-none checks are non-actionable, so 23 findings are actionable as stated.
- The five open submission gates are complete and non-overlapping at the stated aggregation level: BIRD launch authorization; qualified external-pair review/adjudication plus a sealed follow-up set; author identity/affiliation/correspondence/CRediT; author-approved declarations; and license review plus permanent repository DOI/URL. They agree with `HUMAN_ACTION_PACKET.md` and the manuscript remains correctly marked `submission_ready=false`.

## Blocking finding

**R3-CLOSE-B-01 — final PDF identity is stale.** The Round-3 response resolves snapshot traceability by claiming PDF SHA-256 `E5C5...68CF`, but the current 25-page, 664,609-byte PDF is `1A22...7E4F`. Freeze the current PDF once, then update every final identity-bearing closure/response/package record to that one hash (or make the PDF build deterministic and regenerate all bindings). Rerun only the identity checks afterward; no scientific re-analysis is required.

Once this local identity synchronization passes, the appropriate scientific status is `SCIENTIFIC_CLOSED_HUMAN_GATES_OPEN`; the five declared human gates remain submission blockers.
