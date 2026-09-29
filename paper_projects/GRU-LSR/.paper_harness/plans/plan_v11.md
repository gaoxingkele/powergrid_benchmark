---
stages:
  - id: s6
    title: Final default-PATH release identity
    objective: >-
      Complete Stage 6 attempt 5/5 while preserving all accepted science and v10
      s6r3 responsibilities. First, execute the frozen, fully isolated v2 scientific
      rerun without changing its script, configuration, inputs, estimands, controls,
      analysis units, sample sizes, stopping rule, or statistical decisions. Compare
      script/config/input identity, scientific fields, derived tables, and non-scientific
      timing fields separately; require exact equality for all non-timing scientific
      content, disclose timing or environment differences, and support no new claim.
      Separately verify method-to-evidence alignment and preserve every accepted result,
      direction, null or negative finding, evidence boundary, comparison qualification,
      and the accepted 236-word narrative without broadening causal, operational,
      expert-validation, or deployment claims; retain all human placeholders for Stage
      7. For final artifact QA, create or use no custom/local MiKTeX or TEXMF runtime,
      MIKTEX_* override, .miktex* directory, alternate pdflatex binary, output-directory,
      or container. With SOURCE_DATE_EPOCH=1787867025, FORCE_SOURCE_DATE=1, and TZ=UTC,
      invoke only inherited default-PATH pdflatex from manuscript/journal_submission,
      exactly as paper_harness.checks.check_latex_build does: pdflatex
      -interaction=nonstopmode -halt-on-error paper.tex three times in the same order,
      adding its bibliography step only if required. The expected stable raw PDF SHA-256
      is BB61E0B1B20A3E9192BC05C640EB8C8895B0B0C24D8F2255C56FD4C4FF983C5C.
      After the final compile, copy those exact paper.pdf and paper.tex bytes into the
      release package, regenerate PDF_RENDER_QA and PACKAGE_MANIFEST from those bytes,
      render and manually inspect all 9 pages, and make no subsequent stage edit to the
      journal PDF. The terminal validator must be read-only and require equality among
      the post-latex_build journal PDF raw SHA, packaged PDF raw SHA, QA-recorded PDF
      SHA, and manifest PDF SHA; matching journal/package/manifest TeX hashes; identical
      semantically extracted text; identical 9-page counts and per-page render hashes;
      and complete nine-page visual-inspection records. It must fail if any .miktex*
      path, TeX auxiliary/log file, cache, or alternative runtime is tracked or packaged.
    acceptance:
      - custom:experiments/p1_ieee_access_upgrade_v2/validate_upgrade.py
      - narrative_structure
      - artifact_consistency
      - manuscript_hygiene
      - latex_build
      - custom:scripts/validate_p1_stage6_release_identity.py
  - id: s7
    title: Human metadata and submission gate
    objective: >-
      Keep Stage 7 BLOCKED until the author supplies and confirms every missing human
      fact and declaration; do not infer authors, order, affiliations, correspondence,
      ORCID status, funding, acknowledgements, conflicts, or other submission metadata.
      Only after insertion of the confirmed author metadata may the human-gate validator
      print the exact status line manuscript ORCID NONE. Then perform the final
      scientific-continuity and submission checks without changing accepted results,
      directions, sample sizes, statistical decisions, evidence boundaries, or claims.
      Resolve every placeholder before rebuilding or invoking pdf_integrity, and accept
      Stage 7 only after the current human-complete artifact passes all checks.
    acceptance:
      - no_placeholders
      - declarations
      - custom:scripts/validate_p1_stage7_human_metadata.py
      - narrative_structure
      - artifact_consistency
      - manuscript_hygiene
      - latex_build
      - pdf_integrity
---

Stage 6 isolates the already-diagnosed build-environment defect from the accepted scientific, statistical, and narrative record. Its final check runs after the Harness build and proves byte-level, semantic, pagination, rendering, and package identity. Stage 7 remains a genuine human-fact gate; its ordered checks prevent ORCID reporting, compilation, or PDF acceptance while placeholders remain unresolved.