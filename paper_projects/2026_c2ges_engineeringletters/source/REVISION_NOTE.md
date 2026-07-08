# Post-Freeze Manuscript Revision Note

This directory is an isolated post-freeze manuscript revision for the
role-selective graph-gate update. It does not replace the frozen `deliverables/`
package.

Single source for revised quantitative claims:

- `../experiment_outputs/c2ges_role_selective_graph/summary.json`

Scope of this revision:

- Retitles the manuscript as role-aware evidence selection rather than making
  graph/counterfactual modeling the title-level promise.
- Defines graph consistency as active only for `propagation_or_response` and
  `mitigation`.
- Updates the manuscript from the frozen `0.2933` full C2GES result to the
  revised `0.2983` full C2GES result.
- Replaces the old no-graph comparison with `+0.0060` evidence F1, 95% CI
  `[0.0014, 0.0119]`, `p=0.0254`.
- Adds role-stratified graph-effect reporting.
- Adds deterministic scoring constants for query relevance, role cues, graph
  proximity, chain support, role-gated graph signal, and selected mixture
  weights.
- Adds per-role full C2GES precision/recall/F1 and deltas against TF-IDF query
  retrieval and NoRole.
- Adds a scoped post-freeze BM25 and K-sensitivity supplement from
  `../bm25_k_sensitivity/experiment_outputs/bm25_k_sensitivity/summary.json`.
  At the primary `K=3` budget, C2GES reaches `0.2983` evidence F1 versus
  BM25 query retrieval at `0.2273`, with paired document-cluster delta
  `+0.0710`, 95% CI `[0.0423, 0.1000]`, and bootstrap `p<0.001`.
- Adds bounded `K={1,3,5}` sensitivity reporting without changing the primary
  `K=3` benchmark budget.
- Keeps the claim bounded: role compatibility is the primary driver; graph
  consistency is a small role-selective auxiliary signal.

Out of scope:

- Stronger learned or neural retrieval/reranking baselines.
- Segmentation sensitivity sweeps.
- New datasets or relabeling.
- Claims of full causal inference, graph neural inference, causal discovery, or
  power-system counterfactual simulation.

Verification:

- Paper-Harness run `run_20260626-164318` approved the scoped optimization plan.
- Rebuilt `paper.pdf` with `pdflatex -> bibtex -> pdflatex -> pdflatex`.
- Current optimized PDF is 15 pages.
- Final text scans confirmed the old title phrase
  `Causal and Counterfactual Graph-Enhanced` is absent.
- Final text scans confirmed old graph-negative values and wording
  `0.2933`, `0.0010`, `0.8686`, `not significant`, and `negligible` are absent.
- Final text scans confirmed revised values and method constants are present,
  including `0.2983`, `0.0060`, `8000`, `15/21/21/19/19`, `0.45`, `0.55`,
  `0.08`, `0.8`, and `0.25`.
