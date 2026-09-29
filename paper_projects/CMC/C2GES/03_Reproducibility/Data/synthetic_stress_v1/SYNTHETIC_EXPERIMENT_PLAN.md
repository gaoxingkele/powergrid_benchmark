# C2GES DeepSeek + Codex synthetic stress-test protocol v2

## Material Passport

- Origin: academic-research-suite / experiment-agent; experiment-design; experiment-code
- Date: 2026-09-08
- Verification status: IMPLEMENTED / PARENT REJECTED / CHILD PARTIAL
- Evidence class: synthetic implementation and robustness evidence only
- Confirmatory claims allowed: false

## Goal, context, constraints, done condition

Goal: create fictional incident fixtures whose observable document-level and layout
statistics are calibrated against rights-safe aggregate development metadata, then
use a separate Codex CLI context to identify semantic and templating defects.

Context: anchors are limited to `rights_safe_report_metadata.csv` and
`layout_candidate_audit.csv`. Neither model receives real report text, manuscript
text, author data, unpublished inputs, URLs, or source identifiers.

Hard constraints: synthetic data cannot replace prospective unseen-series E1,
two-person E2, or support operational/generalization claims. Passing a distribution
gate establishes only alignment of the explicitly measured observables.

Pilot is done when one immutable run directory contains DeepSeek responses,
converted JSONL, hashes, deterministic gate ledger, a schema-constrained Codex
critic result, and an honest accept/revise/reject decision.

Parent（第一套）的内容、分布与算法说明见 `PARENT_V2B_SYNTHETIC_FLOW.md`。

## Four-stage execution map

1. Initial implementation: validate the compact semantic-core generator locally.
2. Baseline tuning: run four fictional series against frozen aggregate profiles.
3. Creative improvement: Codex proposes one prompt-only amendment after blind audit.
4. Ablation/held-out: a later authorized child run must reuse paired scenario seeds;
   it receives credit only if validity, activation, paired improvement, and held-out
   gates pass. No child result is predeclared here.

## Architecture and privacy fence

- DeepSeek produces exactly 20 concise semantic-core units per report.
- Local deterministic code creates layout distractors, assigns empirical profile
  targets, constructs the extractive reference, and owns all validity decisions.
- Codex receives only synthetic units plus aggregate statistics in an isolated
  temporary working directory, read-only and ephemeral, with a strict JSON schema.
- LLM opinions are advisory. Deterministic gates own acceptance.
- Failed API responses are retained and stop the run; they are never overwritten or
  silently retried.

## Acceptance metrics

- Structural validity and exact extractive provenance.
- Normalized Wasserstein and KS distances for candidate count and page count.
- Unit-type proportion gaps and exact-duplicate rate.
- Codex rubric: causal coherence, numeric consistency, lexical diversity, domain
  plausibility, and template-artifact control.
- Reference length is reported but not distribution-gated because the synthetic
  task intentionally fixes references to 110--180 words.

AUROC, nonsignificant KS tests, or a positive LLM judgment must never be described
as proof that synthetic data are real or equivalent to real data.

## Frozen pilot commands

```text
python generate_deepseek_synthetic.py --env <workspace>/.env --metadata-csv <C2GES>/03_Reproducibility/Data/rights_safe_metadata/rights_safe_report_metadata.csv --layout-csv <C2GES>/03_Reproducibility/Data/prospective_external_v1/layout_dev_pilot_v2/layout_candidate_audit.csv --model deepseek-v4-flash --output <C2GES>/03_Reproducibility/Data/synthetic_stress_v1/run_20260908_parent_v2 --seed 20260908 --series 4 --version-id parent-v2
python evaluate_synthetic_distribution.py --dataset <run>/synthetic_reports.jsonl --metadata-csv <metadata> --layout-csv <layout> --output <run>/evaluation
python run_codex_synthetic_critic.py --packet <run>/evaluation/codex_critic_packet.json --output <run>/codex_critic --model gpt-5.6-sol
```

The Codex invocation is recorded without prompt content; the packet hash and
synthetic-only boundary are recorded. Timeout: 10 minutes. No automatic retry.

## Execution status through 2026-09-10

- `run_20260910_parent_v2b`: complete 4-series generation; deterministic gate
  rejected it only for 0.530 cross-report exact duplicates. Codex verdict `revise`
  with scores 3/3/1/2/1 for causal/numeric/lexical/domain/template dimensions.
- `run_20260910_child_v3_codex1`: stopped at call 1 because the old validator
  conflated causal order with document order. The accepted raw response was
  materialized as a non-promotable two-report diagnostic after correcting the DAG
  validator. Duplicate rate became 0; Codex remained `revise`, scoring 3/3/2/2/1.
- No generated run has been promoted or inserted into the manuscript.
- Next candidate must complete all four series and pass unchanged deterministic
  gates before any held-out synthetic run is opened.
