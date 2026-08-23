# C2GES Balanced Development-Tuning Protocol

Status: frozen before executing the development sweep on 2026-08-23. The historical retained-test outcomes were already known. This sweep is restricted to the 12 development reports and selects configurations only for a future unseen-series experiment.

## Shared data, budgets, and objective

- Development JSONL: 12 reports, SHA-256 `27CE41D37D8BA7B0BBA9D80072B3A3FAC742CEB4997E30DF0BE40CC5B2DF7F79`.
- Frozen MiniLM snapshot/revision and lexical graph implementation are unchanged.
- Every method receives exactly nine evaluated configurations.
- Every configuration is evaluated at K=5 and K=10 on all 12 reports.
- Ordered selection objective: highest mean ROUGE-L across all 24 report--budget cells; then highest mean ROUGE-1; then lowest mean redundancy; then earliest registered grid index.
- No retained-test file is an input to the script.

## Nine-configuration grids

### Semantic-MMR

`lambda` in `{0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90}` with relevance weight `lambda` and maximum-selected-cosine penalty `1-lambda`.

### TextRank

PageRank damping `alpha` in `{0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95}`, with 100 iterations, tolerance `1e-8`, and the frozen weighted-degree fallback.

### C2GES

Path-deletion weight in `{0.000, 0.025, 0.050, 0.075, 0.100, 0.125, 0.150, 0.175, 0.200}`. For every value `w`, the four non-path weights retain their historical ratios and are scaled to sum to `1-w`:

- relevance: `(0.40/0.85)*(1-w)`;
- role: `(0.20/0.85)*(1-w)`;
- graph: `(0.15/0.85)*(1-w)`;
- position: `(0.10/0.85)*(1-w)`.

The redundancy penalty remains 0.50. Candidates, graph construction, path horizon/work bounds, role reservation, and tie rules are unchanged.

## Outputs and boundary

Report per-configuration development metrics, selected configuration identities, exact code/model/data hashes, and the equal nine-configuration budget. Public outputs contain IDs and metrics but no candidate, reference, or prediction text.

The selected configurations must not be evaluated on the already observed retained test and must not replace historical reported configurations. Their only authorized use is preregistration before an external series-disjoint evaluation.
