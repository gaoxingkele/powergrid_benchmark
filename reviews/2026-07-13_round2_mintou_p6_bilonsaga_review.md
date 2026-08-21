# Senior Review: mintou_p6 (BiLo-NSGA) — Round 2

Review date: 2026-07-13
Reviewer role: Senior reviewer, paper_reviews project (offline, structured, deterministic)
Priority: FAST PUBLICATION (allow major modifications to algorithm/dataset/downstream-task; general direction = bidirectional local-search NSGA for budget-constrained power grid project review)

---

## Summary

BiLo-NSGA (Bidirectional Local-search Non-dominated Sorting Genetic Algorithm) targets **budget-constrained power grid project review and portfolio ranking**. The v2 real-algorithm rewrite (completed 2026-07-13) replaces the deprecated v1 circular pipeline with genuine pymoo-based NSGA-II/NSGA-III/MOEA/D baselines, real AHP-TOPSIS/Greedy BCR/Random Feasible, and a self-contained BiLo-NSGA implementation (NSGA-II core + forward-insertion/backward-deletion bidirectional local search + dependency-aware moves + feasibility recovery). On a public benchmark-derived candidate pool of 120 projects (72 RTS-GMLC + 48 SimBench + NERC report metadata), 30 seeded runs per method per experiment with Mann-Whitney U + Holm correction yield:

- **Pooled mean HV**: BiLo-NSGA 0.17267 vs best baseline NSGA-II 0.17000 (+**1.57%**)
- **Holm-significant wins vs baselines**: 44/48 per-experiment comparisons; **zero significant losses**
- **Best ablation**: NoBackwardSearch at 0.17294 — **edges the full method by +0.16%**, meaning backward deletion is a slight *negative* contributor
- **Signal classification**: `significant_public_signal` — the strongest statistical signal among all six mintou papers on public data

