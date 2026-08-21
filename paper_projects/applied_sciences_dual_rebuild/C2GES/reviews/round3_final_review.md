# C2GES Review Round 3 — Final Scientific, Statistical, and Submission Audit

## Decision

**MAJOR REVISION — scientifically much improved, but not yet ready for submission.**

The prospective title and application boundary are now honest, the canonical v2 results remain traceable, and the post-primary exploratory package is correctly disclosed as retrospective/exploratory. However, two substantive issues remain: (1) the legacy-mode extraction still does not locate the method against a contemporary reranker or identify the effect of the mixture floors, and therefore does not fully answer Round 2's comparator/ablation objection; and (2) exploratory-v3 reports instance-weighted point estimates with confidence intervals generated from equally weighted document means, so the plotted point and interval do not target the same estimand. These are resolvable without fabricating NERC labels or missing metadata.

The manuscript is **not submission-ready** for separate external reasons: author/declaration fields and a permanent, license-reviewed artifact URL/DOI remain open. Those human blockers are listed separately and are not counted as scientific defects.

Reviewed snapshot:

- TeX: `manuscript_applsci/paper_applsci.tex`, SHA-256 `5CA575BA65AF87B0094CD964A9048314278AF53D46234774FC04AD9468FA70E7`.
- PDF: `manuscript_applsci/build/paper_applsci.pdf`, SHA-256 `96D648F34855AA01B1C606B96C52553946014BADD5BF741722C11BAD05FBA7A8`, 21 A4 pages.
- Canonical-v2 manifest: SHA-256 `989E91C60EB48220E92A8EAC32047973FA0F7B5D407CC66AF0489F6A51CA4783`.
- Exploratory-v3 protocol: SHA-256 `F77083B98C269180BD3CD458211A5948837596F73FEF592CA5A8BB463726B247`.
- Exploratory-v3 artifact manifest: SHA-256 `85E837388DCF53D7A25AEF29B037EC87BE2AE3A3DBA3721F67B4472E4BDC9154`.
- Local bundle manifest: SHA-256 `14CDE6F4141929832B2C9E8FF8ABC1963F34C2AA48B11FDE31642207CF3F9A72`.

## Major issues

### R3-M01 — The exploratory legacy-mode extraction does not close the contemporary-comparator or true no-floor gap

The new analysis is a useful, complete extraction of the nine modes already present in the source ledgers: BM25, full, Lead-K, LexCue, no-graph/no-local, no-role, query-only, SBERT, and TF-IDF. The paper accurately says that these predictions pre-existed, some modes may have been inspected, the exercise is post-primary exploratory, and the W6 gates are unchanged (`paper_applsci.tex:199–203`). It also correctly states that no cross-encoder and no true no-floor ablation were executed.

This improves transparency but does not fully answer R2-M02. The method is discussed beside current pairwise, setwise, and listwise rerankers (`paper_applsci.tex:54,287`), yet its only independent system baseline remains BM25; SBERT and TF-IDF are component scorers rather than a competitive interaction reranker. More importantly, `no_role` retains the constrained mixture mechanism and is not the requested role-head removal *plus removal of its floor*. Because the manuscript itself identifies the floors as a plausible explanation for the role NO–GO (`paper_applsci.tex:134–136,280,285`), the current extraction cannot identify whether the null role contrast is caused by uninformative role provenance, an unnecessary role head, or the floor constraint.

Required edit: before submission as a full Applied Sciences research article, prospectively freeze and run a compact add-on family on the unchanged documents, candidates, metrics, and budgets containing at least the full model, BM25, query-only, dense-only, no-local, true no-role/no-role-floor, true no-floor, and one feasible contemporary cross-encoder or listwise reranker. Freeze model snapshots and selection rules, report every planned mode, and measure comparable resource boundaries. Keep this family separate from canonical v2 and exploratory-v3. If the experiment cannot be run, the alternative is a substantial article-type/claim reframing centered on an audit artifact rather than presenting the reranker as methodologically located against contemporary systems; merely adding another limitation sentence is insufficient.

