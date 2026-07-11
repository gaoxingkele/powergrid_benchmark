from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MINTOU_ROOT = ROOT / "papers" / "mintou"
OUT = MINTOU_ROOT / "submission_assets"


@dataclass(frozen=True)
class PaperAsset:
    paper_id: str
    directory: str
    title: str
    algorithm: str
    target_journal: str
    backup_journal: str
    status: str
    signal: str
    strongest_claim: str
    boundary: str
    next_validation: str


KNOWN_SIGNALS = {
    "mintou_p1": "narrow_promising_public_signal",
    "mintou_p2": "day_ahead_promising_public_signal",
    "mintou_p3": "narrow_promising_public_signal",
    "mintou_p4": "promising_public_signal",
    "mintou_p5": "promising_public_signal",
    "mintou_p6": "promising_public_signal",
}

CLAIM_SUMMARIES = {
    "mintou_p1": "RTS-GMLC fixed/rolling dispatch proxy and high-renewable stress subset support DSTAR-GRU narrowly.",
    "mintou_p2": "OPSD and SimBench rolling evidence support day-ahead/24h hierarchical load forecasting.",
    "mintou_p3": "SimBench DER/storage stress proxy supports CARS-MODE narrowly after preserving weak revisions.",
    "mintou_p4": "SimBench resilience-planning proxy supports SHIELD-MOEA against baseline and ablation.",
    "mintou_p5": "RTS-GMLC + SimBench + NERC-report-cache project-review proxy supports TRACE-MOEA.",
    "mintou_p6": "Budget-constrained project-review proxy supports BiLo-NSGA and bidirectional local search.",
}

BOUNDARIES = {
    "mintou_p1": "Not AC-OPF or unit-commitment proof; topology-control validation remains pending.",
    "mintou_p2": "Do not claim 1h superiority; claims should focus on day-ahead/24h behavior.",
    "mintou_p3": "Not AC/pandapower feasible planning proof; proxy hypervolume gain is narrow.",
    "mintou_p4": "Scenario proxy lacks full AC/pandapower feasibility and scenario variance.",
    "mintou_p5": "Benchmark-derived review proxy lacks expert-labeled approval outcomes and calibrated costs.",
    "mintou_p6": "Benchmark-derived project-review proxy lacks expert labels and enterprise validation.",
}

NEXT_VALIDATION = {
    "mintou_p1": "Add DC-OPF/UC or Grid2Op validation.",
    "mintou_p2": "Add stronger neural short-horizon baselines only if 1h claims are needed.",
    "mintou_p3": "Add pandapower/AC load-flow and repeated DER-hosting scenario variance.",
    "mintou_p4": "Add AC/pandapower feasibility and repeated scenario variance.",
    "mintou_p5": "Add expert-labeled feasibility-review outcomes and cost calibration.",
    "mintou_p6": "Add expert-labeled review outcomes, dependency labels, and calibrated budget cases.",
}


def read_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end < 0:
        return {}
    block = text[3:end].strip()
    values: dict[str, str] = {}
    for line in block.splitlines():
        if ":" not in line:
            continue
        key, raw = line.split(":", 1)
        values[key.strip()] = raw.strip().strip('"')
    return values


