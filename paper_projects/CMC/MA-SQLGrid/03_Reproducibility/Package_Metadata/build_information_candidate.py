"""Build and unpack a local review candidate. Does not publish or grant rights.

Explicit source selection excludes archives, old manuscripts and working caches.
Verification must leave every unpacked file unchanged and create no extra files.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[2]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def inventory():
    selected = []
    excluded = []
    directories = ["03_Reproducibility/Code", "03_Reproducibility/Data",
                   "01_Manuscript/Supplementary", "01_Manuscript/LaTeX/Definitions",
                   "01_Manuscript/LaTeX/figures"]
    for directory in directories:
        for base, dirs, files in os.walk(ROOT / directory, followlinks=False):
            for name in dirs + files:
                path = Path(base) / name
                if path.is_symlink() or getattr(path.lstat(), "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT:
                    raise ValueError("Reparse point forbidden: " + str(path.relative_to(ROOT)))
            dirs[:] = [name for name in dirs if name not in ("__pycache__", ".git", ".venv")]
            for name in files:
                path = Path(base) / name
                relative = path.relative_to(ROOT).as_posix()
                if path.suffix.lower() in (".pyc", ".aux", ".log", ".out", ".blg"):
                    excluded.append(relative)
                    continue
                if name.lower() in ("database.sqlite", "questions.jsonl") or path.suffix.lower() in (".sqlite", ".db", ".pem", ".key") or name.startswith(".env"):
                    raise ValueError("Restricted filename requires review: " + relative)
                selected.append(path)
    for relative in (
        "01_Manuscript/LaTeX/paper_information.tex",
        "01_Manuscript/LaTeX/paper_information.pdf",
        "01_Manuscript/LaTeX/references_verified.bib",
        "01_Manuscript/LaTeX/references_information.bib",
        "01_Manuscript/LaTeX/BUILD_INFORMATION.md",
        "03_Reproducibility/Package_Metadata/verify_information.py",
        "03_Reproducibility/Package_Metadata/verify_package.py",
        "03_Reproducibility/Package_Metadata/build_information_candidate.py",
        "03_Reproducibility/Package_Metadata/DATA_RIGHTS_NOTICE.md",
    ):
        selected.append(ROOT / relative)
    return sorted(set(selected)), excluded


def snapshot(root):
    return {p.relative_to(root).as_posix(): sha(p.read_bytes())
            for p in root.rglob("*") if p.is_file()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True, help="New directory outside Workspace")
    args = parser.parse_args()
    out = args.output.resolve()
    if out.exists() or out.is_relative_to(ROOT) or not out.parent.is_dir():
        parser.error("Output must be a new directory with existing parent outside Workspace")
    files, excluded = inventory()
    blobs = {p.relative_to(ROOT).as_posix(): p.read_bytes() for p in files}
    manifest = {name: sha(data) for name, data in blobs.items()}
    manifest_text = json.dumps({"schema": "information-local-candidate-v1", "files": manifest,
        "scope": "Local review candidate, not a public release; raw restricted inputs excluded",
        "source_sha256": manifest["01_Manuscript/LaTeX/paper_information.tex"]}, indent=2)
    blobs["CANDIDATE_MANIFEST.json"] = manifest_text.encode("utf-8")
    blobs["READ_ME_FIRST.md"] = (
        "# Information local review candidate\n\n"
        "Run `python -B 03_Reproducibility/Package_Metadata/verify_information.py`.\n"
        "Python 3.12, pdflatex and bibtex on PATH are required. Default reports go to stdout.\n"
        "The included legacy verify_package.py is a data/test dependency, not the current entry.\n"
        "Use INFORMATION_CURRENT_EVIDENCE.md in the supplement to separate current and historical results.\n"
        "This is not an upload authorization, final author approval or acceptance certificate.\n"
        "The all-rights-reserved/third-party restrictions remain applicable.\n"
    ).encode("utf-8")
    out.mkdir()
    archive = out / "MA-SQLGrid_Information_review_candidate.zip"
    with zipfile.ZipFile(archive, "x", zipfile.ZIP_DEFLATED) as handle:
        for name, data in sorted(blobs.items()):
            handle.writestr("MA-SQLGrid/" + name, data)
    (out / "archive_sha256.txt").write_text(sha(archive.read_bytes()) + "  " + archive.name + "\n", encoding="utf-8")
    with tempfile.TemporaryDirectory(prefix="information_unpacked_") as temp:
        with zipfile.ZipFile(archive) as handle:
            handle.extractall(temp)  # Entries are created above from relative local paths only.
        unpacked = Path(temp) / "MA-SQLGrid"
        before = snapshot(unpacked)
        mismatched = [name for name, expected in manifest.items() if before.get(name) != expected]
        if mismatched:
            raise ValueError("Unpacked hash mismatch: " + repr(mismatched))
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
        result = subprocess.run([sys.executable, "-B", str(unpacked / "03_Reproducibility/Package_Metadata/verify_information.py")],
            cwd=unpacked, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
        (out / "verification_stdout.txt").write_text(result.stdout, encoding="utf-8")
        (out / "verification_stderr.txt").write_text(result.stderr, encoding="utf-8")
        after = snapshot(unpacked)
        report = {"verification_exit_code": result.returncode, "files": len(before),
                  "missing": sorted(before.keys() - after.keys()), "unlisted": sorted(after.keys() - before.keys()),
                  "mismatch": sorted(k for k in before.keys() & after.keys() if before[k] != after[k]),
                  "source_files_changed": [p.relative_to(ROOT).as_posix() for p in files
                      if sha(p.read_bytes()) != manifest[p.relative_to(ROOT).as_posix()]],
                  "archive_sha256": sha(archive.read_bytes()), "excluded_cache_files": excluded,
                  "git_directory_present": (unpacked / ".git").exists()}
        report["status"] = "PASS" if result.returncode == 0 and not any(report[k] for k in
            ("missing", "unlisted", "mismatch", "source_files_changed", "git_directory_present")) else "FAIL"
        (out / "UNPACKED_CHECK.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2))
        return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
