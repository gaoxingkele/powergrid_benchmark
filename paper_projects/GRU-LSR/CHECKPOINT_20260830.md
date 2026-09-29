# P1 recovery checkpoint — 2026-08-30

## Goal

Finish the IEEE Access submission version of P1 (`mintou_p1_dstar_gru_dispatch`) without inventing author facts, citations, experiments, or results. Stage 6 scientific and release engineering is complete. Stage 7 must remain fail-closed until the author supplies the missing human metadata.

## Authoritative state

- Repository: `D:/aicoding/powergrid_benchmark`
- Project: `paper_projects/mintou_p1_dstar_gru_dispatch`
- Branch: `main`
- Checkpoint base before the current save: `718119ae` (`docs(p1): add Stage 7 recovery checkpoint`).
- `main` and `origin/main` were both at `718119ae` before the current save.
- After restoring, treat the commit containing this file as the authoritative P1 checkpoint.
- The overall repository contains unrelated user/agent work. Do not reset, restore, stage, commit, or overwrite changes outside the P1 subtree.

Relevant accepted commits:

- `90b11a03` — accept Paper Harness `plan_v12`, Stage `s6r4`
- `a1211b59` — stabilize deterministic release line endings
- `d9020ff3` — refresh the 87-file manifest after LF normalization
- `777ae102` — add the fail-closed Stage 7 metadata ledger and validator
- `c7f8963c` — add the Chinese human-input form
- `718119ae` — add the first Stage 7 recovery checkpoint

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

## Current checkpoint save — Stage 7 finalizer implemented, success path pending

The Stage 7 final release engineering is now implemented. Preserve the following exact state on resume:

- `scripts/validate_p1_stage7_human_metadata.py` now supports `--phase prebuild|release`.
- `prebuild` validates the human ledger plus the authoritative Markdown and journal TeX, but does not require a release package that cannot exist yet.
- `release` remains backward-compatible as the default and additionally validates the packaged TeX, author photographs, and release manifest.
- This removes the circular dependency `release package required before release package can be built` without weakening the terminal release gate.
- Failure-path activation on 2026-08-30 passed: the current official-policy-aligned `prebuild` gate exited 1 with 49 unresolved conditions and the independent Stage 7 `release` path exited 1 with 52 unresolved conditions.
- No manuscript, PDF, release payload, manifest, scientific result, or human metadata value was changed by this preparation.
- The repository contains many unrelated modified/untracked paths. Only P1-scoped files may be staged or committed during recovery.

Implemented Stage 7 entry points:

1. `scripts/verify_stage7_reproducible_build.py` — prebuild gate, isolated three-pass LaTeX compilation, unresolved-reference check, dynamic build identity, and atomic publication of the proved PDF.
2. `scripts/build_stage7_release.py` — metadata-bound, dynamic-hash final package and manifest at `release_package_stage7`, leaving the accepted Stage 6 package untouched.
3. `scripts/update_stage7_pdf_render_qa.py` — dynamic all-page render record requiring an explicit inspector and timezone-aware inspection time before it can record PASS.
4. `scripts/validate_stage7_release.py` — read-only terminal validation of metadata, package completeness, manifest/source identity, independent package recompilation, PDF/TeX identity, placeholders, and independent page renders.
5. `scripts/build_stage7_submission_bundle.py` — terminal-gated complete ZIP containing the final submission package, code, frozen experiment outputs, derived tables/figure sources, audits, four exact RTS-GMLC input files, and the full data-use notice; ZIP must remain under 40 MB.
6. `scripts/_stage7_release_common.py` — shared fail-closed paths, hashes, environment, placeholder, render, and safe-publication primitives.

Machine-readable activation evidence:

- `manuscript/STAGE7_FINALIZER_FAILURE_PATH_EVIDENCE.json`
- Accepted Stage 6 payload tree SHA-256: `60fb88f675b67dc41814738f4ffff10e55b5498c94bb55250b9c39f9e0d0c26e` over 88 files including its manifest.
- All five Stage 7 write/terminal entry points exited 1 before writes; Stage 6 PDF, manifest, QA, and payload remained unchanged.
- No `release_package_stage7`, `STAGE7_BUILD_IDENTITY.json`, or `STAGE7_PDF_RENDER_QA.json` was created.

HarnessBank evidence:

