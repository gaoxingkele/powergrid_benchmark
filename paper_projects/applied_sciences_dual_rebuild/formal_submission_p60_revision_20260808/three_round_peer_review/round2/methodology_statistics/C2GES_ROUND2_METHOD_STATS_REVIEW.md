# C²GES Round 2 Methodology and Statistics Re-Review

## Decision

**Major Revision remains.** Confidence: **5/5**. Round 1 remediation is strong: 9 of 10 substantive items are closed or acceptably bounded. Two newly visible method-description problems remain major.

Status meanings: **closed** = revision fully addresses the prior finding; **partial** = material improvement but residual ambiguity remains; **open** = not addressed or a new decision-relevant problem.

## Round 1 issue traceability

| ID | Status | Severity | Evidence anchor in revised TeX | Round 2 finding / required action |
|---|---|---|---|---|
| R1-M1 equal-sentence/unequal-word estimand | **closed** | Major | Introduction RQ1, line 37; Section 4.3, Table `tab:length-audit`; Section 4.6, line 516 | RQ1 now asks for a descriptive equal-sentence comparison and explicitly includes word imbalance. Results retain the 54--63% qualification. |
| R1-M2 population interpretation of intervals | **closed** | Major | Section 3.7; Table `tab:contrasts`, caption/header; Section 4.4, paragraph beginning “The bootstrap intervals…” | The estimand is now the unweighted mean paired difference across the 15 retained reports, and intervals are named report-composition intervals, not population CIs. |
| R1-M3 practical significance | **closed** | Major | Section 4.4, line 428 | The text explicitly states that no minimum important difference or qualified-reader outcome exists and that practical significance/equivalence are unidentifiable. |
| R1-M4 tuning asymmetry | **closed** | Major | Section 3.6, Table `tab:tuning-opportunity` | The table gives 144 configurations for Full, fixed/default opportunities for baselines, identifies no-CF as the mechanism comparator, and states that selection uncertainty is excluded. |
| R1-M5 theoretical meaning of deletion | **closed** | Major | Section 3.4, Equations (1)--(2), proposition paragraph at line 208 | The revision correctly defines non-negativity, nullity, and path additivity under fixed weights/path membership and denies causal identification. |
| R1-M6 cross-report dependence | **closed as limitation** | Major | Section 5.4, line 556 | Revised-edition, boilerplate, and near-duplicate dependence are now explicitly untested; report independence is not asserted. No new evidence is invented. |
| R1-m1 toy arithmetic | **closed** | Minor | Section 3.4, line 210 | Direct recomputation matches `U(G)=2.218228` and root subtotal `1.308523`. |
| R1-m2 “rules out extremes” wording | **closed** | Minor | Section 4.4, line 476 | Replaced by the defensible statement that signs were not confined to a few reports. |
| R1-m3 bootstrap-tail column clarity | **partial** | Minor | Section 3.7, Equation (4); Table `tab:contrasts` | The caption says the quantity is descriptive and not a p-value, but the manuscript still mentions a registered Holm transformation without displaying it and labels the column only “Registered `t_boot`.” Add “unadjusted” to the column/caption and state that the unused adjusted values remain provenance only. |

## New major finding: the strict no-CF contrast changes relative regularization scale

- **Status:** open
- **Severity:** Major
- **Evidence anchors:** Section 3.5, Equation (3), lines 231--237; Section 3.6, Table `tab:tuning-opportunity`; Table `tab:claim-evidence-map`, RQ2 row.
- **Observed implementation:** Full uses channel weights summing to 1.00 and subtracts a fixed redundancy penalty of `0.50 × max Jaccard`. Strict no-CF sets the 0.15 coefficient on `C_i` to zero, does not renormalize the remaining weights, and leaves the redundancy coefficient at 0.50.
- **Implication:** The no-CF base-score scale has total nominal weight 0.85. Relative to that scale, the unchanged redundancy penalty is `0.50/0.85=0.5882`, approximately **17.6% stronger** than 0.50. Therefore Full-minus-no-CF does not isolate only path-deletion information; it estimates the joint effect of adding `C_i` **and** changing the salience-to-redundancy scale. Calling it a strict single-channel causal attribution is too strong.
- **Required fix without rerunning:** Rewrite RQ2, Table `tab:claim-evidence-map`, Table `tab:tuning-opportunity`, Results, Discussion, and Conclusion to define the estimand exactly as **the effect of setting the registered `C_i` coefficient from 0.15 to zero while all other absolute coefficients remain fixed**. State that this includes relative-scale coupling with the redundancy term. Replace “isolates the implemented perturbation channel” with “removes the channel under the registered unrenormalized scoring rule.” A future preregistered study should include both unrenormalized and renormalized ablations, but no retrospective number should be invented now.

## New major finding: corrected edge semantics expose a false complexity claim

- **Status:** open
- **Severity:** Major
- **Evidence anchors:** Section 3.3, edge formula and edge-gate paragraphs at lines 183--191; Section 3.5 computational-cost paragraph at line 249; frozen `R2_v0_3/v03_methods.py`, `build_causal_graph`, lines 75--90.
- **Verified correction:** The latest manuscript now matches the frozen code on edge semantics: `d_ij` is absolute position distance, source-role sentences need not precede target-role sentences, and `w_ij=round_12[0.45 exp(-d_ij/5)+0.30 J_ij+0.25 min(r_i,r_j)]`. This correction is **closed and accurate**.
- **Residual contradiction:** The complexity paragraph still says that at most `12n` forward neighborhoods are checked instead of all `O(n^2)` pairs. The frozen code loops over every source node and every target node before testing distance, so implemented edge construction performs an `O(n^2)` ordered-pair scan. With unique positions and an absolute 12-position horizon, at most about `24n` ordered pairs can survive the distance gate, but the code still screens all pairs.
- **Required fix without rerunning:** Replace the complexity claim with the actual algorithm: quadratic ordered-pair screening, followed by a bounded number of admitted local edges and capped path enumeration. Do not claim an optimized sliding-window implementation unless code changes under a new protocol identity; no reported result needs rerunning merely to repair this prose.

## Statistical and arithmetic re-audit

1. The revised toy-path values recompute to 0.566964, 0.741559, 0.367423, and 0.542282; totals are correct.
2. The six mean ROUGE-L differences, report-composition intervals, exact sign-flip values, sign counts, and six-value Holm corrections are unchanged from the immutable ledger and remain arithmetically consistent.
3. Word differences remain consistent with unrounded means: Full minus Semantic-MMR is 103.0 and 214.4667 (reported 214.5); Full minus TextRank is 110.7 and 199.9.
4. The sign-flip sensitivity correctly states its independence/sign-exchangeability assumption and post-run status. No multiplicity defect was introduced.
5. The no-CF interval crossing zero is correctly treated as lack of demonstrated benefit, not equivalence. The new scaling issue weakens component attribution but does not reverse or cosmetically improve the reported negative outcome.

## Round 2 conclusion

Estimand, interval, practical-significance, negative-result, and multiplicity language are now substantially sound. Acceptance from a methodology/statistics perspective requires two targeted revisions: stop calling the unrenormalized no-CF comparison a pure isolated-channel effect, and correct the edge-construction complexity from the claimed local-window scan to the quadratic ordered-pair scan actually implemented. The latest absolute-distance edge formula itself is verified against frozen code. The public repository synchronization statement also remains a submission-time reproducibility gate, although it does not alter the frozen numerical results.
