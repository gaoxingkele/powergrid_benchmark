# Round 1 Methodology and Statistics Review: MA-SQLGrid

## Recommendation

**Major Revision**. Confidence: **5/5**. Statistical-reporting status: **Needs Improvement in the manuscript, despite strong retained artifacts**.

The architecture, evidence chronology, adverse-result reporting, and gold-boundary disclosures are strong. The main weakness is that six heterogeneous protocols are narrated in one evidence stream while no completed experiment estimates the benefit of the five-role framework named in the title. Several key intervals and paired denominators exist in retained files but are omitted from the manuscript, preventing readers from independently interpreting precision.

## Strengths

1. **Evidence classes and chronology are unusually explicit.** Sections 3.1--3.3 and Table `tab:chronology` distinguish Inherited, Recomputed, New, and Diagnostic evidence and disclose prior same-item outcome access.
2. **Gold isolation is technically specified rather than asserted.** Section 3.1 defines admissible, executable, and evaluator-correct as separate states; Algorithm `alg:coordination` loads gold only after board sealing.
3. **Negative results and multiplicity are retained.** Section 4.2 reports that zero of nine primary execution tests survives Holm correction; Sections 4.3--4.4 preserve null component and multi-state results; Section 4.5 preserves backbone-dependent BIRD outcomes.
4. **Offline-order fragility is quantified.** Tables `tab:ties` and `tab:sensitivity` expose 130/180 top-score ties, mean tie size about 5.4, and 16--17 additional reference matches after order reversal.
5. **Software safety claims are bounded.** Table `tab:robustness` and Sections 3.3/5.4 separate SQLite mutation denial/resource bounds from authentication, row-level authorization, process isolation, semantic correctness, and deployment approval.

## Major findings

### M1. No reported experiment estimates five-role or multi-agent benefit

- **Severity:** Major
- **Evidence anchors:** Introduction, paragraphs beginning “The inherited GridDB factorial study…” and “This distinction leads to three questions”; Sections 3.7--3.8; Sections 5.1 and 6.
- **Evidence:** Candidate SQL is externally supplied; the Synthesizer packages strings; the GridDB and BIRD studies are prompting workflows; release v3 reuses an eight-slot historical pool with no generation; no matched single-agent versus five-role experiment is reported.
- **Why it matters:** The framework can be evaluated as software architecture, but algorithmic effectiveness or novelty from agent decomposition is not empirically identified.
- **Actionable fix without new experiments:** Make RQ1 explicitly a **software conformance question**, not a benefit question. Move “five-role superiority untested” into the first contribution paragraph and the first Results paragraph. Label release v3 “fixed-pool controller diagnostic,” not evidence of multi-agent efficacy.

### M2. The six protocols need one estimand/visibility map

- **Severity:** Major
- **Evidence anchors:** Sections 3.2, 3.6--3.8; Tables `tab:resources` and `tab:chronology`; Results Sections 4.1--4.6.
- **Evidence:** GridDB factorial, 700-call components, 18-state reliability, BIRD, replay, and v3 use different datasets, experimental units, generation calls, endpoint definitions, multiplicity families, and visibility histories.
- **Why it matters:** Readers can easily combine incomparable counts into a perceived overall framework accuracy, despite the later warning not to do so.
- **Actionable fix:** Add a single master table with columns: protocol; unit; N/clusters; candidate-generation budget; endpoint; gold visibility; inferential/descriptive status; multiplicity family; strongest licensed claim. Use it as the sole gateway into Results.

### M3. The E1 paired denominator is not visible in Table `tab:componentcounts`

