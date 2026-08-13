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

## 1. What the two manuscripts share — and the only thing they share

- A single versioned candidate-generation pipeline that derives a public,
  reproducible pool of 120 grid investment candidates from RTS-GMLC, SimBench,
  and NERC reliability-report metadata. This sharing is declared explicitly in
  Section 3.2 / Section 2.4 and in the Data Availability statement of both
  manuscripts.
- Nothing else is shared: no algorithmic operator, no problem formulation, no
  scenario design, no external backtest design, and (to be confirmed by an
  iThenticate self-check before submission) no overlapping sentences.

## 2. How the two manuscripts differ

| Axis | BiLo-NSGA (this paper, p6) | TRACE-MOEA (companion, p5) |
|---|---|---|
| Mechanism stage | Variation: bidirectional local search — forward insertion under budget slack, backward deletion, dependency-aware move bonuses, feasibility recovery, audit-trail logging | Selection and archiving: preference-adaptive elitism, deterministic budget repair, quarantined decision trace archive |
| Problem formulation | Four objectives; budget as first-class hard constraint | Five objectives (adds compliance-and-evidence quality) |
| Scenario axes | Budget multipliers (0.75x–1.20x) and pool scaling | Review preferences (reliability, renewable, traceability, preference emphasis) |
| External validation | NERC rule backtest + MISO MTEP16 real built/withdrawn outcomes (broad capture 1.084, point-biserial r = 0.105, p = 0.0006) | Two-rung external-validity ladder on the same NERC + MISO MTEP16 anchors, with its own capture statistics |
| Research question | How far can budget-vocabulary local moves extend portfolio quality under hard budget scans? | Can search produce review-grade, auditable justification material at no metric cost? |

## 3. The 0.75x budget reversal: hard evidence that the mechanisms are distinct

The strongest argument that the two papers validate different mechanisms —
rather than describing one method twice — is that the same budget perturbation
moves their results in opposite directions:

- **BiLo-NSGA's margin over NSGA-II SHRINKS to nothing under a tight budget.**
  In this paper's 0.75x budget_sensitivity experiment, BiLo-NSGA scores mean
  HV 0.16013 vs. NSGA-II 0.16067 — a -0.33% margin, not significant (raw
  p = 0.67, Holm p = 1.0). Mechanistic reading: forward insertion converts
  budget slack into projects; when the envelope tightens, the insertion
  vocabulary starves. The margin widens monotonically with headroom, reaching
  +3.40% at the 1.20x envelope. (Evidence:
  `papers/mintou/mintou_p6_bilonsga_project_review/evidence/tables/real_project_review_significance.csv`,
  budget_sensitivity row.)

- **TRACE-MOEA's margin over NSGA-II GROWS under the same tightening.** At
  0.75x, TRACE-MOEA reaches mean HV 0.16606 vs. NSGA-II 0.16378, +1.39%,
  larger than its +0.89% pooled margin at the standard envelope. Mechanistic
  reading: its deterministic repair operator is most valuable exactly when the
  budget constraint binds hardest. (Evidence:
  `papers/mintou/mintou_p5_trace_moea_feasibility_review/evidence/tables/real_budget_sensitivity_075x.csv`
  and `..._significance.csv`, 15 methods x 30 seeds.)

One knob, two opposite responses: insertion-based variation machinery requires
slack while repair-based selection machinery thrives under scarcity. The two
papers therefore probe complementary regions of the design space, and each
result set would be unpublishable as a subsection of the other without losing
its evidential meaning. This paper additionally reports the asymmetry finding
honestly in its own abstract (the backward pass is retained for audit
completeness and substitution semantics, not hypervolume).

## 4. Practical points for the letter

- State the companion submission openly (different journal: Energies), offer
  to share the companion manuscript with the editor/reviewers on request.
- Note the shared-pipeline declaration in both Data Availability statements
  and the planned iThenticate cross-check (target: zero overlapping
  sentences).
- Both evidence packages are released in full, including deprecated pipeline
  revisions retained for transparency.
- Suggested reviewers may overlap; flag this so the editor can decide whether
  to use the same or disjoint reviewer pools.
