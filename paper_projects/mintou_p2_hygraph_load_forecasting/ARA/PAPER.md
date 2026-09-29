---
title: "Cross-Series Attention Neural Forecasting for Day-Ahead Multi-Region Power Load Prediction"
tag: "mintou"
paper_id: "mintou_p2"
status: "route_a_claim_downgrade_v7"
target_journal: "Electronics"
backup_journal: "Applied Sciences"
algorithm: "CSA-LoadNet"
---

# Cross-Series Attention Neural Forecasting for Day-Ahead Multi-Region Power Load Prediction

## Algorithm Identity

- Short name: `CSA-LoadNet`
- Full name: Cross-Series Attention Load Forecasting Network
- Tag: `mintou`
- Target journal: Electronics
- Backup journal: Applied Sciences
- Naming history: the method's working name before the v7 significance verdict was `HyG-LoadFormer` (Hyperbolic Graph Load Forecasting Transformer). All evidence files, CSV columns, and the project directory name retain the historical name; they are unchanged historical evidence. The claim system was downgraded on 2026-07-14 ("Route A") after the v7 10-seed significance analysis showed the hyperbolic-geometry component is statistically inseparable from Euclidean, equal-weight, and fixed-curvature variants.

## Abstract

This ARA project studies CSA-LoadNet, a neural day-ahead multi-region load forecasting model that combines a cross-series attention aggregation module with a shared temporal encoder. Each region's forecast attends over the other regions' recent load representations, so cross-series information is pooled before the temporal head produces the 24h day-ahead prediction.

Main result (v7, 10 seeds, Mann-Whitney U + Holm): on OPSD day-ahead 24h forecasting, CSA-LoadNet significantly outperforms the strongest external neural baseline MLP (p_holm=0.0085) and significantly outperforms the TemporalOnly no-aggregation ablation (p=0.0011) — cross-series aggregation is a demonstrated, significant contributor for day-ahead country-level load forecasting. On SimBench, both horizons are statistically inseparable from MLP (1h: CSA-LoadNet mean slightly ahead; 24h: MLP mean slightly ahead, p=0.084) and are reported as such.

Honest component finding: the specific form of the aggregation weights — hyperbolic (Poincare-ball) distance, Euclidean distance, equal-weight neighbors, or fixed vs adaptive curvature — is statistically inseparable across all five dataset/horizon settings (p_holm ≈ 1). The contribution comes from aggregation itself, not from the geometry of the weighting. This negative finding is reported as a component analysis result, not hidden.

Recorded limitations: on the hierarchical Ausgrid solar-home benchmark (24h, 17-series customer/region/system hierarchy), CSA-LoadNet significantly loses to DLinear (p=0.0044); on OPSD 1h short-horizon forecasting it significantly loses to MLP. Manuscript claims are therefore restricted to day-ahead 24h multi-region (country-level pool) forecasting.

Implementation note: the released implementation retains the Poincare-ball embedding as one available parameterization of the attention weights, but the paper no longer claims hyperbolic geometry as a contribution.

## Current Engineering Status

Evidence chain v5 (ridge implementation lost to all neural baselines) → v6 (neural reimplementation, external competitiveness restored at 3 seeds) → v7 (10 seeds + Ausgrid hierarchical benchmark + Mann-Whitney/Holm significance) is fully preserved and reproducible. Key v7 evidence: `evidence/runs/real_p2_v7_significance_analysis.md`, `evidence/tables/real_p2_v7_significance.csv`.

Claim boundary: the only significance-backed superiority claim is OPSD 24h day-ahead vs MLP and vs the no-aggregation ablation. 1h horizons, SimBench separability, and hierarchical (Ausgrid-type) settings are non-claims or recorded limitations.
