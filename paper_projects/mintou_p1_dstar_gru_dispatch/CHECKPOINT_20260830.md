# P1 recovery checkpoint — 2026-08-30

## Goal

Finish the IEEE Access submission version of P1 (`mintou_p1_dstar_gru_dispatch`) without inventing author facts, citations, experiments, or results. Stage 6 scientific and release engineering is complete. Stage 7 must remain fail-closed until the author supplies the missing human metadata.

## Authoritative state

- Repository: `D:/aicoding/powergrid_benchmark`
- Project: `paper_projects/mintou_p1_dstar_gru_dispatch`
- Branch: `main`
- Latest P1 checkpoint parent: `c7f8963c`
- `origin/main` was synchronized with `c7f8963c` before this checkpoint.
- The P1 subtree was clean before this checkpoint was created.
- The overall repository contains unrelated user/agent work. Do not reset, restore, stage, commit, or overwrite changes outside the P1 subtree.

Relevant accepted commits:

- `90b11a03` — accept Paper Harness `plan_v12`, Stage `s6r4`
- `a1211b59` — stabilize deterministic release line endings
- `d9020ff3` — refresh the 87-file manifest after LF normalization
- `777ae102` — add the fail-closed Stage 7 metadata ledger and validator
- `c7f8963c` — add the Chinese human-input form

Paper Harness library repair:

- Repository: `D:/aicoding/mylib`
- Pushed commit: `e3b5eaa` — recognize `Reproducibility and Data Boundary` as a valid data-availability declaration and add the project-local HarnessBank card.
- Regression result at that commit: `19 passed`.
- The local `mylib/main` later advanced through unrelated work and may be ahead of `origin/main`. Do not reset or push those unrelated commits as part of P1.

## Stage 6 — complete and verified

Accepted scientific/release facts:

- Frozen rerun: 2,310 result rows and 240 training trajectories.
- Five paper-facing derived tables match the frozen evidence.
- Manuscript validator: 38 references, 4 figures, 6 tables, 9 pages.
- Release payload: exactly 87 manifested files.
- PDF SHA-256: `bb61e0b1b20a3e9192bc05c640eb8c8895b0b0c24d8f2255c56fd4c4ff983c5c`
- LF-normalized TeX SHA-256: `201a653f104a5a45856525f74c3ee1b8cdedff8f91dba427ef2fa745857fb6c5`
- Extracted semantic-text SHA-256: `2ac920b06ce75ddc788ce1490b50d7484798fcd7f2c5d60b850ae6390afa9fb8`
- A fresh checkout produced the same PDF hash on three consecutive `pdflatex` passes.
- Main/package PDF identity, main/package TeX identity, all manifest hashes, all nine independent page renders, and the visual review passed.
- The current verified PDF intentionally retains human placeholders and is not submission-ready.

Revalidation commands:

```powershell
$env:SOURCE_DATE_EPOCH='1787867025'
$env:FORCE_SOURCE_DATE='1'
$env:TZ='UTC'
cd D:\aicoding\powergrid_benchmark\paper_projects\mintou_p1_dstar_gru_dispatch
python scripts/generate_p1_stage6_science_comparison.py
python experiments/p1_ieee_access_upgrade_v2/validate_upgrade.py --phase manuscript
python scripts/validate_stage6_deterministic_release.py
```

Do not use checkout mtimes as provenance. Use ordered Harness execution and content hashes.

## Stage 7 — deliberately blocked

Paper Harness `plan_v12/s7` ran and blocked correctly. Its acceptance record is:

`paper_projects/mintou_p1_dstar_gru_dispatch/.paper_harness/runs/v12_s7/acceptance.json`

Passing checks:

- narrative structure
- artifact consistency
- manuscript hygiene
- LaTeX compilation

Expected failures:

- unresolved human placeholders
- incomplete human metadata ledger
- final PDF integrity while placeholders remain

The former Data Availability false negative was fixed in `mylib` and now passes independently.

Stage 7 files:

- `manuscript/STAGE7_HUMAN_INPUT_FORM_ZH.md` — user-facing form
- `manuscript/STAGE7_HUMAN_METADATA.json` — machine-readable fail-closed ledger
- `scripts/validate_p1_stage7_human_metadata.py` — 54-condition validator
- `manuscript/DEEP_REVISION_EVIDENCE.md` — unresolved-human-fact ledger

## Latest user interaction

The user replied `确认` after receiving the form. This confirms continuation, but it does not provide values for blank factual fields. A repository/history audit found that P1's earliest manuscript already contained author placeholders; there is no P1 original author list to inherit.

Do not infer P1 authorship from:

- CMC manuscript authors,
- outbound mail credentials,
- repository commit authors,
- bundled IEEE sample portraits (`author1.png`, `author2.png`, `author3.png`), or
- other Mintou papers.

The manuscript rendering of ORCID must remain exactly `NONE`, per the user's earlier instruction. The submitting-account ORCID remains a separate human-confirmed field in the Stage 7 ledger.

## Human facts still required

At minimum obtain explicit values for:

1. Final author names and order.
2. Complete English affiliations and author-to-affiliation mapping.
3. Corresponding author, e-mail, and postal address.
4. Submitting IEEE account ORCID, or an explicit statement that it is not yet registered.
5. Funding statement or confirmed no-external-funding statement.
6. CRediT roles for every author.
7. Conflict-of-interest declaration.
8. Acknowledgment and confirmed AI-use disclosure.
9. Ethics wording/approval applicability.
10. Biography and non-sample photograph for every author.
11. APC decision.
12. Public repository URL and/or archival DOI.
13. Concurrent-submission and prior-submission yes/no declarations.
14. RTS-GMLC release/vintage if known, plus any shared-material relationship with other manuscripts.
15. Final confirmer name and timezone-aware confirmation date.

## Resume procedure

1. Read this checkpoint and `manuscript/STAGE7_HUMAN_INPUT_FORM_ZH.md`.
2. Ask only for missing factual values. Do not treat a bare `确认` as field-level confirmation.
3. Populate `STAGE7_HUMAN_METADATA.json`, but keep `human_confirmation.confirmed=false` until every field has been echoed back and explicitly approved.
4. Replace placeholders consistently in `manuscript/MANUSCRIPT.md` and `manuscript/journal_submission/paper.tex`; copy real photos into the journal source. Keep scientific claims/results unchanged.
5. Add or adapt a Stage 7 release builder. The Stage 6 builder/validator intentionally requires retained placeholders and the frozen placeholder-PDF hash, so it must not be reused unchanged for the final human-complete PDF.
6. Create and approve a new Harness recovery plan (for example `plan_v13`) because `plan_v12/s7` is already `BLOCKED`.
7. Run: no placeholders, declarations, Stage 7 custom validator, narrative structure, artifact consistency, manuscript hygiene, deterministic LaTeX build, final release manifest, PDF integrity, and independent page rendering/visual QA.
8. Build the final upload ZIP only after all Stage 7 gates pass.
9. Commit only P1-scoped changes, push `powergrid_benchmark/main`, and report the final commit and artifact hashes.

## Temporary audit worktrees

Main is authoritative. Temporary/registered audit worktrees may still exist, including:

- `D:/aicoding/powergrid_benchmark/tmp/p1_stage6_preflight_worktree`
- `D:/aicoding/powergrid_benchmark/tmp/p1_stage6_postmerge_a1211b59`
- Harness worktrees under `C:/Users/10175/AppData/Local/Temp/paper_harness_worktrees/`

Do not delete or force-remove them during resume unless their exact resolved paths and Git worktree registrations are verified. They are not sources of newer scientific content.
