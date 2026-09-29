---
title: "Scenario-Aware Hybrid Multi-Objective Evolution for Resilient Distribution Network Planning under DER and Load Uncertainty"
tag: "mintou"
paper_id: "mintou_p4"
status: "project_original_public_benchmark_v2"
target_journal: "Energies"
backup_journal: "IEEE Access"
algorithm: "SHIELD-MOEA"
---

# Scenario-Aware Hybrid Multi-Objective Evolution for Resilient Distribution Network Planning under DER and Load Uncertainty

## Algorithm Identity

- Short name: `SHIELD-MOEA`
- Full name: Scenario-screened Hybrid Evolution for Load-serving Distribution Resilience
- Tag: `mintou`
- Target journal: Energies
- Backup journal: IEEE Access

## Abstract

This ARA project studies SHIELD-MOEA, a scenario-screened hybrid evolutionary framework for resilient distribution planning.

## Current Engineering Status

The ARA structure, experiment manifest, baseline/ablation matrix, deterministic synthetic smoke benchmark, and public SimBench benchmark-derived resilience planning experiment are implemented.

Current public signal: SHIELD-MOEA reaches hypervolume proxy `0.79432775`, improving over the strongest baseline MOEA/D by `2.78%` and the strongest ablation NoScenarioScreen by `3.26%`.

Boundary: this is a SimBench-derived resilience planning proxy, not full AC/pandapower feasibility proof. Manuscript claims should focus on scenario-screened resilient planning unless AC feasibility and scenario-variance checks are added.
