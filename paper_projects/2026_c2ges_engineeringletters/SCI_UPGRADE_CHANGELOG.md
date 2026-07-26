# SCI Upgrade Changelog — C2GES → IEEE Access

## Update 2026-07-19 — Public reproducibility repository PUBLISHED; Data Availability wired

Public GitHub repository created and pushed: **https://github.com/gaoxingkele/c2ges**
(public, default branch `main`, release **v0.1.0** tagged, 19 files).

Included: `code/` (`main.py`, `requirements.txt`, `analyze_supplement_evidence.py`,
`prepared_baselines/` with its README), `supplement/bm25_k_sensitivity/`
(summary.json, metadata.json, derived_tables.{json,md}, README),
`corpus_manifest/` (c2ges_nerc_report_manifest.{csv,json} +
`download_c2ges_nerc_reports.py` — the 40 raw NERC PDFs are NOT redistributed;
the manifest maps doc_id → official URL), `MISSING_ARTIFACTS.md` at repo root,
plus a NEW root `README.md` (contents map, 105/109 evidence summary, PDF-fetch and
baseline-run instructions) and `LICENSE` (MIT, code).

Excluded: `paper.tex`/`paper.pdf`/`paper.bbl`, `.cls`/`.bst`/font files, `charts/`,
`.codex/`, `AGENTS.md`, `REVISION_NOTE.md`, `OPTIMIZATION_PLAN.md`, stale
`code/README.md`, all `__pycache__/`. Pre-push secret scan (sk-/gho_/ghp_
patterns): clean.

Manuscript: `source/paper.tex` Data Availability `[TODO: repository URL and archival
DOI]` replaced with `\url{https://github.com/gaoxingkele/c2ges}` (release v0.1.0);
the DA text now states that the evidence supplement, analysis/verification code,
prepared baselines, and corpus manifest are in the repository and that the dataset
workspace artifacts will be added in a subsequent release (P1-6 partially closed:
repo exists; dataset release still blocked on MISSING_ARTIFACTS.md §1). Other
TODOs (authors, AI disclosure) left untouched.

Date: 2026-07-17. Maps every item of `PUBLICATION_ASSESSMENT.md` (P0 #1–5, P1 #6–9,
P2 #10–13) to its status. No experimental number in the manuscript was changed; no
new results were fabricated — everything requiring the original workspace is
**prepared-awaiting-workspace** with the exact ask list in `MISSING_ARTIFACTS.md`.

Legend: DONE = completed in this pass · PREPARED = script/infrastructure ready, blocked only on missing workspace data · USER = user-side action required · SKIPPED = intentionally not done (reason given)

## P0 — must fix for any venue

| # | Item | Status | What was done |
|---|---|---|---|
| 1 | Author/affiliation/email placeholders | **USER** | Left untouched per instruction (`Anonymous` / `email@example.com` in `source/paper.tex` header). Must be filled before submission. |
| 2 | Commit to IEEE Access; remove fake DOI; remove "intelligible to IEEE Access readers" | **DONE** | `\doi{10.1109/ACCESS.YYYY.XXXXXXX}` → `\doi{}` (empty; class requires the macro, journal assigns DOI). §4.3 phrase rewritten venue-neutral: "intelligible to readers who are more familiar with reliability reports than with sentence-ranking models". Template stays `ieeeaccess.cls`. |
| 3 | `code/README.md` stale title; incomplete `requirements.txt` | **DONE** | README rewritten with the paper's actual title ("Causal-Role-Aware Extractive Evidence Selection..."), workspace layout, and run instructions. `requirements.txt`: numpy, scikit-learn, networkx, lexrank, rouge-score, sentence-transformers (from `main.py`'s `dependency_status` list). |
| 4 | Main Executor artifacts into package (summary.json, details.jsonl, cv_protocol.json, heldout_predictions.jsonl) | **PREPARED / USER** | Artifacts are not on this machine and cannot be reconstructed. Precise request list + destination paths + what each file evidences: `MISSING_ARTIFACTS.md` §3. |
| 5 | Remove `/media/lenovo/...` hardcoded fallback in `main.py` | **DONE** | `WORKSPACE_FALLBACK` constant deleted. Added `--workspace` CLI argument and `C2GES_WORKSPACE` env var, with validation and a clear error message pointing at MISSING_ARTIFACTS.md. Error paths exercised and verified. Python syntax checked. |

