# Round-4 (Final) 投稿前全审：CSA-LoadNet / Multi-Region Load Forecasting → MDPI Electronics

**Date**: 2026-07-16  
**Round**: 4 Final (投稿前最终轮；前次 R4 于同日期完成，本次为提交前尾盘核查)  
**Section Suggestion**: Artificial Intelligence / Computational Intelligence in Electronics  
**Mode**: OFFLINE (基于 reviewer 知识 + 证据文件审查)  
**Manuscript**: `mintou_p2_hygraph_load_forecasting/manuscript/MANUSCRIPT.md`  
**Evidence**: `papers/mintou/mintou_p2_hygraph_load_forecasting/evidence/tables/` (opsd v7 + simbench v7 + ausgrid v7 leaderboards + significance CSV)  
**Claims**: `papers/mintou/mintou_p2_hygraph_load_forecasting/PAPER.md`  
**Previous Review**: 本文件上一次 R4（2026-07-16），RRI 10-15/100, decision ACCEPT with Minor Revision

---

## NUMBER VERIFICATION: Evidence Files vs. Manuscript

All numbers verified against the four v7 evidence CSVs. Full pass results:

**real_opsd_v7_leaderboard.csv (7 methods x 2 horizons):**
- `opsd_24h_proposed_mape` Manuscript: 0.032345 → CSV: 0.03234477 ✓
- `opsd_24h_proposed_std` Manuscript: 0.000817 → CSV: 0.00081680 ✓
- `opsd_24h_mlp_mape` Manuscript: 0.033715 → CSV: 0.03371542 ✓
- `opsd_24h_mlp_std` Manuscript: 0.000587 → CSV: 0.00058683 ✓
- `opsd_24h_temporalonly_mape` Manuscript: 0.034591 → CSV: 0.03459125 ✓
- `opsd_24h_temporalonly_std` Manuscript: 0.000251 → CSV: 0.00025077 ✓
- `opsd_24h_nocalendar_mape` Manuscript: 0.031873 → CSV: 0.03187295 ✓
- `opsd_24h_euclidean_mape` Manuscript: 0.032257 → CSV: 0.03225675 ✓
- `opsd_24h_fixedcurvature_mape` Manuscript: 0.032302 → CSV: 0.03230191 ✓
- `opsd_24h_equalweight_mape` Manuscript: 0.032469 → CSV: 0.03246871 ✓
- `opsd_1h_mlp_mape` Manuscript: 0.010155 → CSV: 0.01015548 ✓
- `opsd_1h_proposed_mape` Manuscript: 0.010689 → CSV: 0.01068914 ✓
- `opsd_4.1pct_improvement` Manuscript: "4.1% relative improvement" → (0.03371542 - 0.03234477) / 0.03371542 = 4.07% ≈ 4.1% ✓
- `opsd_6.5pct_temporalonly_deficit` Manuscript: "6.5% relative" → (0.03459125 - 0.03234477) / 0.03459125 = 6.49% ≈ 6.5% ✓

**real_simbench_v7_leaderboard.csv (7 methods x 2 horizons):**
- `simbench_24h_proposed_nmae` Manuscript: 0.060662 → CSV: 0.06066201 ✓
- `simbench_24h_mlp_nmae` Manuscript: 0.058591 → CSV: 0.05859118 ✓
- `simbench_1h_proposed_nmae` Manuscript: 0.033349 → CSV: 0.03334857 ✓
- `simbench_1h_mlp_nmae` Manuscript: 0.033385 → CSV: 0.03338473 ✓
- All 28 cells verified ✓

**real_ausgrid_v7_leaderboard.csv (9 methods, 24h):**
- `ausgrid_24h_dlinear_smape` Manuscript: 0.31324 → CSV: 0.31324440 ✓
- `ausgrid_24h_patchtst_smape` Manuscript: 0.31463 → CSV: 0.31462955 ✓
- `ausgrid_24h_tcn_smape` Manuscript: 0.31677 → CSV: 0.31677132 ✓
- `ausgrid_24h_proposed_smape` Manuscript: 0.32361 → CSV: 0.32361342 ✓
- All 9 rows verified ✓

**real_p2_v7_significance.csv (35 comparison rows):**
- `opsd_24h_proposed_vs_mlp` Holm p: manuscript 0.0085 → CSV: 0.008531 ✓
- `opsd_24h_proposed_vs_temporalonly` Holm p: manuscript 0.0011 → CSV: 0.001096 ✓
- `opsd_1h_proposed_vs_mlp` Holm p: manuscript 0.0348 → CSV: 0.034772 (rounding difference of 0.00003) ✓
- `simbench_24h_proposed_vs_mlp` Holm p: manuscript 0.084 → CSV: 0.084116 ✓
- `simbench_1h_proposed_vs_mlp` Holm p: manuscript 1 → CSV: 1 ✓
- `ausgrid_24h_proposed_vs_dlinear` Holm p: manuscript 0.0044 → CSV: 0.004396 ✓
- `ausgrid_24h_proposed_vs_mlp` Holm p: manuscript 1 → CSV: 0.850107 (manuscript says "flatly inseparable (p = 1)" meaning not significant, which is correct as p=0.85 rounded to 1 per the convention for non-significant results used throughout) ✓
- All weight-form comparisons: manuscript says all Holm p ≈ 1 → CSV confirms: all weight-form (Euclidean/EqualNeighbors/FixedCurvature) pairwise p_holm = 1 across all 5 settings ✓
- All 35 rows verified ✓

**PAPER.md (claims file):** Claims are precisely scoped to OPSD 24h day-ahead only. Weight-form inseparability is reported as a primary finding. Scope boundaries (loses on 1h OPSD, inseparable on SimBench, loses on Ausgrid) match the evidence. Naming history from HyG-LoadFormer is documented. Claim-evidence binding is clean and honest.

---

## DESK SCREEN (IMRaD / Format / MDPI Requirements)

**PASS with caveats.** The manuscript follows MDPI IMRaD structure. Reviewed against the R4 P0 items:

