# C2GES Round 2 Editorial and Venue Review

**Independent decision: MAJOR REVISION — not ready for submission.**

**Applied Sciences fit: Medium-to-low in the current form.** The manuscript is technically careful and reproducible, but its quantitative evidence is a document-conditioned FEVER experiment, while the title and featured application promise power-grid reliability-report use. For the current evidence, the natural handling route would be the journal's **Computing and Artificial Intelligence** section, not an energy/power-systems section. A power-grid-facing submission needs a concrete domain evaluation or a visibly prospective title and application claim.

This review is read-only. It evaluates the revised TeX and the 20-page compiled PDF (SHA-256 `4AECFFBC208431A85365FD0B6108BC6489E6415111A3F4A853490D47379A0532`), the Round-1 review and response, the claim ledger, canonical v2, and the local ten-paper Applied Sciences analysis. It does not infer author metadata and does not treat agent-produced NERC labels as human annotations.

## Major issues

### R2-M01 — The title and venue-facing application claim outrun the quantitative evidence

The title says “for Power Grid Reliability Reports” (`paper_applsci.tex:14`), and the featured application promises technical-incident-report review (`paper_applsci.tex:22`). Yet every quantitative result is from Wikipedia/FEVER (`paper_applsci.tex:20,35,57,67–75`), and the NERC section expressly contains no leaderboard, quantitative result, or expert-adjudicated case (`paper_applsci.tex:254–261,284–291`). The candid disclosure is a strength, but disclosure does not supply applied validation. On PDF page 15, the entire power-grid result is a proposed workflow rather than an observed application outcome.

This is the principal Applied Sciences desk-reject risk: the journal prioritizes a concrete applied contribution and validation, while the present engineering beneficiary is hypothetical. Resolve this through one of two honest routes:

1. Retain the strong domain title only after a sealed, independently annotated NERC evaluation with domain baselines, agreement/adjudication, failure analysis, and at least one fully traceable report case; or
2. Make the title visibly prospective with a small change, for example, **“C2GES: Interpretable Extractive Evidence Selection toward Power-Grid Reliability-Report Review”**, and frame the paper as a leakage-controlled benchmark and application protocol rather than a validated power-grid system.

Real expert annotation is an external human dependency. It must not be simulated. A FEVER-only paper can still be honest without it, but then the title, featured application, abstract, and conclusion must consistently use “toward”, “application protocol”, or equivalent prospective language.

### R2-M02 — The remaining novelty claim is not supported by adequate comparator and ablation evidence

After the role-effect NO–GO, the manuscript's supported contribution is an additive mixture of semantic/lexical relevance, a role head, and positional smoothing plus a strong audit protocol (`paper_applsci.tex:31,115–146,266–282`). The only reported performance baseline is BM25 (`paper_applsci.tex:184–223`). The paper itself acknowledges that source ledgers contain diagnostic modes but excludes them from canonical v2 and postpones query-only, no-role, and no-floor tests (`paper_applsci.tex:197,277–280`). It also discusses contemporary pairwise/setwise/listwise rerankers without evaluating any (`paper_applsci.tex:54`).

Avoiding selective post-hoc ablation was correct for Round 1, but it leaves the editorial novelty/evidence question unanswered. Before submission, run a new prospectively specified comparison family on the unchanged document split and candidate pools. At minimum it should include BM25, lexical+semantic query-only, SBERT/dense-only, no-local, no-role/no-floor, and the full system; preferably add one feasible cross-encoder or modern reranker with frozen snapshot and measured cost. Report all planned modes and multiplicity-aware or clearly hierarchical claim gates. Do not retrofit favorable source modes into the existing confirmatory table.

The local ten-paper analysis is not a journal quota, but it shows why the current evidence looks thin for an AI method paper: comparable Applied Sciences studies normally pair a main table with competitive baselines, ablation/sensitivity evidence, and resource or robustness analysis (`papers/literature/applied_sciences_power_ai_10/analysis/README.md`, “Dataset and experiment-design distillation”). The current paper has excellent audit depth but insufficient method-comparison depth.

### R2-M03 — Round-1 prospective-status wording is not fully closed in the abstract and result framing

Methods now accurately states that seed 2026 was inspected before the W4 freeze and that the study was not prospectively frozen (`paper_applsci.tex:155–156`). However, the abstract says “Across five frozen training seeds” and calls the failed hypotheses “registered” (`paper_applsci.tex:20`); figure captions and later prose repeatedly say “all frozen seeds” (`paper_applsci.tex:203,242,250`). A reader encountering the abstract before Methods can reasonably infer five prospectively fixed seeds or a preregistered five-seed study. This means Round-1 item R1-M01 is improved but not genuinely closed.

