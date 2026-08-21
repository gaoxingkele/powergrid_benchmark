# MA-SQLGrid Round 2 Methodology and Statistics Re-Review

## Decision

**Major Revision remains, with a narrower statistical revision list.** Confidence: **5/5**. Most high-impact Round 1 findings are closed. Remaining issues concern full multiplicity specification, complete component precision, cross-protocol cluster assumptions, and public reproducibility.

## Round 1 issue traceability

| ID | Status | Severity | Evidence anchor in revised TeX | Round 2 finding / required action |
|---|---|---|---|---|
| R1-M1 no five-role efficacy experiment | **closed** | Major | Abstract; Introduction RQ1 and Contributions; first Results paragraph, line 359 | RQ1 is now software conformance, and the manuscript repeatedly states that no experiment estimates five-role benefit. |
| R1-M2 dispersed estimands/protocols | **closed** | Major | Section 3.3, Table `tab:protocol-master` | The six protocols now expose unit, N, dependence proxy, calls, endpoint, visibility, status/multiplicity, and claim ceiling. |
| R1-M3 E1 paired denominator | **closed** | Major | Section 4.3, line 429; Table `tab:componentcounts` | Qwen V0 83/170 and paired V1 101/170 reproduce `(101-83)/170=0.105882`; Granite 69/170 versus 69/170 reproduces zero. All-item 180 rows are separated. |
| R1-M4 complete nine-test factorial family | **closed with one presentation caveat** | Major | Section 4.2, Table `tab:factorial-nine` | All nine estimates, intervals, raw p, Holm p, 70 groups, and 100,000 draws are shown. Add one sentence that composition intervals are pointwise sensitivity intervals and are not simultaneous/familywise-adjusted; otherwise their zero exclusion can appear inconsistent with Holm non-rejection. |
| R1-M5 cluster assumptions/effective information | **partial** | Major | Table `tab:protocol-master`; Section 4.2, line 419; Methods Sections 3.6--3.7 | The 70-group GridDB analysis is now clear: 58 singletons, maximum 19, question weighting, proxy status, and sign exchangeability are stated. Equivalent detail is still absent for the 61-group E1, 12-group multi-state, and 11-database BIRD analyses. State weighting/statistic construction and exchangeability for each protocol, not only GridDB factorial. |
| R1-M6 practical significance/equivalence | **closed** | Major | Section 4.2, line 421; Discussion/Conclusion | No MID, equivalence, or non-inferiority margin is claimed; +1/180 remains a mechanism trace. |
| R1-M7 overbroad “prospective” | **closed** | Major | Abstract; Table `tab:protocol-master`; Section 4.3 and Figure `fig:components` | Revised to “prospectively frozen call-and-selection procedure on development-visible GridDB items.” |
| R1-M8 unequal-call BIRD B3 | **closed** | Major | Table `tab:protocol-master`; Section 4.5 and Table `tab:bird` | B0--B2 use one call, B3 two; B3 is visually separated and explicitly not a call-matched repair effect. |
| R1-M9 public reproducibility | **open** | Major | Supplementary Materials; Data Availability Statement | The repository still “must be synchronized and tagged before submission.” Close by publishing an immutable, licensed, fresh-clone-verified release and recording its tag/commit/archive DOI. |
| R1-m1 “equal budget” | **closed** | Minor | Table `tab:offline` | Replaced by “same precomputed candidate/evidence ledger.” |
| R1-m2 order sensitivity | **closed** | Minor | Table `tab:sensitivity`; Discussion | Reverse-order 117--118 remains explicitly outcome-exposed and non-preferred. |
| R1-m3 abstention interpretation | **partial** | Minor | Section 4.6; Table `tab:ties` | The high tie rate is exposed, but the zero-abstention result should explicitly be called a consequence of stable-order forced resolution rather than confidence-calibrated coverage. |
| R1-m4 terminology | **closed** | Minor | RQ3; Tables `tab:protocol-master` and `tab:offline` | “Complete-three-witness selector” replaces overbroad coordination terminology in the main quantitative surfaces. |

## Remaining major statistical issues

