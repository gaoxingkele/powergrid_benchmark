# W9 MA-SQLGrid Dual-Backbone Results and Discussion Staging Draft

> **Evidence boundary.** This draft reports two independently audited quantized instruction backbones—Qwen2.5-Coder-7B Q4_K_M and Granite-3.3-8B Q4_K_M—on the same 180 GridDB questions. It is a bounded two-backbone sensitivity analysis, not evidence of general model-family robustness, external-database accuracy, human-reviewed external validity, or comparative efficiency.

<!-- CLAIM MA-C13 | STATUS ELIGIBLE-E4 | SOURCE ../canonical_dual_backbone/release_manifest.json $.scope,$.canonical_counts,$.claim_boundary -->

## 1. Dual-Backbone Integrity Boundary

Each backbone contributes a complete 720-row Cartesian experiment: 180 questions crossed with four aligned prompt cells. Qwen and Granite use identical question/cell keys, the same GridDB data boundary, and the same 70 normalized-gold-SQL template clusters for paired bootstrap inference. The dual release therefore compares 1440 canonical rows while preserving question-level pairing rather than treating the two runs as independent samples.

<!-- CLAIM MA-C13 | STATUS ELIGIBLE-E4 | SOURCE ../canonical_dual_backbone/release_manifest.json $.canonical_counts; ../canonical_dual_backbone/tables/table01_dual_cell_accuracy.csv all rows -->

The Qwen evidence remains restricted to the independently accepted clean rerun; its earlier incident directory remains quarantined and contributes no canonical row. The Granite audit independently passed all 35 checks, reproduced 720 of 720 execution and answer-shape verdicts, recorded no provider, parse, scoring, retry, or resume failures, and did not read the contaminated Qwen directory. Model, prompt-set, configuration, data, code, and source-artifact hashes are bound in the dual release manifest.

<!-- CLAIM MA-C15 | STATUS ELIGIBLE-E4 | SOURCE ../statistics/MA_LOCAL_FORMAL_INDEPENDENT_AUDIT.json $.eligible_run,$.quarantined_run,$.passed; ../statistics_granite/GRANITE_INDEPENDENT_AUDIT.json $.passed,$.checks; ../canonical_dual_backbone/release_manifest.json $.source_hashes,$.audit_decisions -->

## 2. Cell-Level Replication and Divergence

Without a shape hint, the two backbones are close. In the full/no-shape cell, Qwen execution accuracy is 0.4222 and Granite is 0.4278; in the compact/no-shape cell, Qwen is 0.4333 and Granite is 0.4111. The paired Granite-minus-Qwen differences are +0.0056 [−0.0316, +0.0470] and −0.0222 [−0.0800, +0.0239], and both Holm-adjusted McNemar decisions retain the null. These cells do not establish a backbone difference.

<!-- CLAIM MA-C13 | STATUS ELIGIBLE-E4 | SOURCE ../canonical_dual_backbone/tables/table01_dual_cell_accuracy.csv rows F00,F10; ../canonical_dual_backbone/tables/table05_cross_backbone_cells.csv rows F00/correct_int,F10/correct_int; ../canonical_dual_backbone/figures/fig01_dual_cell_accuracy.svg -->

The strongest cell divergence occurs under full context with the shape hint. Qwen reaches execution accuracy 0.7167, whereas Granite reaches 0.5556. The paired Granite-minus-Qwen difference is −0.1611 with template-cluster interval [−0.2975, −0.0484] and Holm-adjusted p = 3.90 × 10⁻⁵. Both inferential summaries support a Qwen advantage in this specific F01 cell. This is a cell-specific result, not an overall ranking of the backbones.

<!-- CLAIM MA-C14 | STATUS ELIGIBLE-E4 | SOURCE ../canonical_dual_backbone/tables/table01_dual_cell_accuracy.csv rows Qwen/F01,Granite/F01; ../canonical_dual_backbone/tables/table05_cross_backbone_cells.csv row F01/correct_int; ../canonical_dual_backbone/figures/fig05_cross_backbone_cells.svg -->

In the compact/shape cell, both backbones obtain execution accuracy 0.6000, yielding a point difference of 0.0000 with interval [−0.1019, +0.1095] and Holm p = 1.000. Thus the full/shape gap does not persist across the other hint-present context. Answer-shape accuracy is high for both hint cells, but Qwen is numerically higher: 0.9667 versus 0.8778 under full context and 0.9611 versus 0.9222 under compact context.

<!-- CLAIM MA-C14 | STATUS ELIGIBLE-E4 | SOURCE ../canonical_dual_backbone/tables/table01_dual_cell_accuracy.csv rows F01,F11; ../canonical_dual_backbone/tables/table05_cross_backbone_cells.csv rows F11/correct_int,F01/shape_int,F11/shape_int -->

The full/shape answer-shape difference illustrates why the release shows both cluster intervals and Holm decisions. Granite minus Qwen is −0.0889; the cluster interval [−0.2249, +0.0125] crosses zero, whereas the Holm-adjusted exact McNemar p is 0.0108. This is mixed evidence under different dependence assumptions and is not promoted as a robust cross-backbone answer-shape gap.

