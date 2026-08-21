#!/usr/bin/env python3
"""Audit both TeX and extracted PDF text for superseded C2GES claims."""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve()
MANUSCRIPT = HERE.parent.parent
TEX = MANUSCRIPT / "paper_applsci.tex"
PDF = MANUSCRIPT / "build/paper_applsci.pdf"

PATTERNS = {
    "legacy_split": r"(?<!\d)(?:4,?000)\s*(?:training|train).{0,80}(?:800)\s*(?:development|dev).{0,80}(?:800)\s*test",
    "legacy_metrics": r"(?<!\d)(?:0\.5066|0\.5030|0\.4967|0\.4937|0\.4837|0\.4818|0\.4414|\+0\.0099)(?!\d)",
    "unsupported_role_gain": r"(?:role conditioning improves|role head drives the gain|significant predicted.{0,20}blind)",
    "unsupported_prospective_framing": r"\b(?:confirmatory|preregistered)\b",
    "removed_holm_citation": r"holm1979simple|\\cite\{[^}]*holm",
    "oracle_upper_bound": r"oracle.{0,30}upper[- ]bound|upper[- ]bound.{0,30}oracle",
}


def scan(text: str) -> list[str]:
    return [name for name, pattern in PATTERNS.items() if re.search(pattern, text, re.I | re.S)]


def main() -> int:
    findings = [("TeX", name) for name in scan(TEX.read_text(encoding="utf-8"))]
    exe = shutil.which("pdftotext")
    if not exe:
        print("FAIL: pdftotext unavailable; PDF superseded-claim audit was not run.")
        return 1
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "paper.txt"
        subprocess.run([exe, "-layout", str(PDF), str(out)], check=True)
        findings += [("PDF", name) for name in scan(out.read_text(encoding="utf-8", errors="replace"))]
    if findings:
        for where, name in findings:
            print(f"FAIL: {where}: {name}")
        return 1
    print(f"PASS: TeX and PDF are free of {len(PATTERNS)} superseded/unsupported claim classes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
