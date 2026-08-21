# Mintou Six-Paper Stage 2.5 Integrity Report

Date: 2026-08-09 (Asia/Shanghai)  
Scope: the six `paper_projects/mintou_p*/manuscript/MANUSCRIPT.md` files and their corresponding code/evidence trees under `papers/mintou/`  
Decision: **FAIL — author confirmation and evidence-release decisions are required before journal-template assembly and formal review.**

## 1. Checks completed

- Parsed 457 paragraphs and 1405 sentences and compared their structure, journal register, terminology, and evidence linkage with the selected target-journal comparator corpus.
- Re-ran the Mintou experiment unit tests after reconciling the tests with the current standard-hypervolume pipeline: **12/12 tests passed**.
- Audited all 200 bibliography entries through the Crossref DOI endpoint where a DOI is present.
- Corrected four materially wrong DOI/metadata records in P3/P4 and replaced one unrelated P4 reference with a verified resilience-planning article.
- Expanded P5's recent applied planning literature and removed five uncited generic books.
- Retained non-DOI classics and explicitly identified the P3/P4 and P5/P6 companion manuscripts as unpublished rather than presenting them as published work.
- Verified that the current results retain adverse and non-significant findings instead of suppressing them.

## 2. Reference-integrity outcome

| Paper | Entries | Crossref verified | Manual/no DOI | Metadata review | Integrity conclusion |
|---|---:|---:|---:|---:|---|
| P1 DStar-GRU | 28 | 28 | 0 | 0 | Pass |
| P2 CSA-LoadNet | 30 | 30 | 0 | 0 | Pass |
| P3 CARS-MODE | 32 | 27 | 1 | 4 | Pass after manual review; four flags are publication-year/deposit-year differences |
| P4 SHIELD-MOEA | 45 | 42 | 2 | 1 | Pass after manual review; one flag is a publication-year/deposit-year difference |
| P5 TRACE-MOEA | 33 | 32 | 1 | 0 | Conditional pass; the no-DOI item is the local P6 companion manuscript |
| P6 BiLo-NSGA | 32 | 29 | 2 | 1 | Conditional pass; books have no DOI and the remaining flag is a publication-year/deposit-year difference |

Machine-readable evidence: `reference_verification_crossref.csv` and `reference_verification_summary.json` in this directory.

## 3. Scientific-integrity findings by failure mode

### 3.1 Fabricated or unsupported results

**Pass with limitations.** Numerical claims inspected in the manuscripts map to retained CSV/JSON/analysis artifacts. Negative outcomes are disclosed: P1 does not beat the strongest naive baseline overall; P2 does not support the original hyperbolic mechanism claim; P3 FixedDE is statistically tied on proxy hypervolume; P5's adaptive preference layer is weak in aggregate; and P6's backward pass is non-contributing on hypervolume.

### 3.2 Circular evaluation or metric leakage

**Pass for the current pipelines.** The deprecated circular P5/P6 revision is retained under `_deprecated_circular` and excluded from the current claims. Current trace/audit statistics are reported descriptively and do not enter selection metrics.

### 3.3 Selective reporting and post-hoc tuning

**Pass with provenance caveat.** Weak, near-miss, proxy, and deprecated runs remain in the evidence tree. The papers must preserve the present language that distinguishes exploratory development from the frozen decision experiment. No additional tuning may be reported as confirmatory without a new preregistered split or independent test set.

### 3.4 Statistical validity

**Conditional pass.** The main stochastic comparisons use fixed seed sets, non-parametric tests, and Holm correction. Limitations must remain explicit where seed counts are asymmetric (P2 Ausgrid), AC validation is descriptive rather than powered (P3/P4), and real-outcome associations are statistically significant but small (P5/P6).

### 3.5 Data provenance and licensing

**Conditional fail.** Public source datasets are named, but the consolidated code/evidence releases do not yet have persistent public URLs or DOIs. The final archives must include source manifests, licenses or source links, checksums, generation scripts, frozen configurations, and an explicit list of excluded/deprecated runs.

### 3.6 Authorship, funding, and declarations

**Fail.** P1 and P4 lack verified author, affiliation, and corresponding-author metadata. All six lack author-approved CRediT assignments and verified funding declarations. ORCIDs are not available. These facts cannot be inferred or generated.

### 3.7 Duplicate publication / salami slicing

**Pass with disclosure.** P3/P4 share a SimBench candidate-generation pipeline, and P5/P6 share a public project-candidate pipeline. The independence audit found no identical figure files and no identical result-table files across either pair. The exact/near sentence matches are confined mainly to shared references, standard statistical-protocol wording, baseline labels, declarations, and structurally similar table rows; no identical contribution, interpretation, or conclusion passage was found. Companion-paper disclosure must remain in the cover letters and data-availability statements. Machine-readable results are in `companion_independence_summary.json` and `companion_sentence_overlap.csv`.

## 4. Paper-specific experimental readiness

| Paper | Current strongest defensible claim | Remaining high-value validation |
|---|---|---|
| P1 | Reproducible curtailment/dispatch benchmark and failure analysis; not universal superiority | Full-cap rerun or an independent test period if a superiority claim is desired |
| P2 | CSA-LoadNet improves the 24 h OPSD decision setting under the frozen protocol | Forecast-reconciliation baselines and balanced seed counts on Ausgrid |
| P3 | CARS-MODE improves standard hypervolume and shows an AC/proxy trade-off | More compromise plans or networks for powered AC-feasibility inference |
| P4 | SHIELD-MOEA improves scenario-robust hypervolume; survivability evidence is descriptive | Costly-evaluation accounting and focused GA/DE/operator ablations |
| P5 | TRACE-MOEA provides fundable portfolios and auditable decision traces; preference adaptation is auxiliary | Expert-labelled review judgments, monetary cost calibration, and stronger external validation |
| P6 | Forward insertion drives a modest but consistent gain; backward deletion is retained for semantics/audit | Expert-labelled judgments, calibrated costs, and redesign/ablation of the backward operator |

The missing validations are not permission to fabricate data. They may be executed only from existing licensed/public assets with frozen protocols; otherwise they must remain limitations.

## 5. Mandatory author inputs

1. P1: final author order, affiliations, corresponding author/e-mail, and IEEE Access biographies/photos.
2. P4: final author order, affiliations, and corresponding author/e-mail.
3. P1-P6: verified funding statement for each manuscript, including grant numbers and APC funder, or explicit confirmation of no external funding.
4. P1-P6: author-approved CRediT role assignments and confirmation that every author approves the final manuscript.
5. P1-P6: public repository URL/DOI for the reproducibility package, or authorization to use a truthful restricted/on-request statement where public deposit is impossible.
6. ORCIDs where available; absence may be stated but identifiers must not be invented.

## 6. Gate decision

The companion-paper independence check is complete and passes with disclosure. Stage 2.5 cannot pass until Section 5 is resolved. Template conversion, PDF production, three-round review, and submission packaging are downstream stages and should not be represented as final while this gate is open.
