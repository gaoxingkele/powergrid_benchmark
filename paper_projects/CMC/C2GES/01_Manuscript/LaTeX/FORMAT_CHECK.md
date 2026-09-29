# MDPI Information format check — C2GES 2026-09-26（界值 + 跨域迁移 + 参考类型 + 评审增量）

Official style: MDPI layout (about-200-word single-paragraph abstract, 3–10 keywords), IMRaD, numbered references, Data Availability, CRediT, funding, COI, ethics. LaTeX class `Definitions/mdpi` **v6.5a dated 11 September 2026**. Journal option `information`.

| Item | Status |
|---|---|
| `\documentclass[information,article,submit,moreauthors]` | Pass |
| Title / authors / corresponding email `yangyong1@sgepri.sgcc.com.cn` | Pass |
| Featured Application | Removed |
| Abstract one paragraph, 197 words (≤ 200); now closes with the cross-domain bound on the path layer | Pass |
| Keywords 6 (3–10) | Pass |
| Evidence-layer table (`tab:evidence-layers`) | Pass: four layers with may/may-not-support bounds |
| Path-component primary evidence | Normalized Full vs no-path; 7-series −0.00799/−0.00718 |
| Historical numbers conserved | Full 0.1060/0.1276; unrenorm 0.1094/0.1310 |
| Related Work | GraphLSS/StrucSum difference clauses; STAS/Bi-GAE positioning; four same-journal *Information* comparators added (`verma2023graph`, `koniaris2023legal`, `azhar2025urdu`, `nechakhin2024orkg`); no ECT-BPS; no 15-test STAS/PacSum scores |
| Priority C dispositions | Expert 20–30, STAS/PacSum-on-15, 12-position window, RST/EDU, BERTScore/NLI deferred or declined |
| PDF 34 pages, 6 figures, 14 tables, 46 references, 0 Overfull, 0 undefined citations/references | Pass; one page above the 16–33 page range observed for the same-journal comparators, from the bounded path-layer result and the transfer layer; body text ends on p31, abbreviation list p32, references p33–34. The small synthetic-stress table moved to Supplementary Table S20 (main-text tables 15 → 14), which is how the document stays at 34 pages without losing the table |
| External prospective evaluation (§4.4 in results order + Supplementary Table S10) | Pass: 19 frozen external reports from ENTSO-E and NERC; Full−no-path −0.002906 at 260 words (Holm 0.046875, negative on 7 of 7 discordant documents) and TextRank−no-path +0.022940 (Holm 0.032380); the 110-word contrasts are not significant |
| Post-freeze corpus extension (reported as sensitivity) | Pass: +5 documents (three grid incidents, two frequency-deviation reports) → 24 documents; path-channel direction preserved and larger (−0.006908 at 260 words, 10 negative / 1 positive / 13 tied) but mean-based inference fragile (randomised sign-flip 0.444, Holm 0.678); TextRank contrast falls to p=0.130. Primary result stays the frozen 19-document comparison; both are asserted by the public verification |
| Arm-level decision experiment (role layer vs path layer) | Pass: 7 arms × 4 budgets on the same frozen 24 documents. Role layer reverses under an equal-word budget (AB2−AB0 = −0.03510 at 110 words, 18 negative / 4 positive / 2 tied, $p$=0.0039, Holm 0.0774) and is positive only under equal-unit budgets (+0.00626 / +0.01079, neither significant); the path layer stays within ±0.007 in all four budgets (260 words: −0.006908, 10 negative / 1 positive / 13 tied). Conclusion written into the manuscript: the role-layer gain is a length artefact; the path-layer null is the stable result. Asserted by `external_prospective_checks()` (`arms_documents_and_families`, `role_layer_reverses_under_equal_word_budget`, `role_layer_only_positive_under_equal_unit_budget`, `path_layer_stable_across_all_budgets`, `baseline_ordering_flips_with_budget_type`, `arm_numbers_bound_to_manuscript`) |
| Bounded negative result (new §4.3 sentences + Supplementary Tables S15, S17) | Pass: the one-sided 95% bootstrap upper limit on the path-layer difference is ≤ +0.0047 in every budget (+0.0006 at 110 words, +0.0021 at 260 words) and ≤ +0.0059 under leave-one-out, so a path-channel gain above +0.005 ROUGE-L is excluded; family split reported instead of pooling (grid −0.0028, market +0.0036, NERC −0.0031, frequency-deviation −0.0799 at 260 words) |
| Budget-efficiency curve (Supplementary Figure S5) | Pass: six arms at five word budgets and four unit budgets, 1,512 arm–budget–document rows; the ranking reverses with the budget type and the equal-unit protocol lets the role-conditioned arms select ~1.5× more words per unit than the lexical baseline and ~3× more than TextRank |
| Reviewer addenda round 2 (Supplementary Tables S14, S16) | Pass: exact reservation/path/interaction estimates with cluster-bootstrap intervals, exact sign-flip and Holm values (S14); per-report cost against candidate-set size plus role and typed-edge coverage (S16) |
| Out-of-domain transfer layer (L7, Supplementary Table S18) | Pass: the frozen arms applied without tuning to 100 length-stratified GovReport test documents (CRS + GAO reports with human-written summaries, CC BY 4.0; 973 test rows available, seed 20260926), then to the frozen strata in full (970 documents, 12 shards) and to a 160-document energy-topic subset. Path channel negative at every budget in all three runs; the full split keeps every one-sided 95% upper limit below zero (worst −0.0008) with family-corrected significance at all four budgets (Holm 0.0002–0.0040); the energy subset stays inside the +0.005 margin (worst +0.0008, Holm 0.0174 at ten units). Reported as a robustness-transfer bound, not as domain evidence: the cue lexicon is power-domain specific (mean formal role coverage 0.24) and the references are abstractive. Asserted by `govreport_transfer_checks()`; raw GovReport text stays outside the release scope |
| Reference-type sensitivity (Supplementary Table S19) | Pass: the same frozen arms on 400 length-stratified CNN/DailyMail test articles whose reference is the human-written highlight bullet points rather than an abstractive summary. The path-layer difference is zero to the fourth decimal at three of four budgets with 92–99% of articles exactly tied, and every one-sided upper limit is at most +0.0016, i.e. the term is inert rather than harmful under an extractive-style reference. Asserted by `reference_type_checks()`; raw news text stays outside the release scope |
| Upgraded synthetic stress layer (L5, Supplementary Table S20) | Pass: the single four-series stress set was replaced by a frozen parent–held-out pair (16 fictional reports, 8 series; disjoint themes, generator families swapped between sets) generated under `PROTOCOL_synthetic_c2ges_gendata_v1` (sha256 `daf7c969…`, thresholds frozen). All 19 deterministic gates pass in both sets; the component factorial (the paper's own evaluator, bitwise-clean) gives Full−no-path macro means +0.0103/+0.0098 (parent) and −0.0003/+0.0043 (held-out), all Holm 1.0, and G-T−G-U positive with Holm 0.25. Claim boundary unchanged: the fixtures never enter the E1/E2/E3 evidence chain. Asserted by `gendata_synthetic_checks()` |
| Redistribution boundary guard | Pass: the verbatim `SEALED_CHOICES.jsonl` is excluded from the release and replaced by `SEALED_CHOICES_rights_safe.jsonl` (identical identifiers, budgets, realised lengths and scores); `release_boundary_and_addenda_checks()` asserts that no shipped data record contains a ≥300-character natural-language run and that the shipped archive contains every figure the supplement references |
| Annotated-study gate (`tab:e2-gate`) | Pass: three preconditions plus the list of claims that stay closed until E2 |
| Adjacent-corpus construct audit (new §4.10 + Supplementary Table S9) | Pass: GUM 7,678 EDUs / 4.55% role coverage / 45 of 7,285 pairs with role evidence / 0 admissible edges; EBM-NLP 2,139 sentences, precision 0.610 and 0.807 against base rates 0.524 and 0.519, recall 0.064 and 0.060 |
| Public verification | `02_Revision_and_QA/04_Build_Reports/C2GES_DIAGNOSTIC_PUBLIC_VERIFICATION.json`: **PASS** on route `diagnostic`, Python 3.12.10, covering the RSI held-out layer, synthetic stress v8, the construct-audit aggregates, the external prospective record (documents, families, four contrasts, reference floor, the arm-level decision experiment), the bounded/curve/addenda artifacts, and the redistribution boundary |
| Supplementary PDF 10 pages | Pass |
| Word `paper_information.docx` | 12 embedded images, 15 tables |
| Supplementary PDF | 12 pages (Tables S1–S20, Figures S4–S5) |

Cover letter section: Information Applications (or Artificial Intelligence).

Release accounting for this build: package hashes are recorded in `PACKAGE_VERIFICATION.json` / `PACKAGE_VERIFICATION_submission.json` (this file travels inside the review ZIP, so it must not carry the ZIP's own hash); `RELEASE_MANIFEST.json` reports the file count with `--check` PASS (0 missing / 0 unlisted / 0 hash mismatches). Main PDF **34 pages**, supplementary PDF **12 pages**, Word copy **12 embedded images / 14 tables**.

## SuSy upload

1. Manuscript ZIP: `C2GES_Information_20260922_submission.zip`
2. PDF: `01_Manuscript/PDF/C2GES_Information_2026-09-22_diagnostic_submission.pdf`
3. Supplementary ZIP: `C2GES_Information_20260922_supplementary.zip`
4. Cover letter: paste `INFORMATION_COVER_LETTER.md` into the portal.
5. Word is author-review only.

Hashes after packaging are recorded in `PACKAGE_VERIFICATION.json` / `PACKAGE_VERIFICATION_submission.json`.
