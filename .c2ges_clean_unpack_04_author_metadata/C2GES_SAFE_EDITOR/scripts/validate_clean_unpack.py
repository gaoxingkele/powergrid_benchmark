"""Extract the safe-editor ZIP into a fresh directory and reproduce its checks."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
ZIP_PATH = ROOT / "packages" / "C2GES_Applied_Sciences_SAFE_EDITOR_DRY_RUN.zip"
WORKSPACE = next(parent for parent in ROOT.parents if parent.name == "powergrid_benchmark")
# Keep the extraction root short enough for Windows tools that still observe
# legacy path-length limits.  It remains inside the declared workspace.
TARGET = WORKSPACE / ".c2ges_clean_unpack_04_author_metadata"
PREFIX = "C2GES_SAFE_EDITOR"
OUT = ROOT / "CLEAN_UNPACK_RECEIPT.json"


def digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()


def digest(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def run(command: list[str], cwd: Path, env: dict[str, str]) -> dict:
    process = subprocess.run(command, cwd=cwd, env=env, text=True, capture_output=True, timeout=180)
    return {
        "command": command,
        "returncode": process.returncode,
        "stdout_sha256": digest_bytes(process.stdout.encode("utf-8")),
        "stderr_sha256": digest_bytes(process.stderr.encode("utf-8")),
        "stdout_tail": process.stdout[-1200:],
        "stderr_tail": process.stderr[-1200:],
    }


def main() -> None:
    if TARGET.exists():
        raise SystemExit(f"refused: clean target already exists: {TARGET}")
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    failures = []
    with zipfile.ZipFile(ZIP_PATH) as archive:
        for member in archive.infolist():
            destination = (TARGET / member.filename).resolve()
            try:
                destination.relative_to(TARGET.resolve())
            except ValueError:
                raise SystemExit(f"zip traversal refused: {member.filename}")
        archive.extractall(TARGET)

    package = TARGET / PREFIX
    manifest_path = package / "PACKAGE_CONTENT_MANIFEST.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    recorded = {item["path"]: item for item in manifest["files"]}
    actual_before = {
        path.relative_to(package).as_posix(): path
        for path in package.rglob("*")
        if path.is_file() and path != manifest_path
    }
    if set(recorded) != set(actual_before):
        failures.append({"initial_exact_set_mismatch": {"missing": sorted(set(recorded) - set(actual_before)), "extra": sorted(set(actual_before) - set(recorded))}})
    for rel in sorted(set(recorded) & set(actual_before)):
        item = recorded[rel]
        path = actual_before[rel]
        if path.stat().st_size != item["bytes"] or digest(path) != item["sha256"]:
            failures.append({"initial_content_mismatch": rel})

    original_figures = {
        rel: item["sha256"]
        for rel, item in recorded.items()
        if rel.startswith("figures/") and (rel.endswith(".pdf") or rel.endswith(".png") or rel.endswith("FIGURE_LINEAGE.json"))
    }
    original_pdf_hash = recorded["build_r3/paper_applsci.pdf"]["sha256"]
    original_pdf_bytes = (package / "build_r3" / "paper_applsci.pdf").read_bytes()
    original_pdf_copy = TARGET / "original_packaged_paper_applsci.pdf"
    original_pdf_copy.write_bytes(original_pdf_bytes)
    original_citation_hash = recorded["FINAL_CITATION_CONTEXT_AUDIT.json"]["sha256"]
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    commands = [
        [sys.executable, "-m", "unittest", "-v", "test_dev_only_calibration.py"],
        [sys.executable, "verify_calibration.py"],
    ]
    command_results = [
        run(command, package / "supplementary" / "transferable" / "development_calibration", env)
        for command in commands
    ]
    command_results.append(run([sys.executable, "scripts/generate_figures.py"], package, env))
    command_results.append(run([sys.executable, "scripts/build_item_level_citation_audit.py"], package, env))
    command_results.append(
        run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", "build_original_title.ps1"],
            package,
            env,
        )
    )
    for result in command_results:
        if result["returncode"] != 0:
            failures.append({"command_failed": result["command"], "returncode": result["returncode"]})

    for rel, expected in original_figures.items():
        if digest(package / rel) != expected:
            failures.append({"regenerated_figure_hash_mismatch": rel, "expected": expected, "observed": digest(package / rel)})
    if digest(package / "FINAL_CITATION_CONTEXT_AUDIT.json") != original_citation_hash:
        failures.append({"regenerated_citation_audit_hash_mismatch": True})
    rebuilt_pdf = package / "build_r3" / "paper_applsci.pdf"
    raw_pdf_hash_reproduced = digest(rebuilt_pdf) == original_pdf_hash
    pdf_compare = TARGET / "pdf_compare"
    pdf_compare.mkdir()
    original_text = subprocess.run(["pdftotext", "-layout", str(original_pdf_copy), "-"], capture_output=True, timeout=60).stdout
    rebuilt_text = subprocess.run(["pdftotext", "-layout", str(rebuilt_pdf), "-"], capture_output=True, timeout=60).stdout
    text_equal = original_text == rebuilt_text and bool(original_text)
    original_render = subprocess.run(["pdftoppm", "-png", "-r", "100", str(original_pdf_copy), str(pdf_compare / "original")], capture_output=True, timeout=120)
    rebuilt_render = subprocess.run(["pdftoppm", "-png", "-r", "100", str(rebuilt_pdf), str(pdf_compare / "rebuilt")], capture_output=True, timeout=120)
    original_pages = sorted(pdf_compare.glob("original-*.png"))
    rebuilt_pages = sorted(pdf_compare.glob("rebuilt-*.png"))
    pixel_equal = (
        original_render.returncode == 0
        and rebuilt_render.returncode == 0
        and len(original_pages) == len(rebuilt_pages)
        and len(original_pages) > 0
        and [digest(path) for path in original_pages] == [digest(path) for path in rebuilt_pages]
    )
    if not (text_equal and pixel_equal and rebuilt_pdf.stat().st_size == len(original_pdf_bytes)):
        failures.append(
            {
                "rebuilt_pdf_content_mismatch": {
                    "raw_expected": original_pdf_hash,
                    "raw_observed": digest(rebuilt_pdf),
                    "bytes_expected": len(original_pdf_bytes),
                    "bytes_observed": rebuilt_pdf.stat().st_size,
                    "text_equal": text_equal,
                    "original_rendered_page_count": len(original_pages),
                    "rebuilt_rendered_page_count": len(rebuilt_pages),
                    "pixel_equal_all_pages": pixel_equal,
                }
            }
        )
    log_text = (package / "build_r3" / "paper_applsci.log").read_text(encoding="utf-8", errors="replace")
    log_counts = {
        "undefined": log_text.casefold().count("undefined"),
        "overfull": log_text.count("Overfull"),
        "latex_warning": log_text.count("LaTeX Warning"),
        "package_warning": log_text.count("Package ") if " Warning" in log_text else 0,
        "pdftex_warning": log_text.count("pdfTeX warning"),
    }
    if any(log_counts.values()):
        failures.append({"final_log_warning_counts": log_counts})
    forbidden = []
    for path in package.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(package).as_posix()
        if "restricted_local_only" in rel or path.name == "predictions.jsonl":
            forbidden.append(rel)
        if path.name in {"nerc_full_pdf_benchmark_v0_3.jsonl", "nerc_full_pdf_dev_v0_3.jsonl", "nerc_full_pdf_test_v0_3.jsonl"}:
            forbidden.append(rel)
        if "__pycache__" in path.parts or path.suffix.lower() == ".pyc":
            forbidden.append(rel)
    if forbidden:
        failures.append({"forbidden_after_reproduction": sorted(set(forbidden))})

    receipt = {
        "schema": "c2ges-clean-unpack-reproduction-v1",
        "status": "PASS" if not failures else "FAIL",
        "zip_path": ZIP_PATH.relative_to(ROOT).as_posix(),
        "zip_sha256": digest(ZIP_PATH),
        "clean_target": TARGET.relative_to(WORKSPACE).as_posix(),
        "initial_exact_set_verified_files": len(actual_before),
        "commands": command_results,
        "calibration_tests_expected": 10,
        "all_four_figure_hashes_reproduced": not any("regenerated_figure_hash_mismatch" in item for item in failures if isinstance(item, dict)),
        "citation_audit_hash_reproduced": not any("regenerated_citation_audit_hash_mismatch" in item for item in failures if isinstance(item, dict)),
        "pdf_raw_hash_reproduced": raw_pdf_hash_reproduced,
        "pdf_content_reproduced": text_equal and pixel_equal and rebuilt_pdf.stat().st_size == len(original_pdf_bytes),
        "pdf_rendered_page_count": len(original_pages) if len(original_pages) == len(rebuilt_pages) else None,
        "pdf_reproduction_note": "Raw PDF IDs can depend on the absolute build path; acceptance requires identical byte length, extracted text, and every dynamically enumerated rendered page pixel when the raw hash differs.",
        "final_log_counts": log_counts,
        "forbidden_files_after_reproduction": forbidden,
        "failures": failures,
    }
    OUT.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: receipt[key] for key in ("status", "initial_exact_set_verified_files", "all_four_figure_hashes_reproduced", "citation_audit_hash_reproduced", "pdf_raw_hash_reproduced", "pdf_content_reproduced", "final_log_counts", "failures")}, indent=2))
    raise SystemExit(0 if receipt["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
