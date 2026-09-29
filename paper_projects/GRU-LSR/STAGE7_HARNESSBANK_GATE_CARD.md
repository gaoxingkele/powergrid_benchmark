# HarnessBank gate card — P1 Stage 7 two-phase release finalizer

## Candidate identity

- Candidate: `p1-stage7-two-phase-release-finalizer-v1`
- Parent harness: Paper Harness `plan_v12/s7`, acceptance record `.paper_harness/runs/v12_s7/acceptance.json`
- Checkpoint parent: `0d5e2d08` (`docs(p1): checkpoint Stage 7 finalizer preparation`)
- Immutable kernel `K`: Paper Harness scoring, acceptance bookkeeping, scientific validators, Stage 6 accepted hashes, manuscript evidence, and author-fact authority.
- Mutable surface `X`: project-local `runtime + config` only — metadata phase ordering, deterministic compilation, dynamic package identity, page-render QA, and terminal release validation.

## Pathology hypothesis

- WHERE `w`: `runtime + config`
- WHY `y`: `circular-release-dependency` combined with `frozen-placeholder-hash-coupling`
- Diagnosis: the parent Stage 7 release check required packaged human-complete files before a human-complete package could be built, while the Stage 6 builder correctly refused every PDF or TeX identity other than the accepted placeholder version.
- Origin: recombined from the existing fail-closed metadata gate and the accepted Stage 6 deterministic-release pattern; no scientific-content mutation was introduced.
- Beacon: incomplete human metadata must activate the prebuild gate before compilation, copying, rendering, manifest writing, or accepted-artifact mutation.

## Gate ledger

| Gate | Result | Evidence |
|---|---|---|
| Validity | PASS | Seven edited/new Python files parsed with `ast`; all five write/terminal entry points imported and executed without an infrastructure exception. |
| Activation | PASS | With the authoritative incomplete ledger, the current official-policy-aligned `prebuild` gate exited 1 with 49 findings and `release` exited 1 with 52 findings; all five write/terminal entry points emitted `BLOCKED` and exited 1. |
| Mutation beacon | PASS | Before/after Git-object digests proved the Stage 6 payload, journal PDF, Stage 6 manifest, and Stage 6 QA unchanged; no Stage 7 package, build identity, or QA file was created. |
| Paired significance | NOT ESTABLISHED | No sealed multi-task parent/offspring score set exists, so paired `z` is unavailable and must not be inferred. |
| Train delta | NOT ESTABLISHED | The activation case proves removal of the circular control dependency, not a journal-quality score improvement. |
| Held-out delta | NOT ESTABLISHED | No held-out paper or cross-project run has been executed. |

## Bank decision

Keep the candidate **project-local and experimental** in the cell `(runtime+config, circular-release-dependency)`. Do not replace or modify the global Paper Harness parent and do not admit this candidate to a shared gene bank until:

1. a real human-complete P1 release passes the success path;
2. at least one held-out manuscript activates the same pathology;
3. a sealed same-task parent/offspring comparison supplies the required paired statistics.

The global bank decision is therefore `keep parent / reject global admission for now`. Code was available and executed; this card is not methodology-only.