## P1 — strongly recommended before SCI submission

| # | Item | Status | What was done |
|---|---|---|---|
| 6 | Public dataset release (Zenodo/GitHub DOI), Data Availability | **PREPARED / USER** | Added `Data Availability` section to `paper.tex` with `[TODO: repository URL and archival DOI]`. Release itself blocked on dataset (MISSING_ARTIFACTS.md §1) and user's repo/Zenodo account. The "defines a benchmark" contribution stays contingent on this release. |
| 7 | Learned baselines (cross-encoder + bge-reranker) + LLM zero-shot baseline; tradeoff narrative pre-positioning | **PREPARED (scripts) + DONE (narrative)** | Scripts: `source/code/prepared_baselines/{run_crossencoder_baseline.py, run_bge_reranker.py, run_llm_zeroshot_baseline.py, common.py}` — protocol-matched (same data conventions as `main.py`, K=3, evidence P/R/F1 + ROUGE-L, doc-cluster bootstrap seed 202502, metrics/bootstrap functions imported from `main.py`, same details.jsonl/summary.json format, optional paired comparison vs Executor details). LLM script is OpenAI-compatible (`--model/--base-url/--api-key-env`), stdlib-HTTP, response-cached; CE/BGE run on CPU. Harness smoke-tested end-to-end on synthetic data (plumbing only — no real numbers exist or are claimed). Narrative: new Discussion paragraph explicitly positions the deterministic reranker on transparency/auditability/cost vs learned & LLM rerankers, so the contribution framing survives if future LLM baselines win on F1; Related Work and Limitations now cite the prepared harness as declared future work. |
| 8 | Human gold subset (50–100 qs, dual annotation, Cohen's κ) | **PREPARED / USER** | Cannot be done without dataset + human annotators. Manuscript now pre-announces it precisely (new §4 circularity subsection + Limitations bullet) as the planned verification of the label–cue circularity risk. Sampling becomes possible after MISSING_ARTIFACTS.md §1. |
| 9 | Cue-lexicon construction & circularity discussion | **DONE** | New subsection "Cue-Lexicon Construction and Potential Label–Cue Circularity" in §4 (label `sec:cue_lexicon_construction_and_circularity`): states cue provenance honestly (manually curated during development on the same corpus; 5-fold protocol protects only mixture-weight/family selection, NOT cue authorship; no held-out split constrained cue curation), names the shared-surface-preference circularity risk with agent labels, and adds the R×chain interaction caveat: the no-graph ablation removes a role–structure *interaction* term, not a pure structural signal. Cross-referenced from Limitations. |

## P2 — polish

| # | Item | Status | What was done |
|---|---|---|---|
| 10 | Abstract pseudo-precision "40.575%/51.231%" | **DONE** | → "approximately 41%" / "approximately 51%" in the abstract. Underlying F1 values (0.2983 etc.) and all table numbers untouched. The exact percentages appear nowhere else in the tex. |
| 11 | 2–3 real 2024–2026 LLM-reranking references | **DONE** | Three added, each verified via web search with DOI: Qin et al., Findings of NAACL 2024, pp. 1504–1518, doi:10.18653/v1/2024.findings-naacl.97 (pairwise ranking prompting); Zhuang et al., SIGIR 2024, doi:10.1145/3626772.3657813 (setwise zero-shot LLM ranking); Ren et al., WWW 2025, pp. 3692–3701, doi:10.1145/3696410.3714658 (self-calibrated listwise LLM reranking). Added to `references.bib`, cited in Related Work §2.3 (new paragraph), Discussion, and Limitations. Matching `\bibitem` entries appended to `paper.bbl` so the package compiles without a bibtex rerun; a fresh `pdflatex→bibtex→pdflatex×2` will renumber citations in order. |
| 12 | Role-coverage diagnostics / error-type counts in main text | **SKIPPED (no invention)** | The numbers do not exist in the package: `role_coverage` per condition and error-type counts live only in the missing Executor `summary.json`/`details.jsonl` (verified: no `role_coverage` key in the BM25 supplement). Existing qualitative error taxonomy (§7) and the role-coverage diagnostic definition (§5.3) already in text were left as is. Becomes possible after MISSING_ARTIFACTS.md §3. |
| 13 | Post-hoc revision disclosure at graph-gate p=0.0254 | **DONE** | Added to §6.2 next to Table 4, sourced from `REVISION_NOTE.md`: the role-selective gate originated in a post-freeze revision after the frozen all-roles graph term showed no reliable benefit; gated variant selected afterwards within the 5-fold candidate protocol; p=0.0254 to be read as diagnostic, not confirmatory pre-registered. |

## Additional (not in numbered list)

- **AI-use disclosure**: new unnumbered section "Disclosure of the Use of Artificial Intelligence" in `paper.tex` — restates agent label provenance, discloses LLM assistance in drafting/editing, author responsibility; `[TODO: confirm wording against journal AI policy]`.
- **Data Availability skeleton**: see P1-6 above.
- **Conclusion**: future-work sentence now references the prepared harness and inter-annotator agreement.
- **LaTeX compilability**: no LaTeX toolchain on this machine (`pdflatex`/`tectonic`/`latexmk` all absent) — the PDF was NOT rebuilt. A manual balance check of all edited regions was performed (brace/environment/math-delimiter balance; `\section*`, `\cite`, `\ref` targets all defined). User must rerun `pdflatex → bibtex → pdflatex → pdflatex` and re-check the 15-page layout (new text adds roughly half a page).
- **Numbers audit**: zero changes to any experimental value; the only numeric-string edit is the abstract percentage rounding (P2-10), which the assessment itself verified as 1.40575/1.51231 ratios.

## 2026-07-19 — In-package supplement exploitation round

Discovery: `source/supplement/bm25_k_sensitivity/summary.json` is NOT only the
K-sensitivity table — it is the paper's main K=3 run for seven conditions
(bm25/tfidf/sbert query, c2ges full/no_graph/no_role/query_only), with per-document
metrics, role stratification, nine paired bootstrap comparisons, and full dataset
provenance metadata. Anchor verified: K=3 c2ges_full F1 = 0.29828571 = the paper's
0.2983; full−bm25 = 0.0710 = the headline BM25 gap.

- **New script `source/code/analyze_supplement_evidence.py`** (DONE): extracts (a) the
  K=3 aggregate table for all 7 conditions, (b) all 9 paired comparisons × 4 metrics,
  (c) the role-stratified K=3 table, (d) per-document evidence-F1 dispersion, (e) a
  109-point supplement-vs-manuscript cross-check. Outputs
  `source/supplement/bm25_k_sensitivity/derived_tables.{json,md}`.
- **Cross-check result**: 105/109 match. The 4 mismatches are all Table 4 CI
  endpoints for the vs-TF-IDF and vs-SBERT rows (off by 0.0002–0.0015): the printed
  CIs come from the original Executor bootstrap seed, the supplement re-ran with seed
  20260626. Mean diffs match exactly; disclosed in the manuscript's Data Availability
  text. No number was changed.
- **paper.tex §3** (DONE): new dataset-lineage paragraph with concrete provenance
  facts from `dataset` metadata — 25→40 doc lineage, 15 new docs independently
  verified (6 pass / 8 minor repairs / 1 answer-narrowing repair), initial parallel
  verifier failed 5 batches on HTTP 429 then rerun sequentially, 0 schema evidence
  errors, 40 questions per role, 1 low-diversity-flagged document.
- **paper.tex §6.1** (DONE): new Table `tab:role_strata_baselines` (5 roles ×
  BM25/NoRole/Full + Full−BM25 delta at K=3) + analysis paragraph (impact +0.1248 and
  trigger +0.0864 gain most over BM25; propagation/response +0.0321 least; no-role
  falls below BM25 on mitigation and root cause). New cross-document dispersion
  paragraph: per-doc mean F1 for full C2GES spans 0.0800–0.5219 (sample std 0.1092),
  BM25 0.0571–0.5000, SBERT has one zero-evidence document; motivates doc-cluster
  bootstrap. Fills the previously-SKIPPED P2-12 role-diagnostics slot with real
  in-package numbers.
- **paper.tex §6.2** (DONE): new paragraph adding the previously unreported paired
  comparisons — vs SBERT at K=1 (+0.0573, CI [0.0093, 0.1013], p=0.0182) and K=5
  (+0.0808, [0.0387, 0.1208]); vs TF-IDF at K=5 (+0.0688, [0.0421, 0.0949]); K=3
  SBERT precision (+0.1067) and recall (+0.0996) — with an explicit
  multiple-comparison caveat (uncorrected; only K=3 TF-IDF is primary).
- **paper.tex Data Availability** (DONE): precise in-package evidence statement —
  what the shipped supplement evidences (7-condition K=3 aggregates, K-sensitivity,
  9 paired comparisons, role stratification, dispersion, provenance counts) vs what
  still requires the Executor artifacts (5 weak-baseline rows, ablation/legacy CIs
  and p-values, fixed-legacy condition, cv_protocol, §7 case studies); seed-level CI
  reconciliation (≤0.002) disclosed.
- **paper.tex Limitations** (DONE): bullet 2 extended with the agent-based
  verification counts and the low-diversity flag ("verification depth is uneven").
- **MISSING_ARTIFACTS.md** (DONE): new §0 "Already evidenced IN-PACKAGE — do NOT
  re-request"; §3 request narrowed to what the Executor artifacts uniquely evidence;
  exact original-machine paths added from the supplement metadata, including
  `dataset.source_asset_root` on the *other* workspace
  (`c2ges-evidence-audit-krill/datasets/gridmaint_causalsum_pilot/processed`).
- **LaTeX discipline**: no compile available; structural check of all edits
  (environment balance, `\ref` targets, math delimiters) performed; both `[TODO]`
  markers preserved; zero existing numbers altered.

## Submission-blocking remainder (user actions, in order)

1. Fill authors/affiliation/corresponding email in `paper.tex` (P0-1).
2. Supply the files in `MISSING_ARTIFACTS.md` (§1–§3) from the original machine.
3. Run the three prepared baselines; if a learned/LLM baseline wins on F1, the Discussion's tradeoff paragraph already carries the framing — add the cost/latency comparison table it promises.
4. Execute the human-gold subset study (P1-8).
5. Publish dataset+artifacts, fill the two `[TODO]`s (Data Availability, AI disclosure), rebuild the PDF, and submit.

## 2026-07-19 — LaTeX compile & typography fix round (Round-2 defects)

- **Compile status**: clean — `pdflatex -> bibtex -> pdflatex x2` under fresh MiKTeX build, 0 errors, 17 pages, `source/paper.pdf` rebuilt (replaces stale PDF).
- **Defects fixed** (per `ROUND2_SUBMISSION_REVIEW.md` typography section):
  1. Math-mode `\_` rendering as literal underscores instead of subscripts: **30 occurrences** fixed (`D\_i`->`D_i`, `n\_i`, `w\_q/w\_r/w\_g` x13, `\mathcal{R}\_g` x2, `\alpha\_r/\beta\_r/\gamma\_r`, `s\_j/s\_k` x6). Text-mode escapes (`\texttt{doc\_id}`, `\texttt{cv\_protocol.json}`) intentionally left untouched. No numbers changed.
  2. §4.2 cue-lexicon quote breakage: rebuilt the three mangled `\texttt{...''}` cue lists (trigger / root-cause / propagation-response, **18 cue terms**) as proper LaTeX ``...'' quotes; verified rendering in PDF text.
  3. Duplicated Index Terms: removed the literal "Index Terms---..." line embedded in the abstract; the `\begin{keywords}` block is now the single INDEX TERMS source (verified: exactly one occurrence in PDF).
- **PDF content verification**: role-stratified table caption ("Role-stratified evidence F1 at K=3 ...") present; §4.4 label–cue circularity section present; Data Availability now carries `https://github.com/gaoxingkele/c2ges` (release v0.1.0; concurrent DA edit picked up in final recompile). AI-disclosure `[TODO: confirm final wording ...]` remains by design (author-side).
- **Remaining acceptable warnings**: Formata font substitution warnings (`T1/pcr/n/n` undefined, defaults substituted) — expected with the Access class fonts; class-level `Overfull \hbox (505pt) while \output is active` header/footer artifacts (present in baseline build, template-inherent); residual content overfull boxes all <10pt. No undefined references or citations.

## 2026-07-19 — CMC (Computers, Materials & Continua) format conversion

New submission package created at `source/manuscript_cmc/` (source `paper.tex` untouched):
`paper_cmc.tex`, `references_cmc.bib`, `supplementary_cmc.tex`, `Definitions/` (tsp.cls,
vancouver.bst, unmodified template assets), `charts/` (4 PNGs), built `paper_cmc.pdf` +
`supplementary_cmc.pdf`.

- **Build status**: clean — `pdflatex -> bibtex -> pdflatex x2` (MiKTeX, tsp.cls option
  `cmc,article,submit,moreauthors,pdftex`), 0 errors, no undefined refs/citations.
  **Main PDF: 25 pages** (target <=25 met; >15 pages implies ~$1,000 page charges on top
  of the $1,600 APC). **Supplementary PDF: 4 pages** (plain article class; S-numbering).
- **Section mapping (10 -> 6 top-level)**:
  1 Introduction (kept; + Fig. 1 architecture moved up per CMC Fig.-1 convention; 3-bullet
  contribution list + organization paragraph retained) |
  2 Related Work (4 subsections kept) |
  3 Task and Benchmark (kept prominent, self-built-corpus convention) |
  4 Method (4.4 renamed "Methods Integrity: Cue-Lexicon Provenance and Label–Cue
  Circularity"; complexity analysis -> supplement S3) |
  5 Experiments, Results, and Discussion (merges old Experiments + Results + Qualitative
  Error Analysis (5.5) + Discussion (5.6); hyperparameter table -> supplement Table S2;
  K-sensitivity table + per-budget bootstrap prose -> supplement S1/Table S1; per-document
  dispersion details -> S2; third qualitative case -> S5, pointer kept) |
  6 Conclusions, Limitations, and Future Work (old Limitations bullets condensed to prose,
  all caveats retained).
- **Optics de-risking**: abstract (301 words, no citations, 6 keywords) and Results 5.3
  now lead with relative gains (+41% TF-IDF / +31% BM25 / +51% SBERT, doc-cluster
  bootstrap p<0.001) BEFORE absolute 0.2983 F1; new task-hardness calibration paragraph
  added in 5.3 grounded in two locally verified CMC-corpus numbers (Spider strict exact
  match 13.44–28.14% vs >67% execution accuracy, CMC 2026;88(2):80; SecureBERT NER
  baseline recall 0.527 / best F1 0.785, CMC 2026;87(1):32). No experimental number
  altered anywhere.
- **References: 57 -> 47** (45 retained + 2 CMC calibration refs), rebuilt in Vancouver
  via `Definitions/vancouver.bst` (numeric, cited-order, first-6-authors-et-al.,
  [CrossRef] DOI links via note fields; arXiv IDs protected from the bst's journal
  dot-stripping with an `\adot` macro). **12 dropped** (all inside multi-citation
  clusters; no orphaned claims; prose reworded where a named variant was dropped):
  xu2020discourseaware, su2021improve, joshi2024ranksum (duplicate arXiv of
  joshi2022ranksuman), kazemi2020biased, verma2023graphbased, giarelis2023abstractive,
  jia2020neural, huang2021extractive, vladika2024improving, zhang2022situ,
  liello2022pretraining, setiawan2025impact. Max consecutive citation cluster now 4
  (old 6-ref evidence-retrieval chain trimmed to 3).
- **Back matter** in TSP exact order: Acknowledgement (generative-AI disclosure covering
  BOTH agent-generated/verified label provenance AND manuscript drafting assistance, TSP
  wording), Funding [TODO], Author Contributions [TODO CRediT], Availability of Data and
  Materials (sanctioned "openly available" formulation; github.com/gaoxingkele/c2ges
  v0.1.0; NERC sources public; workspace artifacts in subsequent release; long
  artifact-to-table evidence map moved to supplement S4), Ethics Approval (N/A),
  Conflicts of Interest, Supplementary Materials pointer. Author name/affiliation/email
  [TODO] markers preserved.
- **Verified in built PDF**: role-stratified tables present (Tables 4, 5, 7), Table 3
  main results with bolded best column values, relative-gain-led abstract, GitHub URL,
  back-matter statements in canonical order, Figures 1–4 / Tables 1–7 numbered and cited
  sequentially, algorithm box via `algorithmic` (tsp.cls-compatible ruled block).
- **Known deviations / submission notes**: (i) figures are PNG (CMC prefers .tif >=300
  dpi — regenerate TIFFs from chart sources before upload); (ii) floats use `[!ht]`
  rather than the template's `[H]` to meet the 25-page cap (placement remains adjacent
  to first citation); (iii) supplementary uses plain `article` class (TSP accepts any
  format for separately-uploaded supplements); (iv) cover letter (originality,
  non-simultaneous submission, APC commitment) still to be drafted —
  `cmc_cover_letter_draft.md` exists for adaptation.

## 2026-07-20 — Learned/LLM baseline integration (both variants) + repo v0.2.0

Integrated the three new protocol-matched baseline runs (`baseline_runs_2026-07-20/`,
200 questions, K=3, document-cluster bootstrap 10000 samples, paired vs the Executor
`details.jsonl`) into BOTH manuscripts. **All numbers verified against the underlying
`summary.json` files before writing** (aggregates, own-score CIs, paired CIs/p-values,
and the paired-vs-TF-IDF/SBERT contrasts all match RESULTS_SUMMARY.md exactly;
cross-encoder recall 0.31875 → 0.3188).

- **Results integrated**: BGE-reranker-base 0.2604 F1 (vs c2ges_full −0.0379
  [−0.0739, −0.0010] p=0.0448, borderline significant); cross-encoder ms-marco-MiniLM
  0.2787 (−0.0196 [−0.0539, +0.0140] p=0.246, NOT significant — stated as such, no win
  claimed); LLM zero-shot deepseek-chat 0.5887 (+0.2905 [+0.2533, +0.3255] p<0.001,
  LLM decisively ahead ~2x, reported as honest upper reference). LLM run cost ~200
  calls / ~8.5 min / ~US$0.2–0.3.
- **IEEE Access variant (`source/paper.tex`)**: new Results subsection "Learned and
  LLM Baselines" (combined 7-row baseline table with paired CIs + deployment-tradeoff
  table + three-part honest reading); LLM–LLM label-provenance caveat wired into the
  §4 circularity subsection (human-gold subset stays the arbiter, both directions);
  benchmark-headroom sentence (0.05–0.59 discrimination range); abstract, contributions
  (new 4th bullet), related-work LLM-reranker paragraph, discussion positioning
  paragraph, limitations (former "no learned baselines" bullet replaced with bounded-
  coverage + single-model/prompt + provenance caveat; human-gold retained), conclusion,
  and Data Availability all updated (v0.2.0; executor artifacts now in-package under
  `supplement/c2ges_role_selective_graph/`, verified 108/108; seed-level CI note now
  points at the exact Executor endpoints). Rebuilt clean with MiKTeX: **19 pages**
  (was 17), 0 errors, no undefined refs; `paper.pdf` replaced.
