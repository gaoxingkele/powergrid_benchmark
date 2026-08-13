## Material Passport

- Origin Skill: experiment-agent
- Origin Mode: run
- Verification Status: UNVERIFIED
- Version Label: p5_s3_matched_compromise_v1

## Matched-compromise result

This analysis consumes the compromise already selected in every preserved main-run row by the shared normalized-objective-sum rule. Deterministic rules contribute one unique output per scenario; their repeated provenance rows are not treated as independent runs.

| Method | Type | Cost index | Reliability | Renewable | Risk | Size |
|---|---|---:|---:|---:|---:|---:|
| AHP-TOPSIS | deterministic | 0.9865677400 | 35.1204139271 | 0.4154863300 | 0.3202653229 | 14.2857142857 |
| Greedy BCR | deterministic | 0.9715351943 | 7.6598447743 | 156.3508726443 | 0.2157129543 | 13.2857142857 |
| MOEA/D | stochastic_moea | 0.0580850186 | 0.3028404314 | 12.0025643635 | 0.1318430796 | 0.8333333333 |
| NSGA-II | stochastic_moea | 0.9341208897 | 24.7310692209 | 19.2923572319 | 0.2717788491 | 13.5428571428 |
| R-NSGA-II | stochastic_moea | 0.9778825985 | 14.8567972449 | 69.4004826623 | 0.2294848394 | 13.2952380952 |
| TRACE-MOEA | stochastic_moea | 0.9135757165 | 25.5790296935 | 33.1729060473 | 0.2777746001 | 14.0666666667 |
| Weighted Sum | deterministic | 0.9756497286 | 4.3834222643 | 41.7844940571 | 0.3664036157 | 5.4285714286 |

The objectives trade off, so this table does not declare a universal winner. Full-front hypervolume is retained in the CSV only as context and is not a matched-cardinality metric. A deterministic method's single output does not create a sampling distribution, and no p-value is computed against repeated stochastic runs.
