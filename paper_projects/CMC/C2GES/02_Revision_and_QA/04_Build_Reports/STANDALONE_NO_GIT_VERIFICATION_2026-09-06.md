# C2GES standalone no-Git-ancestor verification

Date: 2026-09-06
Status: `PASS`
Scope: current 250-file protocol-ready public allowlist

## Why this verification was repeated

The earlier clean-ZIP checks extracted beneath the active Git workspace. The
package itself contained no `.git`, but Python root-discovery functions could
still find the workspace's ancestor `.git`. That test therefore did not prove
operation in a genuinely independent filesystem location.

The stricter test copied only checksum-allowlisted files and four portable
control files to a fresh system temporary directory:

`<system-temp>/c2ges_standalone_<uuid>/C2GES`

An upward traversal from the copied root to the drive root found zero `.git`
entries.

## First strict attempt and repair

The first strict run reproduced two hidden portability failures:

- three core test modules failed during import because
  `run_test_v0_3_1.py` and `build_full_pdf_dataset.py` required a Git root;
- the rights-safe metadata test required a Git root before it could issue the
  intended restricted-input skip.

Root discovery was changed to prefer an explicit `C2GES_WORKSPACE_ROOT`, then a
Git workspace when present, and finally the portable
`C2GES_RELEASE_MARKER.json`. The public tests use the portable root only when no
workspace exists; restricted data remain excluded and are still skipped rather
than silently substituted.

## Independent result

| Check | Result |
|---|---:|
| `.git` entries in the package or any ancestor | 0 |
| Release manifest | PASS: 250 files; 0 missing, mismatch, or unlisted |
| Core tests | PASS: 29/29 |
| Development tests | PASS: 9 pass, 1 documented restricted-input skip |
| Post-run tests | PASS: 8 pass, 2 documented restricted-input skips |
| Prospective tests | PASS: 31/31 |
| Development-pilot integrity | PASS |
| Main LaTeX clean build | PASS |
| Supplement LaTeX clean build | PASS |
| Public verification | PASS; 0 failures; non-mutating |

This closes the previously hidden no-Git-ancestor portability defect for the
current code and tests. It does not close scientific gates E1, E2, or E3 and
does not authorize the formal external runner.