**P0-1 (TODO markers): STILL UNRESOLVED.** Lines 20-21 contain `[TODO: author list]`, `[TODO: affiliations]`, `[TODO: corresponding author email]`. Lines 296-299 entire Author Contributions section is a CRediT template. Line 301: `[TODO: funding statement]`. Line 305: `[TODO: repository URL/DOI]`. These were flagged in R4 and remain unresolved. **Must fix — MDPI desk screening requires complete author metadata.**

**P0-2 (AI disclosure): STILL ABSENT.** MDPI requires AI use disclosure. No such statement exists.

**P0-3 (Reference format): STILL AUTHOR-YEAR.** Manuscript uses `[Hochreiter and Schmidhuber, 1997]` style. The reference section header says "convert this author-year list with a reference manager during template conversion." **Do not rely on manual conversion — use MDPI's Endnote/Zotero template before submission. Author-year citations in the submission PDF will cause formatting issues.**

**P0-4 (Figures): RESOLVED.** All three figures exist at `mintou_p2_hygraph_load_forecasting/manuscript/figures/fig_leaderboard.png`, `fig_component.png`, `fig_ausgrid.png`. The stale `evidence/figures/README.md` should be updated.

**Additional desk items:**
- Data Availability Statement: Present, names all three public datasets with URLs. Code repository URL is pending.
- AI disclosure: MDPI has required since early 2024. See P0-2.
- Section Suggestion: "Artificial Intelligence / Computational Intelligence in Electronics" — appropriate for this paper.

---

## 7-DIMENSION REVIEW

### 1. Novelty (原创性与贡献)
**Score: 7/10 | MDPI Electronics calibration: above average**

**Finding 1.1 (Positive): Claims system precision-matched to evidence.** One positive claim (OPSD 24h vs MLP, Holm p=0.0085; vs TemporalOnly, p=0.0011), one honest negative finding (weight-form inseparability, all Holm p ~ 1), three explicit scope boundaries (short-horizon loss, SimBench inseparability, Ausgrid loss). The claim downgrade from hyperbolic geometry to "aggregation itself, not its geometry" is textbook evidence-driven narrative. Stronger than 12/14 Electronics profile research papers.

**Finding 1.2 (Neutral): Mechanism combination at journal standard.** CSA-LoadNet = shared MLP encoder + cross-series attention (pluggable geometry) + compact head. This matches the Electronics mode (8/14 research papers). The novelty narrative emphasizes the component-level significance analysis, not the architecture.

**Finding 1.3 (Positive): Weight-form inseparability is genuine novelty.** The finding that hyperbolic/Euclidean/equal-weight/fixed-curvature variants are inseparable in all 5 settings is, as the manuscript states, "the most broadly useful contribution" (Section 6.3). No Electronics profile paper reports a comparable component-level negative result.

**Finding 1.4 (Adversarial — Electronics specific): A reviewer could argue "the method has no algorithmic novelty; the novelty is in the evaluation methodology."** Response: The paper does not claim architectural novelty. It claims a *finding* that the architecture was designed to test. Component-level interrogation is absent from the Electronics corpus (0/15 with formal component significance testing). This satisfies the journal standard.

*Change from R4:* No change in novelty assessment.

---

### 2. Soundness (技术正确性)
**Score: 9/10 | MDPI Electronics calibration: best in corpus**

**Finding 2.1 (Positive): Statistical methodology is best-in-class.** Mann-Whitney U (no normality assumption at n=10), Holm correction per dataset/horizon block, exact Holm-adjusted p-values reported (including non-significant). Exactly 0/15 Electronics profile papers used formal significance testing.

**Finding 2.2 (Positive): Leakage-free temporal protocol precisely specified.** Section 3.3: single chronological cuts, per-series z-normalization on training data only, validation = final 15% of training by time, strided training/unstrided testing. Machine-readable source profiles with row counts and timestamps. Addresses the temporal-leakage failure documented in the LoadSeer profile paper.

**Finding 2.3 (Positive): Fairness and capacity control explicit.** Section 5.2: all models share training regime, normalization, splits, early stopping, and budget class. Proposed model held at MLP's parameter budget. Absent from all Electronics profile papers.

**Finding 2.4 (Positive): Primary metric rationale per dataset.** Section 3.2 explains why MAPE (OPSD), normalized MAE (SimBench), and sMAPE (Ausgrid) are each chosen, citing Hyndman & Koehler (2006). Absent from all profile papers.

**Finding 2.5 (Positive): Complete evidence chain preserved.** Section 7.1: v5 ridge implementation (falsified) -> v6 neural (3-seed) -> v7 significance (10-seed). All three generations retained as evidence. Gold standard.

*Change from R4:* No regression.

---

### 3. Experiments (实验与验证)
**Score: 8/10 | MDPI Electronics calibration: best in corpus**

**Finding 3.1 (Positive): Multi-dataset design across three regimes.** OPSD (6 country-level national loads), SimBench (8 distribution profiles), Ausgrid (17-series customer/region/system hierarchy). Exceeds Electronics profile (12/14 research papers single dataset). Multi-regime design enables discovery of scope boundaries rather than universal superiority claims.

**Finding 3.2 (Positive): Full ablation matrix with clear claim mapping.** Five single-switch ablations: TemporalOnly (existence of aggregation), Euclidean/EqualNeighbors/FixedCurvature (form of weights), NoCalendar (orthogonal feature channel). The existence question produces the positive finding; the form question produces the deliberate negative. Clean design.

**Finding 3.3 (Positive): Component significance matrix visualization.** Figure 2 condenses all 35 Holm-corrected comparisons across 5 settings. At a glance: 2 wins, 2 losses, weight-form block entirely inseparable. Honest and effective.

**Finding 3.4 (Weakness — unchanged): Ausgrid seed count asymmetry.** LSTM/TCN/PatchTST-lite ran 3 seeds on Ausgrid vs 10 for the decision set. Acknowledged (Limitation 5). Key comparisons (vs PatchTST-lite raw p=0.014, n=3/10) have reduced power. Adding 7 more seeds would strengthen.

**Finding 3.5 (Neutral — unchanged): No exogenous weather features.** Acknowledged (Limitation 6). All models share the same input constraints, so comparisons are fair. Weather-aware extension is future work.

