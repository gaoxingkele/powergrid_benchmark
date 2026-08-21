# C2GES Round-3 Independent Review: Power-Grid Application and Engineering Safety

## Review identity and frozen object

I reviewed the frozen R3 object independently as a power-system application and
engineering-safety reviewer. I did not edit the manuscript, figures, code, data,
or evidence package. The reviewed object was:

- PDF: `build/paper_applsci.pdf`, 14 pages, SHA-256
  `3CB2613E9EFA530602DAFB4A165E771E3F7C231AC7C92E8624B209A80F19EBC3`;
- TeX: `paper_applsci.tex`, SHA-256
  `5C56F9751515F03E5FEBA7C4DFF380CF57280121B5592CD306046322929A03D6`;
- round audit: `ROUND_AUDIT.json`, SHA-256
  `ECD73CCE14CADF53A2E894DA8F32847F3F760DFED9E3E6EC450438D147774CE6`;
- rights-safe 40-report CSV: SHA-256
  `709F4FBE567A3E9EAE92785D8296C20A44AD9E05D77115C957C4CA7BCADCC47D`;
- rights-safe evidence index: SHA-256
  `C2AB15020D18B6E41792067489ABF32DFF583ED090EFEEC1BE051D8DD5F26447`.

I also inspected the R2-to-R3 response matrix, structural/citation/visual audits,
four rendered figures, transferable supplement, restricted-local prediction
ledger, frozen runner, and complete local test-candidate file. The PDF and TeX
agree at the material claim locations.

## Recommendation

**Major Revision.** R3 is substantially more candid and technically coherent
than R2. It places the NERC-proxy limitation in the first abstract sentence,
accounts for all 40 PDFs and all 13 exclusions, identifies roles and transitions
as textual proxies, exposes the adverse counterfactual ablation, prohibits
operational use, and states correctly that AI review is not qualified human
validation. Figure 2 has also been repaired successfully.

It is not ready for final audit, however. The principal comparisons use equal
sentence counts but markedly unequal word budgets, with many selected units
being long table-bearing extraction blocks rather than ordinary sentences. In
addition, the immutable output ledger does not actually carry the page locator
that the paper says each selected output preserves. Both issues directly affect
the claimed source-navigation application. The exact maintenance title, domain
semantics, and unsafe-omission value also remain deliberately unvalidated and
therefore remain human/new-corpus gates rather than defects an AI review can
close.

## Five most serious issues, ordered by decision impact

### 1. Equal sentence count is not an equal engineering or lexical budget

**Severity: Major.** The registered comparison is valid as a comparison at
exactly five or ten extracted units, but the units have very unequal lengths.
An independent read-only recomputation from the immutable 210-row ledger found
the following mean output word counts:

| Budget | Full C2GES | Semantic-MMR | TextRank | strict no-CF |
|---:|---:|---:|---:|---:|
| K=5 | 287.7 | 184.7 | 177.0 | 329.0 |
| K=10 | 568.9 | 354.5 | 369.0 | 596.9 |

Thus Full is on average 103.0 and 214.5 words longer than Semantic-MMR at K=5
and K=10, and 110.7 and 199.9 words longer than TextRank. Across the 225 Full
selected-sentence instances, 37 exceed 100 words, one reaches 270 words, and 40
contain a `Table` marker. These are not merely stylistic differences: longer
extracts have more opportunity to overlap a long Executive Summary, while the
operator review burden and omission risk are not comparable. The paper reports
redundancy but no output-length distribution and presents the ROUGE contrasts
without this budget qualification.

**Evidence anchors:** `paper_applsci.tex:57,190,228,286,310`; restricted-local
`predictions.jsonl` (immutable SHA-256
`AAE2BFE0E6C426B6A69D727F24239A07DFD7DBEE8A4CE228E86625CCDCA2338F`).

