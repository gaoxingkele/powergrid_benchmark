# C2GES Original-Title Rebuild Protocol v0.1

## Objective

Construct an auditable extractive-summarization benchmark from public NERC
reports that contain an official `Executive Summary`, then evaluate a real
causal-graph and counterfactual sentence selector without treating machine
annotations as human gold.

## Data boundary

- Source documents: the 40 public NERC PDFs listed in the local frozen manifest.
- Reference summary: text under the report's official `Executive Summary`
  heading. Reports without that heading are excluded from the primary benchmark.
- Candidate text: sentence-segmented report text after removal of the executive-
  summary prefix. The builder records the removed prefix and overlap diagnostics.
- Causal supervision: the existing five-role question/evidence records are
  machine-verified candidates. They are used only to construct a silver causal
  graph and causal-coverage diagnostics, never as human gold.
- No restricted document, manuscript, or private note is sent to an external API.

## Methods

The registered comparison contains `lead`, `centroid`, `textrank`, `role`,
`graph_no_cf`, and `c2ges_full`. `c2ges_full` combines document-centroid
relevance, projected causal-role evidence, graph propagation, deterministic
counterfactual sensitivity, and a positional prior. Mixture weights are selected
on the hash-defined development documents only and are then frozen for test.

## Primary outcomes

- Primary: ROUGE-L F1 at five extracted sentences.
- Secondary: ROUGE-1/2 F1, role-node coverage, adjacent causal-path coverage,
  redundancy, and results at ten sentences.
- Unit of analysis: report. Paired report-level bootstrap intervals are used for
  full C2GES minus each comparator.

## Integrity rules

1. Never copy numeric results from the historical Word draft.
2. Never call the silver graph human or expert gold.
3. Keep every included/excluded report and its reason in the build manifest.
4. Do not tune on test reports.
5. Do not delete failed runs; create a new run directory for every attempt.

