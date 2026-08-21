# Dual-Manuscript Claim Ledger

Updated: 2026-08-05

Status vocabulary:

- `ELIGIBLE-DIAGNOSTIC`: may be reported only with the stated diagnostic scope.
- `ELIGIBLE-E4`: confirmed by the complete registered experiment and independent evidence audit.
- `E4-NO-GO`: the registered evidence gate was completed and rejected the proposed claim.
- `PENDING-E4`: requires the registered complete experiment and independent audit.
- `HUMAN-DEPENDENT`: requires real human review/annotation.
- `LEGACY-ONLY`: reproducibility or limitation context only; not a new main result.
- `PROHIBITED`: contradicted, leaked, fabricated, or otherwise ineligible.

## MA-SQLGrid

| ID | Candidate claim | Current evidence | Status | Permitted wording / next gate |
|---|---|---|---|---|
| MA-C01 | The 2 x 2 prompt protocol is balanced and gold-isolated. | 180 GridDB questions x 4 cells; 720/720 shared audit; stable prompt hash. | ELIGIBLE-DIAGNOSTIC | Protocol/readiness claim only; no model-effect claim until execution. |
| MA-C02 | The external-database protocol generalizes mechanically to RTS-GMLC and SimBench. | 91 AUTO_CANDIDATE questions x 4 cells; 364/364 audit; 91/91 reference SQL safe/executable. | ELIGIBLE-DIAGNOSTIC | State that schema/context/evaluator plumbing generalizes; do not claim text-to-SQL accuracy. |
| MA-C03 | Compact context and shape hints have independent positive effects. | Dual-backbone/GridDB audit: compact execution main effects Qwen -0.0528 [-0.1136, 0.0000] and Granite +0.0139 [-0.0574, +0.0801]; execution interactions Qwen -0.1278 [-0.2449, -0.0339] and Granite +0.0611 [-0.0524, +0.2000]; three-way difference +0.1889 [+0.0067, +0.4310]. | E4-NO-GO | Do not claim two independent positive effects or a backbone-invariant interaction. Report the bounded direction/magnitude sensitivity instead. |
| MA-C04 | MA-SQLGrid improves content retrieval rather than output contract conformance. | Old projection-tolerant rescoring reverses compact/full ordering. | PROHIBITED | Do not claim unless new content/projection-tolerant evidence reverses this diagnosis. |
| MA-C05 | RTS-GMLC and SimBench are publication-ready gold benchmarks. | 91 deterministic AUTO_CANDIDATE records; zero human reviews; development-visible. | PROHIBITED | They are reproducible pilots only. |
| MA-C06 | A reviewed external set supports cross-database accuracy. | Human review packet ready; no completed A/B forms or adjudication. | HUMAN-DEPENDENT | Requires two real reviewers, adjudication, rerun hashes, and honest unsealed status. |
| MA-C07 | Existing GridDB results reproduce earlier behavior. | Legacy predictions re-scored separately under current evaluator. | LEGACY-ONLY | Label all such values legacy/diagnostic and retain projection reversal. |
| MA-C08 | Validator repair provides net benefit with controlled harm. | Existing limited diagnostics only. | PENDING-E4 | Requires trigger precision/recall, repair gain, harm rate, and paired cases. |
| MA-C09 | The method offers a favorable accuracy-cost-latency trade-off. | The audited Qwen and Granite GridDB runs are complete, but the dual-backbone canonical release contains no comparable latency, throughput, token, energy, or memory table. | PENDING-E4 | Requires a common measurement boundary with model/version/token/cost/latency/failure provenance across the intended comparison set. |
| MA-C10 | The clean Qwen/GridDB 2 x 2 run supports bounded factorial and registered-edge findings. | 720/720 canonical rows; 180 paired questions; four cells; 70 template clusters; 20,000 cluster-bootstrap draws; eight registered McNemar tests with Holm adjustment; independent audit passed. | ELIGIBLE-E4 | Report only Qwen2.5-Coder-7B-Instruct Q4_K_M on GridDB and preserve all cell-, edge-, interaction-, and inference-unit qualifications. Granite and external accuracy remain pending. |
| MA-C11 | The promoted Qwen result is isolated from the quarantined run and independently reproducible from canonical artifacts. | Clean rerun only; quarantined directory rejected without reading its artifacts; direct SQLite rescore 720/720; zero mismatches; configuration/data/code/model/prompt hashes verified. | ELIGIBLE-E4 | May report integrity, provenance, and complete Cartesian execution. Do not rehabilitate or numerically cite the quarantined run. |
| MA-C12 | Answer-shape correctness and execution correctness are distinct outcomes in the Qwen/GridDB run. | Canonical taxonomy contains shape-only and execution-only outcomes; hint-present cells include 110 shape-only cases while execution-only is zero. | ELIGIBLE-E4 | Treat answer shape as a diagnostic/contract outcome, not a substitute for execution correctness or proof of content retrieval. |
| MA-C13 | The positive direction of the shape-hint main effect replicates across the two audited quantized backbones on GridDB. | Execution: Qwen +0.2306 [+0.0538, +0.4306], Granite +0.1583 [-0.0200, +0.3665]. Answer shape: Qwen +0.4944 [+0.2662, +0.6912], Granite +0.4528 [+0.2710, +0.6399]. | ELIGIBLE-E4 | May state directional replication for execution with the Granite CI-crossing-zero caveat; answer-shape effects exclude zero for both. Not general model-family robustness. |
| MA-C14 | Prompt-effect magnitude and context interaction are backbone-sensitive in the bounded GridDB comparison. | Granite-minus-Qwen execution shape-main difference -0.0722 [-0.1230, -0.0272]; execution three-way interaction +0.1889 [+0.0067, +0.4310]; F01 execution cell difference -0.1611 [-0.2975, -0.0484], Holm p 3.90e-05; F11 execution difference 0.0000 with CI crossing zero. | ELIGIBLE-E4 | Report paired cell/effect modifiers and complete contrast matrix. Do not turn the F01 gap into a global backbone ranking. |
| MA-C15 | The Granite formal run is independently reproducible and eligible for bounded two-backbone sensitivity analysis. | Independent Granite audit 35/35; 720/720 unique canonical rows and direct SQLite verdicts; zero provider/parse/scoring/retry/resume failures; frozen model/prompt/configuration/data/code hashes match; contaminated Qwen directory not read. | ELIGIBLE-E4 | May report Granite integrity and use its canonical rows in the paired dual-backbone analysis only. |

