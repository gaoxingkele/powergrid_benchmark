# MA-SQLGrid Original-Title Manuscript — R2 Assembly Audit

Audit date: 2026-08-08 (Asia/Shanghai)

## Outcome

R2 is a reproducible review draft, not a portal-ready submission. The original title is retained exactly. Mechanical integrity and descriptive traceability pass, but the scientific prior-outcome-independence gate fails: the frozen v3 pre-run regression test read gold-derived v2 outcomes for the same 180 items. The manuscript therefore labels v3 as deterministic no-generation descriptive re-execution. Stronger scientific validation requires a genuinely untouched evaluation resource and new authorization.

## Manuscript and build gates

- Source: `paper_applsci.tex`
- PDF: `build/paper_applsci.pdf`
- PDF length: 19 pages; 523,999 bytes
- References cited: 13 verified bibliography keys
- Tables: 7
- Figures: 4
- Automated manuscript verifier: PASS
- LaTeX build: PASS
- Overfull boxes: 0
- Undefined citations: 0
- Undefined cross-references: 0
- LaTeX warnings: 0
- Underfull boxes: 66. These are narrow-column line-stretch diagnostics in dense resource, chronology, robustness, and BIRD tables plus one long limitations paragraph; visual inspection found no clipping, collision, or content outside the page area.
- Visual inspection: pages 1, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 18, and 19 inspected from 110-dpi renders. The title block, dense tables, four figures, captions, descriptive results, references, disclaimer, and page boundaries are legible and unclipped.

## Code and experiment gates

- Unit/regression tests: 30/30 PASS on 2026-08-08, including nine central release tests.
- Read-only executor: SQLite URI `mode=ro&immutable=1`, `query_only`, extension denial, authorizer denial for mutation/DDL/attach/pragma/transaction operations, table/column authorization, time/opcode/row bounds, append-only attempt tracing, and failure retention.
- Counterfactual adjudication: required evidence fails closed when state coverage is incomplete; validation-only receives an empty counterfactual map and cannot use counterfactual tie-breaking.
- Release-v3 freeze content SHA-256: `8b34bc370451173197ad07b460908537836409d6eb49f303caf46d13d53889e6`.
- V3 internal mechanical checker: 29/29 checks PASS, but this checker did not detect same-item outcome access in the pre-run tests and is superseded for evidence classification.
- Independent release audit: PASS for mechanical integrity, deterministic reproduction, and descriptive traceability; FAIL for the claimed prior-outcome-independent scientific evidence class.
- Freeze contents: exact witness builder, witness manifest and three databases, release/core runners, agents, executor, all four regression-test files, passing pre-freeze test record, selection/configuration inputs, and content-bound UTC chronology (21 files total).
- Reproduction: run v3a and run v3b produced byte-identical canonical selection, evaluation, sensitivity, and summary outputs; both run manifests are content-bound after the freeze. Repetition on the same previously evaluated items does not restore prior outcome independence.
- Each run: 180 questions, eight historical candidate slots, three methods, four states per candidate, 5,760 candidate-state attempts, and 332 retained failures.
- Fixed order: 80/180 (0.4444), 180 covered, 0 abstained, 177/180 invariant.
- Validation-only: 100/180 (0.5556), 180 covered, 0 abstained, 179/180 invariant, 22 rescues and 2 harms relative to fixed order.
- Complete metamorphic coordination: 101/180 (0.5611), 180 covered, 0 abstained, 180/180 invariant, 23 rescues and 2 harms relative to fixed order.
- Full versus validation-only selection differs only on Q039. M3 rejects `SELECT *` after a nullable `work_orders` column is added and retains an explicit-column projection. The resulting 1/180 increment is reported as a narrow projection-stability case, descriptive, small, dataset-specific, and rule-dependent—not a general counterfactual or multi-agent gain.
- Reversed tie order: 117--118/180; reported as substantial order sensitivity.
- V1 witness incident: preserved, documented, and excluded because the three purported witness states shared one database SHA-256. V2 numerical behavior was reproduced, but independent audit found its release provenance incomplete because builder/tests/chronology were not fully bound; it remains a diagnostic predecessor. Neither predecessor supplies the v3 release claim.

