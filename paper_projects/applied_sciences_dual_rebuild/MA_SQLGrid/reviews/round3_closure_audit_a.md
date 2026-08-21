# MA-SQLGrid Round-3 Independent Closure Audit A

Date: 5 August 2026  
Auditor: `/root/ma_round3_closure_a`  
Decision: **SCIENTIFIC_CLOSED_HUMAN_GATES_OPEN**

## Scope and independence

This was a read-only closure audit of the three Round-3 reviews, `round3_author_response.md/json`, the stable final TeX/PDF, exact sign enumeration, semantic-v5 release, portable manifest and clean-copy report, manuscript verifier, tests, and LaTeX build evidence. I did not edit or compile the manuscript.

Stable final identity:

- TeX: 71,379 bytes; SHA-256 `E8FECF6C8D4223BA75B87FCDAE97EEE6A66035BE500CBD9B0B3991752644C420`.
- PDF: 25 pages, 664,609 bytes; SHA-256 `1A2220381D18E2F5B037320B14377E6010A095F6A9AFAE834F0B3CF6C1FA7E4F`.
- Round-2 response, Round-3 response, and `W10_ASSEMBLY_REPORT.md` all bind this stable PDF identity. The earlier build-time metadata hash drift is therefore closed.

## Closure result

All locally executable Round-3 scientific and editorial actions are genuinely closed. The response accounting is internally consistent: 26 tracked findings comprise 23 actionable findings and three severity-none verification checks; statuses are 18 `resolved`, two `resolved_internal_only`, one `pending_bird_formal_run`, and five `deferred_human`.

Key independent checks passed:

- Semantic-v5 contains 25,920 atomic rows over 18 states, with 1,440 rows per state; the registered denominators are 528 eligible predictions/66 questions/7,920 primary semantic rows and 912 held predictions/114 questions/16,416 all-state diagnostic rows. T0 continuity is 1,440/1,440.
- Independent in-memory exact recomputation used all $2^{12}=4096$ assignments per test and reproduced raw values 0.750, 1.000, 1.000, 0.500, 1.000, 1.000, 0.500, 0.625, and 1.000. All nine Holm-adjusted values are 1.000.
- The cluster-size concentration, the $m=r$ estimand family, base seed 20260805, and family-offset RNG rule are disclosed in Methods.
- Reviewer identity is unambiguous: the abstract and Methods say agent technical reviewers and expressly deny qualified human semantic-audit status.
- Displayed tables use composition-sensitivity terminology. Legacy unused table-source files containing `CI` labels are not included by the final TeX.
- Figure 6 is decongested; Tables 6--7 define F00--F11 and state $n=66$/12 clusters; the Featured Application and Discussion impose the intended human-inspection and no-field-validation boundary.
- The 15 external automatic matches are never presented as accuracy or used in inference.
- Manuscript verifier: PASS (v2=26, v3=15, component-analysis=4, nine figures, 23 citation keys).
- Semantic release verifier: PASS. Portable verifier: PASS locally and on the preserved clean copied root, 19 checked files each; the portable manifest contains 18 repository-relative artifacts and no absolute artifact path.
- Semantic test suite: 22 passed, one explicit skip. Final LaTeX log: zero errors, zero undefined references, zero overfull boxes; four underfull-box and two PDF-string warnings are non-blocking.

The `resolved_internal_only` treatment of the portable package is valid: the locally controllable relative-path manifest and clean-copy verification are complete, while redistribution clearance and DOI creation are separately retained as human/legal gates. The retained IMRaD/evidence-tier structure is also a justified response to an editorial consolidation preference, not an unresolved scientific defect.

## Human gates that remain open

The following are **HUMAN_GATE_OPEN**, not failures of internally executable scientific revision:

1. **BIRD public comparator:** explicit human authorization is required before the frozen 5,000-call launch. Current status is `FROZEN_NOT_RUN`, with zero formal model calls and no imported BIRD result.
2. **External domain validation:** two qualified human reviews and adjudication of the 91 external pairs, followed by a sealed external set, require domain expertise not supplied by agents.
3. **Author metadata and declarations:** identities, affiliations, correspondence, CRediT, funding, conflicts, acknowledgments, ethics/consent confirmations, and final AI-use language require author approval.
4. **Licensing:** GridDB redistribution and source-specific derivative rights require author/legal or rights-holder review.
5. **Repository deposit:** a permanent DOI/URL can be created only after an authorized, license-cleared deposit.

Accordingly, the Round-3 scientific revision is closed, but the package is not yet submission-ready until these human gates are completed.
