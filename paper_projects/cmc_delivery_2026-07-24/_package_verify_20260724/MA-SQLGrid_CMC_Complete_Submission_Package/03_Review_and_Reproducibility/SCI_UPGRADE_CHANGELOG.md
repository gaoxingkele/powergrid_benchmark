# SCI Upgrade Changelog — MA-SQLGrid (fast-track: MDPI Electronics primary, IEEE Access fallback)

## Update 2026-07-20 — x10 scale-robustness experiment integrated into BOTH manuscripts; repo v0.2.0 released

The completed x10 scaled-database experiment (deepseek-chat, 180 test questions
byte-identical to v0.1, x10 database = 10x rows + 2 distractor tables, 540 primary
calls + 13 repair calls, 0 provider errors) was integrated into both manuscript
variants and published to GitHub. All numbers verified against
`source/code/experiment_final/outputs_deepseek_x10/RESULTS_SUMMARY.md` and
`analysis/relaxed_metrics_deepseek_x10.json` before writing.

**Headline (v0.1 -> x10, same generator):** strict C2 0.3389 -> 0.3333,
C4 0.7000 -> 0.5944, C5 0.7667 -> 0.6500; compact advantage survives (+26.1 pp
strict vs +36.1 at v0.1), C5 still adds +5.6 pp (vs +6.7); projection-tolerant
reversal persists (C2 0.8167 > C4/C5 0.6944/0.7000). Token economics: C2 input
2011.6 -> 3042.6 (+51%) vs C4 509.3 -> 504.0 (flat, ~6x cheaper at x10).
Diagnosed artifact: the whole C4/C5 drop is the alphabetical `LIMIT 80`
value-inventory truncation (149/180 byte-identical prompts score 101/149 vs
102/149; the 31 changed-prompt questions fall 23/31 -> 6/31); distractor tables
stress only C2 (C4/C5 builders use a fixed 8-table catalog). Builder fidelity:
received original builders reproduce the archived formal prompts byte-for-byte
180/180 (C2 and C4) on v0.1.

**IEEE Access variant** (`source/manuscript/paper.tex`, recompiled clean, 19 -> 21 pp):
abstract sentence; contributions extended to six (new sixth = scale robustness);
new §6 subsection "Scale Robustness on the Second Generator" with the v0.1-vs-x10
strict/projection-tolerant table + token-economics table + full LIMIT-80 artifact
decomposition + distractor caveat; new x10 row in the claim-to-evidence table;
new Limitations paragraph (fixed-cap value scan -> scalable value index; second
generator only; fixed catalog); conclusion + future work; Data Availability -> v0.2.0.

**CMC variant** (`source/manuscript_cmc/`, both PDFs recompiled clean; main 23 -> 24 pp,
supplementary 7 -> 9 pp): abstract sentence; contribution (4) extended; compact new
§5.5 "Scale Robustness at Tenfold Database Size" (small strict-only table + token
contrast + one-paragraph artifact/caveat summary); full detail moved to supplementary
new Section S4 with Table S8 (full v0.1-vs-x10 metrics) and Table S9 (token economics)
plus the complete artifact diagnosis; Table S7 claim map gains the x10 row;
availability statement updated to v0.2.0 and the "four pending modules" caveat
replaced with the accurate remaining-items statement (only the original researchclaw
LLM client and the v0.1 dataset generator remain unavailable; neither is needed to
recompute any reported number). Hardcoded supplementary cross-reference to the
case-study section fixed (5.5 -> 5.6 after renumbering).

**Repository** (github.com/gaoxingkele/ma-sqlgrid): commit
"Add x10 scale experiment + received builder modules" pushed to `main`
(561 files: `code/smoke/` five received modules byte-identical as received,
`code/experiment_final/run_x10_scale.py`, `outputs_deepseek_x10/` with all 540
traces, `code/agent_reference/` shims, x10 analysis script + JSON, updated
`README.md` + `MISSING_ARTIFACTS.md`, `main.py` sys.path line for the repo layout,
`.gitignore` for pycache). Pre-push secret scan clean; `import main` verified in
the repo layout. Release **v0.2.0** published:
https://github.com/gaoxingkele/ma-sqlgrid/releases/tag/v0.2.0

