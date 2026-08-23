# MA-SQLGrid 3.0 Test Report

## Outcome

- Coordination and original-title rebuild: 30 tests passed.
- Final framework and executor: 14 tests passed.
- Canonical GridDB v2 reanalysis: 15 tests passed.
- Inference-hierarchy analysis: 9 tests passed.
- Component release: 6 tests passed.
- Constructed-state reliability study: 22 tests passed and 1 skipped.
- Total: 96 passed, 1 skipped.

The manuscript compiled without undefined citations, undefined references,
LaTeX errors, or overfull boxes. Visual QA passed on all 25 pages.

## Runtime-specific BIRD note

The BIRD v1.1 formal protocol records Python 3.10.11 and SQLite 3.40.1. The
current verification host provides Python 3.12 and SQLite 3.49.1, so the formal
runtime-identity assertion cannot be re-certified on this host. This is an
environment mismatch, not a failed rerun. The archived formal BIRD results were
not regenerated, replaced, or mixed with the current verification outputs.
