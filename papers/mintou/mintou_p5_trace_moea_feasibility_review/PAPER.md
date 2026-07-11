---
title: "Hybrid Multi-Objective Evolution for Traceable Power Grid Feasibility Review and Investment Effectiveness Optimization"
tag: "mintou"
paper_id: "mintou_p5"
status: "project_original_public_benchmark_v1"
target_journal: "IEEE Access"
backup_journal: "Energies"
algorithm: "TRACE-MOEA"
---

# Hybrid Multi-Objective Evolution for Traceable Power Grid Feasibility Review and Investment Effectiveness Optimization

## Algorithm Identity

- Short name: `TRACE-MOEA`
- Full name: Traceable Review-Aware Coevolutionary Multi-Objective Evolution
- Tag: `mintou`
- Target journal: IEEE Access
- Backup journal: Energies

## Abstract

This ARA project studies TRACE-MOEA, a traceable multi-objective optimization framework for benchmark-derived power grid feasibility review. The current public-data experiment derives project candidates from RTS-GMLC, SimBench, and the cached public NERC report manifest associated with the C2GES literature thread.

## Current Engineering Status

The ARA structure, experiment manifest, baseline/ablation matrix, deterministic synthetic smoke benchmark, and public benchmark-derived project review experiment are implemented.

Current public signal: TRACE-MOEA reaches mean hypervolume proxy `1.74461503`, exceeding the strongest baseline AHP-TOPSIS by `1.23%` and the strongest ablation by `3.71%`. Earlier weak and near-miss revisions are preserved in `evidence/runs/*_v1_weak.md`, `*_v2_weak.md`, and `*_v3_near_miss.md`.

Boundary: the experiment uses public grid statistics and public reliability-report metadata to evaluate traceable project portfolio review proxies. It still requires expert-labeled feasibility outcomes, calibrated costs, and engineering load-flow checks before final manuscript claims.