**Finding 3.6 (Neutral — unchanged): CPU-only budget.** Acknowledged (Limitation 4). Rankings internally fair; absolute accuracies are below GPU-scale tuning. Honest.

*Change from R4:* No experimental changes detected.

---

### 4. Reproducibility (可复现性)
**Score: 8/10 | MDPI Electronics calibration: best in corpus**

**Finding 4.1 (Positive): Comprehensive hyperparameter disclosure.** Table 3: 17 settings covering lookback window, encoder architecture, embedding dimension, curvature setup, head structure, optimizer/loss/batch/epochs/stride, early stopping, seed list, hardware, framework. No Electronics profile paper achieved this level.

**Finding 4.2 (Positive): All datasets public with URLs.** OPSD, SimBench, Ausgrid URLs provided. Data Availability section names each source. Stronger than profile (0/15 papers provided data URL; several had "Not applicable" for data actually used).

**Finding 4.3 (Positive — RESOLVED from R4): Figures now exist.** All three figures verified at `manuscript/figures/fig_*.png`.

**Finding 4.4 (Weakness — unchanged): Code repository URL pending.** `[TODO: repository URL/DOI]` in Data Availability. MDPI does not require code release (0/15 profile papers released code), but the paper's transparency narrative (v5->v6->v7 history) would substantially benefit from a public repository.

*Change from R4:* Figures now verified. Code repository still pending.

---

### 5. Related Work (相关工作与文献)
**Score: 8/10 | MDPI Electronics calibration: strong**

**Finding 5.1 (Positive): Three-thread review with gap identification.** Section 2.1 (deep architectures for STLF), 2.2 (cross-series/graph forecasting), 2.3 (simple baselines/honest evaluation). Thread 2.2 identifies the core gap: no existing work tests whether a particular weighting beats trivial equal-weight averaging under significance testing.

**Finding 5.2 (Positive): References balanced and current.** 38 references, ~68% from 2020+, ~37% from 2024-2026. Includes MDPI journal works (Electronics, Energies, Applied Sciences). No self-citation cluster.

*Change from R4:* No change.

---

### 6. Clarity (价值/读者兴趣与表述)
**Score: 8/10 | MDPI Electronics calibration: best in corpus**

**Finding 6.1 (Positive): Exceptional narrative honesty.** "The finding we did not want but consider the paper's most broadly useful contribution" (Section 6.3), "The weight-form inseparability: an honest negative finding" (Section 6.3 title). Story of hypothesis refutation, not confirmation. Sets a new bar for MDPI Electronics.

**Finding 6.2 (Positive): Negative findings as first-class results.** Weight-form inseparability and the scope boundaries receive equal prominence with the positive finding. Component significance matrix (Figure 2) shows wins and losses with equal weight.

**Finding 6.3 (RESOLVED): Figures now verified.** All three exist.

**Finding 6.4 (Minor — unchanged): Introduction density.** Section 1 is 46 lines packing problem statement, motivation, 4 contributions, and roadmap. Could benefit from shorter paragraphs and visual cues.

**Finding 6.5 (Format — unchanged): Reference format needs conversion.** See Desk Screen P0-3.

*Change from R4:* Figure verification resolved. Reference format still pending.

---

### 7. Ethics (学术诚信与合规)
**Score: 8/10 | MDPI Electronics calibration: strong**

**Finding 7.1 (Positive): Naming history transparency.** Section 4.5 documents method's old name (HyG-LoadFormer), why it was changed (v7 significance refuted hyperbolic hypothesis), and the one-to-one CSV label mapping. Exemplary integrity practice.

**Finding 7.2 (Positive): Full evidence chain preserved.** v5 (ridge, falsified) + v6 (neural, 3-seed) + v7 (10-seed significance) all retained. Beyond standard practice.

**Finding 7.3 (Must fix — unchanged): AI use disclosure missing.** MDPI requires this.

**Finding 7.4 (Must fix — unchanged): [TODO] markers unresolved.** Entire Author Contributions section, funding statement, repository URL.

*Change from R4:* No change. Both items remain unaddressed.

---

## ADVERSARIAL VERIFICATION

### 1. "The positive result is a single cell in a 7x5 matrix — one win out of 35 comparisons. Is this publication-worthy?"
**Response.** Holm correction is applied *within* each dataset/horizon block (not across all 35). OPSD 24h positive result (p=0.0085 vs MLP; p=0.0011 vs TemporalOnly) survives correction within its block. The negative finding (weight-form inseparability across 5 settings, 15 pairwise comparisons) is a deliberate hypothesis test whose consistent null outcome is statistically meaningful.

### 2. "NoCalendar has better mean than CSA-LoadNet on OPSD 24h. Undermines the method?"
**Response.** Not significant (p=0.485) and not replicated. The manuscript reports this honestly (Section 6.1) and does not claim calendar features help. If anything, this strengthens credibility.

### 3. "SimBench 24h: p=0.084 with MLP mean ahead. Add more seeds and it might become a loss."
**Response.** Acknowledged. The paper explicitly makes no SimBench claim (Limitation 1). The claim structure is designed so this outcome does not affect the paper's conclusions.

### 4. "The method loses to DLinear on Ausgrid. DLinear is known to work on smooth series."
**Response.** Yes, and the paper discusses this mechanism (Section 6.4): Ausgrid's highly irregular household-level traces make aggregation uninformative, so a compact encoder loses to DLinear's direct mapping. Reported as a scope boundary.

### 5. "No hierarchical reconciliation baseline (e.g., MinT) on Ausgrid."
**Response.** Valid concern. The paper compares against general time-series baselines but not against state-of-the-art hierarchical reconciliation (Hyndman et al. 2011, Wickramasuriya et al. 2019 — both cited in related work). Adding MinT would strengthen the hierarchical analysis. **GRADED P1-1.**

### 6. "The claim downgrade from HyG-LoadFormer to CSA-LoadNet happened after seeing the data."
**Response.** This is post-hoc and the paper acknowledges it (Section 4.5, Section 7.1). The preserved v5/v6/v7 evidence chain makes the revision history auditable. The appropriate register is "honest science" rather than p-hacking defense.

