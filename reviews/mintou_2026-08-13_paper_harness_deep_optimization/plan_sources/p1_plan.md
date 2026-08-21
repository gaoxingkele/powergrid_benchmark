---
stages:
  - id: p1_s1_claim_contract
    title: P1 headline-to-table repair and evidence contract
    objective: "Create manuscript/DEEP_REVISION_EVIDENCE.md, correct the 24-hour MAE leader contradiction, define one conservative paper story, and map every title and contribution term to methods, direct evidence, negative results, and human blockers without inventing facts. Preserve the distinction between SmallBank's lowest 24-hour MAE with zero event F1, raw-kNN as the strongest non-degenerate 24-hour MAE reference, and Persistence's 1-hour result."
    acceptance:
      - narrative_structure
      - manuscript_hygiene
      - "custom:../../scripts/mintou/harness_scientific_acceptance.py --project mintou_p1_dstar_gru_dispatch --phase narrative"
  - id: p1_s2_task_method
    title: P1 information gate, method name, and reproducibility contract
    objective: "Define forecast issue time, delivery time, data vintage, and information available to every method; decide from the actual assets whether the paper is an operational day-ahead task or retrospective lag forecasting and narrow title and application language accordingly. Replace unsupported digital-twin or Siamese expansion terms unless directly operationalized. Reconcile v5/v6 provenance and publish a table-to-config manifest."
    acceptance:
      - narrative_structure
      - artifact_consistency
      - manuscript_hygiene
      - "custom:../../scripts/mintou/harness_scientific_acceptance.py --project mintou_p1_dstar_gru_dispatch --phase narrative"
  - id: p1_s3_fair_experiments
    title: P1 fair-data and retrieval-mechanism experiments
    objective: "Run evidence-preserving experiments in a new run namespace. Give Ridge and learned methods a symmetric fit, selection, and threshold-calibration information gate. Add the direct policy-transform control if target-hour forecasts exist; otherwise document its inapplicability. Cross retrieval presence with a target-matched selection objective and fixed blend controls, make paired-seed analysis primary, and add method-level cap sensitivity only where the existing data support it. Never overwrite prior runs or remove adverse results."
    acceptance:
      - "custom:../../scripts/mintou/harness_scientific_acceptance.py --project mintou_p1_dstar_gru_dispatch --phase evidence"
  - id: p1_s4_results_narrative
    title: P1 integrate fair results and rebuild the paper
    objective: "Regenerate tables and figures from the new run manifest, rewrite Results by research question and evidential importance, retain metric-specific and horizon-specific negative results in Abstract, Results, Discussion, and Conclusion, and limit inference to the stated temporal units. Keep runtime, version history, and exhaustive audit detail in the supplement."
    acceptance:
      - narrative_structure
      - artifact_consistency
      - manuscript_hygiene
      - "custom:../../scripts/mintou/harness_scientific_acceptance.py --project mintou_p1_dstar_gru_dispatch --phase full"
      - "custom:../../scripts/mintou/harness_acceptance.py --project mintou_p1_dstar_gru_dispatch --allow-human-placeholders"
  - id: p1_s5_three_round_closure
    title: P1 three-round scientific closure
    objective: "Perform sequential logic, methodology-statistics, and theory-innovation adversarial passes against the current evidence matrix; fix every supported major issue, mark unavailable external checks as unverified, and leave authorship, correspondence, funding, and biographies as explicit human blockers. Do not manufacture SOTA, expert review, or broader system generalization."
    acceptance:
      - narrative_structure
      - artifact_consistency
      - pdf_integrity
      - manuscript_hygiene
      - "custom:../../scripts/mintou/harness_scientific_acceptance.py --project mintou_p1_dstar_gru_dispatch --phase full"
      - "custom:../../scripts/mintou/harness_acceptance.py --project mintou_p1_dstar_gru_dispatch --allow-human-placeholders"
  - id: p1_s6_human_submission_gate
    title: P1 author-confirmed submission closure
    objective: "After the authors provide verified names, affiliations, correspondence, CRediT roles, funding, APC statement, and IEEE biographies, insert only those confirmed facts and produce the final IEEE Access package. If any item is absent, stop as BLOCKED rather than guessing."
    acceptance:
      - latex_build
      - no_placeholders
      - declarations
      - artifact_consistency
      - pdf_integrity
      - "custom:../../scripts/mintou/harness_acceptance.py --project mintou_p1_dstar_gru_dispatch"
---

# P1 deep-optimization evidence boundary

Primary question: under a fixed-policy curtailment-risk proxy, what does learned operating-state retrieval add at 1 h and 24 h when data visibility and selection objectives are fair?

This plan does not license operational scheduling utility, general cross-system robustness, or a claim that retrieval is universally beneficial or harmful. New runs use new directories and preserve all failed, adverse, and superseded results.
