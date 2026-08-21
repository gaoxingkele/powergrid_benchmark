# MA-SQLGrid Round-3 Methods, Statistics, and Reproducibility Review

Date: 5 August 2026  
Target: *Applied Sciences* (Computing and Artificial Intelligence)  
Decision: **MAJOR REVISION**

## Review boundary and snapshot

This is a read-only review of the current manuscript and PDF plus the frozen v5 semantic-reliability release, both post-score audits, and the Round-2 author response. I did not modify the manuscript, results, tables, figures, or analysis code.

- TeX SHA-256: `2206ADAEC37BA3C89F5177C1D32AB8519967BA1C688C96E134F754769FE29067`
- PDF SHA-256: `441494CF65860CB7ECDC25F8638DE2BF12D3A06E066DE4D0B677A4B2383E6C44`
- PDF: 24 pages; 662,457 bytes
- v5 freeze content SHA-256: `eb29201bd078e6903bea158d0dba6a974c0e1647dbf3e43972b38499b52a0818`
- Atomic-score SHA-256: `89c0ede848b4487a1edadb2fd771dabaf21a16c8359d7000ad9955c3196968cd`
- Release verifier: `RELEASE_V3_VERIFY PASS`
- Manuscript verifier: `PASS` (26 v2, 15 v3, and 4 component-analysis manifest outputs; 9 figures; 23 citation keys)

## Findings that are correct and require no numerical repair

1. **Denominators are internally consistent.** The release contains 25,920 atomic rows (`1440 x 18`), 528 primary predictions over 66 questions, 7,920 primary semantic-state rows (`528 x 15`), 912 held predictions over 114 questions, and 16,416 held diagnostic rows (`912 x 18`). The manuscript reports these numbers correctly.
2. **T0 continuity is intact.** The v5 T0 slice matches all 1,440 canonical-v2 execution labels. Both post-score audits independently report zero mismatches; Audit B additionally re-executed 29,160 read-only SQL statements.
3. **The 70-cluster and 12-cluster scopes are not conflated.** The original 180-question factorial analysis uses the frozen 70-group dependence proxy. The 66-question retrospective multi-state endpoint occupies 12 of those groups, and its table and figure correctly identify the 12-cluster composition boundary.
4. **Order-sensitive cases are not leaked into the promoted endpoint.** All 114 order-sensitive questions are held from the 15-state logical-AND estimand. Their 18-state executions remain diagnostic only.
5. **Retrospective and semantic-certification boundaries are stated.** The text repeatedly calls the v5 result an automated, retrospective, gold-SQL agreement stress test rather than a human semantic audit or proof of semantic equivalence.
6. **Holm family accounting is consistent.** The v5 release contains nine contrasts, 100,000 cluster sign-flip draws per contrast, 20,000 cluster-bootstrap draws, and one Holm-9 family. All nine adjusted values are 1.0, as reported.
7. **BIRD has not been silently promoted.** The frozen protocol records 500/500 gold-query preflight success and exactly zero formal model calls. The manuscript consistently says the future 5,000-call run is locked and that no BIRD score enters the article.
8. **Error accounting is conservative.** Prediction execution errors remain failed observations; they are not removed from the eligible denominator.

## Major issues

### R3-MS-M01 — The public-comparator experiment remains unexecuted

The manuscript is unusually transparent that the BIRD Mini-Dev protocol has completed only mechanical gold-query preflight and that formal model calls remain zero. Nevertheless, the current empirical evidence still lacks a completed public-benchmark comparator. This was an unresolved Round-2 gate and remains material for an applied text-to-SQL paper whose canonical corpus is a small, synthetic, development-visible database.

**Verifiable revision requirement:** after explicit human launch authorization, execute the exact frozen 5,000-call BIRD protocol, independently verify 5,000 unique call records and 4,000 final predictions, re-execute every final SQL under the pinned evaluator, and integrate cluster-aware results and failure accounting. If the authors elect not to run it, the response must explicitly withdraw BIRD as a submission-readiness gate and justify why the synthetic internal study alone satisfies the selected *Applied Sciences* section; no unexecuted protocol should be presented as compensating evidence.

### R3-MS-M02 — Applied external validity is still development evidence, not validated evidence

The RTS-GMLC and SimBench candidates are automatically constructed and visible, and zero of 91 candidates has completed the prepared two-reviewer adjudication. The manuscript labels this honestly, but the result is that the only accuracy-bearing corpus is the 8-table/98-row GridDB case study whose evaluation partition was visible during earlier development. The 15-state experiment reduces accidental equality within that same database; it does not establish cross-schema or operational grid validity.

