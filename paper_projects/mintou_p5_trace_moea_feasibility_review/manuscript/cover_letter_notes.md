# Cover Letter Notes: Companion-Submission Strategy (TRACE-MOEA, mintou_p5)

Notes for drafting the cover letter to the MDPI Energies editor. This manuscript
(TRACE-MOEA) is submitted alongside a companion study (BiLo-NSGA, mintou_p6,
cited as ref [28], "companion paper, submitted"). The editor should be told
proactively that the two papers exist, what they share, and why they are two
papers rather than one.

## 1. What the two manuscripts share — and the only thing they share

- A single versioned candidate-generation pipeline that derives a public,
  reproducible pool of grid investment candidates from RTS-GMLC, SimBench, and
  NERC reliability-report metadata. This sharing is declared explicitly in the
  Data Availability statement of both manuscripts.
- Nothing else is shared: no algorithmic operator, no problem formulation, no
  scenario design, no external backtest, and (to be confirmed by an iThenticate
  self-check before submission) no overlapping sentences.

## 2. How the two manuscripts differ

| Axis | TRACE-MOEA (this paper, p5) | BiLo-NSGA (companion, p6) |
|---|---|---|
| Mechanism stage | Selection and archiving: preference-adaptive elitism, deterministic budget repair, quarantined decision trace archive | Variation: bidirectional local search — forward insertion under budget slack, deletion of weak selections, dependency-aware move bonuses |
| Problem formulation | Five objectives (adds compliance-and-evidence quality) | Four objectives |
| Scenario axes | Review preferences (reliability, renewable, traceability, preference emphasis) | Budget multipliers and pool scaling |
| External validation | Two-rung external-validity ladder (NERC rule backtest + MISO MTEP16 real built/withdrawn outcomes) | None (internal benchmark only) |
| Research question | Can search produce review-grade, auditable justification material at no metric cost? | How far can budget-vocabulary local moves extend portfolio quality under hard budget scans? |

## 3. The 0.75x budget reversal: hard evidence that the mechanisms are distinct

The strongest argument that the two papers validate different mechanisms —
rather than describing one method twice — is that the same budget perturbation
moves their results in opposite directions:

- **TRACE-MOEA's margin over NSGA-II GROWS under a tight budget.** At 0.75x the
  baseline budget, TRACE-MOEA reaches mean HV 0.16606 vs. NSGA-II 0.16378, a
  +1.39% margin, larger than the +0.89% pooled margin at the standard envelope
  (evidence: `papers/mintou/mintou_p5_trace_moea_feasibility_review/evidence/tables/real_budget_sensitivity_075x.csv`
  and `..._significance.csv`, 15 methods x 30 seeds). Mechanistic reading: the
  deterministic repair operator is most valuable exactly when the budget
  constraint binds hardest.

- **BiLo-NSGA's margin over NSGA-II SHRINKS to nothing under the same tightening.**
  In the companion study's 0.75x budget_sensitivity scenario, BiLo-NSGA scores
  mean HV 0.16013 vs. NSGA-II 0.16067 — a -0.33% (not significant, Holm p = 1.0,
  raw p = 0.67) margin (evidence:
  `papers/mintou/mintou_p6_bilonsga_project_review/evidence/tables/real_project_review_significance.csv`,
  budget_sensitivity row). Mechanistic reading: forward insertion moves need
  budget slack to operate; when the envelope tightens, the insertion vocabulary
  starves.

One knob, two opposite responses: repair-based selection machinery thrives
under scarcity while insertion-based variation machinery requires slack. The
two papers therefore probe complementary regions of the design space, and each
result set would be unpublishable as a subsection of the other without losing
its evidential meaning.

## 4. Practical points for the letter

- State the companion submission openly, cite it (ref [28]) and offer to share
  the companion manuscript with the editor/reviewers on request.
- Note the shared-pipeline declaration in both Data Availability statements and
  the planned iThenticate cross-check (zero overlapping sentences).
- Both evidence packages are released in full, including deprecated pipeline
  revisions retained for transparency (explained in Section 8 of this
  manuscript).
- Suggested reviewers may overlap; flag this so the editor can decide whether
  to use the same or disjoint reviewer pools.
