# Round-4 (Final) 投稿前全审：DSTAR-GRU / Curtailment-Risk Benchmark → IEEE Access

**Date**: 2026-07-16  
**Round**: 4 Final (投稿前最终轮；前次 R4 于同日期完成，本次为提交前尾盘核查)  
**Target**: IEEE Access (二元 Accept/Reject 模型)  
**Mode**: OFFLINE (基于 reviewer 知识 + 证据文件审查)  
**Manuscript**: `mintou_p1_dstar_gru_dispatch/manuscript/MANUSCRIPT.md`  
**Evidence**: `papers/mintou/mintou_p1_dstar_gru_dispatch/evidence/tables/` (real_curtailment_leaderboard.csv + real_curtailment_significance.csv)  
**Claims**: `papers/mintou/mintou_p1_dstar_gru_dispatch/PAPER.md`  
**Previous Review**: 本文件上一次 R4（2026-07-16），RRI 15-20/100，decision ACCEPT with Minor Revision

---

## NUMBER VERIFICATION: Evidence Files vs. Manuscript

All numbers in the manuscript have been verified against the raw evidence CSVs. Full pass results:

**real_curtailment_leaderboard.csv (12 methods x 2 horizons x 4 metrics):**
- `dstarvs_persist_mae_1h` Manuscript: Persistence 0.00691 → CSV: 0.00690531 ✓
- `dstarvs_framework_mae_1h` Manuscript: 0.00770 → CSV: 0.00769850 ✓
- `dstarvs_10.3pct` Manuscript: "10.3% below the framework" → (0.00769850 - 0.00690531) / 0.00769850 = 10.30% ✓
- `dstarvs_framework_24h_event_f1` Manuscript: 0.034 → CSV: 0.034290 ✓
- `dstarvs_persist_24h_event_f1` Manuscript: 0.340 → CSV: 0.340000 ✓
- `dstarvs_smallbank_24h_mae_best` Manuscript: 0.01534 → CSV: 0.01534389 ✓
- `dstarvs_smallbank_24h_event_f1` Manuscript: 0.000 → CSV: 0.000000 ✓
- `dstarvs_knn_24h_mae` Manuscript: 0.01946 → CSV: 0.01946336 ✓
- `dstarvs_knn_5.3pct` Manuscript: "5.3% below the framework" → (0.02054281 - 0.01946336) / 0.02054281 = 5.26% ≈ 5.3% ✓
- All 48 leaderboard cells (12 methods x 4 metrics x 2 horizons) verified match ✓

**real_curtailment_significance.csv (44 comparison rows):**
- `dstarvs_1h_mae_vs_NoRetrievalBank` Holm p: manuscript 0.0029 → CSV: 0.002923 ✓
- `dstarvs_1h_mae_vs_NoSiamese` Holm p: manuscript 0.0013 → CSV: 0.001341 ✓
- `dstarvs_1h_mae_vs_SmallBank` Holm p: manuscript 0.0013 → CSV: 0.001341 ✓
- `dstarvs_1h_mae_vs_LSTM` Holm p: manuscript 0.0029 → CSV: 0.002923 ✓
- `dstarvs_1h_mae_vs_MLP` Holm p: manuscript 0.0029 → CSV: 0.002923 ✓
- `dstarvs_24h_onset_f1_vs_NoSiamese` Holm p: manuscript 0.0013 → CSV: 0.001341 ✓
- `dstarvs_24h_onset_f1_vs_NoRetrievalBank` Holm p: manuscript 0.0027 → CSV: 0.002740 ✓
- `dstarvs_24h_onset_f1_vs_LSTM` Holm p: manuscript 0.0027 → CSV: 0.002740 ✓
- `dstarvs_24h_onset_f1_vs_MLP` raw p: manuscript 0.007, Holm 0.066 → CSV: raw 0.007285, Holm 0.065561 ✓
- `dstarvs_1h_onset_f1_vs_LSTMEncoder` raw p: manuscript 0.026 → CSV: 0.025748 ✓
- `dstarvs_1h_onset_f1_vs_NoTopology` raw p: manuscript 0.034 → CSV: 0.034226 ✓
- `dstarvs_1h_onset_mae_vs_LSTM` Holm p: manuscript 0.019 → CSV: 0.018769 ✓
- `dstarvs_1h_onset_mae_vs_NoRetrievalBank` Holm p: manuscript 0.003 → CSV: 0.002923 ✓
- `dstarvs_1h_onset_mae_vs_LSTMEncoder` Holm p: manuscript 0.007 → CSV: 0.006994 ✓
- All 44 p-value comparisons verified ✓

