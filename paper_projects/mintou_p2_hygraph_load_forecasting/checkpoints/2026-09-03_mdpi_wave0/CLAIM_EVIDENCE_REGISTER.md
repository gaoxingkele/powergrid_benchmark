# P4 Claim–Evidence Register

Status vocabulary: `SUPPORTED_CURRENT`, `SUPPORTED_WITH_SCOPE`, `UNRESOLVED`, `NOT_SUPPORTED`, `FUTURE_HYPOTHESIS`.

## Locked identity and method boundary

- **Title:** `Graph Convolutional Network based on Hyperbolic Space for Power Load Forecasting` (exact and unchanged).
- **Authorship and affiliation:** Zheng Jieyun, Zhang Linyao, Zhang Zhanghuang, Chen Zhuolin, Shi Ying (exact and unchanged); all authors share the Economic and Technological Research Institute of State Grid Fujian Electric Power Co., Ltd. affiliation.
- **First and corresponding author:** Zheng Jieyun; correspondence is `zjy_0701@163.com`.
- **Current-model status:** CSA-LoadNet is the existing baseline. It is neither a GCN nor an HGCN and does not by itself support the method claim in the locked title.

| ID | Claim under review | Status at Wave 0 | Current evidence | Allowed wording now | Prohibited wording / next gate |
|---|---|---|---|---|---|
| P4-C01 | The existing experiment evaluates 24-step point forecasts over eight quarterly rolling blocks and five seeds. | SUPPORTED_CURRENT | `experiments/p2_s3_identifiable_v1/config.json`; frozen outputs and manuscript | State the implemented evaluation design after leakage checks. | Do not treat time points as independent statistical replicates. |
| P4-C02 | The current model is a graph convolutional network. | NOT_SUPPORTED | Existing implementation uses dense cross-series attention rather than adjacency-based graph convolution. | Call it the existing CSA/attention baseline. | A real Euclidean GCN and HGCN must be implemented before locked-title claims. |
| P4-C03 | The current model performs hyperbolic graph message passing. | NOT_SUPPORTED | Poincaré distance is used for weighting; full hyperbolic mapping/convolution/message passing is absent. | Describe Poincaré distance weighting exactly. | Do not rename CSA-Poincaré as HGCN. |
| P4-C04 | Poincaré weighting improves matched forecasting accuracy. | UNRESOLVED | MAPE 0.03664 versus target-self 0.03689; Holm-adjusted p = 0.984. | State that the existing matched comparison did not resolve an improvement. | Requires a new orthogonal graph/geometry experiment; no “significant” wording. |
| P4-C05 | The current approach beats strong non-graph baselines. | NOT_SUPPORTED | DLinear is better in the existing exact hierarchy. | Keep DLinear as a mandatory strong baseline and disclose its advantage. | Do not compare only against persistence or weak neural baselines. |
| P4-C06 | A meaningful graph can be constructed without leakage. | FUTURE_HYPOTHESIS | No accepted graph-data mapping has been frozen. | “The frozen protocol will compare physical, hierarchical, and training-only functional graphs.” | Must pass provenance, time split, node/edge, and leakage audits before any graph-quality claim. |
| P4-C07 | A hyperbolic GCN may improve multi-node load forecasting. | FUTURE_HYPOTHESIS | No HGCN result exists. | Present as the central testable question. | Implement Euclidean GCN sanity baseline and genuine HGCN before prose claims. |
| P4-C08 | Electronics is a plausible route for the rebuilt model. | SUPPORTED_WITH_SCOPE | Target-route review and existing Electronics template | Frame around graph-learning implementation plus power-load forecasting. | Do not equate scope fit with acceptance probability. |

## Writing gate

Until the title-method gate passes, the locked title may appear in planning/front-matter metadata but the manuscript cannot describe the existing CSA model as GCN or HGCN. Negative DLinear and Poincaré comparisons remain mandatory.
