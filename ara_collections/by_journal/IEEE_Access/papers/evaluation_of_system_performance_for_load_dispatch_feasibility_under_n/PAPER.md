---
title: "Evaluation of System Performance for Load Dispatch Feasibility Under N-1 Generator Contingencies in Day-Ahead Unit Commitment"
authors: ["Smriti Jain", "Neeraj Kanwar"]
year: 2025
venue: "IEEE Access"
doi: "10.1109/ACCESS.2025.3620435"
ara_version: "1.0"
domain: "Power systems engineering — day-ahead unit commitment, contingency analysis, reliability"
keywords: ["N-1 generator contingency", "operating margin", "system reliability", "system criticality", "system robustness", "thermal generation", "unit commitment", "LOLP", "contingency margin", "dynamic programming"]
collection: "by_journal"
journal: "IEEE Access"
ownership_status: "external_published_paper_not_project_original"
local_pdf: "papers/literature/target_journal_related/pdfs/p1_twin_gru_dispatch/p1_twin_gru_dispatch__06__evaluation_of_system_performance_for_load_dispatch_feasibility_under_n__a902907c80.pdf"
claims_summary:
  - "A single unified framework of criticality, robustness, LOLP reliability, and a new operating-margin metric exposes DA-UC vulnerabilities that cost-only optimization hides."
  - "Under N-1 generator outages, the loss of the largest-capacity generators drives the greatest UC-cost escalation and identifies the weakest buses of the network."
  - "Spinning-reserve level (and the contingency margin it produces) trades off directly against reliability: raising reserve improves LOLP and operating margin but raises cost and consumes dispatchable headroom."
  - "A negative operating margin flags an infeasible/at-limit DA-UC schedule; a positive margin quantifies residual headroom for absorbing further contingencies."
  - "N-1 generator contingencies with a 10% spinning reserve do not threaten supply-demand balance; they only raise cost for a subset of contingencies while the schedule stays feasible."
abstract: "Day Ahead (DA) Unit Commitment (UC) enhances system preparedness for real-time dispatch. N-1 thermal generator contingencies challenge the reliability of DA UC. This paper proposes a methodology to evaluate the impact of individual generator outages on UC operational cost, reliability, and operating margin of the scheduled DA dispatch plan, aiding better real-time dispatch decisions. System performance is assessed using criticality, robustness, reliability, and operating margin, with the Contingency Margin (CM) as an implementation indicator. The approach identifies robust and weak buses to determine system robustness and criticality. The paper addresses system reliability during contingencies via the Loss Of Load Probability (LOLP) index. Analysis includes three case studies: Base Case, Case 1, and Case 2. The Base Case executes DA UC without n-1 contingencies. Case 1 analyzes n-1 thermal generator contingency-based DA UC with a CM corresponding to a 10% spinning reserve. Weak and robust buses are identified in Case 1. In Case 2(a), 2(b) and 2(c), CM is evaluated with a gradual reduction in spinning reserve from 10% to 8%, then to 5%, and finally to 0%, while executing n-1 generator contingencies for DA UC. System performance is assessed using the proposed parameters and methodology. The Dynamic Programming technique optimizes DA UC, analyzed on the 24-bus, 26-generator IEEE Reliability Test System. Across all cases, DA UC costs range from $774,020 to $895,400 under varying contingencies. Critical generators (IDs 6, 7) and weak buses (Buses 18, 21) are consistently identified. CM improves from 0 MW in Case 2(c) to 310.5 MW in Case 1; LOLP reduces from 0.0501 to 0; and the operating margin increases from -0.0001 to 0.05. Results confirm that the proposed methodology effectively identifies system vulnerabilities and quantifies the impact of reserve levels on dispatch feasibility, emphasizing the importance of incorporating contingency-aware planning in DA UC and reserve allocation strategies. It provides a practical tool for operators to enhance DA UC planning, reserve allocation, and grid resilience under contingency conditions."
---

# Evaluation of System Performance for Load Dispatch Feasibility Under N-1 Generator Contingencies in Day-Ahead Unit Commitment

## Overview

This paper proposes a structured, contingency-aware framework for evaluating whether a Day-Ahead
Unit Commitment (DA UC) schedule will remain feasible in real time when any single thermal
generator is lost (an N-1 generator contingency). Existing DA UC work optimizes cost under
predicted conditions but does not jointly quantify how prepared a schedule is for outages. The
authors introduce four system-performance parameters — criticality, robustness, reliability
(via LOLP), and a newly formulated operating margin — with the Contingency Margin (CM, the
aggregate spinning reserve) as the implementation lever. The methodology is applied to the 24-bus,
26-generator IEEE Reliability Test System, with DA UC solved by Dynamic Programming in MATLAB, over
a Base Case (no contingency), Case 1 (N-1 with 10% spinning reserve / CM = 310.5 MW), and Case 2
sweeping the reserve down through 8%, 5%, and 0% (CM = 248, 155, 0 MW). The framework consistently
flags the two 400 MW generators at buses 18 and 21 as the weakest (most critical contingencies
Cy6, Cy7) and buses 13/15 as the most robust, and shows the reserve-vs-reliability trade-off:
LOLP falls from 0.050113 (Case 1) to 0 (Case 2c) while operating margin rises from -0.000113 to
0.05, at the cost of exhausting dispatchable headroom.

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations → gaps → key insight → assumptions |
| [claims.md](logic/claims.md) | 8 falsifiable claims (C01–C08) |
| [concepts.md](logic/concepts.md) | 12 key technical terms, formally defined |
| [experiments.md](logic/experiments.md) | 7 declarative verification plans (E01–E07) |
| [related_work.md](logic/related_work.md) | Typed dependency graph over the paper's 44 references |
| [solution/constraints.md](logic/solution/constraints.md) | Assumptions, boundary conditions, limitations |
| [solution/formulation.md](logic/solution/formulation.md) | DA UC objective, constraints, CM/LOLP/margin math (Eq. 1–16) |
| [solution/method.md](logic/solution/method.md) | 5-step performance-assessment methodology + 3-case study design |

### Physical Layer (`/src`)
| File | Description |
|------|-------------|
| [environment.md](src/environment.md) | Test system, solver, data sources, protocols |

### Exploration Graph (`/trace`)
| File | Description |
|------|-------------|
| [exploration_tree.yaml](trace/exploration_tree.yaml) | Research DAG (question → cases → metrics → dead ends) |

### Evidence (`/evidence`)
| File | Description |
|------|-------------|
| [README.md](evidence/README.md) | Full index of 13 tables + 10 figures |