- **CMC variant (`source/manuscript_cmc/`)**: same updates compact — new subsection
  5.5 with the combined table + short honest reading + tradeoff sentences in main
  text; full paired-CI detail + LLM cost moved to new supplementary **Section S6**
  (S4 evidence map updated: v0.2.0, 108/108, qualitative cases now §5.6); abstract/
  contribution-free front matter, related work, methods-integrity 4.4, discussion 5.7,
  conclusions/limitations, and Availability of Data and Materials updated. Rebuilt
  clean: **main 26 pages (≤26 budget met after prose compression), supplementary 5
  pages**, 0 errors, no undefined refs.
- **Figure upgrade decision: NOT swapped.** `figure_upgrade/c2ges_teaser_architecture_upgrade.png`
  is aesthetically stronger but contains a factual flaw — the role-chip panel reads
  trigger/root cause/response/impact/**impact**/mitigation (duplicate "impact",
  missing "propagation") plus garbled micro-text in the heatmap label. The current
  accurate `charts/architecture_diagram_1.png` is retained in both variants; the
  upgrade candidate is kept untouched in `figure_upgrade/` for author review after a
  corrected regeneration.
- **Repo github.com/gaoxingkele/c2ges updated to v0.2.0** (commit d247219, release
  https://github.com/gaoxingkele/c2ges/releases/tag/v0.2.0): added
  `dataset/agent_audit_40doc/` (40 docs / 2940 sentences / 200 questions / 608
  evidence IDs + manifest — DA promise fulfilled), `pipeline/` (validated pilot
  scripts + three-pack/config.yaml), `supplement/c2ges_role_selective_graph/` (all 7
  executor files), `baseline_runs/` (three baselines' summary.json + details.jsonl +
  RESULTS_SUMMARY.md; secret-scanned — only the env-var NAME appears, no key), and
  rewrote README (dataset included, 108/108 verification, honest baseline summary
  incl. the LLM result and tradeoff framing) + MISSING_ARTIFACTS.md (annotated
  RESOLVED — nothing material remains missing).

## 2026-07-22 — Final micro-polish per CMC_READINESS_AUDIT.md (abstract honesty, tradeoff reframing, bib, cover letter)

- **Abstract honesty qualifier (both variants)**: the "stays ahead of two neural rerankers"
  sentence now reads "...on point estimates ... (one comparison borderline-significant, one
  statistically indistinguishable)" in `source/manuscript_cmc/paper_cmc.tex`; the Access
  variant `source/paper.tex` (which already carried the per-baseline parenthetical) gained
  the matching "on point estimates" qualifier. In both abstracts the LLM upper-reference
  clause now leads with "offers no per-term score decomposition" before the remote-endpoint note.
