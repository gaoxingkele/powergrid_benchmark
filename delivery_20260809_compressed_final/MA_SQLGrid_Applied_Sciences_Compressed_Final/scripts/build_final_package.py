"""Build the explicit-allowlist MA-SQLGrid FINAL editor/reviewer package."""

from __future__ import annotations

import hashlib
import json
import shutil
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = "MA_SQLGrid_ORIGINAL_TITLE_FINAL"

EXACT_FILES = {
    "paper_applsci.tex",
    "references_verified.bib",
    "build.ps1",
    "build/paper_applsci.pdf",
    "FINAL_RESPONSE_MATRIX.md",
    "FINAL_EXECUTOR_TEST_REPORT.md",
    "INDEPENDENT_EXECUTOR_AUDIT.md",
    "RIGHTS_INVENTORY.csv",
    "PACKAGE_README.md",
    "CLEAN_EXTRACTION_AUDIT.json",
    "STRUCTURAL_VERIFICATION.json",
    "FINAL_ASSEMBLY_AUDIT.json",
    "VISUAL_QA_MANIFEST.json",
    "VISUAL_QA_REPORT.md",
    "ROUND_AUDIT.json",
}

ALLOWED_TREES = {
    "Definitions",
    "code",
    "evidence",
    "figures",
    "reviews_round3",
    "scripts",
    "tests",
}

PROHIBITED_PATH_TOKENS = {
    ".env",
    "__pycache__",
    ".pytest_cache",
    "visual_qa_final",
    "visual_qa_final_v2",
    "build_final_console.log",
    "r2_to_r3_response_matrix",
    "old_title",
    "old-title",
    "accident",
}

PROHIBITED_SUFFIXES = {".zip", ".7z", ".rar", ".pyc", ".pyo", ".log", ".aux", ".blg", ".bbl", ".out"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def rights_class(relative: Path) -> str:
    top = relative.parts[0]
    if top == "Definitions":
        return "third_party_mdpi_template_distribution_check_required"
    if top == "reviews_round3":
        return "internal_review_material"
    if top in {"evidence", "figures"}:
        return "author_derived_research_evidence"
    if top in {"code", "tests", "scripts"} or relative.name == "build.ps1":
        return "author_project_code"
    if relative.name == "references_verified.bib":
        return "bibliographic_metadata"
    return "author_manuscript_and_governance_record"


def collect() -> list[Path]:
    files: list[Path] = []
    for relative_text in sorted(EXACT_FILES):
        path = ROOT / relative_text
        if not path.is_file():
            raise FileNotFoundError(path)
        files.append(path)
    for tree_name in sorted(ALLOWED_TREES):
        tree = ROOT / tree_name
        if not tree.is_dir():
            raise FileNotFoundError(tree)
        files.extend(path for path in sorted(tree.rglob("*")) if path.is_file())

    accepted: list[Path] = []
    for path in files:
        relative = path.relative_to(ROOT)
        normalized = relative.as_posix().lower()
        if any(token in normalized for token in PROHIBITED_PATH_TOKENS):
            continue
        if path.suffix.lower() in PROHIBITED_SUFFIXES:
            continue
        accepted.append(path)
    if len(accepted) != len(set(accepted)):
        raise RuntimeError("duplicate allowlist member")
    return sorted(accepted, key=lambda item: item.relative_to(ROOT).as_posix())


def main() -> None:
    output_dir = ROOT.parents[2] / "deliverables"
    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / "MA_SQLGrid_ORIGINAL_TITLE_FINAL_2026-08-08.zip"
    if output.exists():
        raise FileExistsError(f"refusing to overwrite existing package: {output}")

    files = collect()
    with tempfile.TemporaryDirectory(prefix="ma_sqlgrid_final_package_") as temp_name:
        stage = Path(temp_name) / PACKAGE_ROOT
        stage.mkdir()
        rows: list[dict[str, object]] = []
        for source in files:
            relative = source.relative_to(ROOT)
            target = stage / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
            rows.append(
                {
                    "path": relative.as_posix(),
                    "bytes": target.stat().st_size,
                    "sha256": sha256(target),
                    "rights_class": rights_class(relative),
                }
            )
        manifest = {
            "schema": "ma-sqlgrid-final-package-manifest-v1",
            "package_root": PACKAGE_ROOT,
            "status": "ALLOWLISTED",
            "member_count_excluding_manifest": len(rows),
            "manifest_self_hash": "intentionally omitted to avoid recursive identity",
            "members": rows,
        }
        manifest_path = stage / "PACKAGE_MANIFEST.json"
        manifest_path.write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )

        constant_time = (2026, 8, 8, 12, 0, 0)
        with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for path in sorted(stage.rglob("*")):
                if not path.is_file():
                    continue
                arcname = f"{PACKAGE_ROOT}/{path.relative_to(stage).as_posix()}"
                info = zipfile.ZipInfo(arcname, constant_time)
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                archive.writestr(info, path.read_bytes(), compresslevel=9)

    print(
        json.dumps(
            {
                "status": "PASS",
                "output": str(output),
                "bytes": output.stat().st_size,
                "sha256": sha256(output),
                "members_including_manifest": len(files) + 1,
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
