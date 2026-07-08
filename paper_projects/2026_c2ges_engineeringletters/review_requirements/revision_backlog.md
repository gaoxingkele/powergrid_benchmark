# Revision Backlog

This backlog is derived from `source/REVISION_NOTE.md` and `source/OPTIMIZATION_PLAN.md`.

## Priority 1: Positioning

- Keep title and framing focused on causal-role-aware extractive evidence selection.
- Avoid title-level promises around graph-enhanced or counterfactual modeling.
- Keep C2GES as the method name only where it does not overstate the contribution.

## Priority 2: Reproducibility

- Make deterministic scoring rules self-contained in the manuscript.
- Ensure constants are visible: `8000`, `(1,2)`, `0.08`, `8`, `0.45`, `0.55`, `1.0`, `0.8`, `0.25`.
- Clarify that weights are deterministic cue weights plus 5-fold selected mixture weights, not learned neural parameters.

## Priority 3: Evidence-Only Analysis

- Use existing summary values only.
- Keep primary claims tied to evidence-ID precision, recall, F1, and paired evidence-F1 comparisons.
- Treat ROUGE-L as secondary.

## Priority 4: Limitations

- State that labels are agent-verified candidates, not expert gold.
- State stronger neural retrieval/reranking baselines as future work.
- Avoid broad SOTA, causal discovery, or power-system counterfactual simulation claims.
