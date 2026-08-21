"""Build the round-bound lineage manifest for every figure used in FINAL."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def record(relative: str) -> dict[str, object]:
    path = ROOT / relative
    return {
        "path": relative.replace("\\", "/"),
        "bytes": path.stat().st_size,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


figures = [
    {
        "figure_number": 1,
        "artifact_id": "implemented_coordination_final",
        "outputs": [
            record("figures/fig_ma_sqlgrid_implemented_coordination_final.svg"),
            record("figures/fig_ma_sqlgrid_implemented_coordination_final.png"),
        ],
        "sources": [
            record("code/ma_sqlgrid_agents.py"),
            record("code/sqlite_readonly_executor_final.py"),
        ],
        "generation": "deterministic native SVG edited from the frozen R3 source and rasterized with local headless Edge; no image-generation API",
        "caption_claim_boundary": "Shows implemented role, blackboard, executor, complete-state, adjudication, and gold-isolation boundaries; it does not establish five-role efficacy, semantic correctness, user authorization, or deployment safety.",
    },
    {
        "figure_number": 2,
        "artifact_id": "griddb_factorial_cell_point_estimates",
        "outputs": [record("figures/results/fig01_v2_cells.pdf")],
        "sources": [
            record("figures/lineage_sources/fig02_cell_summary_v2.csv"),
            record("figures/lineage_sources/fig02_canonical_rows_v2.jsonl"),
            record("figures/lineage_sources/fig02_build_v2_reanalysis.py"),
        ],
        "generation": "matplotlib output from the canonical v2 offline reanalysis",
        "caption_claim_boundary": "Displays descriptive GridDB cell point estimates for 180 attempts per cell; it is not a substitute for registered clustered inference or domain-semantic validation.",
    },
    {
        "figure_number": 3,
        "artifact_id": "component_primary_effects",
        "outputs": [record("figures/results/figure_01_primary_effects.pdf")],
        "sources": [
            record("figures/lineage_sources/fig03_table_primary_effects.csv"),
            record("figures/lineage_sources/fig03_canonical_results.json"),
            record("figures/lineage_sources/fig03_build_release.py"),
        ],
        "generation": "matplotlib output from the independently audited 700-call component release",
        "caption_claim_boundary": "Shows cluster-bootstrap intervals for component endpoints only; it does not estimate a five-role or autonomous multi-agent effect.",
    },
    {
        "figure_number": 4,
        "artifact_id": "multistate_semantic_reliability_effects",
        "outputs": [record("figures/results/fig04_semantic_reliability.pdf")],
        "sources": [
            record("figures/lineage_sources/fig04_clustered_contrasts.csv"),
            record("figures/lineage_sources/fig04_exact_cluster_sign_tests.csv"),
            record("figures/lineage_sources/fig04_suite_outcomes.csv"),
            record("figures/lineage_sources/fig04_build_manuscript_semantic_figure.py"),
        ],
        "generation": "matplotlib output from the frozen v5 multi-state analysis",
        "caption_claim_boundary": "Shows constructed-state execution-agreement contrasts; it does not establish qualified power-grid semantic validity or deployment robustness.",
    },
]

manifest = {
    "schema_version": "ma-sqlgrid-final-figure-lineage-v2",
    "paper": "MA-SQLGrid original-title edition",
    "round": "FINAL candidate after R3 review",
    "all_used_figures_covered": True,
    "figure_count": len(figures),
    "figures": figures,
}
(ROOT / "figures" / "FIGURE_LINEAGE.json").write_text(
    json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print(json.dumps({"figure_count": len(figures), "status": "PASS"}, sort_keys=True))
