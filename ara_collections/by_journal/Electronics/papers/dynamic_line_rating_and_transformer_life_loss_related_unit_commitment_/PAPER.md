---
title: "Dynamic Line Rating and Transformer-Life-Loss-Related Unit Commitment Under Extreme High-Temperature Conditions"
authors: [Hong Zhou, Liang Lu, Ke Yang, Li Shen, Yiyu Wen, Qing Wang]
year: 2025
venue: "Electronics"
doi: "10.3390/electronics14204027"
ara_version: "1.0"
domain: "Power system operation / unit commitment optimization under extreme high-temperature conditions"
keywords: [extreme high-temperature conditions, unit commitment, dynamic line rating, transformer life loss, hot-spot temperature, thermal balance, wind curtailment, IEEE 39-bus]
claims_summary:
  - "Conductor ampacity falls as ambient temperature rises because reduced convective/radiative cooling raises temperature rise per unit current, so a thermal-balance DLR model recovers transfer capability that worst-case SLR discards."
  - "Transformer hot-spot temperature is co-driven by ambient temperature and load ratio; pricing thermal aging into dispatch shifts loading away from hot-region transformers and keeps hot-spot near the 98 C rated bound."
  - "Embedding temperature-dependent line ratings and transformer life-loss cost in one UC objective redistributes generation from hot, transmission-bottlenecked regions to cooler ones, jointly improving security and total operating economy."
  - "The transformer life-loss cost function is highly sensitive to temperature; the aging-aware model's relative benefit grows as the temperature scaling factor increases."
  - "The wind-curtailment penalty coefficient produces a U-shaped total-cost response as the system moves from curtailment-tolerant to high-cost full-absorption regimes."
abstract: "The increasing frequency of extreme high-temperature events has led to deteriorating thermal stability in power transmission lines and accelerated life of transformers. Conventional unit commitment (UC) employs static line rating (SLR) and neglects transformer lifetime degradation, posing hidden risks to system security in high-temperature and heavy-load scenarios. To address this challenge, this paper proposes a dispatch method that incorporates dynamic line rating (DLR) and transformer life loss under extreme high-temperature conditions. First, the conductor temperature-rise mechanism is formulated using the thermal balance theory, upon which a temperature-dependent DLR calculation model is developed. Second, the coupling relationship between transformer hot-spot temperature, load ratio, and ambient temperature is quantified, and an ambient temperature-driven transformer life cost function is formulated using linear damage accumulation theory. Finally, a unit commitment (UC) optimization model is established to minimize unit generation costs, transformer lifetime loss costs, and wind curtailment penalties costs, while satisfying power balance, transmission capacity, and other operational constraints. Simulation results on the IEEE 39-bus system demonstrate that, compared to conventional models, the proposed method improves transmission capacity utilization in high-temperature conditions by 12%, reduces transformer life loss costs by 69%, and lowers total operating costs by 4.9%."
collection: by_journal
journal: Electronics
ownership_status: external_published_paper_not_project_original
local_pdf: "papers/literature/target_journal_related/pdfs/p1_twin_gru_dispatch/p1_twin_gru_dispatch__02__dynamic_line_rating_and_transformer_life_loss_related_unit_commitment__2e4f3d4094.pdf"
---

# Dynamic Line Rating and Transformer-Life-Loss-Related Unit Commitment Under Extreme High-Temperature Conditions

## Overview

This paper proposes a day-ahead unit commitment (UC) dispatch method that internalizes two thermal
mechanisms usually ignored under extreme heat: (i) the temperature-driven loss of transmission-line
ampacity, captured by a dynamic line rating (DLR) model derived from conductor thermal-balance
theory, and (ii) accelerated transformer insulation aging, captured by an ambient-temperature-driven
transformer life-loss cost function built on the hot-spot temperature model and linear (Miner's-rule)
damage accumulation. Both are embedded as a temperature-dependent transmission-capacity constraint and
an additive life-loss cost term in a single mixed-integer UC objective that also minimizes generation
cost, start-up/shutdown cost, and wind-curtailment penalty. On the IEEE 39-bus system under an extreme
high-temperature typical day, the aging-aware "TL-TF" model redistributes generation away from hot,
transmission-bottlenecked regions, keeps transformer hot-spot temperature near the 98 C rated bound,
and improves total operating economy relative to a conventional static-rating model.

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | Observations (SLR conservatism, hot-spot aging) → gaps → key insight → assumptions |
| [claims.md](logic/claims.md) | 5 falsifiable claims (C01–C05) |
| [concepts.md](logic/concepts.md) | 8 key technical terms (DLR, hot-spot temperature, life-loss cost, GSDF, …) |
| [experiments.md](logic/experiments.md) | 5 declarative verification plans (E01–E05) |
| [related_work.md](logic/related_work.md) | Typed dependency graph over the 25 references |
| [solution/formulation.md](logic/solution/formulation.md) | UC objective + DLR and transformer life-loss constraints, Eq. numbers |
| [solution/method.md](logic/solution/method.md) | End-to-end DLR + hot-spot + UC method pipeline |
| [solution/constraints.md](logic/solution/constraints.md) | Boundary conditions, assumptions, known limitations |

### Physical Layer (`/src`)
| File | Description | Claims |
|------|-------------|--------|
| [environment.md](src/environment.md) | Solver/hardware/data reproducibility record | — |

Note: the paper prints no source code or pseudocode — only equations (transcribed into
`logic/solution/formulation.md`). Per the no-fabrication rule, `src/` holds only `environment.md`;
no code stub is manufactured from the prose/equation method.

### Exploration Graph (`/trace`)
| File | Description |
|------|-------------|
| [exploration_tree.yaml](trace/exploration_tree.yaml) | 16-node research DAG |

### Evidence (`/evidence`)
| File | Description |
|------|-------------|
| [README.md](evidence/README.md) | Full index of 4 tables + 6 figures |
