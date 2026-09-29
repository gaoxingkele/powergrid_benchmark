---
stages:
  - id: p3_v2_s01_locked_identity_contract
    title: P3 locked-title, authorship and claim contract
    objective: "Keep the exact title Power Distribution Network Planning Strategy Optimization based on Self-Adaption Multi-objective Differential Evolution Algorithm and the confirmed author order unchanged; preserve Zhang Linyao as first author and Zheng Jieyun as corresponding author; bind P3-C01 through P3-C08 to their current evidence and prohibited wording."
    acceptance:
      - narrative_structure
      - manuscript_hygiene
      - "custom:../../scripts/mintou/harness_reconstruction_v2_acceptance.py --project mintou_p3_samode_distribution_planning --phase contract"
  - id: p3_v2_s02_verified_literature_map
    title: P3 verified planning and self-adaptive DE literature map
    objective: "Audit every existing reference for existence, metadata and sentence support; search action-aligned distribution expansion, DER and storage planning, AC validation, self-adaptive DE, constraint handling and multi-objective evaluation; map sources to exact claims and avoid using generic optimizer papers as engineering validation."
    acceptance:
      - "custom:../../scripts/mintou/harness_reconstruction_v2_acceptance.py --project mintou_p3_samode_distribution_planning --phase literature"
  - id: p3_v2_s03_action_method_implementation_contract
    title: P3 action-aligned planning and split-adaptation specification
    objective: "Map each decision variable to an auditable network action, cost and electrical effect; specify load and DER scenarios, voltage and thermal limits, repair, phenotype mapping, evaluation accounting and AC post-validation. Split parameter adaptation from strategy adaptation in code while retaining a tested backward-compatible mode; prohibit attributing effects to a coupled switch."
    acceptance:
      - narrative_structure
      - artifact_consistency
      - manuscript_hygiene
      - "custom:../../scripts/mintou/harness_reconstruction_v2_acceptance.py --project mintou_p3_samode_distribution_planning --phase literature"
  - id: p3_v2_s04_frozen_experiment_protocol
    title: P3 frozen 2-by-2 mechanism and AC-validation protocol
    objective: "Freeze Fixed-Fixed, AdaptiveParam-FixedStrategy, FixedParam-AdaptiveStrategy and Full-SAMODE arms; direct DE and NSGA-II controls; public network cases and action sets; paired seeds; compute budgets; primary metric and method-independent reference; IGD+ and engineering feasibility outcomes; multiplicity, failures and negative-result handling."
    acceptance:
      - "custom:../../scripts/mintou/harness_reconstruction_v2_acceptance.py --project mintou_p3_samode_distribution_planning --phase protocol"
  - id: p3_v2_s05_pilot_activation_gate
    title: P3 action-to-AC and four-arm pilot
    objective: "On at least one declared network and three to five paired seeds, verify that all four arms run, the action mapping changes the intended network parameters, budget repair is deterministic, AC diagnostics use the planned scenarios, metric orientation is correct and resource cost is measured. Keep all pilot values out of confirmatory prose."
    acceptance:
      - "custom:../../scripts/mintou/harness_reconstruction_v2_acceptance.py --project mintou_p3_samode_distribution_planning --phase pilot"
  - id: p3_v2_s06_formal_experiments_statistics
    title: P3 formal mechanism, planning and metric-robustness evaluation
    objective: "Execute the frozen paired design across the accepted network and scenario panel; estimate parameter-adaptation, strategy-adaptation and interaction effects; compare against strong controls under equal evaluation budgets; post-validate deterministic compromise and front samples with AC power flow; report effect sizes, uncertainty, corrected tests, failures, runtime and metric/reference sensitivity."
    acceptance:
      - "custom:../../scripts/mintou/harness_reconstruction_v2_acceptance.py --project mintou_p3_samode_distribution_planning --phase evidence"
  - id: p3_v2_s07_results_first_manuscript
    title: P3 evidence-first reconstruction of planning narrative
    objective: "Generate figures and tables from the formal manifest, then write Results, Planning Model, Algorithm, Experimental Design, Discussion and Limitations before Related Work, Introduction, Abstract and Conclusion. Keep the archived 6.06-percent sampled/clipped-HV result beside its reversal and IGD+ evidence; claim self-adaptation or AC feasibility only if the new ledger licenses it."
    acceptance:
      - narrative_structure
      - artifact_consistency
      - manuscript_hygiene
      - "custom:../../scripts/mintou/harness_reconstruction_v2_acceptance.py --project mintou_p3_samode_distribution_planning --phase evidence"
  - id: p3_v2_s08_pre_review_integrity
    title: P3 mandatory pre-review integrity gate
    objective: "Verify references, citation context samples, action provenance, numeric lineage, statistical units, originality and P3-C01 through P3-C08; clear or explicitly human-override all seven AI-research failure modes, including proxy-to-physics overreach and metric cherry-picking."
    acceptance:
      - "custom:../../scripts/mintou/harness_reconstruction_v2_acceptance.py --project mintou_p3_samode_distribution_planning --phase pre_integrity"
  - id: p3_v2_s09_five_view_review
    title: P3 journal-fit and four technical reviewer pass
    objective: "Run Energies fit, distribution-planning engineering, evolutionary optimization, statistics and reproducibility, and devil's-advocate reviews. Consolidate evidence-linked concerns on action realism, AC validity, mechanism identification, metric robustness and novelty into one roadmap without concealing reviewer disagreement."
    acceptance:
      - "custom:../../scripts/mintou/harness_reconstruction_v2_acceptance.py --project mintou_p3_samode_distribution_planning --phase review"
  - id: p3_v2_s10_revision_and_rereview
    title: P3 evidence-bounded revision and re-review
    objective: "Answer every roadmap item with location and evidence, rerun only through frozen change control, preserve failures and adverse rankings, and compare original and revised hashes in independent re-review. Stop after two full revision loops; unresolved action realism or invalid AC inference forces conditional or NO-GO status."
    acceptance:
      - "custom:../../scripts/mintou/harness_reconstruction_v2_acceptance.py --project mintou_p3_samode_distribution_planning --phase re_review"
  - id: p3_v2_s11_final_integrity_language_pdf
    title: P3 final integrity, writing-regression and PDF gate
    objective: "Complete reference and citation-context verification, equation-code-action checks, figure-table lineage audit and cold-reader prose regression. Improve precision and narrative continuity without changing numbers, citations or claim strength; compile and visually inspect the Energies PDF with the exact locked title."
    acceptance:
      - latex_build
      - artifact_consistency
      - pdf_integrity
      - manuscript_hygiene
      - "custom:../../scripts/mintou/harness_reconstruction_v2_acceptance.py --project mintou_p3_samode_distribution_planning --phase final_integrity"
      - "custom:../../scripts/mintou/harness_acceptance.py --project mintou_p3_samode_distribution_planning --allow-human-placeholders"
  - id: p3_v2_s12_release_human_gate
    title: P3 reproducible package and human submission gate
    objective: "Hash and package LaTeX, PDF, figures, tables, code, data, action mappings and validation records; accept only human-confirmed CRediT, funding, conflicts, rights, correspondence and repository facts; recheck current Energies instructions and stop for final corresponding-author approval."
    acceptance:
      - latex_build
      - no_placeholders
      - declarations
      - artifact_consistency
      - pdf_integrity
      - "custom:../../scripts/mintou/harness_reconstruction_v2_acceptance.py --project mintou_p3_samode_distribution_planning --phase release"
      - "custom:../../scripts/mintou/harness_acceptance.py --project mintou_p3_samode_distribution_planning"
---

# P3 v2 execution contract

- Locked title: `Power Distribution Network Planning Strategy Optimization based on Self-Adaption Multi-objective Differential Evolution Algorithm`.
- Scientific priority: separate parameter and strategy adaptation, and connect optimizer decisions to real network actions and AC constraints.
- Preserved adverse evidence: the archived 6.06-percent result depends on sampled/clipped HV; analytic HV reverses the order; common-reference IGD+ ranks the method fifth; FixedDE is nominally ahead; the current AC check is illustrative.
- Stop rule: if action-to-network mapping and an end-to-end AC validation panel cannot be established, the work remains a proxy optimization study and the locked-title Energies submission is NO-GO.
- Resource control: pilot maximum five paired seeds; formal scale follows measured runtime; at most two manuscript revision loops and three integrity-correction passes.

