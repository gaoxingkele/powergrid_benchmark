# Original-Title Dual Manuscript Reconstruction Protocol

Protocol identifier: `APPLSCI-ORIGINAL-TITLE-DUAL-v1.0-draft`

## Goal

Produce two submission-quality *Applied Sciences* manuscripts while preserving
the author-supplied titles:

1. *Causal and Counterfactual Graph-Enhanced Extractive Summarization (C²GES)
   for Power Grid Maintenance Reports*;
2. *MA-SQLGrid: A Robust Multi-Agent Framework for Text-to-SQL in Power Grid
   Databases*.

## Evidence boundary

- The 2026-08-08 morning review and complete packages are immutable evidence
  sources, not self-contained implementations of every title claim.
- Hash-consistent, independently audited results may be inherited without a
  new generation run.
- A changed executable, evaluator, dataset, prediction path, or title-level
  construct requires a new frozen experiment or explicit diagnostic labeling.
- Machine-silver annotations are never described as human or domain-expert
  ground truth.
- No metric, citation, expert judgment, or run completion may be inferred from
  a planned experiment.

## Three-round version contract

Each paper shall have `R1`, `R2`, and `R3` directories.  A round is complete
only when it contains:

- a manuscript source and compiled PDF;
- a claim-to-evidence ledger;
- code/data/result manifests with SHA-256 values;
- figures and tables with source lineage;
- three independent reviewer reports;
- an editorial synthesis and itemized revision log;
- build and verification logs.

Reviewers who implement a round must not serve as that round's independent
reviewers.  Reviewer reports are preserved even when an author disagrees.

## Experiment gate

Before a new LLM-backed formal run, create a freeze document specifying data,
models, prompts, decoding, order, retry policy, call ceiling, evaluator,
statistics, failure preservation, output directory, runtime, and hashes.  A
new call budget is not implied by this draft protocol.

Local deterministic tests, offline reanalysis of frozen ledgers, and local
non-generative baselines may run without an LLM call authorization.

## Deliverable gate

Final completion requires two independently buildable packages containing
LaTeX, PDF, executable source, dependency lock or environment record, permitted
data or retrieval instructions, frozen predictions/results, figures, tables,
review history, declarations, and an editor/reviewer verification index.
