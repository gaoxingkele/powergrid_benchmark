"""Deterministic per-paper build and evidence checks used by paper_harness stages."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECTS = {
    "mintou_p1_dstar_gru_dispatch",
    "mintou_p2_hygraph_load_forecasting",
    "mintou_p3_samode_distribution_planning",
    "mintou_p4_shield_resilience_planning",
    "mintou_p5_trace_moea_feasibility_review",
    "mintou_p6_bilonsga_project_review",
}
PLACEHOLDER_RE = re.compile(r"AUTHOR INPUT REQUIRED|author-email-required|\bTODO\b|\bTBD\b", re.IGNORECASE)
FORBIDDEN_META = (
    "for editors and reviewers",
    "rather than presenting a licence table",
    "scope conditions are revisited once",
)


def run(argv: list[str], cwd: Path) -> None:
    proc = subprocess.run(argv, cwd=cwd, text=True, encoding="utf-8", errors="replace")
    if proc.returncode:
        raise SystemExit(proc.returncode)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True, choices=sorted(PROJECTS))
    parser.add_argument("--allow-human-placeholders", action="store_true")
    args = parser.parse_args(argv)

    project = ROOT / "paper_projects" / args.project
    master = project / "manuscript" / "MANUSCRIPT.md"
    if not master.exists():
        raise SystemExit(f"master manuscript not found: {master}")
    text = master.read_text(encoding="utf-8", errors="replace")
    lowered = text.lower()
    meta_hits = [phrase for phrase in FORBIDDEN_META if phrase in lowered]
    if meta_hits:
        raise SystemExit("submission-process meta-narrative remains: " + ", ".join(meta_hits))
    if not args.allow_human_placeholders and PLACEHOLDER_RE.search(text):
        raise SystemExit("human-confirmed author/funding metadata remains unresolved")

    build = ROOT / "scripts" / "mintou" / "build_official_journal_previews.py"
    run([sys.executable, str(build), "--project", args.project], ROOT)
    tex = project / "manuscript" / "journal_submission" / "paper.tex"
    pdf = tex.with_suffix(".pdf")
    if not tex.exists() or not pdf.exists() or pdf.stat().st_size < 1024:
        raise SystemExit("official TeX/PDF build artifact missing")
    if not args.allow_human_placeholders and PLACEHOLDER_RE.search(tex.read_text(encoding="utf-8", errors="replace")):
        raise SystemExit("official LaTeX still contains human-confirmed placeholders")
    print(f"OK {args.project}: {tex.relative_to(ROOT)}; PDF bytes={pdf.stat().st_size}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
