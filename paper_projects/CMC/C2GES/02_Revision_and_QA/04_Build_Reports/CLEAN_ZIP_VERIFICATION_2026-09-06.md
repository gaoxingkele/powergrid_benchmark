# C2GES clean-ZIP verification

Date: 2026-09-06  
Status: `PASS`  
Scope: portable rights-safe protocol-ready release

## Assembly boundary

- The ZIP was staged from the 225 exact paths in
  `03_Reproducibility/Package_Metadata/FILE_SHA256SUMS.txt`.
- `C2GES_RELEASE_MARKER.json`, the release manifest, checksum list, and root
  README were added as portable-control files.
- The workspace was not recursively archived. `90_Archive`, `.git`, LaTeX
  intermediates, Python bytecode, rendered QA pages, restricted source PDFs,
  and verbatim derived data were not included.
- Test ZIP size: 3,854,069 bytes.

## Independent-directory result

The archive was extracted beneath
`tmp/c2ges_zip_validation_20260906_011044/extract/C2GES`, which has no `.git`
directory. Python 3.12.10 executed the public verifier from that extracted root.

| Check | Result |
|---|---:|
| Manifest before verification | PASS: 225 checked; 0 missing, mismatch, or unlisted |
| Public verifier | PASS: 7 commands; 0 failed; 3 documented restricted-input skips |
| Main LaTeX clean build | PASS: 24 pages |
| Supplement clean build | PASS: 2 pages |
| Manifest after verification | PASS: 225 checked; 0 missing, mismatch, or unlisted |
| Checksum-list bytes unchanged | Yes |
| Release-manifest bytes unchanged | Yes |
| `.git` entries in extracted package | 0 |

The detailed out-of-package verifier record has SHA-256
`916F4379EB6E378A6296C6D6434E49D79BA0411EE1BAC98B36ED6C285DEAB48F`.
It was intentionally kept outside the extracted package so verification could
not create an unlisted release file.

This closes release repair R1 for the current protocol-ready snapshot. It does
not close the pending external scientific gates E1, E2, or confirmatory E3.

## Final revalidation after integrity and lineage repair

After adding the reference delta audit, full six-figure lineage, Figure 6
machine inputs, and integrity reports, the release was rebuilt from the updated
allowlist and verified again.

- Archive: `tmp/c2ges_zip_validation_20260906_final/C2GES_protocol_ready_public.zip`
- Size: 3,869,571 bytes
- SHA-256: `056C978BD5E08A56282D9F1303598862C841AD29A5E7CA8FE116B0BB232699A7`
- Allowlisted release files: 231
- Clean extracted root: no `.git`
- Manifest before/after: PASS, 231 checked, 0 missing, 0 mismatched, 0 unlisted
- Public verifier in extracted root: PASS, non-mutating, 0 failures
- Checksum SHA-256 before/after: unchanged
  (`6002967C4567968C458724E706B32B6AFC571F6CB75EE0F24BF6FC037737C21B`)
- Manifest SHA-256 before/after: unchanged
  (`C12B71A8A810C59C9071EE5601983F8C17D0AD085AFC53F947A8D071F520B8AA`)

This final revalidation supersedes the 225-file count above for the current
snapshot; the earlier run is retained as chronology rather than deleted.
