# MA-SQLGrid R3 Reviews to FINAL Response Matrix

## Scope and status vocabulary

R3 is immutable. This matrix responds to the three independent AI-assisted
internal reviews in `reviews_round3/`; it is not a human editorial decision.

- `CLOSED-FINAL`: corrected and mechanically verified in this FINAL candidate.
- `MANUAL`: requires an author, rights holder, institution, editor, or public
  repository action; no automated substitute is claimed.
- `UNRESOLVED-SCIENTIFIC`: requires new, properly frozen scientific evidence.
- `BOUNDED-NO-RERUN`: no new evidence was created, but the claim is explicitly
  limited and the adverse/null evidence remains visible.

## Methods and statistics reviewer

| ID | R3 finding | FINAL action | Status | Evidence / remaining acceptance condition |
|---|---|---|---|---|
| M1 | No experiment estimates the end-to-end five-role effect | Preserved the exact title only as a framework identity; retained the explicit no-five-role-benefit boundary in title discussion, Abstract, Methods, Discussion, Limitations, and Conclusions | UNRESOLVED-SCIENTIFIC | Requires an untouched, call-matched integrated generation comparison; no historical-v3 rerun can close it |
| M2 | Applied power-grid semantic validity remains unmeasured | Preserved machine-silver status, zero qualified reviews, and required dual-review/adjudication language | UNRESOLVED-SCIENTIFIC + MANUAL | Requires qualified independent power-system/database reviewers, retained disagreements, adjudication, rights/ethics decision, and a distinct untouched confirmatory set |
| M3 | R3 scalar/result byte claim is false for BLOBs | FINAL executor charges `bytes`, `bytearray`, and `memoryview` at original length before hashing; total budget charges raw payload plus deterministic structure; 1/5/50 MB adversarial tests and trace/boundary tests added | CLOSED-FINAL | `code/sqlite_readonly_executor_final.py`; `tests/test_sqlite_readonly_executor_final.py`; `FINAL_EXECUTOR_TEST_REPORT.md` |
| M4 | Selector behavior is dominated by ties and source order | Kept 130/180 ties, mean multiplicities, reverse-order 117--118/180, and no selector-efficacy claim; no exposed-item tuning was performed | BOUNDED-NO-RERUN | A permutation-invariant rule must be developed without these exposed outcomes and tested once on untouched items to make a new efficacy claim |
| M5 | Release provenance has contradictory labels and no clean current object | Corrected executor docstring and manuscript version labels; renamed Table 7's last column; created a one-title FINAL allowlist package and clean-extraction audit | CLOSED-FINAL locally; MANUAL publicly | Public GitHub repository remains unsynchronized and must receive an author-approved immutable tag/commit |

## Power-grid application and engineering-safety reviewer

| ID | R3 finding | FINAL action | Status | Evidence / remaining acceptance condition |
|---|---|---|---|---|
| D1 | BLOB payloads bypass R3 byte limits | Same raw-payload fix and 14-test FINAL suite as M3; failure returns no partial rows and retains the exact failure kind and observed raw cell size | CLOSED-FINAL | 50 MB `zeroblob` fails a 1 KB cell limit deterministically |
| D2 | Exact title is stronger than integrated system evidence | Retained title at the author's request, but made framework-identity/no-efficacy meaning explicit and did not add a five-role benefit claim | UNRESOLVED-SCIENTIFIC | Requires the frozen four-condition, call-matched untouched study described in Limitations |
| D3 | Power-grid semantics and representativeness are untested | No LLM or author label was promoted to expert gold; authentic-structure assets remain machine silver | UNRESOLVED-SCIENTIFIC + MANUAL | Qualified two-reviewer-plus-adjudicator process and untouched external confirmation remain required |
| D4 | SQL admissibility is not user authorization or operational safety | Preserved this separation in Figure 1, robustness table, Methods, power-grid discussion, Data Availability, and Conclusions | CLOSED-FINAL as a claim boundary | No deployment or operational-safety claim is made; a real authorization stack remains outside scope |
| D5 | Rights, expert governance, and submission metadata are open | Added file-level `RIGHTS_INVENTORY.csv`; restricted/uncertain source assets are excluded from the local package; author order, affiliations, correspondence, funding, CRediT, all-author agreement, and conflict declarations were subsequently confirmed by the authors; the unretained exact Codex backend identifier is disclosed as a provenance boundary rather than a missing value to invent | MANUAL for rights/release; metadata closed | Permissions, ethics decision if experts are added, and repository release remain open |

## Applied Sciences and research-integrity reviewer

| ID | R3 finding | FINAL action | Status | Evidence / remaining acceptance condition |
|---|---|---|---|---|
| J1 | Title-level framework proposition lacks end-to-end/domain evidence | Same bounded title interpretation as M1/D2; no autonomous-agent or qualified domain-validity claim | UNRESOLVED-SCIENTIFIC | Untouched matched generation plus qualified domain review |
| J2 | Scalar/result byte boundary is contradicted | Same correction as M3/D1; old R3 code and review remain immutable; historical v3 counts were not rerun or reinterpreted | CLOSED-FINAL | Code/test/report definitions now agree |
| J3 | No current package and repository conflicts with manuscript | Built a FINAL candidate only from an explicit allowlist and verified a clean extraction; old archives are excluded, not deleted | CLOSED-FINAL locally; MANUAL publicly | GitHub synchronization/tag and author release approval remain required |
| J4 | Figure/table provenance incomplete; Figure 1 says R2; Table 7 says failures | Figure 1 is version-neutral; all four figures have output/source/generator hashes and caption-claim boundaries; Table 7 now says `Final-ledger omissions` | CLOSED-FINAL | `figures/FIGURE_LINEAGE.json`; final PDF visual-QA manifest |
| J5 | GenAI disclosure and mandatory declarations incomplete | Added a Methods disclosure covering prose, experiment/audit suggestions, code/LaTeX, provenance, build/QA, exclusions, validation, and author responsibility; subsequently inserted the author-confirmed correspondence, funding, funder-role, authorship, and declaration fields; the exact backend identifier/version was not retained in project records and is transparently reported without inference | CLOSED-FINAL for declarations and recorded GenAI use; MANUAL for rights | File-level permissions remain open; no unrecorded backend identifier is required or invented |

## Claims deliberately not added

The FINAL candidate does **not** state that five roles improve accuracy, that
release v3 was prospective, that Q039 is a semantic rescue, that the selector is
permutation invariant, that machine labels are qualified expert gold, that
SQLite admissibility proves user entitlement, or that the current GitHub
repository reproduces this candidate.

## Final disposition

The repairable R3 engineering and release-control defects are closed in the
local FINAL candidate. The exact-title end-to-end evidence and qualified
power-grid semantic validation remain unresolved scientific gates. File-level
permissions and the public repository tag remain manual pre-submission gates.
Consequently, this candidate is suitable for author/editor inspection but is
not represented as portal-ready or scientifically complete.
