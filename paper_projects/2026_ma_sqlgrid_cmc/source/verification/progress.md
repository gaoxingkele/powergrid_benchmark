## State
FROZEN

## Current Position

User provided a newer PaperReview link on 2026-06-26. Paper-Harness ad hoc run `run_20260626-234417` returned `REOPEN_FOR_BOUNDED_SUBMISSION_POLISH`: do not add external Spider/BIRD-style benchmarks and do not rerun experiments; perform only submission-facing polish around validator weight sensitivity, artifact availability, hosted-model reproducibility, no-leakage wording, normalization coverage, recent-reference verification, and optional set-insensitive metric deferral.

Executor completed that bounded polish in Stage 22/23: `paper.tex` now includes the approved reviewer-facing clarifications; `paper.pdf` was rebuilt and now has 14 pages; `paper_final_verified.md` was regenerated from the current TeX; `verification_report.json` and `decision.json` preserve the unchanged 45-key citation sync; and `stage-23/recent_reference_external_check.md` records external arXiv/DOI checks for very recent related-work entries. Direct checks found no LaTeX/BibTeX fatal/undefined/missing-file blocker, all 45 cited keys remain covered by `references_verified.bib`, the new text appears in extracted PDF text, embedded images/fonts remain present, and rendered-page inspection found no obvious clipping or overlap.

Paper-Harness approved the bounded submission-polish outputs:

- `paper_text_quality` run `run_20260626-235834`: `APPROVE`
- `paper_pdf_quality` run `run_20260627-000428`: `APPROVE`

The workspace is refrozen from the current Stage 22/23 final artifacts. No further pipeline stage, experiment rerun, external benchmark expansion, paper-text change, figure repair, layout repair, or citation repair is required by Harness.

User reopened the previously frozen workspace on 2026-06-26 for a bounded revision after external PaperReview feedback. Paper-Harness ad hoc run `run_20260626-164515` returned `APPROVE_WITH_CONSTRAINTS`: do not add unrelated Spider/BIRD-style external benchmarks; if keeping component-level claims, add bounded in-domain C4 no-value-hints and no-shape-hints ablations on the same GridDB test split.

Executor completed the approved stronger route and Paper-Harness approved refreezing in ad hoc close-out run `run_20260626-180023` with conclusion `APPROVE_TO_REFREEZE`.

New addendum/finalization artifacts are:

- component ablation addendum: `pipeline/runs/run_001/stage-13/component_ablation_addendum/`
- validator diagnostics: `pipeline/runs/run_001/stage-13/validator_diagnostics/`
- revised Stage 22 paper TeX/PDF: `pipeline/runs/run_001/stage-22/paper.tex`, `pipeline/runs/run_001/stage-22/paper.pdf`
- synchronized Stage 23 verified bibliography/report/markdown: `pipeline/runs/run_001/stage-23/references_verified.bib`, `pipeline/runs/run_001/stage-23/verification_report.json`, `pipeline/runs/run_001/stage-23/paper_final_verified.md`

Current addendum results: C4 no-value-hints reaches 118/180 and 0.6556 execution accuracy; C4 no-shape-hints reaches 77/180 and 0.4278 execution accuracy. Current rebuilt PDF has 13 pages and direct Harness `paper_pdf_quality` approval in run `run_20260626-175000`. Current Stage 23 verified bibliography contains exactly the 45 keys cited by Stage 22 TeX, with zero missing and zero extra keys.

Stages 1-9 are complete. Paper-Harness approved the repaired Stage 9 experiment design.

Harness approval:

- review type: `experiment_design`
- result: `harness/harness-result.md`
- verdict: `APPROVE`
- run: `run_20260622-164234`

Stage 10 `CODE_GENERATION` is complete via Executor repair. Stage 11 `RESOURCE_PLANNING` is complete. Paper-Harness ad hoc review `run_20260622-173217` approved protocol B for Stage 12: one deterministic full-test formal pass per C1-C5 condition; dev smoke seeds `[0,1,2]` are contract evidence only.

