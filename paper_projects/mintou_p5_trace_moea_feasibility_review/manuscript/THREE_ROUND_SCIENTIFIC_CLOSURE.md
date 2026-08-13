# P5 Three-Round Scientific Closure

Stage: `p5_s5_three_round_closure`

This record closes the logic, methodology--statistics, and theory--innovation
reviews against the preserved implementation, accepted configuration, run
tables, sensitivity outputs, and manuscript. It creates no new experimental
observation. Null, adverse, and near-miss results remain in scope.

## Evidence Boundary

The evidence supports performance on a five-objective, hard-budget public proxy,
implemented run-level event counts, and final-front candidate-position
co-occurrence. It does not support expert-validated review accuracy, AC/OPF
feasibility, engineering economics, project-level lineage or replay, human
preference validity, review benefit, or deployment effectiveness.

## Round 1: Logic Review

Disposition: internally consistent after bounded corrections.

- Title, abstract, contribution, method, results, discussion, and conclusion use
  the same proxy-search and run-level co-occurrence claim boundary.
- Preference-best-response records are emitted whether or not replacement occurs;
  the reported count is therefore not an injection, eviction, or causal-impact
  count. Pool-local set overlap is not chronology, lineage, replay, explanation
  quality, or human value.
- The three objective-hiding conditions also change the first scenario-derived
  preference-vector mapping because the implementation truncates four leading
  entries instead of remapping weights to surviving objective indices. They are
  combined-configuration controls. Their contrasts cannot isolate reliability,
  renewable, or schedule-risk contributions.
- `NoPreferenceRanking` remains the direct preference-layer ablation.
  `NSGA2Only` remains a joint removal of review-specific components.
- The companion P6 study shares benchmark and execution infrastructure, but its
  mechanism, runs, outputs, comparisons, and claims do not provide evidence for
  P5 effects.

## Round 2: Methodology--Statistics Review

Disposition: the reported estimands and analysis units are matched; remaining
limitations are explicit.

- The primary stochastic estimand is the within-scenario difference in feasible
  full-front hypervolume between TRACE-MOEA and one named comparator. One seeded
  method--scenario run is the analysis unit; pooled cross-scenario means are
  descriptive.
- Twelve stochastic comparisons are Holm-corrected within each scenario. The
  seven scenario contrasts for a named mechanism/configuration receive a second
  Holm correction where reported. This multiplicity correction does not convert
  a combined control into an isolated component estimand.
- The displayed first-sample Mann--Whitney statistic was corrected to
  $U_1=\sum_i R_i-n_1(n_1+1)/2$. The archived computation already uses the
  library statistic and is unchanged; no p-value, effect size, or conclusion was
  recomputed for this notation correction.
- AHP-TOPSIS, Weighted Sum, and Greedy BCR have one unique output per scenario.
  Their repeated provenance rows have effective sample size one and receive no
  inferential p-values.
- The matched-output estimand is one shared-rule compromise portfolio per run (or
  one unique deterministic output), not full-front hypervolume. The matched-budget
  study uses one seeded method--budget run. Sensitivity cells are descriptive and
  have no p-values.
- The normalization audit retains 9.79% clipping under the reported empirical
  bounds, the deterministic-rule ordering reversal under other bounds, and the
  absence of a normalization-invariant cross-family superiority claim.
- Equal objective-evaluation counts are not claimed because the run archive does
  not retain `n_eval` and MOEA/D uses 35 directions while the principal methods
  use population 40.

## Round 3: Theory--Innovation Review

Disposition: innovation is limited to the measured integration under the proxy
contract; no isolated or human-behavior theory is asserted.

- Adaptive preference elitism is an algorithmic design hypothesis. No interaction
  study validates it as a model of elicited stakeholder preference or reviewer
  behavior.
- The direct `NoPreferenceRanking` effect is small (0.17% pooled difference) and
  unresolved after the seven-scenario correction (minimum adjusted $p=0.0722$).
  The sensitivity scan retains positive, adverse, and near-null cells, including
  the adverse maximum-risk formulation and the near-null compliance-share
  comparison.
- The `NoScheduleRisk` combined control has an adverse within-scenario contrast
  that misses the second correction ($p=0.0510$). The result is retained and is
  not interpreted as an isolated schedule-risk mechanism.
- TRACE-MOEA's independent contribution is the tested combination of constrained
  portfolio search, adaptive preference elitism, deterministic repair, and
  quarantined run-level event summaries. Shared candidate generation, corpora,
  benchmark utilities, and public-record backtest infrastructure are disclosed
  and are not claimed as independent novelty.
- NERC and MTEP16 analyses remain descriptive external-consistency diagnostics.
  They are not expert labels, deployment evidence, or confirmatory portfolio-level
  validation.

## Cross-Round Closure Matrix

| Requirement | Disposition | Preserved limitation |
|---|---|---|
| Consistent method contract | Closed | Objective-hiding runs are combined controls; comparator defaults are incompletely serialized. |
| Matched estimands | Closed | Full-front, matched-output, event, public-record, and sensitivity estimands remain separate. |
| Bounded preference claims | Closed | Direct effect unresolved; no human-preference validation. |
| Bounded trace claims | Closed | Counts and pool-position co-occurrence only; no stable-ID lineage or replay. |
| Scenario-blocked statistics | Closed | Pooled values descriptive; deterministic rules effective $n=1$. |
| Sensitivity evidence | Closed | Adverse and near-null cells retained; update cadence and several parameters untested. |
| Companion disclosure | Closed | Shared infrastructure disclosed; paper-specific evidence is non-interchangeable. |
| Current artifact manifest | Closed for this worktree | Manifest hashes bind the reviewed sources and regenerated closure artifacts, not scientific truth beyond their contents. |

## Negative and Near-Miss Outcomes Retained

- Four of seven TRACE-MOEA versus NSGA-II scenario contrasts are not significant;
  the distribution-scenario mean difference is nominally negative.
- The preference-layer ablation remains unresolved after cross-scenario correction.
- The combined schedule-risk control's adverse cell remains just outside the
  second correction.
- Deterministic-rule rankings change under normalization variants.
- Sensitivity includes adverse and near-null full-front and matched-output cells.
- Public-record checks remain descriptive and label-limited.

## Unresolved Human and Scientific Blockers

- Authors must confirm CRediT roles, funding/APC information, ORCIDs,
  correspondence details, repository/DOI, and companion-manuscript status.
- Expert labels, stable-ID ordered event payloads with replay state, a human
  trace-utility study, calibrated costs, and AC/OPF checks are absent. Stronger
  review-effectiveness, deployment, economic, lineage, or electrical-feasibility
  claims remain blocked.

Closure verdict: the scientific narrative is aligned with the preserved proxy
evidence and its null/near-miss outcomes. Submission metadata and the stronger
human, deployment, lineage, economic, and electrical claims remain unresolved.