- **Severity:** Major
- **Evidence anchors:** Section 4.3; Table `tab:componentcounts`.
- **Evidence:** The text reports a Qwen paired effect of +0.1059 over 170 eligible questions and says this equals 18 additional correct items. Table `tab:componentcounts` shows V0 as 83/170 and V1 as 105/180. The paired V1 numerator needed to reproduce the effect is **101/170**, which is absent. `(101-83)/170=0.105882`; `(105/180)-(83/170)=0.095098`, not 0.1059.
- **Why it matters:** The displayed table cannot reproduce the primary component effect and appears to compare unequal denominators.
- **Actionable fix:** Add “V1 paired eligible: 101/170” for Qwen and the corresponding paired Granite count, while retaining 105/180 and 71/180 as all-item descriptives. State why ten questions are ineligible for E1.

### M4. Primary factorial precision is omitted although available

- **Severity:** Major
- **Evidence anchors:** Section 4.2; Table `tab:cells`; Methods Section 3.6.
- **Evidence:** The manuscript gives six within-backbone effects and three selected raw/adjusted p-values, but not the nine-effect table or composition-sensitivity intervals. Retained canonical files contain, for example, Qwen hint +0.2306 with interval [0.0573, 0.4343], Qwen interaction -0.1278 [-0.2447, -0.0343], and Granite hint +0.1583 [-0.0207, 0.3689]. None survives the registered nine-test Holm family.
- **Why it matters:** A non-rejection statement is not an effect-size interpretation. Readers need estimates and uncertainty to distinguish low precision from evidence of negligible effects.
- **Actionable fix:** Insert the complete nine-row primary table with estimate, composition-sensitivity interval, raw p, Holm p, cluster count, and randomization draws. Explicitly say that intervals are not familywise simultaneous confidence intervals.

### M5. Cluster assumptions and effective information are underexplained

- **Severity:** Major
- **Evidence anchors:** Section 3.2 (70 normalized SQL clusters, 58 singletons); Sections 3.6 and 3.7; Table `tab:bird` (11 databases); Section 4.4 (12 structural clusters).
- **Evidence:** Randomization and resampling treat normalized-SQL clusters, database clusters, or structural clusters as dependence units. Most GridDB clusters are singletons; BIRD has only 11 database clusters; the multi-state subset uses 12 clusters.
- **Why it matters:** Cluster exchangeability, cluster weighting, and within-cluster dependence determine the meaning and resolution of p-values and intervals. They are not justified by naming clusters “dependence proxies.”
- **Actionable fix:** Describe precisely whether statistics are question-weighted or cluster-weighted, how a sign is assigned within a cluster, and why exchangeability is plausible. Add cluster-size ranges. State that 11/12-cluster analyses have limited inferential resolution and their intervals describe composition sensitivity only.

### M6. Practical significance and equivalence are not defined

- **Severity:** Major
- **Evidence anchors:** Sections 4.2--4.5; Section 5.1.
- **Evidence:** The paper interprets Holm non-rejection correctly as “does not meet the rule,” but no smallest important accuracy change, risk--coverage utility, latency/token target, or equivalence margin is registered. Some uncertainty is broad: Granite E1 is 0 with composition interval approximately [-0.1903, 0.1705].
- **Why it matters:** “No detectable improvement” does not establish no practically relevant effect. Conversely, +1/180 for complete witnesses is arithmetically positive but has no demonstrated engineering value and is the ambiguous Q039 case.
- **Actionable fix:** State that no equivalence or non-inferiority conclusion is possible. Report all component intervals in the main table and explicitly classify +1/180 as a mechanism trace with no established minimum meaningful benefit.

### M7. “Prospective” requires a narrower definition for the component study

- **Severity:** Major
- **Evidence anchors:** Abstract; Sections 3.2 and 3.6; Table `tab:chronology`; Section 4.3.
- **Evidence:** The component call/selection protocol was frozen before new calls, but it uses the development-visible synthetic GridDB resource and does not constitute an untouched external test.
- **Why it matters:** “Prospective” may be read as outcome-unseen question selection or independent confirmation.
- **Actionable fix:** Replace unqualified “prospective study” with **prospectively frozen call-and-selection procedure on development-visible GridDB items**. State which outcomes were unseen at freeze and which question/gold assets were already accessible to investigators.

### M8. BIRD B3 is not a call-matched treatment contrast

