---
stages:
  - id: p1v8_s4_literature_integrity
    title: Complete the nearest-neighbor literature audit and bounded advance
    objective: >-
      Produce P1_CITATION_VERIFICATION_V2.md and P1_LITERATURE_GAP_V2.md from
      verifiable evidence only. Preserve the accurate 30-reference
      proposition-level audit, local-corpus paths, hashes, and cache-exclusion
      discipline established in the rejected v7 candidate, but rebuild the
      comparator search so the clear-advance boundary is complete. Inspect and
      classify every PDF in the approved local folder
      papers/literature/target_journal_related/pdfs/p1_ieee_access_extension,
      plus relevant entries in D:/aicoding/mylib/powergrid_paper. At minimum,
      verify and include in a nearest-neighbor matrix: the direct 2021 CAISO
      wind/solar-curtailment study DOI 10.1016/j.enconman.2021.114892; the direct
      2026 IEEE Access curtailment paper DOI
      10.1109/ACCESS.2026.3686958; the 2023/2026 Hadian-Naderkhani conference-to-
      journal lineage including DOI 10.1016/j.segan.2026.102496; RAFT at the
      PMLR 2025 primary record; TimeRAG DOI
      10.1109/ICASSP49660.2025.10889933; CRATEBoost DOI
      10.1016/j.egyai.2026.100855; the 2026 Similar-Day review DOI
      10.3390/forecast8020032; and NeurIPS 2025 SynTSBench DOI
      10.52202/085713-4860. Compare target, data visibility, forecast horizon,
      retrieval mechanism, uncertainty output, baseline breadth, statistics,
      release/provenance, and direct-versus-adjacent status. Check each admitted
      DOI for retraction/correction relations and distinguish abstract-supported
      facts from full-text-supported facts. Label inaccessible claim-bearing
      content UNVERIFIED and exclude it from claims. Search the two approved
      host stores before primary publisher/venue records and record actual files,
      terms, access date, and support level. Never infer host-store absence from
      a sparse worktree. Record retraction provider, snapshot date, URL, commit,
      and checksum, but do not commit databases, API responses, publisher files,
      extracted text, caches, or temporary directories. Make the validator fail
      if any mandatory nearest comparator, matrix dimension, correction status,
      local IEEE Access inventory, or bounded-language token is absent. Limit the
      candidate to compact reports, validators, and provenance. The conclusion
      may claim only a bounded protocol/evidence advance over the explicitly
      verified corpus, never a global first, exhaustive SOTA, or cross-paper
      superiority. Do not rewrite the manuscript in this stage.
    acceptance:
      - narrative_structure
      - manuscript_hygiene
      - "custom:experiments/p1_ieee_access_upgrade_v2/validate_upgrade.py --phase references"
      - "custom:../../scripts/mintou/harness_scientific_acceptance.py --project mintou_p1_dstar_gru_dispatch --phase narrative"

  - id: p1v8_s5_manuscript_figures
    title: Rebuild the IEEE Access manuscript and evidence-bound figures
    objective: >-
      Rebuild MANUSCRIPT.md and the IEEE Access LaTeX from accepted evidence and
      the accepted Stage-4 citation boundary only. Center the reproducible
      benchmark and present retrieval as its matched use case; retain three RQs
      and an explicit gap-to-contribution-to-result map. Keep Persistence ahead
      of the selected learned model at the primary cap where observed, onset
      analysis inapplicable where no onset exists, null or adverse retrieval
      findings, conditional block-bootstrap language, and non-operational scope
      consistent from abstract through conclusion. Add only verified citations,
      including the nearest direct and adjacent records needed to delimit the
      contribution, and repair every PARTIAL or UNSUPPORTED proposition identified
      by Stage 4. Regenerate every paper-facing table and figure from
      manifest-bound code, verify captions and references, improve legibility and
      float placement, remove repetition, and preserve explicit author-controlled
      placeholders. Build the exact source PDF and visually inspect all pages;
      target fewer than 20 pre-biography pages without deleting evidence needed
      for review.
    acceptance:
      - narrative_structure
      - artifact_consistency
      - manuscript_hygiene
      - pdf_integrity
      - "custom:experiments/p1_ieee_access_upgrade_v2/validate_upgrade.py --phase manuscript"
      - "custom:../../scripts/mintou/harness_scientific_acceptance.py --project mintou_p1_dstar_gru_dispatch --phase full"
      - "custom:../../scripts/mintou/harness_acceptance.py --project mintou_p1_dstar_gru_dispatch --allow-human-placeholders"

  - id: p1v8_s6_independent_closure
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

  - id: p1v8_s7_human_submission_gate
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

# P1 IEEE Access nearest-literature continuation plan v8

## Reviewer-loop record

- The frozen experiment and Stage-3 statistics remain immutable accepted inputs.
- Stage 4 attempt 1 was rejected for falsely reporting the approved host corpora
  absent and for committing a roughly 66 MB third-party retraction snapshot.
- Stage 4 attempt 2 corrected those defects and accurately audited the 30 existing
  references, but was rejected because its supposedly complete comparator set
  omitted the closest 2026 IEEE Access curtailment paper, the direct 2021 CAISO
  curtailment study, the current Similar-Day review, and SynTSBench. Its validator
  encoded that incomplete set as sufficient.
- This is Stage 4 attempt 3 of at most 5. It expands only literature coverage and
  the validator; it does not change experiments, statistics, or result direction.

## Binding boundary

Valid null or adverse effects remain publishable bounded findings. Missing cells,
leakage, post-hoc protocol changes, unexplained reproduction divergence,
unverified citations, omission of mandatory nearest comparators, corpus-coverage
misstatements, committed download caches, and invented author data remain Hard
Gate failures.
