---
stages:
  - id: p6_s1_claim_contract
    title: P6 local-search and audit evidence contract
    objective: "Create manuscript/DEEP_REVISION_EVIDENCE.md; align the title and contribution terms with budget-aware local moves and the actual accepted-move log. Name companion project mintou_p5_trace_moea_feasibility_review, disclose shared benchmark assets, and isolate BiLo-NSGA's local-search question without forward-dominant, synergy, audit, or recommendation-path overclaim."
    acceptance:
      - narrative_structure
      - manuscript_hygiene
      - "custom:../../scripts/mintou/harness_scientific_acceptance.py --project mintou_p6_bilonsga_project_review --phase narrative"
  - id: p6_s2_method_contract
    title: P6 violation, local move, and trace specification
    objective: "Reconcile the violation equation, lambda, scenario weights, b_jq normalization, initialization, offspring selection, local-search normalization, tie rules, baseline constraint handling, and counters across equations, pseudocode, config, and code. Narrow dependency claims to a heuristic group bonus unless a dependency benefit or constraint is operationalized; narrow trace to accepted-local-move logging unless lineage and replay are implemented."
    acceptance:
      - narrative_structure
      - artifact_consistency
      - manuscript_hygiene
      - "custom:../../scripts/mintou/harness_scientific_acceptance.py --project mintou_p6_bilonsga_project_review --phase narrative"
  - id: p6_s3_matched_effort
    title: P6 matched-evaluation and matched-time experiments
    objective: "Run new immutable comparisons of BiLo-NSGA, NSGA-II, and Pareto Local Search at identical total objective plus local-proposal evaluation budgets and, where feasible, identical wall-clock budgets on the same scenarios. Report per-run feasible-front hypervolume, runtime, and feasibility with a declared multiplicity family. Add hypervolume-bound, clipping, reference-point, and compact local-search parameter sensitivity. Shared code changes must regress P5 without changing P5 evidence."
    acceptance:
      - "custom:../../scripts/mintou/harness_scientific_acceptance.py --project mintou_p6_bilonsga_project_review --phase evidence"
  - id: p6_s4_results_narrative
    title: P6 integrate quality-compute tradeoff and mechanism limits
    objective: "Regenerate all tables and figures from the new manifest. Present the 1.12-percent existing gain as a quality-compute tradeoff unless matched-effort evidence changes the conclusion, retain the 2.74-times runtime cost and unresolved substitution effect, report forward insertion only in the scenarios where it resolves, and move file lineage out of the main text."
    acceptance:
      - narrative_structure
      - artifact_consistency
      - manuscript_hygiene
      - "custom:../../scripts/mintou/harness_scientific_acceptance.py --project mintou_p6_bilonsga_project_review --phase full"
      - "custom:../../scripts/mintou/harness_acceptance.py --project mintou_p6_bilonsga_project_review --allow-human-placeholders"
  - id: p6_s5_three_round_closure
    title: P6 three-round scientific closure
    objective: "Perform logic, methodology-statistics, and theory-innovation reviews. Close compute-fairness, equation-code, interaction, trace, hypervolume, baseline-feasibility, companion-overlap, and visual-consistency issues with observable evidence. Do not use SOTA or deployment language."
    acceptance:
      - narrative_structure
      - artifact_consistency
      - pdf_integrity
      - manuscript_hygiene
      - "custom:../../scripts/mintou/harness_scientific_acceptance.py --project mintou_p6_bilonsga_project_review --phase full"
      - "custom:../../scripts/mintou/harness_acceptance.py --project mintou_p6_bilonsga_project_review --allow-human-placeholders"
  - id: p6_s6_human_submission_gate
    title: P6 author-confirmed submission closure
    objective: "Insert only verified CRediT, funding, APC, correspondence, rights, and repository facts, validate references, and compile the final Applied Sciences package. Missing confirmations remain BLOCKED."
    acceptance:
      - latex_build
      - no_placeholders
      - declarations
      - artifact_consistency
      - pdf_integrity
      - "custom:../../scripts/mintou/harness_acceptance.py --project mintou_p6_bilonsga_project_review"
---

# P6 deep-optimization evidence boundary

The current result is a modest proxy-quality gain bought with extra local evaluations and runtime. Only matched-effort experiments can license a performance advantage independent of compute; logging alone cannot license audit or recommendation-path utility.
