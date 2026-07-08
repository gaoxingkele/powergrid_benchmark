# Reproduction Plan

## Target Scope

Reproduce or validate the scoped post-freeze C2GES claims for causal-role sentence evidence selection over NERC reliability report excerpts.

## Shared Code Dependencies

- Python environment with `numpy`, `rouge-score`, and the baseline/ranker dependencies used by `verification_pilot/scripts`.
- LaTeX environment if local PDF rebuild is required.

## Paper-Specific Implementation

- Preserve `source/paper.tex` as the current manuscript source.
- Treat `source/REVISION_NOTE.md` and `source/OPTIMIZATION_PLAN.md` as the active reviewer-facing change plan.
- Do not make new graph, counterfactual, causal-inference, or SOTA claims without new evidence.

## Dataset and Grid System

- Dataset named in evidence: `nerc_causal_qa_40doc_agent_audit`.
- 40 documents, 200 causal questions, 608 evidence sentence IDs.
- Labels are agent-rewritten and agent-verified candidate labels, not human gold.

## Experiment Matrix

- Primary `K=3` evidence selection.
- C2GES full, no-role, no-graph, query-only, BM25 query, TF-IDF query, SBERT query.
- Role-stratified reporting over trigger event, root cause, propagation/response, impact, and mitigation.

## Expected Outputs

- `summary.json`
- `details.jsonl`
- `metadata.json`
- manuscript PDF
- ARA evidence entries under `ara_artifacts/2026_c2ges_engineeringletters/evidence/`

## Acceptance Criteria

- Full C2GES evidence F1 remains tied to the imported evidence values, not newly invented values.
- Graph effect is framed as small and role-selective.
- Method constants are explicit enough for readers to understand the deterministic scorer.
- Limitations clearly state missing expert-gold labels and missing stronger learned retrieval baselines.

## Known Blockers

- Current smoke run fails before execution because `numpy` is missing.
- Full execution likely also needs omitted `verification_pilot` assets.
- `pdflatex` is not available in the current shell.