Stage 12 pre-repair protocol-B formal pass and manual Stage 13 canonicalization were completed, but those results are archived as diagnostic failed-pass evidence only. Paper-Harness ad hoc review `run_20260622-185932` returned `ITERATE`: do not treat the pre-repair C4/C5 underperformance as a clean method-level negative result, and do not consume the archived Stage 14 for Stage 15 or paper claims.

Executor repaired the Stage 10 C4/C5 mechanism, reran Stage 12 protocol B as `formal_outputs_repair1`, rebuilt Stage 13 canonical artifacts, and regenerated Stage 14 from the repaired outputs. Current repaired formal results: C1 0.3944, C2 0.4389, C3 0.4000, C4 0.7000, C5 0.7278 execution accuracy over Q021-Q200.

Paper-Harness `run_20260622-203412` returned `ITERATE` for result interpretation, but only for bounded Stage 14 artifact repair. It explicitly found that the repaired C4/C5 results support the MA-SQLGrid direction and that no further formal Stage 12 rerun is justified. Executor repaired Stage 14 consumable artifacts: executable chart scripts, regenerated code-backed PNGs, evidence-faithful figure manifest/plan captions, compact paper-facing `results_table.tex`, paired comparison carry-through, protocol-B seed-policy wording, and C5 validation-boundary documentation.

Paper-Harness `run_20260622-204924` returned `PROCEED`: Stage 15 may proceed from the repaired Stage 13/14 bundle with C4 as the main mechanism evidence and C5 as a modest validation/reranking extension with latency overhead. Stage 15 initially produced a generic seed-count `REFINE`, which conflicted with Harness-approved protocol B; Executor repaired Stage 15 to `PROCEED_WITH_NARROW_CLAIMS`.

Stage 16 `PAPER_OUTLINE` completed and was manually repaired to preserve the fixed title, repaired Stage 13/14 result boundaries, and protocol-B seed wording. Stage 17 `PAPER_DRAFT` completed and was manually repaired into a single coherent draft: duplicate sections and conversational preambles were removed, the fixed title was restored, fake regime/mean-std tables were removed, verified Stage 14 figures were copied and linked, missing citation keys were fixed, and the draft now uses only repaired Stage 13/14 results. Stage 17 verification found 4/4 image links present, zero missing bibliography keys, and no hard placeholder/stale negative-result grep hits.

Stage 18 `PEER_REVIEW` completed with `proceed`. Reviewers requested tighter claim boundaries, clearer evidence mapping, dataset characterization/error analysis, and stricter wording around protocol-B single-pass statistics. The reviewer suggestion to run at least three formal seeds conflicts with Harness-approved protocol B and must be handled in Stage 19 as a limitation/wording issue, not as a formal rerun.

Stage 19 `PAPER_REVISION` completed with `proceed` and was manually repaired after the automatic revision inserted conversational preamble text, changed the fixed title, and referenced missing chart files. Current repaired Stage 19 draft restores the fixed title, keeps protocol-B single-pass wording, includes four copied figures plus verified bibliography, and passes checks for image links, citation keys, abstract length, stale negative-result text, and hard placeholders.

Stage 20 `QUALITY_GATE` passed with quality score 9 and fabrication suspicion false, then Paper-Harness `run_20260622-212647` returned `REVISE` for bounded text quality only. Executor completed the requested bounded Stage 19 text revision without rerunning formal inference: manuscript length is now about 7025 words; added dataset characterization, C5 validator/protocol details, error analysis from existing Stage 13/14 taxonomy, and claim-to-evidence mapping. A later Stage 20 rerun returned `degraded` with a truncation claim that contradicted direct file inspection. Paper-Harness `run_20260622-213933` returned `APPROVE`: the current Stage 19 manuscript may proceed to Stage 21, while Stage 22 still requires direct rendered-PDF review.

Stage 21 `KNOWLEDGE_ARCHIVE` completed. The automatic `archive.md` was unusable conversational fallback text, so Executor replaced it with a concise archive of the approved Stage 19 manuscript, repaired Stage 13/14 evidence chain, claim boundaries, figure/citation assets, and Stage 22 PDF-review requirement.

