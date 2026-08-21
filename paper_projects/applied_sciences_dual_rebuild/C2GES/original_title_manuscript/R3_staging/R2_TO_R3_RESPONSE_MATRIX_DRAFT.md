# C2GES R2-to-R3 Response Matrix (Evidence-Fix Draft)

Status vocabulary: **CLOSED** means the requested manuscript/evidence repair is present and mechanically verifiable; **PARTIAL** means the claim has been bounded but the requested external evidence is absent; **OPEN-MANUAL** identifies an action no AI agent or existing artifact can legitimately complete.

| Review issue | R3 action based on existing immutable evidence | Status | Verification / remaining gate |
|---|---|---|---|
| Registered bootstrap quantities were mislabeled as p-values | Preserve frozen intervals and values, relabel them `registered bootstrap sign-tail summaries`, explain observed-distribution centering and why Holm does not create null calibration | CLOSED for terminology | `REGISTERED_BOOTSTRAP_INTERPRETATION.md`; R3 manuscript must remove conventional p-value/significance language for these quantities |
| Need defensible paired null sensitivity | Added exact two-sided report-level sign-flip enumeration for the same six contrasts and six-item Holm; explicitly unregistered and conditional on joint sign symmetry | CLOSED as post-run sensitivity only | 210-row input SHA `AAE2...338F`; 6 x 32,768 assignments; independent mechanical verifier `PASS`; not replacement confirmation |
| Completed post-unblinding tuning was described as future work | Add factual chronology, full 147-configuration design, 12 LOO folds, 12/12 zero-CF result, and explicit non-reuse prohibition | CLOSED for disclosure | `POST_UNBLINDING_DEV_CALIBRATION_SUPPLEMENT.md`; formal v0.3.1 values unchanged |
| Report-level heterogeneity hidden by aggregate values | Add positive/negative/tie counts for every contrast and retain report-level paired plot | CLOSED | Counts: 7/7/1, 14/1/0, 14/1/0, 6/8/1, 11/4/0, 13/2/0 |
| 40-report sampling frame and 13 exclusions unclear | Add non-verbatim 40-row metadata index; 27 included, 11 missing summary heading, 2 missing summary endpoint | CLOSED for accounting | Metadata build tests pass; years/genres explicitly limited to manifest-derived labels |
| Rights/terms and editor/reviewer access unresolved | Keep fail-closed fields and do not promise redistribution; separate code/hashes/non-verbatim metadata from protected PDFs/text | OPEN-MANUAL | Responsible human/institution must determine rights and terms per source; AI cannot close |
| Maintenance title is not concordant with evaluated population | Put selected public NERC technical-report population and untested maintenance transfer in first two abstract sentences and conclusion; prohibit effectiveness wording | PARTIAL | Claim-scope repair is possible; real title-concordant evidence requires a new license-cleared maintenance corpus |
| Lexical role semantics and causal terminology overclaim | Define roles/edges as deterministic text proxies; describe path deletion as structural sensitivity; never identify physical effects or causal-chain accuracy | PARTIAL | Computational reproducibility can close; qualified semantic validation is absent |
| Qualified human evaluation and safety endpoints absent | Retain explicit limitation and consequential-use prohibition; do not substitute LLM/agent judgments | OPEN-MANUAL | Requires real qualified personnel, protocol/consent where applicable, ratings, disagreements, adjudication and agreement |
| Comparator tuning asymmetry | Disclose that C2GES had a 144-configuration development search while Semantic-MMR lambda 0.5 was fixed; bound comparisons to retained corrective split | PARTIAL | Equal-budget baseline tuning requires a new sealed development/holdout design, not reuse of current test |
| Narrow n=15 and ROUGE-only endpoint | State n=15, selected single-organization English reports, K=5/10 research budgets, and that ROUGE measures Executive-Summary overlap only | PARTIAL | Broader metrics and title-concordant operational validation require new data/humans |
| Repository does not match manuscript-bound package | Do not claim synchronization; list repository release/tag/fresh-clone verification as pre-submission action | OPEN-MANUAL | Repository owner action required |
| Corresponding-author email, author/funder/COI/AI-use verification | Retain placeholders or explicit pending statements; do not fabricate confirmations | OPEN-MANUAL | Yang Yong and all authors must verify |

## Non-negotiable preservation rules

1. Do not edit, overwrite, delete, or rerun the v0.3.1 formal directory.
2. Do not select hyperparameters, subgroups, endpoints, or wording from favorable patterns in the revealed 15 reports.
3. Do not run `C046`, `C055`, or any new configuration on the existing test set.
4. Do not call the exact sign-flip sensitivity registered, preregistered, confirmatory, or assumption-free.
5. Do not call LLM/agent review qualified human expert validation or adjudication.
6. Keep every unresolved human, rights, repository, and title-concordance gate visible through submission assembly.
