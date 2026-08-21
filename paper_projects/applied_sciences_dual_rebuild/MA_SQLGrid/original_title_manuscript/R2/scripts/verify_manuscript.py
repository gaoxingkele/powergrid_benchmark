#!/usr/bin/env python3
"""Fail-closed structural and evidence-boundary checks for MA-SQLGrid R2."""

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
OFFLINE = REBUILD / "prospective_from_freeze_offline_study_v3"
OFFLINE_SUMMARY = OFFLINE / "run_v3a" / "summary.json"
REPRO_CHECK = OFFLINE / "INDEPENDENT_REPRODUCTION_CHECK_V3.json"
OFFLINE_AUDIT = OFFLINE / "INDEPENDENT_RELEASE_AUDIT_V3.md"
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
        "deterministic adjudicator",
        "deterministic no-generation descriptive re-execution",
        "frozen pre-run regression suite had accessed gold-derived v2 outcomes for the same items",
        "database-enforced",
        "incomplete 1/1 record cannot outrank a complete 10/11 record",
        "Zero of nine primary execution tests survives Holm correction",
        "700 scored calls",
        "25,920 registered rows",
        "5000 calls",
        "172 of 180",
        "No retrospective accuracy",
        "101/180",
        "80/180",
        "117--118/180",
        "shared precomputed",
        "Q039",
        "nullable-schema-extension projection-stability case",
        "BIRD Mini-Dev is a public non-grid portability benchmark",
        "must be synchronized and tagged before submission",
        r"\begin{table}",
        r"\toprule",
        r"\bottomrule",
        r"\dataavailability{",
        r"\authorcontributions{",
        "All authors have read and agreed to the published version of the manuscript",
        "grant number 521300250006",
        "https://github.com/gaoxingkele/ma-sqlgrid",
        "may be requested from the corresponding author for editorial and peer-review verification",
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
        "prospective-from-freeze",
        "prespecified sensitivity",
        "outcome-unseen",
        "outcome-blind scientific release",
    ]
    for token in prohibited:
        if token.lower() in text.lower():
            errors.append(f"prohibited unsupported/promoted content found: {token}")

    if text.count(r"\begin{table}") < 7 or text.count(r"\toprule") < 7:
        errors.append("fewer than seven R2 booktabs tables are present")

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
    if "figures/fig_ma_sqlgrid_implemented_coordination_r2.png" not in figures:
        errors.append("R2 executor/coordination framework figure is not included")

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

    if not OFFLINE_SUMMARY.is_file() or not REPRO_CHECK.is_file() or not OFFLINE_AUDIT.is_file():
        errors.append("missing R2 v3 offline-study summary, reproduction check, or independent audit")
    else:
        offline = json.loads(OFFLINE_SUMMARY.read_text(encoding="utf-8"))
        expected_methods = {
            "fixed_order_equal_budget": (80, 180, 0),
            "validation_rank_equal_budget_no_cf": (100, 180, 0),
            "full_coordination_complete_metamorphic": (101, 180, 0),
        }
        for method, (correct, covered, abstained) in expected_methods.items():
            row = offline["methods"].get(method, {})
            if (row.get("correct"), row.get("covered"), row.get("abstained")) != (correct, covered, abstained):
                errors.append(f"offline summary invariant mismatch: {method}")
        if offline.get("freeze_content_sha256") != "8b34bc370451173197ad07b460908537836409d6eb49f303caf46d13d53889e6":
            errors.append("offline freeze hash mismatch")
        repro = json.loads(REPRO_CHECK.read_text(encoding="utf-8"))
        if not repro.get("all_canonical_outputs_identical"):
            errors.append("offline independent reproductions are not identical")
        audit_text = OFFLINE_AUDIT.read_text(encoding="utf-8")
        if "FAIL for the claimed prospective-from-freeze evidence class" not in audit_text or "PASS for mechanical integrity" not in audit_text:
            errors.append("offline v3 split release-audit decision is not preserved")

    if errors:
        for error in errors:
            print("FAIL:", error)
        print(f"R2 verification failed with {len(errors)} error(s).")
        return 1
    print(
        f"PASS: original title, {len(cited)} citation keys, {len(figures)} figures, "
        "R2 booktabs tables, retrospective boundary, and offline dual reproduction verified."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
