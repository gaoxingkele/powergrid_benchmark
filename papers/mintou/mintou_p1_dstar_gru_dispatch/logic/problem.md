# Problem

Route A framework pivot (2026-07-15): repositioned from a method-superiority dispatch paper to a framework/benchmark paper.

## Downstream Task

Reproducible curtailment-risk early warning benchmarking, and systematic evaluation of retrieval-based operating-state decision support (short-horizon risk estimation and day-ahead onset warning).

## Gap (framework/benchmark positioning)

There is no reproducible, public curtailment-risk early-warning benchmark: existing curtailment studies use private system data or ad-hoc curtailment definitions, lack an onset/transition-slice protocol for the operationally relevant warning moments, and rarely apply seeded statistical protocols. Likewise, retrieval-based (analogue/similar-day) decision support is widely proposed for power systems but has never been systematically evaluated across horizons on a common public benchmark — in particular, whether retrieval helps or hurts is horizon-dependent and undocumented. This paper fills both gaps: (a) a method-agnostic benchmark (full-year RTS-GMLC, fixed 70% SNSP-type reference policy, onset-slice protocol, 10-seed Mann-Whitney/Holm), and (b) a complete characterization of learned-embedding Siamese retrieval on it, including significance-backed evidence that retrieval is beneficial at 1h and harmful for 24h onset warning, and honest negative findings (persistence/simple baselines dominate overall and day-ahead onset) that demonstrate the benchmark's discriminative power.

## Datasets

- RTS-GMLC (primary: full-year benchmark substrate)
