## Material Passport

- Origin Skill: experiment-agent
- Origin Mode: validate
- Verification Status: VERIFIED
- Version Label: p5_s3_validation_v1

## Validation Report

- Source: `primary_v4` and `reproduction_v1`
- Overall Confidence: CAUTION

The final deterministic rerun completed twice. Excluding `EXECUTION.md`, whose
declared output-root path necessarily differs, all 17 corresponding
CSV/JSON/Markdown artifacts match byte-for-byte. There are no missing or extra
path-independent artifacts. Within each run, all 441 recomputed reported-HV
cells match the preserved custom-engine/deterministic values at the archived
eight-decimal precision.

Confidence remains `CAUTION` because the host cannot rerun pymoo 0.6.2 and its
`moocore` dependency under one compatible Python/CFFI ABI. The all-method
matched-cardinality comparison therefore consumes preserved pymoo 0.6.2 rows;
new front-level bound/reference recomputation is restricted to TRACE-MOEA,
NoPreferenceRanking, and deterministic rules. No alternate pymoo version is
substituted.

### Statistical findings

The new sensitivity analysis is descriptive and prespecified to emit no
p-values. It reports all nine TRACE cells and all four formulation-matched
NoPreferenceRanking controls. Deterministic decision rules have one unique
output per scenario and are not treated as replicated samples.

### Fallacy scan

- Coverage: 11/11 fallacy types checked

| Fallacy | Severity | Finding |
|---|---|---|
| Simpson's paradox | NOTE | Scenario-balanced means are accompanied by per-scenario tables; no pooled direction is asserted to hold in every scenario. |
| Ecological fallacy | NOTE | Method-scenario summaries are not used to infer candidate-, reviewer-, or utility-level effects. |
| Berkson's paradox | CAUTION | Scenario filters and the constructed candidate pool limit generalization; no unexpected correlation from the selected pool is promoted. |
| Collider bias | NOTE | The new analyses fit no adjusted regression and condition on no post-treatment covariate. |
| Base-rate neglect | CAUTION | No new diagnostic-accuracy claim is made; the existing MTEP imbalance remains an explicit limitation and was not rerun. |
| Regression to the mean | NOTE | There is no pre/post extreme-group design. |
| Survivorship bias | NOTE | All prespecified seeds/cells completed in both final runs; no failed seed is omitted. |
| Look-elsewhere effect | NOTE | All prespecified cells are reported, including adverse and near-null changes; no significance filter is applied. |
| Garden of forking paths | CAUTION | Runtime/path amendments and the numerical clipping tolerance are recorded with failed/superseded directories; results remain descriptive rather than confirmatory. |
| Correlation does not imply causation | CAUTION | One-factor algorithm changes are not described as isolated causal component effects, and public-record associations remain descriptive. |
| Reverse causality | NOTE | The new benchmark comparisons make no temporal observational claim. |

### Reproducibility

- Method: deterministic same-seed rerun in a new output directory
- Verdict: REPRODUCIBLE for the stage-local custom-engine/deterministic scope;
  CANNOT_VERIFY for new pymoo 0.6.2 front reruns because of the recorded ABI
  incompatibility
- Path-independent artifact comparison: 17/17 exact matches
- Preserved-primary metric comparison: 441/441 eight-decimal matches per run

The final evidence directory is `primary_v4`; `primary_v1` and `primary_v2` are
failed pre-result attempts, and `primary_v3` is retained only to document the
strict-floating clipping-counter amendment.
