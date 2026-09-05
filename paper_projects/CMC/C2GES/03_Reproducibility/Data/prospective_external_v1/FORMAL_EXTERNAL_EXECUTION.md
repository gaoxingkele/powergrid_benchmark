# C2GES formal external E1/E3 execution

Status: `IMPLEMENTED / BLOCKED UNTIL HUMAN FREEZE INPUTS EXIST`
Entry point: `03_Reproducibility/Code/prospective_v1/external_confirmatory.py`

## Scope

The runner executes E1 and confirmatory E3 in one access-controlled pass over
the same unseen external reports. It implements:

- E1: Lead, Centroid, TextRank, Semantic-MMR, Role-only, normalized no-path
  C2GES, Full C2GES, and clean-room PacSum-MiniLM at 110 and 260 words;
- E3: AB-0--AB-6, RP-00/RP-10/RP-01/RP-11, and G-U/G-T under the same
  candidates, budgets, seeds, references, and score implementation;
- equal-series paired effects, 10,000-draw series-cluster intervals, exact
  series sign flips when feasible, Holm correction by predefined family, and
  leave-one-series-out diagnostics;
- ROUGE-1/2/L, redundancy, role coverage, typed-edge coverage, realized words,
  budget utilization, selection Jaccard, timing, Python allocation peak, and
  observed process peak working set;
- rights-safe selected-ID/page locators and no public candidate, reference, or
  generated-summary text.

This implementation does not authorize a run and does not supply scientific
results. Current development pilots remain non-confirmatory.

## Mandatory preconditions

Before any authorization is built, the authors/administrator must provide:

1. a rights-cleared CSV containing only the clean external-test reports, with
   unique `doc_id`, `report_series_id`, `split=external_test`, `rights_status`,
   `source_url`, and `source_pdf_sha256` fields, with no overlap against the
   machine-readable seen-exclusion registry;
2. at least eight independent series and the exact report/series counts frozen
   in the formal configuration;
3. a two-reviewer layout audit JSON with `status=PASS`, candidate validity at
   least 0.90, table/body fusion at most 0.05, and no outcome access;
4. balanced tuning-grid and tuning-decision files created only from eligible
   development series, with the decision marked `FROZEN` and
   `external_test_accessed=false`;
5. filled PacSum parameters, recommended C2GES method, long-unit policy,
   runtime versions, seeds, and every AB/RP/G weight in the formal config;
6. matching `freeze_bindings` in both external and factorial protocols;
7. a private dataset and durable attempt-registry location outside the public
   package and outside the new result directory;
8. the local MiniLM snapshot at revision
   `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`.

The clean inventory must exclude every report named in
`PRE_FREEZE_ACCESS_LOG.md` as previously exposed.

## Two-command execution

First, an authorized administrator builds the immutable authorization. The
acknowledgement flag means metadata and hashing only; it is not permission to
inspect report text or reference outcomes.

```text
python 03_Reproducibility/Code/prospective_v1/build_external_authorization.py \
  --config <frozen-config.json> \
  --external-protocol 03_Reproducibility/Data/prospective_external_v1/EXTERNAL_PROTOCOL_FREEZE.json \
  --factorial-protocol 03_Reproducibility/Data/component_factorial_v1/FACTORIAL_PROTOCOL.json \
  --tuning-decision <TUNING_DECISION.json> \
  --tuning-grid <balanced_tuning_grid.csv> \
  --inventory <rights_safe_external_metadata.csv> \
  --seen-exclusion-registry 03_Reproducibility/Data/prospective_external_v1/SEEN_EXCLUSION_REGISTRY.csv \
  --layout-candidate-audit <layout_candidate_audit.csv> \
  --layout-audit-summary <layout_candidate_audit_summary.json> \
  --ablation-registry 03_Reproducibility/Data/component_factorial_v1/ablation_config_registry.json \
  --dataset <private-external-dataset.jsonl> \
  --model-snapshot <local-MiniLM-revision-directory> \
  --output-dir <new-formal-output-directory> \
  --attempt-registry <durable-private-attempt.json> \
  --authorization-output <new-authorization.json> \
  --run-id <stable-run-id> \
  --operator <human-operator-id-or-role> \
  --administrator-confirms-no-content-review
```

Second, compare the printed authorization SHA-256 with the signed execution
record, then invoke the formal runner exactly once:

```text
python 03_Reproducibility/Code/prospective_v1/external_confirmatory.py \
  --authorization <authorization.json> \
  --out-dir <the-exact-authorization-bound-output-directory>
```

The runner completes all non-dataset preflight checks first. It then creates
the attempt registry atomically, records `external_dataset_opened=true`, verifies
the private dataset hash, and starts evaluation. An existing registry always
causes refusal. A crash after the claim is recorded as
`FAILED_AFTER_CLAIM`; it must not be erased or silently retried. Any scientifically
justified repair requires a written fault report and a newly approved protocol,
not deletion of the registry.

## Expected outputs

The external directory contains the 12 E1 files listed in the paper plan plus
the machine-readable layout-audit summary,
including `RUN_MANIFEST.json` and `OUTPUT_SHA256SUMS.txt`. The factorial
directory contains the AB/RP/G item, aggregate, effect, interaction, Jaccard,
and resource tables plus `FACTORIAL_REPORT.md`.

`factorial_human_metrics.csv` is intentionally not generated by this code
runner. It must be derived later by joining completed E2 human judgments to the
frozen E3 selections. Creating an empty or synthetic file would not satisfy the
submission-readiness gate.

## Post-run boundary

Do not interpret or rewrite the paper until all output hashes pass. Preserve the
private attempt record and copy only rights-safe outputs into the public package.
After E2 is complete, backfill the manuscript according to the predefined
result-driven rules, rebuild the PDF, create `SUBMISSION_EVIDENCE_LOCK.json`,
and run:

```text
python 03_Reproducibility/Code/prospective_v1/submission_readiness.py
```

Only exit code 0 with `status=READY` permits creation of a submission-final tag.