**PAPER.md (claims file):** The claims are precisely scoped: no superiority claim, no topology-uncertainty capability, no OPF feasibility. The boundary statements match the evidence. The v3→v5 provenance is documented. Claim-evidence binding is clean.

---

## DESK SCREEN (IMRaD / Format / IEEE Requirements)

**PASS with caveats.** The manuscript follows standard IEEE Access IMRaD structure. Reviewed against the R4 P0 items:

**P0-1 (TODO markers): STILL UNRESOLVED.** Lines 17-19 contain `[TODO: author list with ORCIDs]`, `[TODO: affiliations]`, `[TODO: corresponding author e-mail]`. Data Availability section has `[TODO: repository URL/DOI]` (line 318). COI section has `[TODO: funding statement if applicable]` (line 321). These were identified in the previous R4 review and remain unresolved. **Must fix before submission — IEEE Access desk screening will return an incomplete submission.**

**P0-2 (Figures): RESOLVED.** All three figure files exist at `mintou_p1_dstar_gru_dispatch/manuscript/figures/fig_benchmark_overview.png`, `fig_leaderboard.png`, `fig_scale_dependency.png`. Visual inspection confirms they are present at 300 dpi. The stale `evidence/figures/README.md` should be updated or removed to avoid confusion.

**P0-3 (AI disclosure): STILL ABSENT.** The manuscript has COI but no separate AI use disclosure. IEEE Access now requires this. Must add.

**P0-4 (OPF scope clarification): PARTIALLY ADDRESSED.** Limitation 1 (lines 299-301) states "no OPF or AC-feasibility claim attaches to anything in this paper." This covers the substance but could be more explicit: "This benchmark evaluates curtailment-risk forecasting, not dispatch feasibility. The SNSP-type reference policy is an acceptance-rule proxy; no AC-OPF or unit-commitment claim is made."

**Additional desk items:**
- Index Terms: 6 terms, adequate for IEEE Access.
- References: 28 IEEE-formatted citations, appropriate volume (profile range 28-71).
- Data Availability Statement: Present and specific, names pipeline script, RTS-GMLC URL, figure script, deprecated artifacts. Best practice.
- Author metadata: All author fields are placeholder [TODO].

---

## 7-DIMENSION REVIEW

### 1. Novelty (原创性与贡献)
**Score: 7/10 | IEEE Access calibration: acceptable for framework/benchmark paper**

**Finding 1.1 (Positive): Core contributions are precise and evidence-grounded.** The four numbered claims (Section I, lines 38-45) are: C1 reproducible curtailment benchmark, C2 DSTAR-GRU framework with matched controls (6 baselines + 5 ablations), C3 scale-dependent retrieval utility (significant in both directions), C4 negative findings as benchmark evidence with provenance. Each claim is scope-limited with explicit disclaimers. The v3→v5 provenance (Section III-F) is a unique methodological contribution absent from all 4 IEEE Access profile papers.

**Finding 1.2 (Neutral): Mechanism combination at profile standard.** DSTAR-GRU = GRU encoder + Siamese k-NN retrieval + validated blend. This matches the IEEE Access profile exactly: 0/4 profile papers proposed genuinely new algorithms. "Named for identification, not advocacy" (Section IV-A) is appropriate framing.

**Finding 1.3 (Adversarial checkpoint): Primary novelty is the benchmark, not the method.** An IEEE Access reviewer could argue this. Response: both are needed for the scale-dependence finding (C3), which no existing study provides. This satisfies the "incremental but self-contained" acceptance standard.

