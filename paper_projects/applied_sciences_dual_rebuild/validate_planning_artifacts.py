#!/usr/bin/env python3
"""Validate W2 experiment, manuscript-budget, and review planning artifacts."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
ERRORS: list[str] = []


def load(name: str):
    path = ROOT / name
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        ERRORS.append(f"{name}: cannot parse JSON: {exc}")
        return {}


def require(condition: bool, message: str) -> None:
    if not condition:
        ERRORS.append(message)


def unique_ids(items, label):
    ids = [item.get("id") for item in items]
    duplicates = [value for value, count in Counter(ids).items() if count > 1]
    require(None not in ids, f"{label}: missing id")
    require(not duplicates, f"{label}: duplicate ids {duplicates}")


def validate_registry(registry):
    levels = registry.get("policy", {}).get("evidence_levels", {})
    minimum = registry.get("policy", {}).get("main_table_minimum")
    require(minimum in levels, "registry: main-table evidence level is undefined")
    experiments = registry.get("experiments", [])
    require(len(experiments) >= 20, "registry: too few experiments for dual-paper matrix")
    unique_ids(experiments, "registry")
    required = {
        "id", "paper", "rq", "class", "priority", "datasets", "split", "conditions",
        "replication", "primary_metrics", "cluster_unit", "tests", "figures", "tables",
        "minimum_main_table_evidence", "blocking_conditions", "status"
    }
    allowed_papers = {"MA-SQLGrid", "C2GES"}
    allowed_classes = {"main", "ablation", "robustness", "sensitivity", "efficiency", "error_analysis", "data_quality"}
    for item in experiments:
        missing = sorted(required - set(item))
        require(not missing, f"{item.get('id')}: missing fields {missing}")
        require(item.get("paper") in allowed_papers, f"{item.get('id')}: invalid paper")
        require(item.get("class") in allowed_classes, f"{item.get('id')}: invalid class")
        require(item.get("minimum_main_table_evidence") == minimum,
                f"{item.get('id')}: main-table evidence must be {minimum}")
        for field in ["rq", "datasets", "conditions", "primary_metrics", "tests", "blocking_conditions"]:
            require(isinstance(item.get(field), list) and len(item.get(field, [])) > 0,
                    f"{item.get('id')}: {field} must be a non-empty list")
        prefix = "MA-" if item.get("paper") == "MA-SQLGrid" else "C2-"
        require(all(str(rq).startswith(prefix) for rq in item.get("rq", [])),
                f"{item.get('id')}: RQ prefix mismatch")
    for paper in allowed_papers:
        classes = {item["class"] for item in experiments if item.get("paper") == paper}
        require({"main", "ablation", "robustness", "sensitivity", "efficiency", "error_analysis"}.issubset(classes),
                f"registry: {paper} lacks a required experiment class")


def validate_budgets(budgets):
    disclaimer = budgets.get("disclaimer", "").lower()
    require("not journal" in disclaimer and "not" in disclaimer, "budgets: missing non-hard-rule disclaimer")
    require(budgets.get("corpus_n") == 10, "budgets: corpus_n must be 10")
    source_path = ROOT.parent.parent / budgets.get("corpus_source", "")
    require(source_path.is_file(), f"budgets: corpus source does not exist: {source_path}")
    if source_path.is_file():
        source = json.loads(source_path.read_text(encoding="utf-8"))
        mapping = {
            "pages": "pages",
            "body_words": "body_words",
            "top_level_sections": "top_level_sections",
            "body_paragraphs": "body_paragraphs",
            "numbered_formulas": "numbered_formulas",
            "datasets_or_cases": "evaluation_datasets",
            "figures": "figures",
            "tables": "tables",
            "framework_diagrams": "method_framework_diagrams",
            "experimental_visuals": "experimental_evidence_visuals",
        }
        distilled = budgets.get("corpus_experience", {})
        for budget_key, source_key in mapping.items():
            for statistic in ("median", "q1", "q3"):
                require(distilled.get(budget_key, {}).get(statistic) == source.get(source_key, {}).get(statistic),
                        f"budgets: {budget_key}.{statistic} differs from corpus source")
    papers = budgets.get("papers", [])
    require({p.get("paper") for p in papers} == {"MA-SQLGrid", "C2GES"}, "budgets: paper set mismatch")
    for paper in papers:
        sections = paper.get("sections", [])
        words = sum(section.get("words", 0) for section in sections)
        require(words == paper.get("target_body_words"), f"budgets: {paper.get('paper')} section words sum to {words}")
        require(len(sections) == paper.get("top_level_sections"), f"budgets: {paper.get('paper')} section count mismatch")
        require([section.get("order") for section in sections] == list(range(1, len(sections) + 1)),
                f"budgets: {paper.get('paper')} section order is not contiguous")
        paragraph_total = sum(section.get("paragraphs", 0) for section in sections)
        low, high = paper.get("target_paragraphs", [0, 0])
        require(low <= paragraph_total <= high, f"budgets: {paper.get('paper')} paragraph total {paragraph_total} outside target")
        require(paper.get("framework_diagrams", 0) <= len(paper.get("figure_plan", [])),
                f"budgets: {paper.get('paper')} framework count exceeds figure plan")
        require(len(paper.get("figure_plan", [])) <= paper.get("figures", [0, 0])[1],
                f"budgets: {paper.get('paper')} figure plan exceeds upper budget")
        require(len(paper.get("table_plan", [])) <= paper.get("tables", [0, 0])[1],
                f"budgets: {paper.get('paper')} table plan exceeds upper budget")


def validate_reviews(reviews):
    checks = reviews.get("checks", [])
    unique_ids(checks, "reviews")
    require(len(checks) >= 30, "reviews: checklist is not comprehensive")
    allowed_status = set(reviews.get("workflow", {}).get("allowed_status", []))
    allowed_severity = {"Critical", "Major", "Minor"}
    for item in checks:
        required = {"id", "round", "role", "papers", "severity_if_fail", "check", "evidence", "status"}
        require(required.issubset(item), f"{item.get('id')}: incomplete review check")
        require(item.get("round") in {1, 2, 3}, f"{item.get('id')}: invalid review round")
        require(item.get("severity_if_fail") in allowed_severity, f"{item.get('id')}: invalid severity")
        require(item.get("status") in allowed_status, f"{item.get('id')}: invalid status")
    for round_number in (1, 2, 3):
        require(sum(item.get("round") == round_number for item in checks) >= 8,
                f"reviews: round {round_number} has fewer than 8 checks")


def main() -> int:
    validate_registry(load("experiment_registry.json"))
    validate_budgets(load("manuscript_budgets.json"))
    validate_reviews(load("review_checklist.json"))
    if ERRORS:
        print("W2 planning artifact validation: FAIL")
        for error in ERRORS:
            print(f"- {error}")
        return 1
    print("W2 planning artifact validation: PASS")
    print("- experiment registry: schema, coverage, evidence gates")
    print("- manuscript budgets: corpus disclaimer, sums, figure/table bounds")
    print("- review checklist: unique IDs, three-round coverage, workflow states")
    return 0


if __name__ == "__main__":
    sys.exit(main())
