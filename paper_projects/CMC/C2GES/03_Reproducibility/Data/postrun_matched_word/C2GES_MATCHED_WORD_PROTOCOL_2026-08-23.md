# C2GES Matched-Word-Budget Sensitivity Protocol

Status: frozen before executing the re-budgeting script on 2026-08-23. The retained test results were already visible, so this is a post-run sensitivity analysis and not a fresh confirmatory experiment.

## Frozen inputs

- Development candidate dataset SHA-256: `27CE41D37D8BA7B0BBA9D80072B3A3FAC742CEB4997E30DF0BE40CC5B2DF7F79`.
- Retained test candidate dataset SHA-256: `A9342BD75BB5E20B61C9B06FE21B1FBA260347BFDB77B0AEBBA89A423DFCD127`.
- Frozen formal top-10 prediction ledger SHA-256: `AAE2BFE0E6C426B6A69D727F24239A07DFD7DBEE8A4CE228E86625CCDCA2338F`.

No embeddings, graph scores, candidates, references, or model outputs are regenerated.

## Development-only budget rule

For each of the 12 development reports, count regex word tokens in the first five and first ten body candidates. The observed medians are 113.5 and 260.0 words. Round each median to the nearest 10 words using half-to-even Python rounding, yielding frozen budgets of 110 and 260 words. Reference summaries and test candidates are not used by this rule.

## Re-budgeting rule

- Recover each method's frozen top-10 ranking from the formal audit record. For static scorers, reconstruct rank from the stored scores and frozen position/SID tie rule; for dynamic selectors, use the stored `selection_order`; lead uses document order.
- Traverse the top-10 ranking once. Accept a sentence only if its full word count fits in the remaining budget; otherwise skip it and continue. Never truncate sentence text after selection.
- Concatenate accepted sentences in document order and score ROUGE-1/2/L with the frozen stemming policy.
- The estimand is the equal-weight mean across the 10 `report_series_id` clusters. The equal-report mean is reported as sensitivity only.
- Contrasts are full C2GES minus normalized no-counterfactual, Semantic-MMR, and TextRank at both budgets.
- Uncertainty: 10,000 deterministic series bootstrap draws; seed `20260823 + budget*100 + contrast_index`.
- Testing: exact two-sided sign flip over the 10 series means; Holm adjustment across the six contrasts.

## Interpretation boundary

This audit equalizes realized word caps only within each method's already selected top-10 pool. It does not retune scores, search beyond the frozen top 10, create an unseen test set, or convert the historical test into confirmatory evidence. If a method leaves unused capacity because no remaining top-10 sentence fits, the unused words are reported.

## Acceptance checks

- development rule reproduces 110 and 260 without reading reference summaries;
- 15 test reports, 10 series, seven methods, two budgets, and 210 result rows;
- every selected summary is at or below its word cap and no sentence is partially used;
- exact six-row contrast family with 10,000 bootstrap draws and Holm values;
- public outputs contain document IDs, sentence IDs, word counts, and metrics but no report or summary text.
