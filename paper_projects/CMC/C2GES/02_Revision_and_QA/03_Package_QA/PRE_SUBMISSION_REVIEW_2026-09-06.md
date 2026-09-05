# C²GES Pre-Submission Review

## Summary

- **CRITICAL:** 2
- **MAJOR:** 3
- **MINOR:** 3
- **Top three fixes:** execute frozen E1/E2/E3; condition the title and component claims on E2/E3; replace the protocol narrative with measured results and a submission-final release.

The paper is a technically sound protocol-ready snapshot, not a submission-ready research article. Its strongest quality is unusually explicit separation of historical, exploratory, and future evidence. Its principal weakness is equally explicit: the studies needed to support the title and main contribution have not yet been conducted.

## Dimension 1: Macro logic

| # | Finding | Severity | Suggested fix |
|---|---|---|---|
| 1 | The Abstract states, “Those experiments remain unexecuted”, and the Conclusion states, “Abstract, component claims, and the final recommended configuration must be updated from measured E1--E3 results before submission.” | CRITICAL | Freeze the unseen series, execute E1 and E3 once, complete blinded E2, then rebuild Abstract through Conclusions from the frozen result artifacts. |
| 2 | The title asserts “Structure-Aware ... with Typed-Path Graphs”, while the Abstract states that current evidence does not establish “validated structural relations”. | CRITICAL | Retain the title only if E2 meets the frozen role/edge/path thresholds and E3 supports an independent structural contribution; otherwise weaken the title and all construct-validity language. |
| 3 | The historical main comparison reports that Full C²GES “exceeded Semantic-MMR and TextRank at equal unit counts”, but the same sentence notes extracts were “54--63% longer”. | MAJOR | Make the prospective 110/260-word external comparison the primary result. Keep this comparison only as historical evidence. |
| 4 | The component claim relies on an “unrenormalized coefficient-removal comparison”, which changes both path inclusion and score scale. | MAJOR | Use AB-5 versus AB-6 as the principal path comparison and report the RP interaction and G-U/G-T contrast before attributing any mechanism. |
| 5 | The paper's applied beneficiary is stated as analyst-facing navigation, but “operational reading benefit” is explicitly untested. | MAJOR | For the minimum method-paper route, complete E1--E3 and limit the claim to source-linked technical-report summarization. Run E4 only if review-time, task-accuracy, or safety benefit is claimed. |

## Dimension 2: Writing details

| # | Finding | Severity | Suggested fix |
|---|---|---|---|
| 1 | “This revision treats those results as historical evidence” and repeated “protocol-ready” wording describe document history rather than the scientific study. | MINOR now; MAJOR in final | After result backfill, remove revision-history narration from the article and retain it only in the reproducibility record. |
| 2 | The Introduction contribution paragraph mixes completed contributions with “design commitments”. | MINOR now | In the final version, list only contributions supported by completed E1--E3 results; move protocol chronology to Supplementary Materials. |

## Dimension 3: English grammar

| # | Finding | Severity | Suggested fix |
|---|---|---|---|
| 1 | No systematic article, agreement, or comma-splice error was found in the current pass. Long statistical sentences are dense but grammatically controlled. | — | Preserve present tense for Methods and past tense for executed Results (Rules G3 and G4) during backfill. |

## Dimension 4: LaTeX format

| # | Finding | Severity | Suggested fix |
|---|---|---|---|
| 1 | The MDPI build succeeds with 35/35 citations, 17/17 references, 6 figures, and 9 tables; there are no overfull boxes. | — | No corrective action. |
| 2 | Labels such as `tab:related-comparison` and `fig:component-diagnostic` use hyphens rather than the review skill's preferred underscores. | MINOR | Optional consistency cleanup; this is not a LaTeX or MDPI rejection risk. |
| 3 | Several `[H]` floats contribute to dense page placement. | MINOR | During final backfill, prefer `[t!]` for large figures/tables unless MDPI's template requires the present placement. |

## Dimension 5: Figure quality

| # | Finding | Severity | Suggested fix |
|---|---|---|---|
| 1 | All six final figures are vector PDFs and machine-traced. Figure 6 is legible but its four-panel labels become small at full-width scaling. | MINOR | If the final paper retains Figure 6, consider a two-by-two layout or move secondary panels to the Supplement after E3 replaces the historical diagnosis. |

## Banned-vocabulary and em-dash scan

The entire LaTeX source was scanned, not sampled. The two body-text uses of “reveal” were replaced with “show”. No Unicode em dash remains. The only LaTeX `---` sequences are the standard CRediT phrases `writing---original draft preparation` and `writing---review and editing`, not sentence connectors. No repeated banned AI-tone term reaches the three-occurrence MAJOR threshold.

## Final score

**5/10 in the current evidence state.** Formatting, provenance, claim discipline, and reproducibility engineering are strong; the two CRITICAL evidence gaps prevent a near-ready score.

## Submission recommendation

**Needs major revision before submission.** Do not submit the protocol-ready snapshot as the completed Article. The target becomes reasonable after E1/E2/E3 and result-conditioned rewriting; current venue fit is medium, rising to high if those gates pass.
