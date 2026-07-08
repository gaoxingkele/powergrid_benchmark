# Stage 14 Result Analysis After Bounded Repair

## Source And Consumption Boundary

This Stage 14 analysis consumes only the repaired canonical artifacts:

- formal outputs: `pipeline/runs/run_001/stage-12/formal_outputs_repair1/`
- canonical Stage 13 package: `pipeline/runs/run_001/stage-13/experiment_final/outputs/`
- paired analysis: `pipeline/runs/run_001/stage-13/failure_analysis.md`

The archived pre-repair Stage 12/13/14 outputs remain diagnostic failed-pass evidence only. They must not be used for Stage 15, paper claims, figures, or tables.

Protocol B was approved by Paper-Harness `run_20260622-173217`: the formal run is one deterministic full-test pass over Q021-Q200, with `seed=0` used only as a reproducibility label. The run is not a multi-seed variance estimate, and any paper text must not interpret `execution_accuracy_std=0` as stability evidence.

## Formal Results

| condition | correct / 180 | execution accuracy | answer-shape accuracy | valid SQL | value-hint coverage | prompt tokens | latency ms |
|---|---:|---:|---:|---:|---:|---:|---:|
| C1_SchemaOnly_Direct | 71 | 0.3944 | 0.3278 | 1.0000 | 1.0000 | 381.3 | 3259.8 |
| C2_FullSchemaValues_Direct | 79 | 0.4389 | 0.3667 | 1.0000 | 1.0000 | 710.3 | 2959.0 |
| C3_CHESSLite_Generic | 72 | 0.4000 | 0.5056 | 1.0000 | 1.0000 | 202.0 | 2895.1 |
| C4_MASQLGrid_DomainContext | 126 | 0.7000 | 0.8889 | 1.0000 | 0.9716 | 259.2 | 2887.5 |
| C5_MASQLGrid_DomainContext_Validated | 131 | 0.7278 | 0.9722 | 1.0000 | 0.9972 | 258.2 | 5562.5 |

The repaired result is not a method-level failure. C4 and C5 both clearly outperform C1, C2, and C3 on the formal test split. C4 is the cleanest core method signal: it improves execution accuracy from the strongest non-MA-SQLGrid baseline C2 by +0.2611 absolute while using far fewer estimated prompt tokens than C2. C5 is best overall, with a smaller +0.0278 absolute gain over C4 and higher answer-shape accuracy, but it has a substantial latency cost.

## Paired Evidence

| comparison | A only correct | B only correct | both correct | both wrong | mean diff | exact sign p |
|---|---:|---:|---:|---:|---:|---:|
| C4 vs C1 | 57 | 2 | 69 | 52 | +0.3056 | 6.144e-15 |
| C4 vs C2 | 49 | 2 | 77 | 52 | +0.2611 | 1.179e-12 |
| C4 vs C3 | 55 | 1 | 71 | 53 | +0.3000 | 1.582e-15 |
| C5 vs C1 | 64 | 4 | 67 | 45 | +0.3333 | 5.874e-15 |
| C5 vs C2 | 56 | 4 | 75 | 45 | +0.2889 | 9.085e-13 |
| C5 vs C3 | 63 | 4 | 68 | 45 | +0.3278 | 1.107e-14 |
| C5 vs C4 | 12 | 7 | 119 | 42 | +0.0278 | 0.3593 |

The paired comparisons support a strong narrow claim for MA-SQLGrid against the non-MA-SQLGrid baselines. They do not support a strong standalone claim that C5 is robustly superior to C4; C5 should be described as an incremental validation/reranking layer that improves answer-shape accuracy and slightly improves execution accuracy at higher latency.

## C5 Validation Boundary

C5 uses `c5_candidate_limit=5`. Candidate SQL strings are generated from the same C4 domain context, then ranked with reference-free checks: read-only execution status, inferred answer shape, inferred value hints, ordering hints, and deterministic tie-breaking by candidate order. The ranking and repair logic do not use gold SQL, gold result rows, required-literal metadata, answer-shape metadata, or order-sensitive metadata during formal inference. Gold information is used only after prediction generation by the evaluator and offline diagnostics.

Fallback behavior is conservative: if no candidate is extracted, the runner emits a safe placeholder and records the error; if validation fails, one repair opportunity is allowed under the same no-gold prompt boundary. The repaired formal run reports zero contract errors, zero unsafe SQL records, zero provider/model/extraction errors, and zero leakage-scan problems.

## Paper-Claim Boundary

Supported claim:

MA-SQLGrid improves validated denotation accuracy on the controlled `GridDB-Maintenance-v2 v0.1` Text-to-SQL benchmark against the approved schema-only, full-schema-values, and generic compact baselines under the fixed gpt-5.4-mini/Krill, temperature-0, protocol-B deterministic evaluation.

Unsupported claims:

- broad Text-to-SQL robustness
- production readiness
- SOTA on Spider, WikiSQL, BIRD, or other external benchmarks
- statistical stability across random seeds
- a large isolated validation-layer contribution beyond the C4 domain-context mechanism

## Figure And Table Consumption Notes

The repaired figure manifest provides four Stage 15 consumable figures:

- `charts/architecture_diagram_1.png`: MA-SQLGrid architecture overview.
- `charts/pipeline_overview_2.png`: end-to-end experiment and evaluation flow.
- `charts/fig_main_results.png`: formal execution accuracy with Wilson 95% item-level intervals over 180 test questions. These intervals are not run-to-run variance.
- `charts/fig_multi_metric.png`: accuracy, context-size, and latency tradeoff.

`results_table.tex` is now a compact paper-facing table plus paired-comparison table. It replaces the previous raw metric dump and should be used as the primary Stage 15 table source.

## Recommendation

Proceed only after Paper-Harness accepts this repaired Stage 14 bundle. If accepted, Stage 15 should keep the method story positive but narrow: C4 is the main mechanism win; C5 is a useful but latency-expensive validation extension.
