# Review: mintou_p5 (TRACE-MOEA) — Round 2 Comprehensive Assessment

**Review date:** 2026-07-13
**Reviewer role:** Senior reviewer, paper_reviews project
**Paper:** "Hybrid Multi-Objective Evolution for Traceable Power Grid Feasibility Review and Investment Effectiveness Optimization"
**Algorithm:** TRACE-MOEA (Traceable Review-Aware Coevolutionary Multi-Objective Evolution)
**Priority:** FAST PUBLICATION — major modifications to algorithm/dataset/downstream-task permitted within the general direction (traceable MOEA for power grid project review + investment effectiveness)

---

## Summary

P5 (TRACE-MOEA) addresses traceable multi-objective feasibility review for power grid investment portfolios. After the v1 pipeline was invalidated (hand-parameterized method proxies, circular metrics — `JOURNAL_REVIEW.md` §II), a v2 rewrite has been completed with real algorithm implementations (pymoo NSGA-II/MOEA/D, genuine AHP-TOPSIS, self-contained TRACE-MOEA with preference coevolution + budget repair + decision archive), method-independent standard hypervolume evaluation, 30 seeded runs per method/experiment, and Mann-Whitney U + Holm correction (`evidence/tables/real_project_review_significance.csv`). The v2 signal is `positive_but_partially_significant`: TRACE-MOEA achieves pooled mean HV 0.17425 vs NSGA-II 0.17270 (+0.89%), with 38/42 per-experiment baseline comparisons Holm-significant. However, the strongest ablation (NoScheduleRisk) trails by only 0.13% and significantly *outperforms* TRACE-MOEA in the traceability_evaluation experiment (p_holm=0.022), exposing weak component-level contribution from the preference-coevolution mechanism. The critical remaining gap is external ground truth (P0-3): no expert labels, no historical project outcome validation, no calibrated costs.

**Cross-paper risk with p6 (BiLo-NSGA) is the most dangerous submission-level issue** — identical data pipeline, identical 120-candidate pool, 4 shared baselines, overlapping scenario names, and near-identical PAPER.md abstracts create a "not distinct from prior publication" red line at IEEE Access and salami-slicing exposure at any publisher.

---

## Target Venue

| | IEEE Access (primary) | MDPI Applied Sciences (secondary) |
|---|---|---|
| **Fit (current)** | Medium-Low | Medium |
| **Fit (after P0-3 + P1)** | Medium | Medium-High |
| **Decision model** | Binary Accept/Reject — no revision loop | 1–2 revision rounds possible |
| **First decision** | ~4 weeks | ~15–16 days |
| **APC** | US$2,160 | CHF 2,400 |
| **Key barrier** | Metaheuristics community norm: 50+ runs + Wilcoxon + convergence/boxplots; "not distinct from prior publication" red line (p5+p6 same publisher risk) | Sensitivity analysis near-mandatory (missing = top major-revision trigger); beneficiary sentence required; p3/p4 already at Energies + p6 at AppSci creates portfolio clustering |

**Recommendation:** Given FAST PUBLICATION priority, **MDPI Applied Sciences is the more pragmatic first target** for three reasons: (1) its 15–16 day first decision is 2× faster than IEEE Access; (2) the revision-round model allows digesting "add sensitivity analysis" feedback, whereas Access's binary gate gives no recovery room; (3) Applied Sciences' applied-value logic tolerates proxy benchmarks with quantified benefit framing, while Access's metaheuristics sub-community expects 50+ runs. **IEEE Access should be held in reserve** for after p6 is published or withdrawn from Access consideration, to avoid the "not distinct" collision. If the author insists on Access first, the statistical package must be expanded to 50+ seeds and the p6 differentiation package (Section below) must be completed before submission.

---

## 7-Dimension Review

### 1. Novelty