**Required revision:** do not rerun or tune the revealed test. Add a
non-verbatim, mechanically derived output-length audit for every condition and
budget: report-level words/characters, selected-unit length, table-bearing-unit
counts, and distributions. State in the Abstract, Results, and Conclusion that
the observed advantages over Semantic-MMR and TextRank occur under equal
sentence-count but unequal word-length budgets and cannot establish a
length-controlled advantage. Audit the sentence splitter against fused table,
footnote, heading, and line-break blocks. A length-controlled comparison may be
descriptive on existing outputs, but any newly selected token-budget system
comparison must use a newly frozen, unseen holdout.

**Acceptance test:** an independent script reproduces the length table from the
frozen ledger; all headline comparisons carry the unequal-length qualification;
no current test result is relabeled length controlled; and any future
token-budget claim comes only from a new sealed protocol.

### 2. The frozen output does not preserve the claimed page locator

**Severity: Major.** Section 3.5 says that each selected item preserves report
ID, page, sentence ID, and source order. The frozen runner writes report ID,
selected sentence IDs, selected text, metrics, and selection audit, but not
page. All 210 prediction rows lack a page field, and sentence IDs such as
`s00001` do not encode page. The internal graph node also contains only ID,
text, position, role scores, and dominant role. I verified that all 1,575
selected-ID references can be mapped to pages only by joining the prediction
ledger with the separate frozen candidate file. That join is possible locally,
but it is neither present in the output nor available in the transferable
supplement.

**Evidence anchors:** `paper_applsci.tex:131`; `run_test_v0_3_1.py:463-480`;
`c2ges_offline.py:107-113,201-207`; restricted-local `predictions.jsonl` schema;
frozen `nerc_full_pdf_test_v0_3.jsonl` candidate schema.

**Required revision:** without rerunning selection, deterministically join each
selected `(report_id, sentence_id)` to its frozen page and source URL. Emit a
hash-bound, non-verbatim locator ledger containing condition, K, report ID,
sentence ID, page, source order, and URL, subject to a human rights decision.
Alternatively, reduce the manuscript claim to say that page lookup is possible
only when the protected candidate table is available. Do not describe the
current prediction JSONL itself as page linked.

**Acceptance test:** every one of the 1,575 selected references resolves to
exactly one integer page within the declared PDF page range; zero unresolved or
duplicate mappings; a clean verifier checks the ledger; the manuscript,
supplement statement, and actual output schema use the same wording.

### 3. The exact maintenance title remains an intended use, not an evaluated domain

**Severity: Major for title-concordant validation; not a hidden integrity
defect.** R3 now states this boundary unusually clearly in the Abstract,
Featured Application, Introduction, Discussion, and Conclusion. The evidence
population is nevertheless 27 selected public NERC reliability, disturbance,
event-analysis, recommendation, and assessment reports. It contains no utility
work orders, inspection records, defect tickets, or field-maintenance
narratives. The eligibility mechanism also excludes 13 of 40 PDFs because a
generic Executive Summary endpoint was unavailable, so the retained set is a
layout-selected proxy sample rather than a maintenance sampling frame.

**Evidence anchors:** `paper_applsci.tex:19,21,31,65-75,294-300,310`; Figure 1;
rights-safe Table S1 (40 rows: 27 included, 11 missing recognized summary
heading, 2 missing deterministic summary endpoint).

**Required revision:** preserve every current proxy/aspirational disclaimer.
The current NERC results may support only a bounded technical-report study. For
this reviewer to accept the exact title as empirically validated, the authors
must add a newly frozen, license-cleared maintenance-report corpus with a
site/report-family-isolated unseen test set and qualified-user endpoints. If
that cannot be completed, the cover letter must ask the editor explicitly
whether the exact title is acceptable as an intended-use title; no wording
change inside the paper can convert the present corpus into maintenance data.

