# P1 Claim–Evidence Register

Status vocabulary: `SUPPORTED_CURRENT`, `SUPPORTED_WITH_SCOPE`, `UNRESOLVED`, `NOT_SUPPORTED`, `FUTURE_HYPOTHESIS`.

| ID | Claim under review | Status at Wave 0 | Current evidence | Allowed wording now | Prohibited wording / next gate |
|---|---|---|---|---|---|
| P1-C01 | The current benchmark contains 120 project proxies, seven scenarios, and 30 paired seeds. | SUPPORTED_CURRENT | `experiments/p5_s3_matched_sensitivity/config.json`; frozen outputs and manuscript | Describe the experimental design exactly as implemented. | Do not call the proxies audited real investment projects. |
| P1-C02 | TRACE-MOEA has pooled HV 0.17425 and is about 0.89% above NSGA-II in the frozen proxy analysis. | SUPPORTED_WITH_SCOPE | `experiments/p5_s3_matched_sensitivity`; manuscript result tables | Report as a small pooled proxy-benchmark difference with its paired uncertainty and correction. | Do not generalize to all metrics, grids, or real investment effectiveness. |
| P1-C03 | Preference adaptation independently improves performance. | UNRESOLVED | Preference-removal difference is about 0.17% and is unresolved after correction. | State that the independent contribution was not resolved in the existing experiment. | A new isolated ablation is required before any positive causal wording. |
| P1-C04 | The ranking is robust to normalization and reference choices. | NOT_SUPPORTED | Existing sensitivity analysis shows ordering can change with normalization. | Disclose metric/normalization sensitivity. | Freeze primary normalization/reference rules before re-testing. |
| P1-C05 | The method improves real investment return or engineering reliability. | NOT_SUPPORTED | Current objectives are proxy scores; no audited real cost, AC/OPF, N-1, or external decision validation. | Call the current role pre-decision proxy screening. | Needs traceable cost plus physical or external validation. |
| P1-C06 | Event summaries provide full lineage, causal explanation, or replay. | NOT_SUPPORTED | Existing records support counts/co-occurrence only. | Describe bounded run-event summaries. | Do not use full-lineage, causal, or replayable audit claims. |
| P1-C07 | A hybrid of NDS, deterministic repair, and preference-guided retention is the method examined. | SUPPORTED_WITH_SCOPE | Existing method/code and manuscript description | Define each component operationally and test it separately. | “Hybrid is superior” remains a future hypothesis until matched ablations pass. |
| P1-C08 | Cost/AC/external validation will preserve the proxy-front ranking. | FUTURE_HYPOTHESIS | No result yet. | “We evaluate whether...” only. | Run the Wave 1 validation before stating an outcome. |

## Writing gate

Abstract, contribution list, results, discussion, and conclusion must use the same status. A claim can be upgraded only after its configuration, raw outputs, aggregation code, statistical result, and manuscript location are registered.
