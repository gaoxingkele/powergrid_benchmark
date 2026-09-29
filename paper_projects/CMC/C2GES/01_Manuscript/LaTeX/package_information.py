"""Build hash-bound Information packages for C2GES and verify a fresh extract.

Two modes:
  (default)     review package -- includes FORMAT_CHECK, cover letter, Word copy.
  --submission  SuSy manuscript ZIP -- tex, pdf, bib, Definitions, figures only.
                Cover letter is pasted into the portal, not uploaded.

Supplementary ZIP is always built separately.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MANUSCRIPT_DIR = ROOT.parent
SUPP = MANUSCRIPT_DIR / "Supplementary"
PDF_DIR = MANUSCRIPT_DIR / "PDF"
PROJECT = MANUSCRIPT_DIR.parent

MANUSCRIPT = (
    "paper_information.tex",
    "paper_information.pdf",
    "references_cited_verified.bib",
)
INTERNAL = (
    "BUILD.md",
    "FORMAT_CHECK.md",
    "INFORMATION_COVER_LETTER.md",
    "paper_information.docx",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def add_dir(zf: zipfile.ZipFile, src: Path, arc: str, skip_suffixes=(".pyc",)) -> None:
    for path in src.rglob("*"):
        if path.is_file() and path.suffix not in skip_suffixes and "__pycache__" not in path.parts:
            zf.write(path, arc + "/" + path.relative_to(src).as_posix())


def missing_graphics(tex: Path, names: list[str]) -> list[str]:
    """Every \\includegraphics target must travel inside the archive."""
    wanted = re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", tex.read_text(encoding="utf-8"))
    shipped = {name.rsplit("/", 1)[-1] for name in names}
    return sorted({target for target in wanted if target.rsplit("/", 1)[-1] not in shipped})


def build_submission(out: Path, submission: bool) -> dict:
    if out.exists():
        out.unlink()
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for name in MANUSCRIPT:
            zf.write(ROOT / name, name)
        if not submission:
            for name in INTERNAL:
                path = ROOT / name
                if path.is_file():
                    zf.write(path, name)
        add_dir(zf, ROOT / "Definitions", "Definitions")
        add_dir(zf, ROOT / "figures", "figures")

    staging = Path(tempfile.mkdtemp(prefix="c2ges_info_"))
    try:
        with zipfile.ZipFile(out) as zf:
            zf.extractall(staging)
        required = [
            staging / "paper_information.tex",
            staging / "paper_information.pdf",
            staging / "references_cited_verified.bib",
            staging / "Definitions" / "mdpi.cls",
            staging / "figures" / "fig01_algorithm_dual_panel.pdf",
        ]
        missing = [str(p) for p in required if not p.exists()]
        if missing:
            raise FileNotFoundError(missing)
        if submission:
            leaked = [n for n in INTERNAL if (staging / n).exists()]
            if leaked:
                raise AssertionError(f"internal documents leaked into submission package: {leaked}")
        absent = missing_graphics(ROOT / "paper_information.tex", zipfile.ZipFile(out).namelist())
        if absent:
            raise AssertionError(f"figures referenced by the manuscript are absent from the package: {absent}")
        tex_disk = sha256(ROOT / "paper_information.tex")
        tex_zip = sha256(staging / "paper_information.tex")
        pdf_disk = sha256(ROOT / "paper_information.pdf")
        pdf_zip = sha256(staging / "paper_information.pdf")
        if tex_disk != tex_zip or pdf_disk != pdf_zip:
            raise AssertionError("zip tex/pdf hash does not match disk")
        return {
            "zip": str(out),
            "mode": "submission" if submission else "review",
            "zip_sha256": sha256(out),
            "tex_sha256": tex_disk,
            "pdf_sha256": pdf_disk,
            "files": len(zipfile.ZipFile(out).namelist()),
            "fresh_extract": "PASS",
        }
    finally:
        shutil.rmtree(staging, ignore_errors=True)


def build_supplementary(out: Path) -> dict:
    if out.exists():
        out.unlink()
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.write(SUPP / "supplementary_materials.tex", "supplementary_materials.tex")
        zf.write(SUPP / "supplementary_materials.pdf", "supplementary_materials.pdf")
        for fig in sorted((SUPP / "figures").glob("*.pdf")):
            zf.write(fig, "figures/" + fig.name)
    staging = Path(tempfile.mkdtemp(prefix="c2ges_supp_"))
    try:
        with zipfile.ZipFile(out) as zf:
            zf.extractall(staging)
        pdf_disk = sha256(SUPP / "supplementary_materials.pdf")
        pdf_zip = sha256(staging / "supplementary_materials.pdf")
        if pdf_disk != pdf_zip:
            raise AssertionError("supplementary PDF hash mismatch")
        absent = missing_graphics(SUPP / "supplementary_materials.tex", zipfile.ZipFile(out).namelist())
        if absent:
            raise AssertionError(f"figures referenced by the supplement are absent from the package: {absent}")
        return {
            "zip": str(out),
            "zip_sha256": sha256(out),
            "pdf_sha256": pdf_disk,
            "files": len(zipfile.ZipFile(out).namelist()),
            "fresh_extract": "PASS",
        }
    finally:
        shutil.rmtree(staging, ignore_errors=True)


def main() -> None:
    submission = "--submission" in sys.argv
    if submission:
        out = PROJECT / "C2GES_Information_20260922_submission.zip"
        report = build_submission(out, submission=True)
        manifest = ROOT / "PACKAGE_VERIFICATION_submission.json"
    else:
        out = PROJECT / "C2GES_Information_20260922_review.zip"
        report = build_submission(out, submission=False)
        manifest = ROOT / "PACKAGE_VERIFICATION.json"
    supp_out = PROJECT / "C2GES_Information_20260922_supplementary.zip"
    supp_report = build_supplementary(supp_out)
    dest_pdf = PDF_DIR / "C2GES_Information_2026-09-22_diagnostic_submission.pdf"
    shutil.copy2(ROOT / "paper_information.pdf", dest_pdf)
    dest_supp = PDF_DIR / "C2GES_Supplementary_2026-09-22_information.pdf"
    shutil.copy2(SUPP / "supplementary_materials.pdf", dest_supp)
    payload = {
        "manuscript": report,
        "supplementary": supp_report,
        "copied_pdf": str(dest_pdf),
        "copied_supp_pdf": str(dest_supp),
    }
    manifest.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
