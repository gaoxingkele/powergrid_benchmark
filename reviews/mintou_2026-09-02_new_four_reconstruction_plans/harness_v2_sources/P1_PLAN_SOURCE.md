---
stages:
  - id: p1_v2_s01_locked_identity_contract
    title: P1 locked-title, authorship, authority and claim contract
    objective: "Keep the exact title Investment Effectiveness Optimization Strategy based on Hybrid Multi-objective Evolution and the confirmed author order unchanged; declare canonical, legacy and read-only evidence roots; bind P1-C01 through P1-C08 to allowed and prohibited wording; retain the unresolved 0.17-percent preference effect, normalization sensitivity and bounded event-summary scope."
    acceptance:
      - narrative_structure
      - manuscript_hygiene
      - "custom:../../scripts/mintou/harness_reconstruction_v2_acceptance.py --project mintou_p5_trace_moea_feasibility_review --phase contract"
  - id: p1_v2_s02_verified_literature_map
    title: P1 verified literature and Energies comparator map
    objective: "Audit every existing reference for existence, metadata and sentence-level support; search recent investment-planning, power-system validation, constraint handling and hybrid-MOEA comparators; bind each retained source to a claim and evidence locator; organize Related Work by unresolved problem rather than author chronology; introduce no unverified citation."
    acceptance:
      - "custom:../../scripts/mintou/harness_reconstruction_v2_acceptance.py --project mintou_p5_trace_moea_feasibility_review --phase literature"
  - id: p1_v2_s03_method_data_implementation_contract
    title: P1 investment semantics and hybrid-component specification
    objective: "Specify objectives, units, budget, repair, normalization, preference injection, tie handling, evaluation accounting and event-record semantics consistently across equations, pseudocode, config and code; distinguish proxy effectiveness from actual return; determine whether traceable cost, AC or external records are legally and technically usable, otherwise record a NO-GO for the corresponding claim."
    acceptance:
      - narrative_structure
      - artifact_consistency
      - manuscript_hygiene
      - "custom:../../scripts/mintou/harness_reconstruction_v2_acceptance.py --project mintou_p5_trace_moea_feasibility_review --phase literature"
  - id: p1_v2_s04_frozen_experiment_protocol
    title: P1 frozen confirmatory protocol
    objective: "Freeze datasets, licences, task families, paired seeds, hybrid arms, strong baselines, total-evaluation and wall-time budgets, primary and secondary outcomes, method-independent HV bounds, comparison family, multiplicity rule, failure policy and negative-result policy. The component matrix must include NDS/search, deterministic repair and preference-guided retention controls; tuning and final evaluation must remain disjoint."
    acceptance:
      - "custom:../../scripts/mintou/harness_reconstruction_v2_acceptance.py --project mintou_p5_trace_moea_feasibility_review --phase protocol"
  - id: p1_v2_s05_pilot_activation_gate
    title: P1 minimal pipeline and feasibility pilot
    objective: "Run one declared task or network with three to five paired seeds only to validate code, data lineage, cost and feasibility calculations, budget equality, metric orientation and resource estimates. Store the pilot separately, mark paper_use false, inspect every warning and stop rather than tune against the pilot outcome."
    acceptance:
      - "custom:../../scripts/mintou/harness_reconstruction_v2_acceptance.py --project mintou_p5_trace_moea_feasibility_review --phase pilot"
  - id: p1_v2_s06_formal_experiments_statistics
    title: P1 formal comparison, ablation and engineering validation
    objective: "Execute the frozen paired-seed design in an immutable formal namespace; compare stochastic and deterministic baselines at matched output and compute; isolate the three hybrid components; test scenario, normalization and reference-point robustness; add only traceable cost plus physical or external validation that passed the earlier feasibility gate; retain failed runs, null effects and adverse rankings."
    acceptance:
      - "custom:../../scripts/mintou/harness_reconstruction_v2_acceptance.py --project mintou_p5_trace_moea_feasibility_review --phase evidence"
  - id: p1_v2_s07_results_first_manuscript
    title: P1 evidence-first reconstruction of all sections
    objective: "Regenerate tables and figures from the formal manifest, then rewrite Results, Methods, Experimental Setup, Discussion and Limitations before Related Work, Introduction, Abstract and Conclusion. Report effects, uncertainty, multiplicity and compute cost; keep the old 0.89-percent proxy result scoped and upgrade P1-C03, P1-C05 or P1-C08 only if the new evidence ledger permits it."
    acceptance:
      - narrative_structure
      - artifact_consistency
      - manuscript_hygiene
      - "custom:../../scripts/mintou/harness_reconstruction_v2_acceptance.py --project mintou_p5_trace_moea_feasibility_review --phase evidence"
  - id: p1_v2_s08_pre_review_integrity
    title: P1 mandatory pre-review integrity gate
    objective: "Verify all references and evidence locations, audit citation context, numerical lineage, statistics, originality and P1-C01 through P1-C08, and explicitly clear or human-override all seven AI-research failure modes before reviewers see the manuscript."
    acceptance:
      - "custom:../../scripts/mintou/harness_reconstruction_v2_acceptance.py --project mintou_p5_trace_moea_feasibility_review --phase pre_integrity"
  - id: p1_v2_s09_five_view_review
    title: P1 journal-fit and four technical reviewer pass
    objective: "Run five independent lenses: Energies fit, power-system engineering, multi-objective optimization and statistics, reproducibility and data, plus a devil's advocate. Consolidate all major and minor concerns into one evidence-anchored revision roadmap without averaging away dissent."
    acceptance:
      - "custom:../../scripts/mintou/harness_reconstruction_v2_acceptance.py --project mintou_p5_trace_moea_feasibility_review --phase review"
  - id: p1_v2_s10_revision_and_rereview
    title: P1 evidence-bounded revision and re-review
    objective: "Answer every roadmap item with a manuscript location and evidence anchor, rerun analysis only under the frozen change-control policy, preserve negative outcomes, and conduct an independent re-review against the original manuscript hash and revised hash. Maximum two full revision loops; unresolved major issues force conditional or NO-GO status."
    acceptance:
      - "custom:../../scripts/mintou/harness_reconstruction_v2_acceptance.py --project mintou_p5_trace_moea_feasibility_review --phase re_review"
  - id: p1_v2_s11_final_integrity_language_pdf
    title: P1 final integrity, writing-regression and PDF gate
    objective: "Re-run full reference and citation-context verification, audit every figure and table against source data, and perform a cold-reader prose comparison against the frozen baseline. Improve clarity and scientific flow without changing numbers, citations, equations or claim strength; then compile and visually inspect the Energies PDF."
    acceptance:
      - latex_build
      - artifact_consistency
      - pdf_integrity
      - manuscript_hygiene
      - "custom:../../scripts/mintou/harness_reconstruction_v2_acceptance.py --project mintou_p5_trace_moea_feasibility_review --phase final_integrity"
      - "custom:../../scripts/mintou/harness_acceptance.py --project mintou_p5_trace_moea_feasibility_review --allow-human-placeholders"
  - id: p1_v2_s12_release_human_gate
    title: P1 reproducible package and human submission gate
    objective: "Create a hash manifest covering LaTeX, PDF, figures, tables, code, data and validation records; accept only author-confirmed CRediT, funding, conflicts, rights, correspondence and repository facts; recheck the current journal instructions and stop for the corresponding author's final approval before external submission."
    acceptance:
      - latex_build
      - no_placeholders
      - declarations
      - artifact_consistency
      - pdf_integrity
      - "custom:../../scripts/mintou/harness_reconstruction_v2_acceptance.py --project mintou_p5_trace_moea_feasibility_review --phase release"
      - "custom:../../scripts/mintou/harness_acceptance.py --project mintou_p5_trace_moea_feasibility_review"
---

# P1 v2 execution contract

- Locked title: `Investment Effectiveness Optimization Strategy based on Hybrid Multi-objective Evolution`.
- Scientific priority: establish whether hybrid search improves a clearly defined investment-effectiveness proxy and whether any gain survives cost, physical or external validation.
- Preserved adverse evidence: the existing pooled advantage is small; the isolated preference effect is unresolved; normalization can change rankings; run-level event summaries are not causal explanations or full lineage.
- Stop rule: without traceable cost and at least one accepted engineering/external validation layer, the paper may report pre-decision proxy screening only.
- Resource control: pilot maximum five paired seeds; formal scale is frozen only after pilot resource measurement; at most two full manuscript revision loops and three integrity-correction passes.