Use the same wording everywhere: **“a five-seed frozen continuation and canonical aggregation, including one previously inspected pilot seed.”** Replace “registered claim” with “predefined canonical gate” unless a timestamped registration predating the pilot exists. This wording change does not alter any number or NO–GO decision.

### R2-M04 — Literature positioning does not establish novelty or the closest applied precedent

The Related Work section provides useful coverage of FEVER, summarization, graphs, and reranking (`paper_applsci.tex:41–61`), but it mostly lists families and then states boundaries. It does not compare C2GES against the closest methods by inputs, supervision, candidate scope, interpretability, domain, and evaluation leakage controls. More importantly, the cited bibliography contains no direct Applied Sciences power-grid NLP precedent from the ten-paper corpus. The locally identified closest paper, *A Combined Semantic Dependency and Lexical Embedding RoBERTa Model for Grid Field Relational Extraction* (DOI `10.3390/app131911074`), is absent from `references_cited_verified.bib`.

Add a compact comparison table or a focused synthesis that distinguishes C2GES from sentence evidence retrieval, query-focused extraction, graph/local-context methods, and modern rerankers. Cite the direct power-grid NLP precedent for the specific application-positioning comparison, not merely because it is in the target journal. The gap statement should make clear that protocol integrity and traceability are the demonstrated novelty, while role conditioning and power-grid performance are not.

### R2-M05 — The public reproducibility claim remains incomplete at the submission boundary

The local bundle is unusually strong and its verifier passes, but the manuscript still contains a permanent-repository placeholder (`paper_applsci.tex:173,298,303`). The original Hugging Face revision is also irrecoverable and is correctly disclosed (`paper_applsci.tex:67,303`). Therefore Round-1 R1-M06 remains open, and R1-M05 is only closed as an explicit limitation, not as exact upstream reproducibility.

Before submission, the authors must perform license review, upload the permitted code/data/model/manifest subset, mint a stable URL or DOI, and replace the placeholder. The deposit should preserve the hashes already used by `generated/claim_source_map.json` and the one-command verification route. Do not claim exact upstream regeneration from an unrecorded dataset revision; retain the cache-fingerprint/split-hash boundary.

## Minor issues

### R2-m01 — The main table assigns “GO” to the BM25 reference rows

Table 5 says every displayed gate requires a positive mean difference and positive interval lower bounds (`paper_applsci.tex:186–188`), but the rendered table labels BM25 itself “GO” despite `Delta vs. BM25 = +0.0000` (PDF page 11; canonical `tables/table_main_results.csv`, BM25 rows). A reference row cannot pass a positive superiority gate against itself. Display an em dash or “reference” for BM25 and reserve GO/NO–GO for actual contrasts.

### R2-m02 — “Cost–accuracy trade-off” and the non-dominated-envelope graphic are stronger than the measurements

The abstract calls the result an “auditable cost–accuracy trade-off” (`paper_applsci.tex:20`), while Methods/Results correctly concede that wall time covers a full CPU script, excludes BM25 cost, and is not online latency (`paper_applsci.tex:175,225–237`). Figure 6 additionally labels a “Non-dominated envelope” although only three closely related protocols are plotted and the main baseline is absent (PDF page 14). Call this a resource diagnostic, remove the envelope/Pareto implication, or add comparable end-to-end timing for all baselines under the same boundary.

### R2-m03 — Framework Figure 3 is too dense at journal-page scale

Figure 3 is logically useful, but several node labels are difficult to read in the compiled PDF at normal page scale (PDF page 10; source `paper_applsci.tex:177–180`). Enlarge label fonts, simplify node text, or split the audit and bootstrap portions. Result Figures 4–8 and Tables 5–7 are otherwise legible and use helpful redundant markers/line styles.

### R2-m04 — A small result sentence risks causal interpretation of budget behavior

The sentence that the mixture “can recover additional annotated evidence” at moderate budgets (`paper_applsci.tex:193`) is plausible but not isolated by an ablation, and F1 falls as K grows. State only the observed cutoff-specific comparison until the planned ablations identify which channel changes recovery.

### R2-m05 — Submission metadata and declarations are visibly unfinished

Author, affiliation, correspondence, contributions, funding, ethics confirmation, conflicts, acknowledgments, repository, and AI-use fields still contain `W7_FRONT_MATTER` placeholders (`paper_applsci.tex:15–18,299–308`; PDF pages 1 and 18–19). This is an external author action rather than a scientific flaw, but the file cannot be submitted or circulated as a clean review manuscript in this state.

## Round-1 closure audit

