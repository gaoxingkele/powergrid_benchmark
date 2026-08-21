# Repository Synchronization Staging — 2026-08-08

This directory is a local, non-pushed staging area. No GitHub branch, commit,
tag, Release, issue, pull request, or asset was written remotely.

## Fresh remote baselines

- `c2ges_remote/`: clean shallow clone of
  `https://github.com/gaoxingkele/c2ges.git`, `main` at
  `d247219e0f8685186616298a338a475bee1810c4`.
- `ma_sqlgrid_remote/`: clean shallow clone of
  `https://github.com/gaoxingkele/ma-sqlgrid.git`, `main` at
  `837b4fdaf9e39d5dd4ab7704a804144e2461bad4`.
- Both clones had zero working-tree changes immediately after cloning.

## Candidate source bundles

- `c2ges_safe_bundle/C2GES_SAFE_EDITOR/` was extracted from the final safe ZIP
  whose SHA-256 is
  `68A3287336530A1AF3A3C5AE13FE75E27E875A706AECE75FCC9522E1ABD7B4ED`.
- `ma_sqlgrid_safe_bundle/MA_SQLGrid_ORIGINAL_TITLE_FINAL/` was extracted from
  the final safe ZIP whose SHA-256 is
  `BE6D4A1E11211EA0AB35921D67865F998B19AAA745A219E22E9805E428CA3B99`.

These are rights-safe **editor packages**, not automatically authorized public
repository payloads. A separate file-level public-release decision is required.
In particular, “may be supplied to an editor/reviewer subject to permission” is
not equivalent to public redistribution permission.

## Proposed release sequence after authorization

1. Complete `deliverables/AUTHOR_FINAL_CONFIRMATION_FORM_2026-08-08.md`.
2. Approve a public file allowlist for each repository.
3. Create a new branch from the exact heads above; never move or reuse `v0.2.0`.
4. Add current README boundaries, reproducibility code, non-verbatim metadata,
   hashes and approved derived outputs. Exclude credentials, `.env`, source
   PDFs, verbatim restricted ledgers, incident outputs and unresolved assets.
5. Run tests and fresh-clone checks from that branch.
6. Commit with a manifest binding the paper PDF/ZIP SHA-256 values.
7. Push only after explicit repository write authorization.
8. Create a new immutable tag/Release (proposed `v0.3.0`, subject to author
   choice), attach only approved assets, and repeat anonymous fresh-clone checks.
9. Only then convert the manuscripts' conditional Data Availability wording to
   a positive exact-release statement.

## Current stop condition

Local baselines and candidate bundles are prepared. Public allowlisting, branch
creation, copying, committing, pushing, tagging and uploading are intentionally
not performed until the author supplies the requested factual confirmations and
explicit GitHub authorization.