| # | Finding | Severity | Confidence | Fixability |
|---|---|---|---|---|
| N1 | **"Coevolutionary" mechanism has negligible marginal contribution.** The NoScheduleRisk ablation (which removes the schedule-risk component) trails TRACE-MOEA by only 0.13% in pooled HV and *significantly outperforms* it in the traceability_evaluation experiment (mean 0.17579 vs 0.17521, p_holm=0.022 — `evidence/tables/real_project_review_significance.csv` row 92). The NoPreferenceRanking ablation is only 0.17% behind. The preference co-evolution mechanism — the core algorithmic novelty claim — does not demonstrate clear added value over the NSGA-II backbone with budget repair alone. | 3 | 0.92 | 0.60 |
| N2 | **Incremental differentiation from NSGA-II is thin.** TRACE-MOEA vs NSGA-II: +0.89% pooled HV, but not Holm-significant in 2/7 experiments (benchmark_portfolio_optimization p_holm=0.064, reliability_driven_review p_holm=0.242). In distribution_project_review, NSGA-II actually edges TRACE-MOEA (0.16512 vs 0.16491, not significant). For a paper whose contribution is "a new MOEA," the failure to consistently beat the vanilla NSGA-II backbone across all scenarios is a serious novelty weakness. | 3 | 0.88 | 0.55 |
| N3 | **Cross-paper risk with p6 (BiLo-NSGA) — "not distinct" exposure.** See dedicated Section below. Shared data pipeline, shared candidate pool, shared baselines, overlapping scenarios, near-identical abstract templates. | 4 | 0.95 | 0.70 |

**Evidence paths:**
- N1: `evidence/tables/real_project_review_significance.csv` rows 92 (traceability_evaluation: NoScheduleRisk wins), 8, 5, 22 (non-significant vs NoScheduleRisk/NoFeasibilityRepair/NSGA2Only in benchmark_portfolio_optimization)
- N2: `evidence/tables/real_project_review_significance.csv` rows 13 (benchmark_portfolio_optimization vs NSGA-II p_holm=0.064), 27 (budget_ranking_stability vs NSGA-II p_holm=0.053), 41 (distribution_project_review NSGA-II ahead, not sig.)
- N3: `papers/mintou/portfolio_status.md`, cross-comparison of p5/p6 PAPER.md abstracts

### Cross-paper risk with p6 (BiLo-NSGA)

**Shared infrastructure (confirmed from ARA evidence):**

| Shared element | p5 | p6 | Source |
|---|---|---|---|
| Data pipeline | `mintou_real_project_review.py` `run_paper` | Same function, different params | `mintou_p6_bilonsga_project_review/JOURNAL_REVIEW.md` §I point 3 |
| Candidate pool | 120 (72 RTS + 48 SimBench) | 120 (72 RTS + 48 SimBench) | `evidence/source/real_project_review_source_profile.csv` (identical for both) |
| NERC reports | 40 documents, 28 event reports | Same | `CACHE_STATUS.md` |
| Baselines (shared) | NSGA-II, MOEA/D, Greedy BCR, Random Feasible | NSGA-II, MOEA/D, Greedy BCR, Random Feasible | Both leaderboards |
| Strongest baseline | NSGA-II (v2) | NSGA-II (v2) | Both `real_project_review_analysis.md` |
| AHP-TOPSIS | Yes | Yes | Both leaderboards |
| Scenario overlap | renewable_accommodation_review | renewable_accommodation_review | Both `logic/experiments.md` |
| Scenario near-duplicates | reliability_driven_review | reliability_prioritized_review | Naming only — `JOURNAL_REVIEW.md` §I |
| Abstract template | Near-identical sentence structure | Near-identical sentence structure | Both `PAPER.md` Abstract/Boundary paragraphs |
| Evaluation code | Shared v2 rewrite | Shared v2 rewrite | `portfolio_status.md` P5/P6 entries |
| `repeats` config | 4 (v1), 30 (v2) | 4 (v1), 30 (v2) | Both `real_project_review_config.json` |

**Concrete differentiation strategy:**

1. **Contribution angle (must be made explicit in both papers):**
   - p5 = **"traceability + investment effectiveness"**: the contribution is a review framework where decision-trace linkage and preference-aware ranking support auditable investment decisions. The *traceability* is the novelty, not the MOEA itself.
   - p6 = **"budget-constrained combinatorial optimization"**: the contribution is a bidirectional local-search mechanism (forward insertion / backward deletion / dependency-aware moves) for hard-budget portfolio selection. The *local search operators* are the novelty.
   - Both papers must state these angles in Introduction and Related Work, with a paragraph explicitly contrasting the two approaches. If p5 is published first, p6 cites it; if not, both must structurally avoid each other's phrasing.

