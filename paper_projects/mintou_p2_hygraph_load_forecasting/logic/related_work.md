# Related Work (p2 — mintou_p2_hygraph_load_forecasting)

The authoritative literature review for this paper is **Section 2 of the manuscript**
(`mintou_p2_hygraph_load_forecasting/manuscript/MANUSCRIPT.md`), organized in three threads:

1. **Deep architectures for short-term and 24-hour-ahead load forecasting** (Section 2.1)
2. **Cross-series and graph-structured load forecasting** (Section 2.2) — including the gap this paper fills: no prior work tests whether its particular cross-series weighting beats trivial equal-weight averaging under an identical protocol with seed-level significance testing
3. **Simple baselines and honest evaluation** (Section 2.3)

An extended standalone version of the review, with full citation context and the gap
statement, is at `mintou_p2_hygraph_load_forecasting/manuscript/related_work.md`.
All references are Crossref-verified (DOIs confirmed 2026-07-16); the manuscript's
reference list uses MDPI numbered style in order of first appearance.

## Target-journal comparator papers (positioning set)

Twelve recently published comparator papers from the target-journal collection
(`ara_collections/target_journal_related/papers/tj_p2_*`) informed the positioning.
The subset actually cited in the manuscript: three-channel LSTM-CNN
(10.3390/electronics14112262), GCN-BiLSTM-Adaboost (10.3390/electronics14163332),
BiLSTM-Transformer dynamic adaptive fusion (10.3390/en19061473), LSTM-XGBoost
(10.3390/en18112842), Transformer spatio-temporal GNN (10.3390/en18174466),
GCN+Transformer (10.3390/app15137003), SBOA-SVMD-TCN-BiLSTM
(10.3390/electronics13173441), and LoadSeer (10.1109/ACCESS.2024.3514174).
The remaining comparators (10.3390/electronics12163441, 10.3390/electronics13173552,
10.3390/app15052435, 10.3390/electronics15122549) are load-forecasting hybrids or
reviews without a cross-series weighting mechanism and are not cited.

The earlier auto-extracted scaffold that occupied this file was superseded by the
manuscript review on 2026-07-17.
