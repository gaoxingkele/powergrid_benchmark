"""Build release and supplementary manifests for the current manuscript."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
RELEASE = ROOT.parent


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def record(path: Path, base: Path = RELEASE) -> dict[str, object]:
    return {
        "path": path.relative_to(base).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def pdf_pages(path: Path) -> int:
    completed = subprocess.run(["pdfinfo", str(path)], check=True, capture_output=True)
    match = re.search(
        r"^Pages:\s+(\d+)", completed.stdout.decode("latin-1"), flags=re.MULTILINE
    )
    if not match:
        raise RuntimeError("pdfinfo did not return a page count")
    return int(match.group(1))


def main() -> None:
    supplement = ROOT / "supplementary"
    supplement_files = sorted(
        path
        for path in supplement.rglob("*")
        if path.is_file() and path.name != "SUPPLEMENT_MANIFEST.json"
    )
    supplement_manifest = {
        "schema_version": "ma-sqlgrid-supplement-v1",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "source_boundary": "Byte-preserving copies from original_title_manuscript/FINAL plus the new README.",
        "files": [record(path, supplement) for path in supplement_files],
    }
    supplement_path = supplement / "SUPPLEMENT_MANIFEST.json"
    supplement_path.write_text(
        json.dumps(supplement_manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    core_paths = [
        ROOT / "paper_applsci.tex",
        ROOT / "paper_applsci.pdf",
        ROOT / "references_verified.bib",
        ROOT / "SUPPLEMENTARY_MATERIALS.md",
        ROOT / "VISUAL_QA_MANIFEST.json",
        ROOT / "VISUAL_QA_REPORT.md",
        ROOT / "figures" / "FIGURE_LINEAGE.json",
        supplement_path,
        RELEASE / "README.md",
        RELEASE / "REVISION_LEDGER.md",
        RELEASE / "NARRATIVE_REVISION_SUMMARY.md",
    ]
    figures = [
        ROOT / "figures" / "fig_ma_sqlgrid_dual_panel.pdf",
        ROOT / "figures" / "results" / "fig01_v2_cells.pdf",
        ROOT / "figures" / "results" / "figure_01_primary_effects.pdf",
        ROOT / "figures" / "results" / "fig04_semantic_reliability.pdf",
        ROOT / "figures" / "fig05_offline_selector_diagnostics.pdf",
        ROOT / "figures" / "fig06_evidence_map.pdf",
    ]
    tex_text = (ROOT / "paper_applsci.tex").read_text(encoding="utf-8")
    release_manifest = {
        "schema_version": "ma-sqlgrid-narrative-release-v1",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "release": "formal_submission_ma_narrative_revision_20260812",
        "base_tex_sha256": "AFB06156782467C495E36964FEB541FC6C0C061D8AA8C795DD924D27C7000D99",
        "change_scope": "Narrative restructuring and Figure 6 redesign; no new experiment, dataset, baseline, or quantitative result.",
        "paper": {
            "title": "MA-SQLGrid: A Robust and Auditable Multi-Agent Framework for Power-Grid Text-to-SQL",
            "pages": pdf_pages(ROOT / "paper_applsci.pdf"),
            "figures": len(re.findall(r"\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}", tex_text)),
            "tables": len(re.findall(r"\\begin\{table\}", tex_text)),
        },
        "visual_qa_status": json.loads((ROOT / "VISUAL_QA_MANIFEST.json").read_text(encoding="utf-8-sig"))["status"],
        "core_files": [record(path) for path in core_paths],
        "manuscript_figure_pdfs": [record(path) for path in figures],
    }
    (RELEASE / "RELEASE_MANIFEST.json").write_text(
        json.dumps(release_manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
