# P1 recovery checkpoint — 2026-09-02

## Goal / context / constraints / done condition

- Goal: finish the IEEE Access submission version of P1 (`mintou_p1_dstar_gru_dispatch`) and the complete submission ZIP.
- Context: Stage 6 science, manuscript, deterministic PDF, and release package are accepted; the Stage 7 fail-closed finalizer is implemented.
- Constraints: never invent author identity, affiliation, ORCID, funding, CRediT, declarations, biographies, photographs, or publication decisions; never alter accepted scientific results to make a gate pass; keep unrelated repository changes out of P1 commits.
- Done when: the author supplies and explicitly confirms every human-owned field; Stage 7 prebuild/release gates, deterministic build, all-page visual QA, terminal release validation, a fresh Paper Harness recovery stage, and the complete ZIP all pass; only then commit/push the final P1 submission artifacts.

## Authoritative repository state at pause

- Repository: `D:/aicoding/powergrid_benchmark`
- Project: `paper_projects/mintou_p1_dstar_gru_dispatch`
- Branch: `main`
- Local `HEAD`: `a27ba6213ae09232c280816843e7072c539a5100`
- Local `origin/main` tracking ref: `a27ba6213ae09232c280816843e7072c539a5100`
- Accepted commit: `a27ba621` — `feat(p1): add fail-closed Stage 7 finalizer`
- Before this checkpoint file was added, `git status --short -- paper_projects/mintou_p1_dstar_gru_dispatch` was empty.
- The overall repository has unrelated user/agent changes. Do not reset, restore, stage, commit, or overwrite anything outside the P1 subtree.
- This checkpoint is the only P1 change made in the current pause turn; no manuscript, metadata value, PDF, experiment output, release package, or hash was changed.

## Accepted Stage 6 identity — do not overwrite

- Frozen experiment results: 2,310 result rows and 240 training trajectories.
- Manuscript: 38 references, 4 figures, 6 tables, 9 pages.
- Release payload: 87 manifested files (88 files when its manifest is counted).
- PDF SHA-256: `bb61e0b1b20a3e9192bc05c640eb8c8895b0b0c24d8f2255c56fd4c4ff983c5c`
- LF-normalized canonical TeX SHA-256: `201a653f104a5a45856525f74c3ee1b8cdedff8f91dba427ef2fa745857fb6c5`
- Extracted semantic-text SHA-256: `2ac920b06ce75ddc788ce1490b50d7484798fcd7f2c5d60b850ae6390afa9fb8`
- Accepted Stage 6 payload-tree SHA-256: `60fb88f675b67dc41814738f4ffff10e55b5498c94bb55250b9c39f9e0d0c26e`

The Stage 6 PDF intentionally contains human placeholders and is not submission-ready.

## Stage 7 state at pause

Stage 7 remains correctly blocked by missing human-owned submission metadata. On 2026-09-02 the validators were rerun without mutation:

- `python -B scripts/validate_p1_stage7_human_metadata.py --phase prebuild` → exit 1, 49 unresolved conditions.
- `python -B scripts/validate_p1_stage7_human_metadata.py --phase release` → exit 1, 52 unresolved conditions.
- `manuscript/STAGE7_HUMAN_METADATA.json` still has `gate_status: blocked_pending_human_confirmation` and `human_confirmation.confirmed: false`.
- `authors` and `affiliations` are still empty.
- No `release_package_stage7`, `STAGE7_BUILD_IDENTITY.json`, `STAGE7_PDF_RENDER_QA.json`, or final Stage 7 ZIP exists.

This is a human-input/administrative blocker, not a failed IEEE Access scientific-revision iteration. Do not consume one of the user's five scientific revision attempts merely by rerunning the same blocked metadata gate. Two post-resume audits have observed the same unchanged blocker; neither produced scientific or release progress.

## Human input required before any further build

