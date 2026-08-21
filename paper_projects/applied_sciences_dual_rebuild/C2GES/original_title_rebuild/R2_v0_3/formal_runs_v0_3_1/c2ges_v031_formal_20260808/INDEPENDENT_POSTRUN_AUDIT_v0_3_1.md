# Independent Post-Run Audit — C2GES v0.3.1

## Material Passport

- Audit mode: independent, read-only post-run validation
- Audit date: 2026-08-08 (Asia/Shanghai)
- Formal run: `c2ges_v031_formal_20260808`
- Protocol: `C2GES-NERC-FORMAL-v0.3.1-post-audit-corrective`
- Verification status: `ANALYZED_POSTRUN_OUTPUT`
- Verdict: **PASS**
- Evidence class: **post-audit corrective descriptive; not fresh confirmatory, preregistered, or outcome-unseen evidence**
- Prohibited action respected: the formal runner was not rerun; the freeze, registry, and formal outputs were not modified.

## Verdict

The sole registered v0.3.1 attempt is mechanically complete, hash-bound to the authorized freeze and pretest audit, structurally complete, and internally reproducible from the frozen prediction ledger. All 28 aggregate metric means and all six registered paired-bootstrap/Holm contrast records were independently recalculated from `predictions.jsonl` and matched the published JSON values exactly (maximum absolute difference `0`). No missing, non-finite, out-of-range, duplicate-key, failed, or partial prediction record was found.

This PASS validates the integrity of the retained post-run output. It does **not** upgrade the experiment to fresh confirmatory evidence and does not establish that the counterfactual channel improves over the strict no-counterfactual ablation.

## Run-Control and Binding Checks

| Check | Independent result |
|---|---:|
| Registry entries | 1 (`attempt.json`) |
| Formal output directories | 1 |
| Registry status | `COMPLETE` |
| `run_state.json` status | `COMPLETE` |
| `manifest.json` status | `COMPLETE` |
| Registry transition | `CLAIMED` timestamp retained; terminal `COMPLETE` timestamp retained |
| Authorized physical attempts | 1 |
| Freeze-verification checks recorded at execution | 77/77 passed |
| Currently frozen files independently rehashed | 31/31 matched |
| Registry → authorization binding | PASS |
| Registry → freeze binding | PASS |
| Registry → output-manifest binding | PASS |
| Authorization → pretest decision binding | PASS |
| Pretest decision → independent pretest audit binding | PASS |

Binding SHA-256 values:

- Freeze: `DE3205B0BC8DF65706B40B696F7313953E5905AA875128B569EECB685DAB19B5`
- Authorization: `BB9DDE1CE7FBA3D24C742ECEEA5F86936038AFD78BC7064901500E82FA097C2C`
- Pretest decision: `5D9C5E9DA41ABC2E243532A9EAF2E310F2819E96F10117ECE952970C8B50A894`
- Independent pretest audit: `AEE22F61229704A89B747D6DDA659BE36A0CD92E92BCDD1A44828FDAAB25A048`
- Output manifest: `7B209F55ED774BF2A5CC5D060D5ABD865BE951E1455DD7253E2AE962265254D9`

## Structural and Data-Integrity Checks

- `210 = 15 reports × 7 conditions × 2 budgets` prediction rows were present.
- Every `(doc_id, condition, budget)` key was unique; each report had exactly 14 rows.
- All 210 rows were marked `split=test`.
- The prediction document set exactly equaled the 15-document frozen test set.
- The 12 development and 15 test document IDs had zero intersection.
- Every selected sentence ID/text pair matched its source test candidate.
- Every prediction was the exact ordered join of its selected sentences.
- Selection lengths equaled K=5 or K=10, with no duplicate sentence IDs.
- All ROUGE-1, ROUGE-2, ROUGE-L, and redundancy values were finite and in `[0,1]`.
- Candidate pages remained strictly after the reference-summary pages in all 15 test reports; no normalized exact reference-summary/candidate match was found.
- Frozen dataset SHA-256 values matched: development `27CE41D37D8BA7B0BBA9D80072B3A3FAC742CEB4997E30DF0BE40CC5B2DF7F79`; test `A9342BD75BB5E20B61C9B06FE21B1FBA260347BFDB77B0AEBBA89A423DFCD127`.

## Independent Aggregate Recalculation

All values below are macro-means over 15 reports and exactly match `aggregate_metrics.json`.

| K | Condition | ROUGE-1 | ROUGE-2 | ROUGE-L | Redundancy |
|---:|---|---:|---:|---:|---:|
| 5 | C2GES full | 0.235876 | 0.061120 | 0.106044 | 0.074534 |
| 5 | graph no-CF strict | 0.249729 | 0.064810 | 0.109376 | 0.079794 |
| 5 | Semantic-MMR | 0.178282 | 0.043259 | 0.085307 | 0.023694 |
| 5 | TextRank | 0.150845 | 0.035607 | 0.080606 | 0.255985 |
| 10 | C2GES full | 0.336612 | 0.087390 | 0.127636 | 0.066689 |
| 10 | graph no-CF strict | 0.347123 | 0.093006 | 0.130996 | 0.074643 |
| 10 | Semantic-MMR | 0.283974 | 0.072833 | 0.113276 | 0.026948 |
| 10 | TextRank | 0.247013 | 0.061510 | 0.115607 | 0.214895 |