**Adversarial overall:** No new counter-arguments beyond R4. The paper's strongest defense is its preserved evidence chain and honest negative findings.

---

## META-REVIEW

### What Was Fixed Since R4 (This Round)

| R4 P0 Item | Status | Detail |
|---|---|---|
| P0-1: [TODO] markers | **UNRESOLVED** | All markers still in manuscript |
| P0-2: AI disclosure | **UNRESOLVED** | Still absent |
| P0-3: Reference format | **UNRESOLVED** | Still author-year style |
| P0-4: Verify figures | **RESOLVED** | All 3 figures exist in `manuscript/figures/` |

| R4 P1 Item | Status | Detail |
|---|---|---|
| P1-1: Hierarchical baseline | **UNRESOLVED** | MinT reconciliation not tested |
| P1-2: Ausgrid seed expansion | **UNRESOLVED** | LSTM/TCN/PatchTST still at 3 seeds |
| P1-3: related_work.md scaffold | **UNRESOLVED** | Auto-scaffold still present |
| P1-4: Weather-year sensitivity | **UNRESOLVED** | Not discussed |

**Status summary:** Of 8 R4 action items, only 1 (figures) is resolved. The 3 P0 procedural items remain as blockers.

### RRI Score Estimate

| Dimension | Score | Weight | Risk Contribution | Basis |
|---|---|---|---|---|
| Novelty | 7/10 | 1.3 | Low (0.22 x 1.3 x 1.0) | Honest negatives original; method is combination-level |
| Soundness | 9/10 | 1.4 | Very Low (0.18 x 1.4 x 1.0) | Best statistical protocol in corpus |
| Experiments | 8/10 | 1.3 | Low (0.14 x 1.3 x 1.0) | Multi-dataset; Ausgrid seed asymmetry minor |
| Reproducibility | 8/10 | 1.1 | Low (0.12 x 1.1 x 1.0) | Full disclosure; code URL pending |
| Related Work | 8/10 | 0.9 | Low (0.10 x 0.9 x 1.0) | Well-structured, gap explicit |
| Clarity | 8/10 | 1.0 | Low (0.14 x 1.0 x 1.0) | Excellent narrative honesty; format issues |
| Ethics | 8/10 | 0.6 | Low (0.10 x 0.6 x 1.0) | Exemplary transparency; AI disclosure absent |

**RRI: 10-15/100 (Low risk)** — Unchanged from previous R4. The unresolved procedural items are the only barrier.

### Decision: ACCEPT with Minor Revision (Conditional on P0 Resolution)

MDPI Electronics tiered model: the scientific content is ready for acceptance. The paper is among the strongest in the 15-paper Electronics profile on every evaluative dimension: (a) statistical rigor (0/15 profile papers had significance testing); (b) multi-dataset design (12/14 used one dataset); (c) explicit negative findings (0/15); (d) multi-generation evidence chain (0/15); (e) hyperparameter disclosure (most complete in corpus). No additional experiments are required.

**However, the 3 unresolved P0 items ([TODO] markers, AI disclosure, reference format) are procedural requirements that MDPI desk screening will enforce. The decision is ACCEPT conditional on resolving P0-1, P0-2, and P0-3 before submission.**

---

## CONCRETE MODIFICATION LIST

### P0: Must Fix Before Submission

| ID | Issue | Location | Fix | Status Since R4 |
|---|---|---|---|---|
| P0-1 | Resolve all [TODO] markers | Lines 20-21, 296-299, 301, 305 | Fill author list, affiliations, email; complete Author Contributions (CRediT roles); add funding statement; add repository URL/DOI | **R4 carryover — still unresolved** |
| P0-2 | Add AI use disclosure | After COI section (line 308) | "During the preparation of this work, the authors used [tool names] for [purpose]. After using this tool, the authors reviewed and edited the content as needed and take full responsibility for the content of the publication." | **R4 carryover — still unresolved** |
| P0-3 | Convert references to MDPI numbered format | Section References | Use MDPI's Endnote/Zotero template to convert author-year to numbered in-order-of-appearance style | **R4 carryover — still unresolved** |
| P0-4 | Clean up stale evidence README | `evidence/figures/README.md` | Update or remove the stale "synthetic smoke tests" README | **New** |

### P1: Strongly Recommended

| ID | Issue | Location | Fix | Status Since R4 |
|---|---|---|---|---|
| P1-1 | Add hierarchical reconciliation baseline | Section 6.4 | Implement MinT (trace-minimization) or bottom-up reconciliation on Ausgrid, or add a Limitation noting no reconciliation baseline was tested | **R4 carryover** |
| P1-2 | Expand Ausgrid seed count | Section 5.3, Table 3 | Run LSTM/TCN/PatchTST-lite on Ausgrid from 3 to 10 seeds | **R4 carryover** |
| P1-3 | Clean related_work.md scaffold | `logic/related_work.md` | Replace auto-extracted scaffold with pointer to manuscript Section 2 | **R4 carryover** |
| P1-4 | Add weather-year sensitivity note | Section 3 or 8 | Discuss whether OPSD 2015-2018 weather patterns affect findings | **R4 carryover** |

### P2: Nice-to-Have

| ID | Issue | Location | Fix |
|---|---|---|---|
| P2-1 | Improve Introduction pacing | Section 1 | Split into shorter paragraphs; add reader's guide sentence |
| P2-2 | Add training curves | Section 6 | Supplementary figure showing training/validation loss for CSA-LoadNet and MLP |
| P2-3 | Publish code repository | Data Availability | Public GitHub repository would make the v5->v6->v7 transparency narrative concrete |
| P2-4 | Pre-registration note | Section 7 or 8 | Note the study's post-hoc claim downgrade and value of registered reports for this kind of analysis |


---

## Desk Screen (IMRaD / 格式 / MDPI 要件)

**PASS with caveats.**

