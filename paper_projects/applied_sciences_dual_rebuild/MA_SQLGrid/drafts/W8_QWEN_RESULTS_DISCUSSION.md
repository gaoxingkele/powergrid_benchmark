# W8 MA-SQLGrid Qwen-7B Results and Discussion Staging Draft

> **Evidence boundary.** This staging text reports only the independently audited Qwen2.5-Coder-7B-Instruct Q4_K_M run on GridDB. It does not report Granite, external-database accuracy, or human-reviewed external results. Those gates remain pending. All displayed values must be imported from the canonical release rather than copied into a manuscript table by hand.

<!-- CLAIM MA-C10 | STATUS ELIGIBLE-E4 | SOURCE ../canonical_qwen7b/release_manifest.json $.scope,$.canonical_counts,$.claim_boundary -->

## 1. Canonical Run Integrity and Scope

The canonical release contains a complete 2 × 2 prompt experiment: 180 GridDB questions were evaluated under four aligned prompt conditions, yielding 720 independently recomputed rows. The four conditions cross full versus compact schema context with absence versus presence of an answer-shape hint. Pairing is exact at the question level, and the statistical audit groups dependence using 70 normalized-gold-SQL template clusters. This design supports within-model, within-database prompt-effect statements; it does not support cross-model or cross-database generalization.

<!-- CLAIM MA-C10 | STATUS ELIGIBLE-E4 | SOURCE ../canonical_qwen7b/release_manifest.json $.canonical_counts; ../statistics/MA_LOCAL_FORMAL_INDEPENDENT_AUDIT.json $.checks[24].evidence -->

The independent audit accepted only `formal_run/qwen25coder7b_q4km_seed20260805_clean_rerun1`. It explicitly rejected the earlier directory `formal_run/qwen25coder7b_q4km_seed20260805`, whose incident status is `quarantined_not_eligible_for_claim_promotion`. No prediction or score from that quarantined directory contributes to the canonical rows, tables, figures, or claims in this section. The clean run has 720 prompts, 720 predictions, and 720 scores; all Cartesian identities are unique and complete, and direct SQLite rescoring produced zero mismatches.

<!-- CLAIM MA-C11 | STATUS ELIGIBLE-E4 | SOURCE ../statistics/MA_LOCAL_FORMAL_INDEPENDENT_AUDIT.json $.eligible_run,$.quarantined_run,$.checks[2:7],$.checks[23]; ../canonical_qwen7b/release_manifest.json $.eligible_run_from_audit,$.quarantined_run_excluded -->

The integrity result is stronger than a successful script exit. The audit verified the frozen configuration, data, code, prompt set, local-model artifact, prompt/context/response linkage, single-generation accounting, read-only SQL guard, and gold isolation. Every provider prediction and evaluator row has status success/scored, with no provider or parse errors and no retries. These checks make the Qwen/GridDB result eligible for canonical statistical use, but they do not make the result representative of other local models, hosted models, databases, or prompt budgets.

<!-- CLAIM MA-C11 | STATUS ELIGIBLE-E4 | SOURCE ../statistics/MA_LOCAL_FORMAL_INDEPENDENT_AUDIT.json $.passed,$.checks[7:24]; ../canonical_qwen7b/release_manifest.json $.source_hashes,$.claim_boundary -->

## 2. Performance of the Four Factorial Cells

Figure `fig01_cell_accuracy` and generated Table `table01_cell_accuracy` summarize the four cells. With full context and no shape hint, 76 of 180 questions execute correctly, for execution accuracy 0.4222; 90 of 180 satisfy the answer-shape evaluator, for shape accuracy 0.5000. Adding the shape hint under full context raises execution correctness to 129 of 180 (0.7167) and shape correctness to 174 of 180 (0.9667). Thus the best observed execution cell is full context with the shape hint.

<!-- CLAIM MA-C10 | STATUS ELIGIBLE-E4 | SOURCE ../canonical_qwen7b/tables/table01_cell_accuracy.csv rows F00_Full_NoShape,F01_Full_WithShape; ../canonical_qwen7b/figures/fig01_cell_accuracy.svg -->

