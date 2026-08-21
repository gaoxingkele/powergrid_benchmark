# MA-SQLGrid Evidence-Boundary and Language Audit

Date: 6 August 2026  
Decision: **PASS_CANDIDATE_PATCH_COMPILED**

No BIRD or other model call was made, no expert review was simulated, and no experimental result was changed. The title, author order, affiliations, and corresponding-author metadata remain unchanged.

## Issues found and revised

1. **BIRD was described too briefly and with development-stage wording.** The Methods now records the complete frozen design: 500 items, 11 databases, direct/decomposition/schema-selection/execution-repair methods, 2,500 calls per backbone, 5,000 total calls, and 4,000 final method outputs. It states `FROZEN_NOT_RUN`, absent human authorization, zero calls and outputs, required independent post-run re-execution, and the non-sealed/non-DKASQL boundary. No pending run is written as a result.
2. **The 91 external candidates could be confused with a future sealed test.** The paper now states that their questions, references, and one Qwen diagnostic are development-visible. Completing two qualified reviews and adjudication can make them human-reviewed but cannot make them sealed retroactively.
3. **The future sealed-set condition was underspecified.** The candidate text now requires new or deeply rewritten content after method freeze, overlap screening, custody outside the development team, independent review/adjudication, and one registered no-drop execution. It explicitly states that no such set currently exists.
4. **Agent-role wording could imply qualified human review.** The order screen is now described as two independent, prediction-blinded, machine-assisted protocol audits. Both the abstract and Methods state that this is not qualified human semantic review.
5. **Internal workflow language reduced readability.** `promotion`, `NO--GO`, `Round-1 work`, `sign-off`, and similar process labels were replaced by registered analysis, declared decision/evidence rules, or direct descriptions of what was and was not supported.
6. **Several verbs were stronger than the finite evidence.** Promotional or causal-sounding language was replaced with `evaluates`, `is consistent with`, `indicates`, and similarly bounded terms.
7. **Rendered declarations exposed internal `W10_FRONT_MATTER` markers.** They now use natural pending-author/pending-license statements. No CRediT, funding, conflict, ethics, consent, acknowledgment, AI-use, license, repository, or DOI value was invented.
8. **The first revised abstract was slightly long.** The final mechanical word-like count is 194.

## Final evidence boundaries

- BIRD: technically frozen, human authorization absent, zero formal calls, zero outputs, and no result in the article.
- Existing RTS-GMLC/SimBench set: 91 automatic, development-visible, unreviewed and unsealed candidates.
- Future sealed set: absent; it requires independent creation, review, custody, leakage checks, method freeze and registered execution.
- Order-sensitive screen: machine-assisted protocol audit only; not human annotation or semantic certification.
- Author/legal declarations: still open and visibly stated in natural academic language.

## Verification

- TeX: 73,487 bytes; SHA-256 `04F82EDCA21FE9B57476B8745C0E448EDE03DB6A7331B9BF47835F519F2F1D55`.
- PDF: 26 pages, 667,693 bytes; SHA-256 `05D3E36F9C7B9BB1CDBF66F53C42CC64098BE78EC9C8B9F39EC2C394A41EEE94`.
- Two fixed-epoch builds produced the same PDF SHA and byte count.
- The standard `build.ps1` wrapper subsequently completed with exit code 0 and reproduced the same PDF.
- Manuscript verifier: PASS; 9 figures and 23 citation keys verified.
- Portable semantic manifest: SHA-256 `D9D7F48FA60961A6EBA01E5BAA4D76CF849A1EDF2A86B621719F119BB98DBF60`; local and clean-copy verification both PASS 19/19.
- LaTeX: zero errors, zero undefined references/citations, zero overfull boxes; four nonfatal underfull boxes and two nonfatal PDF-string warnings.

The build wrapper was made tolerant of MiKTeX maintenance notices written to stderr while continuing to fail on nonzero native exit codes. This does not suppress LaTeX failures.

## Assembly follow-up

The Round-2/Round-3 response identities, W10 assembly snapshot, deterministic-build audit, and downstream closure records still bind the pre-revision TeX/PDF. They were not overwritten here because they are owned by the final assembly/closure step. That step should synchronize them to the hashes above before declaring a new authoritative submission snapshot.
