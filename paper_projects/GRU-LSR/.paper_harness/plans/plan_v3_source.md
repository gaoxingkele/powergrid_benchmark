---
stages:
  - id: p1v3_s1_upgrade_contract
    title: Repair and freeze the IEEE Access upgrade contract
    objective: >-
      Replace the rejected v2 contract candidate with a prospectively frozen
      manuscript/P1_IEEE_ACCESS_UPGRADE_CONTRACT.md and deterministic
      experiments/p1_ieee_access_upgrade_v2/validate_upgrade.py. In addition to
      the existing claim/evidence maps, the normative contract must explicitly
      freeze DLinear, LSTM, and TCN architectures, training budgets, checkpoint
      and selection rules, common visibility, failure handling, and their role
      relative to Persistence, Seasonal-24h, Ridge, and the GRU paths. Freeze the
      raw-window and randomized-encoder retrieval controls and k=4/8/16/32 grid.
      Add a machine-checked IEEE Access clear-advance gate whose final literature
      support remains provisional until stage 4. Preserve all known negative,
      null, onset-inapplicable, single-sequence, proxy-target, and non-operational
      boundaries. Do not inspect any new v2 test result and do not alter human
      metadata.
    acceptance:
      - narrative_structure
      - manuscript_hygiene
      - "custom:experiments/p1_ieee_access_upgrade_v2/validate_upgrade.py --phase contract"
      - "custom:../../scripts/mintou/harness_scientific_acceptance.py --project mintou_p1_dstar_gru_dispatch --phase narrative"

  - id: p1v3_s2_fair_baselines_attribution
    title: Run modern fair baselines and learned-space attribution controls
    objective: >-
      Execute a new immutable run namespace without overwriting p1_s3_fair_v1.
      Reuse the frozen source hashes, 48-row seven-feature input,
      50/10/10/30 fit-selection-calibration-test gate, 1 h and 24 h retrospective
      lags, caps 0.60/0.70/0.80, and ten common seeds. Run the contract-frozen
      DLinear, LSTM, and TCN comparators; raw-feature kNN; randomized/frozen-GRU
      retrieval; trained-GRU retrieval; and k=4/8/16/32 sensitivity. Keep the
      privileged direct transform outside forecasting rankings. Record every
      method-seed-cap-lag row, configuration, source/script hash, environment,
      failure, and adverse result. A comparator that cannot meet the frozen
      visibility and budget rules must be marked inapplicable with a
      machine-readable reason rather than silently dropped.
    acceptance:
      - "custom:experiments/p1_ieee_access_upgrade_v2/validate_upgrade.py --phase experiments"
      - "custom:../../scripts/mintou/harness_scientific_acceptance.py --project mintou_p1_dstar_gru_dispatch --phase evidence"

  - id: p1v3_s3_statistics_robustness
    title: Rebuild the inferential family and robustness diagnostics
    objective: >-
      Derive all paper-facing tables from the frozen v2 manifest. Keep paired
      seed-run differences as the primary stochastic analysis, report effect
      sizes and uncertainty intervals, and apply the predeclared within-question
      multiplicity correction. Treat deterministic baselines and cross-cap
      results as descriptive. Add a predeclared moving-block resampling
      sensitivity for temporal dependence without implying cross-year or
      cross-system generalization. Permit learned-space language only when the
      trained retrieval path is distinguished from both raw-feature and
      randomized controls under the frozen family; otherwise narrow the claim
      and title to retrieval-path evaluation. Preserve onset inapplicability.
    acceptance:
      - "custom:experiments/p1_ieee_access_upgrade_v2/validate_upgrade.py --phase statistics"
      - "custom:../../scripts/mintou/harness_scientific_acceptance.py --project mintou_p1_dstar_gru_dispatch --phase evidence"

  - id: p1v3_s4_literature_integrity
    title: Refresh the state-of-the-art boundary and verify every citation
    objective: >-
      Produce manuscript/P1_CITATION_VERIFICATION_V2.md and
      manuscript/P1_LITERATURE_GAP_V2.md. Verify title, authors, venue, year,
      DOI/stable URL, retraction status, and claim-level support for every
      reference. Search the approved local literature stores and verifiable
      primary publisher records for directly relevant 2025-2026 work on
      curtailment/SNSP forecasting, analogue or learned retrieval, and
      reproducible time-series benchmarking. Add sources only after content-level
      verification; mark insufficient evidence as 待核实 and exclude it from
      publication-facing claims. Convert the provisional clear-advance gate into
      a bounded evidence-backed comparison, never a global novelty claim.
    acceptance:
      - narrative_structure
      - manuscript_hygiene
      - "custom:experiments/p1_ieee_access_upgrade_v2/validate_upgrade.py --phase references"
      - "custom:../../scripts/mintou/harness_scientific_acceptance.py --project mintou_p1_dstar_gru_dispatch --phase narrative"

  - id: p1v3_s5_manuscript_figures
    title: Integrate the upgraded evidence into the IEEE Access manuscript
    objective: >-
      Rebuild MANUSCRIPT.md and the official IEEE Access LaTeX from accepted
      evidence only. Center the auditable benchmark and use retrieval as the
      matched empirical study. Keep three explicit RQs and a direct
      gap-to-contribution-to-result map. Reduce abstract density while retaining
      Persistence ordering, onset inapplicability, and non-operational scope.
      Regenerate all result tables and figures from manifest-bound generators;
      improve annotation size, remove redundant decoration and duplicated
      payload, and keep floats near first citation. Preserve explicit human
      placeholders and never invent authors, affiliations, funding, CRediT,
      conflicts, ethics facts, DOI, ORCID, or biographies.
    acceptance:
      - narrative_structure
      - artifact_consistency
      - manuscript_hygiene
      - pdf_integrity
      - "custom:experiments/p1_ieee_access_upgrade_v2/validate_upgrade.py --phase manuscript"
      - "custom:../../scripts/mintou/harness_scientific_acceptance.py --project mintou_p1_dstar_gru_dispatch --phase full"
      - "custom:../../scripts/mintou/harness_acceptance.py --project mintou_p1_dstar_gru_dispatch --allow-human-placeholders"

  - id: p1v3_s6_independent_closure
    title: Independently reproduce and adversarially close the scientific package
    objective: >-
      Rerun the complete v2 experiment in a separate verification namespace and
      require equality of all non-timing scientific fields and derived tables.
      Document every divergence and stop on unexplained mismatch. Perform
      sequential logic, methodology-statistics, and IEEE Access presentation
      passes over the exact manuscript and evidence. Rebuild the source/PDF pair,
      verify labels, citations, figures, tables, readable text and float order,
      and keep the pre-biography paper below the journal-recommended 20 pages.
      Produce the complete package and submission gate while retaining
      not-ready status for unresolved author fields or persistent release URL.
    acceptance:
      - latex_build
      - artifact_consistency
      - pdf_integrity
      - manuscript_hygiene
      - "custom:experiments/p1_ieee_access_upgrade_v2/validate_upgrade.py --phase full"
      - "custom:../../scripts/mintou/harness_scientific_acceptance.py --project mintou_p1_dstar_gru_dispatch --phase full"
      - "custom:../../scripts/mintou/harness_acceptance.py --project mintou_p1_dstar_gru_dispatch --allow-human-placeholders"

  - id: p1v3_s7_human_submission_gate
    title: Close author declarations and produce the upload-ready package
    objective: >-
      Insert only author-approved author order, affiliations, correspondence,
      CRediT roles, funding/no-funding, acknowledgments, AI disclosure, ethics,
      conflicts, biographies, photographs, APC responsibility, and persistent
      code/data release URL or DOI. Record that the submitting IEEE account has
      a public populated ORCID even if the manuscript prints NONE. Rebuild the
      exact matching LaTeX/PDF and supplement, then create the upload checklist
      and cover letter. Remain BLOCKED if any human-controlled item is absent or
      inconsistent.
    acceptance:
      - latex_build
      - no_placeholders
      - declarations
      - artifact_consistency
      - pdf_integrity
      - manuscript_hygiene
      - "custom:experiments/p1_ieee_access_upgrade_v2/validate_upgrade.py --phase submission"
      - "custom:../../scripts/mintou/harness_acceptance.py --project mintou_p1_dstar_gru_dispatch"
---

# P1 IEEE Access upgrade plan v3

## Reason for superseding v2

The first v2 stage candidate was rejected in reviewer loop 1 of 5 because its
contract did not freeze the planned DLinear, LSTM, and TCN comparator budgets or
machine-check the current IEEE Access clear-advance requirement. The executor
logs and rejection event remain immutable historical evidence.

## Non-negotiable evidence boundary

- No v2 test result may be inspected before the repaired contract is accepted.
- Existing negative and null findings remain visible in every downstream layer.
- Training seeds quantify algorithmic variability only.
- Cross-cap, deterministic-baseline, and single-sequence results do not license
  system, year, operator, policy, operational, dispatch, economic, or deployment
  generalization.
- Literature support must come from approved local stores or verifiable primary
  records; insufficient evidence is 待核实.
- Scientific stages may proceed after valid negative results, but not after
  protocol failure, unexplained reproduction mismatch, or unsupported claims.
- Human author and submission metadata remain a final blocking gate.
