#!/usr/bin/env python3
"""Two-phase reference-free selection then gold scoring for frozen candidates."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = next(parent for parent in HERE.parents if (parent / "paper_projects").is_dir())
SOURCE = REPO / "paper_projects" / "2026_ma_sqlgrid_cmc" / "source"
EXPERIMENT = SOURCE / "code" / "experiment_final"
os.environ["MA_SQLGRID_WORKSPACE"] = str(SOURCE)
sys.path.insert(0, str(EXPERIMENT))

import main as formal  # noqa: E402
import verify_freeze  # noqa: E402


def jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def select(model: str) -> None:
    """Gold-blind phase: parse and rank; no evaluator question file is opened."""
    verify_freeze.main()
    run_dir = HERE / "runs" / model
    predictions = jsonl(run_dir / "predictions.jsonl")
    by_key = {(row["question_id"], row["condition"]): row for row in predictions if row["status"] == "success"}
    prompts = {(row["question_id"], row["condition"]): row for row in jsonl(HERE / "frozen_prompts.jsonl")}
    expected = jsonl(HERE / f"call_order_{model}.jsonl")
    if len(by_key) != len(expected):
        raise RuntimeError(f"incomplete immutable prediction ledger: {len(by_key)}/{len(expected)}")

    import sqlite3

    rows = []
    conn = sqlite3.connect(formal.DB_PATH)
    try:
        for item in expected:
            key = (item["question_id"], item["condition"])
            pred = by_key[key]
            prompt = prompts[key]
            candidates = formal.smoke.extract_candidate_sql(pred["raw_response"])[:3]
            row = {
                "question_id": key[0], "condition": key[1], "candidate_count": len(candidates),
                "candidates": candidates, "first_candidate_sql": candidates[0] if candidates else None,
                "prediction_response_sha256": pred["response_sha256"], "prompt_sha256": prompt["prompt_sha256"],
            }
            if key[1] == "V1_WithValueEvidence" and candidates:
                # Context is reconstructed only from the frozen non-gold question.
                clean = {"question_id": key[0], "question": prompt["question"]}
                context = formal.chess.infer_domain_context(conn, clean)
                rendered = formal.chess.render_selected_context(context, domain=True)
                if hashlib.sha256(rendered.encode()).hexdigest() != prompt["context_sha256"]:
                    raise RuntimeError(f"V1 context reconstruction drift for {key[0]}")
                selected_index, trace = formal.chess.rank_candidates(conn, context, candidates)
                row.update({"selected_candidate_index": selected_index, "selected_sql": candidates[selected_index], "rank_trace": trace})
            else:
                row.update({"selected_candidate_index": 0 if candidates else None,
                            "selected_sql": candidates[0] if candidates else None, "rank_trace": []})
            rows.append(row)
    finally:
        conn.close()
    write_jsonl(run_dir / "candidate_selections.jsonl", rows)
    (run_dir / "SELECTION_SEAL.json").write_text(json.dumps({
        "schema_version": "ma-sqlgrid-candidate-selection-seal-v1", "model": model,
        "gold_loaded": False, "row_count": len(rows),
        "selection_ledger_sha256": sha256_file(run_dir / "candidate_selections.jsonl"),
        "statement": "reference-free selections were persisted before evaluator gold was loaded",
    }, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"PASS: sealed {len(rows)} gold-blind selections for {model}")


def score(model: str) -> None:
    """Gold-aware phase; refuses to run without an intact selection seal."""
    run_dir = HERE / "runs" / model
    seal = json.loads((run_dir / "SELECTION_SEAL.json").read_text(encoding="utf-8"))
    selection_path = run_dir / "candidate_selections.jsonl"
    if seal["gold_loaded"] is not False or sha256_file(selection_path) != seal["selection_ledger_sha256"]:
        raise RuntimeError("selection seal missing or drifted")
    selections = jsonl(selection_path)
    # Gold is first loaded below, after reference-free selections are immutable.
    records = {row["question_id"]: row for row in formal.load_split_records("formal")}
    import sqlite3

    scored = []
    conn = sqlite3.connect(formal.DB_PATH)
    try:
        for row in selections:
            record = records[row["question_id"]]
            def correct(sql: str | None) -> bool:
                return bool(sql) and bool(formal.score_prediction(conn, record, sql).correct)
            candidate_correct = [correct(sql) for sql in row["candidates"]]
            scored.append({
                "question_id": row["question_id"], "condition": row["condition"],
                "candidate_count": row["candidate_count"], "first_correct": correct(row["first_candidate_sql"]),
                "validator_selected_correct": correct(row["selected_sql"]),
                "oracle_at_3_correct_diagnostic_only": any(candidate_correct),
                "candidate_correctness_gold_only": candidate_correct,
                "selection_ledger_sha256": seal["selection_ledger_sha256"],
            })
    finally:
        conn.close()
    write_jsonl(run_dir / "scored_rows.jsonl", scored)
    (run_dir / "SCORING_MANIFEST.json").write_text(json.dumps({
        "schema_version": "ma-sqlgrid-component-scoring-v1", "model": model,
        "row_count": len(scored), "selection_ledger_sha256": seal["selection_ledger_sha256"],
        "scored_rows_sha256": sha256_file(run_dir / "scored_rows.jsonl"),
        "gold_loaded_only_after_selection_seal": True,
    }, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"PASS: scored {len(scored)} sealed rows for {model}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", choices=("select", "score"))
    parser.add_argument("--model", required=True, choices=("qwen", "granite"))
    args = parser.parse_args()
    (select if args.phase == "select" else score)(args.model)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
