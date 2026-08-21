# Round 3 Independent Review — Applied Sciences and Research Integrity

## Scope and independence

I reviewed the frozen R3 TeX and 20-page PDF, the round and structural audits,
the visual-QA manifest and page renders, the R2-to-R3 response matrix, the
supersession record, complete R3 evidence tables, the frozen v3 release audit,
the additive executor and tests, the available delivery/reviewer archives, and
the current public repository. I did not edit the manuscript, code, results, or
other reviews. This report is an AI-assisted internal reviewer simulation, not
qualified human peer review or a substitute for the editor's decision.

## Recommendation

**Major revision; not ready for final audit or submission.**

R3 is materially stronger and unusually candid about negative and
outcome-exposed evidence. I independently verified the exact title and author
order, the 20-page A4 PDF, all 57 round-audit file hashes and byte counts, all
20 visual-render hashes, 13 cited bibliography keys, four figures, twelve
tables, one algorithm, and one displayed equation. The PDF has no clipping,
overlap, unresolved citation, or alternate-title manuscript. The complete tie
ledger independently reproduces 130/180 top-score ties for both adjudicating
selectors, mean multiplicities 5.4000 and 5.3889, the printed multiplicity
distributions, and 178/180 original-order choices from Qwen slots. The
supersession notice is consistently reflected in the abstract, Results,
Discussion, and Conclusions: 80/180, 100/180, and 101/180 are descriptive
historical-pool results, and Q039 is not presented as a general gain.

Those strengths do not close the submission gate. The central title-level
proposition remains untested end to end and lacks qualified power-grid semantic
validation. More immediately, the R3 executor's claimed scalar-cell byte limit
is false for BLOB values. I reproduced a 10,000,000-byte `zeroblob` being
accepted with a 1,024-byte cell limit and a 4,096-byte total-result limit. The
final round-bound archive does not exist, the two available archives contain a
different title and older manuscript, and the public repository still presents
the earlier context-grounding paper and different experiments. Figure lineage
is incomplete, and mandatory human metadata, rights, AI-disclosure, and release
actions remain open.

**Confidence: 5/5.** The recommendation is based on direct source inspection,
independent hash and arithmetic recomputation, a fresh 10/10 test run, an
adversarial executor reproduction, PDF-page inspection, archive inspection,
and the current official MDPI ethics and journal-scope pages.

## Five most serious issues

### 1. The retained title is broader than the integrated scientific evidence

**Severity:** Blocking scientific defect  
**Locations:** `paper_applsci.tex:15, 22, 34--42, 116--164, 477--521`  
**Evidence:** direct manuscript/code/evidence inspection

The manuscript implements an inspectable five-role software decomposition, but
does not evaluate the named five-role system in a contemporaneous,
budget-matched generation experiment. The Analyst and Cartographer are
deterministic skeletons, the Synthesizer packages externally generated SQL, and
release v3 only selects among eight historical candidates. Thus no reported
contrast estimates an agent, handoff, communication, candidate-generation, or
five-role effect. The text now discloses this accurately, but disclosure does
not supply the missing evidence behind “robust multi-agent framework”.

The power-grid part is likewise bounded. GridDB is synthetic and
development-visible; BIRD is non-grid; and RTS-GMLC, SimBench, and NERC-derived
question--SQL assets have zero completed qualified-human semantic reviews.
Execution equality cannot adjudicate units, codes, temporal boundaries,
topology, ties, or intended aggregation. The title can remain as the requested
framework identity only if the paper and cover letter prominently state that it
does not denote demonstrated multi-agent superiority or general power-grid
validity. A strong scientific closure still requires the matched untouched
study and qualified semantic adjudication described below.

**Acceptance test:** execute a frozen, call-matched comparison on genuinely
untouched power-grid items: direct one-candidate generation; staged
question/schema handoff with one candidate; matched multi-candidate
validation/adjudication without counterfactual witnesses; and the same pool
with preregistered reference-free witnesses. Hold model snapshot, decoding,
question order, candidate count, physical calls, evaluator, retry/failure
policy, and abstention rule constant. Independently adjudicated reference SQL
and item semantics must be retained with reviewer qualifications,
disagreements, adjudication, and license/ethics determinations.

### 2. The claimed scalar-cell byte boundary is contradicted by the code

