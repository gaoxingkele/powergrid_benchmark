# Cover Letter Notes: Companion-Submission Strategy (TRACE-MOEA, mintou_p5)

Notes for drafting the cover letter to the MDPI Energies editor. This manuscript
(TRACE-MOEA) is submitted alongside the companion project
`mintou_p6_bilonsga_project_review` (BiLo-NSGA, cited as ref [28]). Its
submission-time bibliographic status requires author confirmation. The editor
should be told proactively that the two papers exist, what they share, and why
they are two papers rather than one.

## 1. Shared benchmark infrastructure

- The projects share the public candidate generator, RTS-GMLC/SimBench/NERC
  source inputs, common benchmark execution and evaluation utilities, and
  public-record backtest infrastructure and source records.
- The p5 and p6 configurations, mechanism-specific operators, executions, run
  outputs, selected portfolios, statistical comparisons, and claims are
  paper-specific. Shared infrastructure is disclosed and is not presented as
  either paper's independent contribution.
- Text overlap remains to be assessed by the planned iThenticate self-check.

## 2. How the two manuscripts differ

| Axis | TRACE-MOEA (this paper, p5) | BiLo-NSGA (companion, p6) |
|---|---|---|
| Mechanism stage | Selection and repair: adaptive preference elitism, deterministic budget repair, quarantined run-level event co-occurrence summaries | Variation: bidirectional local search — forward insertion under budget slack, deletion of weak selections, dependency-aware move bonuses |
| Problem formulation | Five objectives (adds compliance-and-evidence quality) | Four objectives |
| Scenario axes | Review preferences (reliability, renewable, traceability, preference emphasis) | Budget multipliers and pool scaling |
| External validation | Paper-specific NERC and MTEP16 checks, interpreted descriptively | Companion-specific scope; confirm from its evidence package before describing it in the letter |
| Research question | How does constrained five-objective search behave with adaptive preference elitism, deterministic repair, and run-level event co-occurrence summaries? | How far can budget-vocabulary local moves extend portfolio quality under hard budget scans? |

## 3. Candidate budget-response contrast (companion verification required)

The p5 evidence below is available in this worktree. The cited p6 output is not,
so its numerical values and interpretation must be checked in
`mintou_p6_bilonsga_project_review` before they enter a cover letter. If that
check succeeds, the opposite budget responses can help distinguish the study
questions; they do not constitute a joint component ablation.

- **TRACE-MOEA's margin over NSGA-II GROWS under a tight budget.** At 0.75x the
  baseline budget, TRACE-MOEA reaches mean HV 0.16606 vs. NSGA-II 0.16378, a
  +1.39% margin, larger than the +0.89% pooled margin at the standard envelope
  (evidence: `papers/mintou/mintou_p5_trace_moea_feasibility_review/evidence/tables/real_budget_sensitivity_075x.csv`
  and `..._significance.csv`, 15 methods x 30 seeds). The larger margin is
  consistent with a tight-budget role for the full p5 configuration, but this
  comparison does not isolate deterministic repair.

- **BiLo-NSGA's margin over NSGA-II SHRINKS to nothing under the same tightening.**
  In the companion study's 0.75x budget_sensitivity scenario, BiLo-NSGA scores
  mean HV 0.16013 vs. NSGA-II 0.16067 — a -0.33% (not significant, Holm p = 1.0,
  raw p = 0.67) margin (evidence:
  `papers/mintou/mintou_p6_bilonsga_project_review/evidence/tables/real_project_review_significance.csv`,
  budget_sensitivity row). This full-method contrast does not isolate the local
  insertion operator and remains unavailable for verification in this worktree.

If the companion values are verified, one budget perturbation produces opposite
full-method responses. That pattern is descriptive evidence that the papers ask
different mechanism questions. It is not evidence that repair alone causes the
p5 response or that insertion alone causes the p6 response.

## 4. Practical points for the letter

- State the companion submission openly, cite it (ref [28]) and offer to share
  the companion manuscript with the editor/reviewers on request.
- Note the shared-infrastructure declaration in both Data Availability
  statements and the planned iThenticate cross-check. Do not state an overlap
  result until the check has been run.
- Describe the release status of each evidence package only after checking its
  submission-time repository or archive record.
- Suggested reviewers may overlap; flag this so the editor can decide whether
  to use the same or disjoint reviewer pools.
