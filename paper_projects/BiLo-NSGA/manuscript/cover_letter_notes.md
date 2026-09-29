# Cover Letter Notes: Companion-Submission Strategy (BiLo-NSGA, mintou_p6)

Notes for drafting the cover letter to the MDPI Applied Sciences editor. This
manuscript (BiLo-NSGA) has a companion study (TRACE-MOEA, mintou_p5, targeted
at MDPI Energies, currently in preparation; cited in Section 2.4 as a
companion study). The editor should be told proactively that the two papers
exist, what they share, and why they are two papers rather than one.

These notes are the p6-side mirror of
`mintou_p5_trace_moea_feasibility_review/manuscript/cover_letter_notes.md`;
the differentiation table and evidence pointers are kept consistent between
the two files.

## 1. What the two manuscripts share

- A versioned candidate-generation pipeline that derives a public,
  reproducible pool of 120 grid investment candidates from RTS-GMLC, SimBench,
  and NERC reliability-report metadata. This sharing is declared explicitly in
  Section 3.2 / Section 2.4 and in the Data Availability statement of both
  manuscripts.
- The source corpora, common benchmark/evaluation utilities, and public-record
  backtest infrastructure are also shared. The formulations, method
  configurations, executions, run outputs, selected portfolios, comparisons,
  and claims are paper-specific. Textual independence remains to be confirmed
  by an iThenticate self-check before submission.

## 2. How the two manuscripts differ

| Axis | BiLo-NSGA (this paper, p6) | TRACE-MOEA (companion, p5) |
|---|---|---|
| Mechanism stage | Variation: forward insertion under budget slack, atomic delete--insert substitution, heuristic 1.06 group-label bonus, deterministic feasibility recovery, and accepted-move/repair counters | Selection: preference-adaptive elitism, deterministic budget repair, and run-level event co-occurrence summaries |
| Problem formulation | Four objectives; budget as first-class hard constraint | Five objectives (adds compliance-and-evidence quality) |
| Scenario axes | Budget multipliers (0.75x–1.20x) and pool scaling | Review preferences (reliability, renewable, and preference emphasis) |
| External consistency | P6-specific NERC and MTEP16 analyses; broad MTEP16 capture 1.071 and raw point-biserial r = 0.088 in the flagship scenario, both descriptive | Separate P5 analyses on the same public source families, with paper-specific configurations and results |
| Research question | How do project-vocabulary local moves behave under a hard budget on the proxy benchmark? | How does adaptive preference elitism behave with deterministic repair and separately reported event summaries? |

## 3. Budget-response evidence and its boundary

The two papers ask different mechanism questions, but their budget results are
not a controlled cross-paper experiment. The P6 points change scenario weights
and random streams as well as budget, while the P5 scan has its own formulation
and configuration. The cover letter may report the patterns, but must not call
their contrast a causal validation of mechanism independence.

- **BiLo-NSGA's margin over NSGA-II SHRINKS to nothing under a tight budget.**
  In this paper's 0.75x budget_sensitivity experiment, BiLo-NSGA scores mean
  HV 0.15965 vs. NSGA-II 0.16067 — a -0.64% nominal margin with Holm
  p = 1.0. Forward insertion can use residual slack, so scarcity is a plausible
  explanation, not a demonstrated mechanism. The cross-scenario margin reaches
  +3.30% in the 1.20x large-pool-labeled setting. (Evidence:
  `papers/mintou/mintou_p6_bilonsga_project_review/evidence/tables/real_project_review_significance.csv`,
  budget_sensitivity row.)

- **The companion reports a different budget pattern under its own protocol.**
  The exact P5 values and comparison family should be copied from the approved
  companion manuscript at submission time, rather than inferred from P6.
  Deterministic repair is a plausible explanation for that pattern, not a
  component attribution. (Evidence:
  `papers/mintou/mintou_p5_trace_moea_feasibility_review/evidence/tables/real_budget_sensitivity_075x.csv`
  and `..._significance.csv`, 15 methods x 30 seeds.)

The defensible differentiation rests on the implemented stages, formulations,
configurations, and paper-specific executions, not on an unadjusted comparison
of their effect sizes. This paper reports its asymmetry directly: atomic
substitution is retained as a paired move representation, not as an accuracy,
dependency, audit-completeness, lineage, or replay claim.

## 4. Practical points for the letter

- State the companion submission openly (different journal: Energies), offer
  to share the companion manuscript with the editor/reviewers on request.
- Note the shared-pipeline declaration in both Data Availability statements
  and the planned iThenticate cross-check (target: zero overlapping
  sentences).
- Describe the availability of each evidence package exactly as verified at
  submission. The current P6 run rows contain event count and pool-position
  co-occurrence, not event payloads or replay state.
- Suggested reviewers may overlap; flag this so the editor can decide whether
  to use the same or disjoint reviewer pools.