## Update 2026-07-19 — Public reproducibility repository PUBLISHED; Data Availability wired

Public GitHub repository created and pushed: **https://github.com/gaoxingkele/ma-sqlgrid**
(public, default branch `main`, release **v0.1.0** tagged, 3,527 files).

Included: `code/` (evaluator + tests, `experiment_final/` with `main.py`,
`run_second_model.py`, `run_consistency_check.py`, `expand_dataset.py`, `analysis/`,
`outputs/` [900 traces], `outputs_deepseek_chat/`, `outputs_deepseek_consistency/`,
`outputs_stage10_smoke/`, `formal_dry_run/`), `data/` (griddb_maintenance_v2_v0_1 +
_x10), `evidence/` (main results, component ablation, diagnostics, stage14),
`assets/charts/`, `MISSING_ARTIFACTS.md` moved to repo root, plus a NEW root
`README.md` (contents map, reproduce instructions, two-generator evidence summary)
and `LICENSE` (MIT for code; README declares CC BY 4.0 for data/artifacts).

Excluded: `manuscript/`, `AGENTS.md`, `.codex/`, `harness_approvals/`,
`verification/`, stale source-root `README.md`, all `__pycache__/`,
`outputs_deepseek_smoke/`, and a stray reserved-name `nul` file. Pre-push secret
scan (sk-/gho_/ghp_ patterns): clean.

Manuscript: `source/manuscript/paper.tex` Data Availability `[TODO: repository URL]`
replaced with `\url{https://github.com/gaoxingkele/ma-sqlgrid}` (release v0.1.0).
Funding / COI / other TODOs left untouched.

## Update 2026-07-19 — P0-1 and P0-6 experiments COMPLETED (real API runs)

DeepSeek API key available; `run_second_model.py` and `run_consistency_check.py`
executed against `deepseek-chat` (https://api.deepseek.com/v1, temperature 0,
byte-identical archived prompts, same packaged evaluator). Evidence:
`source/code/experiment_final/outputs_deepseek_chat/`,
`analysis/relaxed_metrics_deepseek.json`, `analysis/efficiency_stats_deepseek.json`,
`outputs_deepseek_consistency/consistency_report.json`. Manuscript updated
(abstract; five-contribution list; §5 second-model protocol paragraph; new §6
subsection "Second-Generator Validation" with cross-model metric table + DeepSeek
token/latency table + determinism paragraph; efficiency triangulation after the
real-token table; claim-to-evidence rows; limitations; conclusion; data
availability; AI disclosure). Headline numbers below under C11/C12.

Date: 2026-07-17. All numbers below were independently recomputed from the archived
formal-run artifacts (`source/code/experiment_final/outputs/`: 900 predictions,
900 scores, 900 traces). No experimental number was invented; no new model runs
were possible in this environment (KRILL_API_KEY not set), so every item needing
new API calls is delivered as a prepared, documented runner script.

## A. Analysis recomputations (REAL numbers, now in the manuscript)

### A1 / P0-2 — Order-insensitive metrics: DONE
Script: `source/code/experiment_final/analysis/recompute_relaxed_metrics.py`
(output `analysis/relaxed_metrics.json`). Recomputed from predictions.jsonl +
database.sqlite with the packaged evaluator's normalization.

| Condition | Strict | Order-insensitive (exact projection) | + projection-tolerant |
|---|---|---|---|
| C1 | 0.3944 (71/180) | 0.4056 (73/180) | 0.8000 (144/180) |
| C2 | 0.4389 (79/180) | 0.4778 (86/180) | 0.8722 (157/180) |
| C3 | 0.4000 (72/180) | 0.4056 (73/180) | 0.5000 (90/180) |
| C4 | 0.7000 (126/180) | 0.7444 (134/180) | 0.7444 (134/180) |
| C5 | 0.7278 (131/180) | 0.7722 (139/180) | 0.8056 (145/180) |