2. **Framing differentiation in titles/abstracts:**
   - p5 title should anchor on "Traceable Decision Support" (not "Hybrid Multi-Objective Evolution" — which is indistinguishable from p6's "Non-Dominated Sorting with Bidirectional Local Search")
   - p5 abstract must eliminate every sentence that also appears in p6's abstract (currently both use "This ARA project studies... The current public-data experiment derives project candidates from RTS-GMLC, SimBench, and the cached public NERC report manifest...")

3. **Candidate pool differentiation:**
   - **Option A (preferred):** Publish the candidate-generation pipeline as a single named public benchmark ("RTS-SimBench-NERC Review Benchmark v1"), cited by both papers. This converts shared infrastructure into a strength.
   - **Option B:** p5 uses a different pool configuration (e.g., 80 candidates with higher reliability-feature density, or a different RTS/SimBench split ratio) to reduce overlap.
   - Option A is more defensible but requires coordination; Option B is faster.

4. **Timing gap:**
   - Minimum **8–10 weeks** between submissions (see Fastest Path section).
   - CrossCheck/iThenticate share corpora across IEEE and MDPI — same-publisher collision is worst, but cross-publisher is also detectable.

5. **Recommended submission order:** **p6 first → p5 second.**
   - Rationale: p6 has the stronger statistical signal (`significant_public_signal`, +1.57% over NSGA-II, 44/48 Holm-significant, zero significant losses) and is already targeted at Applied Sciences (MDPI). Publishing p6 first establishes the "shared benchmark" precedent and gives p5 a citable reference. p5's weaker signal (+0.89%, partially significant) benefits from being the "follow-up that adds traceability" rather than the "first paper that barely beats NSGA-II."

### 2. Soundness

| # | Finding | Severity | Confidence | Fixability |
|---|---|---|---|---|
| S1 | **No external ground truth.** Expert labels, calibrated costs, and load-flow checks are all absent (`claims.md`: "Exact engineering-economic manuscript claims remain prohibited until expert labels, calibrated costs, and load-flow checks are added"). The entire "feasibility review" claim rests on standard hypervolume computed over proxy objectives derived from grid-case statistics. A reviewer asking "does this actually identify feasible projects?" has no answer. | 4 | 0.97 | 0.50 |
| S2 | **Preference coevolution may be adding noise.** In traceability_evaluation, the NoScheduleRisk ablation significantly outperforms the full method (p_holm=0.022). If the coevolution mechanism is the novelty, its removal *improving* performance in one scenario is a direct soundness challenge to the core claim. The honest interpretation is that the coevolution adds marginal-to-negative value in some contexts — this must be reported, not hidden. | 3 | 0.88 | 0.65 |
| S3 | **No load-flow validation of selected portfolios.** The top-N project portfolios selected by TRACE-MOEA have never been checked for AC power-flow feasibility (no pandapower, no OPF). A portfolio that optimizes proxy objectives but violates network constraints is not "feasible" in any engineering sense. `portfolio_status.md` lists this as an outstanding item for p5. | 3 | 0.90 | 0.75 |

**Evidence paths:**
- S1: `logic/claims.md` prohibition clause; `evidence/runs/real_project_review_analysis.md` "Interpretation Boundary" section
- S2: `evidence/tables/real_project_review_significance.csv` row 92
- S3: `portfolio_status.md` P5 entry ("OPF/UC needed" absent; load-flow check listed as future work)

### 3. Experiments

| # | Finding | Severity | Confidence | Fixability |
|---|---|---|---|---|
| E1 | **30 seeds is below metaheuristics community norm for IEEE Access.** The Access skill profile explicitly states: "metaheuristics papers ship 50+ independent runs + Wilcoxon/Friedman + convergence/boxplots" (SKILL.md, Distilled review standards). Current 30 seeds meets a minimum but falls short of the Access metaheuristics bar. For Applied Sciences, 30 seeds is acceptable (the skill notes 30-run protocols are only "appearing by 2026" in its metaheuristic sub-field). | 2 | 0.85 | 0.90 |
| E2 | **No sensitivity analysis.** Zero systematic parameter sweeps: no budget-level scan, no objective-weight grid, no candidate-pool-size variation. This is near-fatal for Applied Sciences (sensitivity analysis is "the journal's currency of applied credibility" — SKILL.md) and a significant gap for Access. The p6 review notes that budget sensitivity at 0.75x/0.88x/1.0x/1.2x is partially built into its experiment axis; p5 has no equivalent. | 3 | 0.95 | 0.85 |
| E3 | **No convergence curves or boxplots.** Standard visualization for MOEA papers in both target venues. Convergence curves demonstrate that the algorithm actually converges (not just that it lands at a good point by luck); boxplots show distribution shape beyond mean±std. Both are expected by metaheuristics reviewers at Access and are strong加分 at Applied Sciences. | 2 | 0.88 | 0.95 |

**Evidence paths:**
- E1: `evidence/tables/real_project_review_leaderboard.csv` (runs=210 = 7 experiments × 30 seeds)
- E2: `logic/experiments.md` — no sensitivity experiment slots defined; `JOURNAL_REVIEW.md` §V row 8 confirms "无"
- E3: `evidence/figures/README.md` (empty — no figures generated)

### 4. Reproducibility

| # | Finding | Severity | Confidence | Fixability |
|---|---|---|---|---|
| R1 | **Code and configuration are structurally reproducible.** The v2 rewrite provides real algorithm implementations, seeded runs, config files, and a complete evidence trail. Public data sources (RTS-GMLC, SimBench, NERC reports) are identified. The v1 deprecated pipeline is preserved. This is a strength. | 0 | 0.90 | N/A |
| R2 | **NERC report feature-extraction pipeline not fully scripted.** 40 NERC/C2GES reports are locally cached, but the extraction from PDF → `evidence_score` features may involve manual steps. The JOURNAL_REVIEW.md §VI.2 recommends publishing a "manifest (title + official URL + SHA-256) + automated fetch script + feature extraction script" — this has not been done. | 2 | 0.80 | 0.85 |
| R3 | **No Data Availability Statement, Author Contributions, Funding, or COI declarations prepared.** Both target journals require these (MDPI 100% hard gate; Access reproducibility initiative strongly encouraged). | 2 | 0.95 | 0.95 |

**Evidence paths:**
- R1: `src/code/run_real_project_review.py`, `src/configs/real_project_review_config.json`, `evidence/README.md`
- R2: `JOURNAL_REVIEW.md` §VI.2; `evidence/source/real_project_review_source_profile.csv`
- R3: Not present in any ARA artifact

### 5. Related Work

| # | Finding | Severity | Confidence | Fixability |
|---|---|---|---|---|
| RW1 | **Related work is effectively absent.** `logic/related_work.md` contains only a one-line pointer to `papers/literature/target_journal_related/comparison_analysis.md` and a project-separation note. No literature review body exists. For both target journals, a 1.5–3 page Related Work covering (a) MOEA for power system planning, (b) traceable decision support / audit trails in engineering review, (c) project portfolio optimization under uncertainty is required. | 4 | 0.95 | 0.80 |
| RW2 | **No explicit differentiation from p6 in Related Work.** Even if the related work is written, it must include a paragraph positioning TRACE-MOEA against BiLo-NSGA (or the general class of local-search-enhanced NSGA variants) — otherwise reviewers who encounter both papers will flag insufficient differentiation. | 3 | 0.90 | 0.85 |

**Evidence paths:**
- RW1: `logic/related_work.md` (full content: 2 lines)
- RW2: Cross-reference of p5 and p6 `logic/solution/method.md` — Innovation Handles are 3 lines each, no cross-citation

### 6. Clarity

| # | Finding | Severity | Confidence | Fixability |
|---|---|---|---|---|
| CL1 | **PAPER.md is a skeleton, not a manuscript.** Current content is ~32 lines of metadata + abstract + status. No Introduction, Method, Results, Discussion, or Conclusion sections exist. While this is an ARA project file (not a submission manuscript), the distance from current state to submission-ready manuscript is substantial — likely 3–4 weeks of writing for a first-time author. | 3 | 0.90 | 0.75 |
| CL2 | **Method name overclaims.** "Coevolutionary" implies two or more co-evolving populations; the v2 implementation has a preference-vector update every 5 generations based on best-response dispersion (`JOURNAL_REVIEW.md` progress update). This is adaptive preference weighting, not coevolution. Reviewers familiar with cooperative/coevolutionary MOEA literature (e.g., Keim et al., Goh et al.) will flag the mismatch. | 2 | 0.92 | 0.90 |
| CL3 | **Abstract template overlap with p6.** Both PAPER.md abstracts share near-identical sentences: "This ARA project studies [ALGO]... The current public-data experiment derives project candidates from RTS-GMLC, SimBench, and the cached public NERC report manifest..." — this is a CrossCheck trigger and must be rewritten independently. | 3 | 0.95 | 0.95 |

**Evidence paths:**
- CL1: `papers/mintou/mintou_p5_trace_moea_feasibility_review/PAPER.md` (full content read)
- CL2: `logic/solution/method.md` Innovation Handles; `JOURNAL_REVIEW.md` progress update describing preference-vector update
- CL3: Direct comparison of p5 and p6 `PAPER.md` Abstract sections

### 7. Ethics

| # | Finding | Severity | Confidence | Fixability |
|---|---|---|---|---|
| ET1 | **v1 deprecation is handled honestly.** The circular v1 pipeline is preserved as `*_v1_deprecated_circular.*` artifacts, and the v2 analysis explicitly documents why v1 was invalidated. The evidence-retention discipline (constraints.md: "Keep every result table in evidence/") is strong. This is a genuine ethical strength. | 0 | 0.95 | N/A |
| ET2 | **Weak component contribution must be transparently reported.** The ablation evidence shows the coevolutionary component adds marginal-to-negative value (NoScheduleRisk ablation wins in one scenario). If the manuscript presents TRACE-MOEA's contribution as primarily due to coevolution without acknowledging this, it would be a misrepresentation. The JOURNAL_REVIEW.md already flags this; it must carry through to the manuscript's Discussion section. | 2 | 0.88 | 0.90 |
| ET3 | **No IRB/ethics considerations needed** — the work uses only public data (RTS-GMLC, SimBench, NERC reports) and involves no human subjects, proprietary data, or dual-use technology. | 0 | 0.98 | N/A |

**Evidence paths:**
- ET1: `evidence/tables/real_project_review_leaderboard_v1_deprecated_circular.csv`, `evidence/runs/real_project_review_analysis_v1_deprecated_circular.md`
- ET2: `evidence/tables/real_project_review_significance.csv` row 92

---

## RRI (Revision Readiness Index)

| Dimension | Score (0-4) | Weight | Weighted |
|---|---|---|---|
| Novelty | 1.5 | 0.20 | 0.30 |
| Soundness | 1.5 | 0.20 | 0.30 |
| Experiments | 2.0 | 0.15 | 0.30 |
| Reproducibility | 2.5 | 0.10 | 0.25 |
| Related Work | 0.5 | 0.10 | 0.05 |
| Clarity | 1.5 | 0.15 | 0.225 |
| Ethics | 3.0 | 0.10 | 0.30 |
| **Composite RRI** | | | **1.73 / 4.00** |

**Interpretation:** RRI 1.73 = "early-stage, substantial work required before submission." The paper has strong bones (real algorithm v2, honest evidence trail, public data) but is missing critical manuscript components (related work, sensitivity analysis, external validation, written manuscript) and faces a serious cross-paper differentiation challenge.

---

## Predicted Decision

| Venue | Current state | After P0-3 + P1 completion |
|---|---|---|
| **IEEE Access** | **Reject** (soundness: no external ground truth, statistics below metaheuristics norm, "not distinct" risk if p6 also submitted) | **Borderline Accept/Reject** — depends on whether 50+ seeds + external validation + convergence plots clear the binary gate |
| **MDPI Applied Sciences** | **Major Revision** (missing sensitivity analysis, beneficiary sentence, data statements; related work absent) | **Minor Revision → Accept** — if sensitivity analysis + beneficiary framing + honest limitations are added |

---

## Top-3 Revisions

### Revision 1: External Ground Truth Anchor (P0-3) — severity 4, fixability 0.50

**What:** Add at least one external validation anchor to break the "proxy-on-proxy" loop.

**Three options ranked by feasibility:**
1. **Historical outcome back-validation (highest feasibility):** Use LBNL "Queued Up" interconnection queue data (publicly available) to construct a subset of candidates with known outcomes (completed / withdrawn / delayed). Compute Spearman ρ between TRACE-MOEA's portfolio ranking and actual project completion rates. Even a 20–30 project subset with ρ > 0.3 would substantially strengthen the validity claim.
2. **NERC-event rule-based validation (medium feasibility):** The 28 cached NERC event reports identify real reliability incidents by region/type. Construct a rule: "projects addressing regions/types with documented NERC events should be prioritized." Report whether TRACE-MOEA's top-ranked portfolios align with this rule-based priority.
3. **Expert panel (lowest feasibility, highest value):** 2–3 power grid planners rate 30–60 candidates on feasibility/priority; report inter-rater Kappa and Spearman correlation with proxy ranking.

**Effort:** Option 1: ~2 weeks (data download + matching). Option 2: ~1 week (already have reports). Option 3: ~4–6 weeks (recruitment + IRB if applicable).

### Revision 2: Sensitivity Analysis Section (P1-6) — severity 3, fixability 0.85

**What:** Three-dimensional sensitivity sweep:
- **Budget axis:** 50% / 75% / 100% / 125% / 150% of baseline budget → plot HV, feasibility rate, portfolio size curves
- **Objective-weight grid:** systematically vary the weight between reliability, renewable, and cost objectives → show Pareto-front stability
- **Candidate pool size:** 60 / 90 / 120 / 150 candidates → show conclusion robustness to pool scale

**Why:** This is the single highest-ROI revision for Applied Sciences (near-mandatory, top major-revision trigger when absent) and a strong加分 for Access. It also naturally differentiates p5 from p6: p5's sensitivity story is about *preference stability* (how do traceability metrics change under weight perturbation?) while p6's is about *budget feasibility* (how does the portfolio change under budget stress?).

**Effort:** ~1–2 weeks (modify config to add budget/weight/pool sweep dimensions, run experiments, generate plots).

### Revision 3: Related Work + Manuscript Writing (P1-9, P2-10) — severity 4, fixability 0.80

**What:** Write the full manuscript with:
1. **Related Work (2–3 pages):** Three threads: (a) MOEA for power system planning/portfolio optimization — cite NSGA-II/MOEA/D applications in power systems, AHP-TOPSIS in energy MCDM; (b) traceable/auditable decision support — cite explainable AI, decision-archive approaches; (c) project review under uncertainty — cite interconnection queue studies, LBNL/EIA empirical work. Include explicit paragraph differentiating TRACE-MOEA from local-search-enhanced NSGA variants (i.e., the p6 class of methods).
2. **Numbered contribution list (3–5 items, Access convention):**
   - C1: A reproducible public benchmark for traceable power grid feasibility review (RTS-GMLC + SimBench + NERC-derived)
   - C2: TRACE-MOEA: preference-adaptive MOEA with decision-trace archive for auditable portfolio selection
   - C3: Empirical validation on 7 review scenarios with 6 baselines and 8 ablations, 30-seed statistical protocol
   - C4: Honest assessment of component contributions (preference coevolution adds marginal value; budget repair is the primary driver)
3. **Limitations section:** No expert labels, no load-flow validation, proxy objectives, single candidate pool, coevolution contribution weak — Access rewards honesty ("honest limitations win").
4. **Beneficiary sentence (Applied Sciences requirement):** "Grid planning departments and provincial power grid investment review boards can use this framework to generate auditable, trace-ranked portfolio recommendations from public reliability data."

**Effort:** ~3–4 weeks for first complete draft.

---

## Allowable Modifications (including "differentiation from p6" strategy)

The FAST PUBLICATION priority permits major modifications as long as the general direction (traceable MOEA for power grid project review + investment effectiveness) is preserved. Below is the full modification space ranked by impact/effort:

### A. Differentiation from p6 (P0-level, must-do)

| Strategy | Description | Effort | Impact |
|---|---|---|---|
| **A1: Shared benchmark declaration** | Publish the 120-candidate generation pipeline as "RTS-SimBench-NERC Project Review Benchmark v1" with a persistent identifier (Zenodo DOI). Both p5 and p6 cite it as a shared benchmark contribution. Converts a risk into a strength. | 1 week | Very high — eliminates "secret shared data" suspicion |
| **A2: Title/abstract complete rewrite** | p5 title → "Traceable Decision Support for Power Grid Investment Review: A Preference-Adaptive MOEA with Audit Archive on a Public Benchmark" (anchors on traceability, not "hybrid evolution"). Abstract rewritten from scratch, zero sentence overlap with p6. | 2 days | High — CrossCheck/iThenticate risk reduction |
| **A3: Problem framing divergence** | p5 = "How can investment review decisions be made traceable and auditable using public reliability evidence?" (decision-support framing). p6 = "How can budget-constrained project portfolios be optimized under hard budget limits?" (optimization framing). This divergence must permeate: title, abstract, introduction, contribution list, experiment naming, conclusion. | 1 week (writing) | Very high — makes the two papers answer fundamentally different questions |
| **A4: Candidate pool differentiation** | p5 uses a modified pool (e.g., 100 candidates with enriched traceability features from additional NERC reports; or a different RTS/SimBench ratio like 50/50 instead of 72/48). p6 keeps the original 120. | 3 days (re-run) | Medium — reduces overlap but sacrifices the "shared benchmark" narrative |
| **A5: Scenario renaming** | p5 renames its 7 scenarios to emphasize traceability dimensions (e.g., "trace-completeness stress test," "evidence-link coverage evaluation"). p6 keeps budget-oriented scenario names. Eliminates the "renewable_accommodation_review" exact overlap. | 1 day | Medium — cosmetic but reduces CrossCheck hits |

### B. Algorithm modifications

| Modification | Permitted? | Rationale |
|---|---|---|
| Rename "Coevolutionary" → "Preference-Adaptive" | **Yes, recommended** | Current mechanism (preference-vector update every 5 generations) is adaptive weighting, not coevolution. Name change eliminates easiest reviewer attack. |
| Add genuine coevolution (dual-population: project-portfolio pop + review-rule pop) | **Yes, if evidence supports it** | Would strengthen the novelty claim but requires significant implementation effort and may not improve results. Only do if current ablation weakness can't be honestly reframed. |
| Drop the coevolution component entirely, reframe as "NSGA-II + budget repair + trace archive" | **Yes, honest and defensible** | The ablation evidence shows budget repair (NoFeasibilityRepair drops 0.70%) and trace archive are the real contributors. Reframing as a "decision-support wrapper around NSGA-II" is honest and still publishable. |
| Switch downstream task to something else entirely (e.g., transmission expansion planning) | **No — violates general direction** | Would require entirely new problem formulation, data, and literature. Too far from the traceable review direction. |

### C. Dataset modifications

| Modification | Permitted? | Rationale |
|---|---|---|
| Add LBNL Queued Up / EIA-860 for historical outcome validation | **Yes, strongly recommended** | This is P0-3 — the single most impactful dataset addition. |
| Replace NERC reports with a different evidence source | **Yes, if traceability logic is preserved** | Could use IEEE PES technical reports, CIGRE brochures, or utility planning documents. Must preserve the "evidence-linked review" framing. |
| Use a different grid test system (e.g, ACTIVSg, IEEE 118-bus) | **Yes** | Would differentiate from p6 but sacrifices the RTS-GMLC/SimBench combination. Only necessary if Option B (pool differentiation) is chosen for p5/p6. |

### D. Downstream task modifications

| Modification | Permitted? | Rationale |
|---|---|---|
| Reframe from "feasibility review" to "investment prioritization under uncertainty" | **Yes** | Same algorithmic pipeline, different problem name. May help differentiate from p6. |
| Add a real-world case study (e.g., collaborate with a grid company) | **Yes, if achievable** | Would dramatically strengthen both venues but requires industry contact and data-sharing agreement. Timeline risk. |
| Switch to transmission-level expansion planning | **No** | Too far from the review/decision-support framing. |

---

## Honest Boundary

**What this paper CAN claim (with current v2 evidence):**
1. On a reproducible public benchmark derived from RTS-GMLC, SimBench, and NERC reliability reports, TRACE-MOEA achieves statistically significant (Holm-corrected) improvements over 4/6 external baselines across most scenarios.
2. The budget-repair and trace-archive components contribute meaningfully to portfolio quality (ablation evidence: NoFeasibilityRepair −0.70%, NSGA2Only −1.00%).
3. The framework provides auditable decision traces (decision-coverage, trace archive) as a decision-support feature, not as a performance metric.

**What this paper CANNOT claim:**
1. TRACE-MOEA improves *real* power grid feasibility review quality — no expert labels or historical outcomes validate this.
2. The coevolutionary/preference-adaptive component is the primary source of improvement — ablation evidence shows it is marginal-to-negative in some scenarios.
3. The method generalizes to other power systems or investment contexts — only one candidate pool, one evidence source, no cross-system validation.
4. The 0.89% gain over NSGA-II represents a practically significant improvement — it is statistically significant in some but not all scenarios, and the absolute magnitude is small.

**Boundary with p6:**
- Both papers share infrastructure. Neither can claim independent validation of the other's results.
- If both are submitted, the shared benchmark must be declared openly — hiding it is the highest-risk strategy.
- The contribution of each paper must be articulated in terms the other paper does not address.

---

## Fastest Path

### Timeline to submission (MDPI Applied Sciences target)

| Week | Action | Dependencies |
|---|---|---|
| 1 | **A2**: Rewrite title/abstract from scratch, eliminate p6 overlap | None |
| 1 | **A5**: Rename scenarios for traceability framing | None |
| 1–2 | **Revision 2**: Add budget/weight/pool sensitivity sweeps, generate plots | Config modification + compute |
| 1–2 | **A1**: Package candidate-generation pipeline as named benchmark (Zenodo DOI) | Code cleanup |
| 2–3 | **Revision 1**: LBNL Queued Up data download + historical outcome matching (Option 1) or NERC rule-based validation (Option 2) | Data access |
| 2–3 | **E3**: Generate convergence curves + boxplots from existing 30-seed data | Existing results |
| 3–5 | **Revision 3**: Write full manuscript (Introduction, Method, Results, Discussion, Limitations, Conclusion) | All above |
| 5 | **R3**: Prepare MDPI 4-piece compliance (Data Availability, Author Contributions, Funding, COI) | None |
| 5 | **CL2**: Rename "Coevolutionary" → "Preference-Adaptive" throughout manuscript | Writing |
| 5–6 | Internal review + iThenticate self-check vs p6 draft | p6 draft must exist |
| 6 | **Submit to Applied Sciences** | All above |

**Total: ~6 weeks to Applied Sciences submission** (if work is done in parallel and full-time).

### Timing relative to p6

| Scenario | Recommended gap | Risk level |
|---|---|---|
| **p6 submitted first → p5 submitted 8–10 weeks later** | p6 at Applied Sciences (MDPI), p5 at Applied Sciences or IEEE Access. p5 cites p6 (if published) or refers to "companion benchmark." | **Low risk** — optimal ordering. p6's stronger signal establishes the benchmark; p5 is the "traceability extension." |
| **p5 submitted first → p6 submitted 8–10 weeks later** | p5 at Applied Sciences, p6 at Applied Sciences. Same publisher = same editor pool risk. | **Medium risk** — p5's weaker signal goes first, and both land at MDPI. Consider p6 at a different publisher (e.g., IEEE Access). |
| **Both submitted simultaneously** | Different publishers (p5 at IEEE Access, p6 at Applied Sciences). | **High risk** — CrossCheck/iThenticate share corpora; simultaneous submission of same-pipeline papers is detectable. Not recommended. |
| **Both at IEEE Access** | Any timing. | **Very high risk** — "not distinct from prior publication" red line + possible same Associate Editor. Do not do this. |

### Recommended sequence (FAST PUBLICATION optimized)

1. **Now → Week 6:** Prepare p6 for submission to Applied Sciences (p6 is closer to submission-ready: stronger signal, sensitivity partially built in). Submit p6.
2. **Week 6 → Week 12:** While p6 is under review at Applied Sciences (~15–16 day first decision, likely 1 revision round = ~6–8 weeks total), prepare p5 using the timeline above.
3. **Week 14–16:** Submit p5 to **IEEE Access** (not Applied Sciences — avoids same-publisher clustering). By this time p6 may be accepted or in revision, giving p5 a citable reference for the "shared benchmark."
4. **Backup if p5 rejected from Access:** Route to Applied Sciences (different Section than p6) or MDPI Electronics.

### If the author insists on p5 first and fast:

- Submit p5 to **Applied Sciences** within 6 weeks (following the timeline above).
- Hold p6 for **≥10 weeks** after p5 submission, then submit to **IEEE Access** (reversing the current p6 target).
- This gives cross-publisher separation (p5 at MDPI, p6 at IEEE) and a 10-week timing gap.
- Risk: p5's weaker signal at Applied Sciences may draw "incremental" criticism that p6's stronger signal would not.

---

*Review based on ARA evidence chain static analysis as of 2026-07-13. All data citations reference files within `D:\aicoding\powergrid_benchmark\papers\mintou\mintou_p5_trace_moea_feasibility_review\` and `D:\aicoding\powergrid_benchmark\mintou_p6_bilonsga_project_review\`. No findings are invented; all are traceable to specific evidence paths cited above.*
