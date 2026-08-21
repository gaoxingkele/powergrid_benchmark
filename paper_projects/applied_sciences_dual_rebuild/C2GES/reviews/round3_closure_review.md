# C2GES Round-3 Closure Review

## Decision

**MINOR REVISION on scientific/reproducibility grounds.** The two Round-3 major issues are closed: the prospective add-on supplies a frozen contemporary cross-encoder comparison and genuine retrained no-floor/no-role variants, and exploratory-v3 now uses one claim-weighted estimand for points and cluster intervals with exact independent interval recomputation. The canonical W6 conclusions remain unchanged. I found no new major scientific or statistical defect.

The manuscript is nevertheless **not submission-ready**. Three author-resolvable technical minors remain: the newly reported add-on and corrected exploratory packages are outside the main bundle/claim-source verification boundary; the compiled bibliography still has ten `the the` proceedings renderings; and the nominally immutable canonical gzip changed byte hash without an explicit content/version explanation. Author identity/declarations and the license-reviewed permanent deposit/DOI remain separate external human blockers and do not change the scientific decision.

Reviewed snapshot:

- TeX: `manuscript_applsci/paper_applsci.tex`, SHA-256 `154FACA0AA4802298DBB6908CB316620A44BEBC11BB9E8111D3DB7BDE14A3F2A`.
- PDF: `manuscript_applsci/build/paper_applsci.pdf`, SHA-256 `CE8B40D3AF01C9099D872B34AE965B01A54992750356C13AB501B658C28A52F6`, 22 A4 pages, 761,200 bytes.
- Add-on freeze: `addon_round3/ADDON_PROTOCOL_FREEZE.md`, SHA-256 `B1B2DC29FCE3653E4E80A776FAF3F2E903658564581635EA838B22761F9FD69B`.
- Add-on results: `addon_round3/results.json`, SHA-256 `D1D0A4167736C35DBFA2BA0690B5BA9D457E584C7B3D837A84DA6B3536B7417B`.
- Add-on manifest: SHA-256 `97D65C00C8D6D0E0CDE9E4A7524C4E178C245B7263083B41AE0741A2995AEDC6`.
- Corrected exploratory manifest: SHA-256 `E56E7BC974328AF2CBDC19813BE3CF0ABBE19F335094DE2CB00AE8AB7C87E0DD`.
- Canonical manifest: SHA-256 `65BFC220DC8A62814B36D7522A3F58904519173D0232511205F9D969C6B7995F`.
- Main bundle manifest: SHA-256 `11BC01701E2B87F3BA0621BD997C6871DC823EA9850EE3F99B102D5CA389AB75`.

## Round-3 issue closure

### R3-M01 — closed

`addon_round3/ADDON_PROTOCOL_FREEZE.md` is timestamped `2026-08-05T16:50:01+08:00` and binds the unchanged grouped FEVER test set, hashes, label-blind primary cell, all eight arms, all four budgets, seven K=3 arm-minus-full contrasts, uncertainty procedures, multiplicity family, model revisions, and runtime boundaries before outcome inspection. The add-on contains:

- independently retrained five-seed full, true no-floor, and structurally true no-role systems;
- a `ZeroRoleHead` with no learned role parameters and exactly zero mixture role weight;
- a no-floor configuration with all three mixture floors set to zero;
- a frozen zero-shot `cross-encoder/ms-marco-MiniLM-L-6-v2` snapshot at revision `c5ee24cb16019beea0893ab7796b1df96625c6b8`;
- all planned BM25, query-only, dense/SBERT, no-local, true no-floor, true no-role, and cross-encoder comparisons.

Independent point and interval recomputation passes exactly. At label-blind K=3, cross-encoder minus full is `+0.01024381`, 95% cluster CI `[+0.000672,+0.019962]`, raw `p=0.03745`, Holm `p=0.18774`; it is therefore correctly not promoted. Dense/SBERT is the only Holm-significant contrast and is worse (`-0.02213959`, Holm `p=0.00616`). True no-floor is `-0.00395938` (Holm `p=0.35931`) and true no-role is `-0.00801212` (Holm `p=0.18774`). The manuscript reports these boundaries accurately at `paper_applsci.tex:20,206-210,294,310`.

The preserved failed wrapper attempt does not invalidate this closure: it failed before scoring because its output directory already existed, was retained, and the unchanged scorer was then executed once in a fresh directory. No inspected result was overwritten or selectively relaunched.

### R3-M02 — closed

Corrected exploratory-v3 resamples source documents while pooling every claim and its complete five-seed bundle, including repeated sampled clusters. Validation independently reconstructs all 108 cells and every stored claim-weighted interval. It passes for 15 ledgers, 810,000 rows, family sizes 24/81/54, maximum point discrepancy `1.787e-14`, and interval-endpoint discrepancy exactly `0.0`. Figure 4 and the surrounding text explicitly retain the post-primary exploratory boundary (`paper_applsci.tex:199-203`).

### R3-m01 — closed

The compute graphic no longer contains a non-dominated-envelope line or legend, and the prose explicitly disclaims a definitive Pareto frontier (`paper_applsci.tex:242`). The current vector figure SHA-256 is `466AC87B5D78649006B0F255A458779D48D9D1A2D13B1489C5DD0CDB122FAE93`.

### R3-m02 — partially closed

