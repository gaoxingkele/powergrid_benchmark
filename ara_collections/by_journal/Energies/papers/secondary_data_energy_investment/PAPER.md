---
title: "A Secondary-Data-Driven Decision Support Framework for Strategic Energy Investment Prioritization: An Explainable Multi-Criteria Application Across Countries"
authors:
  - name: "Filiz Mizrak"
    affiliation: "Management Information Systems, Atlas University, 34408 Istanbul, Turkiye"
    email: "filiz.mizrak@atlas.edu.tr"
    role: "Conceptualization, methodology, formal analysis, investigation, resources, supervision, project administration"
  - name: "Okan Yasar"
    affiliation: "Information Security Technology, Bahcesehir University, 34353 Istanbul, Turkiye"
    email: "okan.yasar@bau.edu.tr"
    role: "Software, validation, formal analysis, data curation, visualization, funding acquisition"
year: 2026
venue: "Energies"
doi: "10.3390/en19143243"
ara_version: "1.0"
domain: "Energy Systems, Multi-Criteria Decision Making, Decision Support Systems"
keywords:
  - "strategic energy investment"
  - "secondary data"
  - "decision support system (DSS)"
  - "explainable multi-criteria decision-making (MCDM)"
  - "energy transition readiness"
  - "persona-based ranking"
  - "entropy weighting"
  - "CRITIC weighting"
  - "fairness diagnostics"
  - "simulated-agent validation"
claims_summary:
  - "C01: Secondary-data-driven MCDM frameworks produce reproducible, stakeholder-sensitive country-level energy investment readiness rankings that differ from expert-only linguistic scoring approaches."
  - "C02: Strategic energy investment readiness is multidimensional and cannot be captured by a single indicator, requiring integration of macroeconomic, institutional, energy-security, sustainability, market, and technical-resource criteria."
  - "C03: Persona-based weighting yields different country prioritizations across stakeholder types (public planners, private investors, grid operators, sustainability policymakers, infrastructure funds), demonstrating that readiness is stakeholder-sensitive."
  - "C04: The proposed readiness index captures dimensions beyond GDP per capita and institutional maturity, as shown by fairness diagnostics and partial-correlation analyses."
  - "C05: Baseline rankings remain broadly stable under entropy, CRITIC, hybrid entropy-CRITIC weighting, persona-weight perturbation, and simulated-agent preference heterogeneity (median Spearman = 0.932)."
abstract: "This study develops a secondary-data-driven decision support framework for prioritizing strategic energy investment readiness across countries. The empirical application covers 36 countries and 18 criteria grouped under macroeconomic feasibility, institutional capacity, energy security, sustainability and decarbonization, market and demand conditions, and technical resource potential. The study responds to a methodological gap in energy investment prioritization by moving from expert-only linguistic scoring toward a reproducible, explainable, stakeholder-sensitive, and validation-oriented multi-criteria decision support structure. In the implemented empirical model, public secondary data are transformed into a normalized country-level decision matrix, baseline readiness scores are calculated using equal weights, and entropy, CRITIC, and hybrid entropy-CRITIC configurations are used as objective weighting benchmarks. LLM-assisted extraction is used as a documented criterion-discovery and screening aid, not as an autonomous scoring, weighting, or ranking mechanism. The fuzzy component is specified as an uncertainty-sensitive extension and illustrated through panel-based fuzzy interval construction for selected time-series indicators, while the main baseline ranking is based on the latest available normalized data matrix. The results show meaningful cross-country variation, with top-10 readiness scores ranging from 0.675 to 0.537 and the lowest five scores ranging from 0.364 to 0.338. Persona-based results indicate that country priorities differ across public planners, private investors, grid operators, sustainability policymakers, and infrastructure funds, while robustness checks show broad ranking stability, with Spearman correlations between 0.892 and 0.986 and a median simulated-agent correlation of 0.932. Fairness and partial-correlation diagnostics suggest that the model captures multidimensional readiness rather than simply reproducing wealth or existing renewable capacity. Post-hoc validation against observable investment- and transition-related benchmarks further supports the convergent validity of the readiness index."
collection: by_journal
journal: "Energies"
ownership_status: external_published_paper_not_project_original
local_pdf: "papers/literature/target_journal_related/pdfs/p5_hybrid_moea_feasibility_review/p5_hybrid_moea_feasibility_review__02__a_secondary_data_driven_decision_support_framework_for_st__fc9ef6cebc.pdf"
---

