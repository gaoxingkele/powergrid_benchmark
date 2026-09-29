## Material Passport

- Origin Skill: experiment-agent
- Origin Mode: validate
- Origin Date: 2026-08-13T10:09:59.004216+00:00
- Verification Status: ANALYZED
- Version Label: p2_s3_identifiable_v1_validation_v1

# Validation Report

- **Source:** `p2_s3_identifiable_v1`
- **Overall Confidence:** CAUTION
- **Outer unit:** eight rolling origins; seeds averaged before inference
- **Fallacy coverage:** 11/11 checked

## Statistical Findings

| Contrast | Test | MAPE result | Effect interval | Confidence |
|---|---|---|---|---|
| CSA-Poincare-Shared vs TargetSelfContext-Matched | exact paired sign-flip over origins | diff=-0.0002532248, raw p=0.3281250000, Holm p=0.9843750000 | origin bootstrap [-0.0006688492, 0.0002315019] | CAUTION |
| CSA-Poincare-Shared vs UniformCrossSeries-Matched | exact paired sign-flip over origins | diff=-0.0000657529, raw p=0.3906250000, Holm p=0.9843750000 | origin bootstrap [-0.0001949117, 0.0000450800] | CAUTION |
| CSA-Poincare-Shared vs CSA-Euclidean-Shared | exact paired sign-flip over origins | diff=-0.0000094614, raw p=0.7265625000, Holm p=0.9843750000 | origin bootstrap [-0.0000723093, 0.0000549518] | CAUTION |
| CSA-Poincare-Shared vs CSA-FixedScale-Shared | exact paired sign-flip over origins | diff=0.0000409747, raw p=0.0156250000, Holm p=0.0625000000 | origin bootstrap [0.0000205581, 0.0000610251] | CAUTION |
| CSA-Poincare-Shared vs CSA-Poincare-IndependentEncoder | exact paired sign-flip over origins | diff=-0.0053941359, raw p=0.0078125000, Holm p=0.0390625000 | origin bootstrap [-0.0069457336, -0.0039147453] | CAUTION |

WAPE is retained in `paired_comparisons.csv` as the frozen secondary metric.
Its p-values are descriptive and are not inserted into the primary Holm family.
Intervals are pointwise percentile bootstrap intervals over eight origins;
they are not simultaneous intervals and do not make adjacent origin blocks independent.

## Assumptions and warnings

- Exact sign-flip inference assumes origin-level differences are exchangeable
  under the null. Quarterly blocks reduce overlap, but all origins come from
  one dataset and adjacent weather years; full independence is not established.
- The parser scanned 35043 rows,
  retained 35000, and discarded
  43 before reaching the frozen
  35,000-row cap. A 24-position lead is therefore not guaranteed to equal 24
  elapsed UTC hours at every location of a dropped row.
- Five neural seeds improve optimization coverage but are averaged within
  origin and are not treated as data replications.
- No equivalence margin was specified; null weighting-form results remain
  unresolved differences rather than equivalence.
- The independent-encoder control matches total parameters but changes hidden
  width allocation and encoder arithmetic, so it is not a clean causal test of
  parameter sharing.

## Fallacy Scan

| # | Fallacy | Severity | Check result |
|---|---|---|---|
| 1 | Simpson's paradox | NOTE | Origin-specific paired values are preserved; inference is not based only on a pooled target table. Direction counts are reported per contrast. |
| 2 | Ecological fallacy | NOTE | The outer unit is a temporal origin and no claim about individual consumers is made from country-level series. |
| 3 | Berkson's paradox | CAUTION | The six-series complete-row filter selects timestamps where all named country values are present; generalization to discarded timestamps is unsupported. |
| 4 | Collider bias | NOTE | No post-treatment covariate or model-performance collider is adjusted for in the paired analysis. |
| 5 | Base-rate neglect | NOTE | Not applicable: this is continuous-error forecasting, not classification or screening. |
| 6 | Regression to the mean | NOTE | Quarterly origins were frozen by calendar date rather than selected for extreme historical model error. |
| 7 | Survivorship bias | CAUTION | Rows missing any selected series are excluded. Exact discarded-row counts before the retained cap are reported, but performance on those timestamps is unobserved. |
| 8 | Look-elsewhere effect | NOTE | One primary metric and five contrasts were frozen; Holm correction covers that primary family. Secondary WAPE remains descriptive. |
| 9 | Garden of forking paths | CAUTION | The local configuration was frozen before execution, but the study was not externally preregistered and follows earlier fixed-split evidence. |
| 10 | Correlation is not causation | NOTE | Results concern predictive error under code-level component interventions; no physical or behavioral causal mechanism is claimed. |
| 11 | Reverse causality | NOTE | Histories precede target positions, but forecasting precedence is not used to claim a causal load mechanism. |

## Reproducibility

- **Method:** not rerun
- **Verdict:** CANNOT_VERIFY
- The completed manifest records the configuration, driver, input, environment,
  and output hashes. A separate immutable rerun is required for `VERIFIED` status.
