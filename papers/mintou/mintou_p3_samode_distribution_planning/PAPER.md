---
title: "Self-Adaptive Multi-Objective Differential Evolution for Reproducible Distribution Network Planning with DER and Storage Integration"
tag: "mintou"
paper_id: "mintou_p3"
status: "project_original_public_benchmark_v5"
target_journal: "Energies"
backup_journal: "Applied Sciences"
algorithm: "CARS-MODE"
---

# Self-Adaptive Multi-Objective Differential Evolution for Reproducible Distribution Network Planning with DER and Storage Integration

## Algorithm Identity

- Short name: `CARS-MODE`
- Full name: Constraint-Aware Repair and Strategy-adaptive Multi-Objective Differential Evolution
- Tag: `mintou`
- Target journal: Energies
- Backup journal: Applied Sciences

## Abstract

This ARA project studies CARS-MODE, a constraint-aware and strategy-adaptive differential evolution algorithm for distribution planning portfolios.

## Current Engineering Status

The ARA structure, experiment manifest, baseline/ablation matrix, deterministic synthetic smoke benchmark, and public SimBench benchmark-derived planning experiment are implemented.

Current public signal: the DER/storage stress v5 benchmark gives CARS-MODE mean hypervolume proxy `0.55322842`, exceeding the strongest baseline NSGA-II by `0.46%` and the strongest ablation FixedDE by `0.19%`. Earlier weak and near-miss revisions are preserved in the evidence tree.

Boundary: the current result is a narrow proxy-level signal, not a full engineering planning claim. It still requires pandapower/AC load-flow validation, repeated scenario variance, and calibrated investment assumptions before manuscript-level electrical claims.