**Severity:** Blocking integrity/engineering defect; repairable without
rerunning historical v3  
**Locations:** `code/sqlite_readonly_executor_r3.py:1--10, 44--67, 214--257`;
`tests/test_sqlite_readonly_executor_r3.py`; `EXECUTOR_R3_TEST_REPORT.md`;
`paper_applsci.tex:153, 164--175, 497, 507, 517`  
**Evidence:** fresh test execution and adversarial reproduction

`_json_value(bytes)` replaces raw bytes with a small dictionary containing a
SHA-256 digest and the original length. `_encoded_value_size` then measures
that dictionary, not the raw BLOB. The total-result budget uses the same
surrogate. My independent reproduction was:

```text
SQLiteReadOnlyExecutor(max_cell_bytes=1024, max_result_bytes=4096)
  ("SELECT zeroblob(10000000)")
=> executable=true, failure_kind=null, row_count=1,
   returned BLOB length=10000000
```

The fresh published suite still passes 10/10 because it tests oversized TEXT,
not BLOB. Width and explicit-function controls work for the registered tests,
but “maximum scalar-cell bytes” and an unqualified result-memory boundary are
not implemented for raw BLOBs. In addition, the R3 source docstring calls this
“the actual database boundary used by the Round-2 offline study”, whereas the
paper correctly states that the R3 controls were added later and were not used
for release v3.

**Acceptance test:** enforce raw byte length for `bytes`/BLOB before hashing,
retain a separate canonical-output budget, and add adversarial tests for large
TEXT, `BLOB`/`zeroblob`, aggregate output, many rows, wide projections, and
function denial. A 10 MB BLOB must fail a 1 KB raw-cell limit, return no partial
rows, and record the exact failure kind. Correct the docstring, Methods,
operational-robustness table, test report, Discussion, and Conclusion; rebuild
and regenerate every dependent hash. Do not rerun or reinterpret v3 counts.

### 3. No current submission/reviewer package or synchronized repository exists

**Severity:** Blocking release-integrity defect  
**Locations:** `paper_applsci.tex:523, 528`;
`R2_TO_R3_RESPONSE_MATRIX.md:J1/G4/G5`; external delivery and reviewer ZIPs  
**Evidence:** archive listing/content inspection and live repository inspection

The manuscript honestly says that a final archive “must be generated”; it has
not been generated. The two available archives have SHA-256 values
`99E1470C...10EDE1` and `C2C1B886...99FFF` and contain the alternate title
“A Multi-Stage Context-Grounding Framework ...”, older TeX/PDF, caches, and
evidence not bound to this R3 round. They cannot be submitted or sent as the
current reviewer package.

The public repository at <https://github.com/gaoxingkele/ma-sqlgrid> (checked
2026-08-08) likewise describes the earlier context-grounding title and
GPT-5.4-mini/DeepSeek experiments, while the R3 manuscript reports the
Qwen/Granite factorial, component, BIRD, and descriptive release-v3 evidence.
The page exposes no matching immutable release/tag. The R3 Data Availability
Statement correctly avoids claiming synchronization, but a bare link to this
state would confuse reproducibility and provenance.

**Acceptance test:** quarantine—not delete—the old archives; build a new R3
archive from an explicit allowlist; include the exact final TeX, PDF,
bibliography, all used figure/data lineage, code, tests, complete numeric
tables, controlling supersession/release audits, rights inventory, incident
index, and README. From a clean extraction, verify source/PDF/package hashes,
compile and run the registered verifiers, and scan for alternate titles,
credentials, `.env`, caches, unauthorized third-party data, and excluded
incidents presented as evidence. Synchronize the public repository or cite a
new immutable tag/DOI whose clean clone reproduces the package.

### 4. Figure/table provenance and presentation are not fully closed

**Severity:** Major release-control defect  
**Locations:** Figure 1 and caption (`paper_applsci.tex:140--145`); Table 7
(`343--354`); `figures/FIGURE_LINEAGE.json`; `VISUAL_QA_MANIFEST.json`  
**Evidence:** direct page and manifest inspection

The current 20-page visual manifest is valid and all page hashes match. The
four figures and twelve tables are visible without clipping. Nevertheless,
`FIGURE_LINEAGE.json` binds only Figure 1 and calls the round “R2”; the
architecture image itself says “R2 fail-closed coordination”, and its filename
and manuscript caption also retain R2. No round-bound lineage entries are
provided for Figures 2--4, even though they carry quantitative claims. The
response matrix therefore closes J4 too strongly.

