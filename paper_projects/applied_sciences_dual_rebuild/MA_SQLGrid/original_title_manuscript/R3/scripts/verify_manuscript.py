#!/usr/bin/env python3
"""Fail-closed structural and evidence-boundary checks for MA-SQLGrid R3."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


HERE = Path(__file__).resolve()
ROUND = HERE.parent.parent
MA_ROOT = ROUND.parent.parent
TEX = ROUND / "paper_applsci.tex"
BIB = ROUND / "references_verified.bib"
REBUILD = MA_ROOT / "original_title_rebuild"
REPLAY_MANIFEST = REBUILD / "retrospective_diagnostic" / "manifest.json"
OFFLINE = REBUILD / "prospective_from_freeze_offline_study_v3"
OFFLINE_SUMMARY = OFFLINE / "run_v3a" / "summary.json"
REPRO_CHECK = OFFLINE / "INDEPENDENT_REPRODUCTION_CHECK_V3.json"
OFFLINE_AUDIT = OFFLINE / "INDEPENDENT_RELEASE_AUDIT_V3.md"
SUPERSESSION = OFFLINE / "SUPERSESSION_NOTICE.json"
EVIDENCE = ROUND / "evidence" / "evidence_tables" / "R3_EVIDENCE_TABLES.json"
Q039 = ROUND / "evidence" / "evidence_tables" / "q039_projection_trace.csv"
R3_EXECUTOR = ROUND / "code" / "sqlite_readonly_executor_r3.py"
R3_TEST = ROUND / "tests" / "test_sqlite_readonly_executor_r3.py"
FIGURE_LINEAGE = ROUND / "figures" / "FIGURE_LINEAGE.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    errors: list[str] = []
    text = TEX.read_text(encoding="utf-8")

    required = [
        r"\documentclass[applsci,article,submit,moreauthors]{Definitions/mdpi}",
        "MA-SQLGrid: A Robust Multi-Agent Framework for Text-to-SQL in Power Grid Databases",
        "framework identity rather than an empirical superiority claim",
        "typed five-role software decomposition",
        "deterministic no-generation",
        "SUPERSESSION\\_NOTICE.json",
        "130/180",
        "5.4000",
        "5.3889",
        "Q039",
        "Show the first scheduled work order after June 2024",
        "117--118/180",
        "all 18 sensitivity cells",
        "700-call audited prospective component protocol",
        "21-\\emph{artifact}",
        "30/30 tests",
        "10/10 tests",
        "invalid transient 33/33",
        "were \\emph{not} used to obtain its 5760-attempt ledger",
        "not authentication, identity management, row-level access control",
        "must be synchronized and tagged before submission",
        "may be requested from the corresponding author for editorial and peer-review verification",
        "All authors have read and agreed to the published version of the manuscript",
        "grant number 521300250006",
    ]
    for token in required:
        if token not in text:
            errors.append(f"required R3 content missing: {token}")

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
        "state-of-the-art Execution Accuracy",
        "multi-agent framework significantly outperformed",
        "prospective-from-freeze",
        "outcome-blind scientific release",
        "five-role end-to-end gain",
        "33/33 tests passed",
        "current public contents match this manuscript",
        "A manuscript-bound archive has been prepared",
    ]
    for token in prohibited:
        if token.lower() in text.lower():
            errors.append(f"prohibited unsupported/promoted content found: {token}")

    if text.count(r"\begin{table}") < 12 or text.count(r"\toprule") < 12:
        errors.append("fewer than twelve R3 booktabs tables are present")

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
        path = ROUND / rel
        if not path.is_file() or path.stat().st_size == 0:
            errors.append(f"missing or empty figure: {rel}")

    if not FIGURE_LINEAGE.is_file():
        errors.append("missing framework figure lineage")
    else:
        lineage = json.loads(FIGURE_LINEAGE.read_text(encoding="utf-8"))["artifact"]
        svg = ROUND / "figures" / lineage["file"]
        if not svg.is_file() or sha(svg).upper() != lineage["sha256"].upper():
            errors.append("framework SVG does not match its lineage hash")

    if not REPLAY_MANIFEST.is_file():
        errors.append("missing retrospective diagnostic manifest")
    else:
        replay = json.loads(REPLAY_MANIFEST.read_text(encoding="utf-8"))
        expected = {
            "question_count": 180,
            "questions_with_at_least_two_unique_candidates": 173,
            "questions_with_at_least_two_eligible_candidates": 172,
            "questions_with_reference_free_counterfactual_evidence": 0,
            "accuracy_claim_authorized": False,
        }
        for key, value in expected.items():
            if replay.get("summary", {}).get(key) != value:
                errors.append(f"retrospective manifest invariant mismatch: {key}")

    for path, label in (
        (OFFLINE_SUMMARY, "v3 summary"),
        (REPRO_CHECK, "v3 reproduction check"),
        (OFFLINE_AUDIT, "independent release audit"),
        (SUPERSESSION, "supersession notice"),
        (EVIDENCE, "R3 evidence tables"),
        (Q039, "Q039 trace"),
        (R3_EXECUTOR, "R3 executor"),
        (R3_TEST, "R3 executor test"),
    ):
        if not path.is_file() or path.stat().st_size == 0:
            errors.append(f"missing {label}: {path}")

    if not errors:
        offline = json.loads(OFFLINE_SUMMARY.read_text(encoding="utf-8"))
        expected_methods = {
            "fixed_order_equal_budget": (80, 180, 0),
            "validation_rank_equal_budget_no_cf": (100, 180, 0),
            "full_coordination_complete_metamorphic": (101, 180, 0),
        }
        for method, triple in expected_methods.items():
            row = offline["methods"].get(method, {})
            observed = (row.get("correct"), row.get("covered"), row.get("abstained"))
            if observed != triple:
                errors.append(f"offline summary invariant mismatch: {method}")
        if offline.get("freeze_content_sha256") != "8b34bc370451173197ad07b460908537836409d6eb49f303caf46d13d53889e6":
            errors.append("offline freeze hash mismatch")

        repro = json.loads(REPRO_CHECK.read_text(encoding="utf-8"))
        if not repro.get("all_canonical_outputs_identical"):
            errors.append("offline independent reproductions are not identical")

        notice = json.loads(SUPERSESSION.read_text(encoding="utf-8"))
        if notice["decision"].get("prospective_from_freeze") != "SUPERSEDED_AND_INVALID":
            errors.append("supersession decision does not invalidate prospective-from-freeze")
        if notice["decision"].get("permitted_evidence_class") != "deterministic no-generation descriptive re-execution over a historical candidate pool and 180 previously evaluated items":
            errors.append("unexpected permitted v3 evidence class")

        evidence = json.loads(EVIDENCE.read_text(encoding="utf-8"))
        checks = evidence.get("integrity_checks", {})
        if (checks.get("tie_item_rows"), checks.get("griddb_cells"), checks.get("multistate_cells"), checks.get("sensitivity_cells")) != (360, 8, 8, 18):
            errors.append("R3 evidence-table cardinality mismatch")
        tie_summary = evidence.get("top_tie_summary", [])
        if [row.get("questions_with_top_tie") for row in tie_summary] != [130, 130]:
            errors.append("R3 top-tie count mismatch")

        expected_hashes = {
            R3_EXECUTOR: "1474af733b044491b65266c2ebbfd52e9e180c8291fce2e725b881bfb37cd652",
            R3_TEST: "60b9d698395c5ec95699860528508675b389ec48ec9efa06d9797a43c4bc46c8",
            SUPERSESSION: "6b4255a948abaccac7a80deafb46e94297d4ffe762d82bb4e0e0a7c2550d9c98",
            EVIDENCE: "16e9156d097835fdfe4381e24c301cb71d563b19901212b545609d871c1f5d5c",
        }
        for path, expected_hash in expected_hashes.items():
            if sha(path) != expected_hash:
                errors.append(f"hash mismatch: {path.name}")

    if errors:
        for error in errors:
            print("FAIL:", error)
        print(f"R3 verification failed with {len(errors)} error(s).")
        return 1
    print(
        f"PASS: exact original title, {len(cited)} citation keys, {len(figures)} figures, "
        "12 tables, superseded v3 evidence class, complete R3 numerics, and executor lineage verified."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