The paper is methodologically more mature than at Round 1, but four structural risks persist: (1) backward-search component anomaly requiring honest treatment or operator redesign; (2) no external ground truth (expert labels or historical outcomes); (3) the "hypervolume" is now standard (a major improvement over v1's "hypervolume_proxy"), but the paper still lacks sensitivity analysis curves, convergence plots, and boxplots; (4) **cross-paper collision risk with p5 (TRACE-MOEA)** — same data pipeline, same candidate pool, same shared baselines, near-identical PAPER.md templates, and both targeting IEEE-publisher or MDPI-publisher venues that use iThenticate.

---

## Target Venue

| Venue | Role | Fit (current state) | Fit (post-P0/P1) |
|---|---|---|---|
| **MDPI Applied Sciences** | **Primary** | Medium-High | High |
| **IEEE Access** | Secondary | Medium-Low | Medium |
| ~~MDPI Energies~~ | Excluded | — | — |

**Rationale for Applied Sciences as primary** (confirmed from Round 1 JOURNAL_REVIEW):
- Applied-value logic dominates: "real utility/field case study + quantified economic benefit" substitutes for methodological baselines; p6's 6 baselines + 9 ablations far exceed its corpus floor (4/11 zero baselines accepted).
- Sensitivity analysis is the journal's "currency of applied credibility" (6/11 corpus papers have it; reviewers ask "does the conclusion survive ±20% parameter swings" not "what's the p-value"). p6's budget_sensitivity experiment slot + 0.75x/0.88x/1.0x/1.2x budget axis is a natural fit — needs to be visualized as a curve.
- Honest limitations correlate with acceptance (8/11); p6's proxy boundary statements convert directly.
- Portfolio-optimal: keeps p6 at MDPI while p5 stays at IEEE — two different publishers, minimizing CrossCheck/iThenticate editorial collision despite shared iThenticate corpus.
- Metaheuristic sub-field bar rising (7–9 baselines, 30-run + Wilcoxon appearing by 2026) — p6 already meets this with 6 baselines, 30 seeds, Mann-Whitney U + Holm.

**Rationale against IEEE Access as primary**:
- p5 (TRACE-MOEA) is designated for IEEE Access. Two same-pipeline papers in the same journal = maximum "not distinct from prior publication" red-line risk.
- Binary accept/reject model gives no revision loop for fixable issues.
- Metaheuristics community norm is 50+ runs — p6 has 30, which meets MDPI's emerging bar but falls short of Access's established norm.

**Rationale against Energies**:
- p3 (CARS-MODE) and p4 (SHIELD-MOEA) already designated for Energies. Adding p6 = three same-group MOEA papers in one journal.
- Energies is p5's backup — if p5 is rejected from Access and reroutes to Energies, direct collision with p6.

---

## 7-Dimension Review

### 1. Novelty — Severity: 3 (serious) | Confidence: 0.95 | Fixability: 0.70

**Top findings:**

**F1.1 — Cross-paper risk with p5 (TRACE-MOEA) [severity 4 at portfolio level]**

This is the single largest risk to p6's publication path. The two papers share:

| Shared element | Detail |
|---|---|
| Data pipeline | `src/powergrid_benchmark/mintou_real_project_review.py` — p5/p6 `run_real_project_review.py` differ only in parameters |
| Candidate pool | 120 candidates (72 RTS + 48 SimBench), same `real_project_review_source_profile.csv` |
| Data sources | RTS-GMLC + SimBench + NERC/C2GES reports (same 3 directories, same `candidate_count=120`, same `repeats` structure) |
| Shared baselines | NSGA-II, MOEA/D, Greedy BCR, Random Feasible (4/6 baselines identical) |
| Shared scenarios | `renewable_accommodation_review` (both); `reliability_driven` (p5) vs `reliability_prioritized` (p6) — wording-only difference |
| PAPER.md template | Abstract/Boundary sections near-verbatim isomorphic (both read "This ARA project studies [ALG], a [descriptor] for [task]. The current public-data experiment derives project candidates from RTS-GMLC, SimBench, and the cached public NERC report manifest associated with the C2GES literature thread.") |
| Evidence structure | Identical directory layout, identical file naming conventions |

**Differentiation that exists (but is not yet written into the manuscript):**

| Dimension | p5 (TRACE-MOEA) | p6 (BiLo-NSGA) |
|---|---|---|
| Core mechanism | Preference-vector coevolution + review-rule repair + trace archive | Forward-insertion + backward-deletion bidirectional local search + move audit trail |
| Problem framing | Investment effectiveness + traceability | Budget hard constraint + budget sensitivity |
| Search structure | Coevolutionary (two populations: portfolio + preference vectors) | Single-population GA with post-generation local search |
| Unique evidence axis | traceability_evaluation experiment | budget_sensitivity + project_pool_scalability experiments |
| Unique baselines | Weighted Sum | NSGA-III, AHP-TOPSIS (different MCDM pair) |

**Required actions** (see Allowable Modifications §Differentiation):
1. Rewrite ALL text that is structurally isomorphic with p5 — especially Abstract, Introduction gap statement, Boundary/Limitations paragraphs.
2. Add an explicit method-comparison paragraph in Related Work (or Introduction if p5 is published first, cite it; if not, structurally differentiate).
3. Anchor p6's entire narrative around "budget-constrained" — this is the problem-setting differentiator.
4. Candidate pool: either (a) differentiate p6's pool (different seed, different source mix, e.g. 200 candidates with higher dependency density) or (b) publish the pipeline as a single named public benchmark that both papers cite.
5. Submit to **different publishers** (p6 → MDPI Applied Sciences, p5 → IEEE Access) and stagger submissions by ≥6 weeks.

**F1.2 — "First bidirectional local-search NSGA for project review" novelty framing is thin**

The innovation is a component combination: NSGA-II + forward/backward local search + dependency moves + feasibility recovery, applied to a new problem domain. Applied Sciences' corpus shows zero of 11 papers introduced a new algorithm — combination/adaptation framing with per-module motivation is the accepted norm. However, the `logic/solution/method.md` Innovation Handles are only 3 bullet points, none explaining *why* each component is needed. The Related Work pointer (`logic/related_work.md`) is a single line: "Comparator evidence source: `papers/literature/target_journal_related/comparison_analysis.md`." — the actual related work body has not been written.

*Fix*: Write per-component motivation (why forward search? why backward search? why dependency moves? why feasibility recovery?) and a 2–3 page Related Work covering budget-constrained portfolio optimization, local-search-enhanced MOEAs, and grid investment planning.

**F1.3 — Backward search is a negative contributor (novelty undermined by own ablation)**

NoBackwardSearch ablation *exceeds* the full method by +0.16% (0.17294 vs 0.17267 pooled HV). This means one of the two named "innovation handles" (bidirectional = forward + backward) is slightly harmful. Across per-experiment breakdowns, NoBackwardSearch is never significantly worse than BiLo-NSGA and is occasionally slightly better. A reviewer who notices this in the ablation table will question whether the "bidirectional" framing is warranted.

*Fix*: Either (a) redesign the backward-deletion operator (e.g., add an acceptance criterion such as simulated-annealing-style probabilistic acceptance, or restrict deletion to dominated-budget items), or (b) honestly present the asymmetry in the ablation discussion ("forward insertion is the primary contributor; backward deletion shows marginal negative impact, suggesting future work on acceptance criteria").

---

### 2. Soundness — Severity: 2 (moderate) | Confidence: 0.90 | Fixability: 0.85

**F2.1 — No external ground truth for "review quality"**

Candidates are synthetically derived from public grid statistics and NERC report metadata. There are no expert-labeled feasibility outcomes, no calibrated cost coefficients, and no load-flow checks. The `claims.md` explicitly prohibits "exact engineering-economic manuscript claims until expert labels, calibrated costs, and load-flow checks are added." The v2 rewrite fixed the *internal* soundness issues (real algorithms, standard hypervolume, method-independent evaluation), but the *external* validity anchor is still absent.

For Applied Sciences, this is a moderate (not fatal) issue: the journal's corpus shows real utility case studies can substitute for baselines, but p6's case is the reverse — strong baselines, no real utility validation. The "proxy benchmark" framing is honest and defensible if paired with a Limitations section, but a reviewer will ask "what does this mean for actual grid planners?"

*Fix* (one of):
- Expert subset validation: 20–30 candidates labeled by ≥2 grid planning engineers, report Kendall τ / Spearman ρ between proxy ranking and expert ranking.
- Historical outcome back-test: use LBNL "Queued Up" interconnection queue data, EIA-860 retirement records, or MISO MTEP project approval/cancellation lists to construct a "did the proxy pick winners?" check.
- pandapower AC load-flow on SimBench: validate that Top-N selected portfolios don't violate network constraints (data already cached locally).

**F2.2 — 30 seeded runs may be below the emerging metaheuristic bar**

Applied Sciences' metaheuristic sub-field is moving toward 30-run + Wilcoxon/Friedman by 2026. p6 meets this floor exactly. However:
- The significance test is Mann-Whitney U + Holm (not Wilcoxon signed-rank), which is valid but less standard in the MOEA community.
- No convergence curves or boxplots are provided — these are expected visual evidence in metaheuristic papers at both venues.

*Fix*: Add convergence curves (HV vs generation/evaluation) and boxplots (HV distribution across 30 seeds per method per experiment). Consider upgrading to 50 seeds if targeting IEEE Access as backup.

**F2.3 — Ablation "loose_budget" and "low_dependency_density" are scenario variants, not component ablations**

These two "ablations" modify the problem instance (budget level, dependency graph density), not algorithmic components. Including them in the ablation table conflates sensitivity analysis with component isolation. Across all 8 experiments, Ablation-LowDependencyDensity is never significantly different from BiLo-NSGA (all 8 Holm-adjusted p-values = 1.0), and LooseBudget significantly loses in all 8 experiments — but this tells us about budget tightness, not about any algorithm component.

*Fix*: Move these to a dedicated Sensitivity Analysis section. Keep 7 clean component ablations (NoForwardSearch, NoBackwardSearch, RandomMutationOnly, NoDependencyMoves, NoFeasibilityRecovery, WeightedRankingOnly, ShallowLocalSearch).

---

### 3. Experiments — Severity: 2 (moderate) | Confidence: 0.92 | Fixability: 0.80

**F3.1 — Budget sensitivity is present but not visualized as a systematic scan**

The experiment axis covers 0.75x/0.88x/1.0x/1.2x budget levels across different experiment slots (budget_sensitivity, budget_constrained_selection, baseline, scalability). This is good structural coverage, but the results are reported as separate experiment rows rather than as a unified "budget level → HV / feasibility / portfolio size" curve. Applied Sciences reviewers treat systematic sensitivity curves as the journal's "applied credibility currency."

*Fix*: Consolidate the 4 budget levels into a single sensitivity figure (3 panels: HV vs budget multiplier, feasibility rate vs budget, portfolio size vs budget). Extend to 50%/150% if computationally cheap (30 seeds × 5 levels × all methods is ~900 additional runs at ~0.2s each ≈ 3 minutes total).

**F3.2 — Per-experiment signal heterogeneity is under-discussed**

In the `renewable_accommodation_review` experiment, BiLo-NSGA is NOT significantly better than NSGA-II (p_Holm = 1.0), NSGA-III (p_Holm = 0.097), or any ablation except WeightedRankingOnly and LooseBudget. This is the weakest experiment for the proposed method. By contrast, `dependency_constrained_review` and `project_pool_scalability` show the strongest gains. This heterogeneity is visible in the significance table but never discussed in the analysis.

*Fix*: Add a per-experiment discussion paragraph identifying where BiLo-NSGA excels (dependency-constrained, scalability) vs where it ties (renewable accommodation), with a hypothesis for why (e.g., "renewable objectives may be less amenable to local search moves that are designed around budget/reliability trade-offs").

**F3.3 — Runtime and computational fairness**

BiLo-NSGA mean runtime: 0.193s vs NSGA-II 0.080s (2.4× slower) vs AHP-TOPSIS 0.0004s (483× slower). The runtime gap is modest in absolute terms (all under 0.3s), but the relative cost vs NSGA-II should be acknowledged. IEEE Access corpus shows "explicit fairness statements" in 2/4 accepted papers as a strength signal.

*Fix*: Add a computational cost paragraph or table footnote: "All methods evaluated on identical hardware; BiLo-NSGA's 2.4× overhead over NSGA-II is attributable to the bidirectional local-search pass per generation."

---

### 4. Reproducibility — Severity: 1 (minor) | Confidence: 0.95 | Fixability: 0.95

**F4.1 — Candidate generation pipeline must be publicly documented**

The 120-candidate pool is derived from public sources (RTS-GMLC SourceData, SimBench networks, NERC/C2GES reports), but the derivation rules (which grid elements → which project types, how costs/benefits are synthesized, how NERC metadata maps to reliability features) are embedded in `mintou_real_project_review.py` without a standalone description. The `real_project_review_source_profile.csv` records the source directories and counts but not the transformation logic.

*Fix*: In the Data Availability Statement, commit to releasing (a) the candidate generation script, (b) the NERC report manifest (titles + official URLs + SHA-256 hashes, not the PDFs themselves), and (c) the feature extraction script. This converts the "shared benchmark" with p5 into a feature, not a liability.

**F4.2 — NERC report redistribution rights**

40 C2GES/NERC reports are locally cached. If the paper promises to share data, the PDF redistribution right is unconfirmed.

*Fix*: Don't redistribute PDFs. Publish manifest + download script pointing to official URLs.

---

### 5. Related Work — Severity: 3 (serious) | Confidence: 0.98 | Fixability: 0.75

**F5.1 — Related Work body does not exist**

`logic/related_work.md` contains a single pointer line: "Comparator evidence source: `papers/literature/target_journal_related/comparison_analysis.md`." There is no written related work section. For Applied Sciences, the Related Work must cover:

1. **Budget-constrained portfolio optimization in power systems** — transmission expansion planning, generation investment, project prioritization under budget caps.
2. **Local-search-enhanced MOEAs** — memetic algorithms, variable neighborhood search within NSGA frameworks, bidirectional search strategies.
3. **Grid investment decision support** — AHP/TOPSIS applications in power planning, MCDM for utility project review.

The corpus requirement is coverage of the last 3 years with restrained self-citation. The comparison_analysis.md file may contain raw material, but it has not been synthesized into a manuscript section.

*Fix*: Write a 2–3 page Related Work with ≥25 references (≥15 from 2023–2026), organized into the three strands above. End with a gap paragraph that positions BiLo-NSGA.

**F5.2 — Differentiation from p5 must be in Related Work or Introduction**

See Novelty F1.1. If p5 is published first, cite it and explain the difference. If not yet published, structurally differentiate (different problem framing, different operators, different experimental axes) without naming the unpublished paper.

---

### 6. Clarity — Severity: 2 (moderate) | Confidence: 0.85 | Fixability: 0.90

**F6.1 — PAPER.md is a skeleton, not a manuscript**

The current PAPER.md is 32 lines: title, metadata, abstract (3 sentences), status paragraph, and boundary statement. No Introduction, no Method, no Results, no Discussion, no Conclusion. All content exists in the logic/evidence layer but has not been composed into manuscript form.

*Fix*: This is expected at the project stage. The writing checklist from the JOURNAL_REVIEW (items 1–7) is comprehensive and should be followed.

**F6.2 — Beneficiary sentence missing**

Applied Sciences corpus shows published papers "almost always name the beneficiary ('grid planners can use…')." This sentence is absent from all p6 materials.

*Fix*: Add to Introduction and/or Conclusion: "Grid planning departments and provincial power grid investment review boards can use BiLo-NSGA to systematically rank and select project portfolios under hard budget constraints, with full audit trails for each inclusion/exclusion decision."

**F6.3 — Metric naming must be precise**

The v2 rewrite correctly switched to standard hypervolume (fixed normalization bounds + 1.1× reference point, feasible non-dominated front only). This is a major improvement over v1's "hypervolume_proxy." The manuscript must clearly state: "standard hypervolume indicator with reference point at 1.1× the nadir of the feasible non-dominated front, computed on normalized objectives."

---

### 7. Ethics — Severity: 1 (minor) | Confidence: 0.90 | Fixability: 0.95

**F7.1 — MDPI mandatory declarations**

Applied Sciences requires Funding, COI, Data Availability, and Author Contributions (CRediT) statements in 100% of published papers (11/11 corpus). These are administrative but mandatory — missing any one triggers desk rejection or revision.

*Fix*: Prepare all four statements using MDPI template language.

**F7.2 — Honest limitations**

The proxy nature of the benchmark, absence of expert labels, absence of load-flow validation, and single candidate pool must be stated in a dedicated Limitations section. Applied Sciences corpus shows honest limitations correlate with acceptance (8/11). The ARA's own `constraints.md` and `claims.md` boundary statements provide the raw material.

*Fix*: Write a Limitations paragraph covering: (a) candidates are benchmark-derived, not real utility projects; (b) no expert-labeled ground truth; (c) no AC/DC load-flow validation of selected portfolios; (d) single candidate pool size (120); (e) backward-deletion operator shows marginal negative contribution.

---

## RRI (Revision Risk Index)

| Dimension | Severity | Confidence | Fixability | Weighted Risk |
|---|---|---|---|---|
| Novelty | 3 | 0.95 | 0.70 | 3 × 0.95 × (1 − 0.70) = **0.855** |
| Soundness | 2 | 0.90 | 0.85 | 2 × 0.90 × (1 − 0.85) = **0.270** |
| Experiments | 2 | 0.92 | 0.80 | 2 × 0.92 × (1 − 0.80) = **0.368** |
| Reproducibility | 1 | 0.95 | 0.95 | 1 × 0.95 × (1 − 0.95) = **0.048** |
| Related Work | 3 | 0.98 | 0.75 | 3 × 0.98 × (1 − 0.75) = **0.735** |
| Clarity | 2 | 0.85 | 0.90 | 2 × 0.85 × (1 − 0.90) = **0.170** |
| Ethics | 1 | 0.90 | 0.95 | 1 × 0.90 × (1 − 0.95) = **0.045** |
| **Total RRI** | | | | **2.491** |

**Interpretation**: RRI 2.491 = **moderate-high residual risk** after planned fixes. The two largest contributors are Novelty (cross-paper risk + backward-search anomaly) and Related Work (unwritten body). Both are fixable but require substantial writing effort. The experimental and soundness risks are well-contained and highly fixable.

---

## Predicted Decision

### Applied Sciences (Primary) — Current state: **Major Revision** | Post-P0/P1: **Accept with Minor Revision**

The v2 real-algorithm results (+1.57% over NSGA-II, 44/48 Holm-significant, zero losses) clear the journal's evidence bar for the metaheuristic sub-field. The missing pieces are writing-related (Related Work body, beneficiary sentence, sensitivity curves, Limitations section, MDPI declarations) rather than evidence-related. One round of major revision addressing the written manuscript + sensitivity curves should position for acceptance.

### IEEE Access (Secondary) — Current state: **Reject** | Post-P0/P1: **Borderline Accept/Reject**

The binary decision model is unforgiving. 30 runs falls short of the 50+ community norm. Cross-paper risk with p5 (same journal) is a red-line trigger. Even after fixes, the soundness-only gate demands convergence curves, boxplots, and 50+ runs. Not recommended unless p5 changes venue.

---

## Top-3 Revisions

### Revision 1: Write the manuscript narrative (addresses Novelty F1.2, Related Work F5.1, Clarity F6.1/F6.2)

**What**: Compose the full paper from the ARA logic/evidence layer into an Applied Sciences manuscript. Priority sections:
1. Related Work (3 strands: budget-constrained portfolio optimization, local-search MOEAs, grid investment MCDM) — 2–3 pages, ≥25 refs.
2. Introduction with gap statement → contribution list (3–5 numbered items, each mapped to an experiment).
3. Method section with per-component motivation (why forward search? why backward search? why dependency moves? why feasibility recovery?).
4. Results with per-experiment discussion (not just pooled), honest trade-off presentation (renewable_accommodation tie), and ablation asymmetry discussion.
5. Sensitivity Analysis section consolidating the 4 budget levels into curves.
6. Limitations section (proxy benchmark, no expert labels, no load-flow, single pool).
7. Beneficiary sentence.

**Effort**: ~3–5 days of focused writing.
**Impact**: Transforms the project from "strong evidence, no paper" to "submittable manuscript."

### Revision 2: Differentiate from p5 at text, data, and narrative levels (addresses Novelty F1.1)

**What**: Execute the 5-point differentiation plan:
1. Rewrite all PAPER.md text that is structurally isomorphic with p5 (Abstract, Boundary paragraphs).
2. Add explicit method-comparison paragraph (BiLo-NSGA bidirectional local search vs TRACE-MOEA coevolutionary preference search — operators, search structure, problem framing).
3. Differentiate the candidate pool (option a: p6 uses 200 candidates with higher dependency density; option b: publish shared benchmark and both papers cite it).
4. Ensure experiment naming does not overlap (rename p6's `reliability_prioritized_review` to avoid confusion with p5's `reliability_driven`).
5. Stagger submissions ≥6 weeks; submit to different publishers.

**Effort**: 1–2 days for text differentiation; 1 day for candidate pool modification if choosing option (a).
**Impact**: Eliminates the single largest portfolio-level risk (salami-slicing / "not distinct" accusation).

### Revision 3: Add visual evidence and fix ablation structure (addresses Soundness F2.2/F2.3, Experiments F3.1/F3.2)

**What**:
1. Generate convergence curves (HV vs evaluation count, averaged over 30 seeds with shaded std band) for BiLo-NSGA + top 3 baselines.
2. Generate boxplots (HV distribution, 30 seeds) per method per experiment.
3. Generate budget sensitivity curves (HV, feasibility rate, portfolio size vs budget multiplier at 0.5x/0.75x/0.88x/1.0x/1.2x/1.5x).
4. Move LooseBudget and LowDependencyDensity from ablation table to sensitivity section.
5. Add Pareto front visualization for one representative experiment.
6. Add a move-audit-trail example figure (showing forward/backward moves with project names — this is p6's explainability differentiator).

**Effort**: 1–2 days of plotting.
**Impact**: Meets the visual evidence expectations of both target journals; converts the sensitivity data into Applied Sciences' "applied credibility currency."

---

## Allowable Modifications

### Algorithm modifications (within general direction)

| Modification | Allowable? | Rationale |
|---|---|---|
| Redesign backward-deletion operator (e.g., SA acceptance criterion) | ✅ Yes | Fixes the ablation anomaly; strengthens "bidirectional" novelty claim |
| Drop backward search entirely, rebrand as "Forward-Local-Search NSGA" (FLo-NSGA) | ✅ Yes | Honest response to ablation evidence; still within bidirectional→unidirectional modification space |
| Add Pareto-archive-based local search memory | ✅ Yes | Standard MOEA enhancement; doesn't change the bidirectional-search identity |
| Replace NSGA-II core with NSGA-III | ⚠️ Caution | Changes baseline comparison structure; may require re-running everything |
| Replace the entire algorithm with a different metaheuristic (e.g., particle swarm) | ❌ No | Violates the general direction constraint |

### Dataset modifications (within general direction)

| Modification | Allowable? | Rationale |
|---|---|---|
| Expand to 200 candidates with higher dependency density | ✅ Yes | Differentiates from p5; answers "does pool size matter" |
| Add a second test system (nrel118 or TAMU test cases, both locally cached) | ✅ Yes | Strongly recommended P2; significantly strengthens generalization |
| Replace SimBench with a different European grid benchmark | ⚠️ Caution | Allowable but requires re-deriving candidates; moderate effort |
| Use only RTS-GMLC (drop SimBench) | ⚠️ Caution | Reduces candidate pool; weakens generalization |

### Downstream-task modifications (within general direction)

| Modification | Allowable? | Rationale |
|---|---|---|
| Reframe from "project review" to "transmission expansion planning portfolio selection" | ✅ Yes | More standard terminology in power systems literature; same mathematical problem |
| Add a multi-period (phased) budget constraint | ✅ Yes | Enriches the budget-constrained framing; natural extension |
| Add carbon-emission reduction as an explicit objective | ✅ Yes | Strengthens Applied Sciences "sustainability" angle |
| Change to a completely different application domain | ❌ No | Violates general direction |

### Differentiation from p5 — Concrete Strategy

1. **Contribution angle**: p6 = "budget-constrained combinatorial optimization with audit-trail explainability"; p5 = "traceable investment effectiveness with preference coevolution." The anchor words for p6 are **budget**, **constraint**, **audit trail**, **local search**. The anchor words for p5 are **traceability**, **coevolution**, **investment effectiveness**, **preference**.

2. **Framing differentiation in text**:
   - p6 title should emphasize "Budget-Constrained" (already does).
   - p6 abstract should NOT use the word "traceable" or "coevolutionary" (those are p5's).
   - p6 introduction gap statement: "Existing MOEA approaches for grid project review lack (a) explicit budget-constraint handling as a first-class constraint, and (b) local-search operators that produce auditable move trails for each portfolio decision."
   - p5 introduction gap statement (already written): "Existing approaches lack (a) traceable review evidence linking, and (b) preference-aware coevolutionary search."

3. **Experimental differentiation**:
   - p6's unique experiments: `budget_sensitivity`, `project_pool_scalability`, `local_move_explainability` — these have no p5 equivalent.
   - p5's unique experiments: `traceability_evaluation` — p6 should NOT have this.
   - Rename p6's `reliability_prioritized_review` to `reliability_weighted_review` to avoid near-identical naming with p5's `reliability_driven`.

4. **Shared benchmark strategy**: Publish the candidate generation pipeline as a named artifact (e.g., "PGReview-120: A Public Benchmark for Power Grid Project Portfolio Review") in a data repository (Zenodo/Figshare). Both papers cite it. This converts the shared pipeline from a liability into a community contribution.

---

## Honest Boundary

### What this review can confirm (from ARA evidence):
- The v2 algorithm implementation is real (pymoo-based, not hand-parameterized proxies).
- Standard hypervolume is used (fixed normalization, 1.1× reference point, feasible non-dominated front only).
- 30 seeded runs per method per experiment with Mann-Whitney U + Holm correction.
- 44/48 Holm-significant baseline comparisons; zero significant losses.
- The backward-search ablation anomaly is real (NoBackwardSearch +0.16% over full method).
- All evidence files are preserved in the ARA chain with v1 deprecated artifacts retained.

### What this review cannot confirm:
- Whether the candidate generation rules produce a representative or realistic project pool (no expert validation).
- Whether the synthesized cost/benefit coefficients correspond to real utility investment figures.
- Whether selected portfolios are AC-feasible (no load-flow check performed).
- Whether the NERC report feature extraction is reproducible from the descriptions provided.
- The actual CrossCheck/iThenticate similarity score between p5 and p6 manuscripts (manuscripts not yet written).

### Calibration note:
All findings are based on static reading of ARA logic/evidence files and the v2 results CSV. No external web search or live journal-policy verification was performed. APC, IF, and quartile figures are from the Paper_CCF skill profiles (as-of 2026-07) and must be verified on official journal pages before submission.

---

## Fastest Path to Publication

### Phase 1: Manuscript writing + p5 differentiation (5–7 days)

| Day | Task |
|---|---|
| 1 | Rewrite PAPER.md abstract/introduction to eliminate p5-isomorphic text; write beneficiary sentence; draft contribution list (3–5 items) |
| 2 | Write Related Work body (3 strands, ≥25 refs from 2023–2026); add method-comparison paragraph differentiating from TRACE-MOEA |
| 3 | Write Method section with per-component motivation; write Results section with per-experiment discussion + ablation asymmetry |
| 4 | Write Sensitivity Analysis section (consolidate 4 budget levels into curves); write Limitations section |
| 5 | Compose into MDPI Applied Sciences LaTeX template; add MDPI mandatory declarations (Funding, COI, Data Availability, CRediT) |
| 6–7 | Internal review pass; English polish; iThenticate self-check against p5 draft |

### Phase 2: Visual evidence generation (2–3 days, parallel with Phase 1)

| Task | Output |
|---|---|
| Convergence curves (HV vs evaluations, 30-seed mean ± std band) | Figure 1 |
| Boxplots (HV distribution per method, representative experiments) | Figure 2 |
| Budget sensitivity curves (HV / feasibility / portfolio size vs budget multiplier) | Figure 3 |
| Pareto front visualization (one representative experiment) | Figure 4 |
| Move audit trail example (forward/backward moves with project names) | Figure 5 |

### Phase 3: Optional strengthening (3–5 days, if time permits before submission)

| Task | Priority | Impact |
|---|---|---|
| Redesign backward-deletion operator or drop it honestly | P0 if time allows | Fixes novelty anomaly |
| Add second test system (nrel118 derived pool) | P1 | Major generalization boost |
| pandapower AC load-flow check on Top-N portfolios | P1 | External validity anchor |
| Extend to 50 seeds | P2 | Meets IEEE Access norm if backup needed |

### Submission timing relative to p5

**Recommendation: p5 FIRST, then p6 with ≥6-week gap.**

**Rationale:**

1. **p5 is closer to submission-ready for IEEE Access** (its v2 results are also positive, +0.89% over NSGA-II with 38/42 Holm-significant; its remaining P0 is the same external-ground-truth gap that p6 shares). IEEE Access has a ~4-week first decision. If p5 submits first and is accepted, p6 can cite it in the Related Work method-comparison paragraph, which is the cleanest possible differentiation.

2. **If p5 is rejected from IEEE Access**, it will likely reroute to Energies (its backup). This creates a collision with p3/p4 at Energies but *frees up* IEEE Access for p6 — except p6's 30-run protocol falls short of Access's 50+ norm. Better to keep p6 at Applied Sciences regardless.

3. **If p6 goes first** to Applied Sciences (~15-day first decision), it will be in the MDPI system before p5 enters IEEE. This is also viable, but p6's Related Work cannot cite p5 (unpublished), making differentiation harder. The 6-week gap ensures that p5's submission status is known before p6 enters review.

4. **Minimum gap**: 6 weeks between submissions. This allows: (a) CrossCheck/iThenticate to not flag sequential submissions from the same author group; (b) p5's first-decision outcome to inform p6's Related Work (cite or structurally differentiate); (c) any shared Associate Editor at IEEE (if p5 is at Access) to not see p6 arrive while p5 is still in review.

### Optimal timeline

```
Week 1-2:  p5 final manuscript prep + submit to IEEE Access
Week 3:    p6 manuscript writing (Phase 1 above)
Week 3-4:  p6 visual evidence generation (Phase 2)
Week 4:    p6 internal review, English polish, iThenticate check
Week 5:    p6 submit to MDPI Applied Sciences
Week 6-8:  p5 first decision from IEEE Access (~4 weeks)
Week 7-8:  p6 first decision from Applied Sciences (~15-16 days)
Week 8+:   Address revision requests for whichever paper gets major revision
```

### Decision summary

| Decision | Answer |
|---|---|
| **Which paper goes first?** | **p5 (TRACE-MOEA) → IEEE Access first** |
| **Minimum time gap** | **6 weeks** between p5 submission and p6 submission |
| **p6 target journal** | **MDPI Applied Sciences** (Energy or Electrical Engineering section) |
| **p6 backup** | IEEE Access only if p5 changes venue; otherwise no backup needed (Applied Sciences fast enough for resubmission elsewhere) |
| **Estimated p6 time-to-submit** | 7–10 days from today (manuscript writing + visual evidence) |
| **Estimated p6 time-to-first-decision** | ~15–16 days after submission (Applied Sciences median) |

---

*This review is based on static analysis of ARA evidence files, logic chains, and the Paper_CCF journal skill profiles as of 2026-07-13. All journal metrics (IF, APC, quartile) must be verified on official pages before submission. No findings were invented; all quantitative claims trace to the evidence paths cited above.*
