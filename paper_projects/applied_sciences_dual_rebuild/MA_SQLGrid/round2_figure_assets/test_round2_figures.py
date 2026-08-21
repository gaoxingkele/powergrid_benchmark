#!/usr/bin/env python3
"""Integrity and factual tests for the Round-2 presentation assets."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

from PIL import Image


HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
V2 = PROJECT / "canonical_v2_reanalysis"


def sha256(path: Path) -> str:
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return digest


def rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    manifest = json.loads((HERE / "release_manifest.json").read_text(encoding="utf-8"))
    assert manifest["scope"].endswith("no new model or component results")
    assert "Point estimates only" in manifest["cell_interval_policy"]

    for relative, facts in manifest["source_files"].items():
        path = PROJECT / relative
        assert path.is_file(), path
        assert sha256(path) == facts["sha256"], path
        assert path.stat().st_size == facts["bytes"], path

    audit = rows(V2 / "tables" / "context_question_gold_offline_audit.csv")
    multi = [row for row in audit if int(row["gold_required_table_count"]) > 1]
    expected = {
        "all_gold_tables_retained": sum(int(row["gold_all_tables_retained"]) for row in audit),
        "all_gold_tables_denominator": len(audit),
        "all_gold_columns_retained": sum(int(row["gold_all_columns_retained"]) for row in audit),
        "all_gold_columns_denominator": len(audit),
        "multi_table_join_paths_retained": sum(int(row["gold_join_path_retained"]) for row in multi),
        "multi_table_denominator": len(multi),
    }
    assert expected == manifest["derived_context_counts"]
    assert expected == {
        "all_gold_tables_retained": 179,
        "all_gold_tables_denominator": 180,
        "all_gold_columns_retained": 155,
        "all_gold_columns_denominator": 180,
        "multi_table_join_paths_retained": 115,
        "multi_table_denominator": 116,
    }

    expected_stems = [
        "ma_r2_f01_v2_cells_point_estimates",
        "ma_r2_f02_context_audit_direct_counts",
    ]
    for stem in expected_stems:
        for extension in ("svg", "pdf", "png"):
            path = HERE / "figures" / f"{stem}.{extension}"
            assert path.is_file() and path.stat().st_size > 1000, path
        with Image.open(HERE / "figures" / f"{stem}.png") as image:
            dpi = image.info.get("dpi", (0, 0))
            assert min(dpi) >= 449, (stem, dpi)
            assert image.width >= 4000 and image.height >= 1500, (stem, image.size)

    cell_svg = (HERE / "figures" / "ma_r2_f01_v2_cells_point_estimates.svg").read_text(encoding="utf-8")
    assert "POINT ESTIMATES ONLY" in cell_svg
    assert "composition-sensitivity intervals are intentionally omitted" in cell_svg
    context_svg = (HERE / "figures" / "ma_r2_f02_context_audit_direct_counts.svg").read_text(encoding="utf-8")
    for direct_count in ("179/180", "155/180", "115/116"):
        assert direct_count in context_svg

    for extension in ("pdf", "png"):
        path = HERE / "qa" / f"page_scale_preview.{extension}"
        assert path.is_file() and path.stat().st_size > 1000, path

    for relative, facts in manifest["output_files"].items():
        path = HERE / relative
        assert sha256(path) == facts["sha256"], path
        assert path.stat().st_size == facts["bytes"], path

    print("PASS: Round-2 figure assets, frozen-source hashes, direct counts, formats, and 450-dpi PNGs verified.")


if __name__ == "__main__":
    main()
