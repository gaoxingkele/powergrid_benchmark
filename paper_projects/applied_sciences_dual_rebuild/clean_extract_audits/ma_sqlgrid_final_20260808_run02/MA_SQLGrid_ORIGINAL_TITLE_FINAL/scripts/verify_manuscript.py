#!/usr/bin/env python3
"""Fail-closed, self-contained structural verifier for the FINAL candidate."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEX = ROOT / "paper_applsci.tex"
BIB = ROOT / "references_verified.bib"
EVIDENCE = ROOT / "evidence/evidence_tables/R3_EVIDENCE_TABLES.json"
SUMMARY = ROOT / "evidence/release_v3/release_v3_summary.json"
REPRO = ROOT / "evidence/release_v3/INDEPENDENT_REPRODUCTION_CHECK_V3.json"
NOTICE = ROOT / "evidence/SUPERSESSION_NOTICE.json"
REPLAY = ROOT / "evidence/release_v3/retrospective_manifest.json"
LINEAGE = ROOT / "figures/FIGURE_LINEAGE.json"
EXECUTOR = ROOT / "code/sqlite_readonly_executor_final.py"
EXECUTOR_TEST = ROOT / "tests/test_sqlite_readonly_executor_final.py"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    errors: list[str] = []
    text = TEX.read_text(encoding="utf-8")

    required = [
        r"\documentclass[applsci,article,submit,moreauthors]{Definitions/mdpi}",
        "MA-SQLGrid: A Robust Multi-Agent Framework for Text-to-SQL in Power Grid Databases",
        "Liu Bijing", "Sun Chenglong", "Yang Yong",
        "Correspondence: Yang Yong",
        "email address to be provided before submission",
        "framework identity rather than an empirical superiority claim",
        "130/180", "5.4000", "5.3889", "117--118/180", "Q039",
        "invalid transient 33/33", "SUPERSESSION\\_NOTICE.json",
        "FINAL raw-cell-byte", "1, 5, and 50 MB", "14 additive tests",
        "were \\emph{not} used to obtain its 5760-attempt ledger",
        "not authentication, identity management, row-level access control",
        "Final-ledger omissions", "Generative-AI Assistance and Author Responsibility",
        "exact backend model identifier and version for every Codex session were not retained",
        "must be synchronized and tagged before submission",
        "may be requested from the corresponding author for editorial and peer-review verification",
        "All authors have read and agreed to the published version of the manuscript",
        "grant number 521300250006",
    ]
    for token in required:
        if token not in text:
            errors.append(f"required FINAL content missing: {token}")

    prohibited = [
        "state-of-the-art Execution Accuracy",
        "multi-agent framework significantly outperformed",
        "outcome-blind scientific release",
        "five-role end-to-end gain",
        "33/33 tests passed",
        "current public contents match this manuscript",
        "Implemented R2",
        "fig_ma_sqlgrid_implemented_coordination_r2",
        "OpenAI Codex (GPT-5-based)",
    ]
    for token in prohibited:
        if token.lower() in text.lower():
            errors.append(f"prohibited or stale content found: {token}")

    for section in (
        "Introduction", "Related Work", "Materials and Methods", "Results",
        "Discussion", "Limitations and Future Work", "Conclusions",
    ):
        if rf"\section{{{section}}}" not in text:
            errors.append(f"required section missing: {section}")
    if text.count(r"\begin{table}") < 12:
        errors.append("fewer than twelve tables")

    bib_keys = set(re.findall(r"@[A-Za-z]+\s*\{\s*([^,\s]+)", BIB.read_text(encoding="utf-8")))
    cited: set[str] = set()
    for group in re.findall(r"\\cite[pt]?\{([^}]+)\}", text):
        cited.update(item.strip() for item in group.split(","))
    if cited - bib_keys:
        errors.append("missing bibliography keys: " + ", ".join(sorted(cited - bib_keys)))

    used_figures = re.findall(r"\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}", text)
    for rel in used_figures:
        if not (ROOT / rel).is_file():
            errors.append(f"missing figure: {rel}")
    lineage = json.loads(LINEAGE.read_text(encoding="utf-8"))
    if (
        not lineage.get("all_used_figures_covered")
        or lineage.get("figure_count") != 4
        or len(used_figures) != 4
    ):
        errors.append("figure-lineage cardinality/coverage mismatch")
    for figure in lineage.get("figures", []):
        for entry in figure.get("outputs", []) + figure.get("sources", []):
            path = ROOT / entry["path"]
            if not path.is_file() or path.stat().st_size != entry["bytes"] or sha(path) != entry["sha256"]:
                errors.append(f"figure-lineage mismatch: {entry['path']}")

    summary = json.loads(SUMMARY.read_text(encoding="utf-8"))
    expected = {
        "fixed_order_equal_budget": (80, 180, 0),
        "validation_rank_equal_budget_no_cf": (100, 180, 0),
        "full_coordination_complete_metamorphic": (101, 180, 0),
    }
    for method, values in expected.items():
        row = summary.get("methods", {}).get(method, {})
        if (row.get("correct"), row.get("covered"), row.get("abstained")) != values:
            errors.append(f"v3 summary mismatch: {method}")
    if summary.get("freeze_content_sha256") != "8b34bc370451173197ad07b460908537836409d6eb49f303caf46d13d53889e6":
        errors.append("v3 freeze hash mismatch")
    if not json.loads(REPRO.read_text(encoding="utf-8")).get("all_canonical_outputs_identical"):
        errors.append("v3 reproduction mismatch")
    notice = json.loads(NOTICE.read_text(encoding="utf-8"))
    if notice.get("decision", {}).get("prospective_from_freeze") != "SUPERSEDED_AND_INVALID":
        errors.append("supersession decision mismatch")
    replay = json.loads(REPLAY.read_text(encoding="utf-8")).get("summary", {})
    if (replay.get("question_count"), replay.get("questions_with_at_least_two_eligible_candidates"), replay.get("accuracy_claim_authorized")) != (180, 172, False):
        errors.append("retrospective replay mismatch")
    evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    checks = evidence.get("integrity_checks", {})
    if (checks.get("tie_item_rows"), checks.get("griddb_cells"), checks.get("multistate_cells"), checks.get("sensitivity_cells")) != (360, 8, 8, 18):
        errors.append("evidence-table cardinality mismatch")

    for path in (EXECUTOR, EXECUTOR_TEST, ROOT / "FINAL_RESPONSE_MATRIX.md", ROOT / "RIGHTS_INVENTORY.csv"):
        if not path.is_file() or path.stat().st_size == 0:
            errors.append(f"missing FINAL artifact: {path.name}")
    code = EXECUTOR.read_text(encoding="utf-8")
    if "used only by the post-review FINAL executor tests" not in code or "were not used by" not in code:
        errors.append("FINAL executor docstring does not preserve historical boundary")

    if errors:
        for error in errors:
            print("FAIL:", error)
        print(f"FINAL verification failed with {len(errors)} error(s).")
        return 1
    print(
        f"PASS: exact title/authors, {len(cited)} cited keys, {len(used_figures)} fully "
        "lineaged figures, 12+ tables, v3 boundaries, FINAL executor claims, and manual gates verified."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
