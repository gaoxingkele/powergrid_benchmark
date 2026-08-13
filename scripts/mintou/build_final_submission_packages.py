from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECTS = ROOT / "paper_projects"
EVIDENCE = ROOT / "papers" / "mintou"
REVIEWS = ROOT / "reviews" / "mintou_2026-08-12_three_reviewer_rounds"
OUT = ROOT / "deliverables" / "mintou_2026-08-12_final_packages"

PAPERS = (
    "mintou_p1_dstar_gru_dispatch",
    "mintou_p2_hygraph_load_forecasting",
    "mintou_p3_samode_distribution_planning",
    "mintou_p4_shield_resilience_planning",
    "mintou_p5_trace_moea_feasibility_review",
    "mintou_p6_bilonsga_project_review",
)

BUILD_SUFFIXES = {
    ".aux",
    ".log",
    ".out",
    ".toc",
    ".fls",
    ".fdb_latexmk",
    ".synctex.gz",
}

COMMON_AUDIT_FILES = (
    REVIEWS / "round1_logic_p1_p6.md",
    REVIEWS / "round1_statistics_p1_p6.md",
    REVIEWS / "round1_theory_innovation_p1_p6.md",
    REVIEWS / "round2_logic_p1_p6.md",
    REVIEWS / "round2_statistics_p1_p6.md",
    REVIEWS / "round2_theory_innovation_p1_p6.md",
    REVIEWS / "round3_logic_final_p1_p6.md",
    REVIEWS / "round3_statistics_final_p1_p6.md",
    REVIEWS / "round3_theory_innovation_final_p1_p6.md",
    REVIEWS / "FINAL_THREE_ROUND_CLOSURE_ZH.md",
    ROOT / "reviews" / "mintou_2026-08-10_comprehensive_latest_vs_10" / "COMPREHENSIVE_SIX_PAPER_VS_10_REPORT_ZH.md",
    ROOT / "reviews" / "mintou_2026-08-10_comprehensive_latest_vs_10" / "paper_vs_10_average.csv",
    ROOT / "reviews" / "mintou_2026-08-09_journal_fit_audit" / "reference_verification_summary.json",
)

COMMON_REPRO_FILES = (
    ROOT / "scripts" / "mintou" / "build_statistical_audit_v2.py",
    ROOT / "tests" / "test_mintou_statistical_audit_v2.py",
)


def excluded(path: Path) -> bool:
    lower_name = path.name.lower()
    return any(lower_name.endswith(suffix) for suffix in BUILD_SUFFIXES)


def add_file(
    archive: zipfile.ZipFile,
    source: Path,
    arcname: str,
    manifest: dict[str, str],
) -> None:
    data = source.read_bytes()
    archive.writestr(arcname.replace("\\", "/"), data)
    manifest[arcname.replace("\\", "/")] = hashlib.sha256(data).hexdigest().upper()


def add_tree(
    archive: zipfile.ZipFile,
    source_root: Path,
    archive_root: str,
    manifest: dict[str, str],
) -> None:
    for source in sorted(source_root.rglob("*")):
        if source.is_file() and not excluded(source):
            relative = source.relative_to(source_root).as_posix()
            add_file(archive, source, f"{archive_root}/{relative}", manifest)


def package_readme(paper: str) -> str:
    return f"""# {paper}: final internal submission package

Built on 2026-08-12 from the current official manuscript and frozen evidence tree.

Contents:

- `manuscript_project/`: current Markdown manuscript, figures, tables, and journal-formatted LaTeX/PDF source tree. Transient LaTeX build files are excluded.
- `reproducibility/`: code, configurations, evidence tables, run archives, provenance, and claim-scope records for this paper.
- `portfolio_audit/`: the three rounds of logic, statistics, and theory/innovation reviews, the 10-paper journal comparison, and reference-verification summary.
- `shared_reproducibility/`: the corrected statistical audit implementation and its regression tests.
- `SHA256SUMS.txt`: SHA-256 hashes for every included payload file.

Scientific status: the three expert-review dimensions passed after all blocker/major corrections. Core experiments did not require a new run.

Submission gate: do not upload until all `[AUTHOR INPUT REQUIRED]` fields, CRediT roles, author approvals, affiliations, correspondence, ORCIDs where requested, funding/APC statements, and journal declarations have been completed by the authors. Scientific review PASS is not an acceptance guarantee.
"""


def build_package(paper: str) -> dict[str, object]:
    project_root = PROJECTS / paper
    evidence_root = EVIDENCE / paper
    if not project_root.is_dir() or not evidence_root.is_dir():
        raise FileNotFoundError(f"missing project/evidence root for {paper}")

    OUT.mkdir(parents=True, exist_ok=True)
    archive_path = OUT / f"{paper}_complete_submission_package.zip"
    manifest: dict[str, str] = {}

    with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        readme = package_readme(paper).encode("utf-8")
        archive.writestr("PACKAGE_README.md", readme)
        manifest["PACKAGE_README.md"] = hashlib.sha256(readme).hexdigest().upper()

        add_tree(archive, project_root, "manuscript_project", manifest)
        add_tree(archive, evidence_root, "reproducibility", manifest)

        for source in COMMON_AUDIT_FILES:
            if source.is_file():
                add_file(archive, source, f"portfolio_audit/{source.name}", manifest)
        for source in COMMON_REPRO_FILES:
            if source.is_file():
                add_file(archive, source, f"shared_reproducibility/{source.name}", manifest)

        sums = "\n".join(f"{digest}  {name}" for name, digest in sorted(manifest.items())) + "\n"
        archive.writestr("SHA256SUMS.txt", sums.encode("utf-8"))

    return {
        "paper": paper,
        "archive": str(archive_path.relative_to(ROOT)).replace("\\", "/"),
        "bytes": archive_path.stat().st_size,
        "payload_files": len(manifest),
        "sha256": hashlib.sha256(archive_path.read_bytes()).hexdigest().upper(),
    }


def main() -> int:
    rows = [build_package(paper) for paper in PAPERS]
    manifest_path = OUT / "PACKAGE_MANIFEST.json"
    manifest_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for row in rows:
        print(json.dumps(row, ensure_ascii=False))
    print(f"manifest={manifest_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
