# Round 3 Independent Review — Methods and Statistics

## Reviewer scope and independence

I reviewed the frozen R3 TeX and 20-page PDF, `ROUND_AUDIT.json`,
`STRUCTURAL_VERIFICATION.json`, `R3_ASSEMBLY_AUDIT.md`, the R2-to-R3 response
matrix, the supersession record, the complete R3 evidence tables and item-level
tie ledger, the frozen release-v3 audit trail, the 700-call component release,
the frozen and additive SQLite executors, and both test suites. I did not edit
the manuscript, code, results, or prior reviews and did not consult the other
Round-3 reviewers.

## Recommendation

**Major revision; not ready for final audit or submission.**

R3 closes several important R2 reporting and provenance defects. The v3 study
is consistently classified as deterministic no-generation descriptive
re-execution; the complete 8-cell, 12-endpoint, 8-cell, and 18-cell numerical
tables are present; the 130/180 tie counts and Q039 ambiguity are disclosed in
the abstract, results, discussion, and conclusion; and the transient 33/33
result is excluded while 30/30 frozen tests, 10/10 additive tests, and 21/21
manifest checks are correctly distinguished. My independent recomputation from
`top_tie_item_level.csv` reproduces 130/180 top ties for each adjudicating
selector, means 5.400000 and 5.388889, the printed multiplicity distributions,
and 178/180 original-order selections from Qwen slots. All 57 files listed in
`ROUND_AUDIT.json` exist and match their bound byte counts and SHA-256 values.

The central scientific blocker is not closed: no untouched, budget-matched
experiment evaluates the five-role system end to end, and no authentic
power-grid question--SQL set has qualified independent semantic adjudication.
In addition, R3 introduces a new repairable integrity defect. The additive
executor's `max_cell_bytes` check measures the serialized *exposed
representation* of a BLOB after replacing it by a hash and length, not the raw
cell size. A 10,000,000-byte `zeroblob` executes successfully with
`max_cell_bytes=1024` and `max_result_bytes=4096`. Thus the manuscript's
unqualified “maximum scalar-cell bytes” claim and the test report overstate the
implemented resource boundary. This does not invalidate historical v3 counts,
because R3 correctly says the additive executor was not used for them, but it
blocks acceptance of the new engineering claim until corrected.

**Confidence: 5/5.** The verdict is based on frozen source, machine ledgers,
independent arithmetic, direct test execution, and an adversarial executor
reproduction.

## R2 blocker disposition

| R2 blocker | R3 methods verdict | Blocker class |
|---|---|---|
| Five-role method not evaluated end to end | **Open.** R3 discloses rather than closes it. | Scientific |
| 130/180 ties and arbitrary candidate order incompletely reported | **Closed for disclosure and numeric completeness; open for selector efficacy.** | Scientific if efficacy is claimed |
| Conflicting v3 prospective fields | **Closed.** The supersession record controls interpretation throughout the manuscript. | Integrity closed |
| Incomplete numerical tables | **Closed.** Counts and denominators match the bound evidence supplement. | Integrity closed |
| GridDB semantic validity and broader robustness | **Open.** GridDB remains synthetic/development-visible and authentic grid assets have zero qualified reviews. | Scientific plus human execution |
| Missing result/cell/width/function controls | **Partly closed.** Width, total serialized result, text-cell, and function-policy paths are tested, but raw BLOB cell size escapes the registered cell budget. | Scientific integrity, repairable |
| Q039 overinterpretation | **Closed.** It is consistently described as an ambiguous, outcome-exposed projection trace. | Integrity closed |
| Test-count confusion (21 vs. 30 vs. 10 vs. invalid 33) | **Closed.** Counts and dependencies are correctly separated. | Integrity closed |
| Final package, repository, rights, author metadata | **Open.** These are not statistical defects but remain portal/release blockers. | Manual/release |

## Five most serious issues

### 1. No experiment estimates the end-to-end five-role effect

**Severity:** Blocking major scientific defect  
**Evidence anchor:** `paper_applsci.tex:36–42, 62–64, 228–236, 477–493, 507–521`  
**Confidence:** 5/5 — direct manuscript statements and frozen study topology

The architecture is implemented, but the inherited GridDB and BIRD studies are
prompting workflows, the 700-call release tests two components, and release v3
selects among eight historical candidates without generation. None compares
the named five-role system with a call-matched direct or staged baseline on
untouched items. The 80/180, 100/180, and 101/180 values therefore cannot
estimate an agent, handoff, communication, coordination, or generation effect.
Disclosure prevents misreporting but does not supply the missing evidence.

