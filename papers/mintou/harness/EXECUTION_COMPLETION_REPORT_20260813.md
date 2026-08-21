# Mintou Six-Paper Deep-Optimization Completion Report

Date: 2026-08-13 (Asia/Shanghai)

## 1. Outcome

The approved six-paper optimization plan has been executed through the scientific-content, experiment, manuscript, figure, and three-round review stages. For every project, stages 1--5 are `ACCEPTED`. Stage 6 is intentionally `BLOCKED` at the author-controlled submission gate. This terminal state distinguishes completed scientific work from metadata, rights, and authorship declarations that cannot be inferred by the harness.

All six projects passed the final scientific evidence-contract check and rebuilt their official journal PDF with exit code 0 on 2026-08-13. The builds produced only the local MiKTeX update reminder; no fatal LaTeX, undefined-reference, or missing-artifact failure was reported by the acceptance scripts.

This completion report does not claim guaranteed acceptance by a journal. It records that the manuscripts have reached the strongest locally verifiable scientific state supported by the available data and that remaining submission blockers require human confirmation.

## 2. Final manuscript set

| Paper | Final title | Scientific stages | Submission gate | Official PDF |
|---|---|---:|---:|---:|
| P1 | A Reproducible Retrospective Curtailment-Risk Benchmark and Fair Evaluation of GRU Learned-Space Retrieval on RTS-GMLC | 5/5 accepted | Blocked | 12 pages |
| P2 | Cross-Series Context for 24-Step-Ahead Point Forecasting of Multi-Region Power Load: A Matched Rolling-Origin Component Evaluation | 5/5 accepted | Blocked | 25 pages |
| P3 | CARS-MODE: Constraint-Aware Repair and Strategy-Pool Multi-Objective Differential Evolution on a SimBench-Derived Mixed-Voltage Portfolio Proxy | 5/5 accepted | Blocked | 30 pages |
| P4 | SHIELD-MOEA: Scenario Screening with Disjoint Evaluation for Proxy-Based Distribution-Network Resilience Planning | 5/5 accepted | Blocked | 30 pages |
| P5 | TRACE-MOEA: Constrained Power-Grid Portfolio Search with Adaptive Preference Elitism, Budget Repair, and Run-Level Event Co-Occurrence Summaries | 5/5 accepted | Blocked | 29 pages |
| P6 | BiLo-NSGA: Budget-Aware Project-Level Local Moves with Accepted-Move Logging for Power-Grid Portfolio Optimization | 5/5 accepted | Blocked | 30 pages |

Each project retains its manuscript, journal-template LaTeX source, PDF, vector/raster figures, derived tables, experiment code, run configuration, raw or archived results, evidence manifests, review closure, and append-only harness timeline under its own project directory.

## 3. Scientific corrections and retained findings

### P1

The task was reframed as a reproducible retrospective benchmark rather than a general operational forecasting claim. The learned-space retrieval path outperformed the matched GRU head in the registered comparison, but persistence achieved a lower MAE at the primary cap. The manuscript therefore does not claim that learned geometry has been isolated as the cause of the observed difference. The RTS-GMLC time-domain scope was corrected to distinguish 8760- and 8784-hour cases.

### P2

The paper now reports 240 matched rolling-origin runs. Target-context benefits were null in the tested design, the learned weighting forms were unresolved, and the independent encoder performed worse under a comparison that remains compute- and width-confounded. DLinear performed better in the exact hierarchy. These results are retained as component evidence rather than hidden or converted into a superiority claim.

### P3

The manuscript is grounded in a 2940-row archived exact rerun. Analytic hypervolume and IGD+ recomputation changed the method ordering, with FixedDE nominally ahead on the relevant comparison. AC examples are presented as illustrative, dependent checks rather than an independent production-grid validation.

### P4

The final boundary experiment contains 1050 runs. SHIELD-MOEA exceeded NSGA-II with repair within the tested proxy settings, but the isolated contribution of each mechanism remains unresolved. The reported 65% screening reduction is explicitly defined as optimization-loop row arithmetic rather than an end-to-end wall-clock or operational saving. The inactive DER factor and fixed AC mapping are disclosed.

### P5