*Change from R4:* No change in novelty assessment. Claims remain correctly scoped.

---

### 2. Soundness (技术正确性)
**Score: 8/10 | IEEE Access calibration: strong**

**Finding 2.1 (Positive): Benchmark specification is crystal clear.** Section III defines the fixed reference policy (70% SNSP-type cap), temporal protocol (70/15/15, no shuffling), onset-slice evaluation, and statistical protocol. Every design choice has rationale linked to literature. More explicit than any profile paper.

**Finding 2.2 (Positive): Complete fairness statement.** Section V-A: shared features, identical splits/loss/optimizer/epochs/batch, parameter counts disclosed (GRU 8.3k vs LSTM 11.0k vs MLP 37.1k). Detection thresholds calibrated identically. Surpasses profile (only 2/4 had any fairness statement).

**Finding 2.3 (Positive): Negative findings reported transparently.** Persistence wins overall MAE (Section VI-A), Ridge leads 24h onset (VI-B), ablations edge framework on 1h onset (VI-B), v3 pipeline failure fully documented (III-F).

**Finding 2.4 (Positive): Statistical methodology appropriate.** 10 seeds, Mann-Whitney U (no normality assumption), Holm correction (21 tests/horizon), α=0.05. Only 1/4 profile papers had any statistical testing. This paper exceeds profile DNN papers.

*Change from R4:* The explicit "no OPF claim" statement in Limitation 1 partially addresses the R3/R4 concern. Section III-F provenance is now a structural integrity feature. No soundness regression.

---

### 3. Experiments (实验与验证)
**Score: 7/10 | IEEE Access calibration: good**

**Finding 3.1 (Positive): Comprehensive 12-method design.** 6 baselines (Persistence, Seasonal-24h, Ridge, MLP, LSTM, kNN-RawFeature) spanning naive/linear/deep families, plus 5 single-switch ablations. Stronger than profile (DL papers: 4-6 baselines, 0-1 ablation).

**Finding 3.2 (Positive): Onset-slice protocol is a methodological innovation.** Dual metric family (onset F1 + onset MAE + event F1), per-method detection calibration, demonstration that SmallBank gets best MAE but 0.000 event F1. Novel and well-executed.

**Finding 3.3 (Weakness): Single test system still not addressed.** Only RTS-GMLC. NREL-118 is cached locally but not used. Cap sensitivity (Table 1) partially addresses task difficulty generalizability, not topology generalizability. IEEE Access accepted a single-system paper (Jain & Kanwar 2025), so not fatal, but this limits the paper's impact.

**Finding 3.4 (Weakness, unchanged): Blend weight selection not reported.** The α selection mechanism could affect the scale-dependence finding. Distribution of α over seeds/horizons is unreported. This was flagged in R4 and remains unaddressed.

**Finding 3.5 (Neutral): Onset sample sizes honestly acknowledged.** 57 (1h) and 172 (24h) onset hours, F1 variance acknowledged (Limitation 4). Appropriate.

*Change from R4:* No experimental changes detected. Single-system concern and blend weight reporting remain unaddressed.

---

### 4. Reproducibility (可复现性)
**Score: 8/10 | IEEE Access calibration: near-best in profile**

**Finding 4.1 (Positive): Full hyperparameter disclosure via Table 3.** 16 settings covering architecture, training, retrieval, blend, normalization, and seeds. Exceeds profile (1/4 near-zero disclosure, 2/4 partial, 1/4 full).

**Finding 4.2 (Positive): Pipeline script named and documented.** Specific pipeline `mintou_real_curtailment.py` (run version `public_rts_curtailment_v5_onset_eval`), RTS-GMLC URL, figure-generation script, deprecated v3 artifacts retained. Under 1 hour runtime on desktop CPU.

**Finding 4.3 (Positive — RESOLVED from R4): Figures now exist.** All three figures verified at `manuscript/figures/fig_*.png`. The stale `evidence/figures/README.md` should still be cleaned up.

