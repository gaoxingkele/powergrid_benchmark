# Table 4 - Model performance comparison (A week / A day)

**Source**: Table 4, §4.4 (page 16, top of page)
**Caption**: "Model performance comparison (A week/A day)."
**Screenshot**: table4.png
**Extraction type**: raw_table

Stagewise ablation error (lower is better). Best value per column in **bold**.

| Model | Week MAE | Week MAPE | Week RMSE | Day MAE | Day MAPE | Day RMSE |
|-------|----------|-----------|-----------|---------|----------|----------|
| BiLSTM | 2.65 | 5.27% | 3.41 | 1.86 | 3.12% | 2.26 |
| GCN-BiLSTM | 1.99 | 4.23% | 2.61 | 0.70 | 1.19% | 1.02 |
| GCN-BiLSTM-A | 1.93 | 3.78% | 2.57 | 0.26 | 0.41% | 0.37 |
| Proposed model | **0.34** | **0.68%** | **0.43** | **0.19** | **0.33%** | **0.26** |

Notes:
- Error decreases monotonically down every column (BiLSTM → GCN-BiLSTM → GCN-BiLSTM-A → Proposed), on
  both horizons — the core stagewise-ablation evidence for C01/C02.
- "GCN-BiLSTM-A" denotes the GCN-BiLSTM-Adaboost variant (error-only weighting, before the Bayesian
  uncertainty step).
- **Internal inconsistency**: the paper's Abstract states the proposed model's MAE/MAPE/RMSE as
  1.86 / 3.13% / 2.26 — these coincide with the *BiLSTM* "A Day" row here (1.86 / 3.12% / 2.26), not with
  the proposed model's "A Day" values (0.19 / 0.33% / 0.26). The abstract figures appear to be a
  transcription error; Table 4 is authoritative. (See constraints.md item 4.)
