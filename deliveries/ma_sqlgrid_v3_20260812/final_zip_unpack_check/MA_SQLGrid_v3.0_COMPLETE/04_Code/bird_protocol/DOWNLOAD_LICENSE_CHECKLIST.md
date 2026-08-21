# Official download and license checklist

**Audit date:** 2026-08-05. Only official/original sources are listed.

| Resource | Official source and pinned identity | Size / local SHA-256 | License / use decision | Status |
|---|---|---|---|---|
| BIRD current clean dev annotations | `birdsql/bird_sql_dev_20251106@3c11fb193e5439b338e23677fa0aae11e8b85db9`, `data/dev_20251106-00000-of-00001.json` | 946,793 bytes; `ffd8018378ddb1a8794753e0a31cfc81862ff7318a5184c22f3dc4ce03a03feb` | CC BY-SA 4.0; metadata audit only | Downloaded with project aria2-first helper |
| BIRD Mini-Dev SQLite annotations | `birdsql/bird_mini_dev@f65faf4ae3b638c1fa6df1d3370c8d92c8366301`, `data/mini_dev_sqlite-00000-of-00001.json` | 278,513 bytes; `88ceb0710163cae46a256ecea8f0a8c98286599530b60587fda5c3cfe57d45d2` | CC BY-SA 4.0; proposed complete 500-row population | Downloaded with project aria2-first helper |
| BIRD Mini-Dev README | `bird-bench/mini_dev@b3d4bcbbae9a96934ad812551eb400c7a3b23c12/README.md` | 19,219 bytes; `738ec9a76f6a4ff5d039ae61a640a7e7c1d6058cfa0a712092cad4567b07a9fe` | Dataset license inherited from BIRD announcement/card; repository has no SPDX license, so do not redistribute its code blindly | Downloaded |
| BIRD official DAMO README | `AlibabaResearch/DAMO-ConvAI@7635e3f7fd7136cddc462d7f184fd497d5bd5e4c/bird/README.md` | 9,683 bytes; `b6d648bfa97d60e237ba9ff751b7398fa6f34cde8c4945219f383cd672b9be2f` | Repository MIT; data README declares CC BY-SA 4.0 | Downloaded |
| BIRD dev SQLite databases | `https://bird-bench.oss-cn-beijing.aliyuncs.com/dev.zip` | 346,207,293 bytes; ETag `04B4AF221C9186361F09B16ABFD917EC`; local SHA-256 `cdd6d19faeb45a23970b98d3ef6c40a87987c95459c2cf12076897a60cf5a630` | BIRD data CC BY-SA 4.0; preserve notices, attribute, identify changes, ShareAlike derived redistribution | Downloaded and safely extracted 2026-08-05; 11/11 SQLite databases, zero unsafe paths/symlinks/reparse points; gold preflight PASS 500/500 under pinned SQLite 3.40.1; no model execution |
| BIRD official evaluation code | `https://github.com/AlibabaResearch/DAMO-ConvAI/tree/main/bird` | Pin exact commit and tree SHA before run | MIT at repository level | Not cloned; required before freeze |
| DKASQL article | DOI `10.3390/app152011121` | Version of record checked online | MDPI article license applies to article; no code license because no code release was found | Checked |
| ElecSQL | Article-supplied Google Drive folder | Size/hash not audited | Article calls it private while sharing a folder; license/redistribution terms are not stated in the Data Availability text | Do not download/use for this public baseline until written license and version identity are resolved |
| DKASQL source code | No official link located in article, supplement, data statement, DOI/title/author search | N/A | No implementation or code license to rely on | **Blocked; no reproduction claim** |

## CC BY-SA handling checklist

- [ ] Include BIRD citation and author/project attribution.
- [ ] Include a copy/link of CC BY-SA 4.0.
- [ ] State which files were unchanged and which metadata/prompts/manifests were derived.
- [ ] Apply compatible ShareAlike terms to redistributed adapted dataset material.
- [ ] Do not package database contents until redistribution scope has been reviewed.
- [ ] Preserve the exact upstream URL, revision, archive bytes, and locally computed SHA-256.

## Acquisition discipline

`download_official_resources.ps1` uses the workspace's aria2-first helper and only downloads the small pinned metadata by default. The database archive requires the explicit `-IncludeDatabases` switch. The archive has now been downloaded, hash-bound, safely expanded into a dedicated directory, and audited in `DATABASE_ARCHIVE_ACQUISITION.json`. `BIRD_GOLD_PREFLIGHT.json` now passes 500/500 under the pinned Python 3.10.11 / SQLite 3.40.1 runtime. Formal model execution remains prohibited until the remaining prompt, evaluator, leakage, hash, and independent-signature gates close.
