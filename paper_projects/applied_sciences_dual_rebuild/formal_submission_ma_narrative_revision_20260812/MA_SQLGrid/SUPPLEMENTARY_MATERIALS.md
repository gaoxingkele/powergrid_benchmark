# Supplementary Materials Guide

This guide relocates implementation and release-detail material that is needed
for reproduction or editorial inspection but would interrupt the main research
narrative. The `supplementary/` directory materializes a rights-safe subset of
those records. It does not create new evidence and does not replace the
immutable experiment artifacts.

## Section S1. Software Conformance and Executor Tests

Provide the complete typed-message, blackboard, state-coverage, read-only
authorization, timeout/opcode/row-bound, deterministic replay, and failure
retention test matrix.  Keep the historical executor used by the selector study
separate from the later executor revision that adds raw-cell-byte,
total-result-byte, projected-width, and function controls.  Later tests must not
be cited as if they had generated the 80/100/101 results.

## Section S2. Protocol Identity, Version Chronology, and Incidents

Include protocol IDs, runtime versions, freeze and audit hashes, code/data
manifests, output directories, and incident dispositions.  Mark superseded and
failed runs as retained provenance.  The BIRD v1.1 Qwen and Granite clean runs
remain the formal evidence, while earlier accident and legacy directories remain
excluded from all paper results.

## Section S3. Numerical Evidence

Include the complete GridDB cell and factorial tables, component endpoints,
constructed-state cells, BIRD method summaries, historical-pool attempt ledger,
360-row tie ledger, source-slot counts, 18 sensitivity cells, rescue/harm rows,
and the Q039 trace.  Derived tables must carry source identifiers and hashes.

## Section S4. Reproduction, Figures, and Rights

Provide figure-generation scripts and lineage sources for all six figures,
manuscript build instructions, database/evaluator versions, data cards, and the
rights inventory.  Third-party restricted records may be supplied to editors
and reviewers only when the applicable licence permits; reviewer access does
not create a redistribution licence.

## Section S5. Release Verification

Provide the clean-build log, undefined-reference and missing-asset checks, PDF
page/figure count, Visual QA manifest, current manuscript/PDF hashes, and the
revision ledger.  Old 20-page/four-figure QA records are historical only and
must not be packaged as validation of this revision.

The current release keeps S5 at manuscript level: `VISUAL_QA_MANIFEST.json`,
`VISUAL_QA_REPORT.md`, `REVISION_LEDGER.md`, and `RELEASE_MANIFEST.json`.