**Deviation from the assessment**: the assessment reported a single relaxed metric
(C1 0.500 / C2 0.572 / C3 0.461 / C4 0.744 / C5 0.806). My C4/C5 values match it
exactly; C1–C3 could not be reproduced under any single rule I tested
(order-insensitive only; +name-based projection; +ordered column subsets;
+any column permutation). Per instructions the manuscript uses MY numbers, under
two precisely defined relaxed metrics. Substantively my recomputation is
STRONGER than the assessment's finding: under the fully projection-tolerant view
C2 (0.8722) actually exceeds C4 (0.7444), i.e. the strict headline gap is
dominated by answer-contract conformance (projection + ordering conventions),
not row-content retrieval. The manuscript now says this explicitly.
Manuscript changes: new §6 subsection "Evaluation-Convention Sensitivity" with
the 3-metric table and an honest interpretation paragraph; new §5 paragraph
stating the two annotation-protocol conventions, that all conditions share the
same instruction text but only C4/C5 receive the per-question convention hints,
and that the shape-inference rules were designed against the annotation
protocol (coupling by construction); claim-to-evidence table row 1 boundary
updated accordingly; abstract mentions the order-insensitive ranking.

### A2 / P1-5 — Real token/cost table: DONE
Script: `analysis/recompute_efficiency.py` (output `analysis/efficiency_stats.json`),
aggregated from provider-reported usage in the 900 prediction records.
Real input tokens/question: C1 5007.7, C2 6346.7, C3 4756.3, C4 4859.0, C5 5309.8;
output tokens: 45.0 / 45.8 / 47.3 / 52.0 / 197.5; latency mean (median) ms:
3259.8 (1998.0) / 2959.0 (1999.5) / 2895.1 (1959.0) / 2887.5 (2102.5) / 5562.5 (3845.5).
C4-vs-C2 real input reduction = **23.4%** (assessment said ~23% — confirmed);
estimated template reduction 63.5% (710.3→259.2); fixed serving-side overhead
~4500–4600 tokens/call; full run 4.73M input + 69.8k output tokens.
Manuscript: new Table "Measured API resource consumption" in §6 + honest
paragraph separating template vs measured savings; abstract rewritten to state
both numbers (no more bare "710→259" claim); claim-to-evidence token row updated.

### A3 / P0-6 (partial, from existing traces) — Determinism evidence: DONE
From the 900 archived calls: temperature fixed at 0 (runner hyperparameters);
898/900 calls succeeded on first attempt, 2 required one retry (1 in C1, 1 in C4);
zero provider errors in final records. Added to the §5 single-pass-protocol
paragraph, explicitly framed as NOT replacing a repeated-run study.
UPDATE 2026-07-19: the 3-repeat study has now been executed (see C12).

### A4 / P2-2 — Case studies from traces: DONE
New §6 "Case Analysis" subsection with three verbatim-from-trace cases:
- Q021 (kept): contract enforcement (ORDER BY + projection).
- Q110 (new): execution-guided reranking success — candidate 0 hallucinates
  `wo.schedule`, fails execution; ranker selects executable candidate 1 (correct).
- Q161 vs Q156/Q157/Q158/Q160/Q162 (new): repair success vs the 5 residual C5
  execution errors, all on one question template ("work orders assigned to
  technician X"). Root cause verified from contexts.jsonl: compact context omits
  `work_orders.scheduled_date` while the shape hint asks to project it and the
  table comment says "schedule", so the model hallucinates `schedule_date`
  (4 cases) / `schedule` (1 case); the bounded repair fixes it once (Q161) and
  reproduces the same wrong column in the other five.

### A5 / P2-3 — Prompt templates appendix: DONE
New Appendix A reproducing verbatim the direct-generation template (C1–C4),
the C5 candidate-generation template, the C5 bounded-repair template (all from
main.py), a description of the four context-block variants, and the full
rendered C4 compact domain context for Q021 (from the archived trace).

## B. Manuscript text hardening

### B6 / P0-5 — Title & terminology: DONE
Title: "MA-SQLGrid: A Multi-Stage Context-Grounding Framework for Text-to-SQL
over Power Grid Maintenance Databases" ("Multi-Agent"→"Multi-Stage" — matches
the fixed-order pipeline architecture; "Robust" removed). Intro adds an explicit
terminology note (multi-stage, role-specialized, NOT an interacting multi-agent
system; system name retained for artifact continuity). Keywords updated.
The "robust" bounded-sense paragraph reworded (no longer title-referencing).

