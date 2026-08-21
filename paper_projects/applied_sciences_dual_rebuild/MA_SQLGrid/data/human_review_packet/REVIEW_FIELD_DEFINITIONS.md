# Review field definitions

The A and B forms contain the same 91 items in different deterministic orders. Reviewers work independently and must not inspect the other form, `machine_precheck.jsonl`, or prior decisions until both forms are signed and frozen.

## Required judgments

| Field | Allowed values | Meaning |
|---|---|---|
| `decision` | `ACCEPT`, `REVISE`, `REJECT` | Overall disposition before adjudication |
| `semantic_alignment` | `YES`, `NO`, `UNCERTAIN` | SQL and its result answer exactly the natural-language request |
| `question_unambiguous` | `YES`, `NO`, `UNCERTAIN` | A competent grid-data user would infer one intended answer |
| `units_correct` | `YES`, `NO`, `NOT_APPLICABLE`, `UNCERTAIN` | Units are stated or unambiguously implied and agree with fields |
| `sql_correct` | `YES`, `NO`, `UNCERTAIN` | SQL faithfully implements the intent and uses sound ordering/grouping/filtering |
| `answer_useful` | `YES`, `NO`, `UNCERTAIN` | Result is meaningful for the stated request; empty answers may still be useful if intentional |
| `query_class_reviewed` | `single_table`, `filter`, `join`, `aggregate`, `top_k`, `topology`, `other` | Human-confirmed primary class |
| `difficulty_reviewed` | `easy`, `medium`, `hard` | Relative SQL reasoning difficulty under the supplied schema |
| `issue_codes` | pipe-separated controlled codes | All detected issues; use `OTHER` plus notes if needed |
| `proposed_question`, `proposed_sql` | text | Required for `REVISE`; leave original unchanged for `ACCEPT` |
| `confidence_1_to_5` | integer 1–5 | Confidence in the review, not item difficulty |
| `reviewer_qualification` | text | Relevant SQL/data/power-system background; no identity fabrication |
| `reviewer_signature`, `completed_at_utc` | text, ISO-8601 | Accountability and lock record |

Controlled issue codes:

`AMBIGUOUS_SCOPE`, `AMBIGUOUS_ORDER`, `MISSING_UNIT`, `WRONG_UNIT`, `QUESTION_SQL_MISMATCH`, `EMPTY_ANSWER`, `UNBOUNDED_RESULT`, `DUPLICATE_TEMPLATE`, `UNNATURAL_LANGUAGE`, `DOMAIN_TERM_UNCLEAR`, `WRONG_DIFFICULTY`, `WRONG_QUERY_CLASS`, `SQL_ERROR`, `ANSWER_NOT_USEFUL`, `OTHER`.

The proposed class/difficulty is context, not truth. Result preview is limited to five rows. Reviewers should consult the frozen SQLite database and the corresponding field dictionary when the preview is insufficient:

- RTS-GMLC: `../rts_gmlc_pilot/artifacts/field_dictionary.csv`
- SimBench: `../simbench_pilot/field_dictionary.csv`

Machine precheck flags must not be copied into human decisions. They are withheld from A/B forms to reduce anchoring.
