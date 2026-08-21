# Round-3 Power-Grid Application and Engineering-Safety Review

## Review identity and frozen object

I reviewed this manuscript independently as a power-system data application and
engineering-safety reviewer. I did not edit the manuscript, source code, data,
or evidence. The reviewed object was:

- PDF: `build/paper_applsci.pdf`, 20 pages, SHA-256
  `1D1284C35F691717457A592FF24F48D68C29386B7C6D2ED9E7BCF0D4710BE1C6`;
- TeX: `paper_applsci.tex`, SHA-256
  `6B25DA628DA44F4A66852C1A0C366CB3E8F52951C06521C8F3B5DCD691C422B3`;
- R3 executor: `code/sqlite_readonly_executor_r3.py`, SHA-256
  `1474AF733B044491B65266C2EBBFD52E9E180C8291FCE2E725B881BFB37CD652`;
- R3 executor tests: `tests/test_sqlite_readonly_executor_r3.py`, SHA-256
  `60B9D698395C5EC95699860528508675B389EC48EC9EFA06D9797A43C4BC46C8`.

The PDF text corresponds to the reviewed TeX at the material claim locations. I
also reran the R3 test suite independently: 10/10 tests passed. Passing the
existing tests does not close the new adversarial case reported below.

## Recommendation

**Major Revision.** The manuscript is unusually candid about negative results,
historical outcome exposure, the non-grid status of BIRD, the ambiguity of Q039,
and the absence of qualified power-grid semantic review. Those disclosures are
strong. Nevertheless, it is not ready for final audit because one advertised R3
resource boundary is bypassable, and the retained title still identifies a
robust multi-agent power-grid framework although neither the integrated
five-role path nor qualified power-grid semantic performance has been evaluated
on an untouched domain resource. The first defect is code-correctable. The
second is an evidence gap that must be closed by a new study or made an explicit
submission-level positioning decision by the authors and editor.

## Five issues ordered by decision impact

### 1. The R3 cell-byte and result-byte boundary does not bound BLOB payloads

**Severity: Major.** This materially weakens the title-qualified robustness
claim and the executor contribution, but it is repairable without invalidating
the historical v3 results because the manuscript correctly treats R3 as an
additive implementation.

**Evidence anchor:** code, `sqlite_readonly_executor_r3.py:44-48,61-68,238-254`.
For a `bytes` value, `_json_value` replaces the payload by a dictionary
containing a digest and length. `_encoded_value_size` and the total-result
budget then measure that compact representation rather than the raw BLOB. The
existing oversized-scalar test at
`test_sqlite_readonly_executor_r3.py:82-91` covers formatted text, not a BLOB.

**Independent adversarial check:** against a temporary read-only SQLite file,
the following registered limits were used:
`max_cell_bytes=128`, `max_result_bytes=256`, and
`max_output_columns=1`. Queries `SELECT zeroblob(1000000)`,
`SELECT zeroblob(5000000)`, and `SELECT zeroblob(50000000)` all returned
`ok=true`; the last trace reported a returned BLOB length of 50,000,000 bytes.
Thus manuscript lines 153, 497, and 517 and the R3 test report overstate what is
bounded. The same design also cannot prevent SQLite/Python from materializing a
large text or BLOB before the post-fetch check, although the manuscript already
disclaims process-memory containment.

**Required revision:** either (a) reject BLOB-valued cells by policy, or (b)
charge `len(value)` for `bytes` before canonical redaction and charge raw cell
sizes consistently to the result budget. In both cases add stored-BLOB and
`zeroblob` regression tests above and below each limit. Rename the control to
“accepted response-payload budget” if it remains post-materialization, and state
explicitly that it is not a pre-allocation memory bound. Correct the module
docstring at lines 1-5, which presently says the R3 module was the boundary used
by the Round-2 study, contrary to the manuscript's non-retroactivity statement.

**Acceptance test:** a fresh test invokes at least 1 MB and 50 MB BLOBs under a
128-byte cell limit and 256-byte result limit and deterministically returns a
named failure with zero returned rows; below-limit BLOB behavior is specified
and tested. The full R3 suite passes, the code/report/manuscript use the same
budget definition, and new hashes are frozen.

### 2. The exact title remains stronger than the integrated system evidence