Compact context without the shape hint performs similarly to the full/no-shape cell on execution: 78 of 180 are correct (0.4333), while 79 of 180 satisfy answer shape (0.4389). Compact context with the hint improves execution to 108 of 180 (0.6000) and answer shape to 173 of 180 (0.9611). Shape hints are therefore associated with large within-context changes in both context regimes, whereas compacting the context does not show a uniformly beneficial direction.

<!-- CLAIM MA-C10 | STATUS ELIGIBLE-E4 | SOURCE ../canonical_qwen7b/tables/table01_cell_accuracy.csv rows F10_Compact_NoShape,F11_Compact_WithShape; ../canonical_qwen7b/figures/fig01_cell_accuracy.svg -->

The execution/shape scatter in `fig03_execution_shape_tradeoff` makes an important evaluation distinction visible. Shape accuracy approaches 0.97 in both hint-present cells, but execution accuracy remains 0.7167 with full context and 0.6000 with compact context. A response can satisfy the expected projection or output contract while still produce the wrong database result. Accordingly, answer-shape conformity is a diagnostic outcome rather than a substitute for execution accuracy.

<!-- CLAIM MA-C12 | STATUS ELIGIBLE-E4 | SOURCE ../canonical_qwen7b/tables/table01_cell_accuracy.csv rows F01_Full_WithShape,F11_Compact_WithShape; ../canonical_qwen7b/figures/fig03_execution_shape_tradeoff.svg -->

## 3. Paired Factorial Effects and Interaction

The paired factorial analysis averages the compact-versus-full contrast across shape-hint states, the hint-versus-no-hint contrast across context states, and their difference-in-differences interaction. For execution accuracy, the compact-context main effect is −0.0528 with a 95% template-cluster interval [−0.1136, 0.0000]. The interval does not establish a positive compact-context effect. The shape-hint main effect is +0.2306 with interval [+0.0538, +0.4306], supporting a positive average hint effect for this model and database.

<!-- CLAIM MA-C10 | STATUS ELIGIBLE-E4 | SOURCE ../canonical_qwen7b/tables/table02_factorial_effects.csv rows correct_int/context_compact_main,correct_int/shape_hint_main; ../canonical_qwen7b/figures/fig02_factorial_effects.svg -->

The execution interaction is −0.1278 with interval [−0.2449, −0.0339]. Under the registered coding, this interaction equals the shape-hint effect under compact context minus the shape-hint effect under full context. The negative interval therefore shows that the observed execution benefit of the shape hint is smaller with compact context. This is directly inconsistent with an additive narrative in which compact context and the shape hint supply two independent positive contributions. Candidate claim MA-C03 is consequently NO–GO for the audited Qwen/GridDB experiment.

<!-- CLAIM MA-C03 | STATUS E4-NO-GO | SOURCE ../canonical_qwen7b/tables/table02_factorial_effects.csv row correct_int/interaction; ../canonical_qwen7b/figures/fig02_factorial_effects.svg -->

For answer-shape accuracy, the compact-context main effect is −0.0333 with interval [−0.0906, +0.0037], while the shape-hint main effect is +0.4944 with interval [+0.2662, +0.6912]. The answer-shape interaction is +0.0556 with interval [−0.0149, +0.1646]. Hence the hint has a large positive average relationship with output conformance, but neither a positive compact-context main effect nor a nonzero answer-shape interaction is established by the cluster interval.

<!-- CLAIM MA-C10 | STATUS ELIGIBLE-E4 | SOURCE ../canonical_qwen7b/tables/table02_factorial_effects.csv rows shape_int/context_compact_main,shape_int/shape_hint_main,shape_int/interaction; ../canonical_qwen7b/figures/fig02_factorial_effects.svg -->

These paired effects change the preferred interpretation of MA-SQLGrid. The Qwen result does not show that fewer schema tokens are intrinsically better. Instead, it shows that an explicit answer contract can substantially change behavior, with its execution effect depending on how much schema context is retained. The mechanism behind that dependence remains unresolved: the present factorial identifies prompt-level contrasts, not whether the model used column types, value ranges, join structure, or merely a formatting cue.

