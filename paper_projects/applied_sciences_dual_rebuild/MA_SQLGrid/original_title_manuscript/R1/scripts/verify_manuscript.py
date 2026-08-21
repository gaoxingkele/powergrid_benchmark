#!/usr/bin/env python3
"""Fail-closed structural and evidence-boundary checks for MA-SQLGrid R1."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


HERE = Path(__file__).resolve()
R1 = HERE.parent.parent
MA_ROOT = R1.parent.parent
TEX = R1 / "paper_applsci.tex"
BIB = R1 / "references_verified.bib"
REBUILD = MA_ROOT / "original_title_rebuild"
REPLAY_MANIFEST = REBUILD / "retrospective_diagnostic" / "manifest.json"
FIGURE_LINEAGE = R1 / "figures" / "FIGURE_LINEAGE.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    errors: list[str] = []
    text = TEX.read_text(encoding="utf-8")

    required = [
        r"\documentclass[applsci,article,submit,moreauthors]{Definitions/mdpi}",
        "MA-SQLGrid: A Robust Multi-Agent Framework for Text-to-SQL in Power Grid Databases",
        "Query Analyst",
        "Schema Cartographer",
        "SQL Synthesizer",
        "Validation Engine",
        "Counterfactual Critic",
        "append-only blackboard",
        "deterministic Adjudicator",
        "retrospective offline coordination diagnostic",
        "coverage only, not accuracy or multi-agent improvement",
        "Zero of nine primary execution tests survives Holm correction",
        "700 scored calls",
        "25,920 registered rows",
        "5000 generation calls",
        "172 of 180",
        "No retrospective accuracy",
        r"\begin{table}",
        r"\toprule",
        r"\bottomrule",
        r"\dataavailability{",
        r"\authorcontributions{",
        "All authors have read and agreed to the published version of the manuscript",
        "grant number 521300250006",
        "https://github.com/gaoxingkele/ma-sqlgrid",
        "available from the corresponding author upon reasonable request for editorial and peer-review verification",
    ]
    for token in required:
        if token not in text:
            errors.append(f"required R1 content missing: {token}")

    for section in (
        "Introduction",
        "Related Work",
        "Materials and Methods",
        "Results",
        "Discussion",
        "Limitations and Future Work",
        "Conclusions",
    ):
        if rf"\section{{{section}}}" not in text:
            errors.append(f"required section missing: {section}")

    prohibited = [
        "88.2\\%",
        "91.7\\%",
        "93.5\\%",
        "80,654",
        "10,181",
        "5,693",
        "24,241",
        "state-of-the-art Execution Accuracy",
        "multi-agent framework significantly outperformed",
        "EVIDENCE SLOT",
        "retrospectively selected query is more accurate",
    ]
    for token in prohibited:
        if token.lower() in text.lower():
            errors.append(f"prohibited unsupported/promoted content found: {token}")

    if text.count(r"\begin{table}") < 2 or text.count(r"\toprule") < 2:
        errors.append("the two Markdown result tables were not both converted to booktabs tables")

    bib_text = BIB.read_text(encoding="utf-8")
    bib_keys = set(re.findall(r"@[A-Za-z]+\s*\{\s*([^,\s]+)", bib_text))
    cited: set[str] = set()
    for group in re.findall(r"\\cite[pt]?\{([^}]+)\}", text):
        cited.update(key.strip() for key in group.split(","))
    missing = sorted(cited - bib_keys)
    if missing:
        errors.append("missing bibliography keys: " + ", ".join(missing))

    figures = re.findall(r"\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}", text)
    for rel in figures:
        path = R1 / rel
        if not path.is_file() or path.stat().st_size == 0:
            errors.append(f"missing or empty figure: {rel}")
    if "figures/fig_ma_sqlgrid_implemented_coordination_r1_qa3.png" not in figures:
        errors.append("implemented coordination framework figure is not included")

    if not FIGURE_LINEAGE.is_file():
        errors.append("missing framework figure lineage")
    else:
        lineage = json.loads(FIGURE_LINEAGE.read_text(encoding="utf-8"))["artifact"]
        svg = R1 / "figures" / lineage["file"]
        if not svg.is_file() or sha(svg).upper() != lineage["sha256"].upper():
            errors.append("framework SVG does not match its lineage hash")

    if not REPLAY_MANIFEST.is_file():
        errors.append("missing retrospective diagnostic manifest")
    else:
        replay = json.loads(REPLAY_MANIFEST.read_text(encoding="utf-8"))
        summary = replay.get("summary", {})
        expected = {
            "question_count": 180,
            "questions_with_at_least_two_unique_candidates": 173,
            "questions_with_at_least_two_eligible_candidates": 172,
            "questions_with_reference_free_counterfactual_evidence": 0,
            "accuracy_claim_authorized": False,
        }
        for key, value in expected.items():
            if summary.get(key) != value:
                errors.append(f"retrospective manifest invariant mismatch: {key}")
        for name, spec in replay.get("inputs", {}).items():
            path = Path(spec["path"])
            if not path.is_file() or sha(path) != spec["sha256"]:
                errors.append(f"retrospective frozen input mismatch: {name}")

    if errors:
        for error in errors:
            print("FAIL:", error)
        print(f"R1 verification failed with {len(errors)} error(s).")
        return 1
    print(
        f"PASS: original title, {len(cited)} citation keys, {len(figures)} figures, "
        "two booktabs tables, and retrospective evidence boundary verified."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