**Severity: Major.** The manuscript explicitly defines “multi-agent” as five
typed software roles and “robust” as a bounded vector, which prevents a false
autonomous-agent superiority claim. However, the Synthesizer only packages
external historical candidates, the Analyst and Cartographer are deterministic
skeletons, and no end-to-end five-role, call-matched, newly generated evaluation
exists. Calling the title a “framework identity” is a disclosure, not empirical
validation of the title's central conjunction.

**Evidence anchor:** text, `paper_applsci.tex:36-42,149-153,507,517-521`.
The paper itself states that GridDB and BIRD were not five-role executions and
that release v3 does not estimate generation, communication, latency, token, or
autonomous-agent effects.

**Required revision:** because the authors wish to retain the exact title,
complete the already specified hash-locked, call-matched integrated comparison
on genuinely untouched items (line 511), or obtain an explicit editorial
decision that an implementation-and-diagnostics framework paper is acceptable
without that efficacy evidence. Do not use another pass over the same 180
outcome-exposed items as a substitute.

**Acceptance test:** the new protocol freezes the model snapshot, candidates,
calls, decoding, database states, evaluator, order rule, endpoints, clustered
inference, multiplicity, and failure retention before test access; it compares
the complete five-role path with budget-matched controls and reports all
attempts, abstentions, latency, tokens, and adverse cases. If this cannot be
done, title/abstract/featured-application wording must be reduced further and
the editor must be shown the unresolved scope explicitly.

### 3. Power-grid semantic validity and representativeness remain untested

**Severity: Major.** The principal domain evidence is one synthetic,
development-visible database with eight tables and 98 rows. RTS-GMLC and
SimBench provide authentic structures, but all 91 question--SQL pairs are
machine silver, development-visible, unsealed, and have zero qualified-human
reviews. BIRD is a useful public portability benchmark but is non-grid. These
facts do not support claims about real maintenance, protection, dispatch, or
asset-management semantics.

**Evidence anchor:** dataset/text, `paper_applsci.tex:86-94,107-111,503-513`.
The local human-review templates are blank and therefore demonstrate protocol
preparation, not expert completion.

**Required revision:** obtain independent review by qualified power-system and
database experts using a frozen rubric, retained independent labels,
disagreements, adjudication, and qualification records. For confirmatory
performance, use a newly authored or deeply rewritten, family-isolated set that
was not visible during method development. The existing 91 items may be
reviewed as an unsealed development resource but must not be retroactively
called a sealed test. LLM or author triage must not be relabeled as independent
expert judgment.

**Acceptance test:** the paper and archive report reviewer qualifications,
independence, rubric version/hash, item counts, agreement, all conflicts,
adjudicated labels, corrected SQL re-execution, access history, and a clear
development/sealed split. Units, temporal boundaries, topology direction,
status codes, ordering, tie policy, empty results, and intended projection are
explicit fields in the rubric.

### 4. SQL admissibility is not user authorization or operational safety

**Severity: Major for deployment wording; Minor for the present explicitly
experimental study.** The manuscript correctly states that table/column/function
allowlists are caller-supplied query-scope controls rather than authentication,
row-level authorization, entitlement, process isolation, or operational
approval. This boundary must remain visible in every submission artifact;
otherwise “read-only decision-support framework” can be mistaken for an
authorized utility interface. Read-only access can still disclose sensitive
rows or produce a semantically unsafe result.

**Evidence anchor:** text/figure, `paper_applsci.tex:24,145,153,173-177,497`.
Figure 1 correctly places user authorization and operational approval outside
the implementation boundary.

**Required revision:** preserve the current featured-application warning and
add a concise deployment trust model identifying the authenticated principal,
policy-decision point, per-user row/column policy, audit-log custodian, data
owner, and mandatory human approval point. This may be a short table rather
than a new figure. Do not claim deployment safety until these controls and an
operator workflow have been evaluated.

**Acceptance test:** a claim search over title, abstract, highlights, figure
captions, discussion, conclusion, cover letter, and repository README finds no
statement equating query allowlisting with user entitlement or operational
approval. A negative permission test matrix is included if any deployment
claim remains.

### 5. Rights, expert-review governance, and submission metadata are still open

