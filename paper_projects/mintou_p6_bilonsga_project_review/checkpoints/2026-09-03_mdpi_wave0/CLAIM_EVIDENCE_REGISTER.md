# P2 Claim–Evidence Register

Status vocabulary: `SUPPORTED_CURRENT`, `SUPPORTED_WITH_SCOPE`, `UNRESOLVED`, `NOT_SUPPORTED`, `FUTURE_HYPOTHESIS`.

| ID | Claim under review | Status at Wave 0 | Current evidence | Allowed wording now | Prohibited wording / next gate |
|---|---|---|---|---|---|
| P2-C01 | The frozen benchmark uses 120 candidates, eight scenarios, 30 common seeds, and exactly 3,200 evaluations per run. | SUPPORTED_CURRENT | `experiments/p6_s3_matched_effort/config.json`; frozen outputs | State the implemented design and audit equality. | Do not imply that equal configured budgets guarantee equal unique evaluations without checking caches/duplicates. |
| P2-C02 | Pooled HV is 0.16277 for BiLo-NSGA, 0.17213 for NSGA-II, and 0.11626 for PLS. | SUPPORTED_WITH_SCOPE | `p6_s3_matched_effort` result summaries and manuscript | Report as frozen results for the existing proxy task only. | Do not select only the PLS contrast or call BiLo generally superior. |
| P2-C03 | BiLo outperforms NSGA-II. | NOT_SUPPORTED | Four principal BiLo–NSGA-II contrasts contain no BiLo win and four losses. | State that the current benchmark does not support superiority over NSGA-II. | A new independent task family cannot erase this result; it must remain disclosed. |
| P2-C04 | The complete bidirectional mechanism is responsible for improvement. | UNRESOLVED | `(2,2)` is 4.29% above `(8,4)`, while NoBackward and LegacyDeletion have higher means. | Describe the conflicting diagnostic evidence. | Requires frozen NDS-only/forward-only/backward-only/bidirectional orthogonal ablation. |
| P2-C05 | Atomic delete–add substitution is implemented. | NOT_SUPPORTED | Current behavior is not established as one atomic evaluated move. | Use forward and backward local search terminology only where code supports it. | Implement and test atomic substitution before using that term. |
| P2-C06 | The method improves real investment effectiveness. | NOT_SUPPORTED | Existing benefits/costs are proxy-based; no physical/external validation. | Call results proxy portfolio quality/effectiveness screening. | Needs traceable costs plus a physical or external validation layer. |
| P2-C07 | A normal power-grid investment framing fits the active route. | SUPPORTED_WITH_SCOPE | Existing problem semantics and Applied Sciences route review | Develop power-grid action/cost evidence without security relabeling. | Do not claim journal acceptance; venue fit is conditional on completed science. |
| P2-C08 | Bidirectional local search will be valuable on a second task family. | FUTURE_HYPOTHESIS | No result yet. | “We test whether...” only. | Build an independently generated, action-aligned task family and matched experiment. |

## Writing gate

The negative NSGA-II comparison and unresolved mechanism attribution are mandatory facts. They cannot be removed by changing the target journal, dataset, metric, or narrative.
