# Deterministic Build Audit after Author-Metadata Migration

Date: 2026-08-06  
Fixed epoch: `2026-08-05T00:00:00Z` (`SOURCE_DATE_EPOCH=1785888000`)  
Result: **PASS for both manuscripts**

The user explicitly authorized reuse of author and affiliation information from the paired CMC manuscripts. Only author names/order, affiliations, corresponding-author identity, and the available corresponding email were migrated. Scientific content and experimental results were unchanged.

| Paper | TeX identity | Build 1 | Build 2 | PDF | Result |
|---|---|---|---|---|---|
| MA-SQLGrid | 71,708 bytes; `2724D78D...0EC3` | `CF67243F...F96F` | `CF67243F...F96F` | 25 pages; 664,506 bytes | PASS |
| C2GES | 58,318 bytes; `4875F425...5D7D` | `2694417B...90CF` | `2694417B...90CF` | 22 pages; 763,005 bytes | PASS |

For MA-SQLGrid, the semantic portable manifest was regenerated because it binds the manuscript source. Both local-root and clean-copy verification passed 19 files; the new manifest SHA-256 is `513C8556...3588`.

For C2GES, the post-build reproducibility manifest was regenerated and verified: 11,378 artifacts, 1,110,025,006 bytes, every SHA-256 matched, and all five canonical gzip checks passed. Its manifest SHA-256 is `7FD1C0F6...1F5A`.

Build logs contain zero LaTeX errors, undefined references/citations, or overfull boxes. MA-SQLGrid retains four nonfatal underfull boxes; C2GES has none.

This audit supersedes the prior deterministic build identities. Remaining author attestations, license decisions, external validation, BIRD authorization, and permanent repository identifiers are unchanged.