# Overview

This paper proposes and demonstrates a secondary-data-driven decision support framework (DSS) for comparing strategic energy investment readiness across countries. The empirical application evaluates 36 countries across 18 criteria organized into six dimensions: macroeconomic feasibility, institutional capacity, energy security, sustainability and decarbonization, market and demand conditions, and technical resource potential. The framework integrates objective weighting benchmarks (entropy, CRITIC, hybrid), persona-based stakeholder ranking, explainability decomposition, fairness diagnostics, external validation, and simulated-agent robustness analysis. LLM-assisted extraction is used as a documented criterion-discovery aid, while fuzzy intervals are treated as an uncertainty-sensitive extension rather than the primary ranking engine.

## Layer Index

| Layer | File | Description |
|-------|------|-------------|
| **Meta** | `PAPER.md` | Paper metadata, overview, layer index |
| **Logic** | `logic/problem.md` | Research problem: observations, gaps, key insight, assumptions |
| **Logic** | `logic/claims.md` | Claims C01-C05 with conditions, falsification, evidence basis |
| **Logic** | `logic/concepts.md` | Key technical concepts with notation, definitions, boundary conditions |
| **Logic** | `logic/experiments.md` | Experiments E01-E06 with verification, setup, metrics |
| **Logic** | `logic/related_work.md` | Citation footprint with typed dependencies |
| **Logic** | `logic/solution/constraints.md` | Boundary conditions, assumptions, known limitations |
| **Logic** | `logic/solution/method.md` | The proposed DSS architecture (8-stage methodology) |
| **Logic** | `logic/solution/formalization.md` | Mathematical formalization of the MCDM framework |
| **Source** | `src/environment.md` | Reproducibility info, software, data sources |
| **Trace** | `trace/exploration_tree.yaml` | Research exploration DAG |
| **Evidence** | `evidence/README.md` | Evidence index mapping files to claims |
| **Evidence** | `evidence/tables/table1.md` | Table 1: Criteria, measurement units, direction, and main source |
| **Evidence** | `evidence/tables/table2.md` | Table 2: Highest and lowest baseline readiness scores |
| **Evidence** | `evidence/tables/table3.md` | Table 3: Convergent validity against benchmarks |
| **Evidence** | `evidence/tables/table4.md` | Table 4: Alternative weighting assumptions |
| **Evidence** | `evidence/tables/table5.md` | Table 5: Stakeholder-persona dimension weights |
| **Evidence** | `evidence/tables/table6.md` | Table 6: Stakeholder-specific top-ranked countries |
| **Evidence** | `evidence/tables/table7.md` | Table 7: Fairness/wealth-institutional associations |
| **Evidence** | `evidence/tables/table8.md` | Table 8: Ranking stability under multiple scenarios |
| **Evidence** | `evidence/figures/figure1.md` | Figure 1: Workflow of the proposed DSS architecture |
| **Evidence** | `evidence/figures/figure2.md` | Figure 2: Data-flow architecture of the proposed DSS |
| **Evidence** | `evidence/figures/figure3.md` | Figure 3: Dimension-level readiness profiles |
| **Evidence** | `evidence/figures/figure4.md` | Figure 4: Contribution-based readiness profiles |
| **Evidence** | `evidence/figures/figure5.md` | Figure 5: Readiness score vs GDP per capita |
