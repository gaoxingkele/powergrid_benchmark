# Network-calibrated synthetic-data decision

Date: 2026-09-10

## Runs

- `run_20260910_network_calibrated_v5`: DeepSeek generation succeeded; deterministic evaluation failed because exact duplicate rate was 0.2229.
- `run_20260910_network_calibrated_v6`: v5 semantic cores were re-materialized after a deterministic uniqueness fix; all deterministic gates passed and exact duplicate rate was 0.0055. Codex semantic audit verdict: `revise` (causal 5, numeric 5, lexical diversity 3, domain plausibility 5, template control 2).
- `run_20260910_network_calibrated_v7`: new DeepSeek generation using the v6 critic amendment; all deterministic gates passed and exact duplicate rate was 0.0029. Codex semantic audit verdict: `revise` (causal 3, numeric 4, lexical diversity 2, domain plausibility 3, template control 1).

## Decision

No run is promoted as realistic surrogate evidence. v6 is the better engineering stress fixture of the two deterministic-pass runs, but it remains `REVISE / STRESS-TEST ONLY`. v7 is retained as evidence that critic-guided prompting did not improve this sample and must not be silently discarded.

Permitted uses:

- parser and schema testing;
- long-document memory and runtime testing;
- unit-test and failure-injection fixtures;
- dry-run implementation of E3 tables and statistical pipelines.

Prohibited uses:

- replacing the prospective real E1 external series;
- reporting paper performance estimates;
- training or replacing E2 human annotators;
- supporting ethics, operational-benefit, or external-validity claims.