<!-- CLAIM MA-C03 | STATUS E4-NO-GO | SOURCE ../canonical_qwen7b/tables/table02_factorial_effects.csv all rows; ../canonical_qwen7b/CAPTIONS.md sections fig02,fig03 -->

## 4. Registered Edge Contrasts and Holm Decisions

The eight registered edge tests combine four factorial edges with two binary outcomes. Under full context, adding the shape hint changes execution accuracy by +0.2944, with cluster interval [+0.1318, +0.4902], and changes answer-shape accuracy by +0.4667, with interval [+0.2323, +0.6710]. Exact paired McNemar tests remain significant after Holm adjustment across all eight edges (adjusted p values 7.14 × 10⁻¹³ and 1.77 × 10⁻²²). Both the cluster intervals and Holm-adjusted paired tests support these two full-context edge results.

<!-- CLAIM MA-C10 | STATUS ELIGIBLE-E4 | SOURCE ../canonical_qwen7b/tables/table03_registered_contrasts.csv rows shape_at_full/correct_int,shape_at_full/shape_int; ../canonical_qwen7b/figures/fig04_registered_contrasts.svg -->

Under compact context, the shape hint changes execution accuracy by +0.1667 and answer-shape accuracy by +0.5222. The execution cluster interval [−0.0405, +0.3869] includes zero even though the Holm-adjusted exact McNemar p value is 0.000367. The answer-shape interval [+0.2970, +0.7165] excludes zero and its Holm-adjusted p value is 2.45 × 10⁻²⁵. Because the two inference procedures use different dependence assumptions, the compact-context execution edge should be described as mixed evidence rather than as uniformly robust; the answer-shape edge is supported by both summaries.

<!-- CLAIM MA-C10 | STATUS ELIGIBLE-E4 | SOURCE ../canonical_qwen7b/tables/table03_registered_contrasts.csv rows shape_at_compact/correct_int,shape_at_compact/shape_int; ../canonical_qwen7b/figures/fig04_registered_contrasts.svg -->

Without a shape hint, compacting the context changes execution by only +0.0111, with interval [−0.0101, +0.0373] and Holm p = 1.000. Its answer-shape change is −0.0611, with interval [−0.1691, +0.0059]; the Holm-adjusted McNemar p is 0.0382, but the template-cluster interval crosses zero. This edge provides no robust evidence that compact context improves execution, and the answer-shape evidence is sensitive to the inferential unit.

<!-- CLAIM MA-C03 | STATUS E4-NO-GO | SOURCE ../canonical_qwen7b/tables/table03_registered_contrasts.csv rows compact_at_no_shape/correct_int,compact_at_no_shape/shape_int; ../canonical_qwen7b/figures/fig04_registered_contrasts.svg -->

With the shape hint present, moving from full to compact context reduces execution by −0.1167, with cluster interval [−0.2339, −0.0208] and Holm p = 0.000415. In contrast, answer shape changes by only −0.0056, with interval [−0.0340, +0.0195] and Holm p = 1.000. This edge explains the negative execution interaction: compact context preserves the requested output shape but loses execution correctness relative to full context.

<!-- CLAIM MA-C10 | STATUS ELIGIBLE-E4 | SOURCE ../canonical_qwen7b/tables/table03_registered_contrasts.csv rows compact_at_with_shape/correct_int,compact_at_with_shape/shape_int; ../canonical_qwen7b/figures/fig04_registered_contrasts.svg -->

The forest plot deliberately displays both cluster intervals and Holm decisions because they answer related but nonidentical questions. Holm controls the registered family of eight exact McNemar tests, whereas the bootstrap treats normalized SQL templates as dependence clusters. A Holm rejection paired with a cluster interval that crosses zero is not hidden or promoted as a definitive effect. The most stable edge claims are those for which direction, cluster interval, and adjusted paired decision agree.

<!-- CLAIM MA-C10 | STATUS ELIGIBLE-E4 | SOURCE ../canonical_qwen7b/tables/table03_registered_contrasts.csv all rows; ../canonical_qwen7b/CAPTIONS.md section fig04_registered_contrasts -->

