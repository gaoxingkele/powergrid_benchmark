# Registered Statistical Analysis Plan

## Outcomes and denominators

Execution correctness is exact denotation equality under the existing frozen SQLite evaluator and database. Parse/provider/unsafe/execution failures are incorrect and remain in denominators.

- E1 primary outcome: first-candidate execution correctness, V1 minus V0, among the 170 intervention-eligible questions, separately for each backbone.
- E2 primary outcome: validator-selected minus first-candidate execution correctness on all 180 V1 questions, separately for each backbone. If no candidate is parsed, both outcomes are false. Candidate extraction count, selection-change rate, rescue count (0→1), harm count (1→0), and oracle@3 are descriptive; oracle@3 is explicitly gold-only and never a deployable result.
- E4 primary outcome: within-question `log((V1 latency_ms+1)/(V0 latency_ms+1))`, summarized as a geometric latency ratio. Secondary outcomes are input, output, and total tokens, retry incidence, and token throughput. E4 uses the same 170 eligible pairs and is reported within backbone.

## Dependence-aware inference

The frozen template-cluster mapping comes from `canonical_v2_reanalysis/canonical_rows_v2.jsonl`, whose hash is in `PROTOCOL_FREEZE.json`. No question-level McNemar result is primary.

For each binary paired contrast, report the question-weighted risk difference. A 95% percentile interval uses 20,000 template-cluster bootstrap resamples: sample clusters with replacement, retain every question in each sampled cluster, and recompute the question-weighted paired difference. Inferential p-values use 100,000 Monte Carlo sign flips at the cluster unit, flipping every paired difference within a cluster together. Seeds are 20260805 plus fixed analysis-family offsets.

Holm correction is applied to two predeclared families:

1. E1 primary execution effects: Qwen and Granite (two tests).
2. E2 primary validator effects: Qwen and Granite (two tests).

The cross-backbone difference in each paired effect is a secondary two-test family. E4 is estimation-focused: cluster-bootstrap intervals are reported without dichotomous significance language. Descriptive candidate extraction, safety, oracle, and latency sensitivity fields are not promoted through multiplicity testing.

Fixed seed offsets are part of the freeze: E1 bootstrap `+1101/+1102` and randomization `+1201/+1202`; E2 bootstrap `+2101/+2102` and randomization `+2201/+2202`; cross-backbone E1/E2 bootstrap `+3101/+3102` and randomization `+3201/+3202`; E4 latency bootstrap `+4101/+4102`, input tokens `+4201/+4202`, output tokens `+4301/+4302`, total tokens `+4401/+4402`, and throughput `+4501/+4502`, all added to base seed 20260805.

## Efficiency validity checks

Latency claims remain controlled only if at least 95% of scored calls have zero retries, no provider failures occur, both conditions use the same loaded model/backend/server arguments, and the run has no recorded thermal throttling or competing GPU process incident. Otherwise token counts remain valid but latency is demoted to diagnostic. Report V0-first versus V1-first sensitivity and first-half versus second-half drift.

## Claim rules

Positive component efficacy requires a positive estimate, a 95% cluster-bootstrap interval excluding zero, and Holm-adjusted `p < 0.05`. A result failing that rule is reported as no detectable improvement, never omitted. Replication across backbones requires both backbones to satisfy the rule in the same direction. A negative significant estimate is reported as harm. Null or adverse results do not invalidate the experiment; they narrow the manuscript's component claims.
