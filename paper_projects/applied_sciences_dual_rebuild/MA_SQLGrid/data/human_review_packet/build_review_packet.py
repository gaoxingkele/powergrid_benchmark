#!/usr/bin/env python3
"""Build a machine-precheck and two-person blind review packet for MA data.

Machine flags are deterministic triage hints only.  They do not constitute
human, author, or domain-expert review and cannot promote an item to gold or
sealed status.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
import re
from collections import Counter, defaultdict
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any


PACKET_VERSION = "ma-human-review-packet-1.0"
REVIEW_FIELDS = [
    "review_order", "blind_item_id", "dataset", "question", "gold_sql", "query_class_proposed",
    "difficulty_proposed", "referenced_tables", "result_columns", "result_row_count", "result_preview",
    "decision", "semantic_alignment", "question_unambiguous", "units_correct", "sql_correct",
    "answer_useful", "query_class_reviewed", "difficulty_reviewed", "issue_codes", "proposed_question",
    "proposed_sql", "confidence_1_to_5", "reviewer_qualification", "reviewer_signature", "completed_at_utc",
    "reviewer_notes"
]
CONTROLLED_ISSUES = [
    "AMBIGUOUS_SCOPE", "AMBIGUOUS_ORDER", "MISSING_UNIT", "WRONG_UNIT", "QUESTION_SQL_MISMATCH",
    "EMPTY_ANSWER", "UNBOUNDED_RESULT", "DUPLICATE_TEMPLATE", "UNNATURAL_LANGUAGE", "DOMAIN_TERM_UNCLEAR",
    "WRONG_DIFFICULTY", "WRONG_QUERY_CLASS", "SQL_ERROR", "ANSWER_NOT_USEFUL", "OTHER"
]


def jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl(path: Path, values: list[dict[str, Any]]) -> None:
    path.write_text("".join(json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n" for value in values), encoding="utf-8")


def write_csv(path: Path, fields: list[str], values: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(values)


def load_candidates(data_root: Path) -> list[dict[str, Any]]:
    rts_root = data_root / "rts_gmlc_pilot/artifacts"
    sim_root = data_root / "simbench_pilot"
    rts_results = {row["question_id"]: row for row in jsonl(rts_root / "gold_execution.jsonl")}
    sim_results = {row["question_id"]: row for row in jsonl(sim_root / "gold_execution_results.jsonl")}
    values = []
    for row in jsonl(rts_root / "questions_auto_candidate.jsonl"):
        result = rts_results[row["question_id"]]
        values.append({
            "dataset": "RTS-GMLC", "source_question_id": row["question_id"], "question": row["question"],
            "gold_sql": row["gold_sql"].rstrip(";"), "query_class": classify_rts(row),
            "difficulty": row["difficulty"], "template_family": row["template_family"], "split": row["split"],
            "annotation_status": row["annotation_status"], "human_reviewed": bool(row["human_reviewed"]),
            "sealed": bool(row["sealed"]), "tables": row["tables"], "result_columns": result["columns"],
            "result_row_count": result["row_count"], "result_preview": result.get("result_preview", []),
            "result_sha256": result["result_sha256"], "sql_sha256": row["gold_sql_sha256"],
        })
    with (sim_root / "questions_auto_candidate.csv").open(encoding="utf-8", newline="") as handle:
        sim_questions = list(csv.DictReader(handle))
    for row in sim_questions:
        result = sim_results[row["question_id"]]
        values.append({
            "dataset": "SimBench", "source_question_id": row["question_id"],
            "question": row["natural_language"], "gold_sql": row["gold_sql"],
            "query_class": row["query_class"], "difficulty": infer_simbench_difficulty(row["query_class"]),
            "template_family": row["template_family_id"], "split": row["split"],
            "annotation_status": row["provenance_label"],
            "human_reviewed": row["human_gold"].lower() == "true", "sealed": row["sealed"].lower() == "true",
            "tables": extract_tables(row["gold_sql"]), "result_columns": result["columns"],
            "result_row_count": result["row_count"], "result_preview": result["rows"][:5],
            "result_sha256": result["result_sha256"],
            "sql_sha256": hashlib.sha256(row["gold_sql"].encode("utf-8")).hexdigest(),
        })
    return sorted(values, key=lambda value: (value["dataset"], value["source_question_id"]))


def classify_rts(row: dict[str, Any]) -> str:
    tags = set(row.get("sql_feature_tags", []))
    if "top-k" in tags:
        return "top_k"
    if "join" in tags:
        return "join"
    if "aggregate" in tags:
        return "aggregate"
    if "filter" in tags:
        return "filter"
    return "single_table"


def infer_simbench_difficulty(query_class: str) -> str:
    return {"single_table": "easy", "filter": "easy", "aggregate": "medium", "join": "medium",
            "top_k": "medium", "topology": "hard"}[query_class]


def extract_tables(sql: str) -> list[str]:
    return sorted(set(re.findall(r"\b(?:FROM|JOIN)\s+([A-Za-z_][A-Za-z0-9_]*)", sql, flags=re.I)))


def blind_id(item: dict[str, Any]) -> str:
    digest = hashlib.sha256(f"{item['dataset']}:{item['source_question_id']}".encode()).hexdigest()[:12].upper()
    return f"MAHR-{digest}"


def normalize_template(question: str) -> str:
    text = question.lower()
    text = re.sub(r"'[^']*'|\b\d{1,4}(?:[-:.]\d{1,4})+\b|\b\d+(?:\.\d+)?\b", "<value>", text)
    text = re.sub(r"\b(solar|wind|hydro|ng|coal|oil|nuclear)\b", "<category>", text)
    return " ".join(re.findall(r"[a-z]+|<[^>]+>", text))


def family_similarity(items: list[dict[str, Any]]) -> dict[str, float]:
    output = {}
    groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for item in items:
        groups[(item["dataset"], item["template_family"])].append(item)
    for group in groups.values():
        for item in group:
            others = [candidate for candidate in group if candidate is not item]
            output[blind_id(item)] = max(
                (SequenceMatcher(None, normalize_template(item["question"]), normalize_template(other["question"])).ratio()
                 for other in others), default=0.0)
    return output


def unit_tokens(columns: list[str]) -> set[str]:
    tokens = set()
    joined = " ".join(columns).lower()
    for marker, token in [("_mw", "mw"), ("_mva", "mva"), ("_mvar", "mvar"), ("_kv", "kv"),
                          ("_km", "km"), ("percent", "percent"), ("_usd", "usd")]:
        if marker in joined:
            tokens.add(token)
    return tokens


def precheck(item: dict[str, Any], similarity: float) -> dict[str, Any]:
    question = item["question"].lower()
    sql = item["gold_sql"].upper()
    flags = []
    high = []
    semantic_rules = [
        ("how many" in question and "COUNT(" not in sql, "HOW_MANY_WITHOUT_COUNT"),
        ("total" in question and "SUM(" not in sql, "TOTAL_WITHOUT_SUM"),
        ("average" in question and "AVG(" not in sql, "AVERAGE_WITHOUT_AVG"),
        (any(term in question for term in ("highest", "largest", "longest", "most often", "top ")) and
         not ("ORDER BY" in sql and "LIMIT" in sql), "RANKING_WITHOUT_ORDER_LIMIT"),
        (item["query_class"] == "join" and " JOIN " not in sql, "JOIN_CLASS_WITHOUT_JOIN"),
    ]
    for triggered, code in semantic_rules:
        if triggered:
            flags.append(code)
            high.append(code)
    required_units = unit_tokens(item["result_columns"])
    missing_units = sorted(unit for unit in required_units if unit not in question and
                           not (unit == "percent" and "%" in question))
    if missing_units:
        flags.append("UNIT_NOT_EXPLICIT:" + "/".join(missing_units))
    if item["result_row_count"] == 0:
        flags.append("EMPTY_RESULT")
        high.append("EMPTY_RESULT")
    elif item["result_row_count"] > 500:
        flags.append("VERY_LARGE_RESULT")
        high.append("VERY_LARGE_RESULT")
    elif item["result_row_count"] > 50:
        flags.append("LARGE_RESULT")
    if "first" in question:
        flags.append("ORDERING_CONVENTION_REVIEW")
    if any(term in question for term in ("highest", "largest", "longest", "top ")):
        flags.append("TOP_K_TIE_POLICY_REVIEW")
    if re.search(r"\bng\b", question):
        flags.append("DOMAIN_ABBREVIATION_REVIEW")
    if similarity >= 0.90:
        flags.append("HIGH_TEMPLATE_SIMILARITY")
    if not sql.startswith(("SELECT", "WITH")) or ";" in item["gold_sql"]:
        flags.append("SQL_SAFETY_OR_MULTISTATEMENT")
        high.append("SQL_SAFETY_OR_MULTISTATEMENT")
    medium_markers = bool(flags)
    risk = "high" if high else "medium" if medium_markers else "low"
    return {
        **item, "blind_item_id": blind_id(item), "machine_risk_level": risk,
        "machine_flags": flags, "unit_tokens_in_result_columns": sorted(required_units),
        "maximum_within_family_question_similarity": round(similarity, 4),
        "machine_precheck_only": True,
        "machine_judgment_disclaimer": "Heuristic triage only; requires two independent human reviews.",
    }


def form_row(item: dict[str, Any], order: int) -> dict[str, Any]:
    return {
        "review_order": order, "blind_item_id": item["blind_item_id"], "dataset": item["dataset"],
        "question": item["question"], "gold_sql": item["gold_sql"],
        "query_class_proposed": item["query_class"], "difficulty_proposed": item["difficulty"],
        "referenced_tables": "|".join(item["tables"]), "result_columns": "|".join(item["result_columns"]),
        "result_row_count": item["result_row_count"],
        "result_preview": json.dumps(item["result_preview"], ensure_ascii=False, separators=(",", ":")),
        **{field: "" for field in REVIEW_FIELDS[11:]},
    }


def adjudication_rows(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    fields = ["blind_item_id", "dataset", "source_question_id", "reviewer_a_decision", "reviewer_b_decision",
              "conflict_fields", "adjudicator_decision", "final_question", "final_sql", "change_reason",
              "reexecution_result_sha256", "adjudicator_qualification", "adjudicator_signature", "completed_at_utc"]
    return fields, [{**{field: "" for field in fields}, "blind_item_id": item["blind_item_id"],
                     "dataset": item["dataset"], "source_question_id": item["source_question_id"]} for item in items]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    items = load_candidates(args.data_root.resolve())
    if len(items) != 91:
        raise RuntimeError(f"Expected RTS 55 + SimBench 36 = 91 candidates, found {len(items)}")
    similarities = family_similarity(items)
    audited = [precheck(item, similarities[blind_id(item)]) for item in items]
    write_jsonl(output / "machine_precheck.jsonl", audited)
    write_csv(output / "review_item_map.csv",
              ["blind_item_id", "dataset", "source_question_id", "template_family", "split", "annotation_status",
               "human_reviewed", "sealed", "result_sha256", "sql_sha256"], audited)
    summary = {
        "schema_version": PACKET_VERSION, "candidate_count": len(audited),
        "dataset_counts": dict(Counter(item["dataset"] for item in audited)),
        "query_class_counts": dict(Counter(item["query_class"] for item in audited)),
        "difficulty_counts": dict(Counter(item["difficulty"] for item in audited)),
        "risk_counts": dict(Counter(item["machine_risk_level"] for item in audited)),
        "empty_result_count": sum(item["result_row_count"] == 0 for item in audited),
        "large_result_over_50_count": sum(item["result_row_count"] > 50 for item in audited),
        "maximum_result_rows": max(item["result_row_count"] for item in audited),
        "machine_precheck_is_human_review": False, "human_review_completion_count": 0,
        "sealed_count": sum(item["sealed"] for item in audited),
        "flag_counts": dict(Counter(flag.split(":")[0] for item in audited for flag in item["machine_flags"])),
    }
    write_json(output / "machine_precheck_summary.json", summary)
    for reviewer, seed in (("A", 20260811), ("B", 20260812)):
        shuffled = list(audited)
        random.Random(seed).shuffle(shuffled)
        write_csv(output / f"reviewer_{reviewer}_form.csv", REVIEW_FIELDS,
                  [form_row(item, index) for index, item in enumerate(shuffled, 1)])
    adjudication_fields, adjudication = adjudication_rows(audited)
    write_csv(output / "conflict_adjudication_template.csv", adjudication_fields, adjudication)
    packet_hashes = {}
    for name in ["machine_precheck.jsonl", "machine_precheck_summary.json", "review_item_map.csv",
                 "reviewer_A_form.csv", "reviewer_B_form.csv", "conflict_adjudication_template.csv"]:
        packet_hashes[name] = hashlib.sha256((output / name).read_bytes()).hexdigest()
    write_json(output / "packet_hashes.json", {"schema_version": PACKET_VERSION, "sha256": packet_hashes})
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
