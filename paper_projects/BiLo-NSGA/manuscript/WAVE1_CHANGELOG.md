# Wave-1 Changelog — mintou_p6 (BiLo-NSGA, MDPI Applied Sciences)

Date: 2026-07-17. Source review: `mintou_p6_bilonsga_project_review/ROUND_REVIEW.md`
(Round-5 pre-submission review, 2026-07-16).

Note on provenance: the wave-1 editing agent was interrupted by a session limit
after completing all manuscript edits; the final citation-consistency check,
this changelog, and `cover_letter_notes.md` were completed by the supervising
session. All edits below were verified present in the manuscript afterwards.

| Review item | Status | What was done |
|---|---|---|
| P0.1 [TODO] author/affiliation/funding/DA markers | **Skipped — needs author info** | Left untouched; sole remaining submission blocker. |
| P0.2 References → MDPI numbered style | **Done** | All 32 references converted from author–year to numbered style in order of first appearance; all in-text citations remapped. All DOIs re-verified via Crossref (2026-07-17). Two broken entries caught and corrected during conversion: [4] (was "Li et al., 2026" with a non-resolving DOI → real record: Feng, Hu, Chen, Wang, *Neurocomputing* 666:132135, 10.1016/j.neucom.2025.132135) and [32] (was "Chen et al., 2025" with a non-resolving DOI → real record: Regaigui, Bezoui, Moulai, Qaisar, *Applied Soft Computing* 175:113058, 10.1016/j.asoc.2025.113058); author-list corrections to [19] and [31]. Post-hoc automated check: 32 entries sequential 1..32, every entry cited, no out-of-range citations. |
| P0.3 Figures "placeholders" | **Stale review finding — no action needed** | Real 300-dpi PNGs (4 files) have existed at `manuscript/figures/` since 2026-07-15; verified present. |
| P0.4 iThenticate self-check vs p5 | **Skipped — needs external account** | User action before submission. |
| P1.1 "Bidirectional" naming vs evidence | **Done (wording; method NOT renamed)** | Abstract and Introduction now state the asymmetry explicitly: measured gain comes from forward insertion under budget slack (parity at 0.75x, +3.40% at 1.20x); backward pass retained for audit completeness and substitution semantics, not hypervolume. Section 6.3 retitled "Ablation Study: An Asymmetric Bidirectional Search" with a three-reason honest analysis and operator-redesign next step. |
| P1.2 Sensitivity analysis (scalarization weights / penalty / dependency bonus) | **Skipped — needs experiments** | Deferred to a later wave. |
| P1.3 Second benchmark pool | **Skipped — needs experiments** | Deferred (NREL-118 candidate source is cached). |
| P1.4 Companion-submission editorial strategy | **Done** | `cover_letter_notes.md` drafted with the p5/p6 differentiation table and the 0.75x budget-reversal argument (BiLo-NSGA -0.33% n.s. vs TRACE-MOEA +1.39% under the same tightening), consistent with the p5-side notes. |
| P2.1 Abstract ≤200 words | **Done** | Compressed to 198 words; budget-sensitivity pattern and forward/backward asymmetry are now headline elements. No numbers changed. |
| P2.2 Recent Applied Sciences citations | **Done** | Reference list now includes recent MDPI Applied Sciences items (e.g., [10] Liang et al., *Applied Sciences* 2024, 14(15), 6486) among the Crossref-verified additions. |
| P2.3 ORCID | **Skipped — needs author info** | — |
| P2.4 Limitations and Future Work pairing | **Done** | New Section 7.1 pairs each limitation with a concrete actionable next step. |
| P2.5 Companion mechanism description calibration | **Done** | All companion references use "companion study"; TRACE-MOEA described as a preference-adaptive ranking layer over an NSGA-II core with review-rule repair and a trace archive ("cooperative coevolutionary" wording removed; zero occurrences remain). |
| Generative AI statement | **Verified present** | "Generative AI Statement" section exists before Conflicts of Interest. |

## Integrity checks

- No evidence CSV/config/results file modified; no experimental number altered.
- Automated citation-consistency check passed (32/32 sequential, all cited,
  none out of range).
- Abstract word count: 198.
- All `[TODO: author...]` markers byte-identical.

## Remaining before submission

1. Author info: names, affiliations, correspondence, CRediT contributions,
   funding, ORCID, Data Availability repo URL/DOI (P0.1, P2.3).
2. iThenticate cross-check vs the p5 companion manuscript (P0.4).
3. Optional wave-3 experiments: sensitivity scans (P1.2), second benchmark
   pool (P1.3).
4. MDPI template conversion at formatting stage.