- **Tradeoff-defense reframing (both variants)**: primary emphasis shifted from offline/no-API
  to per-term decomposability, determinism, and auditability, with offline CPU operation and
  cost demoted to secondary practical notes — closing the audit's "a local open-weights LLM
  would be offline too" gap. Edits: Section 5.5 third finding (CMC L476 / Access L555) adds
  "The load-bearing distinction is auditability rather than connectivity: a locally hosted
  open-weights LLM would also run offline, yet would still offer no per-term decomposition and
  no bit-reproducibility guarantee" and reorders the requirements sentence; Discussion value-
  proposition sentence (CMC 5.7 / Access) now names "per-term decomposability, determinism, and
  auditability, with offline CPU operation and low cost as secondary practical benefits" and the
  LLM cost list leads with non-decomposability, endpoint/cost "secondarily"; Conclusions and the
  Access contribution bullet reordered the same way. No numbers changed; net growth ~4 sentences.
- **References patched** (`source/manuscript_cmc/references_cmc.bib`), verified via
  api.crossref.org by DOI: xie2022massively **corrected** to Proc IEEE 2023;111(7):762–787
  (entry previously said 2022;110 — Crossref/IEEE print citation is vol 111 no 7, July 2023;
  bib key unchanged); madabhushi2023survey -> 22(6):1799–1832; sahani2023machine -> 7(2):1–31.
  Other pageless entries are conference/arXiv items where NLM carries no pages (left as is).
