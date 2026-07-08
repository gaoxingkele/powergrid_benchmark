# C2GES Manuscript Optimization Plan

## Context

The current post-freeze revision already fixes the original graph-negative
problem by using the role-selective graph gate:

- `c2ges_full` evidence F1: `0.2983`
- `c2ges_no_graph` evidence F1: `0.2923`
- full minus no-graph: `+0.0060`, document-cluster 95% CI
  `[0.0014, 0.0119]`, `p=0.0254`
- role-selective graph gains appear in `propagation_or_response` and
  `mitigation`

The newest agentic review recognizes this revision. The remaining weaknesses are
not mainly about whether graph has any signal. They are about paper positioning,
method reproducibility, and whether the empirical story is framed at the right
level of ambition.

## Core Diagnosis

The paper should be optimized as a role-conditioned evidence-selection benchmark
paper with a transparent role-aware reranker, not as a broad
graph/counterfactual summarization paper.

Current highest-risk mismatch:

- Title and some framing still foreground `Graph-Enhanced` and
  `Counterfactual`.
- Actual evidence supports role-aware evidence-ID reranking as the primary
  contribution.
- Graph consistency is useful but small and role-selective.
- Counterfactual meaning is limited to component ablation.

If this mismatch remains, reviewers will continue to expect stronger graph
modeling, stronger causal inference, and stronger summarization baselines than
the paper is trying to provide.

## Recommended Plan

### Priority 1: Reposition the paper

Change the title and opening framing so the first signal is the real
contribution:

> Causal-Role-Aware Extractive Evidence Selection for Power Grid Reliability
> Reports

Keep C2GES as the method name in the abstract/method if useful, but stop making
`Graph-Enhanced` and `Counterfactual` the title-level promise.

Expected manuscript edits:

- Title.
- Abstract first method sentence.
- Introduction contribution bullets.
- Method opening.
- Discussion/conclusion language that currently sounds like graph/counterfactual
  is a central contribution.

Validation target:

- Title no longer contains `Graph-Enhanced` or `Counterfactual`.
- Abstract still reports the role-selective graph result as a small auxiliary
  finding.
- No text claims graph or counterfactual modeling as a primary contribution.

### Priority 2: Make the method self-contained and reproducible

Add a compact reproducibility subsection or table that specifies the deterministic
scorer without requiring readers to inspect code.

Facts available from the implementation:

- Query score:
  - TF-IDF cosine similarity.
  - `stop_words="english"`, `max_features=8000`, `ngram_range=(1,2)`.
  - Min-max normalization per document/question candidate pool.
- Role score:
  - Five role cue dictionaries.
  - Cue hit score adds `1.0 + 0.15 * (phrase_length - 1)` for each matched cue.
  - Numeric engineering units add `0.8`.
  - domain abbreviations such as `SLG`, `RAS`, `IBR`, `BESS`, `PV`, `ERCOT`,
    `CAISO`, `MISO`, `NERC`, and `WECC` add `0.25`.
  - Role scores are min-max normalized per document.
- Graph matrix:
  - Sentence-pair graph uses sequential and semantic proximity.
  - Sequential term: `exp(-abs(i-j)/4.0)` when distance is at most `8`,
    otherwise `0`.
  - Semantic term: TF-IDF cosine similarity when similarity is at least `0.08`,
    otherwise `0`.
  - Edge weight: `0.45 * sequential + 0.55 * semantic`.
- Chain score:
  - Neighbor-role sets are defined by role adjacency.
  - Ordered neighbors receive weight `1.0`; reverse/cross-reference neighbors
    receive weight `0.45`.
  - Chain support is weighted neighboring-role support, then min-max normalized.
- Revised graph signal:
  - selected family: `role_gated_chain`
  - graph signal: `minmax(target_role_compatibility * chain_support)`
  - graph active only for `propagation_or_response` and `mitigation`
- Selected weights:
  - `w_q=0.52`, `w_r=0.40`, `w_g=0.08`
  - selected under document-level 5-fold protocol from seven candidate
    configurations.

Expected manuscript edits:

- Add a table or paragraph listing exact cue counts per role.
- Replace vague `alpha/beta/gamma` wording with the actual deterministic scoring
  rules, or explicitly state those symbols are a compact abstraction of the
  deterministic cue-weight scheme.
- Define `p(j,k)`, `A`, `C(s,r')`, and window/proximity thresholds in text.
- Clarify that parameters are deterministic cue weights plus 5-fold selected
  mixture weights, not learned neural parameters.

Validation target:

- Searching the revised `paper.tex` finds concrete values:
  `8000`, `(1,2)`, `0.08`, `8`, `0.45`, `0.55`, `1.0`, `0.45`, `0.8`, `0.25`.
- The method can be understood without reading code.

### Priority 3: Strengthen analysis using existing results only

Use existing `summary.json` fields to add analysis that the review asked for
without running new experiments.

Expected manuscript edits:

- Add per-role C2GES F1/precision/recall table.
- Add per-role deltas against TF-IDF and no-role, not only no-graph.
- Add one paragraph explaining practical significance:
  - impact and mitigation are strongest roles;
  - root cause and propagation/response remain harder;
  - graph helps only in structurally contextual roles.
- Clarify ROUGE-L is secondary and not the basis for the graph claim.

Validation target:

- A table reports five roles with F1, precision, recall for full C2GES.
- Text reports the largest and smallest role-level improvements using existing
  summary values.
- Graph claim remains tied to evidence F1, not ROUGE-L.

### Priority 4: Improve limitations and future-work honesty

Make the limitations directly match the strongest likely objections.

Expected manuscript edits:

- Explicitly say no expert-gold labels or inter-annotator agreement are available.
- Say stronger neural IR/reranking baselines are future work rather than silently
  absent.
- Say K sensitivity and segmentation sensitivity are not part of this scoped
  pilot and should be predeclared in a larger follow-up.
- Say BM25 is a reasonable immediate next baseline but is not included in this
  post-freeze manuscript revision unless Harness requests it.

Validation target:

- Limitations include baseline, K sensitivity, segmentation, and label-quality
  constraints.
- The paper does not imply broad SOTA performance.

## Optional Work Not Recommended For This Goal

These may improve a later version but should not be part of the immediate
optimization unless Harness explicitly requests them:

- Cross-encoder, ColBERT, SPLADE, monoT5, or learned LTR baselines.
- New expert labeling or adjudication.
- Full K/segmentation/window sensitivity sweeps.
- Learned role classifiers or logistic calibration.
- Additional graph-gate search.

Reasons:

- They increase scope and risk.
- They can weaken the current story if stronger baselines dominate C2GES.
- They require a predeclared protocol and separate Harness review.

## Proposed Execution If Approved

1. Edit only
   `post_freeze_revisions/role_selective_graph_gate/paper_revision/paper.tex`
   and local revision notes.
2. Regenerate PDF with `pdflatex -> bibtex -> pdflatex -> pdflatex`.
3. Scan revised text/PDF for:
   - title no longer over-promises graph/counterfactual;
   - exact method constants present;
   - per-role analysis present;
   - no new unverified experimental claims.
4. Leave frozen `deliverables/` unchanged.