## 5. Error Taxonomy and Question-Family Diagnostics

The outcome taxonomy separates four mutually exclusive cases: both execution and answer shape correct, execution only, answer shape only, and both incorrect. In the full/no-shape cell, the counts are 52, 24, 38, and 66. With the full-context hint they become 129, 0, 45, and 6. The hint nearly removes shape violations in the full-context cell, but 45 responses still have the requested shape without the correct execution result.

<!-- CLAIM MA-C12 | STATUS ELIGIBLE-E4 | SOURCE ../canonical_qwen7b/tables/table04_error_taxonomy.csv rows F00_Full_NoShape,F01_Full_WithShape; ../canonical_qwen7b/figures/fig05_error_taxonomy.svg -->

The compact cells show the same separation. Compact/no-shape yields 52 both-correct, 26 execution-only, 27 shape-only, and 75 both-incorrect cases. Compact/shape yields 108 both-correct, 0 execution-only, 65 shape-only, and 7 both-incorrect cases. Across both hint-present cells, every execution-correct response also passes the answer-shape evaluator, yet 110 responses are shape-correct without being execution-correct. This is why format or projection conformity cannot be promoted as semantic SQL correctness.

<!-- CLAIM MA-C12 | STATUS ELIGIBLE-E4 | SOURCE ../canonical_qwen7b/tables/table04_error_taxonomy.csv rows F10_Compact_NoShape,F11_Compact_WithShape and sum(shape_only)=110; ../canonical_qwen7b/figures/fig05_error_taxonomy.svg -->

Question-family behavior is heterogeneous. The family heatmap restricts visual comparison to all 12 opaque family clusters containing at least three questions, avoiding unstable rankings driven by singleton families. Aggregated execution accuracy is 0.1389 for `family_f2a050e801ed` (9 questions), 0.1667 for `family_8cd61bcf274e` (3 questions), 0.1786 for `family_e522de2d2816` (28 questions), and 0.1875 for `family_6aab05b51f40` (4 questions). At the other end, three multi-question families are execution-perfect across the four conditions. These identifiers are audit clusters, not semantic error labels.

<!-- CLAIM MA-C10 | STATUS ELIGIBLE-E4 | SOURCE ../canonical_qwen7b/tables/table05_family_error_summary.csv rows family_f2a050e801ed,family_8cd61bcf274e,family_e522de2d2816,family_6aab05b51f40,family_31171172dc6e,family_899e206e4941,family_997207c7abad; ../canonical_qwen7b/figures/fig06_family_execution_heatmap.svg -->

The heatmap also reveals nonuniform prompt responses. For `family_bfc79394b78c` (14 questions), execution is 0.00 in both no-shape cells, 1.00 with full context plus the hint, and 0.86 with compact context plus the hint. For `family_5615d0813d2b` (19 questions), three cells are 1.00 but compact context with the hint is 0.47. These patterns are useful for selecting cases for qualitative review, but they do not by themselves identify a causal error type. Semantic labels require inspection of question text, schemas, predicted SQL, and gold execution behavior under a predefined coding manual.

<!-- CLAIM MA-C10 | STATUS ELIGIBLE-E4 | SOURCE ../canonical_qwen7b/figures/fig06_family_execution_heatmap.svg cells family_bfc79394b78c,family_5615d0813d2b; ../canonical_qwen7b/tables/table05_family_error_summary.csv same rows -->

## 6. Efficiency Boundary

The canonical Qwen release does not contain a comparable latency, throughput, token-count, energy, or memory table. The audit confirms one provider generation per final row and no retries, which supports accounting integrity but not an accuracy–cost–latency claim. MA-C09 therefore remains PENDING. Efficiency results may enter the manuscript only after a predefined measurement boundary covers prompt construction, model inference, parsing, execution, warm-up policy, hardware, and both intended models.

<!-- CLAIM MA-C09 | STATUS PENDING-E4 | SOURCE ../statistics/MA_LOCAL_FORMAL_INDEPENDENT_AUDIT.json $.checks[16:20]; ../canonical_qwen7b/release_manifest.json $.claim_boundary -->