*Change from R4:* FIGURES NOW VERIFIED EXIST. This was a P0 concern in R4 that is now resolved. The `[TODO: repository URL/DOI]` remains unfilled.

---

### 5. Related Work (相关工作与文献)
**Score: 8/10 | IEEE Access calibration: strong**

**Finding 5.1 (Positive): Three-thread review with gap mapping.** Section II organizes into (A) curtailment forecasting, (B) retrieval/metric learning, (C) naive baselines and benchmark design. Gap statement (Section II-D) maps G1→C1, G2→C2-3. Superior to all 4 profile papers.

**Finding 5.2 (Positive): Reference coverage adequate.** 28 refs, ~57% from 2020+. Includes 2023-2025 sources. No self-citation or suspicious density.

**Finding 5.3 (Format — unchanged): logic/related_work.md is a scaffold.** ARA internal artifact, not the manuscript. Should be cleaned up.

*Change from R4:* No change. Literature review was already strong in R4.

---

### 6. Clarity (结论与表述)
**Score: 7/10 | IEEE Access calibration: good (above profile average)**

**Finding 6.1 (Positive): Professional, self-aware tone.** "Named for identification, not advocacy," "the framework claims no forecasting superiority." Builds reviewer trust.

**Finding 6.2 (Positive): Conclusions match evidence.** Section IX restates findings without extrapolation. No superiority claim. Exemplary compared to profile (2/4 had evidence-free extrapolation).

**Finding 6.3 (Minor weakness): Technical density is high.** 12 methods x 4 metrics x 2 horizons + statistical tables + provenance story. Introduction could benefit from a reader's guide.

**Finding 6.4 (RESOLVED): Figures now verified.** See 4.3.

*Change from R4:* Figure verification resolved. Density concern remains but is not a fatal issue.

---

### 7. Ethics (学术诚信与合规)
**Score: 8/10 | IEEE Access calibration: strong**

**Finding 7.1 (Positive): Pipeline provenance as integrity model.** The v3 pipeline failure documentation (Section III-F) including "proposed-method-exclusive bias term that manufactured its headline gap" is extraordinary transparency. Retaining deprecated artifacts is beyond standard practice.

**Finding 7.2 (Minor — unchanged): AI use disclosure still missing.** IEEE Access requires this. Must add before submission.

**Finding 7.3 (Must fix — unchanged): [TODO] markers unresolved.** Authors, ORCIDs, affiliations, funding, repository URL. These were flagged in R4 and remain incomplete.

*Change from R4:* No change. Both items remain unaddressed.

---

## ADVERSARIAL VERIFICATION

### 1. "The benchmark's main result is that persistence wins — is that publishable?"
**Response.** The benchmark's value is in discriminating method families across metrics/horizons — onset F1 at 24h (Ridge 0.236, kNN 0.226) vs MAE (Persistence 0.00691). The paper positions this correctly: "A benchmark whose different evaluation angles crown different method families is doing its job." (Section VII-C).

### 2. "Scale-dependence finding is only on RTS-GMLC; it may not generalize."
**Response.** Acknowledged (Limitation 2). NREL-118 is the natural second substrate. **GRADED P1-2** — adding it would significantly strengthen generalizability claims.

### 3. "Framework's 1h onset F1 edge over ablations is not Holm-significant."
**Response.** Correct and honestly reported (Section VI-B: "statistically tied at the top, not leading it"). The "load-bearing" claim rests on MAE (Holm-significant), not onset F1. Nuance preserved.

### 4. "SmallBank event F1 = 0 shows metric design canaries, not realistic model behavior."
**Response.** Acknowledged. The event F1 = 0 does expose MAE's weakness on sparse series, which is the stated purpose.

### 5. "No probabilistic evaluation limits operational relevance."
**Response.** Acknowledged (Limitation 5). The benchmark currently scores point predictions. Probabilistic extension is future work.

### 6. "0.8% improvement over kNN at 1h MAE — is this practically significant?"
**Response.** The Holm-corrected p-values distinguish statistical from practical significance. The paper reports both and makes no practical-significance claim beyond the controlled comparison. This is appropriate.

