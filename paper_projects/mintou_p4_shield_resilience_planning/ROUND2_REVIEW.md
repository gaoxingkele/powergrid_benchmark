# Senior Review: mintou_p4 (SHIELD-MOEA)

**Paper**: Scenario-Aware Hybrid Multi-Objective Evolution for Resilient Distribution Network Planning under DER and Load Uncertainty
**Algorithm**: SHIELD-MOEA (Scenario-screened Hybrid Evolution for Load-serving Distribution Resilience)
**Review date**: 2026-07-13
**Priority**: FAST PUBLICATION (allowing major modifications to algorithm/dataset/downstream-task within general direction)
**Reviewer role**: Senior reviewer, paper_reviews project (offline, structured, deterministic)

---

## Summary

SHIELD-MOEA is a scenario-screened, local-repair-augmented, resilience-aware multi-objective evolutionary framework for distribution network planning under DER, load, and outage uncertainty. The current evidence package consists of:

1. **SimBench-derived planning proxy v2** (single test system: `1-complete_data-mixed-all-0-sw`, 18 subnets, 72 candidate actions, 8 main experiments, 7 ablations, 5 baselines, 3 repeats per method-experiment).
2. **pandapower AC load-flow validation v1** (4 SimBench MV networks x 6 stress scenarios, all methods + No-Plan reference, added 2026-07-13).

**Headline signal**: SHIELD-MOEA achieves hypervolume proxy `0.794` (+2.78% vs strongest baseline MOEA/D `0.773`; +3.26% vs strongest ablation NoScenarioScreen `0.769`). AC validation shows SHIELD-MOEA tied with MOEA/D at the highest AC-feasible rate (0.653 vs No-Plan 0.500) and lowest mean max line loading (60.3% vs No-Plan 90.8%).

**Core problem**: the paper is not yet a paper. It is a well-structured ARA project with positive signals, but missing related work, sensitivity analysis, statistical backing for its narrow margins, and several evidence-quality issues that any reviewer at any target venue would flag. The priority is FAST PUBLICATION, so this review focuses on the minimum-cost path to acceptance while preserving the general direction.

---

## Target Venue

### Primary: MDPI Energies

| Attribute | Assessment |
|---|---|
| **Fit** | **Medium-High**. Resilient distribution planning under DER/load uncertainty is squarely within Energies "electrical power & energy systems / smart grids" section. Scope desk-reject risk is negligible. |
| **Novelty floor** | **Met at margin**. Energies requires a nameable mechanism-combination tied to a gap statement (0/31 distilled papers introduced a fundamentally new algorithm). "Scenario screening x local repair x resilience-aware Pareto" is a valid combination. The +2.78% gain is within the "≤5% honestly reported" passing range. |
| **Sensitivity analysis** | **NOT MET — the #1 major-revision trigger at Energies** (distilled standard: near-mandatory). No parameter sweep of any kind exists in the SimBench v2 evidence. The AC validation's scenario axis (peak/growth/extreme/high-DER/N-1) provides a partial substitute but was not designed or reported as sensitivity analysis. |
| **External baselines** | **Met with caveats**. 5 baselines nominally, but Weighted Sum ≡ Deterministic Planning (bit-identical results across all experiments/repeats), reducing effective external baselines to 4. Stochastic MILP-small appears only in synthetic smoke, not SimBench v2. |
| **Statistical protocol** | **Not required at Energies** (0/29 distilled accepted papers have significance tests). The 3-repeat protocol is not a hard barrier, but the near-zero variance (most repeats bit-identical) makes the +2.78% claim unconvincing. |
| **Validation** | **Substantially addressed by AC validation v1** (2026-07-13). pandapower load-flow on 4 MV networks x 6 stress scenarios validates plan compositions. Remaining gap: AC validation shows SHIELD-MOEA ties MOEA/D exactly, so it does not differentiate the proposed method from the strongest baseline on electrical grounds. |
| **Hard floor (MDPI 4-piece)** | **Not addressed**. Funding, COI, Data Availability, Author Contributions statements are absent (ARA does not cover these). Must be added at manuscript stage. |

