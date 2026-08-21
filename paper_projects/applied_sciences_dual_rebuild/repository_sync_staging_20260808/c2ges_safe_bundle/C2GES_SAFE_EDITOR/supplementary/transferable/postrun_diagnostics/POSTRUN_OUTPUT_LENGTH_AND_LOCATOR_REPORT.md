# Post-Run Output-Length and Page-Locator Diagnostic

Status: **PASS**. Evidence class: post-run descriptive diagnostic. No selector,
weight, prediction, reference summary, ROUGE value, inclusion decision, or
formal-test artifact was changed or regenerated.

## Frozen inputs and boundaries

- Immutable prediction ledger: 210 rows, SHA-256
  `AAE2BFE0E6C426B6A69D727F24239A07DFD7DBEE8A4CE228E86625CCDCA2338F`.
  It remains in `supplementary/restricted_local_only` and is excluded from the
  safe editor ZIP because it contains verbatim derived text.
- Protected test candidate table: SHA-256
  `A9342BD75BB5E20B61C9B06FE21B1FBA260347BFDB77B0AEBBA89A423DFCD127`.
  It is not packaged because it contains extracted source text.
- Word definition: number of nonempty Unicode whitespace-delimited tokens from
  Python `text.split()`.
- Character definition: number of Unicode code points in each selected unit.
- Table marker: exact, case-sensitive substring `Table`.

## Output-length result

All seven conditions and both budgets (14 groups) are recorded in
`output_length_summary.csv`; all 210 condition--budget--report records are in
`output_length_per_report.csv`. Full C2GES averaged 287.7 and 568.9 words at
K=5 and K=10. Relative to Semantic-MMR it used 103.0 and 214.5 more words;
relative to TextRank it used 110.7 and 199.9 more words. Across the 225 Full
selected-unit instances, 37 exceeded 100 words, 40 contained `Table`, and the
maximum was 270 words. These are equal-sentence but unequal-word comparisons;
they do not establish length-controlled superiority.

## Page-locator result

The join covered all 1,575 selected references from the 210 frozen rows. Every
`(report_id, sentence_id)` resolved to exactly one integer page within the
declared PDF page range. Candidate keys and output primary keys were unique;
there were zero unresolved references, invalid pages, duplicate keys, or
sentence-ID/source-order mismatches. The output contains condition, budget,
rights-safe report metadata, sentence ID, selection rank, page, source order,
declared pages, and source URL. It contains no source sentence, selected text,
prediction text, reference summary, PDF, or extracted candidate table.

## Artifact hashes

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| `OUTPUT_LENGTH_AUDIT.json` | 8,655 | `1E6C2CEB7F50D4DF52258867E39E321E96BED3D22EBDD5A638D416FB8480A405` |
| `output_length_per_report.csv` | 15,783 | `66CF5B103CFFCAA889EB998C1A2DA9A766F2A01E3132CA5228744144DFB5389E` |
| `output_length_summary.csv` | 1,789 | `18D3AE96ECCC4543BA822876EE3398F81C8C900C7A5E1EA2113E444DCD4EE599` |
| `selected_page_locator.csv` | 351,114 | `26AD087BA7355C0AD7A6EFF93948167C21C150DA759A55FE4F2EE76ECF304DBC` |
| `SELECTED_PAGE_LOCATOR_AUDIT.json` | 1,119 | `23D798219D369CA8DFB90165AECB25A720039F77799E96F8C0172C6C04B290A6` |

The two generating scripts are packaged under `scripts/`. Re-running them
requires the two protected, hash-pinned local inputs; the transferable outputs
above are non-verbatim and are included in the safe editor ZIP.