Use `manuscript/STAGE7_HUMAN_INPUT_FORM_ZH.md` as the source form. Obtain explicit values for:

1. Final author names and order.
2. English affiliations and author-to-affiliation mapping.
3. Corresponding author, e-mail, and full postal address.
4. Submitting IEEE account ORCID and confirmation that the profile is public and populated.
5. Funding statement or confirmed no-external-funding statement.
6. CRediT roles for every author.
7. Conflict-of-interest declaration.
8. Acknowledgment and AI-use disclosure.
9. Ethics wording/applicability.
10. Biography and a real, non-sample photograph for every author.
11. APC decision.
12. Data/code availability mode and truthful statement.
13. Concurrent-submission and prior-submission declarations.
14. RTS-GMLC release/vintage if known and any shared-material relationship with other manuscripts.
15. Final confirmer identity and a timezone-aware confirmation timestamp.

The manuscript must continue to render `ORCID(s): NONE`, per the user's instruction. This does not satisfy IEEE's separate submitting-account ORCID requirement. Never infer P1 authorship from CMC papers, mail credentials, Git authors, sample IEEE portraits, or other Mintou papers. A bare “确认” is permission to continue, not confirmation of blank factual fields.

## Resume procedure

1. Read this file, `CHECKPOINT_20260830.md`, `manuscript/STAGE7_HUMAN_INPUT_FORM_ZH.md`, and `manuscript/STAGE7_HUMAN_METADATA.json`.
2. Run `git status --short` and isolate P1 from unrelated worktree changes.
3. Ask only for the still-missing human facts. Do not rerun the same gates unless the metadata changed or a fresh status proof is specifically needed.
4. Populate the ledger and echo all rendered metadata back to the user. Keep `human_confirmation.confirmed=false` until the user explicitly approves the completed values.
5. Replace placeholders consistently in `manuscript/MANUSCRIPT.md` and `manuscript/journal_submission/paper.tex`; add only real author photos. Keep scientific claims/results unchanged.
6. Execute, in order:

   ```powershell
   $env:SOURCE_DATE_EPOCH='1787867025'
   $env:FORCE_SOURCE_DATE='1'
   $env:TZ='UTC'
   python -B scripts/verify_stage7_reproducible_build.py
   python -B scripts/build_stage7_release.py
   python -B scripts/update_stage7_pdf_render_qa.py
   # Independently inspect every rendered page before recording PASS.
   python -B scripts/update_stage7_pdf_render_qa.py --confirm-visual-review --inspected-by '<real inspector>' --inspected-at-utc '<timezone-aware timestamp>'
   python -B scripts/validate_stage7_release.py
   python -B scripts/build_stage7_submission_bundle.py
   ```

7. Create a new Paper Harness recovery plan/stage (for example `plan_v13`); never rewrite the already-blocked `plan_v12/s7` history.
8. Rerun scientific, citation, artifact, hygiene, LaTeX, PDF, and IEEE Access gates from scratch. Follow the user's maximum of five scientific revision attempts; pause if the fifth genuine attempt still fails.
9. After all gates pass, build the complete ZIP, commit only P1-scoped changes, push `powergrid_benchmark/main`, and report commit and artifact hashes.

## Existing implementation/evidence — do not reimplement

- `scripts/_stage7_release_common.py`
- `scripts/verify_stage7_reproducible_build.py`
- `scripts/build_stage7_release.py`
- `scripts/update_stage7_pdf_render_qa.py`
- `scripts/validate_stage7_release.py`
- `scripts/build_stage7_submission_bundle.py`
- `manuscript/STAGE7_FINALIZER_FAILURE_PATH_EVIDENCE.json`
- `STAGE7_HARNESSBANK_GATE_CARD.md`
- `manuscript/STAGE7_IEEE_ACCESS_OFFICIAL_POLICY_AUDIT_20260830.md`

The authoritative next action is to obtain the completed human-input form. There is no safe technical substitute for that input.
