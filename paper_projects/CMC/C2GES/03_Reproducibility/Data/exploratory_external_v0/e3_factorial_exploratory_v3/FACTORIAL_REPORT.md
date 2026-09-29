# C2GES exploratory component-factorial report

Status: EXPLORATORY ONLY; confirmatory claims are not allowed.  
Dataset: seven post-access report series, two complete-ranking word budgets.  
Conditions: AB-0--AB-6, RP-00/RP-10/RP-01/RP-11, and G-U/G-T.  
Execution: 182/182 item rows present; 0 failures.

## Principal controlled contrasts

- AB-5 minus AB-6: -0.007988 ROUGE-L at 110 words and -0.007179 at 260 words; both cluster intervals include zero.
- G-T minus G-U: +0.001390 at 110 words and -0.005440 at 260 words; both cluster intervals include zero.
- No reservation, path, or interaction effect survived its predeclared Holm family.

## Selection overlap and stability

- AB-5/AB-6 mean selection Jaccard: 0.2329 at 110 words and 0.4789 at 260 words.
- G-T/G-U mean selection Jaccard: 0.2207 at 110 words and 0.4388 at 260 words.
- LOSO direction reversals: 15 of 140 leave-one-series-out estimates. These are stability diagnostics, not new hypothesis tests.

## Interpretation

The path term was behaviorally active but did not improve the exploratory ROUGE-L endpoint relative to the normalized no-path condition. The factorial evidence does not isolate functional overlap with reservation because the interaction estimates are uncertain. Typed edges increased the formal edge-coverage metric in several conditions without a stable ROUGE-L benefit; edge coverage is therefore not semantic validation.

No human metrics are reported. `factorial_human_metrics.csv` records `NOT_RUN` and cannot satisfy E2.

## Generated artifacts

- `factorial_selection_jaccard.csv`
- `factorial_series_effects.csv`
- `factorial_loso.csv`
- `factorial_runtime_resources.csv`
- `factorial_human_metrics.csv`
- `factorial_interactions.json`

All files are derived from the hash-bound v3 item metrics, selections, and inference records without reading report text.