Paper-Harness ad hoc review `run_20260622-214833` confirmed that the pre-repair C4/C5 underperformance was a Stage 10/12 implementation and gate-control failure, not a method-level negative result. The repaired Stage 12/13/14 evidence chain remains canonical, and Stage 22 should proceed from the approved Stage 19 manuscript lineage.

Stage 22 `EXPORT_PUBLISH` completed, but the automatic export inserted degraded-mode text, redacted verified numbers, lost approved figure assets, duplicated bibliography keys, and produced an initially defective LaTeX/PDF chain. Executor repaired Stage 22 from the approved Stage 19 manuscript, copied the four approved Stage 19 figures, deduplicated/ASCII-normalized the bibliography, rebuilt `paper.tex`, manually compiled `paper.pdf`, and rendered pages for direct inspection. Paper-Harness `run_20260622-221303` requested one bounded front-matter repair for a visible corresponding-author placeholder. Executor replaced it with anonymous-review correspondence text and rebuilt the PDF. Paper-Harness `run_20260622-222441` returned `APPROVE` for `paper_pdf_quality`; Stage 23 `CITATION_VERIFY` may proceed.

Stage 23 `CITATION_VERIFY` completed with `proceed`. The automatic verification report timed out on the oversized raw bibliography pool, but Executor audited actual consumption: current `paper.tex` cites 37 unique keys, `stage-23/references_verified.bib` contains exactly those 37 keys with zero missing or extra keys, and the one suspicious report key is not cited. The automatic `paper_final_verified.md` had stripped some citation markers, so Executor restored it from trusted Stage 22 markdown and recorded the repair in Stage 23 metadata.

The workspace is frozen. Do not change experiments, paper text, PDF, figures, or bibliography unless a new user-level instruction explicitly reopens the workspace.

## Canonical Design Artifacts

- Stage 9 experiment plan: `pipeline/runs/run_001/stage-09/exp_plan.yaml`
- Stage 9 metadata: `pipeline/runs/run_001/stage-09/decision.json`
- Stage 10 canonical experiment code: `pipeline/runs/run_001/stage-10/experiment/`
- Stage 10 validation report: `pipeline/runs/run_001/stage-10/validation_report.md`
- Stage 11 schedule: `pipeline/runs/run_001/stage-11/schedule.json`
- Harness protocol-B decision: `harness/harness-result.md` (`run_20260622-173217`)
- Archived pre-repair diagnostic artifacts: `pipeline/runs/run_001/archive/pre_repair_iterate_20260622/`
- Repaired Stage 12 formal outputs: `pipeline/runs/run_001/stage-12/formal_outputs_repair1/`
- Current canonical Stage 13 package: `pipeline/runs/run_001/stage-13/experiment_final/`
- Current repaired Stage 14 result analysis: `pipeline/runs/run_001/stage-14/`
- Harness mechanism-iterate decision: `harness/harness-result.md` (`run_20260622-185932`)
- Harness Stage 14 artifact-repair decision: `harness/harness-result.md` (`run_20260622-203412`)
- Harness result-interpretation proceed decision: `harness/harness-result.md` (`run_20260622-204924`)
- Current Stage 15 research decision: `pipeline/runs/run_001/stage-15/decision.md`
- Current Stage 16 paper outline: `pipeline/runs/run_001/stage-16/outline.md`
- Current Stage 17 paper draft: `pipeline/runs/run_001/stage-17/paper_draft.md`
- Current Stage 17 copied figures: `pipeline/runs/run_001/stage-17/charts/`
- Current Stage 18 peer review: `pipeline/runs/run_001/stage-18/reviews.md`
- Current Stage 19 revised paper: `pipeline/runs/run_001/stage-19/paper_revised.md`
- Current Stage 19 copied figures: `pipeline/runs/run_001/stage-19/charts/`
- Current Stage 21 archive: `pipeline/runs/run_001/stage-21/archive.md`
- Current Stage 22 paper PDF: `pipeline/runs/run_001/stage-22/paper.pdf`
- Current Stage 22 paper TeX: `pipeline/runs/run_001/stage-22/paper.tex`
- Current Stage 22 render check: `tmp/pdfs/ma_sqlgrid_stage22/contact_sheet.png`
- Current Stage 23 verified bibliography: `pipeline/runs/run_001/stage-23/references_verified.bib`
- Current Stage 23 verified markdown: `pipeline/runs/run_001/stage-23/paper_final_verified.md`
- Current Stage 23 verification report: `pipeline/runs/run_001/stage-23/verification_report.json`
- Harness handoff: `harness/harness-handoff.md`
- three-pack config: `three-pack/config.yaml`
- three-pack prompts: `three-pack/prompts.yaml`
- research policy: `three-pack/research_policy.yaml`

