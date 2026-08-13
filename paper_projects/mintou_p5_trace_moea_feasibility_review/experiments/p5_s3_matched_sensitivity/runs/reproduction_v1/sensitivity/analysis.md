## Material Passport

- Origin Skill: experiment-agent
- Origin Mode: validate
- Verification Status: ANALYZED
- Version Label: p5_s3_formulation_preference_sensitivity_v1

## Prespecified compact sensitivity result

The registered TRACE-MOEA cell has mean analytic-bound HV 0.1054389208 at reference point 1.2. The scan changes one formulation or preference factor at a time; it is descriptive and emits no p-values.

| Cell | Factor | Mean-HV change | Percent change | Positive-seed fraction | TRACE minus no-preference MOEA |
|---|---|---:|---:|---:|---:|
| registered | reference | 0.0000000000 | 0.0000000000% | 0.0000000000 | 0.0012123349 |
| risk_max | formulation | -0.0072571382 | -6.8827887700% | 0.0333333333 | 0.0031545623 |
| quality_compliance_025 | formulation | 0.0014225210 | 1.3491422230% | 0.7333333333 | 0.0003940571 |
| quality_compliance_075 | formulation | -0.0024264090 | -2.3012460499% | 0.2000000000 | -0.0007952446 |
| preferences_k4 | preference | 0.0002622899 | 0.2487600385% | 0.5000000000 | 0.0014746248 |
| preferences_k16 | preference | -0.0001281518 | -0.1215412668% | 0.5000000000 | 0.0010841831 |
| profile_reliability | preference | -0.0004571156 | -0.4335359244% | 0.3333333333 | 0.0007552193 |
| profile_renewable | preference | 0.0010354230 | 0.9820121376% | 0.6000000000 | 0.0022477579 |
| profile_traceability | preference | 0.0004332763 | 0.4109263417% | 0.4333333333 | 0.0016456112 |

Non-positive changes relative to the registered cell: registered, risk_max, quality_compliance_075, preferences_k16, profile_reliability.
Near-null changes within 0.1% in absolute mean HV: registered.

The scan does not isolate a causal component effect and does not alter the existing negative finding that adaptive preference elitism's direct contribution is unresolved.
