# R3 Statistical Interpretation Patch

## Manuscript-ready Methods text

The registered analysis used 10,000 report-level paired bootstrap resamples to obtain percentile intervals for each Full-minus-comparator mean ROUGE-L difference. The frozen runner also recorded twice the smaller empirical fraction of bootstrap-resampled mean differences at or below and at or above zero, followed by the registered six-item Holm transformation. We retain those machine values for provenance and call them **registered bootstrap sign-tail summaries**. Because the bootstrap samples were drawn from the observed empirical distribution and were not recentered or otherwise generated under a null distribution, these summaries are not null-calibrated hypothesis-test p-values. Applying Holm to them preserves the registered multiplicity calculation but does not convert them into p-values. The registered percentile intervals remain the primary uncertainty summaries.

After results were unblinded, we added an unregistered sensitivity analysis without regenerating predictions. For each of the same six report-paired contrasts, it enumerated all $2^{15}=32{,}768$ sign assignments and evaluated the absolute mean difference. The two-sided probability was the fraction of assignments with an absolute statistic at least as large as observed; Holm adjustment covered all six values. Its randomization interpretation assumes joint sign symmetry/exchangeability of paired report-level differences under each sharp null. This assumption is explicit but cannot be established from 15 reports, so the exact analysis is robustness evidence rather than a replacement confirmatory analysis.

## Manuscript-ready Results text

The immutable 210-row prediction ledger produced the same qualitative pattern under the unregistered exact sign-flip sensitivity. For Full minus strict no-CF, exact two-sided values were 0.4368 at $K=5$ and 0.2007 at $K=10$ (six-item Holm values 0.4368 and 0.4014), with report directions 7/7/1 and 6/8/1 (positive/negative/tie). For Full minus Semantic-MMR, the exact values were 0.000305 and 0.006592 (Holm 0.001526 and 0.026367), with directions 14/1/0 and 11/4/0. For Full minus TextRank, they were 0.000122 and 0.009644 (Holm 0.000732 and 0.028931), with directions 14/1/0 and 13/2/0. These post-run values are conditional on the sign-symmetry assumption and do not alter the registered estimates or percentile intervals.

## Replacement Table 3 terminology

- Replace `Holm p` for registered outputs with `registered Holm-transformed bootstrap sign-tail`.
- State in the caption that this registered column is descriptive and not a null-calibrated p-value.
- Put exact sign-flip values in a separate column or supplementary table headed `unregistered exact sign-flip sensitivity (Holm over 6)`.
- Keep all registered means, intervals, and machine sign-tail values byte-for-value unchanged.

## Evidence binding

- Immutable input: `predictions.jsonl`, SHA-256 `AAE2BFE0E6C426B6A69D727F24239A07DFD7DBEE8A4CE228E86625CCDCA2338F`.
- Machine outputs: `original_title_rebuild/R2_v0_3/postrun_sensitivity/artifacts/`.
- Independent product-enumeration verification: `original_title_rebuild/R2_v0_3/postrun_sensitivity/INDEPENDENT_MECHANICAL_VERIFY.json` (`PASS`).
- Status: unregistered post-run sensitivity; zero generation calls; no formal test rerun; no test-set model selection.
