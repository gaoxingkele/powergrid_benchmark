---
stages:
  - id: p1v9_s5_manuscript_figures
    title: Rebuild and visually close the IEEE Access manuscript
    objective: >-
      Reproduce the scientifically successful v8 Stage-5 draft from the accepted
      experiment, statistics, and literature evidence, while correcting the gate
      conflict and visual defects found in review. Preserve explicit author,
      funding, ethics, contribution, conflict, biography, photo, and release-URL
      placeholders; never invent them. Repair every PARTIAL or UNSUPPORTED
      citation proposition identified in Stage 4 and include the accepted nearest
      direct and adjacent records. Keep the benchmark central and retrieval as
      its matched use case; retain three RQs, the gap-to-contribution-to-result
      map, Persistence's primary-cap ordering, onset inapplicability, null/adverse
      retrieval findings, conditional moving-block language, and non-operational
      scope from abstract through conclusion. Regenerate all four figures and six
      tables from manifest-bound code. Specifically fix the left-edge clipping of
      the FIGURE 3 and TABLE 4 caption labels observed on page 6 of the blocked v8
      draft. Build the exact source PDF, keep the pre-biography article below 20
      pages without deleting review-critical evidence, and render every page for
      manual checks of clipping, overlap, font size, whitespace, floats, captions,
      references, headers, and footers. Built-in pdf_integrity is intentionally
      deferred because it rejects required human placeholders; latex_build plus
      the placeholder-aware project gate and manual rendered-page inspection are
      binding in this stage.
    acceptance:
      - narrative_structure
      - latex_build
      - artifact_consistency
      - manuscript_hygiene
      - "custom:experiments/p1_ieee_access_upgrade_v2/validate_upgrade.py --phase manuscript"
      - "custom:../../scripts/mintou/harness_scientific_acceptance.py --project mintou_p1_dstar_gru_dispatch --phase full"
      - "custom:../../scripts/mintou/harness_acceptance.py --project mintou_p1_dstar_gru_dispatch --allow-human-placeholders"

  - id: p1v9_s6_independent_closure
    title: Independently reproduce and adversarially close the scientific package
    objective: >-
      Re-run the full accepted v2 experiment in a separate namespace and require
      exact equality of every non-timing scientific field and derived table;
      stop on unexplained divergence. Independently review narrative logic,
      method and statistics, citation entailment, and IEEE Access presentation.
      Rebuild matching source and PDF; verify labels, citations, tables, figures,
      text, floats, file inventory, and the under-20-page pre-biography target.
      Render every page and require zero visual defects. Ensure the release package
      contains only necessary source, figures, generated tables, compact evidence,
      code, and declared data pointers, with no caches or bulk third-party
      literature snapshots. Preserve explicit human placeholders and retain
      not-ready status for unresolved author fields or a missing persistent code
      and data URL. Built-in pdf_integrity remains deferred until Stage 7 because
      its placeholder scan conflicts with this required draft boundary.
    acceptance:
      - latex_build
      - artifact_consistency
      - manuscript_hygiene
      - "custom:experiments/p1_ieee_access_upgrade_v2/validate_upgrade.py --phase full"
      - "custom:../../scripts/mintou/harness_scientific_acceptance.py --project mintou_p1_dstar_gru_dispatch --phase full"
      - "custom:../../scripts/mintou/harness_acceptance.py --project mintou_p1_dstar_gru_dispatch --allow-human-placeholders"

  - id: p1v9_s7_human_submission_gate
    title: Insert confirmed submission metadata and build the upload package
    objective: >-
      Insert only author-approved order, affiliations, correspondence, CRediT,
      funding or no-funding declaration, acknowledgments, AI disclosure, ethics,
      conflicts, biographies, photographs, APC responsibility, and persistent
      code and data URL or DOI. Print ORCID as NONE per author instruction while
      separately confirming that the submitting IEEE account has a public,
      populated ORCID if the portal requires it. Rebuild the exact LaTeX and PDF,
      supplement, checklist, cover letter, and final inventory; render every PDF
      page after the final metadata insertion. Remain BLOCKED when any
      author-controlled item is absent, unapproved, or inconsistent; never invent
      submission metadata to pass a gate.
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

# P1 IEEE Access manuscript continuation plan v9

## Reviewer-loop record

- Stages 1-4 are accepted; their experiment, statistics, citation audit, and
  bounded literature position remain immutable inputs.
- Stage 5 attempt 1 was BLOCKED after six checks passed because the approved
  objective required human placeholders while the built-in pdf_integrity check
  unconditionally rejects them. The placeholder-aware project gate passed, and
  the draft contained 38 references, four figures, six tables, and nine pages.
- Independent rendering of all nine blocked-draft pages found generally clear
  layout but identified clipped leading letters in the FIGURE 3 and TABLE 4 labels
  on page 6. No blocked-draft change is accepted or merged by implication.
- This is Stage 5 attempt 2 of at most 5. It corrects the gate contract and visual
  defect without changing any scientific protocol or result.

## Binding boundary

Human placeholders are required until author confirmation and are not PDF
corruption. In Stages 5-6, a successful LaTeX build, placeholder-aware project
gate, and complete manual page rendering replace the incompatible built-in
placeholder scan. Stage 7 still requires zero placeholders and full pdf_integrity.
Valid null or adverse effects remain publishable bounded findings; evidence loss,
visual clipping, unverified citations, post-hoc protocol changes, unexplained
reproduction divergence, and invented author data remain Hard Gate failures.
