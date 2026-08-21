# C²GES original-title R2 assembly audit

Date: 2026-08-08 (Asia/Shanghai)  
Round: R2 review draft  
Scientific evidence class: **post-audit corrective descriptive; not fresh confirmatory, preregistered, or outcome-unseen**

## Outcome

**PASS for R2 peer-review entry.** This is not a submission-readiness verdict. The maintenance-domain transfer, corresponding-author email, exact public release, detailed AI provenance, and rights approvals remain visible manual/external gates.

## Authoritative scientific inputs

| Artifact | SHA-256 |
|---|---|
| Formal freeze | `DE3205B0BC8DF65706B40B696F7313953E5905AA875128B569EECB685DAB19B5` |
| Formal predictions | `AAE2BFE0E6C426B6A69D727F24239A07DFD7DBEE8A4CE228E86625CCDCA2338F` |
| Aggregate metrics | `DF9D9E4EF21BE0BDEC401C27D732D6A2692980FA8C018B119E41D85EE22149AA` |
| Primary contrasts/Holm | `B4C9BF1ACDA24E26DFFA4AA75AA828BED2CA69FDC4C86FA307EA44F56A097239` |
| Formal output manifest | `7B209F55ED774BF2A5CC5D060D5ABD865BE951E1455DD7253E2AE962265254D9` |
| Independent post-run audit | `PASS` in `INDEPENDENT_POSTRUN_AUDIT_v0_3_1.md` |

The figure generator refuses to run if the aggregate or prediction SHA-256 differs. Its lineage file SHA-256 is `E1A630C3C3A27E234DBF82522290B53929DBFF383B4866BA42ADEEAD30B9E341`.

## Manuscript and PDF

| Check | Result |
|---|---:|
| Source SHA-256 | `36FF05A08809870E3493BAAF7F5F51191CAB20C00C1F521BE6477A55DD6A2A2D` |
| PDF SHA-256 | `F57B0C5D965450748A8CDE63D0442F3A6FBD08D872CEA1CC54C030F2DDA04CD8` |
| PDF pages / size | 10 / 293,447 bytes |
| References | 20 |
| Tables / figures | 3 / 4 |
| Overfull / underfull boxes | 0 / 0 |
| Undefined citations/references | 0 |
| LaTeX warnings after final pass | 0 |
| Structural verifier | PASS, 17/17 checks |
| Round freeze | PASS |
| Visual QA | PASS; all 10 pages rendered and inspected |

## Scientific claim checks

- All seven conditions and both budgets appear with all four aggregate metrics.
- The six registered ROUGE-L contrasts appear with paired intervals and Holm-adjusted values.
- Full minus strict no-CF is negative at both budgets and is disclosed in the Abstract, Results, Discussion, and Conclusions.
- Two machine estimator values of `0.0` are rendered as `p_boot < 0.0002` with zero smaller-tail draws; no probability-of-zero claim appears.
- No test-evidence placeholder remains in the manuscript.
- “Causal” and “counterfactual” are bounded to lexical/textual proxies and structural node deletion; no physical causal identification claim is made.
- The NERC-to-maintenance transfer is explicitly untested.
- No post hoc development calibration is incorporated into the primary results. Any future calibration requires a new unseen holdout.

## Manual and external submission gates retained

1. Yang Yong’s email must be supplied and checked.
2. Authors must confirm CRediT, funder role, conflict statement, and tool-by-tool AI disclosure.
3. The GitHub repository must be synchronized, tagged, and verified from a fresh clone.
4. Third-party permissions govern any transfer of PDFs or verbatim derived text.
5. A title-concordant maintenance corpus and qualified-domain evaluation remain future validation, not R2 evidence.
