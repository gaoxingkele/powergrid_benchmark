# Synthetic evidence status — 2026-09-10

## Material Passport

- Artifact type: execution and claim-boundary record
- Evidence class: synthetic robustness diagnostics only
- Verification status: PARTIAL / NO PROMOTED DATASET
- Confirmatory claims allowed: false
- Manuscript insertion allowed: false

## Current judgment

The dual-model harness is operational: DeepSeek generated a complete parent batch,
the local evaluator produced quantitative distribution gates, and Codex CLI returned
a schema-valid blind critique. The current data remain unsuitable for publication or
method-effect estimation.

The complete parent matched the development anchors on candidate count
(`normalized W1=0.208`), page count (`0.131`), and unit-type proportions (maximum
absolute gap `0.019`). It failed the unchanged duplicate-rate gate (`0.530 > 0.20`).
Codex independently returned `revise`, with especially low lexical-diversity and
template-control scores.

The first child response reduced exact duplication to zero in a two-report partial
diagnostic and raised Codex lexical diversity from 1/5 to 2/5. It did not improve
causal coherence, numeric consistency, domain plausibility, or template control.
Because the child did not complete four series, these values are directional only
and cannot be treated as a paired improvement result.

A later complete child (`child-v3b-codex2`) passed every deterministic distribution
gate, including an exact-duplicate rate of 0.0066. Codex nevertheless returned
`revise` with scores 3/4/2/2/1. Because the frozen protocol requires semantic review
in addition to numerical distribution alignment, this dataset is also rejected and
the held-out synthetic set remains unopened.

The subsequent variable-structure candidate (`child-v4-codex3`) stopped during
call 2 because one distractor seed contained 32 words. The frozen validator limit
was not changed after observing this response. The run is an activation failure,
not evidence about final distribution or semantic quality.

## Remaining gates

1. Complete a four-series child run under the repaired DAG validator.
2. Pass every deterministic distribution and validity gate without changing its
   threshold after seeing results.
3. Obtain a Codex verdict no worse than `accept_for_synthetic_stress_only`, with no
   device-function or internal-numeric contradiction classified as major.
4. Run unused fictional themes once as a held-out synthetic test.
5. Keep all synthetic evidence outside the confirmatory E1/E2/E3 evidence chain.

Even if all five conditions are met, the result may support software stress testing
only. It cannot establish equivalence to real incident reports, human construct
validity, operational benefit, or journal readiness.

The formal submission verifier was rerun after this audit and returned `NOT_READY`
with 47 findings. The actionable grouping is recorded in
`../SUBMISSION_BLOCKER_ACTIONS_20260910.md`; none of those findings is closed by the
synthetic harness.