**Required revision:** Freeze and execute an end-to-end comparison on a
genuinely untouched resource: direct generation; staged question/schema
handoff with one candidate; matched multi-candidate validation/adjudication
without witness evidence; and the same candidate pool with pre-registered
reference-free witnesses. Hold model snapshot, decoding, question order,
candidate count, physical calls, evaluator, failure policy, and abstention rule
constant.

**Acceptance test:** the protocol, development-only tests, hashes, and analysis
family predate outcome access; all calls and failures are retained; the
integrated condition is actually executed; an independent recomputation
reproduces counts, effects, uncertainty, costs, and abstentions. No result from
the existing 180 outcome-exposed items can close this item.

### 2. Applied power-grid semantic validity remains unmeasured

**Severity:** Blocking major scientific defect  
**Evidence anchor:** `paper_applsci.tex:86–95, Table 1, 503–513`  
**Confidence:** 5/5 — denominators and review status are explicit

The primary grid result uses one 98-row synthetic database whose 180-item
evaluation split was development-visible. RTS-GMLC, SimBench, and NERC pairs
have zero completed qualified-human semantic reviews and zero sealed items.
BIRD is non-grid. Execution-result equality cannot adjudicate units, status
codes, temporal boundaries, topology, tie handling, or intended aggregation.
Consequently, the paper demonstrates a grid-oriented architecture and local
database mechanisms, not validated power-grid text-to-SQL correctness.

**Required revision:** complete a frozen two-independent-reviewer plus
adjudicator protocol on an authentic, structurally distinct grid resource.
Retain qualifications, independent labels, disagreements, adjudications,
exclusions, re-executed reference SQL, and license/ethics determinations. LLM
review may assist triage but cannot be relabeled as qualified expert gold.

**Acceptance test:** every promoted item has traceable human decisions and an
executable adjudicated reference; denominators include disagreements and
failures; a custodian verifies evaluation-item outcome isolation; uncertainty
is reported at an appropriate database/question-cluster level.

### 3. The new cell-byte resource claim is false for BLOB values

**Severity:** Blocking major integrity defect, repairable without rerunning v3  
**Evidence anchor:** `code/sqlite_readonly_executor_r3.py:38–48, 56–65, 218–246`; `paper_applsci.tex:153, 497, 507, 517`; `EXECUTOR_R3_TEST_REPORT.md`  
**Confidence:** 5/5 — direct code inspection and adversarial reproduction

`_json_value(bytes)` replaces raw bytes by `{bytes_sha256, length}` before
`_encoded_value_size` is evaluated. The registered limit therefore measures a
small surrogate rather than the raw BLOB. I reproduced:

```text
SQLiteReadOnlyExecutor(..., max_cell_bytes=1024,
                       max_result_bytes=4096)("SELECT zeroblob(10000000)")
=> executable=True, row_count=1, returned length=10000000
```

The 10/10 tests exercise a long text scalar but no BLOB. The code remains
fail-closed for the tested paths, and the paper correctly disclaims process
memory isolation; nevertheless, “maximum scalar-cell bytes” is not an accurate
description of the implementation.

**Required revision:** either enforce the raw size of `bytes`/BLOB values before
hash substitution or rename the control everywhere to an encoded-output
representation budget and explicitly exclude raw BLOB/process-memory bounds.
The safer option is to implement both raw-cell and canonical-output budgets.

**Acceptance test:** adversarial tests cover large TEXT, BLOB/`zeroblob`, wide
projection, many rows, aggregate output, and explicit function denial. A raw
10 MB BLOB must fail a 1 KB raw-cell limit, no partial rows may be returned, and
the trace must identify the exact limit. Update the source docstring, test
report, figure/caption, Methods, Discussion, and Conclusion consistently.

### 4. Selector behavior is dominated by uninformative ties and source order

**Severity:** Major for any selector-efficacy or robustness interpretation;
otherwise a disclosed design limitation  
**Evidence anchor:** `paper_applsci.tex:406–471, 489–493, 521`; Tables 10 and 12;
`top_tie_item_level.csv`  
**Confidence:** 5/5 — independent item-level recomputation

Both adjudicating selectors tie on 130/180 questions, with about 5.4 candidates
at the maximum. All eight candidates tie on 79 and 78 questions. Original-order
selection chooses Qwen slots on 178/180 items; reversing order changes the full
condition from 101/180 to 117–118/180. The complete-witness mechanism changes
only Q039. R3 now reports this correctly, so there is no selective-reporting
defect, but the evidence does not identify a useful adjudication rule or a
counterfactual accuracy benefit.

**Required revision:** do not optimize weights, thresholds, or order on these
180 items. Develop a deterministic, permutation-invariant tie rule using
development-only evidence, freeze it, and test it once on the new untouched
resource required by Issue 1. Report risk–coverage and abstention behavior, not
only forced-choice accuracy.

