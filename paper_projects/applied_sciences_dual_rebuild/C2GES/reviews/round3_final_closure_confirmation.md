# C2GES Round-3 Final Closure Confirmation

## Decision

**CLOSED.**

The three closure items are now fully closed. The add-on and exploratory trees are recursively covered and validate successfully; the bibliography/PDF defect is absent; and the canonical gzip transition record is honest and independently reproducible. The remaining workflow wording has been corrected consistently: because the manifest binds the final PDF, the generator status, current manifest status, and Supplementary Materials statement all say that the complete manifest is generated and verified **after compilation**.

Latest reviewed snapshot:

- TeX: 58,045 bytes, SHA-256 `AD4C3AE9F11D1D8D07BAE34D697E32ABD1252D883DCE20CACE30DBE11768D849`.
- PDF SHA-256: `BE3B9B9F0A9B4B4968A9C78D7B00CEB7B8C833EF7D63965D85AFACD865C5A34D`.
- PDF: 22 A4 pages, 762,464 bytes.
- BBL SHA-256: `B90323D04506E3D6F4A6F891B6D489EF368887220752FC836598B62E5C6E6042`.
- Bundle manifest SHA-256: `0D138D4A9628B6683C0CED2D96B4E415BE082BFE39D60DE9FFAF88708ABFF4D0`.
- Claim-source map SHA-256: `A4F6306F00A2FAE6D590188A471C06705D6C800ECA8F1D41C570B5B1A1EBF44E`.
- Gzip-transition record SHA-256: `73A19983E200FCCFAE4DE819B27F27A6D7DC2788334F2A8B50080E97ADB08F01`.
- Bundle-manifest generator SHA-256: `90C1E5C2D36104E5517A2C878F13C517435D8276F75072CEA1D210A86D7CD6F4`.

### Current-snapshot identity synchronization

The earlier closure record contained a record-only identity defect. Its TeX hash was stale relative to both the current file and the already verified bundle manifest. Its PDF SHA-256 was correct, but the stated byte count was not compatible with that same object. Direct hashing and manifest lookup now agree exactly on the TeX and PDF paths, sizes, and SHA-256 values above. The generator hash in the machine-readable closure record has likewise been synchronized to the generator already bound by the current verified manifest. No scientific source, compiled PDF, or bundle content was modified for this correction; therefore the scientific decision remains **CLOSED** with zero open technical issues.

## 1. Claim map, recursive bundle, verifier, and manuscript wording

### Artifact coverage — closed

`create_bundle_manifest.py` recursively walks both `REBUILD_C2 / "exploratory_v3"` and `REBUILD_C2 / "addon_round3"`. An independent set comparison between current files and manifest paths found:

- `addon_round3`: 120 actual files, 120 manifested, 0 missing, 0 extra;
- `exploratory_v3`: 26 actual files, 26 manifested, 0 missing, 0 extra.

The manifest declares 11,378 artifacts and 1,110,024,049 bytes; these equal the actual record count and summed byte count. `verify_local_bundle.py` independently verified every declared size and SHA-256.

The latest claim-map generator includes the gzip-transition record plus the add-on protocol, results, manifest, primary contrasts, primary table, exploratory protocol, manifest, validation, primary contrasts, and primary figure. `verify_claim_sources.py` passed for 24 source hashes, eight generated fragments, nine figures, and 28 citations. The manifest recursively supplies the full run-level closure behind those claim-facing artifacts.

`verify_bundle.ps1` invokes the local manifest verifier, current gzip verifier, corrected exploratory validator, and add-on validator. The complete command exited 0. Separate direct executions of both package validators also exited 0.

The substantive supplement and data-availability inventories are now aligned: both name the corrected exploratory-v3 package, prospectively frozen Round-3 add-on, canonical artifacts, current gzip payload/transition boundary, and the remaining human DOI/license action (`paper_applsci.tex:312,317`).

### Compilation/manifest ordering — closed

`create_bundle_manifest.py:80` and `bundle_manifest.json:3` now use `complete_local_manifest_generated_and_verified_after_manuscript_build`. The Supplementary Materials statement says, “Because the manifest binds the final PDF, it is generated and verified after compilation” (`paper_applsci.tex:312`). These locations now match the actual workflow.

The latest build completed successfully and produced a 22-page PDF. As expected, the pre-existing manifest then failed closed because the newly compiled PDF had a new byte hash. The manifest was regenerated **after** compilation and the complete `verify_bundle.ps1` chain was rerun successfully: 11,378 artifacts, 1,110,024,125 bytes, all SHA-256 hashes verified; all five canonical gzip checks passed; the exploratory and add-on validator stages exited successfully. This observed sequence confirms that the corrected wording is operational rather than cosmetic.

## 2. BBL and PDF bibliography rendering — closed

Case-insensitive independent counts are:

- BBL `the the`: 0;
- BBL `Proceedings of the the`: 0;
- extracted PDF text `the the`: 0;
- extracted PDF text `Proceedings of the the`: 0.

PDF pages 21–22 were visually inspected; proceedings entries now render normally. All 22 pages were rerendered from the latest PDF and inspected. No clipping, broken glyphs, malformed tables, unreadable figures, or new layout defect was found.

## 3. Canonical gzip transition — closed

`canonical_gzip_transition.json` explicitly says the prior compressed artifact is unavailable, exact cross-version decompressed identity cannot be proved, and byte-level immutability is not claimed. It binds only the current compressed and decompressed objects plus separately verified numerical invariance. This is the correct epistemic boundary.

`verify_canonical_gzip.py` independently reads and decompresses the bound artifact and checks compressed SHA-256/size plus decompressed SHA-256/size/line count. It passed. A separate reimplementation reproduced:

- compressed SHA-256: `3E61018BF06FDD0AF27E2504CF79CAB85ABC093722473E5E8445983BB55A5D8F`;
- compressed bytes: 1,846,866;
- decompressed SHA-256: `924D3DECAE9568ED0640673211217C164141CCA6CC50EBF07FF64ED6F8A0D939`;
- decompressed bytes: 28,360,935;
- decompressed lines: 180,001;
- gzip header mtime: `1785922045`, exactly matching the record.

The current gzip contains a source-filename header; the record does not pretend otherwise and correctly establishes a stricter future policy (`mtime=0`, no source filename, both hashes, new manifest version). The record does not claim an unavailable cross-version equivalence proof.

## Final gate

All three Round-3 technical closure items are **CLOSED**. No further scientific recomputation is required. External author metadata and permanent DOI/license review remain separate human submission blockers.
