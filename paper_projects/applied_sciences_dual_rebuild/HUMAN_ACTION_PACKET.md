# Applied Sciences dual-submission human action packet

This form records the decisions that cannot be inferred from local artifacts or supplied by an AI agent. Fill each bracketed field separately for **C2GES** and **MA-SQLGrid**. Do not replace a field with an assumed value. The manuscripts remain non-submittable until every mandatory item is confirmed and the corresponding source/PDF is rebuilt.

## 1. Shared author metadata

Author identity migration authorized on 2026-08-06 is recorded in `AUTHOR_METADATA_MIGRATION_2026-08-06.md`. The following items are now resolved from the paired CMC manuscripts:

- MA-SQLGrid author order: Bijing Liu, Chenglong Sun, Yong Yang. `[RESOLVED]`
- C2GES author order: Bijing Liu, Yong Yang. `[RESOLVED]`
- Both affiliations and postal addresses for every listed author. `[RESOLVED]`
- Corresponding author for both papers: Yong Yang, `yangyong1@sgepri.sgcc.com.cn`. `[RESOLVED]`

The following author-controlled items still require confirmation:

- Public/institutional e-mail addresses for Bijing Liu and Chenglong Sun, if the submission system requires them: `[REQUIRED IF REQUESTED BY JOURNAL]`
- Author initials used in the CRediT statement: `[REQUIRED]`
- ORCID identifiers, if used: `[OPTIONAL]`
- CRediT roles for every author, approved by all authors: `[REQUIRED]`
- Funding organization, grant number, and funder role; or an author-approved no-funding statement: `[REQUIRED]`
- Conflict-of-interest disclosure from every author: `[REQUIRED]`
- Acknowledgments; or author-approved confirmation that there are none: `[REQUIRED]`
- Confirmation that institutional review is not applicable to this computational work: `[REQUIRED]`
- Confirmation that informed consent is not applicable: `[REQUIRED]`
- Final generative-AI-use disclosure naming tools, uses, and human verification: `[REQUIRED]`

## 2. C2GES-specific decisions

- Permanent public repository URL/DOI for the license-reviewed reproducibility subset: `[REQUIRED]`
- FEVER redistribution/attribution review completed by: `[NAME/ROLE/DATE REQUIRED]`
- Decision on whether converted FEVER records may be deposited: `[ALLOW / REGENERATE-ONLY / WITHHOLD, WITH BASIS]`
- Decision on whether NERC-derived text/candidates may be shared; machine labels must remain explicitly non-human: `[REQUIRED]`
- Verify the corrected publisher metadata for the Ahmad/Zhang/Sehar reference before final deposit: `[CONFIRMED BY/DATE]`

Current scientific package: `C2GES/manuscript_applsci/`; Round-3 closure: `C2GES/reviews/round3_final_closure_confirmation.md`.

## 3. MA-SQLGrid-specific decisions

- Permanent public repository URL/DOI for the license-reviewed reproducibility subset: `[REQUIRED]`
- GridDB redistribution decision: `[ALLOW / LICENSED REGENERATION ONLY / WITHHOLD, WITH BASIS]`
- RTS-GMLC, SimBench, and BIRD derivative/evaluator redistribution review completed by: `[NAME/ROLE/DATE REQUIRED]`
- Two qualified independent reviewers for visible grid question--SQL candidates: `[REVIEWER A]`, `[REVIEWER B]`
- Adjudicator for reviewer disagreements: `[REQUIRED]`
- Authorization and authorship plan for a genuinely sealed grid-domain follow-up set: `[REQUIRED FOR EXTERNAL GRID CLAIMS]`

### BIRD formal-run approval

The frozen protocol is `MA-PUBLIC-BIRD-MINIDEV-v1.0`, freeze SHA-256
`29c780c63a2dc2baae221cfce52252c716d8720dbeecdc2f7a2fdd5756b42af5`.
It schedules 500 BIRD Mini-Dev items, five calls per item and model, two models, for 5000 local generation calls on the RTX 3090. The technical audit is 39/39 PASS and no formal call has run.

- Approve this exact formal run: `YES`（2026-08-07 对话中签署；v1.0.1 修订后于同日重签，绑定新冻结哈希 `c77699593d7752ffc2c5c0fa0e58ef4f48db1a05f2a827ff4dde1cb8c936a05b`）
- Human approver name or stable identity: `DONG LUN HAI`
- Approval date/time and time zone: `2026-08-07, Asia/Shanghai`
- Explicit acknowledgment of 5000 generation calls and several hours of local GPU use: `YES`

The runner must reject a missing, mismatched, or non-human approval record. Approval authorizes only the frozen run; it does not authorize publication, external upload, or any DKA-SQL reproduction claim.

## 4. Final submission choices

- Confirm target journal and Section: `Applied Sciences — Computing and Artificial Intelligence`: `[CONFIRM / CHANGE]`
- Confirm whether submission is regular-section or Special-Issue routed: `[REGULAR / SPECIAL ISSUE NAME AND URL]`
- Confirm that all authors approve the final title, abstract, declarations, data statement, and PDF: `[REQUIRED PER MANUSCRIPT]`
- Confirm APC/waiver/IOAP arrangements using current official MDPI terms: `[REQUIRED BEFORE SUBMISSION]`

## 5. Return procedure

Return this completed packet or provide the same information in a signed author-controlled document. The integration agent will then replace only the matching front-matter markers, rebuild both PDFs, rerun all evidence and compliance verifiers, and record the final author-approved hashes.
