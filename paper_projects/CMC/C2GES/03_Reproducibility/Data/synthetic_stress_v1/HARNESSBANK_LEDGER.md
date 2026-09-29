# Synthetic harness evolution ledger

## Parent and mutable surface

- Parent harness: `c2ges-synthetic-parent-v2`
- Immutable kernel: schema checks, entity denylist, local reference construction,
  aggregate profile loader, distance functions, gate thresholds, hashes, and
  non-confirmatory boundary.
- Mutable surface: DeepSeek generator wording and fictional theme schedule only.

## Observed pathology `(w, y)`

- Witness `w`: `run_20260906`, call 2.
- Outcome `y`: provider constructed a 206-word reference despite the requested
  110--180-word interval; the run stopped and created no final dataset.
- Diagnosis: the provider was incorrectly asked to own both large-layout generation
  and a hard combinatorial reference budget.
- Patch: provider now emits only a compact semantic core; deterministic local code
  owns reference selection and layout expansion.

## Gate ledger

1. Validity: strict JSON/core role/length/entity checks and exact extractive linkage.
2. Activation: provider output contains 20 balanced semantic units; local expansion
   reaches an empirical target profile.
3. Paired improvement: future child versus parent uses the same scenario seeds and
   compares deterministic distances plus a frozen Codex rubric.
4. Held-out: unused fictional themes/series are evaluated once after a candidate
   passes the first three gates.

## Bank decision

`REJECTED_PARENT_PILOT`. No candidate is promoted merely because either LLM
recommends it. The 2026-09-06 failure remains preserved and is not replaced.

The 2026-09-08 parent stopped at DeepSeek call 2 because the denylist matched
`MISO` inside the ordinary word `misoperation`. This was a harness false positive,
not evidence leakage. The matcher is now token-boundary aware and a regression test
is present. The accepted call-1 response was materialized only as a non-promotable
partial diagnostic: candidate-count/page-count gates passed, while unit-type mix and
duplicate-rate gates failed. The first Codex transport then failed before model
execution because Windows encoded stdin with the active legacy code page; the
wrapper now pins UTF-8. Neither failed live call was automatically retried.

`parent-v2b` is the repair candidate authorized by the next goal-continuation turn.
In addition to the two correctness fixes, deterministic distractors carry unique
observation identifiers and the aggregate layout profiles are sampled across the
full 12-profile anchor rather than taking a prefix. These changes directly target
the observed 0.644 exact-duplicate rate and 0.170 maximum type-proportion gap.

`child-v3-codex1` is a generator-surface mutation derived from the frozen Codex
critic output for `parent-v2b`; deterministic gates are unchanged. It adds twelve
topic-specific distractor seeds per report and strengthens the semantic contract
around timestamped state transitions, one primary cause, at most two contributing
conditions, device-function correctness, and independently consistent quantities.
The parent remains rejected and its critic result remains immutable.

The first `child-v3-codex1` call was rejected because the validator required every
causal predecessor to occur earlier in document order, while the frozen prompt
explicitly requested nonchronological exposition. Inspection showed one report
with a root-cause unit pointing to later-described conditions and a second report
with no invalid edges. The repaired kernel now separates semantic direction from
document order: any in-range non-self predecessor is permitted, but the full graph
must be acyclic. A future reference plus a cycle-negative regression test binds
this correction. The failed run is preserved and is not silently retried.

`child-v3b-codex2` completed all four series and passed every unchanged
deterministic gate (candidate-count W1 0.208, page-count W1 0.131, maximum unit-type
gap 0.019, exact duplicates 0.0066). Codex still returned `revise`: scores were
3/4/2/2/1, with fixed role counts, repeated distractor frames, forced device motifs,
and omitted contributing causes as the main pathologies. It is therefore not
promoted and the held-out synthetic themes remain unopened.

The next generator candidate removes the equal-four-per-role template, allows
18--26 core units with 2--6 occurrences per role, marks one indispensable unit per
role for deterministic reference construction, expands topic-specific distractor
seeds to 24--36, varies local context frames, and makes device terminology
conditional on the scenario. Evaluation thresholds remain unchanged.

`child-v4-codex3` activated the variable-role design: the four inspected reports
contained 18--20 core units with unequal per-role counts and 24--28 distractor
seeds. The run stopped at DeepSeek call 2 because one of 106 generated distractor
seeds had 32 words, above both the requested 24-word maximum and the frozen
28-word validation tolerance. No real-entity marker was involved. The output is
retained as a failed activation run, not sanitized or retried. The next prompt
adds an explicit per-seed word-count audit while keeping the validator unchanged.

## Code availability

Generator, evaluator, critic wrapper, and unit tests are available in
`03_Reproducibility/Code/prospective_v1/`.