### S1. Component multiplicity families are not reconstructible from the manuscript

- **Status:** open
- **Severity:** Major
- **Evidence anchors:** Methods Section 3.6, lines 317--327; Table `tab:protocol-master`, Component row; Results Section 4.3.
- **Problem:** The Methods refer to “the component family,” the master table says “registered families,” and Results refer to an E2 “two-test Holm family,” but the manuscript never enumerates family membership. The retained analysis shows three two-value families: E1 across the two backbones, E2 across the two backbones, and the two cross-backbone modifiers. This cannot be inferred safely from the printed text alone.
- **Fix:** Add a component multiplicity table or sentence explicitly listing each family, its two members, raw p-values, and Holm-adjusted p-values. Do not merge or redefine families after the fact; report the retained frozen grouping exactly.

### S2. Component precision remains incomplete in the main manuscript

- **Status:** partial
- **Severity:** Major
- **Evidence anchors:** Results Section 4.3, lines 429--431; Table `tab:componentcounts`.
- **Problem:** Only the Qwen E1 interval is numeric. Granite E1 is described merely as spanning zero, and neither E2 interval nor either cross-backbone interval is printed. Retained values are: Granite E1 `[-0.1902, 0.1705]`; Qwen E2 `[-0.0081, 0.1071]`; Granite E2 `[0.0075, 0.1232]`; cross-backbone E1 `[-0.2701, 0.0394]`; cross-backbone E2 `[-0.0062, 0.0457]`.
- **Fix:** Add a six-row component-effect table with estimate, composition interval, raw p, Holm p, question N, group count, and family identifier. These are retained results, not new experiments. This is important because Granite E2 has a pointwise interval above zero while its multiplicity-adjusted rule is not met.

### S3. Pointwise intervals and Holm decisions need explicit reconciliation

- **Status:** partial
- **Severity:** Major
- **Evidence anchors:** Table `tab:factorial-nine`; Section 4.2 lines 419--425; Section 4.3.
- **Problem:** Several composition intervals exclude zero while the corresponding Holm decision does not reject. This is possible because the intervals are unadjusted composition-sensitivity summaries, not simultaneous inferential intervals, but the manuscript does not say this directly.
- **Fix:** Add one explicit statement after each effect table: “Intervals are pointwise composition-sensitivity intervals and are not inverted from, or adjusted to match, the Holm family.” Preserve both quantities without treating one as an error.

## Arithmetic and multiplicity re-audit

1. Table `tab:factorial-nine` estimates recompute exactly from the eight 180-question cells. Raw and Holm p-values match `canonical_v3_inference_hierarchy/tables/core_inference_hierarchy.csv` to printed precision.
2. Its displayed intervals match the current canonical v3 composition-sensitivity table, including Qwen hint `[0.0548, 0.4355]` and three-way modifier `[0.0090, 0.4321]`; they differ slightly from an older v2 bootstrap artifact, so the manuscript should identify canonical v3 as the source.
3. E1 paired counts and +0.1059 arithmetic now reconcile. E2 rescue/harm arithmetic remains `(8-1)/180=0.0389` and `(10-0)/180=0.0556`.
4. `1440×18=25,920`, `180×8×4=5,760`, the 332 retained failures, tie distributions, and `80+22-2=100` / `80+23-2=101` remain consistent.
5. BIRD cell accuracies, pairwise deltas, and 12-value Holm results remain consistent. B3 is correctly treated as unequal-call evidence.
6. Negative findings remain intact: zero of nine primary GridDB factorial tests passes Holm, both E2 selectors miss their registered rule, all nine multi-state adjusted values are 1.0, and no Granite BIRD contrast survives correction.

## Round 2 conclusion

The revised paper now has a defensible finite-corpus evidence hierarchy and does not overclaim five-role efficacy. Statistical closure requires: (1) enumerate the component Holm families, (2) print all six component estimates/intervals/p-values, (3) explain that composition intervals are pointwise rather than familywise, and (4) extend cluster weighting/exchangeability descriptions beyond the 70-group factorial analysis. Public repository synchronization remains an external submission blocker.