**Acceptance test:** candidate permutations leave the selected SQL unchanged
unless the rule explicitly uses a registered semantic feature; tie prevalence,
source distribution, coverage, accuracy, and uncertainty are reported on the
untouched set. A post-hoc choice of the favorable reverse-order result is
prohibited.

### 5. R3 release provenance still contains contradictory or confusing labels

**Severity:** Major release-integrity defect; not a reason to rerun historical experiments  
**Evidence anchor:** `code/sqlite_readonly_executor_r3.py:1–7`; Figure 1 title and
caption; Table 7; `R3_EVIDENCE_README.md`; `R3_ASSEMBLY_AUDIT.md`  
**Confidence:** 5/5 — direct source/PDF/package inspection

The additive R3 executor docstring says it is “the actual database boundary used
by the Round-2 offline study,” while the manuscript and audit correctly say the
R3 limits were not used in release v3. Figure 1 is still labeled “R2” inside an
R3 paper. Table 7 labels its last column “Failures” but populates it only with
“0 final omissions,” which can be misread as zero parse/execution failures. The
controlling independent v3 audit is referenced outside the R3 round tree rather
than included in the bound evidence directory, and the final clean-extraction
archive has not yet been built.

**Required revision:** correct the R3 executor provenance sentence; relabel the
architecture figure to a version-neutral or R3-accurate identity; rename Table
7's column to “Final-ledger omissions” and, if available, give a separate
failure taxonomy; include the controlling audit and component audit in the
final allowlisted reviewer package; then regenerate all hashes.

**Acceptance test:** a clean extraction contains one title and one current PDF,
every cited audit resolves inside the package, source and manuscript make the
same retroactivity claim, no R2/v3/R3 label is ambiguous, and all package hashes
reverify.

## Claim–evidence audit

| Claim | Location | Evidence verdict | Required boundary/action |
|---|---|---|---|
| Five typed roles and deterministic blackboard/adjudicator are implemented | Abstract; Sections 1, 3.3–3.4; Fig. 1; Alg. 1 | **Supported as software architecture.** | Do not infer autonomous-agent or accuracy benefit. |
| Frozen executor provides tested SQLite mutation denial and bounded execution | Sections 3.3, 5.4, 7; frozen code/tests | **Supported for tested SQLite cases; 30/30 independently rerun.** | Retain exclusions for authentication, process isolation, and deployment. |
| R3 adds cell/result/width/function controls | Section 3.3; test report; additive code | **Partly contradicted.** Raw BLOB size bypasses `max_cell_bytes`; 10/10 otherwise reproduce. | Fix/rename and add BLOB tests before acceptance. |
| 700-call component release is prospective and audited | Abstract; Sections 3.6, 4.3, 5.1 | **Boundedly supported by its separate release and audit.** | It is component evidence, not five-role evidence; timing proof is ledger-level, not notarial. |
| v3 yields 80/180, 100/180, 101/180 | Abstract; Table 9; Conclusion | **Numerically supported only as descriptive historical-pool behavior.** | Supersession notice must precede historical fields. |
| Both adjudicators tie on 130/180; means 5.4000/5.3889; reverse order gives 117–118 | Abstract; Tables 10, 12; Discussion | **Supported. Independently recomputed exactly.** | No post-hoc preferred-order claim. |
| Q039 is the sole full-vs-no-CF difference | Table 11; Sections 4.7, 5.3 | **Supported as an outcome-exposed constructed projection trace.** | Not semantic rescue, counterfactual gain, or grid correctness. |
| Complete numerical tables and test counts are reported | Results; R3 evidence supplement | **Supported.** 8 GridDB cells, 12 component endpoints, 8 state cells, 18 sensitivity cells; 30/30, 10/10, and 21/21 correctly separated. | Rename Table 7 failure column and retain invalid 33/33 exclusion. |
| “Robust” describes tested mechanisms | Introduction and Conclusion | **Only partly supported until Issue 3 is repaired; never universal.** | Keep the operational vector and explicit non-established column. |
| Framework is valid for power-grid databases | Title/featured application | **Architecture/domain motivation supported; semantic effectiveness not established.** | Requires Issue 2 evidence for an applied-validity claim. |

No standard bounded arithmetic recomputation from a reported *t*, *F*,
$\chi^2$, or degrees-of-freedom identity was available. The reported inferential
values are randomized/cluster-bootstrap outputs. I instead checked printed
counts, rates, effects, intervals, adjusted values, tie distributions, and test
counts against their canonical retained JSON/CSV sources; no manuscript numeric
mismatch was found.

