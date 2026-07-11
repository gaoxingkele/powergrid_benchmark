---
title: "Hyperbolic Graph Neural Forecasting for Hierarchical Power Load Prediction in Smart Dispatch Systems"
tag: "mintou"
paper_id: "mintou_p2"
status: "project_original_public_benchmark_v4"
target_journal: "Electronics"
backup_journal: "Applied Sciences"
algorithm: "HyG-LoadFormer"
---

# Hyperbolic Graph Neural Forecasting for Hierarchical Power Load Prediction in Smart Dispatch Systems

## Algorithm Identity

- Short name: `HyG-LoadFormer`
- Full name: Hyperbolic Graph Load Forecasting Transformer
- Tag: `mintou`
- Target journal: Electronics
- Backup journal: Applied Sciences

## Abstract

This ARA project studies HyG-LoadFormer, a hyperbolic graph forecasting model for hierarchical load prediction and downstream dispatch sensitivity analysis.

## Current Engineering Status

The ARA structure, experiment manifest, baseline/ablation matrix, deterministic synthetic smoke benchmark, public OPSD/SimBench benchmarks, and rolling temporal split checks are implemented.

Current public signal: HyG-LoadFormer is strongest for day-ahead/24h forecasting. On OPSD, fixed split 24h MAPE is `0.03972575` versus the best baseline `0.05632632`, and rolling 24h mean MAPE is `0.03931968` versus `0.05471780`. On SimBench, fixed split 24h normalized MAE is `0.07822078` versus the best baseline `0.08103131`, and rolling 24h normalized MAE is `0.07951836` versus `0.08361752`.

Boundary: 1h forecasting remains a recorded limitation. OPSD 1h is weaker than the NoCalendar ablation, and SimBench 1h reaches only baseline-level or near-baseline behavior. Manuscript claims should therefore target day-ahead hierarchical load forecasting unless a stronger short-horizon model is added.
