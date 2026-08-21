---
title: "Research of Islanding Operation and Fault Recovery Strategies of Distribution Network Considering Uncertainty of New Energy"
authors: ["Zhichun Yang", "Ji Han", "Li Li", "Yuting Deng", "Fan Yang", "Yang Lei", "Huaidong Min", "Wei Hu", "Lei Su"]
year: 2023
venue: "Electronics"
doi: "10.3390/electronics12204230"
ara_version: "1.0"
domain: "Power systems — distribution network islanding, fault recovery, stochastic optimization"
keywords: ["distribution network", "islanding operation", "fault recovery", "uncertainty", "rolling optimization", "distributed generation", "second-order cone programming", "scenario reduction", "network reconstruction", "load weight"]
claims_summary:
  - "Weight-driven partition makes critical-load islanding emerge from the objective, not manual assignment."
  - "Distribution-based sampling plus K-means reduction compresses renewable uncertainty into a tractable, structure-preserving scenario set."
  - "Short-horizon rolling re-optimization absorbs renewable prediction error before it violates island safety limits."
  - "Post-restoration network reconstruction converts topology freedom into lower loss and higher minimum voltage."
  - "Propagating island-stage supply history into the recovery weight removes satisfaction blind spots a static weight leaves behind."
  - "Remaining dispatchable DG capacity conditions how much reconstruction can recover in economy and voltage."
  - "The optimization strategy is executable as a real-time hardware control loop (OPAL-RT + DSP)."
abstract: "With the problems of fault handling in the distribution network, few studies concern the correlation between islanding operation and fault recovery. Thus, this paper proposes an islanding operation and fault recovery strategy for the distribution network considering the uncertainty of new energy. Firstly, the objectives of the distribution network islanding division scheme and operation optimization are established. Combined with distribution network radiation constraints, islanding power supply capacity, safety constraints, and distributed generator (DG) operation constraints, a rolling optimization method is used to construct the distribution network islanding division and operation model. Secondly, in the fault recovery stage, considering the characteristics of the island operation stage, a node load weight value is designed. A distribution network fault recovery model is then constructed with the goals of ensuring greater load power supply recovery, improving electricity satisfaction, and reducing network losses and switching times. Thirdly, considering the randomness of intermittent DGs such as wind power and photovoltaics, an uncertainty model of intermittent DGs is constructed. A solution method for the distribution network islanding operation and fault recovery model considering uncertainty is proposed by combining scenario generation reduction methods and second-order cone programming theory. Finally, the proposed method's feasibility and effectiveness are verified using the improved IEEE 33-node distribution network. The results show that in the islanding division stage, the node voltage consistently remains between 1.08 pu and 1.1 pu when new energy achieves up to 34.09% and 48.65%, and the line losses represent approximately 0.22% to 0.26% of the total load when the initial energy levels of the storage are at 50% and 80%. In the fault recovery stage, compared to the method without network reconstruction, the system shows significant power loss reductions of approximately 11.9%, 13.6%, and 14.2% in three respective cases."
collection: "by_journal"
journal: "Electronics"
ownership_status: "external_published_paper_not_project_original"
local_pdf: "papers/literature/target_journal_related/pdfs/p4_resilience_distribution_planning/p4_resilience_distribution_planning__10__research_of_islanding_operation_and_fault_recovery_stra__ac45929807.pdf"
---

# Research of Islanding Operation and Fault Recovery Strategies of Distribution Network Considering Uncertainty of New Energy

## Overview

