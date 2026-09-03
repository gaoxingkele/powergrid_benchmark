# P3 Claim–Evidence Register

**Contract status:** `LOCKED_IDENTITY / CURRENT_EVIDENCE_BOUNDARIES`

**Locked title:** `Power Distribution Network Planning Strategy Optimization based on Self-Adaption Multi-objective Differential Evolution Algorithm`

**Locked authors:** Zhang Linyao (first), Zheng Jieyun (corresponding), Zhang Zhanghuang, Ni Shiyuan, Wu Guilian

Status vocabulary: `SUPPORTED_CURRENT`, `SUPPORTED_WITH_SCOPE`, `UNRESOLVED`, `NOT_SUPPORTED`, `FUTURE_HYPOTHESIS`.

| ID | Claim under review | Status at Wave 0 | Current evidence binding | Allowed wording now | Prohibited wording |
|---|---|---|---|---|---|
| P3-C01 | The existing study contains 2,940 runs over six configurations. | SUPPORTED_CURRENT | Frozen manuscript, exact-rerun archive, validation outputs, and the reconstructed configuration manifest. | State that 2,940 archived rows cover six distinct configurations plus one independent base-configuration seed replication; retain the stochastic-versus-deterministic provenance distinction. | Do not call the base replication a seventh configuration or imply that the run count alone establishes mechanism identification, engineering validity, or independence of deterministic repeated rows. |
| P3-C02 | CARS-MODE improves on NSGA-II+repair by 6.06% under sampled/clipped HV. | SUPPORTED_WITH_SCOPE | Existing equal-configuration sampled-bound/clipped-HV analysis and seed-block inference. | Report 6.06% only with the sampled-bound/clipped-HV construction, the NSGA-II+Repair comparator, configuration aggregation, paired uncertainty, and the metric reversal. | Do not present 6.06% as metric-independent, normalization-robust, physical, or general superiority. |
| P3-C03 | The ranking is stable across valid Pareto metrics/reference definitions. | NOT_SUPPORTED | Analytic reference reverses the NSGA-II+Repair contrast; common-reference IGD+ ranks CARS-MODE fifth. | Make metric/reference sensitivity and the observed reversal primary results. | Do not describe the ranking or superiority as stable, consistent, normalization-invariant, or robust across valid Pareto metrics/reference definitions. |
| P3-C04 | Self-adaptation is the identified source of performance. | UNRESOLVED | FixedDE is nominally ahead; one `strategy_adaptive` switch jointly controls parameter and strategy adaptation. | State that current evidence tests a combined adaptation bundle and cannot separate parameter from strategy effects. | Do not state or imply that self-adaptation, parameter adaptation, or strategy adaptation improves or causes performance. |
| P3-C05 | Existing candidate plans are AC feasible. | NOT_SUPPORTED | The archived AC composition check is illustrative, uses dependent fixed cases from selected seed-0 compositions, and is not end-to-end candidate validation. | Call it an illustrative composition-level AC diagnostic or component check and retain its dependence and coverage limits. | Do not call the optimizer outputs, candidate plans, or final fronts AC feasible, physically validated, electrically superior, or deployment-ready. |
| P3-C06 | The current variables represent real distribution planning actions. | UNRESOLVED | The present formulation is a planning portfolio proxy; the AC layer maps compositions onto separate networks. | Describe the proxy actions and the mapping boundary precisely. | Do not claim action-aligned bus/line/project decisions, monetary calibration, or direct network-parameter effects without the required action, cost, and constraint mapping. |
| P3-C07 | Parameter adaptation and strategy adaptation may have distinct effects. | FUTURE_HYPOTHESIS | The existing coupled switch prevents identification of distinct effects. | Present distinct parameter and strategy effects only as future research questions requiring the four-arm design. | Do not state or imply that distinct effects were tested, observed, separated, or identified in the current evidence. |
| P3-C08 | The method is suitable for Energies as a distribution-planning study. | SUPPORTED_WITH_SCOPE | Topic-route review, the existing Energies template, and the portfolio-proxy framing. | Describe Energies as the selected topical route while retaining the need for action-aligned engineering evidence. | Do not equate journal-topic fit or template use with likely acceptance, scientific sufficiency, engineering validation, or editorial endorsement. |

## Writing gate

The locked title is an identity constraint, not evidence that the title's broadest reading has been demonstrated. The 6.06% figure may appear only with its sampled-bound/clipped-HV qualifier, comparator and metric reversal. The phrases “self-adaptation improves” and “AC-feasible plans”, and equivalent causal or physical-validity claims, remain prohibited until their stated gates pass.
