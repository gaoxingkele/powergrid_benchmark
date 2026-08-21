# MA-SQLGrid Round 3 Final Methodology and Statistics Audit

## Final decision

**Methodology/statistics: Acceptable after submission-operation closure.** Confidence: **5/5**.

The six component effects, three Holm families, pointwise-interval interpretation, and cross-protocol cluster assumptions are now explicit and arithmetically consistent. No new multiplicity error or favorable-result inflation was introduced.

## Final blocker classification

| Category | Status | Decision impact |
|---|---|---|
| Scientific/statistical validity for bounded software/finite-corpus claims | **closed** | No blocker |
| Five-role efficacy evidence | **absent and explicitly excluded** | Blocks a five-role superiority claim, not the current software-conformance paper |
| Qualified power-grid semantic validity | **open by design** | Blocks operational/domain-efficacy claims, not the current bounded claims |
| Public reproducibility release | **open submission operation** | Immutable repository release and fresh-clone verification are required before submission |
| Numerical/multiplicity consistency | **closed** | No blocker |

## Round 2 closure verification

### 1. Six component effects and paired counts — closed

- **Evidence anchors:** Results Section 4.3; Tables `tab:componentcounts` and `tab:component-effects`.
- E1 paired Qwen: `83/170 -> 101/170`, difference `18/170=0.105882`, printed 0.1059.
- E1 paired Granite: `69/170 -> 69/170`, difference 0.
- E2 effects reconcile with rescue/harm: Qwen `(8-1)/180=0.038889`; Granite `(10-0)/180=0.055556`.
- All six retained intervals match the component analysis artifact to printed precision.

### 2. Three Holm families — closed

- **Evidence anchor:** Table `tab:component-effects` and paragraph at line 476.
- Family E1 contains the Qwen and Granite E1 effects. Raw p-values 0.01552 and 1.00000 yield Holm p-values 0.03104 and 1.00000.
- Family E2 contains the Qwen and Granite selector effects. Raw 0.50080 and 0.06425 yield Holm 0.50080 and 0.12850.
- Family Cross-E contains the E1 and E2 backbone modifiers. Raw 0.26986 and 0.37477 yield Holm 0.53971 for both.
- Family membership is now reconstructible from the manuscript and matches the retained analysis.

### 3. Pointwise intervals versus multiplicity — closed

- **Evidence anchors:** Section 4.2 line 422; Table `tab:component-effects` caption; line 476.
- The text explicitly states that composition intervals are pointwise sensitivity summaries, not simultaneous intervals and not inversions of Holm tests.
- It correctly explains why Granite E2's pointwise interval `[0.0075, 0.1232]` can exclude zero while Holm p=0.12850 does not meet the registered family rule.

### 4. Cluster/randomization assumptions — closed

- **Factorial:** 70 normalized-SQL groups, 58 singletons, maximum size 19; question-weighted estimand, group-sign exchangeability assumption, proxy status disclosed.
- **Components:** 61/70 group mappings retain question weighting; signs assigned at frozen group level; exchangeability treated as an assumption.
- **Formal-v5:** question-weighted logical-AND endpoint, 12 group-sign assignments, exact `2^12=4096`, coarse resolution and proxy status disclosed.
- **BIRD:** equal item weighting over 500 items; one common sign per database; 11 database clusters; 12-comparison Holm family; database-level exchangeability and non-grid limitation disclosed.

## Complete arithmetic and multiplicity audit

1. The nine factorial effects recompute from the eight 180-item cells. Their raw/Holm p-values and canonical-v3 pointwise composition intervals match retained tables.
2. Zero of nine primary factorial effects survives Holm; no contrary wording was introduced.
3. Secondary structural-adherence effects remain clearly labeled manipulation checks.
4. `1440×18=25,920` and `180×8×4=5,760` are correct.
5. Replay multiplicities sum to 180; 173 have at least two unique candidates, 172 at least two eligible candidates.
6. Tie distributions reproduce 130 tied questions and mean multiplicities 5.4000/5.3889.
7. Offline arithmetic remains `80+22-2=100` and `80+23-2=101`; +1/180 is explicitly a mechanism trace.
8. BIRD accuracies, pairwise deltas, and 12-value Holm results remain consistent; B3 remains separated as a two-call unequal-budget workflow.
9. Negative evidence is retained: component E2 non-rejection for both backbones, all nine multi-state Holm values 1.0, no Granite BIRD contrast surviving, and strong v3 order sensitivity.

## Final verdict

The manuscript now supports software conformance, bounded SQLite enforcement, named-state completeness, finite-corpus prompt/component observations, and outcome-exposed historical-pool diagnostics. It does not support five-role superiority, universal robustness, expert-certified grid semantics, or deployment safety, and the text consistently excludes those claims. No experiment rerun is required for statistical closure. Before submission, the exact repository must be synchronized, licensed, immutably tagged/archived, and verified from a fresh clone.
