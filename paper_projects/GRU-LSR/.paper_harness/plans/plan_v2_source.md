---
stages:
  - id: p1v2_s1_upgrade_contract
    title: Freeze the IEEE Access upgrade contract and decision rules
    objective: >-
      Create manuscript/P1_IEEE_ACCESS_UPGRADE_CONTRACT.md and a deterministic
      experiments/p1_ieee_access_upgrade_v2/validate_upgrade.py gate. Freeze the
      primary contribution as a reproducible retrospective benchmark plus a
      matched retrieval-path evaluation; map every title, abstract, contribution,
      RQ, figure, table, and conclusion claim to existing or planned evidence.
      Predeclare the expanded methods, common seeds, temporal partitions,
      hyperparameter budgets, inferential families, effect-size reporting, and
      stop/go wording rules before any new test result is inspected. Preserve the
      current Persistence advantage, zero pre-test onset support, non-operational
      scope, and all adverse or null findings. Do not alter author-controlled
      metadata and do not turn the old blocked human gate into a scientific claim.
    acceptance:
      - narrative_structure
      - manuscript_hygiene
      - "custom:experiments/p1_ieee_access_upgrade_v2/validate_upgrade.py --phase contract"
      - "custom:../../scripts/mintou/harness_scientific_acceptance.py --project mintou_p1_dstar_gru_dispatch --phase narrative"

  - id: p1v2_s2_fair_baselines_attribution
    title: Run modern fair baselines and learned-space attribution controls
    objective: >-
      Execute a new immutable run namespace without overwriting p1_s3_fair_v1.
      Reuse the frozen RTS-GMLC source hashes, 48-row seven-feature input,
      50/10/10/30 fit-selection-calibration-test gate, 1 h and 24 h retrospective
      lags, caps 0.60/0.70/0.80, and ten common seeds. Add DLinear, LSTM, and TCN
      under the same fit and selection visibility; add raw-feature kNN and a
      randomized/frozen-encoder retrieval control using the same fit-only target
      bank; and run a predeclared k sensitivity grid of 4, 8, 16, and 32. Keep the
      privileged direct transform outside the forecasting ranking. Record every
      method-seed-cap-lag row, configuration, source/script hashes, runtime
      environment, failures, and adverse results. If a planned comparator cannot
      be made information- and budget-comparable, mark it inapplicable with a
      machine-readable reason instead of silently dropping it.
    acceptance:
      - "custom:experiments/p1_ieee_access_upgrade_v2/validate_upgrade.py --phase experiments"
      - "custom:../../scripts/mintou/harness_scientific_acceptance.py --project mintou_p1_dstar_gru_dispatch --phase evidence"

  - id: p1v2_s3_statistics_robustness
    title: Rebuild the inferential family and robustness diagnostics
    objective: >-
      Derive all paper-facing tables from the new frozen manifest. Keep paired
      seed-run differences as the primary stochastic analysis, report effect
      sizes and uncertainty intervals, and apply the predeclared within-question
      multiplicity correction. Treat deterministic baseline comparisons and all
      cross-cap results as descriptive unless a valid analysis unit was frozen in
      stage 1. Add time-dependence sensitivity with predeclared moving-block
      resampling as a supplementary conditional check, not as evidence of
      cross-year or cross-system generalization. Make the learned-space wording
      conditional: causal or attribution language is permitted only if the
      learned-space path is distinguished from both raw-feature and randomized
      controls under the frozen family; otherwise require a retrieval-path-only
      interpretation and, if necessary, a narrower title. Preserve onset
      inapplicability when selection or calibration support remains zero.
    acceptance:
      - "custom:experiments/p1_ieee_access_upgrade_v2/validate_upgrade.py --phase statistics"
      - "custom:../../scripts/mintou/harness_scientific_acceptance.py --project mintou_p1_dstar_gru_dispatch --phase evidence"

  - id: p1v2_s4_literature_integrity
    title: Refresh the state-of-the-art boundary and verify every citation
    objective: >-
      Produce manuscript/P1_CITATION_VERIFICATION_V2.md and
      manuscript/P1_LITERATURE_GAP_V2.md. Verify the title, authors, venue, year,
      DOI or stable URL, retraction status, and claim-level support for every
      existing reference. Search only the author-approved local literature
      stores and verifiable primary publisher records for directly relevant
      2025-2026 work on curtailment/SNSP forecasting, analogue retrieval, learned
      retrieval, and reproducible time-series benchmarking. Add a source only
      after content-level verification; mark insufficient evidence as 待核实 in
      the ledger and keep it out of publication-facing claims. Rewrite G1/G2 as
      bounded advances over the verified corpus, not proof of global novelty or
      an exhaustive state-of-the-art exclusion.
    acceptance:
      - narrative_structure
      - manuscript_hygiene
      - "custom:experiments/p1_ieee_access_upgrade_v2/validate_upgrade.py --phase references"
      - "custom:../../scripts/mintou/harness_scientific_acceptance.py --project mintou_p1_dstar_gru_dispatch --phase narrative"

  - id: p1v2_s5_manuscript_figures
    title: Integrate the upgraded evidence into the IEEE Access manuscript
    objective: >-
      Rebuild MANUSCRIPT.md and the official IEEE Access LaTeX from the accepted
      evidence only. Make the benchmark the narrative center and the retrieval
      study its matched empirical use case. Keep three explicit RQs and a direct
      gap-to-contribution-to-result map. Reduce abstract density while retaining
      the Persistence comparison, onset inapplicability, and non-operational
      boundary; avoid unnecessary eight-decimal reporting in prose. Update all
      result tables and figures from manifest-bound generators, enlarge small
      annotations, remove redundant decorative section rules, reduce duplicate
      table/figure payload, and keep floats near first citation. Do not add
      unverified authors, affiliations, funding, CRediT roles, conflicts, ethics
      text, repository DOI, ORCID, or biographies. Preserve explicit placeholders
      for the final human stage.
    acceptance:
      - narrative_structure
      - artifact_consistency
      - manuscript_hygiene
      - pdf_integrity
      - "custom:experiments/p1_ieee_access_upgrade_v2/validate_upgrade.py --phase manuscript"
      - "custom:../../scripts/mintou/harness_scientific_acceptance.py --project mintou_p1_dstar_gru_dispatch --phase full"
      - "custom:../../scripts/mintou/harness_acceptance.py --project mintou_p1_dstar_gru_dispatch --allow-human-placeholders"

  - id: p1v2_s6_independent_closure
    title: Independently reproduce and adversarially close the scientific package
    objective: >-
      Rerun the complete upgraded experiment from the frozen script,
      configuration, inputs, and seed list in a separate verification namespace.
      Require equality of all non-timing scientific fields and derived tables, or
      document every divergence and stop. Perform sequential logic,
      methodology-statistics, and IEEE Access presentation passes over the exact
      current manuscript and evidence. Rebuild the source/PDF pair, verify all
      labels, citations, figures, tables, readable text, float ordering, and a
      target length below the journal's recommended 20 pages before biographies.
      Generate an updated complete package and submission gate, but keep status
      not-ready while any author-controlled field or persistent release URL is
      unresolved.
    acceptance:
      - latex_build
      - artifact_consistency
      - pdf_integrity
      - manuscript_hygiene
      - "custom:experiments/p1_ieee_access_upgrade_v2/validate_upgrade.py --phase full"
      - "custom:../../scripts/mintou/harness_scientific_acceptance.py --project mintou_p1_dstar_gru_dispatch --phase full"
      - "custom:../../scripts/mintou/harness_acceptance.py --project mintou_p1_dstar_gru_dispatch --allow-human-placeholders"

  - id: p1v2_s7_human_submission_gate
    title: Close author declarations and produce the upload-ready package
    objective: >-
      After the authors provide and approve the final author order, affiliations,
      corresponding-author details, CRediT roles, funding or no-funding statement,
      acknowledgments, generative-AI disclosure, ethics wording, conflicts of
      interest, short biographies, photographs, APC responsibility, and a
      persistent code/data release URL or DOI, insert only the confirmed facts.
      Record that the submitting IEEE account has the required public populated
      ORCID even if ORCID is omitted from the printed manuscript. Rebuild the
      exact matching LaTeX/PDF and final supplement, run all integrity checks, and
      create the upload checklist and cover letter. If any author-controlled item
      is absent or inconsistent, remain BLOCKED rather than guessing.
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

