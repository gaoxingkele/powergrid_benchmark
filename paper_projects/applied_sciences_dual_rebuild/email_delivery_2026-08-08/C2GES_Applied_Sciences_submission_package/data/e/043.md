# C2GES Frozen 5×5 Matrix Independent Audit

Date: 2026-08-06  
Decision: **PASS**

## Scope and non-interference

This audit monitored the already-running `formal_run_5x5` matrix. It did not launch a second matrix, alter a frozen file, repair or rerun a child, or modify the manuscript. No incident marker was observed. Analysis began only after the root `SUCCESS.json` appeared.

## Pre-analysis integrity gate

- `SUCCESS.json`: status `success`; 30 completed children.
- `completed_children.json`: 5 upstream children and 25 downstream children; every return code was zero.
- Output topology: 5 `seed_*` upstream directories and 25 `up_*/down_*` downstream directories.
- Prediction ledgers: 25/25 present; every `predictions.jsonl` contained exactly 54,000 rows; all 25 ledger SHA-256 values were computed and were distinct.
- Provenance linkage: for every downstream cell, the recorded `predicted_labels_sha256` matched both the actual upstream `predicted_labels.json` and the upstream provenance hash.
- Frozen hashes: the protocol, pre-analysis clarification, analysis code, runner, predictor, and selector hashes all matched their frozen values.

The frozen analyzer was then run once with the completed matrix as input and a previously nonexistent `formal_analysis_v1` output directory.

## Analyzer validation

`validation.json` reports `PASS` with 25 ledgers, 450,000 selected rows, 300 mode-by-cutoff cells, 25 primary cells, and 145 documents.

For the frozen primary estimand (`full`, K=3), the analyzer reports:

- grand mean F1: `0.4905990053201013`;
- upstream means: `0.4899928102994357`, `0.48988922314584854`, `0.4905457769624023`, `0.4912675646953666`, `0.49129965149745336`;
- downstream means: `0.49052454168352`, `0.4921869957436211`, `0.49063066958611856`, `0.487931144710123`, `0.4917216748771237`;
- descriptive variance components: upstream `0.0`, downstream `2.1550741852460383e-06`, interaction/residual `2.8572893395756467e-06`;
- document-composition sensitivity interval: `[0.47303446072267663, 0.5080022852066212]` over 145 documents and 10,000 draws.

The interval is a document-composition sensitivity interval, not a population confidence interval. The components are descriptive fixed-seed method-of-moments quantities, not population variance components.

## Independent recomputation

A separate streaming implementation used only Python's standard library and `math.fsum`. It read the 25 raw JSONL ledgers directly, did not import `analyze_matrix.py`, and did not read `cell_summary.csv`.

It independently recovered 37,500 primary claim rows, 145 documents, grand mean `0.4905990053201013`, and the same upstream/downstream means. Its variance components were upstream `0.0`, downstream `2.1550741852460705e-06`, and interaction/residual `2.85728933957564e-06`.

The maximum absolute discrepancy from the frozen analyzer was `5.551115123125783e-17` for marginal means, `1.5415999640028266e-19` for mean squares, and `3.218725199566341e-20` for variance components. These are floating-point summation-order differences only.

## Bound artifact identities

- `ANALYSIS_FREEZE.json`: `0e54d99772439d1f91483d0254134b4d84a13c1db725867d589ba4421c83f94f`
- `PROTOCOL_FREEZE.json`: `4168975fc7b83867fb90c4ea7916084e240aac52c3e297eb5af1611514fbd23a`
- `PROTOCOL_CLARIFICATION_PRE_ANALYSIS.md`: `85a8581111d756326894625438e312309a9ba7e6c3555f5befe92a2c843ee5b1`
- `analyze_matrix.py`: `3c23df96768127ae05924f08e9d97e882adb10ecf91cba4547e07d485417d9c1`
- `formal_run_5x5/SUCCESS.json`: `2142c954e2795761498450ed8035f251ab84136b61c25d1e35629963b8ac5f4c`
- `formal_run_5x5/completed_children.json`: `6f140b0839fbc47afcb8d1a99c7bc22021a593821dd3149cc5eb3888a104b3eb`
- `cell_summary.csv`: `6f64715d48a4842b0a39fc4bd3748efc69d0cb963d01cd1f3d2f1a3a69f6232a`
- `results.json`: `5a04d3f315821e899583819e6654cedf29b2d366ecbb7133d01c543d41a8ad9f`
- `validation.json`: `660551c6b4e4cef128d50a8b2d6c85139907dee5c6dc5e04079d31bfc9101338`

The machine-checkable companion contains all 25 ledger hashes.