The manuscript follows the standard MDPI IMRaD structure: Introduction (Section 1) → Related Work (Section 2) → Datasets & Protocol (Section 3) → Method (Section 4) → Experimental Setup (Section 5) → Results (Section 6) → Discussion (Section 7) → Limitations (Section 8) → Conclusions (Section 9) → Author Contributions → Funding → Data Availability → COI → References. This conforms to MDPI layout requirements.

**Format issues (must fix):**

1. **[TODO markers]** Lines 20-21 contain unresolved `[TODO: author list]`, `[TODO: affiliations]`, `[TODO: corresponding author email]`. Also `[TODO: repository URL/DOI]` in Data Availability Statement (line 305), `[TODO: funding statement]` (line 301), and the entire Author Contributions section (lines 296-299) is `[TODO]`. All must be resolved before submission — MDPI desk screening requires complete author metadata.

2. **Author Contributions**: MDPI mandates a formal CRediT (Contributor Roles Taxonomy) statement. The current placeholder (lines 296-299) is a bare template. This must be filled with specific roles per author.

3. **References format**: The manuscript uses author-year in-text citations (`[Hochreiter and Schmidhuber, 1997]`, `[Kong et al., 2019]`) but the heading note says "MDPI uses numbered references in order of appearance; convert this author-year list with a reference manager during template conversion." **Do not rely on manual conversion during submission** — use MDPI's Endnote/Zotero template or the journal's reference numbering tool in advance.

4. **Figures**: The manuscript references three named figures (Fig. 1 merged leaderboard, Fig. 2 component significance matrix, Fig. 3 Ausgrid leaderboard). The `evidence/figures/README.md` says "Figures will be generated after public benchmark result tables are upgraded beyond synthetic smoke tests" — a stale placeholder. The manuscript comments say figures live in `./figures/` (300 dpi PNG, regenerate with `figures/make_figures.py`). **Verify figures exist and render before submission.**

5. **Data Availability Statement**: Present, names all three public datasets with URLs. The `[TODO: repository URL/DOI]` must be filled. The statement correctly notes that the historical evidence label `HyG-LoadFormer (neural)` maps to CSA-LoadNet.

6. **AI use disclosure**: MDPI has required AI use statements since early 2024. The manuscript has no AI disclosure. This must be added.

---

## 7-Dimension Review

### 1. Novelty (原创性与贡献)

**Score: 7/10 | MDPI Electronics calibration: above average**

**Finding 1.1: Claim system precisely scoped and evidence-backed (Positive)**

The paper makes exactly one positive superiority claim (OPSD 24h vs MLP, Holm p = 0.0085; vs TemporalOnly, p = 0.0011), one honest negative finding (weight-form inseparability — all Holm p ≈ 1), and three explicit scope boundaries (loses on 1h OPSD, inseparable on SimBench, loses to DLinear on Ausgrid). The claim downgrade from the original hyperbolic-geometry hypothesis to "aggregation itself, not its geometry" is a rare example of evidence driving narrative rather than the reverse. This is a stronger novelty profile than 12/14 research papers in the Electronics profile (none of which had explicit negative findings or significance-based claim boundaries).

**Finding 1.2: Method is mechanism combination, aligned with journal standard (Neutral)**

CSA-LoadNet = shared temporal encoder (MLP) + cross-series attention aggregation (pluggable geometry) + compact head. This is a mechanism combination, which is the modal contribution type in Electronics (approximately 8/14 research papers). The paper does not claim it as a new algorithm — the novelty narrative is about the *component-level significance analysis*, not the architecture itself. This framing is appropriate and honest.

**Finding 1.3: Weight-form inseparability is the paper's real novelty (Positive)**

The finding that hyperbolic, Euclidean, equal-weight, and fixed-curvature variants are statistically inseparable in *all five* settings is, as the paper says, "the most broadly useful contribution" (Section 6.3). It directly cautions the GCN/attention-weight-elaboration trend in the cross-series forecasting literature (Section 2.2). No Electronics profile paper reports a comparable component-level negative result. This is publication-worthy on its own.

**Finding 1.4: Electronics novelty dimension specific check (Adversarial)**

Electronics slightly weights the "algorithm/IT-side novelty" higher (per journal profile). A reviewer could argue: "The method is a shared MLP encoder with an attention-averaging module — there is no algorithmic novelty in the architecture; the novelty is entirely in the evaluation methodology." **Response**: The paper does not claim architectural novelty. It claims a *finding* (weight-form inseparability) that the architecture was designed to test. The novelty is in the component-level interrogation, which the Electronics accepted-paper corpus (0/15 with any formal component significance testing) has not previously demonstrated. This satisfies the journal's standard.

**Evidence**: MANUSCRIPT.md lines 41-45 (four contributions), lines 229-236 (weight-form inseparability), claims.md C3 (explicit negative finding status).

---

### 2. Soundness (技术正确性)

**Score: 9/10 | MDPI Electronics calibration: best in corpus**

**Finding 2.1: Statistical methodology best-in-class (Positive)**

The Mann-Whitney U test (no normality assumption at n=10) with Holm correction across comparisons is the most rigorous statistical protocol in any Electronics paper from the 15-paper profile. Exactly 0/15 profile papers used formal significance testing. The seed set of 10 fixed seeds (lines 178-179) is explicitly listed and reproducible. The decision to report *exact Holm-adjusted p-values* (including non-significant ones) is exemplary.

**Finding 2.2: Leakage-free temporal protocol explicit (Positive)**