# P1 IEEE Access upgrade plan v2: evidence boundary

## Goal

Upgrade P1 from a technically coherent, twelve-page retrospective benchmark
paper into an IEEE Access submission whose clear advance is the auditable
benchmark and matched evidence chain, while testing rather than assuming that
the learned representation is responsible for the retrieval gain.

## Frozen starting evidence

- The canonical baseline is the latest journal-submission LaTeX and the accepted
  `p1_s3_fair_v1` evidence family.
- Persistence remains lower-MAE than selected GRU-LSR at the primary cap for
  both retrospective lags.
- Selection and calibration contain zero positive onsets at all executed caps
  and lags; onset-targeted utility is not currently estimable.
- Existing cap scans reuse one fixed RTS-GMLC sequence and are descriptive.
- The source files lack forecast issue time and data-vintage identifiers; no
  operational day-ahead claim is licensed.
- The target is a policy-derived proxy, not observed curtailment, OPF/UC output,
  operator action, economic value, or physical-feasibility evidence.

## Predeclared interpretation rules

1. New runs must use a new namespace and must never overwrite, prune, or hide
   prior runs, failed attempts, negative results, or superseded claims.
2. A modern baseline may enter a ranking only when its data visibility,
   selection budget, test rows, and metric definition are comparable.
3. The phrase "learned-space advantage" requires direct evidence against both a
   raw-feature retrieval control and a randomized/frozen-encoder retrieval
   control. Otherwise the allowed claim is only an implemented retrieval-path
   effect relative to the matched head.
4. Statistical significance over training seeds does not imply uncertainty over
   hours, events, years, systems, policies, vintages, or deployments.
5. No test-set result may change the frozen comparison family, preferred cap,
   metric, baseline inclusion rule, or title decision threshold after the fact.
6. If new evidence weakens the current result, Abstract, Results, Discussion,
   Conclusion, figures, tables, and cover letter must all retain that outcome.
7. A second-system check is optional and may only support transport claims when
   its target, information gate, and evaluation units are genuinely comparable;
   zero-event or incompatible data must be reported as inapplicability.

## Stage dependencies and human boundary

- Stages execute strictly in order and each candidate requires human
  accept/reject before the next stage.
- Stage 1 freezes the protocol; Stages 2-3 create and analyze new evidence;
  Stage 4 closes literature integrity; Stage 5 rewrites; Stage 6 independently
  verifies; Stage 7 is author-controlled submission closure.
- This plan does not authorize invention of authors, affiliations, funding,
  citations, experimental results, expert judgments, repository DOIs, or ORCID
  records.
- The old v1 human-gate failure remains historical evidence. Plan v2 supersedes
  the workflow but does not rewrite or erase that event.