**Verifiable revision requirement:** complete two independent qualified reviews plus adjudication for all 91 external pairs, retain disagreement records, and evaluate a genuinely sealed follow-up set after prompts and schema repair are frozen. At minimum report reviewer agreement and adjudication counts, exact accepted denominators, per-dataset execution results, and all-attempt failures. Until that evidence exists, retain the present bounded claims and do not describe RTS-GMLC/SimBench as external accuracy validation.

### R3-MS-M03 — The release is locally hash-bound but not yet a portable public reproducibility package

The data-availability, supplementary-material, author, funding, ethics-confirmation, conflict, and repository fields still contain submission placeholders. GridDB redistribution permission and source-specific license review remain unresolved. In addition, `formal_v5_release/release_manifest.json` stores machine-specific absolute `D:\\...` artifact paths; the release verifier therefore passes in the current workspace but is not by itself evidence of clean-checkout portability.

**Verifiable revision requirement:** complete license review and author-approved declarations; deposit the permitted package under a permanent DOI; replace or supplement absolute paths with paths relative to a declared package root; and demonstrate a clean-directory verification that recomputes every frozen hash, all fixed denominators, all nine contrasts, and the manuscript tables/figure source identities without relying on the original workspace path. Record the command, runtime lock, and clean-run report in the public package.

## Minor issues

### R3-MS-m01 — Use exact sign enumeration, or disclose Monte Carlo precision, for the 12-cluster suite

The eligible multi-state subset contains only 12 clusters, so there are just `2^12 = 4096` distinct cluster-sign assignments. Sampling 100,000 assignments with replacement is reproducible and does not change the current null conclusion, but it yields needlessly noisy raw values such as 0.750862 instead of the exact 0.750000 and visually implies more precision than the finite assignment space supports. Independent enumeration gives exact raw values of 0.75, 1, 1, 0.5, 1, 1, 0.5, 0.625, and 1 in the released contrast order; Holm conclusions remain unchanged.

**Verifiable revision requirement:** preferably enumerate all 4,096 assignments and regenerate the nine raw/Holm values. Otherwise explicitly state that draws repeat assignments, provide Monte Carlo standard errors or uncertainty bounds, and round raw values to a precision justified by the simulation error.

### R3-MS-m02 — Disclose the severe cluster-size imbalance of the 66-question subset

Reporting “12 clusters” is correct but incomplete for interpreting the effective dependence structure. Their eligible sizes are 18, 15, 12, 8, 6, 1, 1, 1, 1, 1, 1, and 1; the five largest clusters contain 59/66 questions. This imbalance explains the broad and asymmetric composition-sensitivity intervals and should be visible to readers.

**Verifiable revision requirement:** add the 12-cluster size profile (or at least range, median, maximum, singleton count, and 59/66 concentration) to Methods, Results, a table note, or Supplementary Materials, and connect it explicitly to the sensitivity—not population-confidence—interpretation.

### R3-MS-m03 — Formally extend the estimand definition from `m in {z,q}` to the reliability endpoint `r`

The Statistical Analysis subsection writes the factorial equations only for `m in {z,q}`. The multi-state subsection says that the same factorial estimands are used for `r`, and the Results apply them correctly, but the formal definition is indirect.

**Verifiable revision requirement:** state explicitly that the same three within-backbone contrasts and three cross-backbone modifiers are evaluated with `m=r` on the 66-question subset, and that this is a distinct nine-test Holm family from the canonical `z` family and the secondary `q` family.

### R3-MS-m04 — Expose analysis RNG lineage in the reproducibility description

The release is deterministic, but the manuscript does not give the statistical base seed and family-offset rule documented by Post-Score Audit A. Exact reproduction uses base seed 20260805, sign-flip seeds `base + 1000 + i`, and bootstrap seeds `base + 10000 + i` for zero-based family index `i`.

**Verifiable revision requirement:** report this seed/offset rule in Methods or the Supplement, or point to a public machine-readable analysis manifest that contains it and is included in the clean-directory verifier.

## Recommendation

No numerical correction to the current v5 denominators, T0 continuity, suite rates, contrasts, intervals, or Holm conclusions is required. The multi-state integration is methodologically conservative and substantially improves the paper. The manuscript is not submission-ready, however, because the public comparator, qualified external grid validation, and portable licensed repository remain open major gates. After those gates and the four small statistical-disclosure repairs, the methods/statistics package should be re-audited against the final DOI-bound artifacts.
