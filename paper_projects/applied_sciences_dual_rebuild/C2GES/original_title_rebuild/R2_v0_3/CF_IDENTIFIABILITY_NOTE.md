# v0.3 typed-path counterfactual identifiability note

## Retired v0.2 quantity

For total edge flow `F(G)=Σ_e w_e`, deleting node `i` removes exactly its incident edges. Therefore

`F(G)-F(G_-i)=Σ_{e incident to i} w_e=degree_w(i)`.

After the same min–max transform, the v0.2 counterfactual channel and graph-salience channel are identical. v0.2 is retained only as incident history.

## v0.3 quantity

Let `P(G)` be simple, stage-monotone typed paths with at least two and at most four edges, beginning at `root_cause` or `trigger_event` and ending at `impact` or `mitigation`. For path `p`, define

`strength(p) = geometric_mean({w_e : e in p}) × (max_stage(p)-min_stage(p))/4`.

The raw v0.3 counterfactual loss is

`CF_path(i) = Σ_{p in P(G): i in p} strength(p)`.

Equivalently, because deleting `i` removes exactly the qualified paths containing it,

`CF_path(i) = U(G)-U(G_-i)`, where `U(G)=Σ_{p in P(G)} strength(p)`.

This quantity depends on multi-edge path membership, ordered role stages, and products/geometric means of edge weights. Weighted degree depends only on the sum of incident edge weights. They cannot be algebraically identical in general.

## Constructive counterexample

The registered synthetic graph contains a chain `r→t→p→i`, with unit weights, and a separate unit shortcut `x→m`. Nodes `r` and `x` have the same weighted degree. `r` participates in a qualified multi-edge cause-to-impact path, whereas `x→m` is only one edge and is excluded. Hence `CF_path(r)>0` and `CF_path(x)=0` although `degree_w(r)=degree_w(x)`.

`test_counterfactual_paths.py` checks this counterexample, verifies intervention-loss equality, deterministic bounded scaling, and path-length fail-closed behavior. The test is a mathematical/software identifiability check, not evidence of physical causality or summarization benefit.

## Freeze boundary

Path limits, graph construction, scoring weights, redundancy threshold, and selection rules must be chosen from the 12 development reports only. The already viewed 16-report R1 test set cannot yield confirmatory evidence; any v0.3 reuse is a post-audit corrective evaluation and will be reported as such.