### R3-M02 — Exploratory-v3 point estimates and document-bootstrap intervals use different weighting estimands

`build_exploratory_v3.py:76–77,85–91,98–115` computes each reported contrast point as the mean of five seed-level claim-macro means, which weights test claims equally. For the interval, it first averages all claims and seeds within each document (`dsums/dcounts`) and then resamples and averages those document means equally. Documents contain unequal numbers of claims, so this interval targets an equal-document estimand while the plotted point targets the claim-weighted macro-F1 estimand. Figure 4 therefore overlays an interval around a point with a different weighting rule. The freeze says documents are the inferential clusters, but clustering does not require discarding cluster size: the canonical analysis correctly resamples documents and pools all claims in each sampled cluster.

The independent validator does not catch this: it recomputes all 108 cell means, checks family sizes, p-value grids, and stored hashes, but does not independently recompute the interval estimand (`validate_exploratory_v3.py`). This does not appear capable of rescuing a Holm-adjusted positive seed-level claim—the minimum two-sided five-seed sign-flip value remains 0.0625—but it affects the scientific meaning of Figure 4 and its confidence intervals.

Required edit: choose and state one estimand, then recompute points and intervals consistently. For claim-macro F1, resample document clusters and pool every claim (and the complete five-seed bundle) from each sampled document, preserving duplicated clusters and claim counts; alternatively, change both point and interval to an explicitly equal-document estimand. Add an independent interval recomputation check, regenerate exploratory CSV/JSON/figure/manifests/hashes, and update the manuscript if endpoints change. Preserve the exploratory label and all eight frozen contrasts.

## Minor issues

### R3-m01 — Figure 7 still asserts a “Non-dominated envelope”

The prose and caption now correctly call the compute plot a bounded diagnostic, but PDF page 15 still contains a dashed legend entry “Non-dominated envelope.” Only three closely related protocols are plotted; BM25 cost, indexing, model download, and online latency are absent. This is the exact Pareto implication R2-m02 asked to remove.

Required edit: regenerate `fig03_compute_accuracy_tradeoff` without the envelope line/legend, or add comparable end-to-end measurements for all baselines before using non-dominance language. Update the canonical and bundle hashes after regeneration.

### R3-m02 — Bibliography output has systematic proceedings duplication and one unresolved month macro

PDF pages 20–21 repeatedly render “In Proceedings of the Proceedings of …” because many `@inproceedings` `booktitle` values already start with “Proceedings of” while the MDPI bibliography style adds that phrase. The BibTeX log also reports `Warning--string name "jan" is undefined` for the NERC report. Reference 7 assigns the current access year 2026 as the web page's year even though the official page exposes no clear publication year.

Required edit: normalize `booktitle` values for this MDPI style so each citation contains only one “Proceedings of”; replace `month = jan` with a style-safe literal such as `month = {January}`; and, unless a publication/update date can be verified for the NERC program page, cite it as undated with the access date rather than treating access year as publication year. Rebuild and inspect the rendered references. Do not invent missing publication metadata.

### R3-m03 — Two known visual/build-cleanliness defects remain

Framework Figures 1–3 are logically clear but their internal node labels remain small at normal journal-page scale (especially Figure 3 on PDF page 10). The current log also retains two hyperref PDF-string warnings caused by math shifts in front-matter metadata and two underfull implementation-table boxes. No clipping, overfull boxes, undefined citations, or undefined references were observed.

Required edit: simplify/enlarge framework labels (at minimum Figure 3); make abstract metadata PDF-string safe for `$K=3$`; and clean the two table underfull boxes where practical. These are presentation fixes, not reasons to alter numerical claims.

## Round 1/2 closure and scientific consistency

