# MA-SQLGrid Applied Sciences Experiment Plan

## Registered research questions

1. **RQ1---applied accuracy:** compare schema-only, full-schema/value, generic
   selective context, compact domain context, and validated MA-SQLGrid on the
   frozen 180-question held-out split with two generators.
2. **RQ2---mechanism identification:** run a 2x2 factorial crossing context
   scope (full versus compact) with answer-shape hints (absent versus present).
   This replaces the current non-identifiable compact-context interpretation.
3. **RQ3---component value:** remove value normalization and validation/repair
   separately. Report paired changes and failure-category transitions.
4. **RQ4---robustness:** use three independent serving repeats per generator,
   symmetric row scaling {1x, 10x}, and symmetric distractor-schema counts
   {0, 2, 5, 10}. Do not enlarge only the full-context candidate space.
5. **RQ5---engineering transfer:** evaluate on a second independently designed
   maintenance database or a de-identified real operational database. The
   current synthetic single-database evidence cannot establish deployment
   generalization.
6. **RQ6---resource trade-off:** report measured input/output tokens, latency,
   provider failures, repair calls, and accuracy per 1000 input tokens.

## Primary endpoints and statistics

- Primary endpoint: strict execution accuracy on the frozen test split.
- Secondary endpoints: projection-tolerant denotation accuracy, answer-shape
  accuracy, safe-SQL rate, latency, token use, and repair rate.
- Use paired per-question bootstrap confidence intervals and paired McNemar
  tests for accuracy. Correct primary pairwise comparisons with Holm's method.
- Treat temperature-0 repetitions as serving-stability checks, not independent
  samples from a scientific population.
- Freeze prompts, model versions, database hashes, and evaluator version before
  any formal calls. Report API date and exact endpoint because hosted models can
  change without notice.

## Executable factorial

The new runner creates all 720 prompts for the complete 2x2 design without
using gold SQL during prediction. Its default mode incurs no provider cost:

```powershell
python source/code/experiment_final/applsci_factorial.py
python source/code/experiment_final/applsci_factorial.py --execute
```

The second command makes external model calls and should be run only after the
authors confirm the endpoint and budget. Until it completes, manuscript claims
must describe compact context plus answer-shape guidance as a combined
condition rather than attributing the gain to compactness alone.
