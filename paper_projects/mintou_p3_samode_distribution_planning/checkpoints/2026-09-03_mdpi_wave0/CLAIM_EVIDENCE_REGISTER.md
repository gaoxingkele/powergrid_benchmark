# P3 Claim–Evidence Register

Status vocabulary: `SUPPORTED_CURRENT`, `SUPPORTED_WITH_SCOPE`, `UNRESOLVED`, `NOT_SUPPORTED`, `FUTURE_HYPOTHESIS`.

| ID | Claim under review | Status at Wave 0 | Current evidence | Allowed wording now | Prohibited wording / next gate |
|---|---|---|---|---|---|
| P3-C01 | The existing study contains 2,940 runs over six configurations. | SUPPORTED_CURRENT | Frozen manuscript, evidence, and validation outputs | State the executed design after reconstructing its configuration manifest. | Do not imply that run count alone establishes identification or engineering validity. |
| P3-C02 | CARS-MODE improves on NSGA-II+repair by 6.06% under sampled/clipped HV. | SUPPORTED_WITH_SCOPE | Existing sampled/clipped HV analysis | Report with the exact metric/reference construction and paired uncertainty. | Do not present it as metric-independent superiority. |
| P3-C03 | The ranking is stable across valid Pareto metrics/reference definitions. | NOT_SUPPORTED | Analytic reference reverses the HV conclusion; common IGD+ ranks CARS fifth. | Make the metric/reference sensitivity a primary result. | Pre-register a primary metric/reference set before re-testing. |
| P3-C04 | Self-adaptation is the identified source of performance. | UNRESOLVED | FixedDE is nominally ahead; one `strategy_adaptive` switch jointly controls parameter and strategy adaptation. | State that current evidence cannot separate the mechanisms. | Split the code and run the four-arm 2×2 design. |
| P3-C05 | Existing candidate plans are AC feasible. | NOT_SUPPORTED | Existing AC composition check is illustrative and not an end-to-end candidate validation. | Call it an illustrative component check. | Map decisions to grid actions and post-validate final fronts across scenarios. |
| P3-C06 | The current variables represent real distribution planning actions. | UNRESOLVED | Present formulation is largely a planning proxy. | Describe proxy actions precisely. | Each action needs a network parameter change, cost, and constraint effect. |
| P3-C07 | Parameter adaptation and strategy adaptation may have distinct effects. | FUTURE_HYPOTHESIS | Existing coupled switch prevents identification. | Present as RQ1/RQ2. | Requires Fixed-Fixed, AdaptiveParam-FixedStrategy, FixedParam-AdaptiveStrategy, Full-SAMODE. |
| P3-C08 | The method is suitable for Energies as a distribution-planning study. | SUPPORTED_WITH_SCOPE | Topic-route review and existing Energies template | Frame around energy planning plus action-aligned engineering evidence. | Do not equate topic fit with likely acceptance or scientific sufficiency. |

## Writing gate

The 6.06% figure may appear only together with its sampled/clipped-HV qualifier and the metric reversal. “Self-adaptation improves” and “AC-feasible plans” are prohibited until the new gates pass.
