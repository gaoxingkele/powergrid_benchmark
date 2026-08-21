# C²GES Round 3 Final Methodology and Statistics Audit

## Final decision

**Methodology/statistics: Acceptable after minor editorial correction.** Confidence: **5/5**.

There is no remaining statistical or numerical issue that requires a new experiment or changes the reported negative result. The Round 2 attribution and complexity blockers are closed against the latest TeX and frozen code.

## Final blocker classification

| Category | Status | Decision impact |
|---|---|---|
| Scientific/statistical validity for the manuscript's bounded claims | **closed** | No blocker |
| Algorithm/code concordance | **closed** | No blocker |
| Multiplicity and uncertainty reporting | **closed** | No blocker |
| Practical/operational validity | **open by design** | Blocks stronger maintenance/deployment claims, but not the manuscript's explicitly bounded proxy-corpus claims |
| Public reproducibility release | **open submission operation** | Repository must be synchronized, tagged, archived, and fresh-clone verified before submission |
| Editorial clarity | **minor** | Non-blocking; label the Table `tab:contrasts` tail column “unadjusted descriptive `t_boot`” if space permits |

## Round 2 closure verification

### 1. Unrenormalized no-CF ablation — closed

- **Evidence anchors:** Introduction contribution statement; Section 3.1 and Table `tab:claim-evidence-map`; Section 3.5 lines 241--245; Table `tab:tuning-opportunity`; RQ2 answer at line 522.
- The manuscript now defines the estimand exactly: set `C_i` from 0.15 to zero while holding all other absolute coefficients and operations fixed.
- It discloses that positive-channel weight changes from 1.00 to 0.85 while the redundancy coefficient remains 0.50.
- Arithmetic is correct: `0.50/0.85=0.588235`; relative to 0.50 this is `(0.588235/0.50)-1=0.17647`, reported as 17.6% larger.
- The text no longer presents this as pure information-only isolation and explicitly includes relative-scale coupling. No result was rerun or cosmetically improved.

### 2. Edge semantics and complexity — closed

- **Evidence anchors:** Section 3.3 lines 183--191; Section 3.5 line 249; frozen `R2_v0_3/v03_methods.py`, `build_causal_graph`, lines 75--90.
- Absolute distance, nonchronological role-directed edges, and the formula
  `round_12[0.45 exp(-d/5)+0.30 J+0.25 min(r_i,r_j)]`
  match frozen code.
- The manuscript now states that the implementation screens all ordered source--target pairs in `O(n^2)` time and applies the distance gate after that scan.
- The admitted-neighbor bound is sound for unique sentence positions: for `n>=13`, ordered pairs within distances 1--12 number `2 sum_{d=1}^{12}(n-d)=24n-156`, hence “approximately 24n apart from boundary effects” is conservative.

## Full numerical and multiplicity audit

1. The corrected toy path strengths sum to `2.218228`; the root subtotal is `1.308523`.
2. All seven-condition macro-means remain consistent with the immutable 210-row ledger.
3. The six registered paired mean differences and report-composition intervals are unchanged and correctly finite-set/descriptive.
4. Exact enumeration over `2^15=32,768` signs reproduces all six post-run p-values. Holm adjustment reproduces `0.436768, 0.001526, 0.000732, 0.401367, 0.026367, 0.028931`.
5. Output-length differences remain correct from unrounded means: 103.0/214.5 words versus Semantic-MMR and 110.7/199.9 versus TextRank.
6. No minimum important difference, equivalence margin, or qualified-reader outcome is claimed; non-rejection is not treated as equivalence.
7. The negative Full-minus-no-CF result remains visible in Abstract, Results, Discussion, and Conclusions.

## Minor non-blocking wording note

The abstract and a few historical labels still say “strict no-CF” or “incremental value,” but the operative estimand and coupling are explicit in Methods, the claim map, the tuning table, and the RQ2 answer. This is not a validity blocker. For maximum consistency, “registered unrenormalized no-CF” should replace “strict no-CF” wherever layout permits. Table `tab:contrasts` should also identify its final column as unadjusted; no inferential claim currently depends on that column.

## Final verdict

The current negative component conclusion, finite-corpus system descriptions, and auditability claims follow from the reported design. Physical causal identification, length-controlled superiority, maintenance usefulness, and deployment safety remain unsupported and are appropriately excluded. From a methodology/statistics perspective, the paper can proceed to final editorial/build checks without rerunning experiments.
