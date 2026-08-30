#!/usr/bin/env python3
"""Shared, fail-closed primitives for the P1 Stage-7 release finalizer."""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
JOURNAL = ROOT / "manuscript" / "journal_submission"
MARKDOWN_PATH = ROOT / "manuscript" / "MANUSCRIPT.md"
METADATA_PATH = ROOT / "manuscript" / "STAGE7_HUMAN_METADATA.json"
BUILD_IDENTITY_PATH = ROOT / "manuscript" / "STAGE7_BUILD_IDENTITY.json"
PACKAGE_ROOT = ROOT / "release_package_stage7"
PACKAGE = PACKAGE_ROOT / "manuscript"
PACKAGE_MANIFEST_PATH = PACKAGE_ROOT / "PACKAGE_MANIFEST.json"
QA_PATH = ROOT / "manuscript" / "STAGE7_PDF_RENDER_QA.json"
RENDER_DIR = ROOT / "manuscript" / "stage7_rendered_pages"
METADATA_VALIDATOR = ROOT / "scripts" / "validate_p1_stage7_human_metadata.py"

SOURCE_DATE_EPOCH = "1787867025"
EXPECTED_ENVIRONMENT = {
    "SOURCE_DATE_EPOCH": SOURCE_DATE_EPOCH,
    "FORCE_SOURCE_DATE": "1",
    "TZ": "UTC",
}
BUILD_COMMAND = ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "paper.tex"]
MAX_SUBMISSION_FILE_BYTES = 40_000_000

SAMPLE_PHOTO_SHA256 = {
    "198616cf28c75497af183f8e9dc374f28d26537a4a8dc3ace9a5eee44a0d193c",
    "b673e3d89c4021b5984f91983d3b1cd989348bbc50b3581e7eca2ee7d7352a53",
    "df03222e551646eb458e8b8808cc613efa049b387bc2c6b4adba5dc59963bd05",
}
PLACEHOLDER_PATTERNS = (
    re.compile(r"AUTHOR\s+INPUT\s+REQUIRED", re.IGNORECASE),
    re.compile(r"\bT[B]D\b", re.IGNORECASE),
    re.compile(r"\bTO[D]O\b", re.IGNORECASE),
    re.compile(r"\bX{4,}\b", re.IGNORECASE),
    re.compile(r"Author\s+Details\s+Required\s+before\s+Submission", re.IGNORECASE),
    re.compile(
        r"must\s+be\s+confirmed\s+by\s+the\s+authors\s+before\s+submission",
        re.IGNORECASE,
    ),
)
FORBIDDEN_SUFFIXES = {
    ".aux",
    ".log",
    ".out",
    ".toc",
    ".bbl",
    ".blg",
    ".fls",
    ".fdb_latexmk",
    ".synctex",
    ".synctex.gz",
}
FORBIDDEN_PARTS = {
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".cache",
}
RUNTIME_FILENAMES = {
    "pdflatex.exe",
    "pdftex.exe",
    "miktex.exe",
    "miktex-pdflatex.exe",
    "initexmf.exe",
    "mpm.exe",
    "mpm_mfc.exe",
    "miktexsetup.exe",
}


