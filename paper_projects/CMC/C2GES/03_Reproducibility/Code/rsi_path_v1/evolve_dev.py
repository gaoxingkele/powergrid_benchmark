"""Evolve path utilities on the 12-report development split only."""
from __future__ import annotations

import json
import statistics
from pathlib import Path

from path_utilities import UTILITIES
from rsi_common import (
    DEV_JSONL,
    EVOLUTION_DIR,
    PROTOCOL_PATH,
    TEST_JSONL,
    c2ges_select,
    jsonl,
    load_protocol,
    prepare_report,
    sha256,
    write_json,
)


def freeze_sort_key(row: dict) -> tuple:
    return (
        -float(row["mean_both"]),
        -float(row["mean_260"]),
        -float(row["mean_110"]),
        float(row["mean_redundancy_proxy"]),
        str(row["utility"]),
        float(row["path_weight"]),
    )


def main() -> dict:
    protocol = load_protocol()
    if TEST_JSONL.resolve() in {DEV_JSONL.resolve()}:
        raise RuntimeError("dev and test paths collided")
    reports = jsonl(DEV_JSONL)
    if len(reports) != 12 or any(row.get("split") != "dev" for row in reports):
        raise RuntimeError("evolution requires the 12-report development JSONL")
    prepared = [prepare_report(row) for row in reports]
    budgets = list(protocol["evaluation"]["word_budgets"])
    records = []
    # no-path reference
    variants = [("no_path", None, 0.0)]
    for utility in UTILITIES:
        for weight in protocol["path_weights"]:
            variants.append((f"{utility}:{weight}", utility, float(weight)))
    for variant_id, utility, weight in variants:
        per_budget = {110: [], 260: []}
        items = []
        for report in prepared:
            for budget in budgets:
                result = c2ges_select(
                    report, utility=utility, path_weight=weight, word_budget=int(budget)
                )
                per_budget[int(budget)].append(result["rougeL_f1"])
                items.append(
                    {
                        "doc_id": report["doc_id"],
                        "word_budget": int(budget),
                        "rougeL_f1": result["rougeL_f1"],
                        "actual_words": result["actual_words"],
                        "n_selected": len(result["selected_sids"]),
                    }
                )
        mean_110 = statistics.fmean(per_budget[110])
        mean_260 = statistics.fmean(per_budget[260])
        records.append(
            {
                "variant_id": variant_id,
                "utility": utility,
                "path_weight": weight,
                "mean_110": mean_110,
                "mean_260": mean_260,
                "mean_both": (mean_110 + mean_260) / 2.0,
                "mean_redundancy_proxy": statistics.fmean(
                    item["n_selected"] for item in items
                ),
                "items": items,
            }
        )
    candidates = [row for row in records if row["path_weight"] > 0]
    chosen = sorted(candidates, key=freeze_sort_key)[0]
    nopath = next(row for row in records if row["variant_id"] == "no_path")
    freeze = {
        "protocol_sha256": sha256(PROTOCOL_PATH),
        "protocol_seed": protocol["seed"],
        "dev_jsonl_sha256": sha256(DEV_JSONL),
        "utility": chosen["utility"],
        "path_weight": chosen["path_weight"],
        "dev_mean_110": chosen["mean_110"],
        "dev_mean_260": chosen["mean_260"],
        "no_path_dev_mean_110": nopath["mean_110"],
        "no_path_dev_mean_260": nopath["mean_260"],
        "wins_both_dev_budgets": chosen["mean_110"] >= nopath["mean_110"]
        and chosen["mean_260"] >= nopath["mean_260"],
        "freeze_rule": protocol["freeze_rule"],
    }
    EVOLUTION_DIR.mkdir(parents=True, exist_ok=True)
    write_json(EVOLUTION_DIR / "EVOLUTION.json", {"records": records, "n_dev": 12})
    write_json(EVOLUTION_DIR / "FREEZE.json", freeze)
    return freeze


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, sort_keys=True))
