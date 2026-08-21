#!/usr/bin/env python3
"""Fail closed when the manuscript detaches from canonical evidence."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve()
MANUSCRIPT = HERE.parent.parent
MA_ROOT = MANUSCRIPT.parent
REPO_ROOT = MA_ROOT.parents[2]
TEX = MANUSCRIPT / "paper_applsci.tex"
V2 = MA_ROOT / "canonical_v2_reanalysis"
V3 = MA_ROOT / "canonical_v3_inference_hierarchy"
COMPONENT_RAW = MA_ROOT / "prospective_component_experiments" / "analysis"
COMPONENT_RELEASE = MA_ROOT / "component_canonical_release"
ASSETS = MA_ROOT / "round1_revision_assets"
R2_ASSETS = MA_ROOT / "round2_figure_assets" / "figures"
SEMANTIC = MA_ROOT / "semantic_reliability_experiment"
SEMANTIC_RELEASE = SEMANTIC / "formal_v5_release" / "release_manifest.json"
SEMANTIC_LINEAGE = SEMANTIC / "formal_v5_analysis" / "MANUSCRIPT_FIGURE_LINEAGE.json"
SEMANTIC_PORTABLE = SEMANTIC / "formal_v5_release" / "release_manifest_portable.json"
SEMANTIC_CLEAN_REPORT = SEMANTIC / "formal_v5_release" / "PORTABLE_VERIFY_CLEAN_COPY.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_manifest(root: Path, manifest_path: Path, errors: list[str], label: str) -> int:
    if not manifest_path.is_file():
        errors.append(f"missing {label} manifest: {manifest_path}")
        return 0
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    outputs = manifest.get("outputs", manifest.get("files", {}))
    for rel, spec in outputs.items():
        path = root / rel
        expected = spec.get("sha256") if isinstance(spec, dict) else None
        if not path.is_file() or (expected and sha(path) != expected):
            errors.append(f"{label} mismatch: {path}")
    return len(outputs)


def main() -> int:
    errors: list[str] = []
    text = TEX.read_text(encoding="utf-8")
    n_v2 = verify_manifest(V2, V2 / "release_manifest.json", errors, "v2")
    n_v3 = verify_manifest(V3, V3 / "release_manifest.json", errors, "v3")
    n_raw = verify_manifest(
        COMPONENT_RAW,
        COMPONENT_RAW / "ANALYSIS_MANIFEST.json",
        errors,
        "prospective component analysis",
    )

    if not SEMANTIC_RELEASE.is_file():
        errors.append(f"missing semantic release manifest: {SEMANTIC_RELEASE}")
    else:
        semantic_manifest = json.loads(SEMANTIC_RELEASE.read_text(encoding="utf-8"))
        if semantic_manifest.get("invariants", {}).get("atomic_rows") != 25920:
            errors.append("semantic release atomic-row invariant mismatch")
        for artifact in semantic_manifest.get("artifacts", []):
            path = Path(artifact["path"])
            if not path.is_file() or path.stat().st_size != artifact["bytes"] or sha(path) != artifact["sha256"]:
                errors.append(f"semantic release artifact mismatch: {path}")

    for audit_name in ("POST_SCORE_INDEPENDENT_AUDIT_A.json", "POST_SCORE_INDEPENDENT_AUDIT_B.json"):
        audit_path = SEMANTIC / audit_name
        if not audit_path.is_file() or json.loads(audit_path.read_text(encoding="utf-8")).get("decision") != "PASS_INTEGRATION":
            errors.append(f"semantic post-score integration gate failed: {audit_path}")

    if not SEMANTIC_LINEAGE.is_file():
        errors.append(f"missing semantic manuscript lineage: {SEMANTIC_LINEAGE}")
    else:
        semantic_lineage = json.loads(SEMANTIC_LINEAGE.read_text(encoding="utf-8"))
        for group in ("outputs", "tables"):
            for artifact in semantic_lineage.get(group, {}).values():
                path = Path(artifact["path"])
                if not path.is_file() or path.stat().st_size != artifact["bytes"] or sha(path) != artifact["sha256"]:
                    errors.append(f"semantic manuscript artifact mismatch: {path}")

    if not SEMANTIC_PORTABLE.is_file():
        errors.append(f"missing portable semantic manifest: {SEMANTIC_PORTABLE}")
    else:
        portable = json.loads(SEMANTIC_PORTABLE.read_text(encoding="utf-8"))
        for artifact in portable.get("artifacts", []):
            rel = Path(artifact["path"])
            path = REPO_ROOT / rel
            if rel.is_absolute() or ".." in rel.parts or not path.is_file() or path.stat().st_size != artifact["bytes"] or sha(path) != artifact["sha256"]:
                errors.append(f"portable semantic artifact mismatch: {artifact['path']}")
    if not SEMANTIC_CLEAN_REPORT.is_file():
        errors.append(f"missing clean-copy portable verification: {SEMANTIC_CLEAN_REPORT}")
    else:
        clean_report = json.loads(SEMANTIC_CLEAN_REPORT.read_text(encoding="utf-8"))
        if (
            clean_report.get("status") != "PASS"
            or clean_report.get("checked_files_including_root_marker") != 19
            or clean_report.get("manifest_sha256") != sha(SEMANTIC_PORTABLE)
        ):
            errors.append("clean-copy portable verification did not pass")

    # Canonical copied assets from the factorial release and the independently
    # reviewed Round-2 figure release.  The latter adds an explicit
    # point-estimate-only label and direct selector-coverage counts.
    result_sources = {
        "fig01_v2_cells.pdf": R2_ASSETS / "ma_r2_f01_v2_cells_point_estimates.pdf",
        "fig02_v2_factorial_effects.pdf": V2 / "figures" / "fig02_v2_factorial_effects.pdf",
        "fig03_context_audit.pdf": R2_ASSETS / "ma_r2_f02_context_audit_direct_counts.pdf",
    }
    for name, source in result_sources.items():
        target = MANUSCRIPT / "figures" / "results" / name
        if not target.is_file() or sha(target) != sha(source):
            errors.append(f"copied reviewed result figure mismatch: {target}")
    for name in ("ma_r1_f01_executed_pipeline.pdf", "ma_r1_f02_factorial_design.pdf", "ma_r1_f03_external_evidence_gate.pdf"):
        source = ASSETS / "figures" / name
        target = MANUSCRIPT / "figures" / "frameworks" / name
        if not target.is_file() or sha(target) != sha(source):
            errors.append(f"copied framework mismatch: {target}")

    # When the independently rebuilt component release is present, require its two
    # primary manuscript figures to be byte-identical. Final Round-2 assembly adds
    # these assets before delivery.
    component_figures = ("figure_01_primary_effects.pdf", "figure_02_selection_descriptives.pdf")
    if COMPONENT_RELEASE.is_dir():
        release_manifest = COMPONENT_RELEASE / "release_manifest.json"
        if release_manifest.is_file():
            verify_manifest(COMPONENT_RELEASE, release_manifest, errors, "component canonical release")
        for name in component_figures:
            source = COMPONENT_RELEASE / name
            target = MANUSCRIPT / "figures" / "results" / name
            if not target.is_file() or sha(target) != sha(source):
                errors.append(f"copied component figure mismatch: {target}")
        selection_source = COMPONENT_RELEASE / "table_selection_descriptives.tex"
        selection_target = MANUSCRIPT / "tables" / "table_selection_descriptives.tex"
        if not selection_target.is_file() or sha(selection_target) != sha(selection_source):
            errors.append(f"copied component table mismatch: {selection_target}")
        primary_source = COMPONENT_RELEASE / "table_primary_effects.tex"
        primary_target = MANUSCRIPT / "tables" / "table_primary_effects.tex"
        expected_primary = primary_source.read_text(encoding="utf-8").replace(
            "95\\% CI", "95\\% comp.-sens. interval"
        )
        if not primary_target.is_file() or primary_target.read_text(encoding="utf-8") != expected_primary:
            errors.append(f"controlled component interval-label transform mismatch: {primary_target}")

    required = [
        r"\documentclass[applsci,article,submit,moreauthors]{Definitions/mdpi}",
        "MA-SQLGrid: A Multi-Stage Context-Grounding Framework",
        "bundled package factor, not an isolated schema-length intervention",
        "GridDB-tailored composite structural/SQL-operation hint",
        "common-target projected-column diagnostic",
        "Zero of nine primary execution tests survives Holm correction",
        "projected-column adherence increased under the hint",
        "58 singletons",
        "39 difficulty-by-feature groups",
        "composition-sensitivity interval",
        "700 scored calls total",
        "E1 presented value evidence increases first-candidate Qwen execution equality by +0.1059",
        "Neither survives its two-test Holm family",
        "no cross-backbone replication",
        "latency remains diagnostic",
        "SQLite 3.40.1",
        "2500 calls per backbone and 5000 calls",
        "completed all 5000 registered calls",
        "re-executed all 4000 predictions with zero mismatches",
        "machine-adjudicated silver",
        "registered no-drop execution",
        "Retrospective Multi-State Reliability Stress Test",
        "25,920 atomic executions",
        "not semantic certification",
        "15/364 is not reported as accuracy",
        r"\dataavailability{",
        r"\authorcontributions{",
        r"\funding{",
        r"\conflictsofinterest{",
        "During preparation of this manuscript, the authors used OpenAI Codex",
        "Liu Bijing $^{1,2}$, Sun Chenglong $^{1,2}$ and Yang Yong",
        "Conceptualization, B.L. and Y.Y.; methodology, B.L.",
        "grant number 521300250006",
        "https://github.com/gaoxingkele/ma-sqlgrid",
        "available from the corresponding author upon reasonable request for editorial and peer-review verification",
        "All authors have read and agreed to the published version of the manuscript",
        "The authors declare no conflicts of interest",
        "Machine-generated external question--SQL candidates are not used as human or domain-expert ground truth",
    ]
    for token in required:
        if token not in text:
            errors.append(f"required evidence-boundary language missing: {token}")

    prohibited = [
        "gold-SQL preflight remains blocked at 499/500",
        "SQLite 3.49.1",
        "The nonzero three-way modifier",
        "statistically clearer for Qwen",
        "Qwen's structural edges at both packages",
        "comparative efficiency were planned but lack completed",
        "15/364 accuracy",
        "first power-grid text-to-SQL",
        "W10\\_FRONT\\_MATTER",
        "agent technical reviewer",
        "BIRD draft only",
        "post-review",
        "Round-1 audit",
        "paired CMC manuscript",
    ]
    for token in prohibited:
        if token.lower() in text.lower():
            errors.append(f"prohibited stale/promoted claim found: {token}")

    bib = (MANUSCRIPT / "references_verified.bib").read_text(encoding="utf-8")
    bib_keys = set(re.findall(r"@[A-Za-z]+\s*\{\s*([^,\s]+)", bib))
    cited: set[str] = set()
    for group in re.findall(r"\\cite[pt]?\{([^}]+)\}", text):
        cited.update(key.strip() for key in group.split(","))
    missing = sorted(cited - bib_keys)
    if missing:
        errors.append("missing bibliography keys: " + ", ".join(missing))

    figures = re.findall(r"\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}", text)
    for rel in figures:
        if not (MANUSCRIPT / rel).is_file():
            errors.append(f"missing figure: {rel}")
    expected_figures = 9 if COMPONENT_RELEASE.is_dir() and SEMANTIC_RELEASE.is_file() else 8 if COMPONENT_RELEASE.is_dir() else 6
    if len(figures) != expected_figures:
        errors.append(f"expected {expected_figures} revised manuscript figures, found {len(figures)}")
    for rel in re.findall(r"\\input\{([^}]+)\}", text):
        if not (MANUSCRIPT / rel).is_file():
            errors.append(f"missing table input: {rel}")

    if errors:
        for error in errors:
            print("FAIL:", error)
        print(f"Manuscript verification failed with {len(errors)} error(s).")
        return 1
    print(
        f"PASS: v2={n_v2}, v3={n_v3}, component-analysis={n_raw} manifest outputs; "
        f"{len(figures)} figures and {len(cited)} citation keys verified."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
