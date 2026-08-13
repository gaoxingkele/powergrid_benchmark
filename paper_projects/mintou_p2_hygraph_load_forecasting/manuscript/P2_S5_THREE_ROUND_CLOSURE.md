# P2 S5 Three-Round Scientific Closure

This internal record documents three sequential, evidence-bound adversarial passes over `MANUSCRIPT.md`, `DEEP_REVISION_EVIDENCE.md`, the frozen rolling-origin configuration and driver, `run_manifest.json`, `model_audit.csv`, `run_results.csv`, `origin_metrics.csv`, `paired_comparisons.csv`, the historical fixed-split and exact-hierarchy tables, and the deterministic artifact generator. It is not a human peer-review report, an external expert judgment, or an independent experiment rerun.

## Pass 1: Logic and Claim Chain

### Major findings resolved

1. **Temporal-replication overstatement.** Eight quarterly blocks from one six-country record are not eight independent weather-year or system replications. “Temporally replicated” was replaced by “multi-origin” or “multiple temporal blocks.” The manuscript now states that the 672-position test blocks are disjoint while their training histories are nested within the same record.
2. **Combined-ablation authority.** The fixed-split TemporalOnly switch also changes the prediction head and capacity, so it cannot independently isolate aggregation. The matched target-self contrast now has sole authority for the aggregation-existence question. Uniform, Euclidean, and fixed-scale controls jointly support only the family-level conclusion that no tested learned-weight advantage is established; they do not identify a best mechanism or license equivalence.
3. **Unsupported human assertions.** Existing author metadata is explicitly marked for author verification. Unverified claims that every author approved the manuscript, verified all analyses, accepted responsibility, or declared no conflicts were replaced with `AUTHOR INPUT REQUIRED` blockers.

### Strongest counterargument retained

The most parsimonious reading is that the fixed-split positive result is split- and comparator-selection-sensitive rather than evidence that cross-series aggregation helps. The matched target-self contrast is unresolved, fixed scale is nominally better, the independent-encoder comparison is confounded, and DLinear remains more accurate on the exact hierarchy. No revision turns those results into a positive aggregation, geometry, sharing, or deployment claim.

## Pass 2: Methodology and Statistics

### Major findings resolved

1. **Temporal-unit definitions.** A processed position, forecast origin, rolling-origin block, and outer analysis unit are now distinct. Each quarterly block contains 672 forecast origins; seeds are averaged within block, and the eight block differences enter inference. Targets, countries, dates, and seeds are not promoted to independent temporal units.
2. **Elapsed-time boundary.** Table 3 now reports a 168-processed-position lookback rather than 168 h. OPSD and SimBench short-horizon language is expressed as lead positions where filtering or retained-row aggregation prevents a guaranteed elapsed-hour interpretation.
3. **Data-audit scope.** The OPSD parser scanned 35,043 rows, discarded 43 incomplete selected-country rows, and retained 35,000. Filtering precedes every split. The audit output retains date-aggregated forecast targets, not the discarded timestamps, and no missingness-sensitivity result is available. SimBench timezone/discard sensitivity and full-record Ausgrid leaf selection remain explicit limitations.
4. **Baseline fairness.** The manuscript and evidence matrix now distinguish exact matching for the target-self comparison, controlled weight-form changes, parameter-only matching with compute/width confounding for the independent encoder, and unmatched capacity/epoch/stride budgets for historical external baselines. “Matched” no longer implies universal compute or wall-clock equality.
5. **Inferential assumptions.** The exact sign-flip interpretation is explicitly conditional on sign-exchangeability of the eight block differences under the no-effect null. Bootstrap intervals resample the same eight blocks and are descriptive uncertainty summaries; they do not establish independent weather-year replication.

### Deterministic arithmetic checks retained

- The nine manifest-listed outputs were checked; every CSV matched its recorded raw-byte hash. The two Markdown report hashes matched after the artifact generator’s declared CRLF-to-LF checkout normalization.
- The 6 methods × 8 blocks × 5 seeds factorial remains 240 rows, with 48 seed-averaged block rows.
- Recalculation from `origin_metrics.csv` reproduced all five raw exact MAPE sign-flip p-values and their Holm adjustments: target-self 0.328125/0.984375, uniform 0.390625/0.984375, Euclidean 0.7265625/0.984375, fixed scale 0.015625/0.0625, and independent encoder 0.0078125/0.0390625.
- The central proposed-minus-target-self MAPE difference remains -0.0002532248; its interval still crosses zero. The primary claim remains unresolved.
- WAPE remains secondary and unadjusted. No equivalence margin exists.