<!-- CLAIM MA-C14 | STATUS ELIGIBLE-E4 | SOURCE ../canonical_dual_backbone/tables/table05_cross_backbone_cells.csv row F01/shape_int; ../canonical_dual_backbone/figures/fig05_cross_backbone_cells.svg -->

## 3. Shape-Hint Direction Replication and CI Nuance

The average execution shape-hint effect is positive for both backbones: +0.2306 for Qwen and +0.1583 for Granite. Qwen's 95% template-cluster interval [+0.0538, +0.4306] excludes zero, whereas Granite's interval [−0.0200, +0.3665] crosses zero. The correct replication statement is therefore directional: both point estimates are positive, but only Qwen's within-backbone execution interval establishes a nonzero average effect.

<!-- CLAIM MA-C13 | STATUS ELIGIBLE-E4 | SOURCE ../canonical_dual_backbone/tables/table04_shape_effect_replication.csv rows correct_int/Qwen-7B,correct_int/Granite-8B; ../canonical_dual_backbone/figures/fig04_shape_effect_replication.svg -->

Answer-shape main effects are +0.4944 for Qwen with interval [+0.2662, +0.6912] and +0.4528 for Granite with interval [+0.2710, +0.6399]. Both intervals exclude zero. Thus the response-contract effect replicates more clearly than the execution effect: adding the shape hint reliably changes output conformance in these two runs, while correct database execution remains more backbone- and context-sensitive.

<!-- CLAIM MA-C13 | STATUS ELIGIBLE-E4 | SOURCE ../canonical_dual_backbone/tables/table04_shape_effect_replication.csv rows shape_int/Qwen-7B,shape_int/Granite-8B; ../canonical_dual_backbone/figures/fig04_shape_effect_replication.svg -->

The paired backbone modifier quantifies magnitude sensitivity. Granite's execution shape-hint main effect is 0.0722 lower than Qwen's, with Granite-minus-Qwen interval [−0.1230, −0.0272]. In contrast, the answer-shape effect difference is −0.0417 with interval [−0.1811, +0.1049]. The execution magnitude differs between these two backbones, whereas the available interval does not establish an answer-shape magnitude difference.

<!-- CLAIM MA-C14 | STATUS ELIGIBLE-E4 | SOURCE ../canonical_dual_backbone/tables/table03_backbone_effect_modifiers.csv rows correct_int/backbone_x_shape_hint_main,shape_int/backbone_x_shape_hint_main; ../canonical_dual_backbone/figures/fig03_backbone_effect_modifiers.svg -->

## 4. Context Dependence and the Three-Way Interaction

The per-backbone execution interactions have opposite signs. Qwen's context-by-shape interaction is −0.1278 with interval [−0.2449, −0.0339], showing attenuation of the shape-hint benefit under compact context. Granite's corresponding interaction is +0.0611 with interval [−0.0524, +0.2000], whose interval includes zero. The Granite-minus-Qwen three-way interaction is +0.1889 with interval [+0.0067, +0.4310]. This interval establishes backbone sensitivity in how context modifies the shape-hint execution effect.

<!-- CLAIM MA-C14 | STATUS ELIGIBLE-E4 | SOURCE ../canonical_dual_backbone/tables/table02_backbone_factorial_effects.csv rows correct_int/interaction; ../canonical_dual_backbone/tables/table03_backbone_effect_modifiers.csv row correct_int/backbone_x_interaction; ../canonical_dual_backbone/figures/fig03_backbone_effect_modifiers.svg -->

The context main effects themselves remain uncertain. Execution estimates are −0.0528 [−0.1136, 0.0000] for Qwen and +0.0139 [−0.0574, +0.0801] for Granite; their +0.0667 backbone difference has interval [−0.0375, +0.1801]. Neither backbone nor the cross-backbone modifier establishes a uniformly positive compact-context effect. The original claim that compact context and shape hints provide independent positive gains therefore remains NO–GO.

<!-- CLAIM MA-C03 | STATUS E4-NO-GO | SOURCE ../canonical_dual_backbone/tables/table02_backbone_factorial_effects.csv rows correct_int/context_compact_main; ../canonical_dual_backbone/tables/table03_backbone_effect_modifiers.csv row correct_int/backbone_x_context_compact_main -->

Granite's registered edges reinforce the context nuance. Under full context, its execution hint edge is +0.1278 with cluster interval [−0.1019, +0.3623] but Holm p = 0.0222, again mixed across inferential units. Under compact context, its execution hint edge is +0.1889 with interval [+0.0361, +0.3798] and Holm p = 1.86 × 10⁻⁶; both summaries support this edge. Granite therefore does not reproduce Qwen's negative interaction pattern even though both backbones have positive average hint point estimates.

<!-- CLAIM MA-C13 | STATUS ELIGIBLE-E4 | SOURCE ../statistics_granite/granite_registered_contrasts.csv rows shape_at_full/correct_int,shape_at_compact/correct_int; ../canonical_dual_backbone/tables/table02_backbone_factorial_effects.csv row Granite-8B/correct_int/interaction -->

