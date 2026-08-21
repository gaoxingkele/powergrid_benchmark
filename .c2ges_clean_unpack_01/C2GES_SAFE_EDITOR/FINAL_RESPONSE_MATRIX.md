# C2GES Final-Candidate Response Matrix

This matrix responds to the three independent Round-3 reviews of the frozen R3
object. R3 itself was not modified. All repairs are confined to
`original_title_manuscript/FINAL_CANDIDATE`. The immutable v0.3.1 prediction
ledger (210 rows; SHA-256 `AAE2BFE0...2338F`), formal metrics, contrasts,
configuration, split, and scientific conclusions were not changed or rerun.

## Methods and statistics review

| Round-3 finding | Final-candidate response | Evidence / status |
|---|---|---|
| Development-calibration package omitted executable, 10 tests, verifier, four ledgers, state, and three core code snapshots | Included the original frozen executable/test/verifier, a clean-package executable/test/verifier surface, all four ledgers, `RUN_STATE`, decision, run manifest, original and package mechanical audits, report, and three hash-identical core snapshots. Machine paths in the package run manifest were replaced by relative or explicitly not-packaged locators. | Packaged verifier returns PASS, including 147/3,528/12/36 row counts, output and code hashes, 10-test presence, and relative paths. Portable test suite: 10/10 PASS. |
| Allowlist verified presence but not scientific completeness | Replaced the role-free inventory rule with required semantic roles, exact paths, bytes and hashes, plus forbidden-class checks. | `SUPPLEMENT_ALLOWLIST.json`; `scripts/build_supplement_manifest.py`; `scripts/verify_supplement_manifest.py`. |
| Public code repository is not synchronized | Not falsely closed. The manuscript and package explicitly state that the public branch is not asserted to match this candidate. Synchronization, license, immutable tag/archive, and clean-clone receipt remain author/repository-owner actions. | `SUBMISSION_HOLDS.md`; Data Availability Statement; safe-package manifest. **MANUAL HOLD.** |
| Source rights prevent transfer of the prediction ledger | The verbatim ledger remains only in `restricted_local_only` and is explicitly excluded from the safe editor ZIP. No PDF or extracted source text is included. | Safe ZIP exact-set audit and transfer boundary. **MANUAL RIGHTS HOLD** for any later restricted transfer. |
| No formal rerun or favorable reinterpretation is justified | Accepted. No scientific run was performed. Negative Full-minus-no-CF results and 12/12 zero-CF development outcome remain prominent. | TeX Abstract, Results, Discussion, Limitations, Conclusion. |

## Power-grid application and engineering-safety review

| Round-3 finding | Final-candidate response | Evidence / status |
|---|---|---|
| Equal K did not imply equal lexical or operator-review budget | Added a hash-pinned post-run audit for all seven conditions at K=5 and K=10: 210 per-report records plus a 14-group summary. Added a main-text diagnostic table and qualifications in the Abstract, Results, Discussion, Limitations, Conclusion, figure/table captions, and cover letter. | Full uses +103.0/+214.5 words versus Semantic-MMR and +110.7/+199.9 versus TextRank at K=5/K=10. Across 225 Full units, 37 exceed 100 words, 40 contain exact `Table`, maximum 270. No length-controlled superiority is claimed. |
| Prediction JSONL did not directly emit page | Corrected the output-schema claim. A deterministic non-verbatim join maps selected report/sentence IDs to page, source order, report metadata and URL. | 1,575/1,575 resolved; zero duplicate candidate keys, duplicate output keys, unresolved references, invalid pages, or ID/order mismatches. TeX now says page is recovered through the locator ledger, not emitted directly. |
| Long units reveal table/heading/footnote/line-break fusion | Reported, not silently removed or resegmented. No token-budget or splitter retuning was run on the revealed test. | New Results subsection and Limitations; post-run audit CSV/JSON/report. |
| Exact maintenance title exceeds evaluated population | Not empirically closed. All proxy-population, untested-transfer, unsafe-omission and no-operational-use boundaries remain. The cover letter asks the editor explicitly whether the intended-use title is acceptable. | Abstract first sentence; Featured Application; Introduction; Discussion; Conclusion; cover letter. **EDITORIAL/NEW-DATA HOLD.** |
| Roles/edges lack qualified semantic validation | Changed Table 1 language to “summary of executable behavior,” retained textual-proxy framing, and preserved the no-expert/no-physical-causality boundaries. | Exact code snapshot is packaged; qualified-human validation remains future work. **HUMAN/NEW-DATA HOLD.** |