- **Severity:** Major
- **Evidence anchors:** Section 3.6; Table `tab:bird`; Section 4.5.
- **Evidence:** B0--B2 use one call/item, while B3 uses two. The manuscript discloses this, but B3 remains in the same method table and 12-comparison Holm family.
- **Why it matters:** B3 differences combine workflow logic with additional sampling/computation and cannot isolate repair efficacy.
- **Actionable fix:** Visually separate B3 as an unequal-call workflow diagnostic. Restrict causal wording to B0--B2 comparisons, and report B3 only as total-workflow efficacy per its actual two-call budget.

### M9. Reproducibility remains incomplete at submission boundary

- **Severity:** Major
- **Evidence anchors:** Supplementary Materials and Data Availability Statement.
- **Evidence:** The manuscript states that the public repository “must be synchronized and tagged before submission” and does not assert that current public contents match the final candidate.
- **Why it matters:** Extensive local hashes do not provide independent reproducibility if editors cannot obtain the exact code/artifact version referenced by the manuscript.
- **Actionable fix:** Before submission, synchronize, license, tag, archive, fresh-clone test, and cite an immutable release hash/DOI. Until then, call the study locally reproducible, not publicly reproducible.

## Minor findings

1. **“Equal budget” needs qualification.** Table `tab:offline` calls fixed order and validation rank “equal budget,” although all selectors inherit a shared 5760-attempt evidence collection that fixed order would not naturally need. Use “same precomputed candidate/evidence ledger” and separate historical collection cost from selector-time consumption.
2. **Order sensitivity should be an outcome, not a tuning option.** Table `tab:sensitivity` correctly labels reversed order as exposed. Reinforce that 117--118/180 cannot be reported as an alternative performance estimate.
3. **Abstention interpretation is weak.** Zero abstentions in v3 coexist with 130/180 top-score ties. State that coverage reflects permissive stable-order resolution, not calibrated confidence.
4. **Terminology.** “Complete metamorphic coordination” can imply broad robustness; “complete-three-witness selector” is more faithful to the tested mechanism.

## Arithmetic and statistical audit receipt

- GridDB factorial effects recompute exactly from Table `tab:cells`: Qwen hint `(53+30)/360=0.230556`, package `(2-21)/360=-0.052778`, interaction `(30-53)/180=-0.127778`; Granite gives 0.158333, 0.013889, and 0.061111.
- The component selector effects reproduce from rescue/harm counts: Qwen `(8-1)/180=0.038889`; Granite `(10-0)/180=0.055556`.
- The 15-state ledger size is `1440×18=25,920`. The v3 evidence count is `180×8×4=5,760`.
- Replay candidate multiplicities sum to 180; the seven one-candidate cases leave 173 with at least two unique candidates. The eight fail-closed cases reconcile with 172 adjudicated.
- Tie distributions in Table `tab:ties` each sum to 180 and reproduce 130 tied questions. Weighted means reproduce 5.4000 and 5.3889.
- Offline rescue/harm arithmetic reconciles: `80+22-2=100` and `80+23-2=101`.
- BIRD accuracies and deltas reproduce from Table `tab:bird`; the retained 12-value Holm file reproduces adjusted p=0.04296875 and 0.01171875 for the two reported Qwen contrasts.
- No conventional t/F/chi-square statistic with df is reported for bounded p-value recomputation. Randomization values were checked against retained canonical tables; their Monte Carlo/exact algorithms require artifact-level audit rather than inversion from a printed test statistic.

## Conclusion-following-evidence verdict

The conclusions about deterministic traceability, read-only enforcement within the stated threat model, adverse factorial/component results, and fixed-pool order sensitivity follow from the evidence. Five-role superiority, semantic correctness, universal robustness, power-grid operational validity, and prospective end-to-end performance do not follow. The manuscript mostly acknowledges this; the remaining revision should make those limits structurally unavoidable and expose the paired denominators and precision estimates in the main text.
