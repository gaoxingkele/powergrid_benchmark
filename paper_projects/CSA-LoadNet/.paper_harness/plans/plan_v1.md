---
stages:
  - id: p2_s1_claim_contract
    title: P2 title-task-component evidence contract
    objective: "Create manuscript/DEEP_REVISION_EVIDENCE.md and stabilize the scientific story around cross-series aggregation rather than unsupported weighting or curvature superiority. Map the title, contributions, metrics, data visibility, negative results, and unresolved author or funding fields to observable evidence."
    acceptance:
      - narrative_structure
      - manuscript_hygiene
      - "custom:../../scripts/mintou/harness_scientific_acceptance.py --project mintou_p2_hygraph_load_forecasting --phase narrative"
  - id: p2_s2_method_data_contract
    title: P2 forecasting and geometry specification
    objective: "Rename c_i as a temperature or distance-scale parameter unless an actual curvature-dependent metric is implemented; define the prediction target as 24-hour-ahead point forecasting or add a true next-day-trajectory task before using day-ahead language. Fully specify reconciliation, aggregation, model capacities, data cleaning, timestamps, time zones, daylight-saving handling, missingness, aggregation labels, and train-only filters."
    acceptance:
      - narrative_structure
      - artifact_consistency
      - manuscript_hygiene
      - "custom:../../scripts/mintou/harness_scientific_acceptance.py --project mintou_p2_hygraph_load_forecasting --phase narrative"
  - id: p2_s3_identifiable_experiments
    title: P2 capacity-matched and temporally replicated controls
    objective: "Run a new, immutable experiment namespace with an informative cross-series context control matched for head, parameters, optimization, seeds, and compute, plus a shared-versus-independent encoder control only if the manuscript retains that claim. Equalize baseline seed support or narrow confirmatory comparisons, use rolling temporal origins with forecast day or origin as the outer analysis unit, report at least two suitable metrics, and retain weighting-form null results."
    acceptance:
      - "custom:../../scripts/mintou/harness_scientific_acceptance.py --project mintou_p2_hygraph_load_forecasting --phase evidence"
  - id: p2_s4_results_narrative
    title: P2 integrate controls, uncertainty, and exact-hierarchy boundary
    objective: "Regenerate current ranks, percentage denominators, reconciliation results, figures, and tables from the accepted run manifest. Lead with the fixed-split and rolling-origin findings, state that seed variation is conditional on each split, retain the DLinear exact-hierarchy advantage and tested-weighting null result, and remove stale labels or release chronology from the main story."
    acceptance:
      - narrative_structure
      - artifact_consistency
      - manuscript_hygiene
      - "custom:../../scripts/mintou/harness_scientific_acceptance.py --project mintou_p2_hygraph_load_forecasting --phase full"
      - "custom:../../scripts/mintou/harness_acceptance.py --project mintou_p2_hygraph_load_forecasting --allow-human-placeholders"
  - id: p2_s5_three_round_closure
    title: P2 three-round scientific closure
    objective: "Conduct logic, methodology-statistics, and theory-innovation adversarial passes. Close combined-ablation, temporal-unit, data-audit, baseline-fairness, and term-definition issues with evidence; keep unavailable bibliography or artifact checks marked unverified and human metadata blocked."
    acceptance:
      - narrative_structure
      - artifact_consistency
      - pdf_integrity
      - manuscript_hygiene
      - "custom:../../scripts/mintou/harness_scientific_acceptance.py --project mintou_p2_hygraph_load_forecasting --phase full"
      - "custom:../../scripts/mintou/harness_acceptance.py --project mintou_p2_hygraph_load_forecasting --allow-human-placeholders"
  - id: p2_s6_human_submission_gate
    title: P2 author-confirmed submission closure
    objective: "Insert only author-confirmed CRediT, funding, APC, correspondence, and repository-release facts, validate references and persistent links, and build the final Electronics package. Missing confirmations remain BLOCKED."
    acceptance:
      - latex_build
      - no_placeholders
      - declarations
      - artifact_consistency
      - pdf_integrity
      - "custom:../../scripts/mintou/harness_acceptance.py --project mintou_p2_hygraph_load_forecasting"
---

# P2 deep-optimization evidence boundary

The target is identifiable evidence for cross-series aggregation and the limits of weighting geometry. It is not a plan to tune against the test set or to turn a 24-hour point forecast into a true day-ahead trajectory claim without a matching experiment.
