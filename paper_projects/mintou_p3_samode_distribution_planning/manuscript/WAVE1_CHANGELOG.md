# Wave-1 Pre-Submission Changelog (Round-5 终投清单)

- **Date:** 2026-07-17
- **Scope:** `manuscript/MANUSCRIPT.md` only; no experiments re-run, no experimental numbers altered; author/funding/repo-URL `[TODO: ...]` markers left untouched by design.
- **Reference verification:** every completed or added reference was verified against its Crossref DOI record on 2026-07-17 (`api.crossref.org/works/<DOI>`).

## Item-by-item status

| # | Level | Review item | Status | Change description |
|---|---|---|---|---|
| 1 | P0 | References TODO 清零 (refs 8–14, 16, 19 author lists; Gonzalez-Longatt DOI check; MDPI numbered style; commentary spot-check) | **Done** | All 9 `[authors TODO]` entries completed from Crossref DOI records. **Correction found:** DOI 10.3390/en17215432 (ref 8) is authored by *Prenc, R.* (sole author), not Gonzalez-Longatt — reference and the §2.1 in-text mention ("Gonzalez-Longatt et al. [8]" → "Prenc [8]") corrected; a note documenting the misattribution is kept in the references HTML comment. Refs 9–14, 16, 19 filled with full verified author lists (Saldaña-González et al.; Liu et al.; Wang et al.; Alotaibi; Ferreira et al.; Chen, Zhang, Liang; Alrashidi et al.; Cadena-Albuja et al.). Spot-checks: refs 15, 17, 18 author lists and titles match their DOI records; per-reference commentary in §2.1–2.2 matches the actual paper titles/abstracts (Wasserstein [10], WGAN-GP [11], restoration/islanding [12], TSO–DSO [13], AC/DC data centers [14], improved NSGA-II storage+EV [15], CGO DG/CB/EVCS [16], BWO storage [17], coati TNEP [18], DE dispatch comparison [19]). Whole list renumbered to strict MDPI order-of-appearance (now 32 entries); two previously uncited entries (PlatEMO, CoDE) are now cited in §2.2/§2.3 so no orphan references remain. |
| 2 | P0 | 投稿机械项 (authors/affiliation/correspondence/contributions/funding; repo DOI) | **Skipped** | Author-identity items — cannot be filled by this pass; all `[TODO: author...]`, funding, and repository URL/DOI markers deliberately left untouched per constraints. |
| 3 | P0 | Abstract: compress ≤200 words; fix "loses the most (0.569, tied)" contradiction | **Done** | Abstract rewritten at **199 words** (was ~255). Contradictory clause replaced with "the fixed-parameter ablation is tied for the largest AC-feasibility drop (0.569)". No experimental number changed. |
| 4 | P1 | Manual CSV–manuscript cross-check of base composition 6/7/1/0; composition table into evidence trail | **Done (verified)** | Verified in `papers/mintou/mintou_p3_samode_distribution_planning/evidence/tables/real_simbench_planning_compromise_compositions.csv`: base_distribution_planning CARS-MODE = **6 reinforcement / 7 storage / 1 DER / 0 automation — matches §6.3 exactly.** Also verified: FixedDE base = 5/8/1/0 (the "8 storage vs. 7" claim in §6.3/§7 ✓), NSGA-II base = 5/4/6/0 ✓, Standard DE base = 7/4/2/0 ✓, storage_allocation CARS-MODE = NSGA-II = 8/5/0/0 ✓. A composition table already exists in the evidence trail (the CSV above — no new file needed, avoiding data duplication); §6.3 now cites it by filename instead of the vague "Table of compromise compositions in the evidence". |
| 5 | P1 | Abstract AC sentence hedge | **Done** | AC-validation sentence now reads "...then shows, as a consistent qualitative pattern rather than a second statistically powered comparison, that the proxy ranking does not transfer to the electrical layer". |
| 6 | P2 | §2 feature-comparison table; 2–4 new citations | **Done** | New **Table 1** added in §2.4 (feature comparison: task / engine / Pareto front / self-adaptive F-CR & strategy / constraint repair / per-component ablation / AC power-flow check) covering jDE, SaDE, SHADE, refs [15]–[19], and CARS-MODE; entries for related works use ✓ / -- / n.r. marks grounded only in their verified titles/abstracts (no new claims — "n.r." where not reported). Two new verified references added (both Crossref-checked, both ≤5 years old, raising the recent-share): Kudela, *Nat. Mach. Intell.* 2022 (10.1038/s42256-022-00579-0), cited in §2.2 benchmarking-audit sentence; Ahmad et al., *Alex. Eng. J.* 2022 (10.1016/j.aej.2021.09.013), cited in §2.3 DE-survey sentence. Old table numbers shifted: Tables 1–7 → Tables 2–8, all in-text mentions updated. |
| 7 | P2 | Table 7 (now 8) double-default footnote; storage_allocation collision sentence; §3.2 EHV–MV boundary | **Done** | (a) Table 8 caption now carries an explicit footnote: the "$N_p$ = 40 (default)" and "$\tau$ = 0.1 (default)" rows are independent re-runs of the same default configuration on different seed streams; 0.0409 vs. 0.0410 is sampling variance (the old caption wrongly spoke of two "40 (default)" rows). (b) One sentence added in §6.3: in storage_allocation, CARS-MODE and NSGA-II converge to identical 8/5 compositions, so 24 of 72 AC cases coincide by construction (mapping is deterministic and method-independent) — matches the evidence CSV. (c) §3.2 EHV–MV voltage-level boundary statement confirmed already present ("We flag this voltage-level boundary explicitly..."); no change needed. |
| — | — | MDPI AI-use disclosure | **Already present** | "AI-Assisted Development" section exists (Claude disclosure, human-verification statement, MDPI policy reference); confirmed, no change. |

## Post-edit consistency checks (all passed)

- Abstract = 199 words (limit 200).
- 32 in-text citation numbers ↔ 32 reference entries; no orphans, no missing; strict order of first appearance.
- No remaining `[authors TODO]` in references; remaining `[TODO]` markers are author/funding/repo-URL only (out of scope by constraint).
- "loses the most" — 0 occurrences; Table mentions Table 1–8 all consistent.
- All quantitative results, tables 5–8 values, and evidence numbers untouched.

## Remaining blockers for submission (not addressable in this pass)

1. Authors / affiliations / correspondence / contributions / funding (front matter + declarations).
2. Repository URL/DOI in Data Availability (Zenodo/GitHub release).