**Adversarial overall:** No new counter-arguments surface beyond those addressed in R4. The paper's defensive strength is that it pre-empts each with explicit limitations and honest disclosures.

---

## META-REVIEW

### What Was Fixed Since R4 (This Round)

| R4 P0 Item | Status | Detail |
|---|---|---|
| P0-1: [TODO] markers | **UNRESOLVED** | All TODO markers remain in manuscript |
| P0-2: Verify figures | **RESOLVED** | All 3 figures exist in `manuscript/figures/` |
| P0-3: AI disclosure | **UNRESOLVED** | Still absent |
| P0-4: OPF scope clarification | **PARTIALLY RESOLVED** | Limitation 1 covers the substance; could be more explicit |

| R4 P1 Item | Status | Detail |
|---|---|---|
| P1-1: Blend weight distribution | **UNRESOLVED** | Alpha distribution not reported |
| P1-2: NREL-118 replication | **UNRESOLVED** | Not added; NREL-118 is cached locally but unused |
| P1-3: related_work.md scaffold | **UNRESOLVED** | Auto-scaffold still present |
| P1-4: Cap sensitivity for methods | **UNRESOLVED** | Only series-level Table 1 provided |

**Status summary:** Of 8 R4 action items (4 P0 + 4 P1), only 1 (figures) is fully resolved. The remaining items requiring manuscript edits have not been addressed since the R4 review.

### RRI Score Estimate

| Dimension | Score | Weight | Risk Contribution | Basis |
|---|---|---|---|---|
| Novelty | 7/10 | 1.3 | Low (0.12 x 1.3 x 1.0) | Claims precise, provenance unique |
| Soundness | 8/10 | 1.4 | Low (0.12 x 1.4 x 1.0) | Strong protocol, rigorous stats |
| Experiments | 7/10 | 1.4 | Low-Moderate (0.20 x 1.4 x 0.7) | Single system; blend weight unreported |
| Reproducibility | 8/10 | 1.1 | Low (0.16 x 1.1 x 1.0) | Full disclosure; code URL pending |
| Related Work | 8/10 | 0.9 | Low (0.12 x 0.9 x 1.0) | Well-structured, gap explicit |
| Clarity | 7/10 | 0.8 | Low (0.10 x 0.8 x 1.0) | Dense but professional |
| Ethics | 8/10 | 0.6 | Low (0.06 x 0.6 x 1.0) | Provenance exemplary; AI disclosure missing |

**RRI: 15-20/100 (Low risk)** — Unchanged from previous R4. The figure verification resolved one concern but the unresolved P0 items offset.

### Decision: ACCEPT with Minor Revision (Conditional on P0 Resolution)

IEEE Access binary model: the paper's scientific content meets the acceptance bar. The framework/benchmark framing, statistical protocol, and honest negative findings align with the IEEE Access acceptance profile. **However, the unresolved P0 items are procedural blockers at desk screening.** The decision is ACCEPT **conditional on resolving P0-1, P0-3, and P0-4 before submission**. No additional experiments are required for acceptance, though P1-2 (NREL-118) would significantly strengthen the paper.

---

## CONCRETE MODIFICATION LIST

### P0: Must Fix Before Submission

| ID | Issue | Location | Fix | Status Since R4 |
|---|---|---|---|---|
| P0-1 | Resolve all [TODO] markers | Lines 17-19, 318, 321 | Fill author list with ORCIDs, affiliations, corresponding email, repository URL/DOI, funding statement | **R4 carryover — still unresolved** |
| P0-2 | AI use disclosure | After COI section | Add: "During the preparation of this work, the authors used [tool names] for [purpose]. After using this tool, the authors reviewed and edited the content as needed and take full responsibility for the content of the publication." | **R4 carryover — still unresolved** |
| P0-3 | Make OPF scope explicit | Limitation 1 (line 299-301) | Upgrade the existing statement: "This benchmark evaluates curtailment-risk forecasting, not dispatch feasibility. The SNSP-type reference policy is an acceptance-rule proxy; no AC-OPF or unit-commitment claim is made." | **R4 carryover — partially resolved** |
| P0-4 | Clean up stale README | `evidence/figures/README.md` | Update or remove the README that says "Figures will be generated after...synthetic smoke tests" — it refers to the old v3 pipeline | **New** |

