---
stages:
  - id: p1v5_s3_statistics_robustness
    title: Derive frozen inference, uncertainty, and time-dependence sensitivity
    objective: >-
      Generate paper-facing tables only from the accepted v4 Stage-2 frozen
      manifest. Report paired seed effects, predeclared uncertainty intervals,
      exact sign-flip tests, and within-family Holm adjustments. Run the frozen
      moving-block sensitivity on paired hourly loss differences and label it
      conditional/descriptive. Deterministic references and cross-cap findings
      remain descriptive. Apply the predeclared wording router for learned-space,
      method-specific, null/adverse, Persistence, and onset-inapplicable outcomes
      without changing the protocol after seeing results. Preserve executable
      provenance accurately: compare the execution-manifest hash with the
      committed Git blob or an explicitly recorded canonical-LF representation,
      record any CRLF checkout rendering separately, and never misclassify
      line-ending conversion as a scientific source mismatch. Fail closed on a
      real committed-content mismatch.
    acceptance:
      - "custom:experiments/p1_ieee_access_upgrade_v2/validate_upgrade.py --phase statistics"
      - "custom:../../scripts/mintou/harness_scientific_acceptance.py --project mintou_p1_dstar_gru_dispatch --phase evidence"

  - id: p1v5_s4_literature_integrity
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

  - id: p1v5_s5_manuscript_figures
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

  - id: p1v5_s6_independent_closure
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

  - id: p1v5_s7_human_submission_gate
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

# P1 IEEE Access upgrade continuation plan v5

## Reviewer-loop record

- v4 Stage 1 was accepted after the complete prospective contract was frozen.
- v4 Stage 2 was accepted after all 2,310 rows, 240 trajectories, attribution
  controls, failure ledgers, and evidence gates passed.
- v4 Stage 3 candidate 1 was rejected because it mistook a Windows CRLF checkout
  rendering for a mismatch between the executed runner and the committed source.
  The execution-manifest SHA-256 exactly matched the committed LF Git blob.
- v5 continues only the unfinished stages and corrects that provenance
  interpretation without changing any scientific protocol, result, or gate.

## Binding boundary

Accepted v4 Stage-1 and Stage-2 artifacts are immutable inputs. Valid null or
adverse effects remain publishable bounded findings. Missing cells, leakage,
post-hoc protocol changes, real source-identity mismatches, unexplained
reproduction divergence, unverified citations, and invented author data remain
Hard Gate failures.
