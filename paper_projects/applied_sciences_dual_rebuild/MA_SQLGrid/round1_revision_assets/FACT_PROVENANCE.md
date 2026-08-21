# Fact and source provenance

All paths are relative to the repository root.

| Fact | Source location |
|---|---|
| Four cells and prompt-path gold exclusion | `paper_projects/2026_ma_sqlgrid_cmc/source/code/experiment_final/applsci_factorial.py:27-37,146-165` |
| One model request and one parsed SQL per formal cell | `.../applsci_factorial.py:197-260,380-447` |
| Prompt/context/response/config/data/code ledger fields | `.../applsci_factorial.py:387-445` |
| Full package and domain package construction | `paper_projects/2026_ma_sqlgrid_cmc/source/code/experiment_final/main.py:255-268`; `paper_projects/2026_ma_sqlgrid_cmc/source/smoke/dev_chess_style_pilot.py:689-727` |
| Value inventory | `.../dev_chess_style_pilot.py:191-204` |
| Compact selection, FK expansion, normalization rules | `.../dev_chess_style_pilot.py:206-471,661-727` |
| Composite hint rule inventory | `.../dev_chess_style_pilot.py:473-648` |
| First-candidate parser behavior | `paper_projects/2026_ma_sqlgrid_cmc/source/smoke/minimal_text2sql_smoke.py:136-152` |
| Single parsed statement/read-only validator and execution | `paper_projects/2026_ma_sqlgrid_cmc/source/code/evaluator/evaluator.py:113-135` |
| Exact frozen four-cell prompt example | `paper_projects/applied_sciences_dual_rebuild/MA_SQLGrid/formal_run/qwen25coder7b_q4km_seed20260805_clean_rerun1/prompts.jsonl`, records for `Q041` |
| GridDB construction, expansion, split and scope | `paper_projects/2026_ma_sqlgrid_cmc/source/data/griddb_maintenance_v2_v0_1/annotation_protocol.md` |
| All 200 gold SQL executions and five empty results | `.../griddb_maintenance_v2_v0_1/verification_log.md` |
| Table counts and 98 rows | direct read-only queries of `.../griddb_maintenance_v2_v0_1/database.sqlite` |
| Difficulty, feature tags, answer metadata and split | `.../griddb_maintenance_v2_v0_1/questions.jsonl` and `splits.json` |
| 70 normalized-SQL clusters and cluster definition | `paper_projects/applied_sciences_dual_rebuild/MA_SQLGrid/statistics/audit_clean_formal_run.py:222-225,318`; `MA_LOCAL_FORMAL_INDEPENDENT_AUDIT.json` |
| External 91/364 status and evaluator boundary | `paper_projects/applied_sciences_dual_rebuild/MA_SQLGrid/external_protocol/W4_MA_EXTERNAL_PROTOCOL_REPORT.md` |
| Human review and sealing requirements | `paper_projects/applied_sciences_dual_rebuild/MA_SQLGrid/data/human_review_packet/REVIEW_PROTOCOL.md` |
| DKASQL identity and verified scope | `paper_projects/applied_sciences_dual_rebuild/MA_SQLGrid/manuscript_support/REFERENCE_AUDIT.md:31,57`; both Round-1 reviews |
| Review defects and required gates | `paper_projects/applied_sciences_dual_rebuild/MA_SQLGrid/reviews/round1_methods_stats_review.md`; `round1_domain_venue_review.md` |

No fact in these assets depends on the superseded manuscript prose. No DKASQL performance number is copied into the comparison table.