## Pass 3: Theory and Innovation

### Major findings resolved

1. **Executable switch versus causal isolation.** Component switches are now described as interventions that probe sensitivity, not automatic causal isolators. Context content and weight form have matched controls; parameter sharing does not.
2. **Term definitions.** “Matched,” “not separable,” “combined ablation,” “exact hierarchy,” and “coherence” now have explicit operational meanings and excluded interpretations. In particular, non-separation is not equivalence, and exact coherence is not forecast accuracy or physical-network feasibility.
3. **Innovation boundary.** The independent scientific contribution is the matched-control rolling-origin evaluation and the resulting claim correction. Standard metrics, neural layers, Poincaré distance, Adam, sign-flip inference, Holm correction, and reconciliation are not claimed as original. The paper does not claim a new forecasting theory, a state-of-the-art architecture, a causal benefit of learned geometry, or general forecasting superiority.

## External Checks and Verification Status

- **UNVERIFIED:** content-level audit of every cited source and full claim-to-source alignment.
- **UNVERIFIED:** systematic or exhaustive novelty searching.
- **UNVERIFIED:** external domain-expert review or any expert label.
- **UNVERIFIED:** similarity/plagiarism screening, including self-overlap.
- **UNVERIFIED:** independent immutable rerun of `p2_s3_identifiable_v1`; the run remains `UNVERIFIED` despite internal hash and arithmetic checks.
- **UNVERIFIED:** persistent public archive URL or DOI for the evidence package.
- **ENVIRONMENT-BLOCKED:** fresh deterministic quantitative-figure regeneration. The only available Python 3.14 interpreter has an incompatible Pillow `_imaging` extension. The retained P2 S4 figures and tables match all checkout-normalized hashes in their artifact manifest, and their scientific inputs did not change in S5, but no S5 rebuild is claimed.
- **ENVIRONMENT-BLOCKED:** fresh official PDF compilation. The journal conversion helper can refresh generated Markdown/TeX, but no usable `pdflatex` executable was available in the inspected environment. Existing PDFs must remain marked stale until a fresh build succeeds.

The full scientific-evidence acceptance command passes in this worktree. Direct structural, hygiene, generated-source, artifact-hash, row-cardinality, and retained-PDF parser checks also pass. The official journal acceptance command was run with human placeholders allowed and stops at the unavailable `pdflatex` executable; therefore current-manuscript PDF integrity and the overall journal acceptance remain unverified rather than passed.

No unavailable check is treated as passed, and no external reviewer, expert, deployment, or replication status is inferred.

## Remaining Scientific Limitations

- The eight blocks share one 2017--2018 record and nested training histories.
- A lead of 24 processed positions is not guaranteed to equal 24 elapsed UTC hours around dropped source rows.
- The accepted rolling-origin family covers OPSD lead 24 and six component arms only; it excludes MLP, LSTM, TCN, DLinear, PatchTST-lite, lead 1, SimBench, and Ausgrid.
- The independent encoder is parameter-matched but not width- or compute-matched.
- Historical external baselines have unequal capacity and epoch budgets; Ausgrid also has unequal training stride/exposure.
- Full-record Ausgrid leaf selection, missingness sensitivity, weather covariates, holidays, localized civil time, probabilistic forecasts, dispatch effects, and deployment remain untested.

## Unresolved Human Blockers

- **AUTHOR INPUT REQUIRED:** verify author spelling/order, affiliation, correspondence details, and rendered non-Latin names.
- **AUTHOR INPUT REQUIRED:** assign and approve CRediT roles.
- **AUTHOR INPUT REQUIRED:** provide verified funding/grant/APC information or an author-confirmed no-funding statement.
- **AUTHOR INPUT REQUIRED:** approve acknowledgments, conflicts of interest, generative-AI disclosure, data-availability wording, and responsibility language.
- **AUTHOR INPUT REQUIRED:** deposit and verify a persistent public archive before adding a repository URL or DOI.
- **AUTHOR INPUT REQUIRED:** approve the final manuscript and regenerated submission artifacts.
