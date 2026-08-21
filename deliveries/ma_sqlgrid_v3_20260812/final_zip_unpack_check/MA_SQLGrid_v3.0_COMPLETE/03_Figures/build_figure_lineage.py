"""Build a file-level lineage manifest for the six manuscript figures."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


FIGURES = Path(__file__).resolve().parent
ROOT = FIGURES.parent


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def record(relative: str) -> dict[str, object]:
    path = ROOT / relative
    return {
        "path": relative.replace("\\", "/"),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def outputs(stem: str) -> list[dict[str, object]]:
    values: list[dict[str, object]] = []
    for suffix in (".pdf", ".svg", ".png"):
        relative = stem + suffix
        if (ROOT / relative).exists():
            values.append(record(relative))
    return values


def main() -> None:
    specs = [
        {
            "figure_number": 1,
            "label": "fig:coordination",
            "purpose": "Five-role information flow and per-candidate decision lifecycle.",
            "stem": "figures/fig_ma_sqlgrid_dual_panel",
            "sources": ["figures/generate_p60_additions.py", "paper_applsci.tex"],
        },
        {
            "figure_number": 2,
            "label": "fig:cells",
            "purpose": "GridDB factorial cell estimates for the two frozen backbones.",
            "stem": "figures/results/fig01_v2_cells",
            "sources": [
                "figures/rebuild_publication_figures.py",
                "figures/lineage_sources/fig02_cell_summary_v2.csv",
                "figures/lineage_sources/fig02_canonical_rows_v2.jsonl",
            ],
        },
        {
            "figure_number": 3,
            "label": "fig:components",
            "purpose": "Grouped component-effect estimates and sensitivity intervals.",
            "stem": "figures/results/figure_01_primary_effects",
            "sources": [
                "figures/rebuild_publication_figures.py",
                "figures/lineage_sources/fig03_table_primary_effects.csv",
                "figures/lineage_sources/fig03_canonical_results.json",
            ],
        },
        {
            "figure_number": 4,
            "label": "fig:multistate",
            "purpose": "Constructed-state logical-AND agreement for the automatic subset.",
            "stem": "figures/results/fig04_semantic_reliability",
            "sources": [
                "figures/rebuild_publication_figures.py",
                "figures/lineage_sources/fig04_build_manuscript_semantic_figure.py",
                "figures/lineage_sources/fig04_clustered_contrasts.csv",
                "figures/lineage_sources/fig04_exact_cluster_sign_tests.csv",
                "figures/lineage_sources/fig04_suite_outcomes.csv",
            ],
        },
        {
            "figure_number": 5,
            "label": "fig:offline-diagnostics",
            "purpose": "Historical-pool reference matches and constructed-state invariance.",
            "stem": "figures/fig05_offline_selector_diagnostics",
            "sources": [
                "figures/generate_p60_additions.py",
                "figures/lineage_sources/fig05_selector_diagnostics.csv",
            ],
        },
        {
            "figure_number": 6,
            "label": "fig:evidence-map",
            "purpose": "Scientific evidence flow across the four complementary experiment streams.",
            "stem": "figures/fig06_evidence_map",
            "sources": ["figures/generate_p60_additions.py", "paper_applsci.tex"],
        },
    ]
    figures: list[dict[str, object]] = []
    for spec in specs:
        figures.append(
            {
                "figure_number": spec["figure_number"],
                "label": spec["label"],
                "purpose": spec["purpose"],
                "outputs": outputs(str(spec["stem"])),
                "sources": [record(value) for value in spec["sources"]],
            }
        )
    manifest = {
        "schema_version": "ma-narrative-six-figure-lineage-v2",
        "paper": "MA_SQLGrid",
        "release_root": "formal_submission_ma_narrative_revision_20260812",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "all_used_figures_covered": all(item["outputs"] for item in figures),
        "figure_count": len(figures),
        "figures": figures,
    }
    (FIGURES / "FIGURE_LINEAGE.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