## Applied Sciences fit and integrity review

| Round-3 finding | Final-candidate response | Evidence / status |
|---|---|---|
| Obsolete response draft contaminated the supplement | Removed `R2_TO_R3_RESPONSE_MATRIX_DRAFT.md`; this is the single authoritative final-candidate response matrix. | Exact-set verifier prohibits the obsolete filename. |
| Figure 1 hard-coded counts; figure generator used parent-workspace files; lineage lacked per-artifact hashes | Rewrote the generator to read only packaged sources. Dataset counts are parsed from the 40-row rights-safe inventory; aggregate values from packaged JSON; paired values from a 90-row non-verbatim derived CSV; algorithm weights/path horizon from packaged formal configuration. | Clean-unpack regeneration produces all four figures. `FIGURE_LINEAGE.json` records manuscript ID/anchor, each input path/hash, script/function/hash, PDF/PNG bytes/hashes, supported claim, and limitation. |
| Citation audit was only a set check | Replaced it with 23 item-level records covering all 26 citation occurrences. Each record includes key, source/evidence type, DOI/authoritative URL, metadata-verification scope, current TeX line/context hash, bounded support rationale, unsupported extension, and explicit no-human-full-text-read status. | `FINAL_CITATION_CONTEXT_AUDIT.json`: 23/23 records, 26/26 occurrences, zero orphan keys, zero recorded major context distortions; scope limitations preserved. |
| Package required clean-unpack proof | Added a safe editor ZIP dry run and clean extraction checks: exact-set/semantic-role verification, calibration tests/verifier, four-figure regeneration from packaged sources, LaTeX/BibTeX compilation, forbidden-file scan, and hash receipt. | `SAFE_EDITOR_PACKAGE_MANIFEST.json`; `CLEAN_UNPACK_RECEIPT.json`; final freeze audit. |
| Email, funder name/role, final CRediT/COI, AI provenance, rights and repository release remain unresolved | Not falsely closed. The placeholder/confirmation wording remains visible and these items are excluded from machine PASS semantics. | `SUBMISSION_HOLDS.md`; manuscript declarations; package manifest. **MANUAL HOLDS.** |

## Scientific invariants preserved

- Exact original title retained.
- Selected NERC proxy population, 40/27/13 accounting, 12/15 split, and 12,924
  candidates unchanged.
- One authorized v0.3.1 corrective run and 210-row prediction ledger unchanged.
- Full ROUGE-L values 0.1060/0.1276 and all registered/post-run contrasts
  unchanged.
- Adverse Full-minus-strict-no-CF result (about -0.0033 at both budgets) and
  intervals crossing zero unchanged.
- Post-unblinding 147-configuration development result (12/12 zero-CF winner)
  unchanged and not evaluated on the revealed test.
- No claim of length-controlled superiority, counterfactual-channel accuracy
  gain, physical causal identification, maintenance-work-order effectiveness,
  operator usefulness, or safety was introduced.

## Disposition

The repairable machine/package issues from the three Round-3 reviews are
addressed in this final candidate. The object is a **safe editor-package
candidate, not a portal-ready submission** until responsible humans complete
the corresponding-author email, exact funder and role, CRediT/COI, AI-use
provenance, file-level rights decisions, repository release/archive receipt,
and the editorial decision on retaining the aspirational exact title.
