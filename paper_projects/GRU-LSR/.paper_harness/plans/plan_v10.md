---
stages:
  - id: s6r3
    title: Deterministic Stage-6 candidate
    objective: >-
      Produce a new Stage-6 candidate without changing scientific results or broadening claims. Execute four separately recorded workstreams: (1) rerun the full isolated v2 workflow once in the same frozen environment, with estimand = the accepted-v4 primary paired estimand, control = the accepted-v4 frozen comparator arms, analysis unit = the unit declared in PROSPECTIVE_CONTRACT.md and upgrade_contract.json, stopping rule = one complete protocol-valid execution with no optional runs or seed additions, and supportable claim = exact reproduction of the accepted non-timing scientific fields and derived tables only; a timeout or incomplete ledger fails closed and requires a hashed WIP record rather than a candidate; (2) repeat the v6 statistical review and citation/narrative review while preserving every direction, sample size, decision, null or negative result, scope boundary, and comparison limitation; (3) verify title-to-method-to-evidence and contribution-to-test alignment without causal, operational, expert-validation, or deployment upgrades; and (4) rebuild and visually inspect all nine current pages, then recreate the compact 87-file-style release package while retaining explicit human placeholders. Set SOURCE_DATE_EPOCH and FORCE_SOURCE_DATE to the same recorded constant for every agent and Harness compile. After the final Harness latex_build, refresh the package and PDF_RENDER_QA.json if any compile occurred, then run a fail-closed validator requiring raw SHA-256 equality among manuscript/journal_submission/paper.pdf, the release-package manuscript/paper.pdf, and the PDF_RENDER_QA.json PDF hash; matching manuscript/package TeX hashes; verified package-manifest hashes; semantic extracted-text and semantic-hash equality; nine-page identity; current-page render review; and separately reported frozen script/config/input identity, scientific-field identity, derived-table identity, and non-scientific timing differences. Repeated deterministic compiles must be byte-identical. Defer built-in pdf_integrity because the required human placeholders remain.
    acceptance:
      - custom:scripts/validate_stage6_rerun_v2.py
      - custom:scripts/validate_stage6_evidence_alignment.py
      - narrative_structure
      - manuscript_hygiene
      - latex_build
      - artifact_consistency
      - custom:scripts/validate_stage6_deterministic_release.py
  - id: s7
    title: Human metadata and submission gate
    objective: >-
      Run only after s6r3 is accepted and every required fact is author-approved. Insert no inferred metadata; print manuscript ORCID as NONE as instructed, while separately checking whether the submitting account requires an ORCID. Keep this stage BLOCKED while any author, affiliation, funding, CRediT, conflict-of-interest, AI-disclosure, biography, photo, APC, or persistent-URL fact is missing. After authorized insertion, preserve the accepted science, rerun the final citation, narrative, method/evidence, statistical, declaration, and submission checks; compile with the same fixed SOURCE_DATE_EPOCH and FORCE_SOURCE_DATE; refresh the package and current-artifact render QA after the last compile; and require the fail-closed PDF, TeX, manifest, semantic-text/hash, dynamic page-count, and all-page visual identities before handoff.
    acceptance:
      - no_placeholders
      - declarations
      - narrative_structure
      - manuscript_hygiene
      - latex_build
      - artifact_consistency
      - pdf_integrity
      - custom:scripts/validate_stage7_final_submission.py
---

The continuation has one narrowly scoped Stage-6 retry and the unchanged human Stage-7 gate. Stage 6 resolves the timestamp-only rejection through reproducible builds and post-build identity validation; Stage 7 remains the sole point for author-confirmed metadata and final scientific/submission acceptance.