**Severity: Major as a submission-readiness defect.** The Data Availability
Statement is appropriately conditional, but it does not itself establish the
right to distribute or even provide each restricted file to reviewers. The RTS
notice is recorded locally as truncated, SimBench-derived data require an
ODbL/DbCL decision, GridDB redistribution status is unresolved, the public
repository is not asserted synchronized, and no final allowlist archive exists.
The corresponding-author email and exact funder identity/role also remain
manual placeholders. If professional annotation is added, an institutional
ethics/consent determination must be recorded before the current “not
applicable” statement is retained or changed.

**Evidence anchor:** absence/text,
`paper_applsci.tex:20,523-530`; `R3_ASSEMBLY_AUDIT.md`, “Open scientific and
manual blockers”; `data/simbench_pilot/W3_SIMBENCH_REPORT.md:9-21`.

**Required revision:** create a file-level rights inventory with source,
copyright holder, exact license/permission basis, transformation status,
allowed recipient, allowed purpose, redistribution decision, attribution file,
and package action. Build the editor/reviewer archive only from an explicit
allowlist and verify a clean extraction. Complete author email, funder wording,
all-author approval, repository tag/commit, and the ethics/consent decision for
any real expert annotation.

**Acceptance test:** every archive member maps to a completed rights row; no
credential, cache, obsolete manuscript, excluded incident presented as
evidence, or restricted source lacking permission is present. The clean-cloned
tag reproduces the public subset, and the manuscript's availability wording
matches the actual archive exactly.

## Claim--evidence audit

| Claim | Location | Verdict | Basis / required action |
|---|---|---|---|
| Five typed roles and deterministic controller are implemented | Abstract; lines 116-159; Figure 1 | **Supported as software architecture** | Code-derived diagram and tests support role contracts; no efficacy implication should be added. |
| R3 provides cell-byte and total-result-byte limits | Lines 153, 497, 517; executor test report | **Contradicted for BLOB payloads** | The independent `zeroblob` probe bypasses both advertised byte budgets; fix and refreeze. |
| Mutation denial and read-only SQLite behavior | Lines 151, 173; executor tests | **Supported within the tested local SQLite boundary** | Existing mutation, DDL, attach, pragma, metadata, and hash-stability tests passed; not a user-authorization claim. |
| “Robust multi-agent framework for ... power grid databases” | Title; lines 42, 521 | **Partially supported only as a declared framework identity** | Integrated five-role efficacy and qualified grid semantics remain absent. |
| BIRD supports portability, not grid validity | Lines 88, 94, 111, 334 | **Supported and properly bounded** | No revision needed except preserving this wording in all derivatives. |
| Q039 is a general counterfactual or engineering rescue | Lines 424-444, 491, 521 | **Explicitly rejected; appropriate** | The table exposes both SQL strings and unresolved status/date meaning. Preserve this negative interpretation. |
| RTS-GMLC/SimBench support power-grid accuracy | Lines 68, 94, 109-110, 509 | **Not supported, and manuscript correctly says so** | Requires qualified review plus an untouched confirmatory set before any accuracy claim. |
| Data/repository are submission-verifiable | Lines 523, 528 | **Not yet established** | Conditional prose is honest; actual rights inventory, package, tag, and clean-clone verification remain required. |

## Experiment audit

### Required before a submission candidate

1. Fix and adversarially retest raw BLOB/cell/result-byte handling; preserve the
   failed R3 implementation and this review as provenance rather than silently
   overwriting them.
2. For the exact retained title, run an untouched, call-matched integrated
   five-role comparison or obtain an explicit editorial scope decision and
   weaken all framework-efficacy implications.
3. Complete qualified dual review and adjudication for domain semantics, then
   reserve a genuinely untouched power-grid set for one-time confirmation.
4. Freeze and independently audit the new protocol and its access history
   before test execution.

### Desirable, not substitutes for the required work

- Fuzz SQLite functions and scalar types, including BLOB, very large text,
  JSON, recursive CTEs, collations, user-defined functions if ever enabled, and
  cancellation behavior; use an OS-level worker boundary for memory containment.
- Evaluate risk--coverage behavior of abstention and the practical review load
  imposed on operators.
- Add a power-grid error taxonomy for unit, equipment identity, temporal
  window, topology direction, status code, aggregation granularity, tie, and
  empty-result errors.

### Unjustified reruns

- Do not tune order, weights, or thresholds on the same 180 exposed items and
  then report 117--118/180 as confirmatory.
