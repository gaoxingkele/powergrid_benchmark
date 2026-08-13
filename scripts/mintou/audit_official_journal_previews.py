"""Audit content preservation and compilation health of the six journal previews."""

from __future__ import annotations

import csv
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "reviews" / "mintou_2026-08-11_mean_target_revision"
PROJECTS = sorted((ROOT / "paper_projects").glob("mintou_p*"))


def count_references(markdown: str) -> int:
    parts = re.split(r"^## References\s*$", markdown, maxsplit=1, flags=re.M | re.I)
    if len(parts) != 2:
        return 0
    block = re.split(r"^##\s+", parts[1], maxsplit=1, flags=re.M)[0]
    return len(re.findall(r"^(?:\[\d+\]|\d+\.)\s+", block, flags=re.M))


def pdf_pages(path: Path) -> int:
    output = subprocess.run(["pdfinfo", str(path)], check=True, capture_output=True, text=True).stdout
    match = re.search(r"^Pages:\s+(\d+)", output, flags=re.M)
    return int(match.group(1)) if match else 0


def main() -> int:
    rows: list[dict[str, str | int]] = []
    for project in PROJECTS:
        manuscript = project / "manuscript" / "MANUSCRIPT.md"
        submission = project / "manuscript" / "journal_submission"
        tex_path = submission / "paper.tex"
        pdf_path = submission / "paper.pdf"
        log_path = submission / "paper.log"
        md = manuscript.read_text(encoding="utf-8")
        tex = tex_path.read_text(encoding="utf-8")
        log = log_path.read_text(encoding="utf-8", errors="replace")
        md_figures = len(re.findall(r"^!\[[^\]]*\]\([^)]+\)\s*$", md, flags=re.M))
        md_table_captions = len(re.findall(r"^\*\*Table\s+\d+\.\*\*", md, flags=re.M))
        md_tables = len(re.findall(r"^\|[^\n]+\|\s*\n\|(?:\s*:?-+:?\s*\|)+\s*$", md, flags=re.M))
        md_references = count_references(md)
        tex_figures = len(re.findall(r"\\begin\{figure\*?\}", tex))
        tex_tables = len(re.findall(r"\\begin\{table\*?\}", tex))
        tex_references = len(re.findall(r"\\bibitem\{", tex))
        rows.append(
            {
                "project": project.name,
                "pages": pdf_pages(pdf_path),
                "markdown_figures": md_figures,
                "latex_figures": tex_figures,
                "markdown_tables": md_tables,
                "markdown_table_captions": md_table_captions,
                "latex_tables": tex_tables,
                "markdown_references": md_references,
                "latex_bibitems": tex_references,
                "missing_glyph_warnings": len(re.findall(r"Missing character|Invalid UTF-8", log)),
                "undefined_reference_warnings": len(re.findall(r"undefined references|Citation.+undefined|Reference.+undefined", log)),
                "hard_gate_markers": len(re.findall(r"UNVERIFIED CITATION|HIGH-WARN|anchor:none|severity=HIGH-BLOCK|data-ars-component", md + "\n" + tex)),
                "content_counts_match": "yes" if (md_figures == tex_figures and md_tables == tex_tables and md_references == tex_references) else "no",
            }
        )

    OUT.mkdir(parents=True, exist_ok=True)
    target = OUT / "official_build_integrity.csv"
    with target.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    for row in rows:
        print(row)
    return 0 if all(row["content_counts_match"] == "yes" and row["hard_gate_markers"] == 0 for row in rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
