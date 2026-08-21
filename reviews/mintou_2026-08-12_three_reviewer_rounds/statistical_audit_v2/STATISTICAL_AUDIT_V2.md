# Statistical Audit v2

This post-freeze analysis preserves all run archives and excludes deterministic-output copies from seed-level inference.
Mean-difference intervals use 5000 bootstrap resamples with seed 20260812; they are pointwise and multiplicity-unadjusted.
P1/P2 exact sign-flip tests are paired sensitivity analyses; the frozen Mann--Whitney tests remain the prespecified primary analysis.
Paired sign balance is the fraction difference between positive and negative nonzero paired differences; it is not a Wilcoxon rank-biserial effect.

## Stochastic baseline counts

| Paper | Eligible comparisons | Significant wins | Significant losses | Positive means | Deterministic descriptive gaps | Proposed higher in deterministic gaps |
|---|---:|---:|---:|---:|---:|---:|
| P3 | 56 | 55 | 0 | 56 | 7 | 7 |
| P4 | 32 | 32 | 0 | 32 | 16 | 16 |
| P5 | 28 | 24 | 0 | 27 | 21 | 21 |
| P6 | 40 | 36 | 0 | 37 | 16 | 16 |

## Paired sensitivity

P1 contains 54 paired method--metric comparisons; P2 contains 34. Detailed estimates and Holm-adjusted paired p-values are in the CSV files.

## Interpretation boundary

A non-significant comparison is reported as unresolved, not equivalent. Deterministic rules retain point estimates but have no seed-level p-value.
