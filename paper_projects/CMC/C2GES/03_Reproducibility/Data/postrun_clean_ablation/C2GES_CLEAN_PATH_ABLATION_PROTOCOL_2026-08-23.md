# C2GES Clean Normalized Path-Ablation Protocol

Status: frozen before executing the audit on 2026-08-23. This is a post-run component diagnostic on the retained corpus.

## Problem addressed

The historical `graph_no_cf_strict` diagnostic sets the path-deletion weight from 0.15 to zero but leaves all other positive coefficients and the 0.50 redundancy penalty unchanged. Positive weights therefore sum to 0.85 and the effective redundancy strength relative to the positive scale increases by 17.6%. That contrast is not a scale-preserving information ablation.

## Frozen inputs

- Retained test candidates SHA-256: `A9342BD75BB5E20B61C9B06FE21B1FBA260347BFDB77B0AEBBA89A423DFCD127`.
- Formal prediction/audit ledger SHA-256: `AAE2BFE0E6C426B6A69D727F24239A07DFD7DBEE8A4CE228E86625CCDCA2338F`.
- Original full positive weights: relevance 0.40, role 0.20, graph 0.15, path-deletion 0.15, position 0.10; redundancy penalty 0.50.

## Clean normalized variant

- Set path-deletion weight to zero.
- Divide each remaining positive coefficient by 0.85, yielding relevance 0.4705882353, role 0.2352941176, graph 0.1764705882, and position 0.1176470588.
- Keep redundancy penalty at 0.50, the same ratio to the now unit-sum positive score as in Full.
- Preserve candidates, lexical roles, graph, role-group reservation, Jaccard redundancy, K=5/10, tie rules, source-order restoration, and ROUGE scoring.

Because the frozen strict audit stores every candidate's no-path base score, the clean base score is exactly `strict_base / 0.85`; path values and reference outcomes are not needed to construct it.

## Verification and endpoints

1. Rebuild lexical roles and redundancy from the frozen candidates.
2. Using stored full and strict base scores, reproduce every archived Full and strict selection at both budgets before accepting the new result.
3. Report clean-versus-Full and clean-versus-historical-strict selection overlap, ROUGE, and redundancy.
4. For Full minus clean normalized, report equal-series mean ROUGE-L, 10,000-draw series bootstrap, exact 1024-assignment series sign flip, and Holm adjustment across K=5/10.

Outputs contain IDs, scores, and metrics but no report, candidate, reference, or prediction text. The analysis is post-run and cannot establish a confirmatory component effect.
