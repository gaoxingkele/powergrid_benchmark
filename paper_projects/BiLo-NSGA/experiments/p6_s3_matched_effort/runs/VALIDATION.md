# P6 S3 Validation Record

## Immutable run audit

- Evidence-of-record: `primary_v1/`.
- Comparison rows: 1440 (720 exact-evaluation and 720 equal-time).
- Exact-evaluation cells: 24 method--scenario cells with 30 rows each; every row records exactly 3200 total units.
- Equal-time cells: 24 method--scenario cells with 30 rows each; realized search time ranges from 0.200004 to 0.201374 s.
- Hypervolume sensitivity: 4320 rows (six schemes for each of 720 primary fronts).
- Local sensitivity: 560 rows (seven cells by eight scenarios by ten seeds).
- Every comparison row has a nonempty feasible front and final-population budget-feasibility rate 1.0.
- The registered hypervolume-sensitivity rows match the primary per-run hypervolume field exactly.
- No failed seed, omitted row, replacement seed, or result-dependent retuning occurred.

## Shared P5 regression

P5 evidence hashes were identical before and after the run:

| File | SHA256 |
|---|---|
| `evidence/runs/real_project_review_results.csv` | `12c32586de768a21205f6c85f5864f1a3f6408aa02f7c910f30f2a0b19c84024` |
| `evidence/tables/real_project_review_leaderboard.csv` | `0f5494c82070d4c5b0e13a8ff81e25712139986d5b9f8ef6e40ed86303142c3b` |
| `src/configs/real_project_review_config.json` | `50e7b6c22e088edd5c387de24d15e590f7dfc5a43fd7fc598aaeadce87fd42bb` |

The shared source remained `1780647cc226e1c54a076863154945a9df53686f21ebadf9548c827a9081a4ba`.

The required acceptance command initially stopped at pytest collection because its subprocess lacked the repository `src` path. Re-running the same command with `PYTHONPATH=<harness-root>/src` passed:

```text
OK mintou_p6_bilonsga_project_review: scientific evidence contract (evidence)
```

This acceptance includes `tests/test_mintou_experiments.py` and therefore exercises the shared Mintou/P5 evidence scaffold.

## Submission artifact build

The official preview generator refreshed `manuscript/journal_submission/paper.tex`, and the generated Markdown/TeX body was restored from the manuscript master. The simple `submission_preview/paper.tex` was also regenerated with the pinned Pandoc executable. PDF compilation could not run because no `pdflatex`, `xelatex`, `lualatex`, `latexmk`, or `tectonic` executable exists on this host. The existing PDFs are prior builds and are not claimed as regenerated evidence.

## Independent consistency checks

- JSON parsing, row counts, per-cell replication, exact budgets, feasibility, family sizes, registered-HV equality, and local-sensitivity cell sizes passed an independent read-only audit.
- `git diff --check` passed.
- All seven required `DEEP_REVISION_EVIDENCE.md` headings are present exactly.