## Experiment audit

### Required before submission candidacy

1. The untouched, call-matched four-condition end-to-end study in Issue 1.
2. Qualified independent semantic adjudication on an authentic power-grid set,
   with licensing and ethics/consent determination.
3. Repair and adversarial re-test of the R3 executor's raw-cell resource limit.
4. Independent recomputation of the new study's complete ledgers, including
   accuracy, abstention, valid SQL, failure taxonomy, token/call budget,
   latency under an eligible environment, and clustered uncertainty.

### Desirable but not blocking by itself

- Evaluate multiple structurally distinct grid databases and schema families.
- Report risk–coverage curves and a permutation-invariant tie analysis.
- Add metamorphic families for value drift, temporal boundaries, code mappings,
  topology, missingness, and aggregation granularity after expert validation.
- Perform process-isolated resource testing if deployment safety is discussed.

### Unjustified reruns or analyses

- Any weight, threshold, order, or candidate-choice tuning on the exposed 180
  GridDB items.
- Promoting 117–118/180 because it is numerically favorable.
- Re-running v3 on the same candidates and calling it prospective or
  confirmatory.
- Repeating the 5000-call BIRD run merely to strengthen a power-grid claim;
  BIRD remains non-grid.
- Treating LLM/API labels as independent qualified-expert adjudication.
- Adding 30 and 10 as “40 independent tests” or reviving the invalid 33/33 run.

## Figure and table audit

- The PDF is visually usable and has no clipping or overfull boxes. Figure 2
  explicitly says point estimates only, and Figure 3 clearly separates the
  registered component effects.
- Figure 1 is informative but its internal text is small at normal print scale
  and its title/caption say R2 in the R3 paper. Relabel and enlarge or split the
  architecture/control details.
- Tables 4–6, 9, and 12 match the bound numerical evidence.
- Table 10 is complete but dense; selected-source counts wrap awkwardly. A
  compact main-paper summary plus the existing item-level supplement would be
  clearer.
- Table 11 responsibly exposes Q039, but the selected SQL cells are difficult to
  read. Use a smaller two-row code listing or move full SQL to a supplement.
- Table 7's “Failures” heading is methodologically ambiguous because the cells
  report only final-ledger omissions. Rename it and report any retained
  parse/execution failure counts separately.

## Reproducibility and ethics findings

### Verified strengths

- PDF SHA-256: `1D1284C35F691717457A592FF24F48D68C29386B7C6D2ED9E7BCF0D4710BE1C6`.
- TeX SHA-256: `6B25DA628DA44F4A66852C1A0C366CB3E8F52951C06521C8F3B5DCD691C422B3`.
- R3 evidence JSON SHA-256:
  `16E9156D097835FDFE4381E24C301CB71D563B19901212B545609D871C1F5D5C`.
- All 57 `ROUND_AUDIT.json` entries independently rehashed with zero mismatch.
- Frozen tests independently rerun: 30/30 PASS. Additive R3 tests independently
  rerun: 10/10 PASS. The BLOB escape is an uncovered case, not a contradiction
  of those ten recorded outcomes.
- The supersession notice correctly prevents the v3 mechanical freeze from
  being mistaken for prospective scientific evidence.
- Failed runs and negative results are retained rather than silently removed.

### Open manual/release blockers, distinct from scientific defects

- Yang Yong's correspondence email remains a manual placeholder.
- Funding-agency name and funder-role wording for 521300250006 need author
  confirmation.
- Author names/order/affiliations, contributions, conflicts, and AI disclosure
  require final all-author approval.
- Qualified reviewer identities/records and the professional-annotation
  ethics/consent determination require human/institutional action.
- File-level third-party rights and reviewer-access permissions require rights
  holder/editor decisions.
- The public repository must be synchronized, clean-clone verified, and tagged;
  the final allowlisted archive must be clean-extraction verified.

These manual items block portal upload but do not substitute for the scientific
experiments in Issues 1–3.

## Final acceptance decision and title judgment

**Round-3 methods/statistics gate: FAIL.** There are unresolved scientific and
integrity blockers, so this reviewer cannot recommend “ready for final audit.”

The exact original title may remain during revision because R3 consistently
defines it as a framework identity and avoids a superiority claim. The title is
not, by itself, the primary defect. It becomes defensible for submission only
after (i) the integrated untouched study, (ii) qualified authentic-grid
semantic validation, and (iii) the R3 executor resource claim are closed. If
the authors decline those scientific additions, the manuscript can remain an
honest architecture/safety study, but retaining “Robust Multi-Agent … in Power
Grid Databases” will continue to carry a substantial desk-rejection risk and
cannot be converted into evidence by additional caveats alone.
