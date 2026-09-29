---
stages:
  - id: s6r4
    title: Engineering-only release recovery
    objective: >-
      Recover the Stage-6 release strictly as an engineering/package-ordering task after the five-attempt pause. Preserve every accepted scientific result, direction, sample size, statistical decision, figure meaning, citation set, the 236-word abstract, limitation, negative/null/adverse finding, and evidence boundary; make no new claim, rerun no experiment, edit neither MANUSCRIPT.md nor scientific prose, and infer no Stage-7 metadata. Treat experiments/p1_ieee_access_upgrade_v2_stage6_attempt5 as the independently verified scientific rerun and require scripts/generate_p1_stage6_science_comparison.py to confirm exact non-timing scientific identity, 2310 rows, 240 trajectories, and five derived tables. The executor must not compile TeX, create the release package, or touch paper.pdf; those operations occur only through the ordered Harness acceptance checks. Run the parent environment with SOURCE_DATE_EPOCH=1787867025, FORCE_SOURCE_DATE=1, and TZ=UTC, with latex_build using inherited default-PATH pdflatex. After that build, finalize the release by copying the exact journal PDF and TeX plus all 87 compilable submission-source files, excluding TeX auxiliary/log/cache/custom-runtime debris; generate PACKAGE_MANIFEST and nine current page renders; bind the prior manual visual review to PDF SHA-256 bb61e0b1b20a3e9192bc05c640eb8c8895b0b0c24d8f2255c56fd4c4ff983c5c; and perform an independent terminal re-render. Accept only raw main/package PDF equality, raw main/package TeX equality, canonical frozen-TeX identity, semantic-text identity, nine pages, all 87 source/manifest hashes, nine render hashes, and retained human placeholders. Do not invoke scripts/validate_p1_stage6_release_identity.py.
    acceptance:
      - custom:scripts/generate_p1_stage6_science_comparison.py
      - custom:experiments/p1_ieee_access_upgrade_v2/validate_upgrade.py --phase manuscript
      - narrative_structure
      - artifact_consistency
      - manuscript_hygiene
      - latex_build
      - custom:scripts/build_stage6_release.py
      - custom:scripts/update_pdf_render_qa.py --compile-hash-a bb61e0b1b20a3e9192bc05c640eb8c8895b0b0c24d8f2255c56fd4c4ff983c5c --compile-hash-b bb61e0b1b20a3e9192bc05c640eb8c8895b0b0c24d8f2255c56fd4c4ff983c5c --confirm-visual-review
      - custom:scripts/validate_stage6_deterministic_release.py
  - id: s7
    title: Human-fact and submission gate
    objective: >-
      Keep the final stage blocked until humans confirm and insert every author name and order, affiliation, correspondence detail, submitting-account ORCID, funding statement, CRediT role, conflict declaration, acknowledgment, AI-use confirmation, biography, photograph, APC choice, public repository/DOI, and concurrent/prior-submission declaration, replacing all placeholders without inference. Preserve manuscript ORCID rendering as NONE after confirmed metadata is inserted, while explicitly not treating NONE as satisfaction of the IEEE submission-account ORCID requirement. After factual completion, run the ordered checks as the final scientific-continuity, declaration, artifact, PDF, and submission-readiness gate.
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

Stage s6r4 separates frozen experiment/statistics verification, narrative and method/evidence alignment checks, and ordered artifact construction/QA without changing scientific content. Only after its acceptance may s7 resolve human-supplied facts and perform the final scientific and submission checks.