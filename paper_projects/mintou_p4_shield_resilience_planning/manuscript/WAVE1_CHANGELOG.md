# Wave-1 Changelog — mintou_p4 (SHIELD-MOEA, MDPI Energies)

Date: 2026-07-17. Source review: `mintou_p4_shield_resilience_planning/ROUND_REVIEW.md`
(pre-submission review, 2026-07-16).

Note on provenance: the wave-1 editing agent was interrupted by a session limit
immediately after completing the manuscript edits and `cover_letter_notes.md`;
this changelog was written by the supervising session after verifying each
edit in the manuscript. The agent's last status: "All 45 references sequential
and consistent."

| Review item | Status | What was done |
|---|---|---|
| P0#1 Submission admin (authors/affiliations/contributions/funding/DA URL) | **Skipped — needs author info** | All `[TODO: author...]` markers left untouched; sole remaining submission blocker. |
| P0#2 Literature refresh + MDPI numbering | **Done** | Reference list expanded from 29 to 45 entries in MDPI numbered style (order of first appearance), adding 2022–2026 work on resilience-oriented distribution planning, scenario generation/robust optimization, and NSGA-II-based planning (e.g., refs 11–17, 23–29, 37–41). Supervising session independently spot-checked 6 of the newest DOIs against Crossref (10.3390/en19020574, 10.3390/en19122798, 10.1049/rpg2.70185, 10.3390/electronics14214324, 10.1016/j.swevo.2025.101860, 10.3390/app151910303) — all resolve with exactly matching titles/venues/years. Automated post-check: 45 entries sequential 1..45, every entry cited, no orphan citations. |
| P1#3 Screening positioning | **Done (positioning paragraph; title unchanged)** | New Section 1 paragraph "What scenario screening is, and is not": screening buys 65% search-phase evaluation economy at statistically unchanged mean front quality; no mean-HV claim; wall-clock realization explicitly deferred to the power-flow-in-the-loop deployment regime. Echoed honestly in Section 6 (0.073 s vs 0.066 s per-run wall-clock disclosure). |
| P1#4 GA/DE hybrid ablation gap | **Done (discussion; no new experiment)** | Section 4 states the design rationale (DE injects direction-informed diversity, GA crossover preserves building blocks); Section 6.3 adds an explicit attribution-boundary paragraph: the hybrid is a motivated default, not a validated contribution; an unconditional NoDE/NoGA ablation is recorded as a limitation and future work. |
| P1#5 AC experiments named + hedge | **Done** | Section 5.4 names the three AC-validated experiments (deterministic_vs_scenario, der_uncertainty, outage_contingency) with the selection rationale (reference setting plus the two experiments deviating most strongly along single uncertainty axes that the AC scenario suite can probe directly). Abstract and Conclusion use "consistent qualitative pattern" hedging; AC readout framed as qualitative-consistency check at composition granularity. |
| P1#6 pop=60 30-seed expansion | **Skipped — needs experiment** | Deferred to a later wave. Mechanism discussion for the pop=60 significance loss retained. |
| P1#6 Table 5 double-default footnote | **Done** | Table 5 note explains the three default rows come from independent 10-seed streams (0.2674/0.2658/0.2687 — sampling variance, not inconsistency) and why the NSGA-II reference is identical across K/T_s rows but re-run for population rows. |
| P1#6 Deprecated-pipeline sentence neutral | **Verified** | Section 5 uses the neutral phrasing ("a preliminary proxy-based scoring pipeline that was deprecated in full"); deprecated artifacts declared retained in the public evidence trail. |
| P2 Same-journal perception management (p3/p4) | **Done** | `cover_letter_notes.md` drafted: proactive companion disclosure paragraph, differentiation table, shared-artifact scope (candidate-pool generation code only). |
| AI use disclosure | **Verified present** | AI-assistance statement present near declarations (authors reviewed and take full responsibility). |
| P2 MOEA/D constraint-domination variant, Figure 1 readability | **Skipped — needs experiment / formatting stage** | — |

## Integrity checks

- No evidence CSV/config/results file modified; no experimental number altered
  (headline numbers 0.2740, +5.09%, +5.56%, 40/40, 0.708→0.625, 68.8%→82.3%
  spot-checked unchanged).
- Automated citation-consistency check passed (45/45 sequential, all cited;
  the only bracket flags are math intervals like [0,1]^n, not citations).
- All `[TODO: author...]` markers byte-identical.

## Remaining before submission

1. Author info: names, affiliations, correspondence, contributions, funding,
   Data Availability repo URL/DOI (P0#1).
2. Optional wave-3 experiment: pop=60 at 30 seeds or pop=80 x 10 seeds (P1#6);
   MOEA/D constraint-domination baseline variant.
3. MDPI template conversion at formatting stage; Figure 1 readability check.
