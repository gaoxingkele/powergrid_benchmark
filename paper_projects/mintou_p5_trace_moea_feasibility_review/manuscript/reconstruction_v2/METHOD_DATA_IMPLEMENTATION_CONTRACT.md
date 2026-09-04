# P1 Method, Data, and Implementation Contract

**Stage:** `p1_v2_s03_method_data_implementation_contract`  
**Status:** evidence-bound retrospective specification; no new experiment and no claim upgrade  
**Machine-readable authority:** `method_implementation_contract.json`  
**Executable consistency check:** `python manuscript/reconstruction_v2/validate_method_contract.py`

This document fixes the semantics used by the equations, pseudocode, archived
configuration, stage-local analysis code, and manuscript. The archived main-run
configuration is not rewritten: it did not serialize all implementation
constants, ties, event fields, or objective-call counts. The JSON contract
records those evidence-supported semantics retrospectively and labels missing
state rather than presenting the legacy configuration as a complete replay
contract.

## Objective, Unit, and Budget Contract

For scenario-local candidate positions (j=1,\ldots,n), (x_j\in\{0,1\}).
The minimized vector is

\[
F(x)=\left(\sum_j k_jx_j,-\sum_j r_jx_j,-\sum_j g_jx_j,
\bar\rho(x),-\bar q(x)\right),
\]

where the empty-portfolio conventions are \(\bar\rho=1\) and \(\bar q=0\).
Cost \(k_j\), total cost, and budget (B) share **synthetic cost units**.
The remaining coordinates are proxy indices. None is currency, energy, outage
cost, realized benefit, or return. The hard constraint and dimensionless
violation are

\[
\sum_j k_jx_j\le B,\qquad
v_B(x)=\max\{0,(\sum_j k_jx_j-B)/B\}.
\]

The nominal budget is 1160 synthetic units; `budget_ranking_stability` uses
0.88 times that amount. This exception changes the feasible proxy set, not the
meaning or unit of cost.

## Repair, Normalization, Preference, and Ties

Repair repeatedly drops the selected item minimizing

\[
s_j=(r_j+g_j+\ell_j+q_j)/\max(k_j,1).
\]

These inputs are not normalized. Selected positions are enumerated in ascending
order and first-`argmin` therefore drops the smallest pool-local position in an
exact tie. The rule is deterministic conditional on portfolio and pool order;
it is a proxy heuristic, not a calibrated benefit--cost ratio.

Preference selection uses generation-local union minima and ranges with a
(10^{-9}) range floor and no clipping. Reported hypervolume instead uses
fixed method-independent per-scenario bounds, clipping to [0,1], and reference
point (1.1,...,1.1). The two normalizations are not interchangeable.

The full method uses eight weights and penalty 10. Its first weight maps scenario
cost, reliability, renewable, risk, and combined compliance-plus-evidence
weights; load support is not a fifth-objective coordinate. Seven weights are
Dirichlet samples. Every five generations, componentwise absolute Gaussian
perturbation (scale 0.1) is followed by L1 normalization. Reselection begins
from one seeded-uniform candidate and greedily maximizes response dispersion;
`argmax` resolves exact dispersion ties by first occurrence. Preference best
response also uses first-`argmin`. When the response row is absent after
environmental selection, one seeded-uniform selected slot is replaced; later
weights may evict earlier restorations.

Environmental selection admits constraint-dominated fronts and truncates the
last front by descending crowding distance. No authored secondary crowding-tie
criterion exists, so executed NumPy ordering is part of the preserved behavior,
not a scientific preference. Equal genotypes may occupy separate search rows;
only the feasible returned rows are lexicographically deduplicated before final
front evaluation.

## Evaluation Accounting and Event Semantics

TRACE-MOEA, NSGA-II, and R-NSGA-II share nominal population 40 and 40 generation
labels. MOEA/D uses 35 directions. Because archived rows omit `n_eval`, this is
not evidence of equal objective-call budgets. Deterministic rules do not share a
stochastic evaluation budget. The stochastic analysis unit remains one seeded
method--scenario run; a deterministic rule contributes one unique
method--scenario output.

