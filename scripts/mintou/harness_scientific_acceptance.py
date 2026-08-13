"""Evidence-contract checks for the six Mintou paper-harness projects.

The script is intentionally conservative.  It does not decide whether a
scientific claim is true; it verifies that a candidate revision records the
claim-to-evidence contract needed for a human acceptance decision and that the
shared Mintou evidence scaffold still passes its deterministic regression
tests.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PROJECTS = {
    "mintou_p1_dstar_gru_dispatch": {"companions": ()},
    "mintou_p2_hygraph_load_forecasting": {"companions": ()},
    "mintou_p3_samode_distribution_planning": {
        "companions": ("mintou_p4_shield_resilience_planning",),
    },
    "mintou_p4_shield_resilience_planning": {
        "companions": ("mintou_p3_samode_distribution_planning",),
    },
    "mintou_p5_trace_moea_feasibility_review": {
        "companions": ("mintou_p6_bilonsga_project_review",),
    },
    "mintou_p6_bilonsga_project_review": {
        "companions": ("mintou_p5_trace_moea_feasibility_review",),
    },
}

REQUIRED_MATRIX_HEADINGS = (
    "Title-to-Evidence Map",
    "Primary Estimand and Analysis Unit",
    "Comparison Budget and Data Visibility",
    "Negative and Null Results",
    "Shared Assets and Independent Contribution",
    "New or Rerun Experiments",
    "Unresolved Human Blockers",
)

FORBIDDEN_HEADLINE_CONTRADICTIONS = {
    "mintou_p1_dstar_gru_dispatch": (
        "Persistence achieves the lowest overall MAE at both horizons",
        "Persistence leads aggregate MAE",
    ),
}


def fail(message: str) -> None:
    raise SystemExit(message)


def run_regression_tests() -> None:
    pytest = shutil.which("pytest")
    if not pytest:
        fail("pytest executable not found; cannot run Mintou evidence regression tests")
    proc = subprocess.run(
        [pytest, "-q", "tests/test_mintou_experiments.py"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
    )
    if proc.returncode:
        fail("Mintou evidence regression failed:\n" + (proc.stdout + proc.stderr)[-4000:])


def check_matrix(project: str) -> Path:
    project_root = ROOT / "paper_projects" / project
    matrix = project_root / "manuscript" / "DEEP_REVISION_EVIDENCE.md"
    if not matrix.exists():
        fail(f"revision evidence matrix missing: {matrix}")
    text = matrix.read_text(encoding="utf-8", errors="replace")
    missing = [heading for heading in REQUIRED_MATRIX_HEADINGS if heading.lower() not in text.lower()]
    if missing:
        fail("revision evidence matrix is incomplete: " + ", ".join(missing))
    if "AUTHOR INPUT REQUIRED" not in text and "human blocker" not in text.lower():
        fail("matrix must preserve unresolved author/funding metadata as a human blocker")
    companions = PROJECTS[project]["companions"]
    for companion in companions:
        if companion not in text:
            fail(f"shared-asset disclosure must name companion project: {companion}")
    return matrix


def check_manuscript(project: str) -> None:
    master = ROOT / "paper_projects" / project / "manuscript" / "MANUSCRIPT.md"
    if not master.exists():
        fail(f"manuscript master missing: {master}")
    text = master.read_text(encoding="utf-8", errors="replace")
    for phrase in FORBIDDEN_HEADLINE_CONTRADICTIONS.get(project, ()):
        if phrase.lower() in text.lower():
            fail(f"known headline/table contradiction remains: {phrase}")


def check_evidence_tree(project: str) -> None:
    evidence = ROOT / "papers" / "mintou" / project / "evidence"
    for relative in ("runs", "tables", "source"):
        target = evidence / relative
        if not target.is_dir() or not any(target.iterdir()):
            fail(f"evidence subtree missing or empty: {target}")
    config_root = ROOT / "papers" / "mintou" / project / "src" / "configs"
    if not config_root.is_dir() or not any(config_root.glob("*.json")):
        fail(f"machine-readable experiment configuration missing: {config_root}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True, choices=sorted(PROJECTS))
    parser.add_argument(
        "--phase",
        choices=("narrative", "evidence", "full"),
        default="full",
        help="narrative checks the claim contract; evidence also checks assets/tests",
    )
    args = parser.parse_args(argv)

    check_matrix(args.project)
    check_manuscript(args.project)
    if args.phase in {"evidence", "full"}:
        check_evidence_tree(args.project)
        run_regression_tests()
    print(f"OK {args.project}: scientific evidence contract ({args.phase})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