### B7 / P1-4 — Jargon sweep: DONE
Removed/replaced all pipeline-internal jargon: "repaired formal run"→"archived
formal run", "repaired artifact chain"→"archived artifact chain", "repaired
Stage 13/14 artifacts"→"archived run artifacts released with the paper",
"protocol-B formal pass"→"single archived formal pass", "repaired results"→
"reported results", residual "multi-role"→"multi-stage". Verified zero
remaining occurrences of: repaired Stage / protocol-B / bounded submission.

### B8 / P1-3 — Feature-comparison table: DONE
New Table in §2.2 comparing DIN-SQL, MAC-SQL, CHESS, MAG-SQL, SQLFixAgent,
CHASE-SQL vs MA-SQLGrid on 7 capability dimensions (schema selection,
value/content linking, answer-shape inference, multi-candidate, execution-based
validation, bounded repair, domain specialization), based only on already-cited
papers' documented mechanisms; caption states entries are documentation-based,
no performance claim. No new references were needed (all six systems already in
references_verified.bib, which was externally verified per the assessment), so
no unverifiable citations were added.

### B9 / P0-4 (partial) — Disclosures & template: DONE (content), template conversion deferred
- GPU sentence DELETED; replaced with accurate statement (hosted API generation;
  local machine only prompts/SQLite/scoring; no GPU in any reported number).
- Added back-matter: Data Availability (with [TODO: repository URL]), AI Use
  Disclosure (model-as-subject + AI writing/coding assistance, with [TODO:
  venue wording]), Funding [TODO], Conflicts of Interest ([TODO confirm]).
- Author/affiliation placeholders left as placeholders (per instructions).
- Template kept as IEEE Access (`ieeeaccess` class). NOTE: MDPI Electronics
  conversion happens at submission time if Electronics is chosen; content edits
  were kept venue-neutral. `\bibliography{references}` fixed to
  `\bibliography{references_verified}` (a `references.bib` did not exist).
- LaTeX compile NOT verified locally: no pdflatex/latexmk/tectonic on this
  machine and ieeeaccess.cls is not in the package. Structural checks pass
  (balanced environments; all \ref labels defined; all \cite keys present in
  references_verified.bib). [TODO: compile on a TeX-equipped machine.]

### B10 / P0-2 (§5 statement): DONE
§5 now explicitly states the answer-shape inference rule's relationship to the
annotation protocol: gold ordering + minimal-projection conventions come from
the protocol, the shape stage encodes exactly these conventions, hints go only
to C4/C5, and part of the strict gap is convention conformance (quantified in §6).

## C. Experiment infrastructure (C11/C12 EXECUTED 2026-07-19; C13 partially blocked)

### C11 / P0-1 — Second-model run: DONE (2026-07-19)
Executed with `deepseek-chat` (direct endpoint, temperature 0): 540 calls,
0 provider errors, safe-SQL rate 1.0 in all conditions.
Strict execution accuracy: C2 0.3389 (61/180), C4 0.7000 (126/180),
C5 0.7667 (138/180) — compact-context gain replicates and is LARGER
(C4−C2 = +36.1pp vs +26.1pp on gpt-5.4-mini); validation gain replicates
(C5−C4 = +6.7pp vs +2.8pp). Set-exact: 0.3667/0.7944/0.8278; set-relaxed
(projection-tolerant): 0.8500/0.7944/0.8278 — the convention-sensitivity
reversal (C2 > C4 under projection tolerance) REPLICATES; now a cross-model
result. Real input tokens/question 2011.6/509.3/680.5 → C4-vs-C2 reduction
74.7% on the clean direct endpoint (vs 23.4% on the original proxy stack with
~4.5k fixed overhead tokens/call; template estimate 63.5% — triangulated in
the manuscript). C5 ranker reimplementation validated at 167/169 (98.8%)
agreement with archived selections before use. Runner details below (as prepared):
`source/code/experiment_final/run_second_model.py` — stdlib-only
OpenAI-compatible client, parameterized `--model/--base-url/--api-key-env/
--provider/--conditions/--max-questions/--output-dir`; runs C2/C4/C5 on the
same 180 questions; writes `outputs_<model>/` in the identical schema.
Fidelity design: reuses the BYTE-IDENTICAL archived prompts from
`outputs/traces/` (the missing `dev_chess_style_pilot` module is not needed);
C5 validator/ranker/repair reimplemented from the paper's published weight
specification and VERIFIED against the archive: 167/169 (98.8%) agreement with
the archived candidate selections on non-repair cases. Commands + cost estimate
(~4M input tokens/model) in `README_EXPANSION.md`.

