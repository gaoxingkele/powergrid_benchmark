---
title: "Transmission and Generation Expansion Planning Considering Virtual Power Lines/Plants, Distributed Energy Injection and Demand Response Flexibility from TSO-DSO Interface"
authors:
  - "Flávio Arthur Leal Ferreira"
  - "Clodomiro Unsihuay-Vila"
  - "Rafael A. Núñez-Rodríguez"
year: 2025
venue: "Energies"
doi: "10.3390/en18071602"
ara_version: "1.0"
domain: "Power Systems — Transmission and Generation Expansion Planning"
keywords:
  - "expansion planning"
  - "energy storage"
  - "virtual power line"
  - "data-driven distributionally robust optimization"
  - "TSO-DSO interface"
  - "demand response flexibility"
claims_summary: >-
  The paper proposes a computational model for transmission and generation expansion planning (TGEP) that incorporates virtual power lines (VPL) via battery energy storage systems, virtual power plants (VPP), and TSO-DSO interface flexibility. The model demonstrates cost reductions of approximately 15%, improvements in transmission system utilization of approximately 20%, and improved locational marginal pricing indicators.
abstract: >-
  This article presents a computational model for transmission and generation expansion planning considering the impact of virtual power lines, which consists of the investment in energy storage in the transmission system as well as being able to determine the reduction and postponement of investments in transmission lines. The flexibility from the TSO-DSO interconnection is also modeled, analyzing its impact on system expansion investments. Flexibility is provided to the AC power flow transmission network model by distribution systems connected at the transmission system nodes. The transmission system flexibility requirements are provided by expansion planning performed by the connected DSOs. The objective of the model is to minimize the overall cost of system operation and investments in transmission, generation and flexibility requirements. A data-driven distributionally robust optimization-DDDRO approach is proposed to consider uncertainties of demand and variable renewable energy generation. The column and constraint generation algorithm and duality-free decomposition method are adopted. Case studies using a Garver 6-node system and the IEEE RTS-GMLC were carried out to validate the model and evaluate the values and impacts of local flexibility on transmission system expansion. The results obtained demonstrate a reduction in total costs, an improvement in the efficient use of the transmission system and an improvement in the locational marginal price indicator of the transmission system.
collection: by_journal
journal: Energies
ownership_status: external_published_paper_not_project_original
local_pdf: "D:\\aicoding\\powergrid_benchmark\\papers\\literature\\target_journal_related\\pdfs\\p3_self_adaptive_mode_distribution_planning\\p3_self_adaptive_mode_distribution_planning__07__transmission_and_generation_expansion_planning__89f570db56.pdf"

# Layer Index
layers:
  semantic:
    - "Problem formulation (deterministic model): Section 2"
    - "Net demand model with load duration curve: Section 2.1"
    - "Flexibility (upward/downward): Section 2.2"
    - "Virtual power lines (VPL): Section 2.3"
    - "Virtual power plants (VPP): Section 2.4"
    - "Objective function and constraints: Sections 2.5-2.16"
    - "Uncertainty modeling via DDDRO: Section 3"
    - "Solution procedure: Section 4"
    - "Case studies: Garver 6-node and IEEE RTS-GMLC: Section 5"
  cognitive:
    - "logic/problem.md"
    - "logic/claims.md"
    - "logic/concepts.md"
    - "logic/experiments.md"
    - "logic/related_work.md"
    - "logic/solution/constraints.md"
  artifact:
    - "src/environment.md"
  evidence:
    - "evidence/README.md"
    - "evidence/figures/"
    - "evidence/tables/"
  trace:
    - "trace/exploration_tree.yaml"
---