- **Cover letter refreshed** (`cmc_cover_letter_draft.md`): release v0.1.0 -> v0.2.0; data-
  availability bullet now states the dataset workspace and learned/LLM baseline harness+outputs
  are **included in v0.2.0** (no longer "subsequent release"); new contribution #3 summarizing
  the three protocol-matched baselines (BGE 0.2604, cross-encoder 0.2787, zero-shot LLM 0.5887
  framed as honest upper reference + decomposability/determinism tradeoff); explicit COI
  sentence added; also corrected a stale factual slip in contribution #2 (gains re-attributed
  to the manuscript's numbers: ~41% over TF-IDF, 31% over BM25, 51% over SBERT — the draft had
  said "41% over BM25 / 51% over query-only"). [TODO] markers preserved.
- **Recompiled clean (MiKTeX)**: CMC main `paper_cmc.pdf` 27 pages, 0 errors, 0 undefined refs,
  same 6 pre-existing minor Overfull boxes (page 26 was already full; the qualifier sentences
  push the last 3 references onto p.27 — APC formula moves ~$100; final TSP typesetting will
  repaginate anyway). CMC supplementary untouched. Access `paper.pdf` 19 pages, 0 errors, no
  undefined citations.

## 2026-07-22 — Author information filled (both variants) + recompile