## Required Stage 10 Guardrails

- Implement the prediction contract from `exp_plan.yaml`: required fields present, forbidden gold-derived fields absent.
- Keep gold SQL, gold result rows, answer-shape metadata, required-literal metadata, and order-sensitive metadata out of formal test prompts, rankers, candidate selection, and repairs.
- Smoke-test every formal condition output contract before any formal test-split result table is produced.
- Run dataset validation and evaluator tests before formal experiments.
- Use the same `gpt-5.4-mini` Krill `responses` provider, temperature 0, split, evaluator, and retry policy for C1-C5.
- Keep DAIL/DIN/MAC optional unless implemented or prompt-style adaptations are contract-tested and labeled as non-official.
- Do not report dev-only pilot numbers as formal paper results.
- Do not describe `GridDB-Maintenance-v2 v0.1` as real industrial data.
- Do not use `gpt-5.5` or another frontier model as the main reported SQL generator.
- Do not inherit old manuscript, old pilot, or `ma-sqlgrid-evidence-audit` results.

## Paper Direction

Paper title:

**MA-SQLGrid: A Robust Multi-Agent Framework for Text-to-SQL in Power Grid Databases**

Current method:

CHESS-style MA-SQLGrid, a domain-aware Text-to-SQL framework that combines compact schema/value context construction, power-grid value normalization, answer-shape control inferred from the question, SQL generation with a fixed non-frontier model, and reference-free execution/shape/value validation.

## Verified Foundation

- Dataset: `GridDB-Maintenance-v2 v0.1`
- Dataset path: `data/griddb_maintenance_v2_v0_1/`
- Dataset size: 200 question-SQL pairs
- Split: `Q001`-`Q020` dev, `Q021`-`Q200` test
- Semantic evaluator: `evaluator/evaluator.py`
- Evaluator tests: `evaluator/tests/test_evaluator.py`
- Main SQL-generation model/provider: `gpt-5.4-mini` via Krill `https://api.krill-ai.com/codex/v1`, `wire_api=responses`, temperature 0
- Dev-only C1-C5 smoke chain: `smoke/dev_chess_style/`

## Next Step

No next pipeline stage. Workspace is refrozen after Harness close-out approval `run_20260626-180023`.

## Do Not

- Do not consume archived pre-repair Stage 14 artifacts for Stage 15 or paper claims.
- Do not treat archived pre-repair C4/C5 underperformance as a clean method-level negative result.
- Do not run formal test-split inference before repaired Stage 10/12 setup and condition smoke tests exist.
- Do not treat dev-only pilot results as paper results.
- Do not use old `VG-Rerank`, `AutoCompact`, or `MA-SQLGrid-VG` final-method framing.
- Do not consume archived pre-repair Stage 12/13/14 artifacts for writing claims.
- Do not let generic multi-seed warnings override Harness-approved protocol B.
- Do not treat Stage 22 runner `done/proceed` as sufficient PDF approval; the trusted PDF approval is Harness `run_20260622-222441`.
- Do not add unrelated external benchmarks unless Paper-Harness explicitly requires them.
- Do not overwrite the Stage 22 PDF/TeX beyond the current reopened review-driven revision without a user-level instruction or Harness blocker.
