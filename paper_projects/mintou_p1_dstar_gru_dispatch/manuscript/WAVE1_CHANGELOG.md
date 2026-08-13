# Wave-1 Pre-Submission Changelog (from ROUND_REVIEW.md, Round-4 Final)

Date: 2026-07-17. Scope: apply the Round-4 final review's P0/P1/P2 modification list to
`MANUSCRIPT.md` and associated repo files, under three hard constraints: (1) no `[TODO:...]`
author/funding/repository markers touched (author info pending), (2) no new experiments and no
modification of evidence CSV/results files, (3) no experimental numbers altered (all verified
against evidence CSVs by the review itself).

Note on numbering: ROUND_REVIEW.md contains two "Concrete Modification List" tables with shifted
P0 numbering. This changelog uses the second (final) list's numbering and notes the alias from
the first list where they differ.

## P0 — Must fix before submission

| Item | Status | Change |
|---|---|---|
| P0-1 Resolve all [TODO] markers (authors, ORCIDs, affiliations, email, repo URL/DOI, funding) | **SKIPPED — needs-author-info** | All `[TODO]` markers left exactly as-is per instruction; author metadata pending from the user. Locations: title block (authors/affiliations/corresponding email), Data Availability (repository URL/DOI), COI (funding statement). |
| P0-2 Verify figures exist in `manuscript/figures/` at 300 dpi | **DONE (verified, no change needed)** | Confirmed `fig_benchmark_overview.png`, `fig_leaderboard.png`, `fig_scale_dependency.png` all present in `mintou_p1_dstar_gru_dispatch/manuscript/figures/` alongside `make_figures.py`, `series_stats.json`, `cap_sensitivity.json`. Review had already marked this RESOLVED. |
| P0-3 Add AI use disclosure (alias: P0-2 in first list) | **DONE** | Added a "Use of Generative AI" section immediately after Conflicts of Interest: generative AI assistant (Claude, Anthropic) used for drafting/editing assistance; all experimental design, code, results, and analysis produced and verified by the authors; authors reviewed/edited AI-assisted content and take full responsibility. Wording follows the IEEE-recommended template quoted in the review. |
| P0-4 Make OPF scope explicit (alias: P0-3 in first list) | **DONE** | Limitation 1 upgraded with the review's exact substance: "This benchmark evaluates curtailment-risk forecasting, not dispatch feasibility"; the SNSP-type reference policy named an "acceptance-rule proxy"; "no AC-OPF, unit-commitment, or AC-feasibility claim attaches to anything in this paper." |
| P0-4 (first list) Clean up stale `evidence/figures/README.md` | **DONE** | Rewrote `papers/mintou/mintou_p1_dstar_gru_dispatch/evidence/figures/README.md` (the only existing copy of that path): it now points to `manuscript/figures/` and its three PNGs + regeneration script, and explains that the old "after synthetic smoke tests" text referred to the deprecated v3 pipeline. |

## P1 — Strongly recommended

| Item | Status | Change |
|---|---|---|
| P1-1 Report blend-weight (alpha) distribution per horizon/seed | **SKIPPED — needs-experiment** | The selected alpha values are not logged in the existing evidence (`real_curtailment_results.csv` has no alpha column; verified). Producing them requires re-running the pipeline, which is prohibited in this wave. |
| P1-2 NREL-118 replication or strengthened caveat | **DONE (option b — caveat)** | NREL-118 run would be a new experiment (prohibited). Limitation 2 retitled "Single test system, single weather year" and upgraded to the review's requested language: "No generalization to other systems or to other weather years is claimed or implied," with NREL-118 named as the natural second substrate. |
| P1-3 Replace `logic/related_work.md` auto-scaffold | **DONE** | The 12-entry auto-extracted dispatch/UC comparator scaffold existed in two copies: `mintou_p1_dstar_gru_dispatch/logic/related_work.md` and `papers/mintou/mintou_p1_dstar_gru_dispatch/logic/related_work.md`. Both replaced with a pointer file directing to manuscript Section II and to the Crossref-verified bibliography notes in `manuscript/related_work.md`. |
| P1-4 Cap-sensitivity for method rankings (run 0.60/0.80 or roadmap) | **DONE (roadmap option)** | Full-suite reruns at other caps would be new experiments (prohibited). Section III-E's future-work sentence expanded into a concrete roadmap: the reruns' attached question is whether the naive-baseline MAE stronghold and the retrieval sign reversal persist as event density doubles (0.60) or halves (0.80). Table 1 numbers untouched. |

## P2 — Nice-to-have

| Item | Status | Change |
|---|---|---|
| P2-1 Reader's guide paragraph at end of Section I | **DONE** | Extended the organization paragraph with an explicit reader's guide (benchmark-only readers → III+V; central result → VI-C + Fig. 3; negative findings → VI-A/B + VII-C; trust assessment → III-F), addressing the review's density concern (Finding 6.3). |
| P2-2 Training/convergence curves figure | **SKIPPED — needs-experiment** | Requires re-running training to log loss curves and generating a new figure; prohibited in this wave. |
| P2-3 Weather-year sensitivity note | **DONE** | Folded into the upgraded Limitation 2: results come from the single meteorological year shipped with RTS-GMLC; multi-year re-instantiations would test year specificity. (Phrased without asserting a specific calendar year.) |

## Additional item requested by the task

| Item | Status | Change |
|---|---|---|
| Reference list IEEE-style consistency check | **DONE** | 28 references confirmed IEEE numbered style, order-of-citation. Normalized six article-number entries to "Art. no." form ([5], [7], [8], [11], [12], [21]) and fixed lowercase DOI strings to canonical registered case in [9] (10.1175/MWR-D-12-00281.1) and [17] (10.1109/TPWRS.2007.901670). No references added or removed, so no external verification was required. |

## Not altered (by design)

- All experimental numbers, tables (Tables 1–4), leaderboards, p-values, and figure files.
- All evidence CSVs under `papers/mintou/mintou_p1_dstar_gru_dispatch/evidence/`.
- All `[TODO: ...]` author/affiliation/funding/repository markers.
