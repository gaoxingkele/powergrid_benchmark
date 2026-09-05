"""Build one complete, hash-bound lineage registry for all manuscript figures."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


PROJECT = Path(__file__).resolve().parents[3]
FIGURES = PROJECT / "03_Reproducibility" / "Figures"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def record(path: str, *, name: str | None = None) -> dict:
    target = PROJECT / path
    if not target.is_file():
        raise FileNotFoundError(target)
    return {
        "name": name or target.stem,
        "path": path.replace("\\", "/"),
        "bytes": target.stat().st_size,
        "sha256": sha256(target),
    }


def outputs(stem: str, extensions: tuple[str, ...]) -> dict:
    return {
        extension: record(f"03_Reproducibility/Figures/{stem}.{extension}")
        for extension in extensions
    }


def main() -> None:
    shared_script = record(
        "03_Reproducibility/Code/figure_generation/generate_figures.py",
        name="generate_figures",
    )
    artifacts = {
        "fig01_algorithm": {
            "manuscript_id": "Figure 1 / label fig:framework",
            "function": "method_schematic",
            "inputs": [],
            "script": record(
                "03_Reproducibility/Code/figure_generation/generate_framework_revision.py",
                name="generate_framework_revision",
            ),
            "outputs": {
                "pdf": record("03_Reproducibility/Figures/fig01_algorithm_dual_panel.pdf"),
                "svg": record("03_Reproducibility/Figures/fig01_algorithm_dual_panel.svg"),
                "png": record("03_Reproducibility/Figures/fig01_algorithm_dual_panel_preview.png"),
            },
            "supported_claim": "conceptual rendering of the implemented deterministic pipeline and path-deletion definition",
            "limitation": "method schematic; it contains no empirical observation",
            "caption_claim_anchor": "Materials and Methods, Method Overview",
        },
        "fig02_dataset_flow": {
            "manuscript_id": "Figure 2 / label fig:data-flow",
            "function": "dataset_flow",
            "inputs": [record("03_Reproducibility/Data/rights_safe_metadata/rights_safe_report_metadata.json", name="rights_inventory")],
            "script": {**shared_script, "function": "dataset_flow"},
            "outputs": outputs("fig02_dataset_flow", ("pdf", "png")),
            "supported_claim": "40 to 27 to 12/15 sampling flow, 3,200 pages and 12,924 candidates",
            "limitation": "rights-safe metadata only; source prose and PDFs are excluded",
            "caption_claim_anchor": "Materials and Methods, Source PDFs, Inclusion, and Leakage Gates",
        },
        "fig03_aggregate_rougel": {
            "manuscript_id": "Figure 3 / label fig:aggregate",
            "function": "aggregate",
            "inputs": [
                record("03_Reproducibility/Data/formal_protocol/formal_config_v0_3_1.json", name="formal_config"),
                record("03_Reproducibility/Data/audits/aggregate_metrics.json", name="aggregate_metrics"),
            ],
            "script": {**shared_script, "function": "aggregate"},
            "outputs": outputs("fig03_aggregate_rougel", ("pdf", "png")),
            "supported_claim": "descriptive macro-mean ROUGE-L for seven conditions at K=5 and K=10",
            "limitation": "equal-sentence, not equal-word, budgets; bars omit paired uncertainty",
            "caption_claim_anchor": "Results, Aggregate Test Results",
        },
        "fig04_paired_differences": {
            "manuscript_id": "Figure 5 / label fig:paired",
            "function": "paired",
            "inputs": [
                record("03_Reproducibility/Data/formal_protocol/formal_config_v0_3_1.json", name="formal_config"),
                record("03_Reproducibility/Data/figure_inputs/paired_rougel_differences_nonverbatim.csv", name="paired_differences"),
            ],
            "script": {**shared_script, "function": "paired"},
            "outputs": outputs("fig04_paired_differences", ("pdf", "png")),
            "supported_claim": "all 90 rights-safe paired differences and six sign-count labels",
            "limitation": "non-verbatim report indices replace titles; inferential assumptions remain as stated in the manuscript",
            "caption_claim_anchor": "Results, Paired Directions and Exact Post-Run Sensitivity",
        },
        "fig05_output_length": {
            "manuscript_id": "Figure 4 / label fig:length",
            "function": "output_length",
            "inputs": [record("03_Reproducibility/Data/postrun_diagnostics/output_length_summary.csv", name="output_length_summary")],
            "script": record(
                "03_Reproducibility/Code/figure_generation/generate_output_length.py",
                name="generate_output_length",
            ),
            "outputs": outputs("fig05_output_length", ("pdf", "svg", "png")),
            "supported_claim": "mean selected words for four principal conditions at K=5 and K=10",
            "limitation": "diagnostic of archived selections; no word-budget reselection was performed",
            "caption_claim_anchor": "Results, Output-Length and Unit-Type Audit",
        },
        "fig06_component_diagnostic": {
            "manuscript_id": "Figure 6 / label fig:component-diagnostic",
            "function": "component_diagnostic",
            "inputs": [
                record("03_Reproducibility/Data/audits/POSTRUN_AUDIT_v0_3_1.json", name="independent_postrun_audit"),
                record("03_Reproducibility/Code/dev_calibration/artifacts/CALIBRATION_DECISION.json", name="development_calibration_decision"),
            ],
            "script": record(
                "03_Reproducibility/Code/figure_generation/generate_component_diagnostic.py",
                name="generate_component_diagnostic",
            ),
            "outputs": outputs("fig06_component_diagnostic", ("pdf", "svg", "png")),
            "supported_claim": "registered score and selection activity, report-level contrast intervals, and development-only zero-weight fold count",
            "limitation": "historical post-run diagnosis; it is neither a clean normalized ablation nor fresh confirmation",
            "caption_claim_anchor": "Results, Component Diagnosis",
        },
    }
    lineage = {
        "schema": "c2ges-figure-lineage-v3",
        "status": "PASS",
        "clean_unpack_portable": True,
        "workspace_parent_access": False,
        "artifact_count": len(artifacts),
        "artifacts": artifacts,
    }
    target = FIGURES / "FIGURE_LINEAGE.json"
    target.write_text(json.dumps(lineage, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(target)


if __name__ == "__main__":
    main()
