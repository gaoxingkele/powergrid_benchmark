---
title: "Multi-Timescale Coordinated Planning of Wind, Solar, and Energy Storage Considering Generalized Adequacy"
authors:
  - Jian Yin
  - Lixiang Fu
  - Liming Xiao
  - Zijian Meng
  - Yuejun Luo
  - Zili Chen
  - Zhaoyuan Wu
year: 2025
venue: "Energies"
journal: "Energies"
doi: "10.3390/en18185024"
ara_version: "1.0.0"
domain: "Power System Planning, Resource Adequacy, Renewable Energy Integration"
collection: "by_journal"
ownership_status: "external_published_paper_not_project_original"
local_pdf: "D:/aicoding/powergrid_benchmark/papers/literature/target_journal_related/pdfs/p5_hybrid_moea_feasibility_review/p5_hybrid_moea_feasibility_review__07__multi_timescale_coordinated_planning_of_wind_solar_and_en__872293ee4b.pdf"
keywords:
  - generalized adequacy
  - coordinated planning framework
  - flexibility adequacy
  - inertia adequacy
  - multi-timescale energy storage
  - renewable energy utilization
  - PROMETHEE-II
claims_summary:
  - C01: Generalized adequacy framework integrates power/energy, flexibility, and inertia adequacy into a unified planning paradigm, revealing interdependencies previously treated in isolation.
  - C02: Coordinated planning of wind, solar, short-term and long-term energy storage, and transmission reduces loss-of-load hours by more than half compared to traditional approaches.
  - C03: Dynamic frequency security constraints in the planning model ensure system inertia margin remains positive, preventing frequency instability in high-renewable scenarios.
  - C04: Incorporating low-probability extreme weather scenarios into planning significantly reduces Conditional Value at Risk of energy not served, mitigating tail-risk supply shortages.
  - C05: PROMETHEE-II with combined AHP-entropy weighting enables systematic scheme comparison across economic, technical, and environmental dimensions.
abstract: |
  The core of power system planning lies in optimizing resource portfolios to ensure reliable
  electricity supply, with generalized adequacy serving as a key indicator of supply security.
  As the share of renewable energy increases, the mechanisms underlying system security
  undergo profound changes, extending the concept of adequacy from mere power balance to
  encompass flexibility and inertia support while exhibiting spatial and temporal heterogeneity
  and wide-area characteristics. Traditional planning approaches can no longer meet these
  evolving requirements. To address this, a power grid coordinated planning framework is
  proposed based on generalized adequacy, which integrates power and energy adequacy,
  flexibility adequacy, and inertia adequacy. Within this framework, generalized adequacy
  metrics and their quantification methods are developed, and a coordinated planning strategy
  for wind power, photovoltaic power, multi-timescale energy storage, and transmission
  expansion is introduced to enhance renewable energy utilization and meet flexibility needs
  across multiple timescales. Furthermore, a scheme evaluation and selection method based
  on generalized adequacy is proposed. Finally, the effectiveness of the proposed approach is
  validated through case studies on the IEEE 24-bus system.
---

# Layer Index

| Layer | Path | Description |
|-------|------|-------------|
| Cognitive | `logic/problem.md` | Problem formulation: limitations of traditional adequacy, gaps in fragmented planning approaches |
| Cognitive | `logic/claims.md` | Five falsifiable claims (C01--C05) about generalized adequacy and coordinated planning |
| Cognitive | `logic/concepts.md` | Formal definitions of generalized adequacy, flexibility/inertia adequacy metrics |
| Cognitive | `logic/experiments.md` | Four planning scenarios (M1--M4) comparing resource configurations and adequacy outcomes |
| Cognitive | `logic/solution/constraints.md` | Model limitations: scope boundaries, linearization assumptions, omitted resource types |
| Cognitive | `logic/related_work.md` | Typed dependency graph covering adequacy metrics, planning models, MCDM methods |
| Physical | `src/environment.md` | Reproducibility: IEEE 24-bus test system, software dependencies, parameter sources |
| Trace | `trace/exploration_tree.yaml` | Research DAG: central questions, scenarios, design decisions, dead ends |
| Evidence | `evidence/README.md` | Evidence ledger: 8 tables, 10 figures, source pages, extraction methods |
| Evidence | `evidence/tables/` | Tables 1--8 with transcriptions and screenshots |
| Evidence | `evidence/figures/` | Figures 1--10 with visual descriptions and screenshots |