**Acceptance test:** either (a) a new title-concordant study passes independent
pre/post audits and qualified review, or (b) an explicit editorial scope
decision is recorded and every artifact continues to call maintenance an
untested intended use. No NERC report is renamed a maintenance report.

### 4. Roles, transitions, and node deletion are executable proxies but not validated grid semantics

**Severity: Major for a causal/domain-validity interpretation; appropriately
bounded for a software diagnostic.** Table 1 and the failure-mode subsection
are useful improvements. They disclose tie abstention, lexical matching,
stage-monotone transitions, negation failures, hypothetical statements, and
false edges. However, the table gives representative cue classes rather than a
complete lexicon or qualified examples, and no protection, operations,
maintenance, or event-analysis expert evaluated a role or edge. The 111
development ties demonstrate deterministic abstention behavior, not semantic
accuracy. Likewise, mathematical non-identity from degree and active execution
do not show that node deletion expresses a power-system counterfactual.

**Evidence anchors:** `paper_applsci.tex:47,79-119,135,276,292,300,306`; Table 1;
Figure 2; `R2_TO_R3_RESPONSE_MATRIX.md`, role/transition response row.

**Required revision:** change “executable taxonomy” to “summary of the
executable taxonomy” unless the exact registered lexicon, normalization,
matching, transition matrix, and tests are delivered in synchronized code.
Retain the textual-proxy terminology. Qualified power-grid personnel must
independently label roles, relations, ambiguity, negation, hypothetical status,
and recommendation status before any semantic-validity claim. LLM or author
labels may be reported only as machine/author annotations, never as qualified
expert adjudication.

**Acceptance test:** code and documentation reproduce every cue and transition;
no text attributes physical, operational, or root-cause validity to the graph;
and any future semantic result reports expert qualifications, independent
labels, disagreements, adjudication, and agreement.

### 5. Unsafe omissions and qualified-user value remain unevaluated

**Severity: Major for deployment, safety, or engineering-usefulness claims;
properly disclosed for the present research prototype.** The paper now warns
that a fluent extract may omit mitigation, qualification, negation, or
uncertainty and prohibits operational decisions without source review. That is
the correct boundary. It does not, however, measure whether K=5/K=10 preserves
equipment identity, units, chronology, observed-versus-suspected cause,
recommendation status, implementation status, or safety-critical qualifiers.
No qualified engineer has evaluated source faithfulness, chain coverage,
usefulness, or unsafe omission. A link to a source page reduces inspection cost
only if the link is actually delivered and the surrounding context is read; it
does not make the extract safe.

**Evidence anchors:** `paper_applsci.tex:21,59,131-135,296-306,310,318`;
absence of qualified-user ratings in the frozen evidence package.

**Required revision:** keep the present prohibition and treat qualified human
evaluation as an open manual gate. Before making any operator-usefulness or
safety claim, freeze a blinded rubric covering source faithfulness, equipment
identity, quantities/units, temporal order, causal-status uncertainty,
recommendation/implementation status, and unsafe omissions. Preserve
independent ratings, disagreement, adjudication, and qualifications. Record an
institutional ethics/consent determination before involving personnel.

**Acceptance test:** either no usefulness/safety claim is made, or a completed
qualified-human protocol with retained provenance supports it. AI-assisted
triage and three AI review agents are never represented as the required expert
study.

## Five questions for the authors

1. Why is a five- or ten-sentence budget operationally comparable when Full
   outputs average 56--60% more words than Semantic-MMR and contain numerous
   table-bearing blocks? What user time or token budget is intended?
2. Which artifact delivered to a reviewer currently maps a selected sentence
   ID to its page without requiring the protected full candidate file, and how
   will that mapping be rights-cleared?
3. What exact maintenance document classes does the retained title intend:
   work orders, inspection narratives, defect reports, outage reports, or
   lessons-learned reports? Which will form the new unseen population?
4. Which qualified power-system roles will validate the lexical role/transition
   taxonomy, and how will suspected causes, negation, recommendations, and
   unimplemented actions be distinguished?
