# C2GES AI-research failure-mode gate

Date: 2026-09-06  
Pipeline point: ARS Stage 2.5 integrity gate  
Decision: **BLOCK — do not advance to submission finalization**

This audit distinguishes an honest protocol-ready paper from a completed
empirical paper. The current manuscript explicitly labels E1, E2, and
confirmatory E3 as unexecuted. It therefore does not fabricate their outcomes,
but it also cannot pass the final scientific gate until those outcomes exist and
are hash-bound to the backfilled manuscript.

## Seven-mode audit

| Mode | Current verdict | Evidence | Required resolution before submission |
|---|---|---|---|
| 1. Implementation bug passing self-review | **INSUFFICIENT EVIDENCE for E1/E3; CLEAR for packaged historical and development checks** | Core, post-run, prospective, layout, and human-validation tests pass; the development factorial has a saved integrity report and is explicitly non-confirmatory. No formal external run exists yet. | Execute the frozen one-attempt runner; retain zero-exit logs, configuration/code hashes, per-item status, failed-row count, environment versions, and output hashes. |
| 2. Hallucinated citation | **CLEAR for the current reference list** | `REFERENCE_DELTA_AUDIT_2026-09-06.json` accounts for all 35 cited keys and records 0 unresolved references; PacSum was checked against the ACL Anthology record. | Re-run the complete citation and claim-context audit if E1--E3 backfill adds or changes any reference or literature claim. |
| 3. Hallucinated experimental result | **CLEAR for current prose; INSUFFICIENT EVIDENCE for future E1/E3 claims** | The Abstract, Results, Discussion, Conclusions, ethics statement, and data statement say that E1--E3 are not results. Historical numbers are tied to packaged ledgers and scripts. | Every new numerical sentence, table cell, and plot must trace to a frozen E1/E2/E3 artifact listed in `SUBMISSION_EVIDENCE_LOCK.json`. |
| 4. Shortcut reliance | **SUSPECTED / unresolved** | Existing equal-unit advantages are confounded by 54--63% longer output, and the historical path ablation changes score scale. The planned matched-word comparison and controlled factorial directly target these shortcuts but have not run. | Complete E1 matched-word evaluation and E3 AB/RP/G controls. Do not use superiority or component-causality language unless the predefined gates support it. |
| 5. Implementation bug reframed as insight | **CLEAR for the current negative-path narrative; INSUFFICIENT EVIDENCE for formal external results** | The manuscript does not convert the path term's negative historical finding into a positive novelty claim; it reports zero-weight development calibration and scale confounding. | Independently reproduce the formal run from frozen inputs and confirm all unexpected findings against item-level selections before narrative backfill. |
| 6. Methodology fabrication | **CLEAR for current historical/future-tense separation; INSUFFICIENT EVIDENCE for submission-final Methods** | Prospective procedures are consistently described as planned, protocols remain `DRAFT_NOT_FROZEN`, and `external_test_accessed=false` is explicit. | After execution, cross-check every past-tense Methods statement, sample count, budget, model revision, seed, parameter, failure count, and statistical family against formal manifests. |
| 7. Early frame-lock | **SUSPECTED / title-dependent** | The title commits to “Structure-Aware” and “Typed-Path Graphs,” while human construct validity and independent path value remain unverified. The pre-submission review flags this as critical. | Use E2/E3 result-driven rules. If structure thresholds or typed/path controls fail, downgrade the corresponding title, abstract, contribution, and conclusion language rather than preserving the frame. |

## Blocking determination

Modes 1, 4, 5, 6, and 7 remain unresolved for a submission-final empirical
claim set. Under the fail-closed ARS integrity rule, the manuscript cannot move
to finalization. This is not a judgment that the method has failed; it records
that the necessary confirmatory evidence does not yet exist.

The executable check is:

```text
python 03_Reproducibility/Code/prospective_v1/submission_readiness.py
```

On the protocol-ready snapshot it must return exit code 2 and `NOT_READY`.
Changing labels in the public verification report is insufficient: the gate
also checks formal run state, at least eight external series, zero failed item
rows, two completed blinded annotation files, adjudication, ethics status,
factorial outputs, removal of provisional manuscript language, and a complete
SHA-256 evidence lock.

## Re-audit trigger

Re-run this seven-mode audit from scratch after E1/E2/E3 backfill. The final
gate may state `CLEAR` only when the actual logs, data, manuscript, figures,
tables, PDF, and release manifest agree. Any author override must record the
reasoning explicitly and cannot override missing experimental evidence or an
unresolved ethics determination.
