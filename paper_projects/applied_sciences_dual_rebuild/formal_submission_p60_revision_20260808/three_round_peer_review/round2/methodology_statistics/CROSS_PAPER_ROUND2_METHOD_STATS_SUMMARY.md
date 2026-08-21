# Cross-Paper Round 2 Methodology/Statistics Summary

## Outcome

Round 1 revisions materially improved both manuscripts. No favorable result was fabricated, no negative result was removed, and the reported arithmetic remains largely consistent. Both papers remain at **Major Revision** for a small number of decision-relevant residual issues.

## Closure matrix

| Manuscript | Closed | Partial | Open/new major |
|---|---:|---:|---:|
| C²GES | Equal-sentence estimand; composition-interval wording; practical-significance boundary; tuning table; path-functional proposition; dependence limitation; toy arithmetic; sign wording | Bootstrap-tail column provenance | Unrenormalized no-CF ablation changes the redundancy penalty’s relative scale, so it is not a pure isolated-channel effect |
| MA-SQLGrid | Software-conformance RQ; no five-role efficacy claim; master protocol table; paired E1 counts; nine-row factorial table; practical-significance boundary; prospective wording; unequal-call B3; shared-ledger wording; selector terminology | Cross-protocol cluster assumptions; component precision; zero-abstention interpretation; pointwise interval wording | Component Holm family membership is not reconstructible from the manuscript; public immutable repository release remains absent |

Additional C²GES code-concordance audit: the revised absolute-distance edge formula is closed and matches frozen `v03_methods.py`, but the complexity prose remains open because it claims `12n` forward checks whereas the frozen nested loops screen all ordered node pairs in `O(n^2)` time.

## Highest-priority Round 2 fixes

1. **C²GES:** redefine RQ2/ablation claims as the effect of setting `C_i` from 0.15 to zero under the unrenormalized fixed-coefficient rule. Because the base-channel sum changes from 1.00 to 0.85 while the redundancy penalty stays 0.50, its relative strength rises to 0.5882, about 17.6%. Do not claim pure channel isolation.
2. **C²GES:** retain the corrected absolute-distance/edge-weight formula, which matches frozen code, but replace the false `12n` forward-neighborhood complexity statement with the implemented `O(n^2)` ordered source--target scan; the distance gate only bounds admitted local pairs.
3. **MA-SQLGrid:** add the six-row component effect table and explicitly enumerate the three frozen two-value Holm families.
4. **MA-SQLGrid:** state that composition intervals are pointwise sensitivity intervals, not simultaneous intervals corresponding to Holm decisions; extend weighting/exchangeability descriptions to E1, multi-state, and BIRD clusters.
5. **Both:** synchronize/tag/archive and fresh-clone verify the exact public repositories before submission. This is a reproducibility gate, not permission to alter results.

## Numerical audit summary

- C²GES’s corrected path total, six paired means, six exact sign-flip values, six Holm corrections, and length differences all reconcile with retained artifacts.
- MA-SQLGrid’s nine factorial estimates/p-values/intervals match the current canonical v3 tables; E1 paired counts now reproduce +0.1059; factorial, call/state, rescue/harm, tie, and BIRD arithmetic remain consistent.
- Negative evidence remains preserved in both papers. Round 2 requests only attribution and reporting corrections; it does not request post hoc tuning or a new favorable experiment.
