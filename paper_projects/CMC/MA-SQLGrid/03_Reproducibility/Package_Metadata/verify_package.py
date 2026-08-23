#!/usr/bin/env python3
"""Portable, read-only verification for the MA-SQLGrid 3.0 email package."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def jsonl_count(path: Path) -> int:
    with path.open(encoding="utf-8") as handle:
        return sum(1 for line in handle if line.strip())


def require(relative: str) -> Path:
    path = ROOT / relative
    if not path.is_file():
        raise AssertionError(f"missing required file: {relative}")
    return path


def verify_hashes() -> int:
    manifest = require("FILE_SHA256SUMS.txt")
    checked = 0
    for line in manifest.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        expected, relative = line.lstrip("\ufeff").split("  ", 1)
        path = require(relative)
        actual = sha256(path)
        if actual != expected:
            raise AssertionError(f"hash mismatch: {relative}")
        checked += 1
    return checked


def verify_manuscript() -> dict[str, int]:
    tex = require("02_LaTeX/paper_applsci.tex").read_text(encoding="utf-8")
    require("01_PDF/MA_SQLGrid_v3.0_Applied_Sciences.pdf")
    assert "80/180" in tex and "100/180" in tex and "101/180" in tex
    assert "email to be provided by the corresponding author" in tex
    figures = re.findall(r"\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}", tex)
    for figure in figures:
        require("02_LaTeX/" + figure)
    tables = len(re.findall(r"\\begin\{table\}", tex))
    return {"figures": len(figures), "tables": tables}


def verify_data() -> dict[str, int]:
    canonical_n = jsonl_count(require("05_Data/canonical_v2/canonical_rows_v2.jsonl"))
    atomic_n = jsonl_count(require("05_Data/constructed_state/atomic_scores.jsonl"))
    evaluation_n = jsonl_count(require("05_Data/historical_pool/run_v3a/evaluation_ledger.jsonl"))
    summary = json.loads(require("05_Data/historical_pool/run_v3a/summary.json").read_text(encoding="utf-8"))
    methods = summary["methods"]
    assert canonical_n == 1440
    assert atomic_n == 25920
    assert evaluation_n == 540
    assert methods["fixed_order_equal_budget"]["correct"] == 80
    assert methods["validation_rank_equal_budget_no_cf"]["correct"] == 100
    assert methods["full_coordination_complete_metamorphic"]["correct"] == 101
    with require("05_Data/BIRD_aggregates/method_summary.csv").open(encoding="utf-8", newline="") as handle:
        bird = list(csv.DictReader(handle))
    assert len(bird) == 8 and all(int(row["n"]) == 500 for row in bird)
    forbidden = list(ROOT.rglob("database.sqlite")) + list(ROOT.rglob("questions.jsonl"))
    if forbidden:
        raise AssertionError("raw restricted dataset unexpectedly included")
    return {
        "canonical_rows": canonical_n,
        "constructed_state_atomic_rows": atomic_n,
        "historical_pool_evaluation_rows": evaluation_n,
        "bird_method_cells": len(bird),
    }


def run_unit_tests() -> dict[str, str]:
    suites = {
        "framework": [
            sys.executable,
            "-m",
            "unittest",
            "tests/test_ma_sqlgrid_agents.py",
            "tests/test_sqlite_readonly_executor.py",
            "tests/test_replay_diagnostic.py",
        ],
        "final_executor": [sys.executable, "-m", "unittest", "test_sqlite_readonly_executor_final.py"],
    }
    outcomes: dict[str, str] = {}
    for name, command in suites.items():
        cwd = ROOT / "04_Code" / name
        result = subprocess.run(command, cwd=cwd, capture_output=True, text=True)
        if result.returncode:
            raise AssertionError(f"{name} unit tests failed:\n{result.stdout}\n{result.stderr}")
        outcomes[name] = "PASS"
    return outcomes


def main() -> int:
    result = {
        "schema_version": "ma-sqlgrid-portable-package-check-v1",
        "hash_files_checked": verify_hashes(),
        "manuscript": verify_manuscript(),
        "data": verify_data(),
        "unit_tests": run_unit_tests(),
        "status": "PASS",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