- Do not repeat BIRD and reinterpret it as power-grid validation.
- Do not convert the 91 development-visible silver candidates into a sealed
  test by adding labels after exposure.
- Do not use LLM votes as a substitute for qualified independent expert labels.

## Figure and table audit

- The 20-page render is clean and the four inspected pages, including the title,
  chronology table, power-grid safety discussion, and references, show no
  clipping or overlap. Figure 1 is preferable to an aspirational agent diagram
  because it exposes external candidate supply, the gold boundary, and the
  location of human authorization.
- Table 1 correctly separates synthetic grid, constructed states, authentic
  structures/machine silver, and non-grid BIRD. Table 11 is a strong adverse-case
  disclosure because it prevents Q039 from being marketed as semantic rescue.
- Table 3's “Resource boundedness” row currently lists only timeout/opcode/row
  endpoints, while prose adds cell/result/width controls. After the executor
  fix, either add the new limits and their exact evidence boundary to this table
  or remove the broader prose claim. Keep “worst-case bounds for every SQLite
  feature” in the not-established column.
- The resized tables are readable in the reviewed PDF, but production proofing
  should verify minimum text size after MDPI typesetting. No additional
  generative diagram is required for scientific validity.

## Reproducibility and engineering-integrity audit

**Strengths.** The manuscript binds exact source/PDF/evidence hashes, preserves
failed incidents, carries a supersession notice rather than rewriting history,
reports all sensitivity cells and tie multiplicities, and distinguishes the
21 freeze entries from test counts. The independent 10-test rerun passed.

**Residual defects.** Test coverage is not equivalent to the advertised input
domain; BLOBs are untested and bypass the byte budgets. The R3 module docstring
incorrectly attributes the additive module to the Round-2 study. The public
repository and final reviewer archive are not yet synchronized or verified.

## Ethics, authorization, and licensing

- No human-participant labels are used in the reviewed results, so the current
  “not applicable” statement is internally consistent for R3. It must be
  revisited if professional annotations are collected before submission.
- An LLM API can assist triage but cannot be called an independent power-system
  expert, and author adjudication cannot be described as independent dual review.
- Database read-only state is not informed authorization. Any operational use
  requires authenticated identity, institutional policy, data-owner approval,
  and authorized human inspection of SQL and source rows.
- “Available from the corresponding author” is valid only for files that the
  authors are legally and institutionally permitted to share with that
  recipient for that purpose. The completed rights inventory must control the
  package, not the generic sentence.

## Positive findings that should survive revision

1. **Negative-result integrity:** zero corrected primary factorial effects,
   failed selector efficacy, backbone-dependent BIRD behavior, high tie rates,
   and Q039 ambiguity are not hidden.
2. **Evidence-class discipline:** prospective component evidence, descriptive
   historical re-execution, machine-silver domain assets, and non-grid BIRD are
   kept separate.
3. **Operational restraint:** the featured application and discussion require
   human inspection and reject control/protection/maintenance validation claims.
4. **Q039 handling:** the manuscript gives the complete competing SQL and does
   not promote frozen-reference agreement to engineering correctness.
5. **Visual and provenance quality:** the reviewed PDF is legible, the diagram
   is code-native, and the main numerical artifacts are hash-bound.

## Final acceptance criteria for this reviewer

I would upgrade the recommendation only after all of the following are shown:

1. raw BLOB budgets are fixed or explicitly excluded, new adversarial tests
   pass, the module provenance text is corrected, and code/manuscript/report
   definitions agree;
2. the exact-title framework has a defensible integrated evidence path on an
   untouched power-grid resource, or an editor-approved narrower contribution
   interpretation is recorded without efficacy implication;
3. qualified independent semantic review and adjudication are complete, with a
   distinct untouched confirmatory set if external accuracy is claimed;
4. Q039 remains an ambiguous projection-stability trace and the 130/180 tie and
   reverse-order sensitivity results remain visible;
5. user authorization, operational approval, and SQL admissibility remain
   explicitly distinct;
6. file-level rights, ethics/consent determination, author/funder metadata,
   repository synchronization, final allowlist package, and clean-extraction
   audit are complete; and
7. a new frozen PDF/source/evidence audit resolves this report item by item
   without modifying the reviewed R3 record.

