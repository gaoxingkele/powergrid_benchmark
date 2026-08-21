# W4 MA-SQLGrid Candidate Human-Review Packet Report

## Status and non-substitution boundary

The packet is ready for two real, independent reviewers. **No human review has been performed by this build.** The automatic scan is deterministic machine triage, not author judgment, expert validation, gold annotation, or sealed-test certification.

Input inventory:

| Dataset | Candidates | Status at input | Human-reviewed | Sealed |
|---|---:|---|---:|---:|
| RTS-GMLC | 55 | `AUTO_CANDIDATE` | 0 | 0 |
| SimBench | 36 | `AUTO_CANDIDATE` | 0 | 0 |
| Total | 91 | `AUTO_CANDIDATE` | 0 | 0 |

The A and B packets contain all 91 items in different deterministic orders. Neither form contains machine risk or flag fields, original source IDs, split assignments, template-family labels, or the other reviewer's decisions.

## Independent machine precheck

The precheck scans question/SQL pattern consistency, units visible in result-column names, empty and large results, ordering/tie wording, abbreviations, template similarity, query class, proposed difficulty and read-only SQL form.

| Dimension | Result |
|---|---:|
| Machine high-risk | 4 |
| Machine medium-risk | 69 |
| Machine low-risk | 18 |
| Empty results | 4 |
| Results over 50 rows | 6 |
| Maximum result rows | 131 |
| Unit-not-explicit hints | 44 |
| High within-family template-similarity hints | 57 |
| Top-k tie-policy hints | 22 |
| Domain-abbreviation hints | 2 |
| Ordering-convention hints | 1 |

The four high-risk items are all empty-result SimBench filters/topology queries:

- `SB-AUTO-008`: in-service lines longer than 2 km;
- `SB-AUTO-009`: loads above 1 MW maximum active power;
- `SB-AUTO-010`: controllable generators;
- `SB-AUTO-035`: lines connecting different nominal voltages.

An empty answer is not automatically wrong. Reviewers must decide whether it is intentional, useful, unambiguous and representative, or whether the threshold/question should be revised. The machine did not detect a simple keyword-level `how many`/`COUNT`, total/`SUM`, average/`AVG`, ranking/`ORDER BY LIMIT`, or join-class/`JOIN` contradiction. This negative heuristic result is weak evidence and does not establish semantic correctness.

The six results over 50 rows are RTS `RTS_AUTO_001`, `011`, `012`, `016`, `018`, and `020` (57–131 rows). Reviewers should judge whether an unbounded/list response is appropriate for a text-to-SQL benchmark and whether answer-shape expectations are explicit.

## Coverage audit

Unified proposed class counts:

| Class | Count |
|---|---:|
| Single-table | 6 |
| Filter | 16 |
| Join | 26 |
| Aggregate | 16 |
| Top-k | 21 |
| Topology | 6 |

Difficulty proposals comprise 22 easy, 58 medium and 11 hard items. There are 17 dataset-specific template families: 11 RTS families with 5 candidates each and 6 SimBench families with 6 candidates each. Existing family-level split policies remain visible only in the internal map; reviewers independently confirm class/difficulty rather than treating them as labels.

The corpus is rich in joins and top-k questions but relatively thin in topology and structurally simple single-table questions. It contains no human-authored natural requests and therefore cannot yet support a natural-query representativeness claim.

## Packet files

- `machine_precheck.jsonl`: 91 normalized items, risk flags and provenance. Triage only; withhold from reviewers.
- `machine_precheck_summary.json`: aggregate counts; explicitly records zero human reviews and zero sealed items.
- `reviewer_A_form.csv`, `reviewer_B_form.csv`: independent full-review forms with different item order.
- `review_item_map.csv`: protected blind-ID to source-ID/family/split/hash map.
- `conflict_adjudication_template.csv`: 91-row adjudication skeleton; use after A/B lock.
- `REVIEW_FIELD_DEFINITIONS.md`: allowed values, issue taxonomy and review meaning.
- `REVIEW_PROTOCOL.md`: independence, full/sampled review, adjudication and sealed gate.
- `agreement.py`: field-level coverage, raw agreement, Cohen's kappa and conflict extraction.
- `packet_hashes.json`: hashes of generated packet artifacts.
- `build_review_packet.py`, `test_review_packet.py`: deterministic builder and tests.

## Human execution requirements

For benchmark promotion, both real reviewers examine all 91 items. They independently judge overall disposition, question–SQL alignment, ambiguity, units, SQL correctness, usefulness, class and difficulty. Each revision requires a proposed question/SQL; every conflict goes to a third real adjudicator. Revised SQL must execute against the frozen database and receive a new result hash.

Exploratory resource-limited review may inspect all machine-high-risk items plus a deterministic 25% stratified sample of the remainder, but that sample cannot support claims that all 91 are human-reviewed or benchmark quality.

Suggested internal reliability targets are 100% coverage of critical fields, decision raw agreement of at least 0.85, and Cohen's κ of at least 0.75 for decision, semantic alignment and SQL correctness. These are project gates, not Applied Sciences requirements. Agreement quantifies consistency and cannot prove correctness.

## Sealed promotion gate

The current candidates are development-visible. A later human review cannot retroactively make a previously used item sealed. An item may enter a genuinely sealed subset only if access history proves it was never used for method/prompt/repair/threshold/model selection, and if it passes dual review, adjudication, duplicate/family leakage tests, source-license review, hash freeze, access control, method freeze and a single no-drop sealed execution. Otherwise it remains a human-reviewed **unsealed** item.

The preferred sealed set is newly authored or deeply rewritten by real people after development data and methods are frozen, with the model-building team denied access until the registered final run.

## Validation

Commands:

```powershell
python build_review_packet.py
python -m unittest -v test_review_packet.py
```

The final suite covers exact 55+36 counts and status boundaries; dataset/family/class/difficulty coverage; blind-form isolation and differing order; complete ID mapping and adjudication skeleton; known-value Cohen κ; end-to-end agreement CLI; and deterministic packet rebuild.
