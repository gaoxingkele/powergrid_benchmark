# P1 S5 Three-Round Scientific Closure

This record documents three sequential, evidence-bound adversarial passes over
`MANUSCRIPT.md`, `DEEP_REVISION_EVIDENCE.md`, the frozen fair-run configuration,
script, manifest, and CSV outputs. It is an internal closure record, not a human
peer-review report or evidence of external expert validation.

## Pass 1: Logic and Claim Chain

### Major findings resolved

1. **Calendar-year overstatement.** The source files contain 8784 rows, but the
   frozen loader evaluates the first 8760. The manifest delivery keys end on
   December 30. Publication-facing claims were changed from “weather year” or
   “full year” to “fixed 8760-row sequence,” and the truncation is now explicit.
2. **Overbroad novelty language.** Statements that no public benchmark or
   multiple-lag retrieval evaluation exists were stronger than the documented
   literature process. They are now bounded to the cited corpus, with no claim
   of an exhaustive systematic search, SOTA exclusion, or expert validation.

### Counterargument retained

Persistence remains lower-MAE at the primary cap at both lags. The paired GRU
result is a component comparison and does not establish overall forecasting
superiority. No wording change converts this negative comparison into a
positive system claim.

## Pass 2: Methodology and Statistics

### Major findings resolved

1. **Temporal-gate wording.** The executable code offsets downstream target
   indices so that the query endpoint has reached the phase boundary. It does
   not require every row of the 48-row historical window to be downstream of
   that boundary. The manuscript, evidence matrix, and table manifest now state
   the executed rule.
2. **Selection order.** The GRU-head checkpoint is selected first, and the
   head-weight grid is evaluated second on the same selection phase. Matched
   retrieval controls share that head-selected checkpoint. The paper no longer
   implies joint checkpoint/weight optimization.
3. **Inferential boundary.** The two-sided exact sign-flip calculation enumerates
   all sign assignments of ten paired seed differences. Its interpretation
   assumes sign-exchangeability under the no-effect null; seeds are common
   algorithmic initializations, not randomized experimental assignments. No
   interval over seeds, hours, event blocks, years, or systems is available.
4. **Feature transparency.** The engineered branch-informed stress feature is
   now defined from the executable formula and explicitly separated from
   power-flow, contingency, or feasibility analysis.

### Numerical findings retained

- Selected-minus-head MAE differences remain -0.0049606891 at 1 h and
  -0.0022005539 at 24 h, with ten favorable pairs in each lag.
- The unadjusted exact sign-flip value remains 0.001953125 and the within-lag
  Holm value remains 0.01171875 for each of the three MAE contrasts.
- Selected onset GRU-LSR remains identical to the head in all ten pairs at each
  lag; this remains inapplicability evidence because selection and calibration
  contain zero positive onsets.
- Fixed 0.5 onset F1 remains positive at 1 h and non-significant at 24 h under
  the declared fallback qualification.

## Pass 3: Theory and Innovation

### Major finding resolved

The v2 controls identify the implemented retrieval prediction path relative to
its matched GRU head and compare learned $k=8$ retrieval with raw-feature and
randomized-encoder retrieval. Learned-space attribution is favorable at 1 h but
not licensed at 24 h, where raw retrieval is better and the randomized contrast
is unresolved. Alternative distances remain unevaluated, and $k=4/16/32$
remains descriptive. The contribution is an auditable retrospective benchmark
and matched use case, not a new GRU architecture, representation-learning
theory, SOTA method, or general system result.

## External Checks and Verification Status

- The current official IEEE Access submission guidance was checked for the
  required Access template, matching source/PDF content, AI-generated-text
  disclosure, submitting-author ORCID, and all-author biographies:
  <https://ieeeaccess.ieee.org/authors/submission-guidelines/>.
- Metadata/content spot checks were completed for the central SNSP, RTS-GMLC,
  analogue-ensemble, day-ahead SNSP, and curtailment-model comparators
  (references [4], [5], [6], [9], and [13]).
- **UNVERIFIED:** a content-level audit of every cited source.
- **UNVERIFIED:** systematic or exhaustive novelty searching.
- **UNVERIFIED:** external domain-expert review.
- **UNVERIFIED:** similarity/plagiarism screening, including self-overlap.
- **UNVERIFIED:** whether the locally bundled IEEE Access class files are the
  latest publisher download; the submitting authors must compare the final
  source with the current official template package.
- **UNVERIFIED:** exact RTS-GMLC release/tag beyond the frozen file hashes.
- The Stage-5 build record and manuscript-phase validator, rather than this
  historical closure note, are authoritative for the current TeX/PDF identity,
  page count, and visual-inspection status.

No unavailable check is treated as passed, and no external reviewer or expert
label is attributed to this closure.

## Remaining Scientific Limitations

- Delivery issue times, as-of mappings, and source vintages are absent.
- The label is an SNSP-type proxy, not observed curtailment or operator action.
- Selection and calibration contain zero positive onsets at all executed caps
  and lags.
- Only one system and one truncated 8760-row sequence are evaluated.
- The v2 run contains four direct-head architectures and learned/raw/randomized
  retrieval controls, but it does not reproduce the full historical roster or
  evaluate alternative retrieval distances.
- No OPF/UC feasibility, probabilistic, economic, operator, user, deployment,
  or cross-hardware/external-investigator validation is available.

## Unresolved Human Blockers

- **AUTHOR INPUT REQUIRED:** final author list, public ORCIDs, complete
  affiliations, and corresponding-author name/e-mail.
- **AUTHOR INPUT REQUIRED:** funding/grant statement or explicit no-funding
  statement.
- **AUTHOR INPUT REQUIRED:** CRediT contributions, conflicts of interest,
  acknowledgments, and venue-compliant generative-AI disclosure.
- **AUTHOR INPUT REQUIRED:** IEEE Access biography and photograph for every
  author.
- **AUTHOR INPUT REQUIRED:** public repository URL or archival DOI before any
  public-release claim.
- **AUTHOR INPUT REQUIRED:** disclosure of any shared code, text, figures, data
  preparation, or evidence with another manuscript.