### Secondary: PCMP (Protection and Control of Modern Power Systems)

| Attribute | Assessment |
|---|---|
| **Fit** | **LOW — desk-reject risk is high**. PCMP scope = protection / control / fault diagnosis-location / stability / resilience *in the protection-control sense*. SHIELD-MOEA is a planning optimization algorithm, not a protection or control scheme. |
| **Advantages** | Diamond OA (free), ~4-week review (fastest of all venues), IF ≈ 11.9 Q1. |
| **Can we pull a protection/control angle?** | See "Allowable Modifications" section below. **Short answer: not without a fundamental rewrite of the downstream task.** |
| **PCMP feasibility verdict** | **Not viable for the current paper direction.** The planning-optimization framing, MOEA methodology, and hypervolume-proxy metrics are all outside PCMP's protection/control/fault/stability scope. Even aggressive re-framing (e.g., calling resilience planning "protection planning") would not survive reviewer scrutiny because the paper's actual contribution is an evolutionary optimization algorithm, not a protection relay, fault location method, stability controller, or adaptive protection scheme. |

### PCMP Feasibility Analysis (detailed)

PCMP's scope language from SKILL.md: "New theories/technologies in **protection and control** of modern power systems: relay protection, fault diagnosis & location, stability & control, DER/renewable integration, grid resilience, and increasingly data-driven/AI methods applied to protection and control."

The word "resilience" appears in PCMP's scope, but in the sense of resilience-through-protection-and-control (e.g., adaptive protection schemes that maintain reliability during extreme events, self-healing control algorithms, fault-ride-through strategies). SHIELD-MOEA's resilience is planning-stage investment optimization (where to place reinforcement, storage, DER, automation) — this is a **planning problem**, not a **protection/control problem**.

**What would need to change to fit PCMP:**
- The downstream task would need to shift from "where to invest" to "how to set protection relay parameters" or "how to design a self-healing control sequence" under uncertainty.
- The algorithm would need to operate on protection/control decision variables (relay pickup settings, recloser sequences, section breaker coordination) rather than planning actions (line reinforcement, storage siting, DER placement).
- The validation would need PSCAD/EMTP/RTDS-level transient or protection simulation, not steady-state AC load flow.
- The metrics would need to be protection-specific (fault clearing time, protection coordination margin, relay misoperation rate).

**Bottom line**: pulling a PCMP angle requires abandoning the planning problem entirely. This contradicts the "general direction stays" constraint. **PCMP is not a viable secondary venue for this paper.**

---

## 7-Dimension Review

### 1. Novelty

| Finding | Severity | Confidence | Fixability |
|---|---|---|---|
| **N1**: Mechanism motivation is one sentence. method.md says "Combines scenario screening with resilience-aware Pareto optimization" with no justification for why screening (vs. full evaluation), why local repair (vs. penalty), or why resilience-as-objective (vs. constraint). v1 weak results (-1.71%) prove the mechanism combination is configuration-sensitive. | 3 | 0.95 | 0.8 |
| **N2**: +2.78% over MOEA/D is narrow and SHIELD-MOEA ties MOEA/D exactly on AC validation (both 0.653 feasible rate). The differentiation story rests entirely on the proxy hypervolume, which is a self-defined metric. | 2 | 0.90 | 0.5 |
| **N3**: Scenario screening's computational-cost motivation is undermined by runtime ~0.0003 s per method. At this problem scale (72 candidates), screening saves negligible time. | 2 | 0.95 | 0.7 |

**Narrative**: The combination innovation is *potentially* sufficient for Energies (which has never required a fundamentally new algorithm in its distilled corpus). But the paper must argue *why* this particular combination is needed and *what* each component contributes — right now, the ablation table provides quantitative isolation (NoScenarioScreen -3.26%, NoRepair -4.12%, NoResilienceObj -8.79%) but no qualitative motivation. The v1-to-v2 trajectory (-1.71% → +2.78%) should be disclosed as a sensitivity-to-configuration lesson, which actually strengthens the screening-motivation story if told honestly.