- **Closed:** prospective-status disclosure. The abstract, Methods, figures, limitations, and conclusion consistently say “five-seed frozen continuation and canonical aggregation, including one previously inspected pilot seed.” Prohibited confirmatory/preregistered language is absent.
- **Closed:** title/application honesty. “Toward” is explicit; FEVER is named as the only quantitative corpus; NERC labels are machine-produced silver material; and the manuscript makes no NERC score, causal-diagnosis, or deployment claim. Independent NERC annotation is not required for the present prospective-title route.
- **Closed:** canonical gate wording, BM25 reference-row display, role-effect NO–GO, blanket-superiority NO–GO, conditional-oracle boundary, ledger scope, implementation detail, data-conversion audit, and closest Applied Sciences power-grid NLP precedent.
- **Partially closed:** R2-M02, because the complete legacy-mode extraction adds useful ablation evidence but lacks the modern comparator and true no-floor/no-role-floor test.
- **Open external:** permanent public artifact deposit/license review and author-approved metadata/declarations.
- **Irrecoverable but correctly disclosed:** the original Hugging Face revision. Retain frozen cache fingerprints and converted-file hashes; do not claim exact upstream regeneration.

The current abstract is 163 words by a plain-text token count and is safely below 200 words.

## Applied Sciences fit

The honest target is the **Computing and Artificial Intelligence** section, whose current scope explicitly includes applied AI, machine learning/pattern recognition, explainable AI, and information processing ([official section scope](https://www.mdpi.com/journal/applsci/sections/computing_artificial_intelligence)). The journal also asks for sufficiently detailed experimental reporting and permits software/calculation artifacts as supplementary material ([official aims and scope](https://www.mdpi.com/journal/applsci/about)). The manuscript fits this section at a **medium** level after the title correction; it remains a poor fit for an electrical/power-systems section because power-grid performance is not evaluated. The unresolved modern-comparator gap is the main editorial risk within the Computing and AI section.

## Independent verification and PDF QA

- `audit_superseded_claims.py`: PASS for all six prohibited/superseded claim classes in TeX and PDF.
- `verify_claim_sources.py`: PASS for 13 source hashes, 8 generated fragments, 9 figures, and 28 cited keys.
- Exploratory-v3 validator: PASS; 15/15 source ledgers, 810,000 rows, 108 cells, maximum mean-F1 recomputation difference `1.787e-14`, frozen F1/F2/F3 sizes, Holm checks, figures, and hashes.
- Independent recomputation tests: 4/4 PASS; compliance regression tests: 5/5 PASS.
- Local bundle verifier: PASS for 11,230 artifacts and 689,478,296 bytes; permanent DOI/license action remains explicitly blocked.
- Canonical-v2 validation: PASS; 180,000 canonical rows, 15 source runs, 176/176 evidence checks, and expected tables/figures.
- Full visual inspection: all 21 pages inspected. The new exploratory forest plot on page 12 is legible, shows all eight contrasts, labels direction as mode-minus-full, and does not visually merge with canonical results. Main tables/equations are readable; no clipping or broken glyphs were found.
- Canonical primary values remain consistent: predicted-label K=3 `0.4920 ± 0.0021`, BM25 `0.4864`, difference `+0.0056` with hierarchical CI `[0.0008, 0.0107]`; predicted-minus-blind `+0.0010` with intervals crossing zero.

## External human blockers — do not automate or fabricate

1. Supply author names, affiliations, e-mails, correspondence, CRediT roles, funding/funder role, conflicts, acknowledgments, ethics/consent confirmation, and the final generative-AI-use declaration.
2. Perform license/redistribution review, upload the permitted reproducibility subset, mint a stable URL/DOI, and replace all repository placeholders.
3. Do not fabricate or infer the missing historical Hugging Face revision. Preserve the stated limitation.
4. Do not fabricate human NERC labels. Independent expert annotation becomes necessary only if authors later strengthen the title or claims to imply validated power-grid performance.

## Final gate

Round 3 can close after R3-M01 and R3-M02 are substantively resolved, the three minor presentation/metadata issues are corrected, all verifiers are rerun with new hashes, and the external human blockers are completed. The negative canonical decisions and prospective power-grid boundary should remain unchanged.
