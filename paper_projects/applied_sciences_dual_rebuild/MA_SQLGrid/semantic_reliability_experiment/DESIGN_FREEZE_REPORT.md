# Design-freeze report (pre-score)

Status: **READY_AWAITING_INDEPENDENT_DESIGN_AUDIT**

Freeze content SHA-256:
`a51880693b8aa50242fde27d2927f5b4bf6323b132b20244fb9408603e6a53fe`

No prediction file was opened by the freeze stage.  No execution-agreement or
false-agreement result has been produced.  `RESULTS.json` and
`logs/execution.jsonl` are absent at this gate.

## Frozen inputs

| Input | Bytes | SHA-256 |
|---|---:|---|
| original GridDB SQLite | 36,864 | `ba74e84f30c15ecf04bf2b1ffb5d1ccbb978a9e210b69f4676b9bde64e5bbc46` |
| questions JSONL | 135,867 | `a08f302afb47bc2e7c352d20ca69efa0068b74d9ad296c988bc7b27160593a82` |
| protocol | 2,811 | `bbec190af8d55b20aeb60eb2bb961e55a2a9377671306df08fbf0b9afc3cc3eb` |
| generator/runner | 28,080 | `c0fce8143a9f18b5f5a55f23f7913cbe1f1dc4ba04b026bd983d019d808cf587` |

The freeze contains the original state plus six deterministic perturbations.
Every frozen SQLite file returns `integrity_check=ok`, has zero foreign-key
violations, and is individually SHA-256 locked.  Five one-cohort states contain
twice the original row count in every table; the two-cohort state contains
three times the original row count.

## Generator and safety tests

`python -m unittest discover -s tests -v` completed 4/4 tests:

- repeated combined-state generation is byte-for-byte deterministic;
- unchanged-schema integrity, foreign keys, and table denominators pass;
- the lexical gate accepts a single SELECT/CTE and rejects writes, PRAGMA, and
  multiple statements;
- a `mode=ro&immutable=1` connection plus SQLite authorizer blocks a direct
  DELETE even if the lexical wrapper is bypassed.

`python semantic_reliability.py verify` returned `VERIFY PASS`.

As an additional fail-closed check, `python semantic_reliability.py run`
terminated before prediction loading with:

> formal scoring is locked until INDEPENDENT_DESIGN_AUDIT.json exists

Formal scoring additionally requires that the independent audit record contain
`decision=PASS` and this exact freeze SHA.  The audit should examine the
estimand, perturbation validity/claim boundary, all-denominator accounting,
read-only executor, and whether any design element could have used model
outcomes.

