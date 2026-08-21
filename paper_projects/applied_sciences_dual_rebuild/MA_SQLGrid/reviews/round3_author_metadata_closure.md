# MA-SQLGrid Author-Metadata Superseding Closure

Date: 6 August 2026  
Auditor: `/root/ma_round3_closure_a`  
Decision: **SCIENTIFIC_CLOSED_HUMAN_GATES_OPEN**

## Scope and supersession

This independent, read-only audit follows the authorized migration of author names, affiliations, and corresponding-author metadata from the paired CMC manuscript. I did not recompile or modify the manuscript, experiments, release, or build artifacts.

This closure **supersedes the build identity only** in `round3_deterministic_build_closure.md/json`:

- prior TeX SHA-256: `E8FECF6C8D4223BA75B87FCDAE97EEE6A66035BE500CBD9B0B3991752644C420`;
- prior PDF: 25 pages, 664,597 bytes, SHA-256 `789696175B80A1CE2778524F0D293A54287233097F4F7235C7FBD5D2AD92A0A4`;
- current TeX: 71,708 bytes, SHA-256 `2724D78D2D2CDBD74E06783094FE07795E326BF2042803A606EB3EE2CDED0EC3`;
- current PDF: 25 pages, 664,506 bytes, SHA-256 `CF67243F9D6C100BDA76C3965E6513D2801741A1A5BF773C990FCCD23C8AF96F`.

The prior closure files remain historical records. Scientific findings and experiment results are unchanged.

## Author-metadata provenance

The source `paper_projects/2026_ma_sqlgrid_cmc/source/manuscript_cmc/paper_cmc.tex` has SHA-256 `3CFF9C5945FE36A1287058AEC3037E99D1E1E3141659ACE34C81C8A2BE832AF0`. The migration record `AUTHOR_METADATA_MIGRATION_2026-08-06.json` has SHA-256 `731A55617261FCEBA0E21746A55F94B3020AA86F6AEEA0759D424AD99600D94D` and records explicit user authorization.

Source and target agree exactly on:

- author order: Bijing Liu; Chenglong Sun; Yong Yang;
- affiliation indices 1 and 2 for all three authors;
- affiliation 1: NARI Group Corporation (State Grid Electric Power Research Institute), Nanjing 211106, Jiangsu Province, China;
- affiliation 2: Beijing Kedong Electric Power Control System Co., Ltd., Beijing 100080, China;
- corresponding author: Yong Yang;
- corresponding email: `yangyong1@sgepri.sgcc.com.cn`.

No non-corresponding-author email or ORCID was inferred. The author-name, affiliation, and correspondence gate is therefore closed by authorized migration; it is not conflated with CRediT or declaration approval.

## Identity, deterministic build, and release evidence

The current TeX/PDF identity is synchronized across the Round-2 response, Round-3 response, and `W10_ASSEMBLY_REPORT.md`. These records now correctly describe author identity as resolved while retaining CRediT and other attestations as open.

The current `DETERMINISTIC_BUILD_AUDIT.json` (SHA-256 `B21E8194D772AC6E6B9499ADAF62564F2FEFC72B185CD94FCDFC0195A55245C2`) records two fixed-epoch builds with the identical PDF SHA-256 `CF67243F9D6C100BDA76C3965E6513D2801741A1A5BF773C990FCCD23C8AF96F`, 25 pages, and 664,506 bytes. The retained final log contains zero LaTeX errors, zero undefined references/citations, and zero overfull boxes; four underfull boxes are nonfatal.

Because the portable release binds the TeX source, it was regenerated. The current 18-artifact manifest has SHA-256 `513C855638395B8A09D56CD04D8386123FABE5BB055F26271362223A346C3588`. Local and clean-copy reports both pass 19 files including the root marker. Independent read-only hash/byte checks found zero mismatches in either root. Scientific denominators and results are unchanged.

## Remaining non-identity human gates

The following remain **HUMAN_GATE_OPEN** and are not internal scientific failures:

1. Explicit human authorization for the frozen 5,000-call BIRD run; status remains `FROZEN_NOT_RUN`, with zero formal calls and no BIRD result in the manuscript.
2. Qualified dual review/adjudication of the external grid pairs and a sealed follow-up set.
3. Author-approved CRediT roles and any journal-requested non-corresponding-author emails; no absent values or ORCIDs were fabricated.
4. Author-approved funding, conflicts, acknowledgments, ethics/consent, and AI-use declarations.
5. GridDB/derivative license review and an authorized permanent repository DOI or URL.

Accordingly, the author identity migration and all internally executable scientific/reproducibility work are closed. Submission readiness remains false until these five human gates are completed.
