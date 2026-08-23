# C2GES claim--evidence audit

Date: 2026-08-23
Scope: `01_Manuscript/LaTeX/paper_applsci.tex` after the 0823 revision analyses.

| Claim family | Manuscript treatment | Evidence | Verdict |
|---|---|---|---|
| `outperform` / `superior` | No unqualified method-superiority statement retained | Equal-unit results are explicitly paired with the 54--63% output-length mismatch and tuning asymmetry | PASS |
| `effective` / `effectiveness` | Operational maintenance effectiveness is explicitly not established | No expert task-utility or maintenance-record experiment exists | PASS |
| `engineering reading aid` | Presented as motivation/intended role, not a demonstrated outcome | No qualified-reader trial exists; abstract now denies operational reading benefit | PASS |
| `reproducible` | Removed from abstract, keyword and conclusion as an unconditional core claim | Public verification rebuilds tests/data/LaTeX, but restricted source text prevents complete public regeneration | PASS |
| `sentence` | Candidate units are no longer silently equated with clean sentences | Output-length diagnostic identifies fused table/heading/footnote/line-break units | PASS |
| `counterfactual` | Physical/causal interpretation is denied; the manuscript uses `path-deletion term` | Code tests establish structural non-identity only | PASS |
| `improve` | Path deletion is explicitly reported as not improving the predefined ROUGE-L endpoint | Full-minus-strict deltas are negative at both budgets; zero weight won 12/12 development folds | PASS |
| baseline lexical advantage | Restricted to observed equal-unit, unequal-length results | Report-level deltas plus post-run series and 110/260-word sensitivities; every matched-word series interval crosses zero | PASS with limitation retained |
| balanced tuning | Not retroactively applied to retained test | Equal-nine development program selected MMR 0.9, TextRank 0.65, normalized path 0.0 and records `test_input_accessed=false` | PASS for future configuration only |
| embedding robustness | No general robustness or preferred encoder claimed | 29/9504 test candidates exceed 256 tokens; 512/chunk diagnostics change few same-corpus selections and all four Holm values equal 1.0 | PASS as post-run diagnostic |
| layout validity | No human-validity upgrade | Block audit reduces long-unit incidence and reports 0 table-detection failures, but is heuristic and not used for ranking | PASS as diagnostic; external gate remains open |
| source faithfulness / structure validity | Explicitly unverified | No independent expert annotation | PASS as limitation; external gate remains open |
| portability | Restricted to a `portable public verification subset` | Python 3.12 public verifier passes code/data/main and supplementary LaTeX checks with explicit restricted skips | PASS |

## Residual prohibited upgrades

- Do not change “auditable implementation” back to “validated engineering aid” or unconditional “reproducible system”.
- Do not describe lexical roles, typed edges or path deletion as expert-validated causal structure.
- Do not use the series sensitivity to claim a fresh confirmatory test.
- Do not treat equal-unit baseline differences as matched-length superiority.
- Do not state external maintenance generalization until rights-cleared external data and qualified expert evaluation exist.