- `STAGE7_HARNESSBANK_GATE_CARD.md`
- Validity, activation, and mutation-beacon gates pass.
- Paired significance, train delta, and held-out delta are not established; the repair remains project-local and is not admitted to the global bank.

Required execution order after the human facts are supplied:

```text
prebuild metadata gate
  -> render confirmed metadata into Markdown/TeX and add real photos
  -> three-pass deterministic LaTeX build + build identity
  -> Stage 7 release package + dynamic manifest
  -> independent all-page render/visual QA
  -> terminal release validator
  -> new Paper Harness recovery plan/stage
  -> terminal-gated complete upload ZIP
```

The builders are proved to fail before mutating current accepted artifacts while metadata is incomplete. Never overwrite the accepted Stage 6 identity merely to make Stage 7 pass.

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
4. Submitting IEEE account ORCID, with explicit confirmation that its profile is public and populated; if not registered, registration is a real submission blocker.
5. Funding statement or confirmed no-external-funding statement.
6. CRediT roles for every author.
7. Conflict-of-interest declaration.
8. Acknowledgment and confirmed AI-use disclosure.
9. Ethics wording/approval applicability.
10. Biography and non-sample photograph for every author.
11. APC decision.
12. Explicit data/code availability mode: public URL/DOI, submission supplementary material, or a truthful non-public statement.
13. Concurrent-submission and prior-submission yes/no declarations.
14. RTS-GMLC release/vintage if known, plus any shared-material relationship with other manuscripts.
15. Final confirmer name and timezone-aware confirmation date.

## Resume procedure

1. Read this checkpoint and `manuscript/STAGE7_HUMAN_INPUT_FORM_ZH.md`.
2. Inspect `git status --short` and isolate P1 from all unrelated worktree changes.
3. Re-run both metadata phases; both are expected to block until the human fields are complete:

   ```powershell
   python -B scripts/validate_p1_stage7_human_metadata.py --phase prebuild
   python -B scripts/validate_p1_stage7_human_metadata.py --phase release
   ```

4. Do not reimplement the finalizer. Review `STAGE7_FINALIZER_FAILURE_PATH_EVIDENCE.json` and `STAGE7_HARNESSBANK_GATE_CARD.md` first.
5. Ask only for missing factual values. Do not treat a bare `确认` as field-level confirmation.
6. Populate `STAGE7_HUMAN_METADATA.json`, but keep `human_confirmation.confirmed=false` until every field has been echoed back and explicitly approved.
7. Replace placeholders consistently in `manuscript/MANUSCRIPT.md` and `manuscript/journal_submission/paper.tex`; copy real photos into the journal source. Keep scientific claims/results unchanged.
8. Set the deterministic environment and run the finalizer chain:

   ```powershell
   $env:SOURCE_DATE_EPOCH='1787867025'
   $env:FORCE_SOURCE_DATE='1'
   $env:TZ='UTC'
   python -B scripts/verify_stage7_reproducible_build.py
   python -B scripts/build_stage7_release.py
   python -B scripts/update_stage7_pdf_render_qa.py
   # Inspect every rendered page independently before recording PASS.
   python -B scripts/update_stage7_pdf_render_qa.py --confirm-visual-review --inspected-by '<real inspector>' --inspected-at-utc '<timezone-aware timestamp>'
   python -B scripts/validate_stage7_release.py
   python -B scripts/build_stage7_submission_bundle.py
   ```

9. Create and approve a new Harness recovery plan (for example `plan_v13`) because `plan_v12/s7` is already `BLOCKED`.
10. Run the complete scientific, citation, artifact, hygiene, LaTeX, and PDF gates from scratch; do not treat the finalizer alone as IEEE Access acceptance evidence.
11. Build the final upload ZIP only after all Stage 7 and Harness gates pass.
12. Commit only P1-scoped changes, push `powergrid_benchmark/main`, and report the final commit and artifact hashes.

## Temporary audit worktrees

Main is authoritative. Temporary/registered audit worktrees may still exist, including:

- `D:/aicoding/powergrid_benchmark/tmp/p1_stage6_preflight_worktree`
- `D:/aicoding/powergrid_benchmark/tmp/p1_stage6_postmerge_a1211b59`
- Harness worktrees under `C:/Users/10175/AppData/Local/Temp/paper_harness_worktrees/`

Do not delete or force-remove them during resume unless their exact resolved paths and Git worktree registrations are verified. They are not sources of newer scientific content.
