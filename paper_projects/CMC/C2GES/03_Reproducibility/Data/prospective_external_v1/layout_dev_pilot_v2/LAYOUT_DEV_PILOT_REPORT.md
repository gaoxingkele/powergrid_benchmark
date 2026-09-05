## Material Passport

- Artifact: C2GES layout-aware candidate-builder development pilot v2
- Evidence class: implementation/reproducibility evidence
- Verification status: `VERIFIED` for execution integrity;
  `PENDING_HUMAN_REVIEW` for candidate validity
- Data scope: 12 existing development reports in 6 report series
- Confirmatory use: prohibited
- External test accessed: false

# Development-pilot outcome

The builder produced 3,782 layout-aware candidates and a 244-row non-verbatim
human-audit sample. It detected 86 table regions with zero page-level table
detection failures. Candidate types were retained separately as body, heading,
list item, table unit, caption, and footnote. The audit sample contains up to 30
examples per type and risk-enriched strata comprising 40 possible fragments, all
13 repaired cross-boundary units, and all 23 units longer than 256 tokenizer
tokens.

The non-mutating validator confirmed consecutive candidate identifiers and source
order, monotonic page locators, recomputed word counts, table/non-table block-ID
separation, public-schema privacy, sample-locator existence, and all bound hashes.

This output does not establish candidate validity. Across the full development
output, 364 units remain marked `possible_fragment`; these and other sampled units
must be reviewed independently by two humans under
`../LAYOUT_BOUNDARY_AUDIT_PROTOCOL.md`. The builder may advance to external freeze
only if the adjudicated overall validity rate is at least 0.90 and the table/body
fusion error rate is at most 0.05.

# Reproduction

Run the builder only with the existing development JSONL and local official-report
PDFs. Store `layout_dev_candidates_v1.jsonl` outside the release scope, then run:

```text
py -3.12 validate_layout_run.py --private-output <private-v2-dir> --public-audit-output <public-v2-dir>
```

Expected terminal line: `LAYOUT VALIDATION PASS`.