## C2GES

| ID | Candidate claim | Current evidence | Status | Permitted wording / next gate |
|---|---|---|---|---|
| C2-C01 | The rebuilt FEVER corpus is document-disjoint by normalized Wikipedia title. | 8000/1500/1500 instances; 745/141/145 documents; exact overlap zero. | ELIGIBLE-DIAGNOSTIC | State exact-title grouping and retain redirect/semantic-near-duplicate limitation. |
| C2-C02 | The predicted-label workflow is end-to-end with leakage-controlled train roles. | Train roles generated by document-grouped OOF classifier; dev/test fit on train only. | ELIGIBLE-DIAGNOSTIC | Report upstream accuracy and errors jointly with selector results. |
| C2-C03 | Oracle-label results are end-to-end evidence selection. | Oracle consumes human FEVER veracity labels. | PROHIBITED | Always label conditional/oracle upper-bound and `end_to_end=false`. |
| C2-C04 | Role conditioning significantly improves evidence F1. | Five seeds: predicted-label minus blind at K=3 is 0.00097; seed t-CI [-0.00165, 0.00359] and hierarchical CI [-0.00119, 0.00307]. | E4-NO-GO | Do not present role conditioning as a reliable gain or primary novelty. |
| C2-C05 | C2GES broadly outperforms BM25. | Five seeds: all protocols are about 0.029--0.032 F1 below BM25 at K=1; the registered blanket gate fails. | E4-NO-GO | Report the complete K-dependent pattern; only protocol/K-specific contrasts with their intervals are allowed. |
| C2-C06 | Full-corpus three-protocol execution is reproducible. | Five seeds x three protocols; 15/15 runs; 176/176 evidence checks; frozen code/data/encoder/predicted-label hashes. | ELIGIBLE-E4 | May report the full registered experiment and its bounded findings. |
| C2-C07 | NERC cases prove quantitative power-grid-domain superiority. | Existing NERC labels are agent-generated silver/qualitative material. | PROHIBITED | NERC remains a case study unless real expert annotation is completed. |
| C2-C08 | C2GES offers an interpretable low-cost evidence-selection trade-off. | Seed-2026 component scores, weights, runtime, and candidate traces exist. | PENDING-E4 | Requires five-seed stability, efficiency aggregation, and case audit. |
| C2-C09 | The final role-related title is supported. | The five-seed role gate is NO-GO. | E4-NO-GO | Retain `C2GES`, evidence selection, power-grid application, and interpretable reranking; remove or subordinate `Causal-Role-Aware` as the claimed advance. |

## Manuscript integration rule

Every quantitative sentence in an abstract, Results, Discussion, or Conclusion
must cite a claim ID and an exact canonical artifact plus row/key. A figure or
table derived from non-E4 evidence must be visibly labelled pilot, diagnostic,
legacy, or supplementary. No writing or review agent may promote a claim by
changing the dataset subset, metric, K, seed family, or statistical unit after
seeing the result.
