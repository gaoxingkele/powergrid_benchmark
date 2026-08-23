# C2GES Layout-Aware Extraction-Unit Audit Protocol

Status: frozen before running the audit on 2026-08-23. This is a post-result extraction diagnostic over the 27 already included reports. It does not replace the frozen experiment or release third-party text.

## Inputs

- Source manifest: 40 rows, SHA-256 `753939D6500320AD2E3DE1CED3E145399E90A9395E85A16DADE31D166C22BFE2`.
- Frozen development JSONL: 12 reports, SHA-256 `27CE41D37D8BA7B0BBA9D80072B3A3FAC742CEB4997E30DF0BE40CC5B2DF7F79`.
- Frozen retained-test JSONL: 15 reports, SHA-256 `A9342BD75BB5E20B61C9B06FE21B1FBA260347BFDB77B0AEBBA89A423DFCD127`.
- The source PDF SHA-256 for every included report must match the hash recorded in its frozen JSONL row.

## Layout-aware unit construction

Use PyMuPDF text blocks and their page coordinates, not page-wide merged text. Process only pages at or after the frozen `candidate_min_page` boundary.

For each page:

1. obtain text blocks with bounding boxes;
2. mark blocks in the top 8% or bottom 8% of page height as margin material;
3. use PyMuPDF table detection and mark blocks whose bounding area overlaps a detected table by at least 25%;
4. mark normalized block strings recurring on at least 20% of report pages (minimum three pages);
5. exclude margin, table, recurrent, blank, and non-text blocks;
6. split text only within a retained block, preserving block/page identity;
7. discard units shorter than 35 characters or six alphanumeric word tokens;
8. normalize and deduplicate exact units, retaining the first page/block occurrence.

This block-preserving rule prevents a sentence from being formed by joining unrelated columns or a table with narrative text across block boundaries. It does not claim perfect reading order or semantic segmentation.

## Nonverbatim outputs

- per-report counts of pages, source blocks, detected tables, drop reasons, layout units, exact overlap with legacy units, and long-unit rates;
- aggregate counts and runtime identities;
- deterministic sample audit rows for the first, median-position, and longest retained unit per report, containing only document ID, page/block/bounding-box ratios, length, normalized-text hash, and legacy exact-match flag.

No source, candidate, reference, title, URL, or SQL text is written to public outputs. An optional restricted text export is deliberately out of scope for this audit.

## Acceptance checks

- exactly 27 included reports and their recorded PDF hashes match;
- all processed pages respect the frozen body boundary;
- zero public output fields named `text`, `reference`, `summary`, `title`, or `url`;
- deterministic reruns yield identical non-time-varying CSV/JSON content;
- table-detection failures are counted and cannot be silently interpreted as successful table removal.

The resulting diagnostics do not establish improved ROUGE, human coherence, or engineering usefulness. A prospective external experiment must rebuild candidates under this rule, freeze word budgets, and obtain independent structure/utility review.
