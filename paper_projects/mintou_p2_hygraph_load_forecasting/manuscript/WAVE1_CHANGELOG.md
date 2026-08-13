# WAVE1 Changelog — mintou_p2 (CSA-LoadNet → MDPI Electronics)

**Date**: 2026-07-17
**Source review**: `mintou_p2_hygraph_load_forecasting/ROUND_REVIEW.md` (Round-4 Final, decision: ACCEPT with Minor Revision conditional on P0-1/P0-2/P0-3)
**Files changed**: `manuscript/MANUSCRIPT.md`, `logic/related_work.md` (both copies), `papers/mintou/.../evidence/figures/README.md`
**Constraints honored**: no [TODO] markers touched; no experiments run; no evidence CSV/results files modified; no experimental numbers altered; no new references added (so no new-reference verification was needed — all 30 existing references were already Crossref-verified 2026-07-16 and were only renumbered).

| Review item | Status | Change |
|---|---|---|
| P0-1 Resolve all [TODO] markers (authors, affiliations, email, CRediT roles, funding, repository URL) | **Skipped (per task constraints)** | Task instructions explicitly forbid touching [TODO: author/affiliation/ORCID/email/funding/repository-URL] markers; they require real author metadata only the authors can supply. All markers left byte-identical. Still a submission blocker. |
| P0-2 Add AI use disclosure | **Done** | New "Use of Generative Artificial Intelligence" section added after Conflicts of Interest (MANUSCRIPT.md line ~318), following MDPI's required wording pattern: tool named (Claude, Anthropic), purpose stated (drafting/editing and analysis-code assistance), full author verification and responsibility affirmed. |
| P0-3 Convert references to MDPI numbered format | **Done** | All 30 references renumbered in order of first appearance (1 = Li 2025 ... 30 = Meinecke 2020) and reformatted as a numbered MDPI-style list with italics/bold volume-year markup; every in-text author-year citation (44 occurrences, including compound citations) mechanically replaced with the matching [n]/[n,m]/[n–m] form. Mapping double-checked: numbers first appear in strictly ascending order (Intro [1–8], Sec 2.1 [9–18], Sec 2.2 [19–24], Sec 2.3 [25–28], Table 1 [29,30]); all repeats verified against the map. All DOIs preserved unchanged. Note: final journal-template conversion (Zotero/EndNote) at submission time is still advisable, but the manuscript is no longer author-year. |
| P0-4 Clean up stale `evidence/figures/README.md` | **Done** | `papers/mintou/mintou_p2_hygraph_load_forecasting/evidence/figures/README.md` rewritten: stale "synthetic smoke tests" placeholder replaced with pointers to the three verified 300-dpi figures in `manuscript/figures/` and the `make_figures.py` regeneration path against the v7 evidence tables. |
| P1-1 Hierarchical reconciliation baseline (MinT) on Ausgrid | **Done via fallback option in review** | Running MinT would require new experiments (forbidden). Applied the review's stated alternative: added an explicit statement in Section 6.4 and an extension of Limitation 2 noting that no reconciliation-specific baseline (bottom-up / MinT trace minimization, refs [22,23]) was tested and comparisons are against general time-series baselines only. |
| P1-2 Expand Ausgrid seed count (LSTM/TCN/PatchTST 3→10 seeds) | **Skipped** | Requires re-running experiments, forbidden by task constraints. Already acknowledged in manuscript as Limitation 5 with exact n reported. |
| P1-3 Replace `logic/related_work.md` auto-scaffold | **Done** | Both copies (`mintou_p2_hygraph_load_forecasting/logic/related_work.md` and `papers/mintou/.../logic/related_work.md`) replaced with a pointer to manuscript Section 2 and the extended `manuscript/related_work.md`, retaining the 12 comparator DOIs with cited/not-cited disposition. |
| P1-4 Weather-year sensitivity note | **Done** | New Limitation 7 added to Section 8: single chronological split, test segment Oct 2017–Dec 2018 spans essentially one weather-year; possible effect on absolute errors and aggregation-benefit size stated; no weather-year-robustness claim made. Cross-referenced to the Section 7.2 mechanism conjecture. |
| P2-1 Improve Introduction pacing | **Done (light touch)** | The dense second Introduction paragraph split into three shorter paragraphs (ornate-machinery trend / skeptics' line / middle ground). Contribution list was already bold-numbered and a roadmap paragraph already exists, so no further restructuring. |
| P2-2 Add training curves (supplementary figure) | **Skipped** | Would require generating new results artifacts (training/validation loss logs); out of scope under no-new-experiments constraint. |
| P2-3 Publish code repository | **Skipped** | Tied to the [TODO: repository URL/DOI] marker, which must not be touched; publishing a repository is an author action outside manuscript editing. |
| P2-4 Pre-registration note | **Done** | Closing paragraph added to Section 7.1: acknowledges the post-hoc nature of the claim downgrade, names the preserved v5→v6→v7 evidence chain as the compensating control, and recommends pre-registered analysis plans / registered reports for similar component-level studies. |
| Abstract length/wording fixes | **N/A — none listed** | The review lists no abstract-length or abstract-wording item; abstract left unchanged. |

## Verification performed

- No remaining author-year bracket citations in MANUSCRIPT.md (regex sweep clean).
- 44 numbered in-text citations audited against the appearance-order map; all correct.
- All [TODO] markers byte-identical to pre-edit state (lines 20–22, 304, 308, 312).
- Spot-check of all headline experimental numbers (0.032345, 0.033715, 0.034591, p = 0.0085/0.0011/0.0348/0.0044/0.084, 0.31324, 0.32361, SimBench nMAEs) — all present and unchanged.
- No evidence CSV, leaderboard, significance, or config file modified.
