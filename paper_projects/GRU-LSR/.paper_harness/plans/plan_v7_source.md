---
stages:
  - id: p1v7_s4_literature_integrity
    title: Re-run verified literature integrity with local-corpus provenance
    objective: >-
      Produce P1_CITATION_VERIFICATION_V2.md and P1_LITERATURE_GAP_V2.md from
      verifiable evidence only. Inspect the approved host stores
      D:/aicoding/powergrid_benchmark/papers/literature and
      D:/aicoding/mylib/powergrid_paper before using primary publisher records;
      record the actual local files or corpus entries inspected, search terms,
      access date, and support level. Never infer that a host corpus is absent
      merely because it is outside the sparse Harness worktree. Verify all 30
      manuscript references for bibliographic identity, DOI or stable URL,
      retraction or correction status, and the exact manuscript proposition
      they support. For 2025-2026 curtailment or SNSP forecasting, analogue or
      learned retrieval, and reproducible time-series benchmarks, admit a new
      comparator only when its primary record and claim-bearing content have
      been checked; otherwise label it UNVERIFIED and exclude it from claims.
      Record retraction-data provider, snapshot date, URL, and checksum, but do
      not commit downloaded databases, Crossref responses, publisher files,
      caches, temporary directories, or other third-party bulk assets. Limit
      the candidate to compact review reports, validators, and provenance. Close
      the IEEE Access case as a bounded advance over the explicitly verified
      corpus, with no global-first, exhaustive-SOTA, or unsupported superiority
      language. Do not rewrite the manuscript in this stage.
    acceptance:
      - narrative_structure
      - manuscript_hygiene
      - "custom:experiments/p1_ieee_access_upgrade_v2/validate_upgrade.py --phase references"
      - "custom:../../scripts/mintou/harness_scientific_acceptance.py --project mintou_p1_dstar_gru_dispatch --phase narrative"

  - id: p1v7_s5_manuscript_figures
    title: Rebuild the IEEE Access manuscript and evidence-bound figures
    objective: >-
      Rebuild MANUSCRIPT.md and the IEEE Access LaTeX from accepted evidence and
      the accepted Stage-4 citation boundary only. Center the reproducible
      benchmark and present retrieval as its matched use case; retain three RQs
      and an explicit gap-to-contribution-to-result map. Keep Persistence ahead
      of the selected learned model at the primary cap where observed, onset
      analysis inapplicable where no onset exists, null or adverse retrieval
      findings, conditional block-bootstrap language, and non-operational scope
      consistent from abstract through conclusion. Add only verified citations.
      Regenerate every paper-facing table and figure from manifest-bound code,
      verify captions and references, improve legibility and float placement,
      remove repetition, and preserve explicit author-controlled placeholders.
      Build the exact source PDF and visually inspect all pages; target fewer
      than 20 pre-biography pages without deleting evidence needed for review.
    acceptance:
      - narrative_structure
      - artifact_consistency
      - manuscript_hygiene
      - pdf_integrity
      - "custom:experiments/p1_ieee_access_upgrade_v2/validate_upgrade.py --phase manuscript"
      - "custom:../../scripts/mintou/harness_scientific_acceptance.py --project mintou_p1_dstar_gru_dispatch --phase full"
      - "custom:../../scripts/mintou/harness_acceptance.py --project mintou_p1_dstar_gru_dispatch --allow-human-placeholders"

  - id: p1v7_s6_independent_closure
    title: Independently reproduce and adversarially close the scientific package
    objective: >-
      Re-run the full accepted v2 experiment in a separate namespace and require
      exact equality of every non-timing scientific field and derived table;
      stop on unexplained divergence. Independently review narrative logic,
      method and statistics, citation entailment, and IEEE Access presentation.
      Rebuild matching source and PDF; verify labels, citations, tables, figures,
      text, floats, file inventory, and the under-20-page pre-biography target.
      Ensure the release package contains only necessary source, figures,
      generated tables, compact evidence, code, and declared data pointers, with
      no caches or bulk third-party literature snapshots. Retain not-ready status
      for unresolved author fields or a missing persistent code and data URL.
    acceptance:
      - latex_build
      - artifact_consistency
      - pdf_integrity
      - manuscript_hygiene
      - "custom:experiments/p1_ieee_access_upgrade_v2/validate_upgrade.py --phase full"
      - "custom:../../scripts/mintou/harness_scientific_acceptance.py --project mintou_p1_dstar_gru_dispatch --phase full"
      - "custom:../../scripts/mintou/harness_acceptance.py --project mintou_p1_dstar_gru_dispatch --allow-human-placeholders"

  - id: p1v7_s7_human_submission_gate
    title: Insert confirmed submission metadata and build the upload package
    objective: >-
      Insert only author-approved order, affiliations, correspondence, CRediT,
      funding or no-funding declaration, acknowledgments, AI disclosure, ethics,
      conflicts, biographies, photographs, APC responsibility, and persistent
      code and data URL or DOI. Print ORCID as NONE per author instruction while
      separately confirming that the submitting IEEE account has a public,
      populated ORCID if the portal requires it. Rebuild the exact LaTeX and PDF,
      supplement, checklist, cover letter, and final inventory. Remain BLOCKED
      when any author-controlled item is absent, unapproved, or inconsistent;
      never invent submission metadata to pass a gate.
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

# P1 IEEE Access literature-integrity continuation plan v7

## Reviewer-loop record

- Stages 1-3 of the scientific upgrade are accepted and remain immutable inputs.
- Stage 4 attempt 1 was rejected even though its automated gates passed: it
  incorrectly reported the approved host literature stores as unavailable and
  committed a roughly 66 MB third-party Retraction Watch snapshot under a
  temporary directory.
- This is Stage 4 attempt 2 of at most 5. It repairs evidence provenance and
  repository hygiene without changing the frozen experiment, statistics, or
  interpretation rules.

## Binding boundary

Valid null or adverse effects remain publishable bounded findings. Missing
cells, leakage, post-hoc protocol changes, unexplained reproduction divergence,
unverified citations, corpus-coverage misstatements, committed download caches,
and invented author data remain Hard Gate failures.
