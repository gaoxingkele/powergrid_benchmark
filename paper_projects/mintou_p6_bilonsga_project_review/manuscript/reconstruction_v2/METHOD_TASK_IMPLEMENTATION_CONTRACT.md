# P2 Bidirectional Local-Search and Investment-Task Contract

**Stage:** `p2_v2_s03_method_task_implementation_contract`  
**Status:** `IMPLEMENTED / INPUT REGISTRIES NO-GO / NO NEW RESULTS`  
**Scope:** prospective method and task specification only. The legacy and matched-effort archives are unchanged.

## 1. Evidence boundary

The existing 120-candidate proxy mixes RTS-GMLC and SimBench-derived archetypes. It is suitable for the reported historical questions but is not two independent action-aligned task families: several candidates denote archetypes rather than a uniquely identified asset intervention, and their costs are synthetic coefficients without a frozen row-level formula record. This stage therefore does not relabel that archive or manufacture action IDs, increments, or calibrated costs.

The prospective code in `scripts/p2_s03_method_task_contract.py` defines the required semantics and validators. Formal execution remains **NO-GO** until both source registries, source hashes, increments, cost-model coefficients/provenance, family-specific budgets, seeds, normalization bounds, and the comparison plan are frozen. No numerical result is introduced here.

## 2. Two independently generated action-aligned task families

| Family | Source and generator | Decision action | Traceable cost |
|---|---|---|---|
| `rts_transmission_reinforcement` | identified RTS-GMLC branch rows; `build_rts_transmission_tasks` | increase the registered branch rating by the row's preregistered MVA increment | `fixed_units + variable_units * capacity_increment_mva` in synthetic benchmark units |
| `simbench_feeder_reinforcement` | identified SimBench line rows; `build_simbench_feeder_tasks` | increase the registered line rating by the row's preregistered MVA increment | `fixed_units + variable_units * line_length_km` in synthetic benchmark units |

Every action row carries a family-qualified action ID, source artifact and SHA-256, persistent source-element ID, action type, increment and unit, cost value, formula ID, formula input/name, and cost provenance. Formula coefficients are configuration inputs, not constants invented by the implementation. “Synthetic benchmark units” must remain the label unless external calibration evidence is supplied.

Independence means separate source snapshots, generator functions, action namespaces, task instances, seeds, budgets, normalization references, and result rows. A source digest cannot be shared between the two families. Results may be compared within each family under its frozen multiplicity plan; they may not be pooled into an “independent-family” claim without a separately registered estimand.

## 3. Violation and deterministic repair

For binary portfolio \(x\), positive budget \(B\), and registered action costs \(c_j\),

\[
C(x)=\sum_j c_jx_j,\qquad v_B(x)=\max\{0,(C(x)-B)/B\}.
\]

Evaluation, constraint ranking, acceptance, and reporting use this same dimensionless violation. Repair repeatedly removes the selected action minimizing \(b_j/c_j\), where \(b_j\) is the preregistered proposal-ranking benefit. A nonnegative-benefit zero-cost action has infinite ratio and is not selected ahead of a finite-ratio action. Exact ratio ties are broken by ascending stable `action_id`. Each deletion reduces selected cardinality, so repair stops when affordable after at most \(\lVert x\rVert_0\) removals. Repair is a deterministic feasibility transformation, not a scored local proposal.

## 4. Move grammar and atomicity

Let \(A_+(x)=\{j:x_j=0,\ c_j\le B-C(x)\}\). Forward insertion selects the maximum benefit/cost ratio in this set, with ascending action ID resolving exact ties, and proposes \(x^+=x+e_{j_+}\). If the set is empty, the pass ends.

Backward deletion selects the minimum benefit/cost ratio among selected actions, with the same tie rule, and proposes \(x^-=x-e_{j_-}\). `backward_only` means this standalone deletion move. It must not silently mean replacement.

Atomic substitution is a separate optional control: provisionally delete \(j_-\), choose the best affordable \(j_+\ne j_-\), score the combined phenotype once, and either commit or roll back both edits. No deletion-only intermediate state is evaluated or retained by atomic substitution.

