# C2GES Round-3 Deterministic-Build Superseding Closure

Date: 2026-08-06 (Asia/Shanghai)  
Audit mode: independent, read-only, post-build identity and closure verification  
Decision: **SCIENTIFIC_CLOSED_HUMAN_GATES_OPEN**

## Scope and supersession

This record supersedes the **build-identity fields** in `round3_final_closure_confirmation.md/json`. It does not supersede or reopen the scientific decisions established by the three review rounds. The earlier closure correctly reported zero open scientific issues, but its build record preceded the deterministic two-build audit and retains a stale PDF byte count and earlier bundle totals. This record binds closure to the current deterministic artifact identities.

No manuscript, experiment, figure, table, manifest, or build artifact was modified or regenerated during this audit. The audit read the current TeX/PDF, `DETERMINISTIC_BUILD_AUDIT.json`, all three review/response chains, the prior final closure, the current bundle manifest, and the existing build log; it then executed only the read-only `verify_bundle.ps1` validation chain.

## Stable manuscript identity

| Artifact | Bytes | Pages | SHA-256 |
|---|---:|---:|---|
| `manuscript_applsci/paper_applsci.tex` | 58,045 | -- | `AD4C3AE9F11D1D8D07BAE34D697E32ABD1252D883DCE20CACE30DBE11768D849` |
| `manuscript_applsci/build/paper_applsci.pdf` | 762,452 | 22 A4 | `BE3B9B9F0A9B4B4968A9C78D7B00CEB7B8C833EF7D63965D85AFACD865C5A34D` |

`DETERMINISTIC_BUILD_AUDIT.json` records two independent C2GES builds under `SOURCE_DATE_EPOCH=1785888000`; both produced the same PDF SHA-256, byte count, and 22-page count. Its SHA-256 is `03E92AD6D91EAF36B277EE484F01B28B58AD11D5C5D2602726DDF1E591F2A86F`, and its C2GES deterministic-build status is `PASS`.

The retained build log is 62,117 bytes with SHA-256 `775429129A85D45905A2417606F6F337C72821487853B0D50F895F7D7A2CD445`; the read-only scan found zero LaTeX errors, undefined references/citations, overfull boxes, and underfull boxes. The prior closure's all-22-page visual-QA conclusion remains the applicable visual record because the deterministic audit changed build identity, not manuscript content or pagination.

## Bundle identity and independent verification

The authoritative current manifest is `manuscript_applsci/reproducibility/bundle_manifest.json`:

- SHA-256: `267AE228D94B5194B7BE687E640A8E9B83CAE0274901995E725CA15F04983253`
- size: 3,076,681 bytes
- status: `complete_local_manifest_generated_and_verified_after_manuscript_build`
- artifact count: **11,378**
- total bytes: **1,110,024,180**

The manifest contains exactly one TeX entry and one PDF entry, and both match the direct file hashes and byte counts above. The read-only one-command verifier exited successfully and reported:

> PASS: 11378 local artifacts, 1110024180 bytes, all SHA-256 hashes verified.

All five canonical compressed/decompressed payload checks passed. Because `verify_bundle.ps1` completed with exit code 0, its chained exploratory-v3 and Round-3 add-on validators also completed without error. The verifier separately reported that permanent DOI/URL creation and license review remain human blockers.

## Three-round closure continuity

The current tree contains the following complete sequence:

- Round 1 methods/statistics review and issue matrix, followed by `round1_response_matrix.md` (SHA-256 `5146F8564F3C835862AFFC09D2E18046D15F1F0745ED648906CA7212F0AF0313`).
- Round 2 editorial/venue review and issue matrix, followed by `round2_response_matrix.md` (SHA-256 `9109F18A1FC85A1CDDBB20CE572CE61A840E689F497AEBE391D3AA081AE2BA37`).
- Round 3 scientific review, issue matrix, response, closure review/matrix, and final confirmation. `round3_response_matrix.md` has SHA-256 `CD806AF83B30F9680DD5552A549F67BB66EF01F9137CBCE0844A6A5718376762`.

The prior `round3_final_closure_confirmation.json` (current file SHA-256 `C0C8549117DC8B70DB6F043AFDA72943C884E5061175A2285C5980D4BC8B190E`) records `decision: closed`, zero open scientific issues, and closure of the reproducibility-scope, bibliography-rendering, and gzip-provenance items. Its scientific and visual conclusions remain valid. Only its earlier build/bundle identity fields are superseded by this deterministic record.

The current evidence therefore contains no open local scientific, statistical, figure/table, provenance, bibliography, or reproducibility blocker for the manuscript's deliberately prospective “toward power-grid NERC” claim boundary.

## Open human gates

The manuscript is not submission-ready. The following actions require real author or rights-holder authority and remain open:

1. Replace the 12 `W7_FRONT_MATTER` markers with author names, affiliations, e-mails, and corresponding-author information.
2. Obtain author approval for CRediT contributions, funding/funder role, ethics/consent wording, acknowledgments, conflicts of interest, and the final generative-AI-use disclosure.
3. Complete license and redistribution review for the reproducibility package; do not infer permission or fabricate the irrecoverable historical Hugging Face revision.
4. Deposit the permitted package and supply a permanent public repository URL/DOI.

Independent NERC expert annotation is not required for the current prospective claim boundary, but it becomes a human validation gate before any upgrade to validated quantitative power-grid/NERC performance.

## Final determination

The deterministic two-build identity, current TeX/PDF, current 11,378-artifact manifest, full read-only verifier chain, and all three review rounds agree. The earlier closure's scientific decision is retained, while its build identity is superseded by the exact values above. Decision: **SCIENTIFIC_CLOSED_HUMAN_GATES_OPEN**; local scientific blockers: **0**; submission-ready: **no**.
