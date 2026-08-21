---
title: "Multi-Level Network Topology and Time Series Multi-Scenario Optimization Planning Method for Hybrid AC/DC Distribution Systems in Data Centers"
authors: [Bing Chen, Yongjun Zhang, Handong Liang]
year: 2025
venue: "Electronics"
journal: "Electronics"
volume: "14"
article: "264"
doi: "10.3390/electronics14020264"
collection: by_journal
ownership_status: external_published_paper_not_project_original
local_pdf: "papers/literature/target_journal_related/pdfs/p3_self_adaptive_mode_distribution_planning/p3_self_adaptive_mode_distribution_planning__08__multi_level_network_topology_and_time_series_mu__1468c373df.pdf"
ara_version: "1.0"
domain: "power systems — hybrid AC/DC distribution network planning for data centers"
keywords: [data center, AC/DC distribution system, network topology, time series multi-scenario, optimization planning, distributed generation, voltage source converter, DC-load penetration, IEEE33, Pareto optimization]
claims_summary:
  - "C01: DC share of the cost-optimal topology tracks data-center DC-load penetration, above a converter-cost threshold"
  - "C02: Grid-connection and large-capacity AC-generator buses resist DC conversion even at high penetration"
  - "C03: Cost-optimal DC conversion concentrates at feeder extremities"
  - "C04: Allowing line DC retrofit reallocates conversion from many per-unit converters to few shared ones, lowering total cost"
  - "C05: Eliminating converter links via DC sub-systems raises distributed-generation hosting capacity"
  - "C06: Probability-weighted time-series multi-scenario embedding makes the optimal topology scenario-dependent"
  - "C07: Reliability tier, not electrical load alone, sets the redundancy of the DC supply architecture"
  - "C08: Converting a branch to DC removes it from the AC voltage-stability drop mechanism"
  - "C09: Feeder pairs with unbalanced load rates are the practical DC-interconnection candidates"
abstract: "With the rapid development of the Internet, cloud computing, big data, artificial intelligence, and other information technologies, data centers have become a crucial part of modern society's infrastructure, which puts forward very high requirements for the safety and reliability of power supply. Most of the servers, networks, and other equipment in data centers are DC-driven loads, which can significantly enhance resource utilization efficiency by efficiently accessing the DC power supply through voltage source converter-based high-voltage direct current transmission and distribution technology. For this reason, this paper first proposes a multi-level network topology design method for AC/DC distribution systems in the context of data centers. Based on the analysis of the adaptability of AC/DC distribution systems in data center access, the design and analysis of its multi-level network topology is carried out at the physical level for the construction of hybrid AC/DC distribution systems in data center. On this basis, a time series multi-scenario planning model of AC/DC distribution system with distributed generation in data center is established, the configuration strategy of AC/DC distribution system is investigated, and a time series multi-scenario optimization planning method for hybrid AC/DC distribution systems in data centers is proposed. Finally, the validity of the proposed method is verified by simulation examples."
---

# Multi-Level Network Topology and Time Series Multi-Scenario Optimization Planning Method for Hybrid AC/DC Distribution Systems in Data Centers

## Overview

This paper addresses two coupled problems in powering DC-load-dominated data centers. First, at the physical level, it proposes a multi-level (reliability-tier-aware) network topology design for flexible-DC distribution: GB50174 grades A/B/C are mapped to Uptime/TIA Tiers I–IV, and for each tier a 750 V DC-bus supply architecture is designed (dual hot-standby buses for fault-tolerant tiers down to a single non-redundant path for basic tiers). Second, at the planning level, it builds a time-series multi-scenario optimization model that jointly decides line DC retrofit/new-build, distributed-generation siting/sizing, and converter placement, minimizing annual economic cost, annual network loss, and a max-line voltage-stability index over probability-weighted typical time-series scenarios; the multi-objective problem is solved by a hybrid chaotic binary PSO (SABPSO) with Pareto ranking and small-niche sharing.

Simulations on a 13-node system show the cost-optimal DC share of the topology growing in stages with data-center DC-load penetration (no retrofit at 0–40%, near-total DC except the grid-connection buses at 80%), and on a modified IEEE33 system the DC-enabled plan lowers total annual cost, network loss and voltage-stability index versus a DC-forbidden plan while hosting more distributed generation. A regional engineering case identifies unbalanced-load-rate feeder pairs as practical DC-interconnection candidates.

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | 4 observations → 2 gaps → key insight (converter-cost threshold) → 4 assumptions |
| [claims.md](logic/claims.md) | 9 falsifiable claims (C01–C09) |
| [concepts.md](logic/concepts.md) | 8 technical concepts |
| [experiments.md](logic/experiments.md) | 7 verification/analysis plans (E01–E07) |
| [related_work.md](logic/related_work.md) | 5 full RW blocks + brief entries for all 22 references |
| [solution/formulation.md](logic/solution/formulation.md) | Multi-level topology design (Part A) + objective functions Eqs. 1–7 (Part B) + constraints Eqs. 8–10 (Part C) |
| [solution/method.md](logic/solution/method.md) | SABPSO solver, Pareto/crowding/elite machinery, 14-step planning procedure, scenario generation |
| [solution/constraints.md](logic/solution/constraints.md) | Boundary conditions, assumptions, known limitations |

### Physical Layer (`/src`)
| File | Description | Claims |
|------|-------------|--------|
| [environment.md](src/environment.md) | Reproducibility record — no code released; simulation parameters and data sources | — |

### Exploration Graph (`/trace`)
| File | Description |
|------|-------------|
| [exploration_tree.yaml](trace/exploration_tree.yaml) | 17-node research DAG (questions → designs → experiments, incl. rejected generic topologies and the undefined-f4 gap) |

### Evidence (`/evidence`)
| File | Description |
|------|-------------|
| [README.md](evidence/README.md) | Full index of 9 tables + 11 figures (each with .md + .png) |
