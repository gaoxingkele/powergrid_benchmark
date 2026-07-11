---
title: "Digital-Twin Siamese GRU for Similarity-Aware Multi-Objective Power Grid Dispatch under Load and Topology Uncertainty"
tag: "mintou"
paper_id: "mintou_p1"
status: "project_original_public_benchmark_v3"
target_journal: "IEEE Access"
backup_journal: "Electronics"
algorithm: "DSTAR-GRU"
---

# Digital-Twin Siamese GRU for Similarity-Aware Multi-Objective Power Grid Dispatch under Load and Topology Uncertainty

## Algorithm Identity

- Short name: `DSTAR-GRU`
- Full name: Digital-twin Siamese Temporal Alignment and Retrieval GRU
- Tag: `mintou`
- Target journal: IEEE Access
- Backup journal: Electronics

## Abstract

This ARA project studies DSTAR-GRU, a digital-twin Siamese GRU that learns dispatch-state transferability and couples retrieved operating analogues with constrained multi-objective dispatch decisions.

## Current Engineering Status

The ARA structure, experiment manifest, baseline/ablation matrix, deterministic synthetic smoke benchmark, and public RTS-GMLC benchmark-derived dispatch experiment are implemented.

Current public signal: DSTAR-GRU reaches composite dispatch score `0.73965420`, improving over the strongest baseline Renewable-First ED by `0.08%` and over the strongest ablation by `0.36%`. Rolling scenario windows show a `0.07%` gain over the strongest baseline, and the high-renewable stress subset shows a `0.72%` gain over the strongest baseline and `3.08%` over the strongest ablation.

Boundary: this remains a standard-library RTS-GMLC dispatch proxy, not AC-OPF or unit-commitment proof. Manuscript claims should focus on similarity-aware renewable-stress dispatch recommendation unless an OPF/UC validation layer is added.