## Claim boundaries enforced in R2

- The new study evaluates deterministic offline selection over an already existing historical eight-slot candidate pool; it is not a new-generation experiment.
- Schema grounding is trace-only in the v3 selector and is not claimed as a causal source of gain.
- The 5,760 executions are one shared precomputed physical evidence collection used by all three selectors, not 5,760 separately executed attempts per method or an estimate of each method's natural runtime cost.
- BIRD Mini-Dev is non-grid portability evidence with unequal calls per method; it is not evidence of power-grid semantic validity or a call-matched repair effect.
- GridDB constructed states are prediction-blinded robustness diagnostics, not operator-certified grid snapshots.
- No five-role end-to-end gain, autonomous-agent benefit, qualified-human semantic validation, production safety, or universal robustness claim is made.

## Integrity hashes

- `paper_applsci.tex`: `17EE387DD2C47CFE63C63E7D071E98A297E4D9BEE437B6DD24F5C43536EEC2E1`
- `references_verified.bib`: `155EB9325FF0C0D9C4A0F2A54B750C0FCBC21873B2807B51156F7988ACBDADDE`
- `build/paper_applsci.pdf`: `C4C83B2FBC31E938F0EC1A8240DE29F4B6C19D8256DC4927E0A73643F8B0EC01`
- `figures/fig_ma_sqlgrid_implemented_coordination_r2.svg`: `8BC0CFE3E2AEB4AC14BFAC366347ADBF91936D03C948B92F326C37C80A347C9E`
- `figures/fig_ma_sqlgrid_implemented_coordination_r2.png`: `AF27B3FF5D9530F1250BE38FAA6DC94C073415881319DF5F545A79AB25D78C66`
- `ma_sqlgrid_agents.py`: `EA8105FC3AB6F8F54B59E74B0AD9AC96D5CD1ABB073469C51E9DB5A7066915BE`
- `sqlite_readonly_executor.py`: `3F28F832F437CFE74DEC56E989D54A5626BBEB5DD4B1311A7D2681D3F314DC55`
- `offline_coordination_release_v3.py`: `C936E44B44F42DD27588D0C8CCC823F2FB9276178F62EBD6D00EF31CC61FEB6D`
- `build_metamorphic_witnesses_v3.py`: `0D9B5B694037E0483E842A1BEFE3E63C9B35669E6615DF42F1312D77BA959654`
- `test_offline_coordination_release_v3.py`: `3ABC9B7F1B42640916796FF3F2AB9186E22E767D46F8411C5F3328DA5E09A44E`
- `freeze_manifest.json`: `888A3CC840E2071F1CADBD3DF45517193212D35E874AF58A2DD68C16D98B8E5F`
- `INDEPENDENT_AUDIT_V3.json`: `B0C23C55E1885859F61785C8BB1F6E4598E3E01EAD0E8AEFBBDEE6D3AEC356C0`
- `INDEPENDENT_RELEASE_AUDIT_V3.md`: `DF92DA2DDE1717846798B6D7D5A0C914831F822F3114FF1184FE4C166FE7BC8A`

## Manual blockers before submission

1. Insert Yang Yong's actual correspondence email and verify the author/affiliation spelling and order with every author.
2. Obtain and document qualified power-grid expert review. If human validation is used as scientific evidence, predefine the rubric, adjudication rule, qualifications, sampling, agreement statistic, exclusions, and retained records before evaluation.
3. Confirm the exact funding agency name and funder role for grant `521300250006`; do not infer them from the number.
4. Synchronize the manuscript-bound source/data archive to `https://github.com/gaoxingkele/ma-sqlgrid`, create a release/tag, and record the immutable commit or archive DOI. The manuscript correctly does not assert that this is already done.
5. Complete third-party license review and prepare the restricted verification bundle for editor/reviewer access through the corresponding author.
6. Run the planned external three-expert review and author response cycle before promoting R2 to the next round.
7. For a confirmatory selector evaluation, obtain authorization for a genuinely untouched evaluation resource whose outcomes have not entered development, tests, reports, or previous runs; do not attempt to relabel another rerun of these same 180 items.