### C12 / P0-6 — 3-repeat consistency check: DONE (2026-07-19)
Executed: 3 repeats × 180 questions × {C4, C5} on deepseek-chat at temperature 0
(1080 calls). Per-repeat execution accuracy: C4 0.7056/0.6944/0.7000,
C5 0.7667/0.7667/0.7611 (max spread 1.1pp). Per-question verdict agreement
(all 3 repeats same correct/incorrect verdict): 98.3% both conditions.
Exact SQL string agreement: C4 82.2%, C5 77.2% — token-level nondeterminism
exists at temperature 0, but aggregate metrics and verdicts are highly stable.
Output: `outputs_deepseek_consistency/consistency_report.json`. Added to
manuscript §6 determinism paragraph, combined with the original-run 898/900
first-attempt evidence. Runner details below (as prepared):
`source/code/experiment_final/run_consistency_check.py` — 3 repeats at
temperature 0 (default C4,C5; configurable), full C5 pipeline repeated each
time; reports exact-SQL agreement, evaluator-verdict agreement, per-repeat
accuracy to `consistency_report.json`. Command in README_EXPANSION.md.

### C13 / P1-2 — Dataset expansion: SCRIPT DONE AND RUN (re-run of conditions awaits API key)
`source/code/experiment_final/expand_dataset.py` — built
`source/data/griddb_maintenance_v2_x10/`: all entity tables x10 via
deterministic block replication with convention-preserving names (asset
prefixes TX-/BR-/... derived from data; person/location name pools; vocabularies
unchanged) + 2 distractor tables (vegetation_inspections 60 rows,
spare_parts_inventory 12 rows). Gold SQL validated on the scaled DB:
**200 questions, 0 errors** (packaged evaluator). Re-running C2/C4/C5 on it
needs the API key AND (for C4/C5 context regeneration) the missing pilot
module — both options documented in README_EXPANSION.md §3.

### C14 / P0-3 — Packaging fixes: DONE (code-supply item remains for the author)
- Evaluator tests: **13/13 passing** (was 2/13). Root cause: tests resolved the
  dataset relative to the wrong parent; now search upward for
  `data/griddb_maintenance_v2_v0_1`. Assertions untouched.
- `main.py`: `/media/lenovo/...` hardcoded fallback REMOVED (now raises a clear
  error / uses MA_SQLGRID_WORKSPACE); fragile `parents[2]` guarded.
- `MISSING_ARTIFACTS.md` documents the four artifacts the author must supply
  (`dev_chess_style_pilot`, `minimal_text2sql_smoke`, `researchclaw.llm.client`,
  `build_griddb_maintenance_v2.py`), their roles, and the suggested package layout.

## D. Venue recommendation state

- **MDPI Electronics (primary)** [updated 2026-07-19]: P0-1 second-model
  results DONE (deepseek-chat; see C11) and P0-6 consistency check DONE (see
  C12); both are in the manuscript. The two assessment-flagged mines
  (eval-convention circularity, token-claim inflation) are defused with real
  cross-model numbers (reversal replicates; 23.4%/63.5%/74.7% triangulation).
  Remaining before submission: MDPI template conversion + real
  author/ORCID/funding/COI.
- **IEEE Access (fallback)**: template already compliant; P0-1 requirement now
  satisfied.
- Still blocked (needs the missing `dev_chess_style_pilot` context builder, not
  the API key): P1-2 scaled-DB (x10) C4/C5 re-run and any Spider/BIRD transfer
  probe (P1-1 also needs a dataset-selection decision first).
- Remaining author-side TODOs in the manuscript: repository URL, funding, COI
  confirmation, real names/affiliations, venue-specific AI-disclosure wording,
  LaTeX rebuild / compile check on a TeX machine (and MDPI template port if
  Electronics).

