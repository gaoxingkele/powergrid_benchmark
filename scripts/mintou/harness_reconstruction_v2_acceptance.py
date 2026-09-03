"""Deterministic artifact gates for the four locked-title Mintou rebuilds.

This checker verifies that a paper-harness candidate carries the declared
artifacts and provenance.  It does not decide whether a scientific claim is
true and it never converts a pilot result into confirmatory evidence.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

PROJECTS = {
    "mintou_p5_trace_moea_feasibility_review": {
        "paper_id": "P1",
        "title": "Investment Effectiveness Optimization Strategy based on Hybrid Multi-objective Evolution",
        "docclass": "energies",
        "experiment": "p5_s4_energies_investment_validation_v1",
        "authors": ("Yubin Lin", "Jiyu Li", "Xiaofei Ruan", "Xiaoyu Huang", "Dishan Yang"),
        "claim_ids": ("P1-C01", "P1-C02", "P1-C03", "P1-C04", "P1-C05", "P1-C06", "P1-C07", "P1-C08"),
        "min_existing_refs": 33,
    },
    "mintou_p6_bilonsga_project_review": {
        "paper_id": "P2",
        "title": "Multi-objective Evolution Algorithm based on Non-Dominated Sorting and Bidirectional Local Search for Investment Effectiveness Strategy Optimization",
        "docclass": "applsci",
        "experiment": "p6_s4_applsci_grid_investment_v1",
        "authors": ("Yubin Lin", "Jingbo Zhang", "Xiaoyu Huang", "Dishan Yang", "Jiyu Li"),
        "claim_ids": ("P2-C01", "P2-C02", "P2-C03", "P2-C04", "P2-C05", "P2-C06", "P2-C07", "P2-C08"),
        "min_existing_refs": 33,
    },
    "mintou_p3_samode_distribution_planning": {
        "paper_id": "P3",
        "title": "Power Distribution Network Planning Strategy Optimization based on Self-Adaption Multi-objective Differential Evolution Algorithm",
        "docclass": "energies",
        "experiment": "p3_s4_energies_samode_ac_planning_v1",
        "authors": ("Zhang Linyao", "Zheng Jieyun", "Zhang Zhanghuang", "Ni Shiyuan", "Wu Guilian"),
        "claim_ids": ("P3-C01", "P3-C02", "P3-C03", "P3-C04", "P3-C05", "P3-C06", "P3-C07", "P3-C08"),
        "min_existing_refs": 32,
    },
    "mintou_p2_hygraph_load_forecasting": {
        "paper_id": "P4",
        "title": "Graph Convolutional Network based on Hyperbolic Space for Power Load Forecasting",
        "docclass": "electronics",
        "experiment": "p2_s4_electronics_hgcn_load_v1",
        "authors": ("Zheng Jieyun", "Zhang Linyao", "Zhang Zhanghuang", "Chen Zhuolin", "Shi Ying"),
        "claim_ids": ("P4-C01", "P4-C02", "P4-C03", "P4-C04", "P4-C05", "P4-C06", "P4-C07", "P4-C08"),
        "min_existing_refs": 30,
    },
}

PHASES = (
    "contract",
    "literature",
    "protocol",
    "pilot",
    "evidence",
    "pre_integrity",
    "review",
    "re_review",
    "final_integrity",
    "release",
)


def fail(message: str) -> None:
    raise SystemExit(message)


def require_file(path: Path) -> Path:
    if not path.is_file() or path.stat().st_size == 0:
        fail(f"required non-empty file missing: {path}")
    return path


def load_json(path: Path) -> dict:
    require_file(path)
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail(f"invalid JSON {path}: {exc}")
    if not isinstance(value, dict):
        fail(f"JSON root must be an object: {path}")
    return value


def require_keys(value: dict, keys: tuple[str, ...], path: Path) -> None:
    missing = [key for key in keys if key not in value]
    if missing:
        fail(f"missing keys in {path}: {', '.join(missing)}")


def csv_rows(path: Path, required_columns: tuple[str, ...]) -> list[dict[str, str]]:
    require_file(path)
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = tuple(reader.fieldnames or ())
        missing = [column for column in required_columns if column not in fields]
        if missing:
            fail(f"missing CSV columns in {path}: {', '.join(missing)}")
        rows = list(reader)
    if not rows:
        fail(f"CSV contains no records: {path}")
    return rows


def project_paths(project: str) -> tuple[dict, Path, Path, Path]:
    meta = PROJECTS[project]
    project_root = ROOT / "paper_projects" / project
    checkpoint = project_root / "checkpoints" / "2026-09-03_mdpi_wave0"
    experiment = project_root / "experiments" / meta["experiment"]
    return meta, project_root, checkpoint, experiment


def check_contract(project: str) -> None:
    meta, project_root, checkpoint, experiment = project_paths(project)
    tex = require_file(project_root / "manuscript" / "journal_submission" / "paper.tex").read_text(
        encoding="utf-8", errors="replace"
    )
    master = require_file(project_root / "manuscript" / "MANUSCRIPT.md").read_text(
        encoding="utf-8", errors="replace"
    )
    for name, text in (("paper.tex", tex), ("MANUSCRIPT.md", master)):
        if meta["title"] not in text:
            fail(f"locked title absent or changed in {name}: {meta['title']}")
    if not re.search(rf"\\documentclass\[{re.escape(meta['docclass'])}\b", tex):
        fail(f"wrong MDPI document class for {project}: expected {meta['docclass']}")
    missing_authors = [author for author in meta["authors"] if author not in tex]
    if missing_authors:
        fail("locked author names missing from paper.tex: " + ", ".join(missing_authors))

    for name in (
        "BASELINE_MANIFEST.md",
        "CLAIM_EVIDENCE_REGISTER.md",
        "REFERENCE_AUDIT.csv",
        "NEXT_STAGE.md",
    ):
        require_file(checkpoint / name)
    register = (checkpoint / "CLAIM_EVIDENCE_REGISTER.md").read_text(encoding="utf-8")
    missing_claims = [claim_id for claim_id in meta["claim_ids"] if claim_id not in register]
    if missing_claims:
        fail("claim register is incomplete: " + ", ".join(missing_claims))
    protocol = require_file(experiment / "EXPERIMENT_PROTOCOL.md").read_text(encoding="utf-8")
    if "NO_RESULTS" not in protocol:
        fail("Wave-0 experiment scaffold must state NO_RESULTS")


def check_literature(project: str) -> None:
    meta, project_root, _, _ = project_paths(project)
    root = project_root / "manuscript" / "reconstruction_v2" / "literature"
    refs = csv_rows(
        root / "REFERENCE_VERIFICATION.csv",
        (
            "citation_id",
            "title",
            "authors",
            "year",
            "venue",
            "doi_or_url",
            "existence_status",
            "metadata_status",
            "context_status",
            "evidence_source",
        ),
    )
    if len(refs) < meta["min_existing_refs"]:
        fail(f"reference inventory shorter than frozen baseline: {len(refs)} < {meta['min_existing_refs']}")
    blocked = {
        "",
        "pending",
        "unchecked",
        "not_found",
        "mismatch",
        "unverified",
    }
    for row in refs:
        for key in ("existence_status", "metadata_status", "context_status"):
            if row[key].strip().lower() in blocked:
                fail(f"unresolved reference audit {row.get('citation_id', '?')} field {key}: {row[key]}")
    matrix = csv_rows(
        root / "LITERATURE_EVIDENCE_MATRIX.csv",
        ("claim_id", "source_id", "evidence_locator", "support_relation", "verification_status"),
    )
    if not any(row["claim_id"].strip() for row in matrix):
        fail("literature evidence matrix has no claim binding")
    search = load_json(root / "SEARCH_LOG.json")
    require_keys(
        search,
        ("searched_at", "databases", "queries", "inclusion_criteria", "exclusion_criteria", "included_sources"),
        root / "SEARCH_LOG.json",
    )


def check_protocol(project: str) -> None:
    meta, _, _, experiment = project_paths(project)
    config_path = experiment / "config.json"
    config = load_json(config_path)
    require_keys(
        config,
        (
            "schema_version",
            "experiment_id",
            "project",
            "locked_title",
            "status",
            "datasets",
            "baselines",
            "primary_outcomes",
            "secondary_outcomes",
            "seeds",
            "comparison_family",
            "multiplicity",
            "failure_policy",
            "negative_result_policy",
            "pilot",
            "formal",
            "output_schema",
        ),
        config_path,
    )
    if config["status"] != "FROZEN":
        fail(f"experiment protocol is not FROZEN: {config_path}")
    if config["project"] != project or config["locked_title"] != meta["title"]:
        fail(f"experiment config identity mismatch: {config_path}")
    if len(config["baselines"]) < 2 or len(config["seeds"]) < 3:
        fail("formal protocol requires at least two baselines and three paired seeds")
    require_file(experiment / "data_manifest.json")
    require_file(experiment / "environment.json")
    require_file(experiment / "RUNBOOK.md")
    require_file(experiment / "planned_vs_executed.json")


def check_pilot(project: str) -> None:
    _, _, _, experiment = project_paths(project)
    gate_path = experiment / "pilot" / "PILOT_GATE.json"
    gate = load_json(gate_path)
    require_keys(
        gate,
        ("status", "paper_use", "exit_codes_clear", "warnings_reviewed", "budget_audit", "leakage_audit", "decision"),
        gate_path,
    )
    if gate["status"] != "PASS" or gate["paper_use"] is not False:
        fail("pilot must PASS and remain excluded from confirmatory paper results")
    require_file(experiment / "pilot" / "run_manifest.json")
    require_file(experiment / "pilot" / "PILOT_REPORT.md")


def check_evidence(project: str) -> None:
    _, _, _, experiment = project_paths(project)
    formal = experiment / "formal"
    manifest = load_json(formal / "run_manifest.json")
    require_keys(
        manifest,
        ("experiment_id", "config_sha256", "environment_sha256", "runs_planned", "runs_completed", "failed_runs", "artifacts"),
        formal / "run_manifest.json",
    )
    if manifest["runs_completed"] != manifest["runs_planned"] and not manifest["failed_runs"]:
        fail("incomplete formal run set without an explicit failed-runs ledger")
    require_file(formal / "raw" / "results.csv")
    stats = experiment / "statistics"
    require_file(stats / "PRIMARY_RESULTS.csv")
    require_file(stats / "NEGATIVE_RESULTS.csv")
    require_file(stats / "CLAIM_EVIDENCE_FINAL.csv")
    audit = load_json(stats / "STATISTICAL_AUDIT.json")
    require_keys(
        audit,
        ("analysis_unit", "paired_design", "effect_sizes", "confidence_intervals", "multiplicity", "failed_runs_handling"),
        stats / "STATISTICAL_AUDIT.json",
    )


def check_integrity_report(path: Path, *, final: bool) -> None:
    report = load_json(path)
    require_keys(
        report,
        ("verdict", "references", "citation_context", "statistical_data", "originality", "claims", "failure_modes"),
        path,
    )
    if report["verdict"] != "PASS":
        fail(f"integrity report is not PASS: {path}")
    refs = report["references"]
    if refs.get("checked") != refs.get("total"):
        fail(f"reference verification is not 100%: {path}")
    if final and report["citation_context"].get("checked") != report["citation_context"].get("total"):
        fail(f"final citation-context verification is not 100%: {path}")
    modes = report["failure_modes"]
    for mode in range(1, 8):
        item = modes.get(str(mode), {})
        if item.get("status") not in {"CLEAR", "OVERRIDDEN"}:
            fail(f"AI research failure mode {mode} unresolved in {path}")
        if item.get("status") == "OVERRIDDEN" and not item.get("reason"):
            fail(f"failure-mode override lacks human reasoning for mode {mode}: {path}")


def check_pre_integrity(project: str) -> None:
    _, project_root, _, _ = project_paths(project)
    check_integrity_report(
        project_root / "manuscript" / "reconstruction_v2" / "integrity" / "PRE_REVIEW_INTEGRITY.json",
        final=False,
    )


def check_review(project: str) -> None:
    _, project_root, _, _ = project_paths(project)
    root = project_root / "manuscript" / "reconstruction_v2" / "review"
    decision = load_json(root / "ROUND1_EDITORIAL_DECISION.json")
    require_keys(decision, ("decision", "reviewer_ids", "manuscript_sha256", "roadmap_items"), root / "ROUND1_EDITORIAL_DECISION.json")
    expected = {"JF", "R1", "R2", "R3", "DA"}
    if set(decision["reviewer_ids"]) != expected:
        fail("round-1 review must include Journal-Fit, R1, R2, R3, and Devil's Advocate")
    csv_rows(
        root / "REVISION_ROADMAP.csv",
        ("item_id", "priority", "source", "issue", "evidence_anchor", "required_action", "acceptance_test", "status"),
    )


def check_re_review(project: str) -> None:
    _, project_root, _, _ = project_paths(project)
    root = project_root / "manuscript" / "reconstruction_v2" / "review"
    responses = csv_rows(
        root / "RESPONSE_TO_REVIEWERS.csv",
        ("item_id", "author_response", "change_location", "evidence", "status"),
    )
    if any(not row["status"].strip() for row in responses):
        fail("response-to-reviewers contains an untracked item")
    rereview = load_json(root / "REREVIEW_REPORT.json")
    require_keys(rereview, ("decision", "original_draft_sha256", "revised_draft_sha256", "score_trajectory", "residual_issues"), root / "REREVIEW_REPORT.json")
    csv_rows(
        root / "RNR_TRACEABILITY.csv",
        ("concern_id", "authors_claim", "revision_location", "verified", "status", "quality_assessment"),
    )


def check_final_integrity(project: str) -> None:
    _, project_root, _, _ = project_paths(project)
    root = project_root / "manuscript" / "reconstruction_v2"
    check_integrity_report(root / "integrity" / "FINAL_INTEGRITY.json", final=True)
    require_file(root / "qa" / "FIGURE_TABLE_AUDIT.md")
    quality = load_json(root / "qa" / "WRITING_QUALITY_REGRESSION.json")
    require_keys(
        quality,
        ("baseline_sha256", "revised_sha256", "numbers_unchanged", "equations_checked", "citations_unchanged", "claim_strength_drift", "cold_reader_verdict"),
        root / "qa" / "WRITING_QUALITY_REGRESSION.json",
    )
    if quality["numbers_unchanged"] is not True or quality["citations_unchanged"] is not True:
        fail("writing-quality regression detected numeric or citation drift")
    if quality["claim_strength_drift"]:
        fail("writing-quality regression detected unsupported claim-strength drift")
    if quality["cold_reader_verdict"] != "PASS":
        fail("cold-reader writing-quality gate is not PASS")


def check_release(project: str) -> None:
    _, project_root, _, _ = project_paths(project)
    root = project_root / "manuscript" / "reconstruction_v2"
    manifest = load_json(root / "release" / "SUBMISSION_MANIFEST.json")
    require_keys(
        manifest,
        ("locked_title", "target_journal", "latex", "pdf", "figures", "tables", "code", "data", "hashes", "human_gates"),
        root / "release" / "SUBMISSION_MANIFEST.json",
    )
    if manifest["locked_title"] != PROJECTS[project]["title"]:
        fail("release manifest title differs from the locked title")
    if not all(manifest["human_gates"].values()):
        fail("human submission fields remain unconfirmed")
    require_file(project_root / "manuscript" / "journal_submission" / "paper.pdf")


CHECKS = {
    "contract": (check_contract,),
    "literature": (check_contract, check_literature),
    "protocol": (check_contract, check_literature, check_protocol),
    "pilot": (check_contract, check_literature, check_protocol, check_pilot),
    "evidence": (check_contract, check_literature, check_protocol, check_pilot, check_evidence),
    "pre_integrity": (check_contract, check_literature, check_protocol, check_pilot, check_evidence, check_pre_integrity),
    "review": (check_contract, check_literature, check_protocol, check_pilot, check_evidence, check_pre_integrity, check_review),
    "re_review": (check_contract, check_literature, check_protocol, check_pilot, check_evidence, check_pre_integrity, check_review, check_re_review),
    "final_integrity": (check_contract, check_literature, check_protocol, check_pilot, check_evidence, check_pre_integrity, check_review, check_re_review, check_final_integrity),
    "release": (check_contract, check_literature, check_protocol, check_pilot, check_evidence, check_pre_integrity, check_review, check_re_review, check_final_integrity, check_release),
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True, choices=sorted(PROJECTS))
    parser.add_argument("--phase", required=True, choices=PHASES)
    args = parser.parse_args(argv)
    for check in CHECKS[args.phase]:
        check(args.project)
    print(f"OK {args.project}: reconstruction-v2 artifact contract ({args.phase})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