class ValidationError(RuntimeError):
    """Raised when a Stage-7 release invariant is not proved."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def display(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def sha256(path: Path) -> str:
    require(path.is_file(), f"required file is missing: {display(path)}")
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_text_sha256(path: Path) -> str:
    require(path.is_file(), f"required text file is missing: {display(path)}")
    data = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(data).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    require(path.is_file(), f"required JSON is missing: {display(path)}")
    try:
        value = json.loads(path.read_text(encoding="utf-8", errors="strict"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValidationError(f"cannot parse {display(path)}: {exc}") from exc
    require(isinstance(value, dict), f"JSON root must be an object: {display(path)}")
    return value


def atomic_write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temporary = Path(handle.name)
            json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
            handle.write("\n")
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def require_environment() -> None:
    actual = {key: os.environ.get(key) for key in EXPECTED_ENVIRONMENT}
    require(
        actual == EXPECTED_ENVIRONMENT,
        f"deterministic build environment mismatch: expected {EXPECTED_ENVIRONMENT}, observed {actual}",
    )


def tool_version(executable: str, version_args: list[str] | None = None) -> tuple[str, str]:
    resolved = shutil.which(executable)
    require(resolved is not None, f"required executable is unavailable on PATH: {executable}")
    completed = subprocess.run(
        [resolved, *(version_args or ["--version"])],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    require(completed.returncode == 0, f"cannot query {executable} version")
    first_line = next((line.strip() for line in completed.stdout.splitlines() if line.strip()), "")
    require(bool(first_line), f"{executable} version output is empty")
    return str(Path(resolved).resolve()), first_line


def page_count(pdf: Path) -> int:
    completed = subprocess.run(
        ["pdfinfo", str(pdf)],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    require(completed.returncode == 0, f"pdfinfo failed for {display(pdf)}: {completed.stdout.strip()}")
    match = re.search(r"^Pages:\s+(\d+)\s*$", completed.stdout, flags=re.MULTILINE)
    require(match is not None, f"pdfinfo did not report pages for {display(pdf)}")
    return int(match.group(1))


def semantic_text(pdf: Path) -> bytes:
    completed = subprocess.run(
        ["pdftotext", "-enc", "UTF-8", str(pdf), "-"],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    require(completed.returncode == 0, f"pdftotext failed for {display(pdf)}")
    text = completed.stdout.decode("utf-8", errors="strict").replace("\r\n", "\n").replace("\r", "\n")
    normalized = "\n".join(line.rstrip() for line in text.splitlines()).strip() + "\n"
    return normalized.encode("utf-8")


def semantic_sha256(pdf: Path) -> str:
    return hashlib.sha256(semantic_text(pdf)).hexdigest()


def placeholder_findings(text: str) -> list[str]:
    return [pattern.pattern for pattern in PLACEHOLDER_PATTERNS if pattern.search(text)]


def require_no_placeholders(path: Path, *, pdf: bool = False) -> None:
    if pdf:
        text = semantic_text(path).decode("utf-8", errors="strict")
    else:
        require(path.is_file(), f"required manuscript file is missing: {display(path)}")
        text = path.read_text(encoding="utf-8", errors="strict")
    findings = placeholder_findings(text)
    require(not findings, f"human placeholders remain in {display(path)}: {findings}")


def run_metadata_gate(phase: str) -> None:
    require(phase in {"prebuild", "release"}, f"unknown metadata phase: {phase}")
    completed = subprocess.run(
        [sys.executable, "-B", str(METADATA_VALIDATOR), "--phase", phase],
        cwd=ROOT,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    require(
        completed.returncode == 0,
        f"Stage-7 {phase} metadata gate blocked:\n{completed.stdout.rstrip()}",
    )


def is_reparse(path: Path) -> bool:
    return path.is_symlink() or bool(getattr(path, "is_junction", lambda: False)())


def require_safe_tree(root: Path) -> None:
    require(root.exists(), f"required tree is missing: {display(root)}")
    require(not is_reparse(root), f"reparse-point tree root is forbidden: {display(root)}")
    for path in root.rglob("*"):
        require(not is_reparse(path), f"reparse point is forbidden: {display(path)}")


def forbidden_path_reason(relative: str) -> str | None:
    normalized = relative.replace("\\", "/")
    lowered = normalized.lower()
    parts = [part for part in lowered.split("/") if part]
    if any(part.startswith(".miktex") for part in parts):
        return "local MiKTeX path"
    if set(parts) & FORBIDDEN_PARTS:
        return "cache path"
    if any(lowered.endswith(suffix) for suffix in FORBIDDEN_SUFFIXES):
        return "TeX auxiliary/log file"
    if parts and parts[-1] in RUNTIME_FILENAMES:
        return "packaged TeX runtime executable"
    if set(parts) & {"texmf", "texmf-local", "texmflocal", "miktex-portable"}:
        return "packaged TeX runtime tree"
    return None


def render_pngs(pdf: Path, output: Path, *, dpi: int = 144) -> list[Path]:
    require(not output.exists(), f"render output already exists: {output}")
    output.mkdir(parents=True)
    completed = subprocess.run(
        ["pdftoppm", "-r", str(dpi), "-png", str(pdf), str(output / "page")],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    require(completed.returncode == 0, f"pdftoppm failed: {completed.stderr.strip()}")
    pages = sorted(output.glob("page-*.png"), key=lambda item: int(item.stem.split("-")[-1]))
    require(len(pages) == page_count(pdf), "rendered page count differs from PDF page count")
    return pages


def validate_build_identity() -> dict[str, Any]:
    identity = load_json(BUILD_IDENTITY_PATH)
    require(identity.get("schema") == "p1_stage7_build_identity", "Stage-7 build identity schema changed")
    require(identity.get("schema_version") == 1, "Stage-7 build identity version changed")
    require(identity.get("environment") == EXPECTED_ENVIRONMENT, "Stage-7 build environment changed")
    require(identity.get("build_command") == BUILD_COMMAND, "Stage-7 build command changed")
    require(identity.get("build_passes") == 3, "Stage-7 build must record three passes")
    pass_hashes = identity.get("compile_pdf_sha256")
    require(
        isinstance(pass_hashes, list)
        and len(pass_hashes) == 3
        and all(isinstance(value, str) and re.fullmatch(r"[0-9a-f]{64}", value) for value in pass_hashes)
        and len(set(pass_hashes)) == 1,
        "three Stage-7 compile hashes are not byte-identical",
    )
    require(
        isinstance(identity.get("pdflatex_executable"), str) and bool(identity["pdflatex_executable"].strip()),
        "Stage-7 pdflatex executable record is missing",
    )
    require(
        isinstance(identity.get("pdflatex_version"), str) and bool(identity["pdflatex_version"].strip()),
        "Stage-7 pdflatex version record is missing",
    )
    require(identity.get("unresolved_latex_diagnostics") == [], "Stage-7 LaTeX diagnostics are unresolved")
    require(identity.get("human_placeholders_retained") is False, "Stage-7 build identity retains placeholders")
    journal_pdf = JOURNAL / "paper.pdf"
    journal_tex = JOURNAL / "paper.tex"
    require(identity.get("pdf_sha256") == sha256(journal_pdf), "Stage-7 build identity PDF hash is stale")
    require(pass_hashes[0] == identity.get("pdf_sha256"), "compile hashes differ from current PDF")
    require(identity.get("pdf_bytes") == journal_pdf.stat().st_size, "Stage-7 PDF byte count is stale")
    require(journal_pdf.stat().st_size < MAX_SUBMISSION_FILE_BYTES, "Stage-7 PDF reaches the 40 MB submission limit")
    require(journal_tex.stat().st_size < MAX_SUBMISSION_FILE_BYTES, "Stage-7 TeX reaches the 40 MB submission limit")
    require(identity.get("page_count") == page_count(journal_pdf), "Stage-7 page count is stale")
    require(0 < int(identity.get("page_count", 0)) < 20, "Stage-7 paper must contain 1-19 pages")
    require(identity.get("semantic_text_sha256") == semantic_sha256(journal_pdf), "Stage-7 semantic PDF hash is stale")
    require(identity.get("tex_sha256") == sha256(journal_tex), "Stage-7 raw TeX hash is stale")
    require(
        identity.get("tex_canonical_sha256") == canonical_text_sha256(journal_tex),
        "Stage-7 canonical TeX hash is stale",
    )
    require(identity.get("metadata_sha256") == sha256(METADATA_PATH), "Stage-7 metadata hash is stale")
    require(identity.get("markdown_sha256") == sha256(MARKDOWN_PATH), "Stage-7 Markdown hash is stale")
    require_no_placeholders(journal_tex)
    require_no_placeholders(MARKDOWN_PATH)
    require_no_placeholders(journal_pdf, pdf=True)
    return identity


def publish_directory(staging: Path, target: Path) -> Path | None:
    """Publish a complete staging tree; preserve any prior target as a backup."""

    require(staging.is_dir(), f"staging directory is missing: {staging}")
    resolved_root = ROOT.resolve()
    require(staging.resolve().parent == resolved_root, "staging directory must be a direct child of project root")
    require(target.resolve().parent == resolved_root, "publish target must be a direct child of project root")
    require_safe_tree(staging)
    backup: Path | None = None
    if target.exists():
        require_safe_tree(target)
        marker = sha256(target / "PACKAGE_MANIFEST.json")[:12] if (target / "PACKAGE_MANIFEST.json").is_file() else "unmanifested"
        backup = target.with_name(f"{target.name}.previous-{marker}")
        require(not backup.exists(), f"recoverable backup already exists; inspect it before replacing: {backup}")
        target.rename(backup)
    try:
        staging.rename(target)
    except Exception:
        if backup is not None and backup.exists() and not target.exists():
            backup.rename(target)
        raise
    return backup


def main_error(prefix: str, callable_main: Any) -> int:
    try:
        return int(callable_main())
    except ValidationError as exc:
        print(f"{prefix}: {exc}", file=sys.stderr)
        return 1