The complete 28-value comparison (7 conditions × 2 budgets × 4 metrics) had maximum absolute discrepancy `0`.

## Independent Registered Contrast Recalculation

The independent calculation used report-level paired deltas, 10,000 bootstrap samples, seeds `20260808 + 100K + contrast_index`, percentile intervals, the registered two-sided tail estimator, and Holm step-down correction across all six tests.

| K | C2GES full minus | Mean Δ ROUGE-L | 95% bootstrap CI | raw p | Holm p |
|---:|---|---:|---|---:|---:|
| 5 | graph no-CF strict | -0.003332 | [-0.010889, 0.002826] | 0.3544 | 0.3544 |
| 5 | Semantic-MMR | 0.020737 | [0.012765, 0.028354] | 0.0000 | 0.0000 |
| 5 | TextRank | 0.025438 | [0.017542, 0.033722] | 0.0000 | 0.0000 |
| 10 | graph no-CF strict | -0.003360 | [-0.008306, 0.001040] | 0.1444 | 0.2888 |
| 10 | Semantic-MMR | 0.014360 | [0.006082, 0.022215] | 0.0008 | 0.0032 |
| 10 | TextRank | 0.012029 | [0.004397, 0.019241] | 0.0022 | 0.0066 |

All fields in all six contrast records matched `primary_contrasts_holm.json` exactly. The two `p=0.0000` results had zero smaller-tail draws among 10,000 registered resamples. They must be described as **“registered bootstrap p < 0.0002; zero smaller-tail draws in 10,000 resamples”**, not as a true probability of zero. The machine artifact correctly retains the registered estimator's raw value `0.0`.

## Counterfactual and Baseline Checks

- Full and strict no-CF base scores were non-identical in all 30 report-budget comparisons.
- Across 19,008 sentence-score comparisons, 9,774 had nonzero full-minus-no-CF differences; the maximum absolute difference was `0.150000`.
- The selected sentence sequence differed in 28/30 report-budget comparisons.
- Full rows retained counterfactual weight `0.15`; strict no-CF rows set only that weight to `0.0`, with all registered non-CF weights unchanged.
- Semantic-MMR was present for all 30 report-budget cases with local frozen MiniLM embeddings, lambda/relevance/redundancy coefficients all `0.5`, and complete per-step selection audits.
- The counterfactual path traversal was independently counted for all 15 test graphs. Maximum expansions were `19,638 / 2,000,000`; maximum qualifying paths were `16,182 / 250,000`. No limit was approached or triggered, and the completed output contained no fail-closed path exception.

Crucially, C2GES full was numerically below strict no-CF at both budgets, with CIs crossing zero and Holm-adjusted p-values `0.3544` and `0.2888`. Therefore the retained evidence does not support a claim that the counterfactual channel improves ROUGE-L over the strict graph ablation.

## Statistical-Fallacy and Claim-Boundary Scan

All 11 experiment-agent fallacy categories were checked. Simpson/ecological/base-rate/regression-to-mean/reverse-causality patterns were not applicable to the registered report-level benchmark claim; no covariate adjustment created collider bias. Selection of 15 eligible public reports limits external validity (Berkson/survivorship caution). Six primary tests were fully retained and Holm-corrected, mitigating look-elsewhere reporting. The study remains post-audit corrective rather than fresh preregistration, so garden-of-forking-paths risk must remain visible. Algorithmic benchmark differences must not be converted into causal claims about real maintenance outcomes.

## Limitations and Permitted Conclusions

1. This is a 15-report public NERC test split, not a representative sample of all power-grid maintenance reports, organizations, languages, or operational settings.
2. References are official executive summaries and evaluation is extractive ROUGE plus redundancy; factuality, operator usefulness, and expert preference were not established.
3. The role and causal graph are deterministic lexical proxies; the word “causal” does not establish causal identification of real-world mechanisms.
4. The run follows a corrective freeze created after an earlier pretest audit failure. Results may be reported only as **post-audit corrective descriptive evidence**.
5. The strongest defensible result is descriptive superiority over the registered Semantic-MMR and TextRank baselines on this retained split after Holm correction. No superiority over strict no-CF is supported.

## Audited Output SHA-256

- `predictions.jsonl`: `AAE2BFE0E6C426B6A69D727F24239A07DFD7DBEE8A4CE228E86625CCDCA2338F`
- `aggregate_metrics.json`: `DF9D9E4EF21BE0BDEC401C27D732D6A2692980FA8C018B119E41D85EE22149AA`
- `primary_contrasts_holm.json`: `B4C9BF1ACDA24E26DFFA4AA75AA828BED2CA69FDC4C86FA307EA44F56A097239`
- `manifest.json`: `7B209F55ED774BF2A5CC5D060D5ABD865BE951E1455DD7253E2AE962265254D9`
- `run_state.json`: `1181B0424AFDE527116459F8E08CFF0F8F7DB6D965B6784D7EEEBAC90C4D8B73`
- Registry `attempt.json`: `0855450D06C15CB55C5A072069D0CF9007CF955A57A29782996469F665706D13`

