# P2 Locked-Identity Contract Verification

**Stage:** `p2_v2_s01_locked_identity_contract`  
**Scope:** title, author order, active journal route, P2-C01--P2-C08 evidence bindings, and the protected primary NSGA-II comparison. No experiment was added, rerun, removed, or retuned in this stage.

## Verified contract

- The controlling title is exactly `Multi-objective Evolution Algorithm based on Non-Dominated Sorting and Bidirectional Local Search for Investment Effectiveness Strategy Optimization` in the manuscript master and Applied Sciences LaTeX source.
- The controlling author order is Yubin Lin, Jingbo Zhang, Xiaoyu Huang, Dishan Yang, and Jiyu Li. Affiliation, correspondence, funding, and CRediT confirmation remain separate human gates.
- Applied Sciences is the sole active route. The journal source retains the `applsci` document-class option.
- `CLAIM_EVIDENCE_REGISTER.md` contains one evidence-bounded row for each of P2-C01 through P2-C08.
- Direct parsing of `matched_summary.csv` and `matched_inference.csv` confirms eight negative BiLo-NSGA scenario mean differences against NSGA-II, zero Holm-significant wins, and four Holm-significant losses in the primary matched-evaluation family.

## Check record

- `harness_scientific_acceptance.py --phase narrative`: PASS.
- `harness_reconstruction_v2_acceptance.py --phase contract`: PASS.
- Read-only identity/hygiene audit: PASS for eleven required nonempty files, the exact source title, exact source author order, `applsci` route, eight unique claim IDs, all seven required evidence headings, forbidden submission-process meta-narrative, and absence of the superseded title from Markdown and TeX sources.
- Journal-preview build with human placeholders allowed: NOT COMPLETED. The installed MiKTeX reports an unfinished fresh setup and `pdflatex` exits before compilation. The retained PDF files predate this contract and display superseded titles; they are not contract-current artifacts. The failed build did not replace the accepted experiment evidence or the author-owned journal source.

## Release boundary

This stage establishes the textual contract but does not certify submission readiness. Regenerating both PDFs after TeX setup is completed remains necessary before release, alongside the unresolved human gates recorded in `manuscript/DEEP_REVISION_EVIDENCE.md`.