def first_heading(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.parent.name


def collect_assets() -> list[PaperAsset]:
    assets: list[PaperAsset] = []
    for paper_dir in sorted(MINTOU_ROOT.glob("mintou_p*")):
        if not paper_dir.is_dir():
            continue
        paper = paper_dir / "PAPER.md"
        meta = read_frontmatter(paper)
        paper_id = meta.get("paper_id", paper_dir.name.split("_")[0])
        assets.append(
            PaperAsset(
                paper_id=paper_id,
                directory=paper_dir.name,
                title=meta.get("title") or first_heading(paper),
                algorithm=meta.get("algorithm", ""),
                target_journal=meta.get("target_journal", ""),
                backup_journal=meta.get("backup_journal", ""),
                status=meta.get("status", ""),
                signal=KNOWN_SIGNALS.get(paper_id, "not_classified"),
                strongest_claim=CLAIM_SUMMARIES.get(paper_id, ""),
                boundary=BOUNDARIES.get(paper_id, ""),
                next_validation=NEXT_VALIDATION.get(paper_id, ""),
            )
        )
    return assets


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def collect_evidence_rows(assets: list[PaperAsset]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for asset in assets:
        root = MINTOU_ROOT / asset.directory
        for path in sorted((root / "evidence").rglob("*")):
            if not path.is_file():
                continue
            kind = "other"
            if "\\tables\\" in str(path) or "/tables/" in str(path):
                kind = "table"
            elif "\\runs\\" in str(path) or "/runs/" in str(path):
                kind = "run"
            elif "\\source\\" in str(path) or "/source/" in str(path):
                kind = "source"
            preserved = "yes" if re.search(r"_(weak|mixed|marginal|near_miss)", path.stem) else "no"
            rows.append(
                {
                    "paper_id": asset.paper_id,
                    "algorithm": asset.algorithm,
                    "kind": kind,
                    "path": relative(path),
                    "file": path.name,
                    "bytes": str(path.stat().st_size),
                    "preserved_negative_or_mixed": preserved,
                }
            )
    return rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys()) if rows else []
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown_table(path: Path, headers: list[str], rows: list[list[str]], title: str, intro: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"# {title}", ""]
    if intro:
        lines.extend([intro, ""])
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join("---" for _ in headers) + " |")
    for row in rows:
        lines.append("| " + " | ".join(cell.replace("|", "/") for cell in row) + " |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_readme(assets: list[PaperAsset], evidence_rows: list[dict[str, str]]) -> None:
    lines = [
        "# Mintou Submission Assets",
        "",
        "This directory is the portfolio-level submission asset package for the six `mintou` ARA papers.",
        "",
        "It does not replace each paper ARA. It indexes the current evidence, claim scope, preserved negative results, and remaining validation gaps so manuscript drafting can stay aligned with the evidence.",
        "",
        "## Files",
        "",
        "- `paper_asset_manifest.csv`: one-row summary for each paper.",
        "- `evidence_index.csv`: all current evidence files under the six ARA directories.",
        "- `claim_scope_matrix.md`: supported claim scope and boundary for each paper.",
        "- `reviewer_readiness_checklist.md`: pre-submission checklist against reproducibility and evidence discipline.",
        "- `remaining_validation_gaps.md`: unresolved validation items that must not be hidden.",
        "",
        "## Portfolio Snapshot",
        "",
    ]
    lines.append("| Paper | Algorithm | Target | Signal | Evidence Files | Preserved Negative/Mixed |")
    lines.append("|---|---|---|---|---:|---:|")
    for asset in assets:
        rows = [row for row in evidence_rows if row["paper_id"] == asset.paper_id]
        preserved = [row for row in rows if row["preserved_negative_or_mixed"] == "yes"]
        lines.append(
            f"| `{asset.paper_id}` | `{asset.algorithm}` | {asset.target_journal} | `{asset.signal}` | {len(rows)} | {len(preserved)} |"
        )
    lines.extend(
        [
            "",
            "## Manuscript Discipline",
            "",
            "- Claims must cite the exact evidence table or analysis file.",
            "- Weak, mixed, marginal, and near-miss results are preserved as part of the research trace.",
            "- Public benchmark-derived proxy results must not be rewritten as enterprise, AC-OPF, UC, or expert-labeled results.",
        ]
    )
    (OUT / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def build_checklist(assets: list[PaperAsset]) -> None:
    rows = []
    for asset in assets:
        root = MINTOU_ROOT / asset.directory
        rows.append(
            [
                asset.paper_id,
                "yes" if (root / "PAPER.md").exists() else "no",
                "yes" if (root / "logic" / "claims.md").exists() else "no",
                "yes" if (root / "src" / "environment.md").exists() else "no",
                "yes" if any((root / "evidence" / "tables").glob("real_*_leaderboard*.csv")) else "no",
                "yes" if any((root / "evidence" / "runs").glob("*_weak.*")) or any((root / "evidence" / "runs").glob("*_mixed.*")) or any((root / "evidence" / "runs").glob("*_marginal.*")) else "no",
                asset.next_validation,
            ]
        )
    write_markdown_table(
        OUT / "reviewer_readiness_checklist.md",
        ["Paper", "PAPER", "Claims", "Environment", "Real Tables", "Negative Trace", "Next Gate"],
        rows,
        "Reviewer Readiness Checklist",
        "This checklist verifies evidence-package completeness, not final acceptance readiness.",
    )


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    assets = collect_assets()
    evidence_rows = collect_evidence_rows(assets)
    write_csv(OUT / "paper_asset_manifest.csv", [asset.__dict__ for asset in assets])
    write_csv(OUT / "evidence_index.csv", evidence_rows)
    build_readme(assets, evidence_rows)
    write_markdown_table(
        OUT / "claim_scope_matrix.md",
        ["Paper", "Algorithm", "Supported Scope", "Boundary", "Next Validation"],
        [[a.paper_id, a.algorithm, a.strongest_claim, a.boundary, a.next_validation] for a in assets],
        "Claim Scope Matrix",
        "Use this matrix before manuscript drafting to keep every claim within the evidence boundary.",
    )
    write_markdown_table(
        OUT / "remaining_validation_gaps.md",
        ["Paper", "Signal", "Remaining Validation Gap"],
        [[a.paper_id, a.signal, a.next_validation] for a in assets],
        "Remaining Validation Gaps",
        "These are not failures of the ARA package; they are boundaries that must be disclosed or closed before stronger claims.",
    )
    build_checklist(assets)
    print(f"wrote submission assets to {OUT}")
    print(f"papers={len(assets)} evidence_files={len(evidence_rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
