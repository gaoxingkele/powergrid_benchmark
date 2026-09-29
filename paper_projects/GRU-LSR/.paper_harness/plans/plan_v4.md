---
stages:
  - id: p1v4_s1_upgrade_contract
    title: Freeze the complete IEEE Access experiment and interpretation contract
    objective: >-
      Produce the prospective contract, normative JSON, and deterministic
      validator without creating or inspecting v2 results. Preserve the existing
      title/abstract/contribution/RQ/figure/table/conclusion evidence maps and all
      negative, null, onset-inapplicable, proxy, single-sequence, and
      non-operational boundaries. Machine-freeze all caps 0.60/0.70/0.80 with
      0.70 primary and cross-cap comparisons descriptive; horizons 1/24 h; ten
      common seeds; exact temporal partitions; GRU, LSTM, DLinear, and TCN
      architectures and common training/checkpoint/selection budgets; Persistence,
      Seasonal-24h, and Ridge roles; learned/raw/randomized retrieval spaces;
      k=4/8/16/32 with k=8 primary; failure handling; complete row expectations;
      paired effect sizes; exact sign-flip and Holm families; a seed-conditional
      uncertainty interval; and a supplementary moving-block analysis with
      explicit loss series, block lengths, repetitions, RNG seeds, and descriptive
      interpretation. Separate protocol validity from effect direction: a valid
      null/adverse result must yield a bounded benchmark contribution, not a
      protocol failure. Learned-space wording requires both named attribution
      controls; architecture-superiority wording is contrast-specific and is not
      a gate for the benchmark contribution. The IEEE Access clear-advance gate
      must require complete valid evidence plus Stage-4 verified literature
      positioning of the auditable benchmark, without requiring every model
      comparison to be favorable. Human metadata remains untouched.
    acceptance:
      - narrative_structure
      - manuscript_hygiene
      - "custom:experiments/p1_ieee_access_upgrade_v2/validate_upgrade.py --phase contract"
      - "custom:../../scripts/mintou/harness_scientific_acceptance.py --project mintou_p1_dstar_gru_dispatch --phase narrative"

  - id: p1v4_s2_fair_baselines_attribution
    title: Execute all frozen caps, modern baselines, and attribution controls
    objective: >-
      In a new immutable namespace, execute every contract-frozen
      method-seed-cap-horizon cell using the hashed RTS-GMLC sources, common
      48-by-7 windows, exact temporal visibility, and fixed budgets. Run GRU,
      LSTM, DLinear, TCN, Persistence, Seasonal-24h, Ridge, learned/raw/randomized
      retrieval at k=4/8/16/32, the selected GRU-LSR path, and the privileged
      construction audit outside the forecast rank. Record configurations,
      source/script hashes, parameter counts, environments, runtimes, selections,
      every metric row, completeness ledger, and all failures/adverse results.
      Fail closed on any missing or incomparable cell.
    acceptance:
      - "custom:experiments/p1_ieee_access_upgrade_v2/validate_upgrade.py --phase experiments"
      - "custom:../../scripts/mintou/harness_scientific_acceptance.py --project mintou_p1_dstar_gru_dispatch --phase evidence"

  - id: p1v4_s3_statistics_robustness
    title: Derive frozen inference, uncertainty, and time-dependence sensitivity
    objective: >-
      Generate paper-facing tables only from the frozen manifest. Report paired
      seed effects, predeclared uncertainty intervals, exact sign-flip tests, and
      within-family Holm adjustments. Run the frozen moving-block sensitivity on
      paired hourly loss differences and label it conditional/descriptive.
      Deterministic references and cross-cap findings remain descriptive. Apply
      the predeclared wording router for learned-space, method-specific,
      null/adverse, Persistence, and onset-inapplicable outcomes without changing
      the protocol after seeing results.
    acceptance:
      - "custom:experiments/p1_ieee_access_upgrade_v2/validate_upgrade.py --phase statistics"
      - "custom:../../scripts/mintou/harness_scientific_acceptance.py --project mintou_p1_dstar_gru_dispatch --phase evidence"

  - id: p1v4_s4_literature_integrity
    title: Verify citations and close the bounded clear-advance literature case
    objective: >-
      Produce P1_CITATION_VERIFICATION_V2.md and P1_LITERATURE_GAP_V2.md. Verify
      every reference's bibliographic identity, DOI/stable URL, retraction status,
      and claim-level support. Search approved local stores and primary publisher
      records for relevant 2025-2026 curtailment/SNSP forecasting, analogue or
      learned retrieval, and reproducible time-series benchmark work. Add only
      content-verified sources; label insufficient evidence 待核实 and exclude it
      from publication claims. Close the IEEE Access advance as a bounded advance
      over the verified corpus, never global novelty or exhaustive SOTA exclusion.
    acceptance:
      - narrative_structure
      - manuscript_hygiene
      - "custom:experiments/p1_ieee_access_upgrade_v2/validate_upgrade.py --phase references"
      - "custom:../../scripts/mintou/harness_scientific_acceptance.py --project mintou_p1_dstar_gru_dispatch --phase narrative"

  - id: p1v4_s5_manuscript_figures
    title: Rebuild the IEEE Access manuscript and evidence-bound figures
    objective: >-
      Rebuild MANUSCRIPT.md and IEEE Access LaTeX from accepted evidence only.
      Center the reproducible benchmark; present retrieval as its matched use
      case; keep three RQs and a gap-to-contribution-to-result map. Preserve
      Persistence ordering, onset inapplicability, null/adverse effects, and
      non-operational scope in abstract through conclusion. Regenerate tables and
      figures from manifest-bound code, improve legibility and float placement,
      remove redundancy, and preserve explicit author-controlled placeholders.
    acceptance:
      - narrative_structure
      - artifact_consistency
      - manuscript_hygiene
      - pdf_integrity
      - "custom:experiments/p1_ieee_access_upgrade_v2/validate_upgrade.py --phase manuscript"
      - "custom:../../scripts/mintou/harness_scientific_acceptance.py --project mintou_p1_dstar_gru_dispatch --phase full"
      - "custom:../../scripts/mintou/harness_acceptance.py --project mintou_p1_dstar_gru_dispatch --allow-human-placeholders"

  - id: p1v4_s6_independent_closure
    title: Independently reproduce and adversarially close the scientific package
    objective: >-
      Rerun the full v2 experiment in a separate namespace and require exact
      equality of non-timing scientific fields and derived tables, stopping on
      unexplained divergence. Perform separate logic, methodology-statistics,
      and IEEE Access presentation reviews. Rebuild matching source/PDF, verify
      citations, labels, tables, figures, text, floats, and keep the pre-biography
      article below 20 pages. Create a complete package but retain not-ready
      status for unresolved author fields or persistent release URL.
    acceptance:
      - latex_build
      - artifact_consistency
      - pdf_integrity
      - manuscript_hygiene
      - "custom:experiments/p1_ieee_access_upgrade_v2/validate_upgrade.py --phase full"
      - "custom:../../scripts/mintou/harness_scientific_acceptance.py --project mintou_p1_dstar_gru_dispatch --phase full"
      - "custom:../../scripts/mintou/harness_acceptance.py --project mintou_p1_dstar_gru_dispatch --allow-human-placeholders"

  - id: p1v4_s7_human_submission_gate
    title: Insert confirmed submission metadata and build the upload package
    objective: >-
      Insert only author-approved order, affiliations, correspondence, CRediT,
      funding/no-funding, acknowledgments, AI disclosure, ethics, conflicts,
      biographies, photographs, APC responsibility, and persistent code/data
      URL or DOI. Confirm the submitting IEEE account has a public populated
      ORCID even if the manuscript prints NONE. Rebuild exact LaTeX/PDF and
      supplement, checklist, and cover letter. Remain BLOCKED when any item is
      absent or inconsistent.
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

# P1 IEEE Access upgrade plan v4

## Reviewer-loop record

- Loop 1 rejected a contract that omitted the planned architecture baselines.
- Loop 2 rejected a contract that omitted caps 0.60/0.80 and uncertainty/block
  sensitivity, and incorrectly made universal favorable method results a
  prerequisite for the benchmark contribution.
- Loop 3 repairs those omissions prospectively before any v2 result exists.

## Binding boundary

All earlier candidates, logs, adverse results, and rejection events remain
historical evidence. Valid null or adverse effects are publishable bounded
findings; missing cells, leakage, post-hoc protocol changes, unexplained
reproduction mismatch, unverified citations, and invented author data are not.