The preference effect remains unresolved at approximately 0.17%. Trace evidence is described as run-level event co-occurrence, not causal lineage, exact replay, or demonstrated human decision value. All 46 archived artifacts passed the declared hash check.

### P6

The fair-effort study comprises 1440 runs: 720 under exact evaluation accounting and 720 under matched elapsed-time accounting. Every exact-evaluation row used 3200 accounting units, and the matched-time rows stayed within 0.200004--0.201374 seconds.

Under matched evaluation, BiLo-NSGA obtained mean HV 0.162766 versus 0.172131 for NSGA-II, with four significant losses and no wins; it exceeded bounded PLS on all eight scenarios. Under matched time, BiLo-NSGA obtained 0.170979 versus 0.172211 for NSGA-II, with three wins, two losses, and three unresolved scenarios, and again exceeded bounded PLS on all eight. Depth 2 improved the registered depth comparison by 4.288%; the group-bonus and penalty interventions were small or null. The title and conclusions were revised to avoid a general superiority claim.

## 4. Narrative and review closure

The Applied Sciences experience from MA-SQLGrid and C2GES was distilled into the six-paper workflow in four ways:

1. Every title and contribution is bound to an explicit task--method--evidence contract.
2. Main text prioritizes the scientific problem, mechanism, main result, and limitations; hashes, version history, and operational logs remain supporting evidence.
3. Matched-budget, rolling-origin, boundary-condition, and analytic-metric checks are used where they directly address a claim; experiment volume is not treated as a substitute for identification.
4. Negative and unresolved findings remain visible in the abstract, results, discussion, and conclusion whenever they constrain the claim.

Each paper completed three review-and-revision rounds covering narrative logic, method/theory consistency, statistical interpretation, artifact traceability, figure/table consistency, and journal-template compilation. The paper-specific closure records remain in the corresponding project directories.

## 5. Harness improvements produced by the execution

The workflow exposed and corrected three orchestration defects in `D:\aicoding\Lib\paper_harness`:

- version 0.2.3 added process-tree timeout containment;
- version 0.2.4 made custom Python checks import code from the isolated worktree rather than the mutable main tree;
- version 0.2.5 preserved locked worktrees after timeout, excluded legacy worktree directories from retries, and assigned a fresh retry nonce.

The final harness smoke suite passed 18/18 tests. An earlier custom-check import failure was rerun inside the preserved isolated worktree with the worktree `src` directory on `PYTHONPATH`; no scientific values were changed by that infrastructure correction.

The complete process lessons and reusable six-stage template are recorded in `DEEP_OPTIMIZATION_LESSONS_20260813.md`.

## 6. Submission gate

No paper has been auto-submitted. For each project, the final gate correctly refuses submission until the project-specific acceptance record is satisfied. Typical author-controlled requirements include:

- confirmed author order, affiliations, and corresponding-author email;
- confirmed CRediT contributions and final author approval;
- funding number, funder wording, and APC responsibility;
- conflict-of-interest, ethics, consent, and acknowledgment statements where applicable;
- persistent data/code repository identifier and redistribution-rights confirmation;
- disclosure and independence statement for overlapping companion manuscripts.

The exact blocker list is authoritative in each stage-6 `acceptance.json` and associated submission-gate record. These fields must be supplied and approved by the authors; they must not be guessed by an automated agent.

## 7. Preserved incident evidence

The P6 timeout incident remains preserved and excluded from accepted results. Its work-in-progress patch is stored at:

`paper_projects/mintou_p6_bilonsga_project_review/.paper_harness/attributions/p6_s2_method_contract_timeout_wip_20260813.patch`

SHA-256:

`0A8869FE0B638113353DD10EDEED55CCF54B2988AFA8D7C13FE2F3A5C141356C`

The locked legacy worktree was neither continued, overwritten, deleted, nor included in the manuscripts. The approved clean retry is the accepted lineage.

## 8. Final acceptance boundary

The locally complete state is therefore:

- scientific narrative and evidence contract: passed for six papers;
- planned experiments and derived analyses: completed and incorporated;
- figures, tables, LaTeX, and official PDF: rebuilt and verified;
- three-round expert-style review: completed and closed;
- author-controlled declarations and external submission: blocked pending human confirmation.

This boundary is deliberate. It prevents a technically complete research package from being mistaken for an authorized submission package.