Table 7 labels its final column “Failures” but every value is “0 final
omissions”; that is not a failure taxonomy and can be mistaken for zero parsing,
authorization, execution, or provider failures. Tables 1 and 2 are unusually
dense and use small text; Table 11 is compact but remains legible in the
144-dpi render.

**Acceptance test:** create lineage for all four used figures with source
tables/JSON, generator code, source/render hashes, and caption-claim boundaries;
make the architecture label version-neutral or R3-accurate; rename Table 7's
column to “Final-ledger omissions” and report other failures separately if
available; improve Tables 1--2 at normal reading scale; then render and inspect
the exact new final PDF and rebind every page hash.

### 5. Journal-facing AI disclosure and mandatory manual declarations remain incomplete

**Severity:** Major compliance defect plus portal blockers  
**Locations:** `paper_applsci.tex:20, 22, 525--530`  
**Evidence:** manuscript and current official MDPI policy

The author list, affiliations, corresponding-author identity, grant number
`521300250006`, CRediT roles, “All authors have read and agreed ...” sentence,
Data Availability limitations, and conflict declaration are present. However,
Yang Yong's email is still a placeholder; funding-agency identity and funder
role are unconfirmed; author/order/affiliation approval, file-level third-party
rights, repository release, and final all-author approval have no signed
record. These are correctly disclosed as open, but a manuscript with those
placeholders is not ready for portal upload.

The Acknowledgments mention “OpenAI Codex (GPT-5-based)” for drafting, code
review, and reproducibility checks. Current MDPI ethics policy requires GenAI
uses beyond ordinary text editing to be declared during submission, detailed
in Materials and Methods, and identified by product/version and purpose in the
Acknowledgments. R3 has no Methods subsection explaining what code,
data/labels, analysis, figures, or scientific decisions were or were not
produced with GenAI, and “GPT-5-based” is not an exact recorded model/version.
Machine-generated external question--SQL assets are acknowledged generically,
but their providers/models/stages are not inventoried where records exist.

The abstract is approximately 235 words by a conservative token count and is
dense with audit chronology. Common current MDPI instructions recommend about
200 words; the Applied Sciences instruction endpoint returned HTTP 429 during
this check, so the exact journal-specific limit is **待核实**, not assumed.

**Acceptance test:** obtain written author confirmations for correspondence,
metadata, funding agency and sponsor role, rights, and final declarations. Add
a Methods disclosure inventory that distinguishes text editing, code
generation/review, experiment design, data/question generation, machine
adjudication, analysis, and figure production, with exact tool/model/version
where logged and explicit author validation/responsibility. Recheck the live
Applied Sciences instructions immediately before submission and shorten the
abstract if the current limit requires it. If qualified professional annotation
is added, obtain the institution's ethics/consent determination before carrying
forward “Not applicable”.

## Claim--evidence audit

| Claim | Exact location | Verdict | Required boundary/action |
|---|---|---|---|
| Exact original title and named five-role architecture | Title; Abstract; Sections 1 and 3.3; Figure 1 | **Supported as a software/framework identity.** | Does not establish autonomous-agent, coordination, or accuracy benefit. |
| “Robust” means tested mutation denial, bounded execution, complete evidence, and three witnesses | Sections 1, 3.4, 5.4, 7 | **Partly supported.** Mutation denial, width/function controls, and fail-closed evidence are tested; raw BLOB cell/result bounds are contradicted. | Repair Issue 2 and keep robustness vector-bounded. |
| R3 executor has maximum scalar-cell and total-result byte controls | Section 3.3; Table 3; Conclusion; test report | **Contradicted for raw BLOBs.** A 10 MB BLOB passes 1 KB/4 KB registered limits. | Fix code/tests or relabel as canonical exposed-representation budgets with explicit raw-memory exclusion. |
| v3 produces 80/180, 100/180, 101/180 over one shared 5760-attempt collection | Abstract; Sections 3.8, 4.7, 5.3; Table 9 | **Numerically supported only as descriptive historical-pool behavior.** | Supersession notice must remain first authority; no prospective/confirmatory wording. |
| Both adjudicators tie on 130/180; means 5.4000/5.3889; reverse order yields 117--118/180 | Abstract; Tables 10 and 12; Discussion; Conclusion | **Supported. Independently recomputed exactly.** | No post-hoc preferred-order claim. |
| Q039 is the sole full-vs-no-CF selection difference | Table 11; Sections 4.7 and 5.3 | **Supported as a constructed, outcome-exposed projection trace.** | Not semantic rescue, counterfactual gain, or grid correctness. |
| 700-call component release is prospective and separately audited | Abstract; Sections 3.6 and 4.3 | **Boundedly supported by its separate retained audit.** | It is component evidence, not five-role evidence. |
| Power-grid semantic validity | Title/featured application; Table 1; Limitations | **Not established.** The text generally says so accurately. | Qualified independent semantic review and untouched applied evaluation are needed. |
| Current public repository/package reproduces R3 | Supplementary Materials; Data Availability | **Accurately stated as not yet true.** Existing public/archive content conflicts with R3. | Build/tag/clean-extract before any positive availability claim. |
| Author, funding, AI, and ethics declarations are complete | Back matter | **Partly supported; manual and policy gaps remain.** | Close Issue 5 before portal upload. |

