## Material Passport

- Origin Skill: experiment-agent
- Origin Mode: validate
- Origin Date: 2026-08-13
- Verification Status: VERIFIED
- Version Label: validation_v1

## Validation Report

- **Source**: P3 2940-row planning archive plus archived AC common panel
- **Overall Confidence**: CAUTION

### Statistical Findings

| Metric | Test | Value | Effect Size | Confidence |
|---|---|---|---|---|
| legacy HV reproducibility | deterministic eight-decimal comparison | exact=True; max diff=0 | exact archive-scale match | SOLID |
| analytic HV r=1.10 | Mann--Whitney U; Holm within experiment | see `hv_diagnostics/inference.csv` | mean differences retained | CAUTION |
| analytic HV r=1.05 | Mann--Whitney U; Holm within experiment | see `hv_diagnostics/inference.csv` | mean differences retained | CAUTION |
| common-reference IGD+ | Mann--Whitney U; Holm within experiment | see `hv_diagnostics/inference.csv` | mean differences retained | CAUTION |

### Warnings

- The sampled-bound legacy metric clips 2281 below-zero coordinates (and no above-one coordinates); analytic-bound results are the robustness check.
- Pooled means/ranks combine seven problem variants and are descriptive.
- The empirical IGD+ reference is constructed from the compared methods and seeds.
- AC rows are dependent fixed-case evaluations of three run-index-0 compositions; no hierarchical seed uncertainty is available.

### Fallacy Scan

- **Coverage**: 11/11 fallacy types checked

| Fallacy | Severity | Detail | Disposition |
|---|---|---|---|
| Simpson's paradox | NOTE | Experiment-level results are retained; pooled rank is labeled descriptive. | Do not replace experiment-level contrasts with pooled direction. |
| Ecological fallacy | CAUTION | AC cases are nested within three compositions; case counts are not optimizer replications. | AC claims remain composition-level and illustrative. |
| Berkson's paradox | NOTE | No filtered clinical/admission sample; optimizer fronts are feasibility-filtered by the declared budget. | Scope is explicit. |
| Collider bias | NOTE | No causal adjustment model is fitted. | Not applicable to the ranking analysis. |
| Base-rate neglect | NOTE | AC feasibility is paired with the common No-Plan panel rather than sensitivity/specificity. | No diagnostic-classification claim. |
| Regression to the mean | NOTE | No extreme-group pre/post selection is used. | Not detected. |
| Survivorship bias | CAUTION | Hypervolume uses feasible returned fronts by definition; empty fronts retain score zero. | Feasibility filtering and zero handling are explicit. |
| Look-elsewhere effect | CAUTION | Twelve stochastic opponents are tested per experiment for each robustness metric. | Holm correction is applied within each metric/experiment; metrics are robustness analyses. |
| Garden of forking paths | CAUTION | Analytic envelopes and ref=1.05 were fixed by equation bounds and a predeclared closer reference, not selected from favorable results. | Preserve all generated variants and negative/null findings. |
| Correlation != causation | CAUTION | Optimizer comparisons do not establish engineering deployment effects. | Claims remain proxy-optimizer claims. |
| Reverse causality | NOTE | No directional observational causal model is used. | Not detected. |

### Reproducibility

- **Method**: deterministic seed/source rerun with preserved fronts
- **Verdict**: REPRODUCIBLE

The archived scalar HV column is compared at its stored eight-decimal precision. New analytic-bound and common-reference metrics have no prior archived target and are verified by deterministic recomputation plus runtime self-tests, not by claiming a second independent implementation.
