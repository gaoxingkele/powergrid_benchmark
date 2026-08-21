# Round 1 Cross-Paper Methodology/Statistics Summary

## Overall decision

Both manuscripts require **Major Revision**, not rejection on integrity grounds. Their strongest shared quality is unusually transparent negative-result and provenance reporting. Their shared weakness is that framework novelty is stronger than the available effectiveness evidence.

## Highest-priority revisions

| Priority | C²GES | MA-SQLGrid |
|---|---|---|
| 1 | Recast RQ1 as an equal-sentence, unequal-word finite-set description; no performance superiority | State upfront that no experiment estimates five-role/multi-agent benefit |
| 2 | Rename bootstrap CIs as report-composition sensitivity intervals for 15 selected reports | Add a master protocol/estimand/visibility table for the six heterogeneous studies |
| 3 | Declare practical significance unidentified because no MID or expert endpoint exists | Repair Table `tab:componentcounts` with the paired V1 denominator/numerator (Qwen 101/170) |
| 4 | Treat strict no-CF as the primary controlled mechanism contrast; external baselines are tuning-asymmetric | Put all nine primary factorial estimates, intervals, raw p, and Holm p in the manuscript |
| 5 | Define `C_i` as weighted qualified-path participation, not causal identification | Explain cluster weighting/exchangeability and the low effective cluster counts |
| 6 | Add unresolved cross-report duplication/dependence to leakage limitations | Narrow “prospective” and separate unequal-call BIRD B3 from call-matched comparisons |
| 7 | Correct synthetic `U(G)` from about 2.217 to about 2.218 | Synchronize and immutably archive the public repository before submission |

## Shared statistical judgment

- Both papers report effect estimates and adverse outcomes better than many benchmark papers, but neither defines a smallest practically important effect.
- Non-rejection must not be interpreted as equivalence. This matters especially for C²GES Full versus no-CF and MA-SQLGrid’s wide component intervals.
- Multiplicity handling is generally explicit: six-value Holm in C²GES; named protocol-specific families in MA-SQLGrid. MA-SQLGrid must expose the full primary family in the main manuscript rather than only selected p-values.
- Both use selected/development-visible resources. Their intervals should be framed as finite-corpus composition sensitivity, not population confidence.
- Neither paper has qualified domain-expert semantic validation. Therefore ROUGE overlap, execution equality, mutation denial, and metamorphic invariance must remain separate from engineering usefulness or correctness.

## Arithmetic audit outcome

C²GES’s six exact sign-flip values and Holm corrections reproduce from the immutable 15-report ledger. One minor synthetic-example error was found: the unrounded path strengths sum to `U(G)=2.218228`, not approximately 2.217. MA-SQLGrid’s factorial effects, call/state counts, tie distributions, rescue/harm arithmetic, and reported BIRD adjusted values reconcile. Its main reproducibility defect is presentational: the E1 paired V1 count needed to obtain +0.1059 is not shown in Table `tab:componentcounts`.

## Revision gate for Round 2

Round 2 should verify four concrete outcomes: (1) RQs and conclusions use only licensed estimands; (2) all primary denominators, intervals, multiplicity families, and analysis units are visible; (3) causal/robust/multi-agent terminology is tied to formal tested properties; and (4) no caveat is weakened while improving readability. No new experimental number is necessary to satisfy these Round 1 findings, although genuinely new unseen-data validation would be required for stronger application claims.
