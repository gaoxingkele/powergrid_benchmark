# Wave-1 Changelog — TRACE-MOEA (mintou_p5) pre-submission fixes

Scope: cheap, non-experimental items from `ROUND_REVIEW.md` (Round-5, verdict
Major Revision). Date: 2026-07-17. Experimental gaps (second pool, load-flow,
hyperparameter scans) are intentionally out of scope for this wave.

## P0 — blocking items

| Item | Status | Notes |
|---|---|---|
| P0.1 Replace all [TODO] markers | **Partially done** | Ref [28] filled with the companion manuscript's actual title ("BiLo-NSGA: Bidirectional Local Search Within Non-Dominated Sorting for Budget-Constrained Power Grid Project Portfolio Review", marked companion paper, submitted). Author Contributions, Funding, affiliations, correspondence email, and repository URL remain [TODO] — **skipped: needs-author-info**. |
| P0.2 Generative AI use statement | **Done** | Added a "Generative AI Statement" section before Conflicts of Interest, copying the format already present in the BiLo-NSGA companion manuscript. |
| P0.3 Figures are placeholders | **Stale finding — no action needed** | The review's claim is outdated. Real 300 dpi PNGs exist at `manuscript/figures/` (fig_hv_boxplot.png, fig_ablation.png, fig_external_validity.png, rendered 2026-07-16 17:53 by `figures/make_figures.py`, 136–215 KB each). Header comment and Pre-Submission Checklist updated to record this. Remaining sub-task: confirm readability inside the MDPI template (formatting stage). |
| P0.4 iThenticate/CrossCheck self-check | **Skipped: needs-external-account** | Requires an iThenticate subscription; cannot be run from this environment. Kept in checklist. |
| P0.5 Publish 0.75x budget-scan evidence | **Done (re-run, exact reproduction)** | No prior 0.75x output existed anywhere in the repo (the `budget_sensitivity` experiment was implemented in `src/powergrid_benchmark/mintou_real_project_review.py` but only wired into the p6 experiment list; it was never persisted for p5). Because seeding is deterministic (SHA-1 of paper/experiment/method), the scan was re-run with the existing pipeline (Python 3.12 + pymoo 0.6.2, 15 methods x 30 seeds, ~3 min) and reproduces the manuscript numbers exactly: TRACE-MOEA 0.16605998 vs. NSGA-II 0.16378155, +1.39%. Published: `evidence/tables/real_budget_sensitivity_075x.csv` (leaderboard), `evidence/tables/real_budget_sensitivity_075x_significance.csv` (Holm-corrected comparisons), `evidence/runs/real_budget_sensitivity_075x_results.csv` (450 per-run records). No manuscript number changed. |

## P1 — major-revision items

| Item | Status | Notes |
|---|---|---|
| P1.1 Extended sensitivity analysis (K/cadence scan, weight perturbation, pool scaling) | **Skipped: needs-experiment** | The 0.75x budget dimension is now fully evidenced (P0.5); the remaining sub-scans require new experiment design and runs. |
| P1.2 Second independent benchmark pool | **Skipped: needs-experiment** | Largest remaining risk per the review; requires building a NREL-118/TAMU pool. |
| P1.3 Naming/evidence asymmetry (wording only) | **Done** | Added explicit auxiliary-role statements without renaming the method: (a) Introduction, new paragraph after the contribution list ("auxiliary role — its isolated pooled contribution is +0.17% ... gains derive mainly from the deterministic budget repair operator and the decision trace archive"); (b) Conclusions, expanded the architectural-findings sentence with the same attribution. Abstract also now says "the main gains come from budget repair and the trace archive". |
| P1.4 Load-flow (pandapower) verification | **Skipped: needs-experiment** | Requires AC power-flow runs on recommended portfolios. |

## P2 — minor items

| Item | Status | Notes |
|---|---|---|
| P2.1 Abstract ≤220 words | **Done** | Compressed from ~250 to 218 words; all quantitative claims preserved verbatim. |
| P2.2 Practical implications for utilities | **Done** | Added to the new Introduction paragraph (fundability by construction, sub-second runtimes/seed-ensembling, per-project contestability record). Discussion already carried the "Operational reading for planning departments" passage. |
| P2.3 Companion-reference consistency | **Done** | All five "[sibling]" citation markers replaced with "[28]"; "companion paper" unified to "companion study" wording; Section 2.4 heading already used "Companion Study". |
| P2.4 ORCID identifiers | **Skipped: needs-author-info** | |
| P2.5 MDPI template formatting | **Skipped: needs-author-info** (formatting stage; manuscript is still Markdown source) | |
| P2.6 Deprecated-versions explanation | **Done** | Added closing paragraph to Section 8 (Limitations): deprecated revisions are retained for transparency as part of the reproducibility record; readers must treat them as historical artifacts; no reported number derives from them. |
| P2.7 Compact 0.75x margin-pattern table | **Done** | New Table 6 in Section 6.4: margins at 1.00x (+1.26%, Holm p 0.064), 0.88x (+1.09%, p 0.053), 0.75x (+1.39%, p 0.145), full pool, balanced weights, 30 seeds each; text notes the margin is largest at the tightest envelope while no single level is Holm-significant at n = 30. Section 6.4 also now cites the three published evidence files. |

## Additional deliverables

- `manuscript/cover_letter_notes.md` — companion-submission strategy note for
  the editor (p5 vs. p6 differentiation; 0.75x budget reversal as evidence of
  distinct mechanisms: TRACE-MOEA +1.39% grows under tightening via repair,
  BiLo-NSGA -0.33% n.s. shrinks because forward insertion needs slack).
- Data Availability statement updated to include the 450-run 0.75x scan in the
  released-artifacts list.
- Pre-Submission Checklist updated (4 items now checked off).

## 0.75x evidence trail — finding of record

The Round-5 review correctly flagged that Section 6.4's 0.75x numbers had no
independent evidence file. Investigation confirmed no raw output existed in
`evidence/runs/`, `evidence/tables/`, or anywhere else in the repository. The
numbers were reproduced exactly (to the 5 decimals quoted in the manuscript)
by re-running the deterministic pipeline, which both validates the manuscript's
claims and closes the evidence gap. Note for the response letter: the
TRACE-MOEA vs. NSGA-II comparison at 0.75x is not Holm-significant in
isolation (p_holm = 0.145, raw p = 0.048, n = 30); the manuscript never claimed
per-level significance, and Table 6 now reports these p-values explicitly.