Each executed drop appends `repair_drop(gen,event,item)`. Each of eight weights
appends `preference_elite(gen,event,pref,items)` in every one of 40 generations,
whether or not replacement occurred. Thus the full-method count is

\[
|A|=D+8\times40=D+320.
\]

The released table contains only total count, repair-drop count (as
`local_move_count`), and whole-run set co-occurrence

\[
|U_A\cap U_{\mathcal P}|/\max(1,|U_{\mathcal P}|).
\]

Events are quarantined from objectives, constraints, repair score, preference
score, environmental selection, and hypervolume. Missing stable IDs, ordered
payloads, replacement flags, evictions, parentage, snapshots, and retained
weight indices preclude chronology, lineage, replay, causal, auditability, and
human-value claims.

## Canonical Pseudocode

```text
sample 40 binary rows; repair each row and append one repair_drop per drop
initialize one mapped scenario weight and seven Dirichlet weights
for generation 1..40:
    create 40 children; repair and append repair_drop records
    concatenate parents then children
    select 40 union-row indices by constraint NDS and crowding truncation
    normalize objectives on this union only, without clipping
    for weights 0..7 in order:
        best = first argmin(weighted normalized objectives + 10*violation)
        if best union-row index is absent, replace a seeded-uniform selected slot
        append preference_elite regardless of whether replacement occurred
    every fifth generation, perturb and greedily reselect weights
    retain exactly the selected 40 rows
deduplicate feasible returned rows; evaluate their nondominated front
release count and pool-position co-occurrence summaries, not ordered payloads
```

## Cross-Artifact Consistency

| Semantic item | Manuscript | Machine config | Code check | Preserved limitation |
|---|---|---|---|---|
| Objectives and units | Sections 3.1 and 4 | `objectives`, `budget` | objective and empty-case assertions | synthetic/proxy only |
| Repair and ties | Sections 4.3 and 4.5 | `repair` | first-tie assertion | no economic calibration |
| Two normalizations | Sections 4 and 5.2 | `normalization` | clipped/unclipped assertions | ranking is normalization-sensitive |
| Preference injection | Sections 4.2 and 4.5 | `preference` | count/cadence invariant | isolated effect unresolved |
| Evaluation accounting | Sections 4.6 and 5.1 | `evaluation_accounting` | `n_eval_archived=false` | no equal-call claim |
| Event records | Section 4.4 | `event_records` | 8x40 invariant | count/co-occurrence only |

`experiments/p5_s3_matched_sensitivity/config.json` and its outputs remain
historical evidence and are not modified by this contract. Its analysis code
already uses the five named objective coordinates and distinguishes clipped
reported evaluation from unclipped sensitivity schemes. The executable checker
above verifies only semantic consistency and creates no result table.

## Validation-Asset Usability Decisions

| Layer | Legal/provenance decision | Technical decision | Claim decision |
|---|---|---|---|
| Traceable cost | **NO-GO.** No source-specific licence/redistribution record for a candidate-level cost corpus exists in this worktree. | **NO-GO.** No candidate-to-cost-record mapping or currency/base-year transform exists. | Keep synthetic units; no actual return or calibrated cost-effectiveness claim. |
| AC/OPF | Source URLs do not by themselves document permission for redistribution of a derived validation package; a stage-local licence manifest is absent. | **NO-GO.** Candidate bits denote archetype proxies, not bus/branch/generator/topology/dispatch actions. | Budget feasibility only; no AC, OPF, N-1, or electrical-feasibility claim. |
| NERC/MTEP16 public records | Official records may be cited by URL; source PDFs/portal extracts are not approved here for redistribution. Derived summaries remain bounded to recorded provenance. | **GO, DESCRIPTIVE ONLY.** Existing checks retain source reuse, label imbalance, and portfolio-dependence limitations and no confirmatory randomization family. | Descriptive external consistency only; no return, above-chance, causal, external-validity, or deployment claim. |

These are present-evidence decisions, not permanent legal opinions. A future GO
requires a source-level licence/provenance manifest and an executable mapping
from each selected decision variable to the validating record or network action,
frozen before outcomes are inspected.
