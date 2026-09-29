---
title: "Non-Dominated Sorting with Bidirectional Local Search for Budget-Constrained Power Grid Project Review"
tag: "mintou"
paper_id: "mintou_p6"
status: "project_original_public_benchmark_v1"
target_journal: "Applied Sciences"
backup_journal: "IEEE Access"
algorithm: "BiLo-NSGA"
---

# Non-Dominated Sorting with Bidirectional Local Search for Budget-Constrained Power Grid Project Review

## Algorithm Identity

- Short name: `BiLo-NSGA`
- Full name: Bidirectional Local-search Non-dominated Sorting Genetic Algorithm
- Tag: `mintou`
- Target journal: Applied Sciences
- Backup journal: IEEE Access

## Abstract

This ARA project studies BiLo-NSGA, a non-dominated sorting algorithm with forward and backward local search for budget-constrained power grid project review. The current public-data experiment derives project candidates from RTS-GMLC, SimBench, and the cached public NERC report manifest associated with the C2GES literature thread.

## Current Engineering Status

The ARA structure, experiment manifest, baseline/ablation matrix, deterministic synthetic smoke benchmark, and public benchmark-derived project review experiment are implemented.

Current public signal: BiLo-NSGA reaches mean hypervolume proxy `1.70989680`, exceeding the strongest baseline AHP-TOPSIS by `3.87%` and the strongest ablation by `3.57%`.

Boundary: the experiment uses public grid statistics and public reliability-report metadata to evaluate budget-constrained project portfolio review proxies. It still requires expert-labeled feasibility outcomes, calibrated costs, and engineering load-flow checks before final manuscript claims.