The four principal arms are `nds_only`, `forward_only`, `backward_only`, and `bidirectional`; the last applies a forward pass and a standalone backward pass with separately frozen depths. If atomic substitution is tested, its gate and comparison must be explicit and factorially identifiable. Combined arms support only joint conclusions.

## 5. Acceptance and tie rules

With task-family-specific objective bounds \((L_q,H_q)\) frozen before search,

\[
\Phi(x)=\sum_q\frac{f_q(x)-L_q}{\max(H_q-L_q,10^{-12})}+\lambda v_B(x).
\]

A proposal is accepted iff \(\Phi(x')<\Phi(x)\). Equality is rejection. Bounds and \(\lambda\) do not change inside a run. Non-finite objective values are hard failures. Each pass uses a first-improvement path: after acceptance it proposes from the new state; at the first non-improvement it retains the current state and stops. Ranking ties use ascending action ID. Any population-selection tie rule must be frozen separately before a formal run; no cross-version replay claim is made for the legacy unstable sorts.

## 6. Duplicate cache, unique evaluation, and termination

The cache key is the canonical binary phenotype within one task-family instance. Each scoring request increments `requests`. A cache miss computes objectives and violation once, stores both, and increments `unique_evaluations`; a cache hit increments `cache_hits` and uses the stored values without a second unique charge. Population and local-search requests share the cache. Repair does not itself increment the unique counter, but its repaired phenotype is charged on first scoring.

Formal method comparisons use the same frozen maximum unique-evaluation budget. Because repeated phenotypes do not consume it, every run must also have a common request cap. A local pass terminates on its depth cap, neighborhood exhaustion, first non-improvement, request cap, or unique-evaluation cap. The outer algorithm terminates on the first reached global unique-evaluation or request cap; generation count alone is not the budget. Final-front extraction and metrics are post-search readouts.

The implementation returns explicit termination reasons. Strict improvement plus finite depth prevents an accepted-move cycle within a pass; the request cap prevents a duplicate-only outer loop. Generated requests, unique evaluations, cache hits, repair calls/removals, accepted moves by type, and termination reason must be exported separately.

## 7. Pseudocode

```text
BUILD-FAMILY(source rows, frozen source SHA, frozen cost model):
  validate one persistent source-element ID and one action increment per row
  compute synthetic cost from the declared formula and retain formula inputs
  namespace and sort actions by action_id; reject duplicates or source mixing

SCORE(x):
  requests += 1; stop if request cap is exhausted
  if canonical(x) is cached: cache_hits += 1; return cached (F, v_B)
  stop if unique-evaluation cap is exhausted
  compute F(x) and the same v_B(x) used everywhere; cache them
  unique_evaluations += 1; return (F, v_B)

LOCAL-PASS(x, operator, depth):
  score current x through SCORE
  repeat at most depth times:
    propose deterministic forward insertion, backward deletion,
      or explicitly gated atomic substitution; ties by action_id
    stop if no candidate or either evaluation cap is reached
    score the complete proposed phenotype once
    if Phi(proposal) < Phi(current): commit the complete move
    else: reject/roll back the complete move and stop
  return current state, accepted count, and termination reason

BILO arm:
  build and repair initial population; score through the shared cache
  while both global evaluation caps remain:
    generate offspring; repair; score through the shared cache
    apply only the arm's declared local pass(es)
    perform frozen constraint-NDS selection and its declared tie rule
  return population and separate accounting fields
```

## 8. Claim and records boundary

These rules define reproducible optimization bookkeeping; they do not establish accuracy, field value, calibrated economics, electrical feasibility, cybersecurity, provenance security, or auditability. Logs and counters are diagnostics. They are not an audit mechanism, lineage proof, replay record, or explanation validation. No reliability label or grid event is reinterpreted as cybersecurity evidence.

Required next-stage inputs are the two complete action registries and hashes, frozen formula coefficients with provenance, per-family objectives/budgets/bounds, population tie rule, arm depths and order, unique/request budgets, seed and tuning split, multiplicity plan, environment record, and output schema. Until all gates pass, `formal_run_allowed` remains false and `results` remains empty.