- **Author/affiliation/correspondence filled** (user-provided, confirmed): authors Bijing Liu
  (affil 1,2) and Yong Yang (affil 1,2, corresponding; yangyong1@sgepri.sgcc.com.cn).
  Affil 1: NARI Group Corporation (State Grid Electric Power Research Institute), Nanjing
  211106, Jiangsu Province, China; Affil 2: Beijing Kedong Electric Power Control System Co.,
  Ltd., Beijing 100080, China. No ORCID provided — ORCID fields omitted (optional for CMC).
  Files: `source/manuscript_cmc/paper_cmc.tex` (`\Author`, `\AuthorNames`, `\address`,
  `\corres`), `source/paper.tex` (IEEE Access `\author`/`\address[1..2]`/`\corresp` +
  new `\tfootnote` funding footnote), `source/manuscript_cmc/supplementary_cmc.tex`
  (`\author`, recompiled).
- **Funding statement filled (both variants)**: "This work was supported by the Science and
  Technology Project of NARI Group Corporation (State Grid Electric Power Research Institute)
  (Grant No. [TODO: grant number])." — the grant number is now the **only** remaining [TODO]
  in the manuscript sources.
- **Author Contributions (CRediT) filled — DRAFT, needs author confirmation**:
  Conceptualization, methodology, software, validation, data curation, writing—original draft:
  L.B.; supervision, project administration, resources, funding acquisition, writing—review and
  editing: Y.Y. (in `\authorcontributions` of the CMC variant).
- **Resolved reminder TODOs**: Access-variant AI-disclosure "[TODO: confirm final wording]"
  removed (statement text unchanged and complete). Cover letter
  (`cmc_cover_letter_draft.md`): corresponding-author line, signature (Bijing Liu and Yong
  Yang), and all-author-approval line filled; only the optional suggested-reviewers [TODO]
  remains there.
- **Recompiled clean (MiKTeX, pdflatex→bibtex→pdflatex×2)**: CMC `paper_cmc.pdf` 27 pages,
  0 errors, 0 undefined refs; Access `paper.pdf` 19 pages, 0 errors; CMC supplementary
  5 pages, 0 errors. Page-1 text extraction verified names, both affiliations, corresponding
  e-mail, and funding footnote render correctly. No experimental number or other content touched.