## 7. Discussion and Claim Boundary

The most defensible Qwen/GridDB conclusion is conditional rather than universal. Shape hints have a positive average effect on execution and answer-shape accuracy in this run, but the negative execution interaction shows that their execution benefit is attenuated under compact context. Compact context has no established positive main effect and, when a shape hint is present, significantly reduces execution relative to full context. The data therefore reject the proposed story of two independent positive prompt interventions while supporting a narrower interaction-aware account.

<!-- CLAIM MA-C03 | STATUS E4-NO-GO | SOURCE ../canonical_qwen7b/tables/table02_factorial_effects.csv rows correct_int/context_compact_main,correct_int/shape_hint_main,correct_int/interaction; ../canonical_qwen7b/tables/table03_registered_contrasts.csv row compact_at_with_shape/correct_int -->

This result also clarifies what “answer-shape guidance” can and cannot mean. It is effective at enforcing a response contract, and under full context it coincides with a large execution improvement. However, the shape-only cases demonstrate that contract conformance is not sufficient for retrieving the correct database answer. MA-SQLGrid should therefore report execution accuracy as the primary outcome and answer shape as a diagnostic that helps locate projection and formatting failures.

<!-- CLAIM MA-C12 | STATUS ELIGIBLE-E4 | SOURCE ../canonical_qwen7b/tables/table01_cell_accuracy.csv all rows; ../canonical_qwen7b/tables/table04_error_taxonomy.csv all rows -->

The experiment has five important external-validity limits. First, it evaluates one quantized Qwen model and one execution seed. Second, it uses only GridDB in the formal accuracy analysis. Third, the RTS-GMLC and SimBench records remain deterministic `AUTO_CANDIDATE` pilots rather than publication-ready human gold; no external-database accuracy is reported here. Fourth, Granite robustness is PENDING and must not be represented by a placeholder result. Fifth, external question review is HUMAN-DEPENDENT: the prepared forms and adjudication protocol do not substitute for two real reviewers and completed adjudication.

<!-- CLAIM MA-C02 | STATUS ELIGIBLE-DIAGNOSTIC | SOURCE ../../CLAIM_LEDGER.md rows MA-C02,MA-C05,MA-C06; ../canonical_qwen7b/release_manifest.json $.claim_boundary -->

These limits define the next gates rather than invalidate the canonical Qwen result. Granite must execute the identical registered 2 × 2 protocol before cross-model stability is discussed. External GridDB-to-RTS-GMLC/SimBench accuracy requires an independently reviewed, sealed gold set. Efficiency requires a common measurement harness. Validator-repair benefit requires its own trigger, benefit, and harm audit. Until those gates close, the canonical release supports only the local paired prompt effects and integrity statements recorded as MA-C10 through MA-C12.

<!-- CLAIM MA-C06 | STATUS HUMAN-DEPENDENT | SOURCE ../../CLAIM_LEDGER.md rows MA-C06,MA-C08,MA-C09; ../canonical_qwen7b/release_manifest.json $.claim_boundary -->

## 8. Staging Integration Notes

- Import Tables `table01`–`table04` from `canonical_qwen7b/tables/*.tex`; keep the full family table supplementary and use `table05_family_error_summary.tex` only as a descriptive diagnostic.
- Use Figures `fig01`, `fig02`, `fig04`, and `fig05` as the main evidence chain. Figure `fig03` is an explanatory trade-off view, and Figure `fig06` is a family diagnostic rather than a confirmatory result.
- Keep all figures at full text width; the page-scale QA specifically prohibits narrow placement for Figures 2, 4, and 6.
- Do not merge this staging draft into the manuscript until the claim verifier maps every quantitative sentence to the release manifest and the manuscript explicitly labels Granite, external accuracy, efficiency, and human review as pending.

<!-- CLAIM MA-C11 | STATUS ELIGIBLE-E4 | SOURCE ../canonical_qwen7b/VISUAL_QA.md; ../canonical_qwen7b/release_manifest.json $.outputs -->