The literal January month and undated NERC program/access-date treatment are corrected. However, the bibliography normalization was applied to `references_cited_verified.bib`, while the compiled source still produces ten instances of `In Proceedings of the the ...`: `manuscript_applsci/build/paper_applsci.bbl:35,75,84,94,125,134,142,163,173,221`, visible on PDF pages 21-22. For example, `references_applsci.bib:25` still begins its `booktitle` with `Proceedings of the ...` while the MDPI style supplies `In Proceedings of the`.

Required edit: normalize the actual bibliography input used for compilation (or change the bibliography source consistently), rebuild, confirm zero `Proceedings of the the`/`the the` occurrences in the BBL and PDF, and update affected hashes.

### R3-m03 — closed

Figure 3 is enlarged and readable, the implementation table is clean, and the build log has no actual overfull/underfull, undefined-reference/citation, hyperref PDF-string, BibTeX, or fatal warnings. All 22 pages render without clipping, broken glyphs, or illegible main content.

## New minor reproducibility issues

### R3C-m01 — new add-on/exploratory claims are outside the main bundle and claim map

`manuscript_applsci/reproducibility/bundle_manifest.json` contains zero `addon_round3` paths and zero `exploratory_v3` paths. `manuscript_applsci/generated/claim_source_map.json` likewise covers the original 13 sources/eight generated fragments but not the add-on values/table at `paper_applsci.tex:206-210` or the corrected exploratory package. Consequently, `verify_claim_sources.py` and `verify_bundle.ps1` can pass while omitting evidence now used in the abstract, Results, Discussion, and Conclusions. The supplementary-material statement at `paper_applsci.tex:312` also describes only the original downstream/canonical boundary. The add-on root manifest hashes root outputs and ledger inventory, but does not recursively bind every run configuration, checkpoint, prediction, provenance/resource/log, and retained failure record.

Required edit: extend the local bundle manifest and one-command verifier to recursively include the frozen add-on and corrected exploratory packages; extend the claim map/checker to bind every hard-coded add-on value and the generated Table 6/figure inputs; and update the supplementary statement. This is a packaging/traceability minor because the separate validators and independent recomputations already support the reported science.

### R3C-m02 — canonical numerical invariance passes, but byte-level immutability is unexplained

The two central generated table hashes are unchanged from the prior review (`F9758D983DB549A24BF45192169F2C1B7DD6FDA7DD557C1D8E3203CDBBB0F404` and `150F3752944190A9BDA330E3B9368151E5D3DE13D44E43143D73D61EA8CF75D5`), all four independent recomputation tests pass, canonical validation still finds 180,000 rows/15 runs, and both W6 gates are identical. Thus scientific/numerical invariance is established.

However, `paper_projects/2026_c2ges_engineeringletters/workspace/w6_c2_canonical_v2/data/canonical_full_and_bm25_predictions.csv.gz` changed from prior SHA-256 `ED58EAA1E09619960A4977D6F0B97AD155723DFB55EDAEA2D81108F5795A8780` to `3E61018BF06FDD0AF27E2504CF79CAB85ABC093722473E5E8445983BB55A5D8F` even though Round 3 described only figure/manifest regeneration. The current decompressed payload hashes to `924D3DECAE9568ED0640673211217C164141CCA6CC50EBF07FF64ED6F8A0D939` (28,360,935 bytes; 180,001 lines). Equal compressed size and unchanged numerical products are consistent with recompression metadata, but the prior decompressed payload was not retained here, so exact content identity cannot be independently proved from the available manifests.

Required edit: restore the prior immutable gzip if available, or record a decompressed-content equivalence proof and deterministic compression policy (for example fixed gzip mtime) while explicitly versioning the regenerated manifest/figures. Do not describe byte-level v2 immutability without accounting for this hash transition.

## Verification summary

- Superseded-claim audit: PASS, all 6 TeX/PDF classes.
- Main claim-source verifier: PASS for its declared 13 sources, 8 fragments, 9 figures, and 28 citation keys; scope gap noted above.
- Corrected exploratory validator: PASS, including exact independent interval recomputation.
- Round-3 add-on validator: PASS, including frozen protocol binding, 32 independent cell points, seven-arm Holm family, and exact claim-weighted intervals.
- Holm independently checked from the seven stored raw p-values; adjusted values match Table 6.
- Independent canonical recomputation tests: 4/4 PASS.
- Canonical validation: PASS, 180,000 rows, 15 source runs, all expected tables/figures and gates.
- Local bundle verifier: PASS for 11,230 artifacts and 689,469,710 bytes, subject to the add-on/exploratory scope gap.
- PDF QA: all 22 pages inspected; figures, tables, equations, cross-references, and links are visually intact. Figure 3 and Table 6 are readable. Bibliography duplication is the only visible production defect.

## External human blockers — separate from the scientific decision

1. Replace all author/front-matter placeholders with author-approved names, affiliations, e-mails, correspondence, CRediT roles, funding/funder-role statement, ethics/consent confirmation, acknowledgments, conflicts, and generative-AI-use disclosure.
2. Perform redistribution/license review, deposit the permitted complete reproducibility subset, mint a stable public URL/DOI, and replace the repository placeholder without altering verified hashes silently.
3. Preserve the honest limitation that the original upstream Hugging Face revision is irrecoverable; do not fabricate it.
4. No human NERC annotation is required for the current prospective-title/qualitative-application boundary. Independent expert annotation becomes necessary only if claims are strengthened to validated power-grid performance.

## Closure gate

Scientifically, the paper is acceptable after minor revision. Close Round 3 after integrating the add-on/exploratory evidence into the main reproducibility boundary, fixing the compiled bibliography source, and accounting for the canonical gzip hash transition. Submission additionally requires the external author/deposit actions above.