## 2026-07-19 — First LaTeX compile of machine-edited manuscript

- **Compile status**: clean — first-ever compile of `source/manuscript/paper.tex` (692-line machine-edited tex): `pdflatex -> bibtex(references_verified) -> pdflatex x2`, 0 errors, **19 pages**, `source/manuscript/paper.pdf` built.
- **Build setup fixed**: manuscript dir lacked class/assets — copied `ieeeaccess.cls`, `IEEEtran.bst`, `spotcolor.sty`, `logo.png`, `notaglinelogo.png`, `bullet.png`, all `t1-*` Formata/Times font files (.pfb/.tfm/.map) and `.fd` files from the c2ges source dir; copied `../assets/charts/*.png` into `manuscript/charts/` (4 figures referenced, all resolve).
- **Defects fixed**: 1 structural — the 8-column feature-comparison table (`tab:feature-comparison`) overflowed `\textwidth` by 134pt; wrapped in `adjustbox{max width=\textwidth}` (tabular* -> tabular). No other errors: underscores/verbatim/appendix all compiled as written. No numbers changed.
- **PDF content verification**: title "Multi-Stage" present; SECOND-GENERATOR VALIDATION section present; deepseek numbers 0.3389 (x4) and 74.7 (x5) present; EVALUATION-CONVENTION SENSITIVITY table present; `deepseek-chat` (x21).
- **Remaining acceptable warnings**: 13 bibtex `empty journal` warnings (arXiv-style entries); Formata substitution font warnings; class-level header/footer overfulls; residual content overfulls all <16pt. No undefined references or citations.

## 2026-07-19 — CMC (Tech Science Press) variant created: `source/manuscript_cmc/`

- **Build status**: clean. `paper_cmc.tex`: pdflatex -> bibtex(references_cmc) -> pdflatex x2,
  0 errors, 0 overfull boxes, 0 undefined refs/citations — **23 pages** (`paper_cmc.pdf`).
  `supplementary_cmc.tex`: pdflatex x2, clean — **7 pages** (`supplementary_cmc.pdf`).
  Class: `Definitions/tsp.cls` with options `[cmc,article,submit,moreauthors,pdftex]`
  (template Definitions/ dir copied wholesale). One machine-level fix was needed:
  MiKTeX could not build the `stix-mathcal` PK font (used by tsp's math setup for
  `\mathcal`); resolved with `miktex fontmaps configure`. No numbers changed anywhere.

- **Structure mapping (IEEE Access 9 sections + appendix -> CMC 6 sections)**:
  - Introduction -> 1 Introduction (5-contribution prose rewritten as a 4-item numbered
    contribution list per CMC convention; content-identical, items 4+5 merged; bounded-robustness
    paragraph and reorganized paper-organization paragraph retained).
  - Related Work -> 2 Related Work (3 subsections unchanged; ADDED the in-journal precedent:
    Borovčak K, Bagić Babac M, Mornar V. Comput Mater Contin. 2026;88(2):80,
    doi 10.32604/cmc.2026.078330 — verified against the local PDF — with 2 positioning
    sentences at the end of 2.3).
  - Problem Formulation -> folded into 3 Method as subsection 3.1; Method body split into
    3.2 Framework Overview / 3.3 Compact Schema-Value Selection / 3.4 Value Normalization /
    3.5 Answer-Shape Inference / 3.6 Generation, Validation, and Bounded Repair.
  - Experiments -> 4 Experimental Setup (4.1 Dataset / 4.2 Conditions and Generators /
    4.3 Metrics, Contract, Conventions).
  - Results + Discussion -> merged 5 Results and Discussion (5.1 Main Results /
    5.2 Evaluation-Convention Sensitivity / 5.3 Component Ablation / 5.4 Second-Generator
    Validation and Consistency / 5.5 Error Analysis and Case Studies (condensed) /
    5.6 Discussion (condensed from 7 to 4 paragraphs, no claims dropped)).
  - Limitations -> folded into 6 Conclusions and Limitations.
  - Appendix (prompt templates) -> Supplementary Section S1; per-question case SQL listings
    -> Supplementary Section S2 (main text 5.5 keeps condensed case summaries + pointers).