### 2. Soundness

| Finding | Severity | Confidence | Fixability |
|---|---|---|---|
| **S1**: Weighted Sum ≡ Deterministic Planning — bit-identical across ALL experiments, ALL repeats, ALL 14 metrics (evidence: `real_simbench_planning_results.csv` lines 14-19 vs 17-19, 44-49 vs 47-49, etc.). This is two baselines that are actually one, reducing effective external baselines from 5 to 4. Any reviewer cross-checking the table will immediately flag this. | 4 | 1.00 | 0.9 |
| **S2**: 3 repeats with near-zero variance. SHIELD-MOEA's `deterministic_vs_scenario` results are bit-identical across all 3 repeats (`0.80131149`). NSGA-II repeats 1-2 are identical; MOEA/D repeats 2-3 are identical. The random seed is either not varied or the algorithm is near-deterministic at this problem scale. A +2.78% claim with no variance is statistically empty. | 3 | 0.95 | 0.8 |
| **S3**: Outage model produces zero method discrimination. In `outage_contingency`, ALL methods report `survivability_rate = 0.94`; in `unseen_stress_generalization`, ALL report `0.91`. This means the outage/stress model is a global scalar, not an element-level fault model. The resilience claims rest partly on these metrics. | 3 | 0.95 | 0.7 |
| **S4**: `restoration_aware_evaluation` experiment produces results bit-identical to `deterministic_vs_scenario` for every method (CSV line-level comparison). No actual restoration process is being modeled. | 3 | 0.95 | 0.9 |

**Narrative**: AC validation v1 (2026-07-13) was a major step forward — pandapower load-flow confirms that SHIELD-MOEA plans are electrically feasible at a higher rate than No-Plan and most baselines. But the remaining soundness issues (duplicate baselines, zero-variance repeats, non-discriminative outage model) are each independently sufficient to trigger major revision or rejection. S1 is fatal if not fixed — a reviewer who spots two baselines with identical numbers will question the entire experimental setup.

### 3. Experiments