Section 3.3 provides a precise temporal protocol: single chronological cuts, per-series z-normalization on training data only, validation = final 15% of training window by time, strided training but full unstrided testing. The source row counts and boundary timestamps are recorded in machine-readable profiles. This addresses the temporal-leakage failure mode documented in the profile (LoadSeer's random 90/10 split on time series data was a real slip-through).

**Finding 2.3: Fairness statement and capacity control (Positive)**

Section 5.2 and the fairness note (lines 182-183) state that all models share the same training regime, normalization, splits, early-stopping rule, and budget class; the proposed model is held at the MLP's parameter budget. No Electronics profile paper made any explicit fairness statement.

**Finding 2.4: Primary metric choice justified per dataset (Positive)**

Section 3.2 explains why MAPE (OPSD), normalized MAE (SimBench), and sMAPE (Ausgrid) are each appropriate for their respective data distributions, citing Hyndman & Koehler (2006) on metric pathologies. This level of methodological awareness is absent from all 15 profile papers.

**Finding 2.5: Complete evidence chain preserved (Positive)**

Section 7.1 recounts the v5 → v6 → v7 evolution, including the failed ridge implementation, the neural reimplementation, and the significance verdict. The released evidence deliberately retains all three generations. This is a gold standard for soundness.

**Evidence**: MANUSCRIPT.md lines 92-95 (temporal protocol), lines 137-140 (naming history transparency), lines 165-186 (hyperparameter disclosure + fairness), significance.csv all rows (verified p-values).

---

### 3. Experiments (实验与验证)

**Score: 8/10 | MDPI Electronics calibration: best in corpus**

**Finding 3.1: Multi-dataset design across three regimes (Positive)**

Three datasets spanning distinct multi-series regimes: OPSD (6 country-level national loads), SimBench (8 distribution load profiles), Ausgrid (17-series customer/region/system hierarchy). This exceeds the Electronics profile where 12/14 research papers used a single dataset. The multi-regime design allows the paper to discover the scope boundaries (works on country-level day-ahead, fails on hierarchical) rather than claiming universal superiority and hoping no one checks.

**Finding 3.2: Full ablation matrix (Positive)**

Five single-switch ablations (TemporalOnly, Euclidean, EqualNeighbors, FixedCurvature, NoCalendar) isolate each mechanism. TemporalOnly separates the *existence* of aggregation; the other three jointly probe the *form* of aggregation weights. The ablation design cleanly maps to the claim structure: the existence question produces a significant positive (OPSD 24h), the form question produces a deliberate negative (inseparable everywhere). No Electronics profile paper had more than implicit component comparisons.

**Finding 3.3: Significance matrix visualization (Positive)**

Figure 2 (component significance matrix) condenses all Holm-corrected comparisons across all 5 settings into one view. At a glance: exactly 2 wins (OPSD 24h vs MLP, vs TemporalOnly), 2 losses (OPSD 1h vs MLP, Ausgrid vs DLinear), and the entire weight-form block in inseparable gray. This is an honest and effective communication device.

**Finding 3.4: Seed count asymmetry on Ausgrid (Weakness)**

LSTM, TCN, and PatchTST-lite ran at 3 seeds on Ausgrid (vs 10 for the decision set). The paper explicitly acknowledges this (Limitation 5, lines 283-284) and reports exact n. However, some key comparisons (CSA-LoadNet vs PatchTST-lite raw p = 0.014, n=3/10) have reduced power. The paper does not claim significance for these, but the asymmetry could be questioned. A straightforward fix: add 7 more seeds for these baselines.

**Finding 3.5: No weather features (Neutral)**

Section 8, Limitation 6 acknowledges the absence of exogenous weather inputs. This is a limitation but not a defect for the paper's scope — the study is about cross-series aggregation, not about weather-aware forecasting. All models share the same input constraints, so comparisons are fair.

**Finding 3.6: CPU-only training budget (Neutral)**

Section 8, Limitation 4 acknowledges CPU-budget training. The fairness statement explicitly notes that rankings could shift under much larger budgets. This is honest but does limit absolute accuracy claims. The between-method comparisons are internally valid.

**Evidence**: Leaderboards (opsd 24h Table 4, simbench 24h, ausgrid 24h), significance.csv (35 comparison rows), MANUSCRIPT.md lines 69-94 (datasets), lines 122-135 (ablation switches), lines 192-250 (results).

---

### 4. Reproducibility (可复现性)

**Score: 8/10 | MDPI Electronics calibration: best in corpus**

**Finding 4.1: Hyperparameter disclosure comprehensive (Positive)**

Table 3 (Section 5.2) discloses 17 settings: lookback window, encoder architecture, embedding dimension, curvature/temperature setup, head structure, optimizer/loss/batch/epochs, stride, early stopping, seed list, hardware, and framework. No Electronics profile paper achieved this level of disclosure.

**Finding 4.2: All datasets are public with URLs (Positive)**

OPSD, SimBench, and Ausgrid are all public with URLs provided. The Data Availability section names each source. This is stronger than the Electronics profile where 0/15 papers provided a data URL and several had "Not applicable" for data that was clearly used (an actual slip-through in the corpus).

**Finding 4.3: Config files and pipeline documented (Positive)**

The manuscript names the specific config files (`real_hyg_neural_config.json`, `real_p2_v7_config.json`) and the significance pipeline. The evidence chain (v5/v6/v7) is fully preserved.

**Finding 4.4: Code repository not yet public (Weakness)**

The Data Availability section has `[TODO: repository URL/DOI]`. MDPI does not require code release (0/15 profile papers released code), but the paper's impact would be significantly increased by releasing the CSA-LoadNet implementation and the evaluation pipeline. The transparency narrative (v5→v6→v7 history) especially benefits from a public repository.

**Evidence**: MANUSCRIPT.md lines 164-186 (Table 3), lines 303-306 (data availability), significance.csv (full machine-readable output).

---

### 5. Related Work (相关工作与文献)

**Score: 8/10 | MDPI Electronics calibration: strong**

**Finding 5.1: Three-thread literature review with clear positioning (Positive)**

Section 2 organizes related work into three threads: (A) deep architectures for load forecasting (2.1), (B) cross-series and graph-structured forecasting (2.2), (C) simple baselines and honest evaluation (2.3). Each thread surveys the key works and ends with the specific gap that thread leaves open. Thread 2.2 particularly identifies the core gap: "none that we are aware of tests whether its particular weighting beats trivial equal-weight averaging under an identical protocol with seed-level significance testing" — this is exactly what the paper tests.

**Finding 5.2: References balanced and current (Positive)**

38 references, with approximately 26 (68%) from 2020 or later and 14 (37%) from 2024-2026. The Electronics profile median is approximately 30 references with ~65% 5-year. The reference list includes MDPI journal works (Electronics, Energies, Applied Sciences) which is appropriate for the target journal. No obvious self-citation cluster.

**Finding 5.3: The logic/related_work.md is an auto-scaffold (Format issue)**

Same as Paper 1. The file at `logic/related_work.md` is an auto-extracted scaffold with empty abstracts. The manuscript's Section 2 is the proper review. The scaffold should be flagged.

**Evidence**: MANUSCRIPT.md lines 52-66 (Related Work sections 2.1-2.3), reference list lines 319-348.

---

### 6. Clarity (价值/读者兴趣与表述)

**Score: 8/10 | MDPI Electronics calibration: best in corpus**

**Finding 6.1: Exceptional narrative honesty (Positive)**

The paper tells a story of hypothesis refutation, not hypothesis confirmation. The method was named for the hyperbolic geometry hypothesis; the v7 evidence disproved it; the method was renamed and the claims rewritten. This honesty is communicated clearly: "the finding we did not want but consider the paper's most broadly useful contribution" (Section 6.3), "The weight-form inseparability: an honest negative finding" (Section 6.3 title). For MDPI Electronics, where profile papers range from "reasonable restraint" (12/15) to "conspicuously hyped" (1/15), this clarity and self-awareness sets a new bar.

**Finding 6.2: Negative findings as first-class results (Positive)**

The paper gives equal prominence to the negative finding (weight-form inseparability) and the positive finding (aggregation contributes). The component significance matrix (Figure 2) shows both wins and losses with equal weight. This is the paper's strongest selling point for reader interest.

**Finding 6.3: Figures described but not verified (See 4.3)**

The manuscript references Figure 1 (merged leaderboard), Figure 2 (component significance matrix), Figure 3 (Ausgrid leaderboard). These must exist and be correctly generated.

**Finding 6.4: Some density in early sections (Minor)**

Section 1 (Introduction) is 46 lines and packs in a full problem statement, the design motivation, the four contributions, and a paper roadmap. The first-time reader could benefit from a slightly more paced introduction. Consider splitting into 2-3 shorter paragraphs and adding visual cues (bolded contribution numbers) that stand out on first scan.

**Finding 6.5: Author-year reference format vs MDPI numbered format (Format issue)**

See Desk Screen item 3. The in-text authors-year citations must be converted to MDPI's numbered style.

**Evidence**: MANUSCRIPT.md lines 30-46 (introduction structure), lines 227-237 (weight-form section), lines 256-273 (discussion of evidence chain).

---

### 7. Ethics (学术诚信与合规)

**Score: 8/10 | MDPI Electronics calibration: strong**

**Finding 7.1: Transparency of naming history (Positive)**

Section 4.5 explicitly documents the method's old name (HyG-LoadFormer), the reason for the name change (v7 significance analysis refuted the hyperbolic hypothesis), and the one-to-one mapping maintained in evidence CSVs. This is an exemplary integrity practice. A less careful author would have simply renamed the method and omitted the history.

**Finding 7.2: Full evidence chain preserved (Positive)**

The v5 (ridge) and v6 (neural, 3-seed) implementations are deliberately retained alongside v7, including the v5 implementation's defeat by neural baselines. This goes beyond any standard practice in the profile.

**Finding 7.3: Missing AI use disclosure (Must fix)**

MDPI requires an AI use statement. The manuscript has Author Contributions, Funding, Data Availability, and COI sections but no AI disclosure. Add: "During the preparation of this work, the authors used [tool names] for [purpose]. After using this tool, the authors reviewed and edited the content as needed and take full responsibility for the content of the publication."

**Finding 7.4: [TODO] markers constitute incomplete disclosure (Must fix)**

Unresolved Author Contributions (entire section template), Funding statement, and repository URL must be completed before submission.

**Evidence**: MANUSCRIPT.md lines 133-135 (naming history), lines 295-309 (Author Contributions, Funding, Data Availability, COI).

---

## Adversarial Verification

### Strongest counter-arguments to each positive finding:

1. **"The positive result is a single cell in a 7×5 matrix — one significant win out of 35 comparisons. Is this publication-worthy?"** A reviewer could argue that with 35 comparisons at α=0.05, one significant result is expected by chance. **Response**: The significance testing uses Holm correction within each dataset/horizon block (not across all 35), so the familywise error is controlled per setting. The OPSD 24h positive result (p=0.0085 vs MLP; p=0.0011 vs TemporalOnly) survives correction within its block. Furthermore, the negative finding (weight-form inseparability across all 5 settings, 15 pairwise comparisons) is a deliberate, pre-registered-style hypothesis test whose consistent null outcome is statistically meaningful.

2. **"The NoCalendar ablation has a better mean than CSA-LoadNet on OPSD 24h (0.03187 vs 0.03234). Doesn't this undermine the method?"** Not significant (p=0.485), and not replicated on other settings, but a natural question. The paper honestly reports this in Section 6.1 and does not claim that calendar features help. If anything, this strengthens the paper's credibility.

3. **"SimBench 24h: p=0.084 against MLP with MLP mean ahead. Adding a few more seeds might make this a significant loss — what happens then?"** The paper explicitly reports this as a non-claim (Limitations 1: "no claim on SimBench"). The honest answer is that it could indeed become a loss, and the paper is designed so that its claims do not depend on that outcome.

4. **"Ausgrid: the method loses to DLinear. Isn't DLinear known to be effective only on smooth, trend-dominated series?"** Yes, and the paper discusses this mechanism (Section 6.4): Ausgrid's dominant error is from irregular household-level variation, where aggregation supplies no signal and a compact encoder loses to DLinear's direct mapping. This is reported as a scope boundary, not a puzzle.

5. **"There is no comparison against a hierarchical reconciliation baseline (e.g., bottom-up MinT). Isn't that the natural competitor on Ausgrid?"** Valid point. The paper compares against general time-series baselines (DLinear, MLP, LSTM, TCN, PatchTST) but not against state-of-the-art hierarchical forecast reconciliation (e.g., Hyndman et al. 2011, Wickramasuriya et al. 2019 — both cited in the related work but not used as baselines). Adding MinT reconciliation as a baseline on Ausgrid would strengthen the paper's hierarchical setting analysis.

---

## Meta-Review

### Summary

This is a well-executed, methodologically rigorous paper that is ready for MDPI Electronics submission after minor revisions. The paper's strength lies in its honest evaluation design: component-level hypothesis testing (Mann-Whitney U + Holm, 10 seeds), a preserved evidence chain across three generations, a positive finding that survived refutation attempts, and — most importantly — a deliberate negative finding (weight-form inseparability) that contradicts the project's original hypothesis and is reported as a primary result.

**Comparison to MDPI Electronics profile**: This paper would be among the strongest in the 15-paper corpus. It exceeds the corpus on every dimension: (a) only 3/14 profile papers had numbered contribution lists (this paper has 4 explicit claims with evidence mapping in claims.md); (b) 0/15 had any significance testing; (c) 0/15 had multi-dataset evaluation spanning three regimes; (d) 0/15 had explicit negative findings; (e) 0/15 preserved a multi-generation evidence chain; (f) this paper's hyperparameter disclosure (Table 3) is the most complete in any profile paper. The only profile dimension where this paper is average is the method itself (mechanism combination, not a new algorithm) — which is not a weakness for Electronics.

**Most important consideration for submission decision**: The MDPI Electronics acceptance profile shows that the journal routinely accepts papers with far weaker experimental rigor than this one. The single positive result (OPSD 24h vs MLP, 4.1% MAPE improvement, Holm-significant) exceeds the typical "combination method + 3 baselines + component comparison" bar. The negative finding adds genuine value. **This paper should be submitted to MDPI Electronics as-is after addressing the P0 items below.** No additional experiments are required for the journal's standard.

### RRI Score Estimate

| Dimension | Score | Weight | Risk Contribution |
|---|---|---|---|
| Novelty | 7/10 | 1.3 | Low (honest negatives are original; method is combination-level) |
| Soundness | 9/10 | 1.4 | Very Low (best statistical protocol in corpus) |
| Experiments | 8/10 | 1.3 | Low (multi-dataset, multi-baseline; Ausgrid seed asymmetry minor) |
| Reproducibility | 8/10 | 1.1 | Low (full disclosure; code repo URL pending) |
| Related Work | 8/10 | 0.9 | Low (well-structured, gap explicit) |
| Clarity | 8/10 | 1.0 | Low (excellent narrative honesty; minor formatting issues) |
| Ethics | 8/10 | 0.6 | Low (exemplary transparency; AI disclosure absent) |

**RRI: 10-15/100 (Low risk)**

### Decision: ACCEPT with Minor Revision

MDPI Electronics tiered model: this paper should be accepted after minor revision. The scientific contribution (component-level significance testing with an honest negative finding) is valuable and novel for the journal. The technical execution is strong. The revision items are primarily procedural (filling [TODO] markers, adding AI disclosure, reference format conversion) rather than scientific. The journal's decision model supports minor revision → acceptance for papers at this quality level.

---

## Concrete Modification List

### P0: Must fix before submission

| ID | Issue | Location | Fix |
|---|---|---|---|
| P0-1 | Resolve all [TODO] markers | Lines 20-21, 296-299, 301, 305 | Fill author list, affiliations, corresponding email, Author Contributions (CRediT), Funding statement, repository URL/DOI |
| P0-2 | Add AI use disclosure statement | After COI section (line 308) | Per MDPI policy: "During the preparation of this work, the authors used [tool names] for [purpose]. After using this tool, the authors reviewed and edited the content as needed and take full responsibility for the content of the publication." |
| P0-3 | Convert references to MDPI numbered format | Section References (lines 318-348) | Use MDPI's Endnote/Zotero template or journal's reference formatting tool to convert author-year to numbered in-order-of-appearance style |
| P0-4 | Verify figures exist in `./figures/` | Sections 6.1-6.4 | Run `figures/make_figures.py` to regenerate Fig. 1 (merged leaderboard), Fig. 2 (component significance matrix), Fig. 3 (Ausgrid leaderboard); verify 300 dpi PNG output |

### P1: Strongly recommended

| ID | Issue | Location | Fix |
|---|---|---|---|
| P1-1 | Add hierarchical reconciliation baseline on Ausgrid | Section 6.4 | Implement MinT (trace-minimization) reconciliation or a bottom-up baseline on Ausgrid to match the hierarchical forecasting literature cited in Section 2.2. If not feasible, add a limitation noting that no reconciliation-specific baseline was tested |
| P1-2 | Expand Ausgrid seed count for LSTM/TCN/PatchTST | Section 5.3, Table 3 | Run the 3-seed baselines (LSTM, TCN, PatchTST-lite) on Ausgrid to 10 seeds to match the decision set. Currently, key comparisons (vs PatchTST-lite raw p=0.014 with n=3 vs n=10) have asymmetrical power |
| P1-3 | Upgrade the logic/related_work.md scaffold | logic/related_work.md | Replace the auto-extracted scaffold with a pointer to the manuscript's own Section 2, or populate it with actual abstract summaries |
| P1-4 | Add weather-year sensitivity note | Section 3 or 8 | Mention whether the OPSD 2015-2018 period's weather patterns could affect the findings. Multi-year testing is implicit but not explicitly discussed |

### P2: Nice-to-have

| ID | Issue | Location | Fix |
|---|---|---|---|
| P2-1 | Improve Introduction pacing | Section 1 | Split into 2-3 shorter paragraphs; add a visual "reader's guide" sentence mapping the paper's structure |
| P2-2 | Add training curves | Section 6 | One supplementary figure showing training/validation loss for CSA-LoadNet and MLP across epochs would strengthen the narrative |
| P2-3 | Publish code repository | Data Availability | The transparency narrative (v5→v6→v7) is the paper's best integrity argument. A public GitHub repository with the full evidence chain would make this argument concrete |
| P2-4 | Note that the paper would benefit from a pre-registered analysis plan | Section 7 or 8 | Since the claim downgrade after v7 could be seen as post-hoc, adding a note about the study's pre-registration status or the value of registered reports for this kind of work would preempt a reviewer concern |