## 5. Interpretation

The dual-backbone result supports a narrower and more useful conclusion than a universal prompt recipe. Shape hints consistently push answer-shape conformity upward and have positive execution point estimates for both backbones. However, the execution magnitude, the strongest cell, and the context-by-shape interaction vary by backbone. Prompt recommendations should therefore be conditioned on the backbone and validated with execution, rather than inferred from formatting compliance or averaged across models.

<!-- CLAIM MA-C13 | STATUS ELIGIBLE-E4 | SOURCE ../canonical_dual_backbone/tables/table02_backbone_factorial_effects.csv all rows; ../canonical_dual_backbone/tables/table03_backbone_effect_modifiers.csv all rows -->

The F01 gap is operationally important but should not be overgeneralized. Qwen is better than Granite for full context plus shape hint in this GridDB execution test, yet the backbones are equal in the compact/shape execution cell and statistically indistinguishable in both no-shape execution cells. Selecting only F01 would exaggerate a global backbone ranking; reporting all eight paired cell/metric contrasts preserves the actual boundary.

<!-- CLAIM MA-C14 | STATUS ELIGIBLE-E4 | SOURCE ../canonical_dual_backbone/tables/table05_cross_backbone_cells.csv all rows; ../canonical_dual_backbone/figures/fig05_cross_backbone_cells.svg -->

Answer-shape correctness remains diagnostic rather than semantic. Both models can produce high shape accuracy while retaining substantially lower execution accuracy, particularly in hint-present cells. The replicated answer-shape effect demonstrates reliable contract following, not reliable content retrieval. Execution accuracy remains the primary endpoint for text-to-SQL claims.

<!-- CLAIM MA-C12 | STATUS ELIGIBLE-E4 | SOURCE ../canonical_dual_backbone/tables/table01_dual_cell_accuracy.csv all rows; ../canonical_dual_backbone/figures/fig01_dual_cell_accuracy.svg -->

## 6. Remaining Gates and Limitations

This evidence covers two quantized instruction backbones, not a model family. Both are evaluated on one synthetic GridDB benchmark, one frozen execution per backbone, one prompt factorial, and one evaluator boundary. The result does not cover hosted frontier models, alternative quantizations, decoding variability, different databases, or prompt-budget sensitivity beyond the registered full/compact contrast.

<!-- CLAIM MA-C13 | STATUS ELIGIBLE-E4 | SOURCE ../canonical_dual_backbone/release_manifest.json $.scope,$.claim_boundary -->

RTS-GMLC and SimBench remain `AUTO_CANDIDATE` external pilots. Their schema, prompt, and evaluator plumbing is mechanically audited, but no text-to-SQL accuracy from those pilots enters this draft. Cross-database accuracy remains HUMAN-DEPENDENT until independent reviewers complete the prepared forms, disagreements are adjudicated, and a sealed external set is frozen without model-output exposure.

<!-- CLAIM MA-C06 | STATUS HUMAN-DEPENDENT | SOURCE ../../CLAIM_LEDGER.md rows MA-C02,MA-C05,MA-C06; ../canonical_dual_backbone/release_manifest.json $.claim_boundary -->

Comparative efficiency also remains PENDING. The dual canonical release contains integrity accounting but no common latency, throughput, token, energy, or memory table for the two backbones. No accuracy–cost–latency claim should be derived from run completion times or log timestamps. A future efficiency experiment must freeze hardware, serving configuration, warm-up, prompt accounting, parsing, execution, and failure handling.

<!-- CLAIM MA-C09 | STATUS PENDING-E4 | SOURCE ../../CLAIM_LEDGER.md row MA-C09; ../canonical_dual_backbone/release_manifest.json $.claim_boundary -->

Validator-repair benefit remains PENDING, and the external human-gold gate remains open. These incomplete items are not placeholders for favorable values and must not be inserted into Results until their registered protocols finish. The present release is complete for the bounded two-backbone/GridDB estimands only.

<!-- CLAIM MA-C08 | STATUS PENDING-E4 | SOURCE ../../CLAIM_LEDGER.md rows MA-C06,MA-C08; ../canonical_dual_backbone/release_manifest.json $.claim_boundary -->

## 7. Staging Integration Notes

- Use generated dual Tables 1, 2, 3, and 5 for the main evidence chain; Table 4 provides the concise replication boundary.
- Use Figures 1–5 at full text width. Figures 2, 3, and 5 must not be reduced to a narrow column.
- State “positive direction replicated” separately from “interval excludes zero”; Granite execution is the required nuance.
- Report the Qwen-versus-Granite F01 gap together with the equal F11 execution cell and null no-shape comparisons.
- Do not merge into the main manuscript until a claim/source verifier checks every imported generated fragment and the declarations retain the external/human/efficiency gates.

<!-- CLAIM MA-C15 | STATUS ELIGIBLE-E4 | SOURCE ../canonical_dual_backbone/VISUAL_QA.md; ../canonical_dual_backbone/release_manifest.json $.outputs -->