- **Table disposition (13 -> 6 main + 7 supplementary)**:
  - KEPT in main: Table 1 feature comparison; Table 2 formal protocol summary (main results);
    Table 3 measured API tokens (efficiency); Table 4 strict-vs-relaxed convention sensitivity;
    Table 5 C4 component ablation; Table 6 cross-model second-generator comparison.
  - MOVED to supplementary (each referenced from main text): S1 implementation details,
    S2 dataset characterization, S3 paired sign-test comparisons (key numbers kept in 5.1 prose),
    S4 deepseek-chat resource consumption (74.7% numbers kept in 5.4 prose), S5 tag-level
    diagnostics (headline deltas kept in 5.5 prose), S6 residual error taxonomy (key counts in
    5.5 prose), S7 claim-to-evidence map.
  - Figures: all 4 kept (architecture, pipeline, main results, multi-metric); [H] placement,
    captions below per CMC. Architecture/pipeline PNGs (1408 px wide) displayed at 11.9 cm
    so effective resolution is 300 dpi; fig_main_results at 11 cm (300 dpi); fig_multi_metric
    at full width (~335 dpi).

- **References**: 45 -> 46 (added the CMC precedent), rebuilt for `Definitions/vancouver.bst`
  in `references_cmc.bib`: 15 ACL/KDD/CHI/AAAI entries converted to @inproceedings with
  NLM-style "Proceedings of ...; date; location" booktitles; 24 arXiv entries converted to
  @misc with the identifier in `note` (vancouver.bst strips dots from the journal field);
  journal entries given ISO4 abbreviated names (VLDB J, Artif Intell Rev, ACM Trans Softw
  Eng Methodol, Adv Eng Inform, Found Trends Databases, Comput Mater Contin). All in-text
  citation groups merged to single \cite{a,b,c}; max consecutive run = 4 (<=5 rule OK).
  Local bst patch: added `new.block` in FUNCTION {misc} to fix "et al.." double periods.
  Abstract rewritten to CMC flow (~300 words, background->method->results->conclusion,
  no citations); keywords expanded to 7 semicolon-separated.

- **Back matter**: TSP 6-statement block in exact order — Acknowledgement (contains the
  mandatory generative-AI-use disclosure in TSP wording, adapted from the old "AI Use
  Disclosure" section), Funding Statement [TODO], Author Contributions [TODO, CRediT
  skeleton + mandatory closing sentence], Availability of Data and Materials (sanctioned
  "openly available" wording, https://github.com/gaoxingkele/ma-sqlgrid v0.1.0, + note that
  4 upstream modules are pending upload), Ethics Approval (not applicable), Conflicts of
  Interest, then \supplementary listing S1/S2 + Tables S1–S7.

- **PDF content verified**: deepseek 0.3389 (x3) and 74.7 (x4) present; 0.7667 (x5);
  convention-sensitivity table (Order-insensitive / projection-tolerant columns) present;
  numbered contribution list present; Borovčak citation rendered as
  "Comput Mater Contin. 2026;88(2):80"; 8 [TODO] markers preserved; no "et al.." artifacts.

- **Remaining TODOs before submission**: real author names/affiliations/email + ORCID;
  funding statement; CRediT roles; COI confirmation; supplementary link is the class
  placeholder (\linksupplementary); figures remain PNG — TSP prefers .tif and wants
  line art >= 900 dpi, so the two diagram PNGs (216 dpi at full width, 300 dpi as scaled)
  should ideally be regenerated as high-res/vector before submission; cover letter
  (originality, non-simultaneous submission, all-author approval, COI, APC commitment).
  Page count 23 => APC = $1,600 + 8 x $100 = $2,400 at current typesetting.

## 2026-07-22 — Final micro-polish per CMC_READINESS_AUDIT.md (assistant-fixable items #8 and #10)