The title, abstract, Results, Discussion, and Conclusion are internally aligned
in their negative boundaries. The problem is evidentiary adequacy for the title,
not hidden overclaiming inside the current prose.

## Experiment audit

### Required before submission candidacy

1. Repair and independently adversarial-test the executor's raw BLOB/cell and
   total-result boundary; no historical-v3 rerun is needed.
2. Run the untouched, call-matched four-condition end-to-end study specified in
   Issue 1 if an empirical five-role claim is to be retained.
3. Complete qualified two-reviewer-plus-adjudicator semantic validation on an
   authentic, structurally distinct power-grid resource, including retained
   disagreements, exclusions, reference-SQL re-execution, and rights/ethics
   decisions.
4. Independently recompute complete counts, uncertainty, failures,
   coverage/abstention, calls/tokens, and eligible latency for any new study.

### Desirable but not independently blocking

- Develop a deterministic permutation-invariant tie rule on development-only
  data, then test it once on untouched items and report risk--coverage.
- Add authenticated-domain metamorphic families for units, code values,
  temporal boundaries, topology, missingness, and aggregation granularity.
- Evaluate multiple structurally distinct grid databases and schema families.
- Add process isolation if deployment or resource containment is discussed.

### Unjustified reruns or relabeling

- Any rerun of the same 180 v3 items to restore prospectivity or outcome
  blindness.
- Choosing the favorable 117--118 reverse-order result after outcome access.
- Tuning weights, thresholds, or candidate order on the exposed 180 items and
  reporting the result as confirmatory.
- Calling LLM/API judges qualified human experts or treating machine silver as
  human gold.
- Dropping failed calls, incidents, ambiguous items, harms, or abstentions from
  denominators.
- Applying the R3 executor controls retroactively to release-v3 results.

## Figure and table audit

### Verified strengths

- The exact PDF SHA-256 is
  `1D1284C35F691717457A592FF24F48D68C29386B7C6D2ED9E7BCF0D4710BE1C6`;
  it is 20 A4 pages and 546,758 bytes.
- All 20 page-image hashes match the visual manifest; direct inspection found
  no clipping, overlap, missing glyphs, or unresolved references.
- Figures 2--4 visually match the bounded descriptive/component/multi-state
  narratives; point estimates are not disguised as population intervals.
- Q039 and order sensitivity are visible rather than hidden.

### Required corrections

1. Add complete round-bound lineage for all four figures.
2. Replace every R2 label/filename/caption in Figure 1 with a version-neutral or
   R3-accurate identity.
3. Correct Table 7's “Failures” header and provide a true failure taxonomy if
   claimed.
4. Improve the normal-scale readability of Tables 1 and 2.
5. Re-render and re-inspect all pages after these changes; old R2 visual assets
   must remain excluded from the final allowlist.

## Reproducibility, ethics, and declarations

### Positive findings

- All 57 frozen round records and all 20 page-render records independently
  match their listed byte counts and SHA-256 values.
- The structural verifier passes the exact title, authors, corresponding-author
  boundary, grant number, declarations, and prohibited-value checks.