| Finding | Severity | Confidence | Fixability |
|---|---|---|---|
| **E1**: No sensitivity analysis (Energies' #1 major-revision trigger, near-mandatory per distilled standards). No sweep of scenario count K, screening threshold, population size, objective weights, or uncertainty magnitude. The `low_scenario_count` ablation exists only in synthetic smoke, not SimBench v2. | 3 | 0.95 | 0.9 |
| **E2**: Stochastic MILP-small (method.md promised baseline, representing the planning-literature gold standard of two-stage stochastic programming) appears only in synthetic smoke, not in SimBench v2 public results. The strongest domain-appropriate baseline is absent. | 3 | 0.90 | 0.7 |
| **E3**: Problem scale (72 candidates, 18 subnets, runtime ~0.0003 s) is toy-level for a planning paper. Cannot support "scenario screening reduces computational burden" motivation. | 2 | 0.90 | 0.6 |
| **E4**: Single test system. Norm at Energies (~2/3 of accepted papers), but the SimBench network contains EHV1/HV1/HV2 voltage levels — title says "Distribution Network" but the source has transmission-level subnets. | 2 | 0.85 | 0.8 |
| **E5**: No modern MOEA baselines (post-2015). NSGA-II (2002), MOEA/D (2007), GA are legacy. No NSGA-III, SPEA2, MOPSO, or C-TAEA. | 2 | 0.85 | 0.8 |

**Narrative**: The experiment design has breadth (8 main + 7 ablations) but lacks depth. The three fixes with highest ROI for Energies are: (1) promote `low_scenario_count` to SimBench v2 and add 1-2 more sensitivity axes (E1); (2) fix the duplicate baseline (S1); (3) add IEEE 33-bus as a second test system using the already-cached pandapower/matpower cases (E4, zero download cost).

### 4. Reproducibility

| Finding | Severity | Confidence | Fixability |
|---|---|---|---|
| **R1**: Metric naming is inconsistent across layers. `experiments.md` lists `survivability_rate`, `voltage_violation_probability`, `expected_loss_index`; the CSV has `voltage_risk`, `reliability_proxy`, `survivability_rate`; concepts.md defines none of them formally. A reader cannot map manuscript metrics to evidence. | 3 | 0.95 | 0.9 |
| **R2**: Hypervolume proxy is never formally defined. No reference point, no normalization scheme, no formula linking it to standard hypervolume. | 2 | 0.95 | 0.9 |
| **R3**: Code is not available. Not required at Energies (1/34 in distilled corpus), but SimBench-derived reproducibility depends on documenting the exact candidate-generation, objective-evaluation, and mapping pipeline. | 1 | 0.80 | 0.8 |

**Narrative**: The ARA structure is internally reproducible (evidence files, source profiles, analysis scripts are all present and traceable). But the *external* reproducibility — what a reader or reviewer would need — is poor. Metric definitions, the hypervolume proxy formula, and the SimBench-to-plan mapping rules must all be written into the manuscript.

### 5. Related Work

| Finding | Severity | Confidence | Fixability |
|---|---|---|---|
| **RW1**: related_work.md is effectively empty — a single line pointing to `comparison_analysis.md` plus a separation note. No literature coverage of any kind. Energies explicitly lists "inadequate literature review" as a desk-reject trigger. | 4 | 1.00 | 0.9 |

**Narrative**: This is a binary gate: the paper cannot be submitted without a proper related work section. Three strands are needed: (1) resilience-oriented distribution planning (hardening/restoration paradigms); (2) scenario generation and reduction for power system uncertainty; (3) multi-objective evolutionary algorithms in distribution planning. Each strand needs 5-10 references and must converge on the gap: "no existing work embeds scenario screening within the MOEA loop for resilience-aware distribution planning."

### 6. Clarity

| Finding | Severity | Confidence | Fixability |
|---|---|---|---|
| **C1**: No numbered contribution list. Energies/Access both expect 3-6 numbered contributions in the introduction. | 2 | 0.90 | 0.95 |
| **C2**: No limitations section in the manuscript (ARA's "Interpretation Boundary" is excellent but lives outside the paper). | 2 | 0.90 | 0.95 |
| **C3**: Title says "Distribution Network" but SimBench `1-complete_data-mixed-all-0-sw` contains EHV1/HV1/HV2 subnets (source profile: 18 subnets spanning all voltage levels). Must either narrow the experimental scope to MV/LV subnets only, or adjust the title/framing. | 2 | 0.95 | 0.8 |
| **C4**: Claims C1-C4 in claims.md use placeholder language ("target-journal-level baselines") that must be replaced with specific baseline names in the manuscript. | 1 | 0.95 | 0.95 |

### 7. Ethics

| Finding | Severity | Confidence | Fixability |
|---|---|---|---|
| **ET1**: No ethics concerns identified. SimBench is a legitimate public benchmark with proper provenance. No human subjects, no dual-use risk. | 0 | 0.95 | N/A |
| **ET2**: MDPI mandatory declarations (Funding, COI, Data Availability, Author Contributions) are absent from ARA. Must be added at submission stage. | 1 | 0.90 | 0.95 |

---

## RRI (Revision Readiness Index)

| Dimension | Score (0-4) | Weight | Weighted |
|---|---|---|---|
| Novelty | 2.3 | 0.15 | 0.35 |
| Soundness | 2.3 | 0.25 | 0.58 |
| Experiments | 2.4 | 0.20 | 0.48 |
| Reproducibility | 2.0 | 0.10 | 0.20 |
| Related Work | 4.0 | 0.10 | 0.40 |
| Clarity | 1.8 | 0.10 | 0.18 |
| Ethics | 0.3 | 0.10 | 0.03 |
| **RRI** | | | **2.22 / 4.00** |

**Interpretation**: RRI 2.22 = "significant revisions required before submission." The paper is roughly halfway between initial project and submission-ready. The good news: the two highest-severity items (RW1: related work = 4.0, S1: duplicate baseline = 4.0) are both highly fixable (0.9+). The hard parts (S2: repeat variance, N2: AC differentiation) require re-running experiments but have clear paths.

---

## Predicted Decision

### MDPI Energies (Primary)

**Current state**: **Reject** or **Major Revision** (leaning Reject due to RW1 + S1 combination).

**After P0 fixes** (related work, baseline fix, sensitivity analysis, 30-seed re-run): **Minor-to-Major Revision** with high probability of acceptance after one revision round.

**Reasoning**: Energies' distilled standards show that (a) related-work gaps and (b) missing sensitivity analysis are the top two revision triggers, but both are routinely resolved in one revision round. The AC validation v1 substantially de-risks the "unvalidated simulation" desk-reject concern. The +2.78% gain is within Energies' acceptance range for honestly-reported incremental improvements. With 30-seed runs providing genuine variance and a sensitivity sweep, the paper would meet or exceed Energies' typical accepted-paper quality.

**Estimated timeline after fixes**: Submission → first decision ~16-17 days → one revision round (~20 days) → acceptance → publication ~3-4 days. Total: ~6-8 weeks from submission.

### PCMP (Secondary)

**Current state**: **Desk Reject (scope)**. Planning optimization with MOEA is outside protection/control/fault/stability scope.

**After any feasible modification**: Still **Desk Reject** unless the entire downstream task changes from planning to protection/control. Not viable under the "general direction stays" constraint.

---

## Top-3 Revisions (ordered by ROI for Energies acceptance)

### Revision 1: Write Related Work + Unify Metric Definitions (fixes RW1, R1, R2)

**What**: Produce a 3-strand literature review (resilience planning, scenario reduction, MOEA-in-distribution-planning) with 25-40 references converging on the screening-within-MOEA-loop gap. Simultaneously, write formal mathematical definitions for every metric (hypervolume proxy, survivability_rate, voltage_risk, expected_loss_index, constraint_violation_rate) with reference points, normalization, and mapping to standard resilience metrics (EENS, load not served, resilience trapezoid).

**Why**: RW1 is severity-4 and a known desk-reject trigger. R1/R2 undermine every numerical claim in the paper. These are pure-writing tasks with zero computational cost.

**Effort**: ~2-3 days of focused writing. References available from cached literature.

### Revision 2: Fix Baseline Table + Re-run with 30 Seeds (fixes S1, S2, S4, E5)

**What**:
1. Eliminate the Weighted Sum ≡ Deterministic Planning duplication (make them actually different methods, or remove one and add a real 6th baseline).
2. Fix the random seed handling so that 30 independent runs produce genuine variance.
3. Replace or remove the `restoration_aware_evaluation` experiment (currently bit-identical to `deterministic_vs_scenario`).
4. Add 1-2 modern MOEA baselines (NSGA-III or MOPSO from pymoo, already available as p5/p6 use pymoo).

**Why**: S1 (duplicate baselines) is severity-4 and trivially detectable. S2 (no variance) makes the +2.78% claim indefensible. These are the most common reviewer complaints for MOEA papers.

**Effort**: ~1-2 days code fix + ~1 day compute (30 seeds x 11 methods x 8 experiments). The p5/p6 v2 pipeline already implements 30-seed + Mann-Whitney U; the same infrastructure can be reused for p4.

### Revision 3: Sensitivity Analysis + Second Test System (fixes E1, E3, E4)

**What**:
1. Promote `low_scenario_count` ablation from synthetic smoke to SimBench v2 results.
2. Add 2-3 sensitivity sweeps: scenario count K ∈ {5, 10, 20, 50}, DER penetration variance σ ∈ {0.1, 0.2, 0.3}, population size N ∈ {50, 100, 200}.
3. Add IEEE 33-bus (or SimBench LV subnet subset) as a second test system using cached pandapower/matpower cases. This also addresses the EHV/HV-in-"distribution"-title mismatch (E4/C3).
4. Scale up the candidate action space (e.g., per-bus rather than per-subnet candidates) to make runtime meaningful.

**Why**: E1 (no sensitivity analysis) is the single most common major-revision trigger at Energies. A second test system is standard in the top half of Energies planning papers and neutralizes the "toy problem" concern.

**Effort**: ~2-3 days (sensitivity sweeps are parametric re-runs; IEEE 33-bus integration reuses existing pandapower infrastructure).

---

## Allowable Modifications (within "general direction stays" constraint)

### Can change freely:
- **Dataset**: Switch from SimBench mixed-voltage to IEEE 33-bus/123-bus standard test systems (already cached). Can also add `ausgrid_solar_home` (real PV) and `sgsc` (real smart-meter load) for realistic uncertainty distributions (already cached).
- **Baselines**: Add/replace baselines freely. Recommended: NSGA-III, MOPSO, Stochastic MILP (promote from smoke). Remove duplicate.
- **Metrics**: Rename, redefine, add standard metrics (EENS, SAIDI, load curtailment). Can replace the hypervolume proxy with standard hypervolume (pymoo native).
- **Ablation design**: Redesign ablations to isolate components more cleanly.
- **Problem scale**: Expand candidate space, add more subnets, increase evaluation budget.

### Can change with care (must preserve direction):
- **Algorithm internals**: Can refine scenario screening criterion, local repair operator, or resilience objective formulation. Cannot remove the scenario-screening + MOEA combination entirely (that changes the paper's identity).
- **Test system**: Can add or substitute, but must remain a distribution-network planning problem.
- **Downstream task details**: Can shift from "investment planning" to "planning + operational dispatch" for richer validation, but must remain planning-stage.

### Cannot change (direction constraint):
- The general framing: scenario-aware MOEA for resilient distribution network planning under uncertainty.
- The core algorithmic identity: SHIELD-MOEA as a named method.

### Can we pull a protection/control angle? (PCMP analysis)

**No, not within the direction constraint.** Here is the detailed analysis:

1. **What PCMP means by "resilience"**: In PCMP's scope, "grid resilience" refers to the ability of protection and control systems to maintain service during and after faults/extreme events. This includes: adaptive relay protection settings, self-healing distribution automation (FLISR: fault location, isolation, and service restoration), wide-area protection schemes, cyber-physical security of protection systems, and stability control under high-DER conditions.

2. **What SHIELD-MOEA does**: It optimizes long-term investment decisions (where to reinforce lines, place storage, install DER, add automation devices) over a planning horizon, using a multi-objective evolutionary algorithm with scenario screening. This is a **planning-stage** optimization, not an **operational protection/control** algorithm.

3. **The gap**: Protection和控制 papers in PCMP operate on timescales of milliseconds to seconds (relay coordination, fault clearing), or at most minutes (self-healing restoration sequences). SHIELD-MOEA operates on planning timescales of years (investment decisions). The decision variables are fundamentally different (relay settings vs. infrastructure placement).

4. **Could we reframe?**: Even calling it "resilience-oriented protection planning" would not work because:
   - The algorithm does not design protection schemes (relay coordination, fuse selection).
   - The "automation" planning action is a binary siting decision, not a control algorithm.
   - The validation (AC load flow) is steady-state, not transient/protection-grade.
   - Reviewers at PCMP would expect PSCAD/EMTP simulation of fault scenarios with protection system response.

5. **What would it take**: To genuinely fit PCMP, the paper would need to become something like "Scenario-aware optimization of adaptive protection settings for distribution systems with high DER penetration" — using SHIELD-MOEA to tune relay pickup currents, time-dial settings, or recloser sequences under DER uncertainty scenarios. This is a completely different downstream task that happens to use the same algorithm skeleton. **This violates the "general direction stays" constraint.**

**Verdict**: PCMP is not a feasible venue for this paper. Do not attempt to force-fit it.

---

## Honest Boundary

### What the evidence actually supports:
- SHIELD-MOEA produces a modestly better hypervolume proxy (+2.78% over MOEA/D) on a single SimBench-derived planning benchmark with 72 candidate actions.
- SHIELD-MOEA plans pass pandapower AC load-flow checks at the same rate as MOEA/D plans (0.653) and better than most other methods, with lower peak line loading.
- The scenario screening component contributes measurably to the proxy metric (+3.26% over no-screening ablation).
- The resilience objective component contributes the most to the proxy metric (+8.79% over no-resilience-objective ablation).

### What the evidence does NOT support:
- That SHIELD-MOEA is *electrical-engineering-better* than MOEA/D (AC validation shows identical feasibility rates).
- That scenario screening reduces computational cost (runtime is ~0.0003 s; screening saves nothing at this scale).
- That the outage model differentiates methods (all methods get survivability = 0.94 in outage scenarios).
- That the method generalizes beyond one SimBench network configuration.
- That the results are statistically robust (3 near-identical repeats provide no variance estimate).

### v1-to-v2 trajectory disclosure:
The preserved v1 weak result (-1.71% vs MOEA/D) shows that SHIELD-MOEA's advantage is configuration-sensitive. This is not a weakness to hide — it is an honest finding that strengthens the paper if disclosed as motivation for careful scenario/repair configuration. Reviewers at Energies appreciate honest limitation statements (distilled standard: "honest limitations are a net positive").

---

## Fastest Path to Publication

### Target: MDPI Energies, ~6-8 weeks from start of revisions to publication

| Step | Task | Effort | Priority |
|---|---|---|---|
| 1 | Write related work (3 strands, 25-40 refs) | 2-3 days | **P0 — blocking** |
| 2 | Fix Weighted Sum / Deterministic Planning duplication | 0.5 days | **P0 — blocking** |
| 3 | Fix random seed handling; run 30 seeds | 1 day fix + 1 day compute | **P0 — blocking** |
| 4 | Sensitivity analysis: K, σ, N (at least 2 of 3) | 2-3 days | **P0 — Energies near-mandatory** |
| 5 | Unify metric names + formal definitions + hypervolume proxy formula | 1 day | **P0 — blocking** |
| 6 | Add IEEE 33-bus as second test system | 2 days | **P1 — strongly recommended** |
| 7 | Add NSGA-III or MOPSO baseline (pymoo) | 1 day | **P1 — strongly recommended** |
| 8 | Redo outage model: element-level N-k fault sampling | 2-3 days | **P1 — makes resilience story credible** |
| 9 | Write numbered contributions + limitations section | 0.5 days | **P1 — standard formatting** |
| 10 | MDPI template + 4 mandatory declarations | 0.5 days | **P1 — submission gate** |
| 11 | Replace proxy hypervolume with pymoo standard hypervolume | 1 day | **P2 — strengthens metric credibility** |
| 12 | Access real uncertainty data (ausgrid_solar_home, sgsc) | 2-3 days | **P2 —锦上添花** |

### Minimum viable submission (P0 only): ~7-10 days of focused work

After P0, the paper has: related work, fixed baselines, 30-seed variance, sensitivity analysis, unified metrics. This meets Energies' floor. Predicted outcome: Major Revision → one revision round → acceptance.

### Recommended submission (P0 + P1): ~15-20 days of focused work

Adds: second test system, modern MOEA baselines, element-level outage model, proper formatting. This exceeds Energies' typical accepted-paper quality. Predicted outcome: Minor-to-Major Revision → one revision round → acceptance.

### Cost note:
- MDPI Energies APC: ~CHF 2,600 (verify on official page). Check for matching Special Issues on distribution resilience / smart grid planning (often open, same review standard, same indexing).
- PCMP is free but not viable for this paper.
- IEEE Access (backup): ~USD 2,160, but requires 50-run statistical protocol — more expensive AND more work than Energies. Keep as fallback only if Energies rejects.

---

*Review based on ARA snapshot 2026-07-13. All journal metrics (IF, APC, timelines) must be verified at official pages before submission.*