| Round-1 item | Round-2 status | Evidence |
|---|---|---|
| R1-M01 prospective freeze | **Partially closed** | Honest disclosure at `paper_applsci.tex:155–156`; abstract/“registered” wording remains misleading at line 20. |
| R1-M02 Holm claim | **Closed** | Exact implemented inference is stated and absence of Holm is explicit at `paper_applsci.tex:160–168`; `Holm` appears only in the negative disclosure/diagram context. |
| R1-M03 upstream model | **Closed** | Feature, solver, OOF grouping, seeds, serialization, shared ledger, and excluded upstream uncertainty are specified at `paper_applsci.tex:87–96`. |
| R1-M04 downstream implementation | **Closed** | Loss equations and hash-bound implementation table are present at `paper_applsci.tex:115–153`. |
| R1-M05 conversion provenance | **Partially closed, irrecoverable field disclosed** | Deterministic conversion/counts/hashes at `paper_applsci.tex:63–85`; original upstream revision remains unknown at lines 67 and 303. |
| R1-M06 public package | **Open external blocker** | Local manifest/verifier exists, but public DOI/license review remains at `paper_applsci.tex:173,298,303`. |
| R1-M07 component attribution | **Closed** | Unsupported shared-component attribution was removed; bounded exclusion rationale at `paper_applsci.tex:195–197`. |
| R1-m01 gate definition | **Closed with display defect** | Gate definition is consistent at `paper_applsci.tex:160,164,168,187`; BM25 self-gate display needs R2-m01. |
| R1-m02 oracle upper-bound wording | **Closed** | TeX consistently uses privileged-label conditional sensitivity diagnostic (`paper_applsci.tex:96,100`). |
| R1-m03 ledger scope | **Closed** | 810,000 source rows versus 180,000 canonical rows is explicit at `paper_applsci.tex:184`. |
| R1-m04 bootstrap estimand | **Closed** | Sampling, duplicate clusters, weighting, percentile interval, RNG and 2,000-draw limitation at `paper_applsci.tex:160–166`. |
| R1-m05 build warnings/metadata | **Partially closed** | Current PDF is 20 pages; no undefined reference/citation or cited warning class was observed, but author PDF metadata/placeholders remain. |

## Canonical and prohibited-claim verification

**PASS.** Independent checks were rerun against the current manuscript and canonical v2:

- `audit_superseded_claims.py`: PASS for TeX and PDF across all six prohibited/superseded claim classes.
- `verify_claim_sources.py`: PASS for 13 source hashes, 8 generated fragments, 8 figures, and 27 citation keys.
- Independent recomputation tests: 4/4 pass; canonical validation contains 180,000 rows, 15 source runs, and 176/176 evidence checks.
- The primary values in `generated/canonical_numbers.tex` match canonical `table_main_results.csv` and `table_role_effects.csv`: predicted-label K=3 F1 `0.4920 ± 0.0021`; BM25 K=3 `0.4864`; delta `+0.0056`, hierarchical CI `[0.0008, 0.0107]`; predicted-minus-blind `+0.0010`, seed-t CI `[-0.0016, 0.0036]`, hierarchical CI `[-0.0012, 0.0031]`.
- Legacy split `4000/800/800`, legacy point estimates, positive role-effect claims, blanket BM25 superiority, oracle-as-end-to-end, and “Causal-Role-Aware” title language are absent. The string `0.0099` in the current PDF is a legitimate upper endpoint for a canonical oracle-minus-blind interval, not the prohibited legacy gain.

## Verified strengths and venue-calibrated assessment

- The abstract is 165 words and meets the approximately 200-word MDPI target.
- The structure (six primary sections), 20-page length, 8 figures, and 7 tables are compatible with the ten-paper Applied Sciences sample; these are descriptive comparators, not journal quotas.
- FEVER versus NERC provenance, oracle versus deployable protocols, document-conditioned versus open retrieval, and positional versus causal interpretation are unusually clear.
- Negative results are retained rather than hidden, and the claim ledger correctly marks C2-C04, C2-C05, and C2-C09 as NO–GO.
- Tables and result figures are generally readable; generated values and hashes substantially reduce transcription risk.

## External human blockers (do not automate or fabricate)

1. Independent power-grid-domain annotation/adjudication is required only if the authors retain a title or claim implying validated NERC performance.
2. Author identities, affiliations, correspondence, CRediT roles, funding, conflicts, acknowledgments, ethics wording, and the final AI-use declaration require author confirmation.
3. Repository selection, redistribution/license review, upload authority, and DOI minting require human/institutional action.
4. The missing historical Hugging Face revision cannot be reconstructed. Preserve that limitation; a future clean regeneration should pin a revision before execution.

## Decision gate for Round 3

Round 3 should begin only after R2-M01–M05 are answered. The minimum scientifically viable route is: prospective title/application wording; a new, complete baseline/ablation experiment family; corrected freeze language; explicit closest-work positioning; and a public, license-reviewed reproducibility location. If a strong “for Power Grid Reliability Reports” title is retained, independently adjudicated domain evidence becomes mandatory. Without one of those two scope resolutions, the manuscript remains at high desk-reject risk despite its strong statistical hygiene.
