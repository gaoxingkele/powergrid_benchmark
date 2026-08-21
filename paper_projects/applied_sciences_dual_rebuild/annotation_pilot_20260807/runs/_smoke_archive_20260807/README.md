# Smoke-run archive (2026-08-07, 14 LLM calls, limit=2 per paper)

These records come from the pre-pilot smoke test. They exposed two RUNNER-side defects
(not model behavior): (1) the runner prompt did not show the qid/question_id to the
annotators, making the frozen "qid echoes input" deterministic check unsatisfiable;
(2) gemini-2.5-flash thinking tokens consumed the 1024-token output budget, truncating
JSON. Both defects were fixed in run_annotation_pilot.py before the real pilot
(qid now embedded in the QUESTION line; Gemini thinkingConfig.thinkingBudget=0).
Per governance, nothing was deleted: all raw ledger entries, parsed labels,
adjudications and manifests are preserved here. These records are EXCLUDED from the
final pilot statistics because the measurement instrument was non-conformant;
they are retained for audit. The 14 calls count toward the 400-call global cap.