This paper couples the two stages of distribution-network fault handling — island division/operation
(while the upstream grid is down) and fault recovery (after it returns) — which prior work treated
separately. Three mechanisms carry the contribution: (i) a **rolling optimization** scheme
(ΔT = 15 min, commit-one-step with feedback correction, threshold-triggered re-partitioning) that
replaces fixed 24-h look-ahead planning under uncertain troubleshooting time; (ii) a **stage-coupling
recovery load weight** β (Eq. 36) that adds, on top of the static importance weight α, penalties for
island-membership churn and no-supply periods a node endured during islanding — so recovery
re-energizes loads a static-weight method (β = α) provably leaves behind; and (iii) a
**scenario-weighted mixed-integer SOCP** (Weibull wind / normal PV-error models, Latin hypercube
generation of 500 scenarios, K-means reduction to 5 plus two extreme scenarios) solved with CPLEX
12.10. On an improved IEEE 33-node network with 4 DGs, islanded node voltages stay within
1.08–1.1 pu at up to 34.09% wind / 48.65% PV share and across 20 random scenarios; recovery-stage
reconstruction cuts losses ≈11.9% / 13.6% / 14.2% in three fault cases while raising the minimum
node voltage. An OPAL-RT + DSP semi-physical experiment verifies the strategy runs as a real-time
hardware control loop.

## Layer Index

### Cognitive Layer (`/logic`)
| File | Description |
|------|-------------|
| [problem.md](logic/problem.md) | 5 observations → 3 gaps → key insight (stage coupling via β + rolling SOCP) → assumptions |
| [claims.md](logic/claims.md) | 7 falsifiable mechanism claims (C01–C07) |
| [concepts.md](logic/concepts.md) | 11 technical terms (islanding/recovery stages, rolling optimization, α/β weights, radiality, SOC relaxation, scenario methods, Ψcom, semi-physical simulation) |
| [experiments.md](logic/experiments.md) | 11 verification plans (E01–E11), directional only |
| [related_work.md](logic/related_work.md) | 11 RW blocks + brief footprint for the remaining refs [1–31] |
| [solution/method.md](logic/solution/method.md) | End-to-end two-stage pipeline, test system, reconfiguration behaviors, semi-physical setup |
| [solution/islanding_formulation.md](logic/solution/islanding_formulation.md) | Islanding objective (Eq. 1), rolling scheme, re-partition trigger (Eq. 2) |
| [solution/recovery_formulation.md](logic/solution/recovery_formulation.md) | Recovery objective (Eq. 35), stage-coupling weight β (Eq. 36), recovery constraints (Eqs. 37–39) |
| [solution/uncertainty_method.md](logic/solution/uncertainty_method.md) | Wind/PV models (Eqs. 40–42), scenario generation/reduction, SOCP shell (Eqs. 43–48) |
| [solution/constraints.md](logic/solution/constraints.md) | Full constraint catalogue (Eqs. 2–39), assumptions, limitations |

### Physical Layer (`/src`)
| File | Description | Claims |
|------|-------------|--------|
| [environment.md](src/environment.md) | CPLEX 12.10; OPAL-RT + DSP rig; Hubei wind data; JZ818 metering; reproduction gaps | — |

No `src/execution/` code: the paper releases no code and prints no pseudocode beyond the K-means
steps already captured in `logic/solution/uncertainty_method.md`; the method lives in `logic/solution/`.

### Exploration Graph (`/trace`)
| File | Description |
|------|-------------|
| [exploration_tree.yaml](trace/exploration_tree.yaml) | 19-node research DAG (1 root question, 5 decisions, 11 experiments, 1 explicit dead end, 1 open question) |

### Evidence (`/evidence`)
| File | Description |
|------|-------------|
| [README.md](evidence/README.md) | Full index: 5 tables + 24 figures, each filed as .md + .png |
| tables/table1–5 | DG parameters; load weights; loss & voltage before/after reconstruction (3 fault cases) |
| figures/figure1–24 | Topology, scenario sets, island partition, per-period voltages/dispatch, box plots, reconfiguration results, β=α comparison, semi-physical framework and waveforms |
| [proofs/socp_relaxation.md](evidence/proofs/socp_relaxation.md) | SOC relaxation + scenario-weighted stochastic form (reconstructed derivation) |
