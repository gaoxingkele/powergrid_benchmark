"""Package and render the exact Stage-6 journal PDF/TeX bytes.

Run only after the mandated default-PATH three-pass LaTeX build succeeds and
the journal PDF has the expected raw SHA-256. This generator does not compile
TeX and does not modify the journal submission directory.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from PIL import Image
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
JOURNAL = ROOT / "manuscript" / "journal_submission"
RELEASE = ROOT / "manuscript" / "release_package"
RENDERS = RELEASE / "rendered_pages"
EXPECTED_PDF_SHA256 = "bb61e0b1b20a3e9192bc05c640eb8c8895b0b0c24d8f2255c56fd4c4ff983c5c"
EXPECTED_PAGES = 9
SOURCE_DATE_EPOCH = "1787867025"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"STAGE6 RELEASE GENERATION FAILED: {message}")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def file_record(path: Path, relative_to: Path) -> dict[str, Any]:
    return {
        "path": path.relative_to(relative_to).as_posix(),
        "sha256": sha256(path),
        "bytes": path.stat().st_size,
    }


def main() -> int:
    journal_pdf = JOURNAL / "paper.pdf"
    journal_tex = JOURNAL / "paper.tex"
    require(journal_pdf.is_file(), "journal paper.pdf is missing")
    require(journal_tex.is_file(), "journal paper.tex is missing")
    require(sha256(journal_pdf) == EXPECTED_PDF_SHA256, "journal PDF is not the frozen default-PATH build")
    require(len(PdfReader(str(journal_pdf)).pages) == EXPECTED_PAGES, "journal PDF is not nine pages")

    RELEASE.mkdir(parents=True, exist_ok=True)
    RENDERS.mkdir(parents=True, exist_ok=True)
    package_pdf = RELEASE / "paper.pdf"
    package_tex = RELEASE / "paper.tex"
    shutil.copyfile(journal_pdf, package_pdf)
    shutil.copyfile(journal_tex, package_tex)
    require(package_pdf.read_bytes() == journal_pdf.read_bytes(), "packaged PDF copy is not byte exact")
    require(package_tex.read_bytes() == journal_tex.read_bytes(), "packaged TeX copy is not byte exact")

    with tempfile.TemporaryDirectory(prefix="p1_stage6_pdf_render_") as temporary:
        prefix = Path(temporary) / "page"
        completed = subprocess.run(
            ["pdftoppm", "-png", "-r", "150", str(package_pdf), str(prefix)],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        require(completed.returncode == 0, f"pdftoppm failed: {completed.stderr.strip()}")
        rendered = sorted(Path(temporary).glob("page-*.png"))
        require(len(rendered) == EXPECTED_PAGES, f"rendered page count is {len(rendered)}, expected nine")
        page_records: list[dict[str, Any]] = []
        for page_number, source in enumerate(rendered, start=1):
            destination = RENDERS / f"page-{page_number:02d}.png"
            shutil.copyfile(source, destination)
            with Image.open(destination) as image:
                width, height = image.size
            page_records.append(
                {
                    "page": page_number,
                    "file": destination.relative_to(RELEASE).as_posix(),
                    "sha256": sha256(destination),
                    "bytes": destination.stat().st_size,
                    "width_px": width,
                    "height_px": height,
                    "visual_inspection": {
                        "status": "pending",
                        "inspected_by": None,
                        "checks": {
                            "no_clipping": None,
                            "no_overlap": None,
                            "tables_figures_legible": None,
                            "fonts_glyphs_rendered": None,
                            "headers_footers_page_numbering_consistent": None,
                        },
                        "notes": "Manual visual inspection required before terminal validation.",
                    },
                }
            )

    pdf_record = file_record(package_pdf, RELEASE)
    tex_record = file_record(package_tex, RELEASE)
    package_manifest = {
        "schema": "p1_stage6_release_package_manifest",
        "schema_version": 1,
        "stage": "s6_attempt_5_of_5",
        "build_contract": {
            "working_directory": "manuscript/journal_submission",
            "executable": "inherited default-PATH pdflatex",
            "command": ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "paper.tex"],
            "passes": 3,
            "bibliography_step_required": False,
            "environment": {
                "SOURCE_DATE_EPOCH": SOURCE_DATE_EPOCH,
                "FORCE_SOURCE_DATE": "1",
                "TZ": "UTC",
            },
            "custom_or_local_miktex_or_texmf_runtime": False,
            "miktex_or_texmf_override": False,
            "alternate_pdflatex_binary": False,
            "output_directory": False,
            "container": False,
        },
        "paper_pdf": {**pdf_record, "page_count": EXPECTED_PAGES},
        "paper_tex": tex_record,
        "package_scope": [
            "paper.pdf",
            "paper.tex",
            "PACKAGE_MANIFEST.json",
            "PDF_RENDER_QA.json",
            "rendered_pages/page-01.png through rendered_pages/page-09.png",
        ],
        "scientific_claim_change": False,
        "stage7_human_placeholders_retained": True,
    }
    (RELEASE / "PACKAGE_MANIFEST.json").write_text(
        json.dumps(package_manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    render_qa = {
        "schema": "p1_stage6_pdf_render_qa",
        "schema_version": 1,
        "source_pdf": {
            "path": "../journal_submission/paper.pdf",
            "sha256": sha256(journal_pdf),
            "bytes": journal_pdf.stat().st_size,
        },
        "packaged_pdf": {**pdf_record, "page_count": EXPECTED_PAGES},
        "render": {
            "tool": "inherited default-PATH pdftoppm",
            "format": "PNG",
            "dpi": 150,
            "page_count": EXPECTED_PAGES,
            "pages": page_records,
        },
        "visual_inspection_complete": False,
        "complete_page_records": 0,
        "expected_page_records": EXPECTED_PAGES,
        "scientific_claim_change": False,
    }
    (RELEASE / "PDF_RENDER_QA.json").write_text(
        json.dumps(render_qa, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(
        "OK Stage 6 release bytes copied and nine pages rendered; "
        "manual visual inspection remains pending in PDF_RENDER_QA.json"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