- The supersession record preserves rather than rewrites the failed v3
  evidence-class history; v1/v2 and BIRD incidents remain retained and excluded.
- Complete numerical tables and the item-level tie ledger expose adverse and
  null results.
- Machine-silver assets are not relabeled as qualified-human gold, and the paper
  rejects operational-control or deployment-safety interpretation.

### Open integrity and ethics gates

- The BLOB bypass makes one engineering control claim false until repaired.
- The end-to-end five-role and qualified domain-semantic evidence gaps remain.
- No matching clean-extraction archive or immutable public release exists.
- Yang Yong's email, funding agency/sponsor role, all-author approval,
  file-level permissions, and repository release require human confirmation.
- GenAI use in code/reproducibility/data stages is not fully described in
  Materials and Methods or by exact product/version in Acknowledgments.
- Current “IRB not applicable” is supportable only for the presently reported
  automated study. Any new professional annotation requires an institutional
  ethics/consent determination.

## Final acceptance checklist

| Priority | Required closure | Acceptance evidence |
|---|---|---|
| P0 | Fix raw BLOB/cell/result boundary and provenance wording | New adversarial tests, corrected code/report/TeX, fresh independent reproduction, regenerated hashes |
| P0 | Close or explicitly editorially bound the title-evidence gap | Untouched matched integrated study plus qualified semantic review; otherwise cover letter and final audit flag architecture-only identity as an unresolved editorial risk |
| P0 | Produce current release package and repository identity | Allowlist archive, clean-extraction compile/tests, restricted-file scan, exact final hashes, synchronized immutable tag/DOI |
| P1 | Complete all four figure lineages and repair R2/Table 7 labels | Lineage manifest, current figures, readable tables, fresh 20-page-or-final visual QA |
| P1 | Complete AI and author/funding/rights declarations | Methods AI inventory; exact logged product/version; correspondence, funder role, metadata, rights and author sign-off |
| P1 | Recheck current Applied Sciences instructions | Dated official-site record; confirmed abstract/declaration/template compliance |
| Final gate | Run a clean independent final audit | Zero unresolved blocking scientific, integrity, build, package, or required manual-field defects; all new hashes reproduce |

## Final decision rationale

R3 is a credible review draft and a substantial integrity improvement over R2,
but it does not satisfy the protocol's “three reviewers find no unresolved
blocking defect” gate. The BLOB limit is a newly demonstrated false engineering
claim; the retained title still lacks integrated and expert-grounded applied
evidence; and the final archive, repository identity, figure lineage, AI
disclosure, and mandatory human metadata are incomplete. The appropriate
decision is therefore **Major Revision**, not “ready for final audit”.

## Audit trail

- Frozen PDF: 20 pages, 546,758 bytes, SHA-256
  `1D1284C35F691717457A592FF24F48D68C29386B7C6D2ED9E7BCF0D4710BE1C6`.
- Frozen TeX: 65,916 bytes, SHA-256
  `6B25DA628DA44F4A66852C1A0C366CB3E8F52951C06521C8F3B5DCD691C422B3`.
- Round audit: independently recomputed 57/57 file hashes/byte counts.
- Visual manifest: independently recomputed 20/20 page hashes; selected figure,
  table, Q039, and declaration pages directly inspected.
- R3 executor: fresh `unittest` run 10/10 PASS; independent 10 MB `zeroblob`
  bypass reproduced.
- Tie ledger: 360 rows; 180 per selector; exact tie counts, means,
  distributions, and selected-source counts recomputed.
- Existing delivery ZIP SHA-256: `99E1470CCF28990DB97D4A922700A6B4FAC432C74A3001C06E4D6C9BF910EDE1`;
  reviewer ZIP SHA-256: `C2C1B886DAEA8983B7423D545DF5B4381338701BC548B2B15AAD1F2030299FFF`;
  both contain the alternate-title manuscript.
- Official sources checked 2026-08-08: MDPI Research and Publication Ethics,
  <https://www.mdpi.com/ethics>; Applied Sciences Aims and Scope,
  <https://www.mdpi.com/journal/applsci/about>; Computing and Artificial
  Intelligence section,
  <https://www.mdpi.com/journal/applsci/sections/computing_artificial_intelligence>.
  The Applied Sciences instruction endpoint returned HTTP 429, so unresolved
  journal-specific wording is marked **待核实** rather than guessed.
