"""Score the frozen path utility on the 15-report held-out test split."""
from __future__ import annotations

import json
import statistics
from pathlib import Path

from rsi_common import (
    EVOLUTION_DIR,
    PROTOCOL_PATH,
    RUN_DIR,
    TEST_JSONL,
    assert_run_dir_writable,
    c2ges_select,
    jsonl,
    load_protocol,
    prepare_report,
    sha256,
    textrank_select,
    write_json,
)


def mean_for(rows: list[dict], condition: str, budget: int) -> float:
    values = [
        float(row["rougeL_f1"])
        for row in rows
        if row["condition"] == condition and int(row["word_budget"]) == budget
    ]
    if len(values) != 15:
        raise RuntimeError(f"{condition}@{budget} expected 15 rows, got {len(values)}")
    return statistics.fmean(values)


def main() -> dict:
    protocol = load_protocol()
    freeze = json.loads((EVOLUTION_DIR / "FREEZE.json").read_text(encoding="utf-8"))
    assert_run_dir_writable(RUN_DIR)
    reports = jsonl(TEST_JSONL)
    if len(reports) != 15 or any(row.get("split") != "test" for row in reports):
        raise RuntimeError("evaluation requires the 15-report retained-test JSONL")
    prepared = [prepare_report(row) for row in reports]
    budgets = list(protocol["evaluation"]["word_budgets"])
    settings = protocol["textrank"]
    rows = []
    for report in prepared:
        for budget in budgets:
            nopath = c2ges_select(report, utility=None, path_weight=0.0, word_budget=int(budget))
            redesigned = c2ges_select(
                report,
                utility=freeze["utility"],
                path_weight=float(freeze["path_weight"]),
                word_budget=int(budget),
            )
            textrank = textrank_select(report, int(budget), settings)
            for condition, result in (
                ("no_path_c2ges", nopath),
                ("redesigned_path", redesigned),
                ("textrank", textrank),
            ):
                rows.append(
                    {
                        "doc_id": report["doc_id"],
                        "report_series_id": report["report_series_id"],
                        "condition": condition,
                        "word_budget": int(budget),
                        "selected_sids": result["selected_sids"],
                        "selected_text": result["selected_text"],
                        "reference_text": report["reference"],
                        "actual_words": result["actual_words"],
                        "rougeL_f1": result["rougeL_f1"],
                    }
                )
    summary = {
        "n": 15,
        "label": "held-out-for-this-revision",
        "utility": freeze["utility"],
        "path_weight": freeze["path_weight"],
        "means": {
            "no_path_c2ges": {"110": mean_for(rows, "no_path_c2ges", 110), "260": mean_for(rows, "no_path_c2ges", 260)},
            "redesigned_path": {
                "110": mean_for(rows, "redesigned_path", 110),
                "260": mean_for(rows, "redesigned_path", 260),
            },
            "textrank": {"110": mean_for(rows, "textrank", 110), "260": mean_for(rows, "textrank", 260)},
        },
    }
    summary["wins_both_vs_nopath"] = (
        summary["means"]["redesigned_path"]["110"] >= summary["means"]["no_path_c2ges"]["110"]
        and summary["means"]["redesigned_path"]["260"] >= summary["means"]["no_path_c2ges"]["260"]
    )
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    write_json(
        RUN_DIR / "EVALUATION.json",
        {
            "protocol_sha256": sha256(PROTOCOL_PATH),
            "freeze": freeze,
            "summary": summary,
            "n_rows": len(rows),
        },
    )
    with (RUN_DIR / "SEALED_CHOICES.jsonl").open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    (RUN_DIR / "SEALED").write_text("sealed\n", encoding="utf-8")
    write_json(RUN_DIR / "SUMMARY.json", summary)
    return summary


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, sort_keys=True))