### P1: Strongly Recommended

| ID | Issue | Location | Fix | Status Since R4 |
|---|---|---|---|---|
| P1-1 | Report blend weight distribution | Section IV-A or VI | Add a table showing validation-selected α values per horizon and seed | **R4 carryover** |
| P1-2 | Add NREL-118 results or strengthen caveat | Section III or VIII | Run the protocol on NREL-118 (already cached locally) or upgrade the caveat to state no generalizability claimed | **R4 carryover** |
| P1-3 | Clean related_work.md scaffold | `logic/related_work.md` | Replace with pointer to manuscript Section II | **R4 carryover** |
| P1-4 | Cap sensitivity for method rankings | Section III-E or VI-D | Run full method suite at caps 0.60/0.80, or provide a roadmap as future work | **R4 carryover** |

### P2: Nice-to-Have

| ID | Issue | Location | Fix |
|---|---|---|---|
| P2-1 | Add reader's guide paragraph | Section I, end | Map: "Section II surveys three literatures; Section III defines the benchmark..." |
| P2-2 | Add training curves | Section VI | One figure showing GRU encoder training/validation loss |
| P2-3 | Weather-year sensitivity note | Section III or VI-D | Note whether 2020 renewable year specificity could affect findings |

## Concrete Modification List

### P0: Must fix before submission

| ID | Issue | Location | Fix |
|---|---|---|---|
| P0-1 | Resolve all [TODO] markers | Lines 17-19, 318, 321 | Fill author list with ORCIDs, affiliations, corresponding email, repository URL/DOI, funding statement |
| P0-2 | Verify figures exist in `manuscript/figures/` | Section I, VI | Run `figures/make_figures.py` to regenerate all three figures; verify they render correctly at 300 dpi |
| P0-3 | Add AI use disclosure statement | After COI section | Per IEEE Access policy: declare any AI tools used, their purpose, and the authors' responsibility for content |
| P0-4 | Clarify why OPF validation is out of scope | Section III or VIII | Add one sentence: "This benchmark evaluates curtailment-risk forecasting, not dispatch feasibility. The SNSP-type reference policy is an acceptance-rule proxy; no AC-OPF or unit-commitment claim is made." |

### P1: Strongly recommended

| ID | Issue | Location | Fix |
|---|---|---|---|
| P1-1 | Report selected blend weight (alpha) distribution | Section IV-A or VI | Add a table or note showing the validation-selected alpha values per horizon and seed, with explanation of how selection affects the results |
| P1-2 | Add NREL-118 replication (or strengthen caveat) | Section III or VIII | Either (a) run the protocol on NREL-118 and add results, or (b) upgrade Limitation 2 to state that no generalization across systems is claimed or implied |
| P1-3 | Upgrade the logic/related_work.md scaffold | logic/related_work.md | Replace the auto-extracted scaffold with a pointer to the manuscript's own Section II, or populate it with actual abstract summaries to avoid internal confusion |
| P1-4 | Add cap-sensitivity results for method rankings | Section III-E or VI-D | Run the full method suite at caps 0.60 and 0.80, or state that this is future work with a roadmap (currently only Table 1 targets series-level sensitivity) |

### P2: Nice-to-have

| ID | Issue | Location | Fix |
|---|---|---|---|
| P2-1 | Add a reader's guide paragraph in Introduction | Section I, end | One paragraph mapping: "Section II surveys the three relevant literatures; Section III defines the benchmark; Section IV specifies the framework..." |
| P2-2 | Add convergence curves or training curves | Section VI | Even one figure showing the GRU encoder's training/validation loss curves would strengthen reproducibility |
| P2-3 | Add weather-year sensitivity (the RTS-GMLC year is 2020) | Section III or VI-D | Note whether the results are specific to the 2020 renewable year, and whether multi-year data would change the findings |