5. Who is authorized to decide source redistribution and reviewer-access terms,
   annotation ethics/consent, AI-use disclosure, and the final operational-use
   warning before submission?

## Claim--evidence audit

| Claim and location | Domain verdict | Required action |
|---|---|---|
| Exact title; Abstract line 19; Introduction line 31 | Maintenance is clearly disclosed as aspirational, but not empirically evaluated | Preserve the boundary; new maintenance corpus and qualified users are required for title-concordant validation |
| “40 complete PDFs,” 27 retained, 13 excluded; lines 65--75; Figure 1 | Supported; independent count gives 40/27/13, 3,200 pages, and 12,924 retained candidates | Preserve; do not call the layout-selected retained population representative |
| Executive Summary never enters candidates; lines 57, 75 | Supported for registered exact/page/substring gates; not proof of semantic cleanliness | Preserve the exact gate wording; add extraction-unit quality/length audit |
| “Each selected item preserves ... page”; line 131 | Contradicted by the frozen prediction schema | Add the deterministic page-locator ledger or narrow the claim |
| Full has higher ROUGE-L than Semantic-MMR/TextRank; lines 190, 228, 286, 310 | Numerically supported under equal sentence counts; not length controlled | Report unequal word budgets beside every comparative interpretation |
| Typed path deletion is distinct from degree; lines 107--119 | Supported as a mathematical/software property | Do not infer domain-causal correctness or usefulness |
| Roles/edges are textual proxies; lines 79--104, 135 | Appropriately bounded; semantic validity absent | Keep proxy wording; complete code delivery and qualified validation before semantic claims |
| Source navigation rather than decision support; lines 131, 310 | Sensible intended workflow, but page delivery and user value are unverified | Repair locator output and retain mandatory source/context inspection |
| Unsafe omissions are unevaluated; lines 21, 131, 300 | Correct and important disclosure | Preserve; qualified-human study required before safety/usefulness claims |
| AI was not treated as expert; line 318 | Correct and ethically necessary | Preserve; complete provider/model/purpose/date provenance manually |

## Experiment audit

### Required before a revised final-audit candidate

1. Derive and independently verify per-condition output word/character and
   extraction-unit length statistics from the immutable ledger; do not rerun
   selection on the revealed 15 reports.
2. Derive a non-verbatim selected-ID-to-page locator ledger from the frozen
   candidate file, verify all 1,575 mappings, and refreeze its hash and rights
   status.
3. Audit candidate segmentation for table blocks, footnotes, fused headings,
   line-break artifacts, and extremely long pseudo-sentences; report the
   incidence without silently deleting or replacing formal outputs.
4. For exact-title effectiveness or safety, freeze a new license-cleared
   maintenance corpus and qualified-human protocol before test access.

### Desirable but not substitutes for the required work

- On a genuinely unseen corpus, compare sentence-count and token/word-budget
  selection, with output length and human review time as explicit endpoints.
- Stratify descriptively by verified document genre only when all cells and
  denominators are shown; do not select a favorable subgroup from the current
  15 reports.
- Evaluate omission risk, source-faithfulness, and role/edge validity with
  qualified power-grid and technical-document reviewers.

### Unjustified reruns or relabeling

- Do not tune the splitter, K, weights, path horizon, or baseline parameters on
  the revealed 15-report test and then call the result confirmatory.
- Do not run C046, C055, or another counterfactual weight on the existing test.
- Do not reinterpret NERC reports as maintenance records or LLM ratings as
  qualified expert labels.
- Do not remove long or adverse output units from the existing ledger; retain
  them and report the diagnostic honestly.

## Figure and table audit

- **Figure 1 passes the R2 repair.** It visibly accounts for all 40 PDFs,
  branches 13 exclusions from the inventory, and then splits the 27 retained
  reports into 12 development and 15 test reports. It no longer portrays
  exclusion as a stage through which retained reports pass.
