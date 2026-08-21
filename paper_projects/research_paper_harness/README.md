# Research Paper Harness

This directory contains the reusable orchestration layer for the Mintou six-paper
portfolio and the two Applied Sciences papers.  It is deliberately conservative:
the default commands inspect state and verify hashes; they do not rerun frozen
experiments, rewrite manuscripts, rebuild release artifacts, send email, or submit
papers.

## Design

The harness treats a paper portfolio as a versioned stage machine:

1. intake and title/claim boundary;
2. journal comparator and manuscript budget;
3. asset and version-boundary audit;
4. experiment registry and protocol freeze;
5. preflight/integrity gate;
6. formal experiment execution;
7. statistics, negative-result retention, and claim ledger;
8. section-by-section writing and figure lineage;
9. three review/revision rounds;
10. build, visual QA, release manifest, and packaging;
11. manual author/licence/submission gate.

The portfolio-specific truth lives in JSON profiles under the corresponding
project subdirectories.  The Python runner is standard-library only and supports
Python 3.10 or later.

## Commands

From the workspace root:

```powershell
python paper_projects/research_paper_harness/harness.py check --profile papers/mintou/harness/profile.json
python paper_projects/research_paper_harness/harness.py status --profile papers/mintou/harness/profile.json
python paper_projects/research_paper_harness/harness.py plan --profile papers/mintou/harness/profile.json

python paper_projects/research_paper_harness/harness.py check --profile paper_projects/applied_sciences_dual_rebuild/harness/profile.json
```

`run-stage` is a dry run unless `--execute` is supplied.  Even with `--execute`,
only a stage explicitly marked `auto_safe: true` can run.  Formal experiments,
release rebuilds, packaging, email, and submission remain manual/authorized steps.

```powershell
python paper_projects/research_paper_harness/harness.py run-stage --profile <profile.json> --stage <stage-id>
```

To write a fresh checksum snapshot, choose a new output path.  Existing snapshots
are never overwritten:

```powershell
python paper_projects/research_paper_harness/harness.py manifest --profile <profile.json> --write <new-manifest.json>
```

## Status vocabulary

- `complete`: evidence exists and the configured gate is satisfied.
- `pending`: planned work has not been completed.
- `blocked`: a manual decision or unavailable prerequisite is required.
- `optional`: not required for the present release.
- `superseded`: retained for provenance but forbidden as current evidence.

`complete` does not imply that a scientific claim is true.  It means only that the
declared stage evidence is present and internally consistent.  Claim validity is
controlled separately by the experiment registry, statistical audit, and claim
ledger.

