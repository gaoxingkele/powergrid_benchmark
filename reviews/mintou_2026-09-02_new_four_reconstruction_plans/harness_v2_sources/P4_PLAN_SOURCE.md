---
stages:
  - id: p4_v2_s01_locked_identity_contract
    title: P4 locked-title, authorship and title-method claim contract
    objective: "Keep the exact title Graph Convolutional Network based on Hyperbolic Space for Power Load Forecasting and the confirmed author order unchanged; preserve Zheng Jieyun as first and corresponding author; bind P4-C01 through P4-C08; state explicitly that the current CSA model is a baseline and not a GCN or HGCN."
    acceptance:
      - narrative_structure
      - manuscript_hygiene
      - "custom:../../scripts/mintou/harness_reconstruction_v2_acceptance.py --project mintou_p2_hygraph_load_forecasting --phase contract"
  - id: p4_v2_s02_verified_literature_map
    title: P4 verified HGCN, STGNN and load-forecasting literature map
    objective: "Audit every existing reference for existence, metadata and sentence support; verify foundational GCN and hyperbolic graph-network sources from primary papers; search recent load-forecasting STGNN, learned-graph, simple-linear-baseline and evaluation-rigor work; map each source to an exact claim and avoid claiming novelty from an incomplete search."
    acceptance:
      - "custom:../../scripts/mintou/harness_reconstruction_v2_acceptance.py --project mintou_p2_hygraph_load_forecasting --phase literature"
  - id: p4_v2_s03_graph_data_model_implementation_contract
    title: P4 leakage-free graph and genuine hyperbolic convolution specification
    objective: "Freeze node and target semantics, edge provenance and train-only construction; implement a Euclidean GCN sanity baseline and a genuine hyperbolic GCN with explicit manifold, curvature treatment, maps, aggregation and numerical safeguards; share the same temporal encoder and prediction head where identification requires it; keep CSA and DLinear as mandatory predecessors."
    acceptance:
      - narrative_structure
      - artifact_consistency
      - manuscript_hygiene
      - "custom:../../scripts/mintou/harness_reconstruction_v2_acceptance.py --project mintou_p2_hygraph_load_forecasting --phase literature"
  - id: p4_v2_s04_frozen_experiment_protocol
    title: P4 frozen graph-geometry forecasting protocol
    objective: "Freeze licensed datasets, node and edge maps, rolling origins, horizons, normalization, covariates, graph provenance, paired seeds, tuning budget and final test separation. Predefine DLinear, persistence, CSA, Euclidean GCN and HGCN; graph-only and geometry-only ablations; accuracy, calibration where applicable, efficiency and numerical-stability outcomes; comparison family and correction."
    acceptance:
      - "custom:../../scripts/mintou/harness_reconstruction_v2_acceptance.py --project mintou_p2_hygraph_load_forecasting --phase protocol"
  - id: p4_v2_s05_pilot_activation_gate
    title: P4 graph, leakage and numerical-stability pilot
    objective: "Run one accepted graph dataset, one rolling origin and three to five paired seeds to validate temporal boundaries, train-only graph construction, Euclidean GCN learning, hyperbolic forward and backward passes, finite gradients, parameter and compute accounting, and deterministic metrics. Pilot outputs remain paper_use false."
    acceptance:
      - "custom:../../scripts/mintou/harness_reconstruction_v2_acceptance.py --project mintou_p2_hygraph_load_forecasting --phase pilot"
  - id: p4_v2_s06_formal_experiments_statistics
    title: P4 formal multi-origin graph and geometry evaluation
    objective: "Execute the frozen paired design over accepted datasets and rolling origins; compare DLinear, CSA, Euclidean GCN and HGCN at matched tuning and reporting budgets; use origin or dataset-origin as the outer unit; isolate graph and hyperbolic contributions; report uncertainty, corrected tests, compute, numerical failures and all null or adverse outcomes."
    acceptance:
      - "custom:../../scripts/mintou/harness_reconstruction_v2_acceptance.py --project mintou_p2_hygraph_load_forecasting --phase evidence"
  - id: p4_v2_s07_results_first_manuscript
    title: P4 evidence-first HGCN manuscript reconstruction
    objective: "Generate all tables and figures from the formal manifest, then rewrite Results, Data and Graph Construction, Model, Experimental Design, Discussion and Limitations before Related Work, Introduction, Abstract and Conclusion. The prose may describe HGCN only after implementation evidence exists; retain the predecessor Poincare-weighting null and DLinear advantage."
    acceptance:
      - narrative_structure
      - artifact_consistency
      - manuscript_hygiene
      - "custom:../../scripts/mintou/harness_reconstruction_v2_acceptance.py --project mintou_p2_hygraph_load_forecasting --phase evidence"
  - id: p4_v2_s08_pre_review_integrity
    title: P4 mandatory pre-review integrity gate
    objective: "Verify references, citation context samples, graph provenance, leakage tests, numerical and statistical lineage, originality and P4-C01 through P4-C08; clear or human-override all seven AI-research failure modes, with special attention to architecture relabeling, test-informed graph construction and weak-baseline selection."
    acceptance:
      - "custom:../../scripts/mintou/harness_reconstruction_v2_acceptance.py --project mintou_p2_hygraph_load_forecasting --phase pre_integrity"
  - id: p4_v2_s09_five_view_review
    title: P4 journal-fit and four technical reviewer pass
    objective: "Run Electronics fit, graph and hyperbolic learning, power-load forecasting, statistics and reproducibility, and devil's-advocate reviews. Consolidate evidence-linked issues on model identity, graph validity, leakage, baseline strength, multi-origin inference and practical value into one roadmap without suppressing dissent."
    acceptance:
      - "custom:../../scripts/mintou/harness_reconstruction_v2_acceptance.py --project mintou_p2_hygraph_load_forecasting --phase review"
  - id: p4_v2_s10_revision_and_rereview
    title: P4 evidence-bounded revision and re-review
    objective: "Resolve every roadmap item with location and evidence, rerun only under frozen change control, retain numerical failures and adverse rankings, and conduct independent re-review against original and revised hashes. Limit work to two full revision loops; failure of the genuine-HGCN or leakage gate makes the locked-title submission NO-GO."
    acceptance:
      - "custom:../../scripts/mintou/harness_reconstruction_v2_acceptance.py --project mintou_p2_hygraph_load_forecasting --phase re_review"
  - id: p4_v2_s11_final_integrity_language_pdf
    title: P4 final integrity, writing-regression and PDF gate
    objective: "Complete full reference and citation-context verification, model-code-equation audit, figure-table lineage audit and cold-reader prose regression. Improve readability without numerical, citation or claim-strength drift; compile and visually inspect the Electronics PDF with the exact locked title."
    acceptance:
      - latex_build
      - artifact_consistency
      - pdf_integrity
      - manuscript_hygiene
      - "custom:../../scripts/mintou/harness_reconstruction_v2_acceptance.py --project mintou_p2_hygraph_load_forecasting --phase final_integrity"
      - "custom:../../scripts/mintou/harness_acceptance.py --project mintou_p2_hygraph_load_forecasting --allow-human-placeholders"
  - id: p4_v2_s12_release_human_gate
    title: P4 reproducible package and human submission gate
    objective: "Hash and package LaTeX, PDF, figures, tables, code, data, graph construction and validation records; accept only human-confirmed CRediT, funding, conflicts, rights, correspondence and repository facts; recheck current Electronics instructions and stop for final corresponding-author approval."
    acceptance:
      - latex_build
      - no_placeholders
      - declarations
      - artifact_consistency
      - pdf_integrity
      - "custom:../../scripts/mintou/harness_reconstruction_v2_acceptance.py --project mintou_p2_hygraph_load_forecasting --phase release"
      - "custom:../../scripts/mintou/harness_acceptance.py --project mintou_p2_hygraph_load_forecasting"
---

# P4 v2 execution contract

- Locked title: `Graph Convolutional Network based on Hyperbolic Space for Power Load Forecasting`.
- Scientific priority: implement and identify a genuine leakage-free graph-convolutional model in hyperbolic space rather than rename the current attention model.
- Preserved adverse evidence: the current CSA is not a GCN; Poincare weighting is unresolved; DLinear is stronger on the existing exact hierarchy; time points and seeds are not independent temporal replications.
- Stop rule: without a valid graph, a Euclidean GCN sanity baseline and a genuine HGCN implementation, the locked-title Electronics submission is NO-GO.
- Resource control: pilot maximum five paired seeds; formal scale follows measured GPU or CPU cost; at most two manuscript revision loops and three integrity-correction passes.

