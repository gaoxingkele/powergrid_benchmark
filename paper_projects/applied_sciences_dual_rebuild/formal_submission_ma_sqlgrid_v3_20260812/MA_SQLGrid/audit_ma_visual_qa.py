"""Render and hash the current MA-SQLGrid PDF for visual inspection.

The script discovers page and figure counts from the current artifacts. It does
not contain the superseded 20-page/four-figure constants and refuses to
overwrite an existing QA record.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parent


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def pdf_pages(pdf: Path) -> int:
    run = subprocess.run(["pdfinfo", str(pdf)], check=True, capture_output=True)
    text = run.stdout.decode("latin-1", errors="replace")
    match = re.search(r"^Pages:\s+(\d+)", text, flags=re.MULTILINE)
    if not match:
        raise RuntimeError(f"Cannot determine page count: {pdf}")
    return int(match.group(1))


def figure_paths(tex: Path) -> list[str]:
    text = tex.read_text(encoding="utf-8")
    figures = re.findall(r"\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}", text)
    return [item for item in figures if not item.startswith("Definitions/")]


def make_sheets(pages: list[Path], output: Path) -> list[Path]:
    sheets: list[Path] = []
    for start in range(0, len(pages), 4):
        group = pages[start : start + 4]
        canvas = Image.new("RGB", (1940, 2740), "white")
        draw = ImageDraw.Draw(canvas)
        for index, page in enumerate(group):
            with Image.open(page) as opened:
                opened.thumbnail((950, 1320))
                page_image = opened.convert("RGB")
            x = 10 + (index % 2) * 960
            y = 30 + (index // 2) * 1350
            draw.text((x, y), page.stem, fill="black")
            canvas.paste(page_image, (x, y + 20))
        path = output / f"contact_{start + 1:02d}_{start + len(group):02d}.png"
        canvas.save(path, dpi=(144, 144))
        sheets.append(path)
    return sheets


def main() -> None:
    pdf = ROOT / "paper_applsci.pdf"
    tex = ROOT / "paper_applsci.tex"
    qa = ROOT / "visual_qa"
    manifest_path = ROOT / "VISUAL_QA_MANIFEST.json"
    report_path = ROOT / "VISUAL_QA_REPORT.md"
    for target in (qa, manifest_path, report_path):
        if target.exists():
            raise FileExistsError(f"Refusing to overwrite existing QA artifact: {target}")
    pages_dir = qa / "pages"
    sheets_dir = qa / "contact_sheets"
    pages_dir.mkdir(parents=True)
    sheets_dir.mkdir(parents=True)
    subprocess.run(
        ["pdftoppm", "-png", "-r", "144", str(pdf), str(pages_dir / "page")],
        check=True,
    )
    page_files = sorted(pages_dir.glob("page-*.png"))
    expected_pages = pdf_pages(pdf)
    if len(page_files) != expected_pages:
        raise RuntimeError(f"Rendered {len(page_files)} pages, expected {expected_pages}")
    figures = figure_paths(tex)
    missing = [value for value in figures if not (ROOT / value).exists()]
    if missing:
        raise FileNotFoundError(f"Missing manuscript figures: {missing}")
    sheets = make_sheets(page_files, sheets_dir)
    manifest = {
        "schema_version": "ma-narrative-revision-visual-qa-v1",
        "status": "RENDERED_PENDING_VISUAL_INSPECTION",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "tex": {"path": tex.name, "sha256": sha256(tex), "bytes": tex.stat().st_size},
        "pdf": {
            "path": pdf.name,
            "sha256": sha256(pdf),
            "bytes": pdf.stat().st_size,
            "pages": expected_pages,
        },
        "manuscript_figures": [
            {"path": value, "sha256": sha256(ROOT / value), "bytes": (ROOT / value).stat().st_size}
            for value in figures
        ],
        "rendered_pages": [
            {"page": index, "path": page.relative_to(ROOT).as_posix(), "sha256": sha256(page)}
            for index, page in enumerate(page_files, 1)
        ],
        "contact_sheets": [
            {"path": sheet.relative_to(ROOT).as_posix(), "sha256": sha256(sheet)}
            for sheet in sheets
        ],
        "inspection": None,
    }
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    report_path.write_text(
        "# Visual QA Report - MA-SQLGrid Narrative Revision\n\n"
        "**Status: RENDERED_PENDING_VISUAL_INSPECTION**\n\n"
        f"- Pages discovered from current PDF: {expected_pages}\n"
        f"- Figures discovered from current TeX: {len(figures)}\n"
        f"- PDF SHA-256: `{manifest['pdf']['sha256']}`\n\n"
        "All pages have been rendered and contact sheets created. A visual reviewer must inspect them before status may be changed to PASS.\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
