# C²GES Integrity Delta Audit

**Audit date:** 2026-09-06  
**Evidence state:** protocol-ready snapshot; E1/E2/confirmatory E3 not executed  
**Verdict:** **PASS_FOR_PROTOCOL_SNAPSHOT / FAIL_FOR_SUBMISSION_FINALIZATION**

## 1. Citation and reference integrity

- Current bibliography: 35 entries; 35 cited keys; 0 dangling citations; 0 uncited entries.
- Thirty-four entries inherit the 2026-08-24 existence audit (34/34 verified, 13 days old at this audit).
- The only new entry, `zheng2019pacsum`, was checked against the official ACL Anthology BibTeX record and PDF. Authors, title, venue, year, pages, DOI, asymmetric preceding/following weighting, and thresholded centrality agree with the primary source.
- The manuscript calls the implementation `PacSum-MiniLM`, states that it is a controlled clean-room implementation, and does not claim byte-equivalence to the authors' task-fine-tuned BERT implementation.
- Ghost references detected: 0. Fabricated metadata detected: 0.

Machine record: `REFERENCE_DELTA_AUDIT_2026-09-06.json`.

## 2. Claim–evidence boundary

The manuscript maintains three distinct evidence tiers:

1. the 15-report formal run is historical post-audit corrective descriptive evidence;
2. post-run matched-word, cluster, embedding, layout, and normalized-ablation analyses are sensitivity or diagnostic evidence;
3. E1/E2/E3 text is a prospective protocol and uses future tense or explicit non-execution statements.

No numerical E1, E2, or confirmatory E3 result has been inserted. The current abstract, Results, Discussion, and Conclusions continue to state that a matched-length system advantage and human structural validity have not been established.

Figure 6 now reads its historical numbers from two machine artifacts: the exact independent post-run audit (`EB517D...BF1F`) and the development-only calibration decision (`AA4671...DBF`). This removes the prior hard-coded plotting dependency without changing the reported values.

## 3. Failure-mode scan

| ID | Failure mode | Status | Evidence-based assessment |
|---|---|---|---|
| M1 | Experiment code runs but does not implement the claimed algorithm | CLEAR for recorded historical runs; OPEN for unexecuted external study | Historical outputs passed frozen-run and recalculation audits. Prospective runner tests verify implementation behavior but are not scientific validation. |
| M2 | Citations are nonexistent or metadata is invented | CLEAR | 35/35 identities covered by the inherited audit plus official ACL delta check. |
| M3 | Numerical results cannot be traced to data artifacts | CLEAR for reported results | All six figures now have input/script/output lineage; historical tables point to packaged machine results. Future outcomes remain absent. |
| M4 | Shortcut features dominate while the claimed mechanism is not isolated | OPEN / suspected risk | Role reservation, typed graph, path deletion, and redundancy are not yet isolated on unseen series. The predeclared AB, RP, and G-U/G-T experiment is required. |
| M5 | A negative result is rhetorically converted into positive novelty | CLEAR | Path deletion is reported as active but not beneficial on the predefined historical endpoint. |
| M6 | Manuscript method differs from code | CLEAR for historical method; implementation-ready only for prospective method | Historical equations and frozen code agree. Prospective sections describe registered code paths but remain conditional on data freeze and execution. |
| M7 | Title or framing overstates construct validity | OPEN / submission-blocking | “Structure-Aware” remains a hypothesis-bearing label until E2 meets the predefined role, edge, path, locator, and faithfulness thresholds. A failed E2 gate requires explicit downgrading to heuristic proxy language and title reconsideration. |

## 4. Scientific and ethical limits

- No AI-generated annotation is treated as an eligible human label.
- E2 requires two independent qualified annotators and a documented institutional ethics review or exemption determination before recruitment.
- Source locator correctness is not equated with engineering usefulness.
- NERC technical reports remain a maintenance-oriented proxy; they do not establish generalization to confidential work orders or inspection narratives.
- Originality is **NOT CERTIFIED**. Similarity screening and final scientific judgment remain author/publisher responsibilities.

## 5. Submission-final blockers

The manuscript cannot yet be labeled submission-final because the title and planned contribution require:

1. rights-cleared unseen report series with series-disjoint assignment and signed freeze;
2. E1 one-time external evaluation under equal word budgets and balanced tuning;
3. E2 double-blind independent human validation plus ethics/exemption record;
4. E3 clean AB-0…AB-6, RP-00…RP-11, and G-U/G-T execution on the frozen series;
5. result-conditioned backfill of Abstract, Results, Discussion, Conclusions, Supplement, and claims.

The current package is therefore internally consistent and auditable as a **protocol-ready version**, but it is not yet evidence-complete for submission.
