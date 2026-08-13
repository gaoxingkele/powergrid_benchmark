# P6 Three-Round Scientific Closure

This record separates the three requested reviews before synthesizing their closures. It introduces no new experiment run, label, dataset, or numerical result. Numerical statements below are limited to the retained artifacts under `experiments/p6_s3_matched_effort/`.

## Round 1 — Logic Review

### Findings

1. **Objective equation mismatch — corrected.** `PortfolioProblem.objectives` assigns risk objective 1 to the empty portfolio, while the prior manuscript expression evaluated it as 0. The piecewise expression in Section 3.1 of `manuscript/MANUSCRIPT.md` now states the implemented convention.
2. **Legacy-to-metered BiLo equivalence — scope corrected.** `run_custom_ea` in the shared legacy source freezes normalization bounds before repair and uses a `1e-9` denominator floor. `run_bilo` in `experiments/p6_s3_matched_effort/run_experiments.py` freezes bounds after child repair and uses `1e-12`. Section 5.4 and the experiment README now identify the matched runner as a stage-local variant; the frozen result archive was not rewritten to imply equivalence.
3. **Claim chain — aligned.** The title identifies the mechanism, while the abstract, results, discussion, and conclusion retain the observed loss to matched NSGA-II, win over PLS, and mixed equal-time result. No superiority conclusion is drawn.
4. **Trace semantics — bounded.** The legacy trace stores accepted-event counts and project-position co-occurrence. It is not lineage, replay, causal attribution, or a complete audit trail. The matched runner reports accepted-move and repair counts but does not evaluate the legacy event-log artifact itself.

### Logic verdict

The two material specification mismatches are closed by an equation correction and an explicit implementation-scope limitation. The matched archive remains evidence for the metered stage-local runner only.

## Round 2 — Methodology and Statistics Review

### Findings

1. **Primary estimand and analysis unit — retained.** The primary comparison is the paired seed-level hypervolume difference within scenario under an exact 3200-unit objective-evaluation budget. Runs are the analysis units; individual front points are not independent replicates.
2. **Compute fairness — bounded claim.** `EvaluationLedger` counts one four-objective candidate evaluation per unit, including locally scored proposals. It does not charge repair, sorting, control flow, or equalize generations and neighborhood opportunities. The equal-time protocol supplies a complementary computational estimand.
3. **Inference — internally consistent.** The retained analysis uses common seeds, exact paired sign tests, one Holm adjustment across the primary 16-contrast family, and a separate Holm adjustment across the secondary 16-contrast family. The artifact reports paired mean and median differences without adding an unsupported interval claim. The manuscript preserves four adjusted losses and no wins against NSGA-II under the exact budget, plus the mixed equal-time result.
4. **Joint intervention and interactions — scope corrected.** The depth cells jointly change forward/backward caps to `(2, 2)`, `(8, 4)`, and `(16, 8)`. They do not isolate either cap. The one-factor scan cannot estimate interactions among depth, penalty, and bonus.
5. **Hypervolume — stress-tested, not absolute.** Reported, expanded, and analytic normalization bounds retain the ordering NSGA-II > BiLo-NSGA > PLS, while absolute scale and gaps change. The claim is limited to ordering stability under the implemented conventions.
6. **Baseline feasibility — qualified.** BiLo-NSGA and PLS construct or repair candidates. The matched NSGA-II has constraint-domination but no repair. Its final feasibility of 1.0 is observed across retained runs and is not a guaranteed property of its variation operators.

### Methodology-statistics verdict

The statistical conclusions are supported at the paired-run level. Compute fairness, feasibility, sensitivity, and hypervolume claims are now limited to what their protocols observe.

## Round 3 — Theory and Innovation Review

### Findings

1. **Innovation boundary — narrowed.** The paper claims a particular integration of project-level move grammar, generation-frozen scalar acceptance, and a bounded event schema. It does not claim that local search, repair, or hybrid evolutionary search is new.
2. **Literature scope — bounded.** Universal statements about all knapsack or grid MOEAs were replaced with claims about the cited/reviewed studies. No frontier-performance claim is made.
3. **Companion overlap — disclosed.** Shared benchmark assets, normalizers, and legacy implementation provenance are recorded. This paper's independent contribution is the matched-effort archive, statistical analysis, hypervolume sensitivity, and bounded trace interpretation. Full textual-overlap and venue-policy clearance remains a human check because the complete companion submission was not available in this isolated worktree.
4. **Visual semantics — checked.** Figure 1's caption now matches its lower elements. Figure 8's shared legend was moved outside the data panels. Proposed, comparator, and ablation encodings remain consistent across the generated figure set.

### Theory-innovation verdict

The supported contribution is an integration and evaluation contribution with explicit provenance, not a universal novelty or superiority claim. Companion-text clearance remains unresolved and is recorded as a human blocker.

## Issue Closure Matrix

| Issue | Observable evidence | Closure |
|---|---|---|
| Compute fairness | `EvaluationLedger`, Section 5.4, exact- and equal-time artifacts | Closed by two estimands and an explicit accounting boundary |
| Equation–code | `PortfolioProblem.objectives`, `run_custom_ea`, `run_bilo`, Section 3.1, Section 5.4 | Closed by correction and stage-local variant disclosure |
| Interaction | local sensitivity config and Section 6.8.3 | Closed by joint-only and no-interaction language |
| Trace | legacy `trace_metrics`, Sections 4.6 and 7 | Closed by bounded, non-causal scope |
| Hypervolume | `experiments/p6_s3_matched_effort/runs/primary_v1/hypervolume_sensitivity_*`, Section 6.8.3 | Closed for the implemented normalization conventions |
| Baseline feasibility | runner baseline definitions and final-feasibility artifacts | Closed as an empirical, not constructive, result |
| Companion overlap | `manuscript/DEEP_REVISION_EVIDENCE.md`, shared-provenance records | Scientifically scoped; textual/venue clearance remains human-blocked |
| Visual consistency | `manuscript/figures/make_figures.py`, generated figure directories | Closed after regeneration, visual inspection, and cross-directory hash verification |

## Verification Status

- `manuscript/figures/make_figures.py` completed after verifying all 16 manifest sources and regenerated 13 derived tables and nine figures.
- `harness_scientific_acceptance.py --project mintou_p6_bilonsga_project_review --phase full` passed when the repository `src` directory was supplied on `PYTHONPATH`.
- `harness_acceptance.py --project mintou_p6_bilonsga_project_review --allow-human-placeholders` was run but did not complete: the installed MiKTeX reports an unfinished fresh setup and cannot invoke `pdflatex` within the permitted workspace. The regenerated `paper.tex` exists, but the retained `paper.pdf` predates it, so current-PDF integrity is not claimed.
- The required manuscript, evidence, manifest, trace map, matched-run validation, review record, generated TeX, and all numbered figure copies exist in the worktree.