- **Cover letter refreshed** (`cmc_cover_letter_draft.md`): release reference updated
  v0.1.0 -> v0.2.0; the stale "four upstream context-builder modules pending" data-availability
  bullet replaced with the current state (second-generation builders included and reproduce the
  archived experiment prompts byte-for-byte, 180/180; only the original researchclaw LLM client
  shim and the v0.1 dataset-generator script remain unreleased, neither affecting any reported
  number); trace count corrected 2,520 -> 3,073 (2,520 original + 540 x10 main + 13 x10 repair
  calls); new contribution bullet #3 added for the x10 scale-robustness stress test (+26.1 points
  strict at flat token cost, 51% prompt growth for full-schema, degradation traced to the
  31-question value-list truncation artifact with stated fix path) — contributions renumbered 1–5;
  explicit COI sentence added ("The authors declare no conflicts of interest related to this
  submission."). All [TODO] author markers preserved.
- **References patched** (`source/manuscript_cmc/references_cmc.bib`), all values verified via
  api.crossref.org by DOI (plus Springer landing page for the article number of huang2024survey):
  quamar2022natural -> 11(4):319–414; katsogiannismeimarakis2023survey -> 32(4):905–936;
  huang2024survey -> 57(7):175 (Crossref vol/issue; Springer article no. 175);
  beyer2022verification -> 31(4):1–69; pauwels2024validation -> 60:102426 (article number).
  borovcak2026evaluating left as `88(2):80` **deliberately**: the CMC landing page
  (techscience.com/cmc/v88n2/67604) displays "Article Number: 80", so the current form matches
  the journal's own citation style (Crossref's page field "1-10" is internal pagination).
- **Recompiled** `paper_cmc.tex` (pdflatex + bibtex + 2x pdflatex, MiKTeX): 24 pages, 0 errors,
  0 undefined citations; remaining BibTeX "empty pages / missing publisher" warnings are the
  pre-existing conference/arXiv entries where NLM format carries no page field. Supplementary
  untouched (no recompile needed). Experimental numbers untouched throughout.

## 2026-07-22 — Author information filled (both variants) + recompile

- **Author/affiliation/correspondence filled** (user-provided, confirmed): authors Bijing Liu
  (affil 1,2), Chenglong Sun (affil 1,2) and Yong Yang (affil 1,2, corresponding;
  yangyong1@sgepri.sgcc.com.cn). Affil 1: NARI Group Corporation (State Grid Electric Power
  Research Institute), Nanjing 211106, Jiangsu Province, China; Affil 2: Beijing Kedong
  Electric Power Control System Co., Ltd., Beijing 100080, China. No ORCID provided — ORCID
  fields omitted (optional for CMC). Files: `source/manuscript_cmc/paper_cmc.tex` (`\Author`,
  `\AuthorNames`, `\address`, `\corres`), `source/manuscript/paper.tex` (IEEE Access
  `\author`/`\address[1..2]`/`\corresp` + new `\tfootnote` funding footnote),
  `source/manuscript_cmc/supplementary_cmc.tex` (`\author`, recompiled).
- **Funding statement filled (both variants + Access Funding section)**: "This work was
  supported by the Science and Technology Project of NARI Group Corporation (State Grid
  Electric Power Research Institute) (Grant No. [TODO: grant number])." — the grant number is
  now the **only** remaining [TODO] in the manuscript sources.
- **Author Contributions (CRediT) filled — DRAFT, needs author confirmation**:
  Conceptualization, methodology, software, writing—original draft: L.B.; validation, data
  curation, investigation, writing—review and editing: S.C.; supervision, project
  administration, funding acquisition, writing—review and editing: Y.Y. (in
  `\authorcontributions` of the CMC variant).
- **Resolved reminder TODOs**: COI "[TODO: confirm for all listed authors]" removed in both
  variants (author list now final; declaration unchanged); Access AI-disclosure "[TODO: adapt
  wording]" removed (statement text unchanged and complete). Cover letter
  (`cmc_cover_letter_draft.md`): corresponding-author line, signature (Bijing Liu, Chenglong
  Sun, and Yong Yang), and all-author-approval line filled; only the optional
  suggested-reviewers [TODO] remains there.
- **Recompiled clean (MiKTeX, pdflatex→bibtex→pdflatex×2)**: CMC `paper_cmc.pdf` 24 pages,
  0 errors, 0 undefined refs; Access `paper.pdf` 21 pages, 0 errors; CMC supplementary
  9 pages, 0 errors. Page-1 text extraction verified all three names, both affiliations,
  corresponding e-mail, and funding footnote render correctly. No experimental number or other
  content touched.