- **Figure 2 passes the requested algorithm repair.** Q, R, G, C, and P feed
  the weighted-combination node in parallel, the no-CF switch is visible, and
  the caption denies learned-graph, physical-simulation, and causal-identification
  interpretations. No GPT-generated replacement is needed.
- Figures 3 and 4 are legible and their numbers agree with the tables. Figure 4
  usefully shows all report-level directions and sign counts.
- Tables 2--5 are readable, state n=15, and distinguish registered descriptive
  bootstrap summaries from the unregistered sign-flip sensitivity.
- A new compact table or panel is needed for output word lengths and long/table-
  bearing unit counts. It should be code generated from the immutable ledger,
  not manually transcribed.

## Reproducibility, rights, and ethics audit

**Positive findings.** The round binds source/PDF/evidence hashes, retains
earlier incidents, exposes adverse and post-unblinding results, separates the
transferable and restricted-local compartments, and carries a rights-safe
40-row inventory. The manuscript does not promise that the public repository
already reproduces R3. The AI statement correctly denies expert, annotator,
adjudicator, and author status.

**Residual reproducibility defect.** The output-schema/page-link mismatch means
the advertised navigation object is not self-contained. The public repository
is unsynchronized, and the transferable supplement does not contain the core
selector implementation. These must be reconciled before a reproducible release
claim.

**Rights and ethics.** Every source-rights row remains fail closed. Source PDFs,
full extracted data, and the verbatim prediction ledger must not be transmitted
until a responsible human or institution confirms the applicable terms. “May
be requested from the corresponding author” is conditional on that permission,
not permission by itself. The current no-human-participant statement is
internally consistent only because no real expert labels are used; it must be
revisited before a professional annotation study. Corresponding-author email,
funder wording/role, CRediT, conflict confirmation, AI-use provenance, rights,
repository release, and qualified-human/new-maintenance-corpus work remain
manual submission holds.

## Positive findings that should survive revision

1. The first abstract sentence and conclusion make the maintenance aspiration
   and NERC proxy population impossible to miss.
2. The 40/27/13 inventory and Figure 1 close the prior sampling-accounting gap.
3. Executive Summary overlap is consistently separated from quality, safety,
   causal correctness, and operator usefulness.
4. The unfavorable strict no-CF result and 12/12 zero-weight development result
   are preserved rather than optimized away.
5. The role/transition table, linguistic failure taxonomy, and repaired Figure
   2 make the software hypothesis more inspectable.
6. Unsafe omission, operational-use, AI-expertise, and third-party-rights
   boundaries are explicit.

## Final acceptance criteria for this reviewer

I would upgrade R3 to **ready for final audit** only after all of the following
are demonstrated in a new frozen revision:

1. the immutable comparisons are accompanied by independently verified output-
   length and extraction-unit-quality diagnostics, and every headline result
   states the unequal-word-budget limitation;
2. every selected sentence reference has an actual verified page locator in a
   delivered, rights-controlled artifact, or the source-linked claim is narrowed;
3. the current 40/27/13, leakage, adverse CF, proxy-causality, and selected-NERC-
   population disclosures remain unchanged in substance;
4. no current evidence is used to claim maintenance-work-order effectiveness,
   causal-chain validity, operator usefulness, or safety;
5. any such expanded claim is supported by a new sealed, license-cleared
   maintenance corpus and qualified independent human evaluation, not AI review;
6. synchronized code exposes the exact role lexicon, transition rules,
   normalization, splitter, selector, locator generation, and verification
   tests from a clean clone;
7. file-level rights and reviewer-access decisions, ethics/consent disposition,
   author/funder/COI/email fields, and AI provenance are completed by responsible
   humans; and
8. a final source/PDF/supplement/figure/table/hash audit closes each item without
   modifying the reviewed R3 record.

