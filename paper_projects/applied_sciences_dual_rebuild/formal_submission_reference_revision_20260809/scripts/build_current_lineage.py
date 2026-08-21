"""Build six-figure lineage and a hash-bound current-release manifest."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def record(path: Path) -> dict:
    if not path.is_file():
        raise FileNotFoundError(path)
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def page_count(pdf: Path) -> int:
    raw = subprocess.run(["pdfinfo", str(pdf)], check=True, capture_output=True).stdout
    output = raw.decode("latin-1", errors="replace")
    match = re.search(r"^Pages:\s+(\d+)", output, flags=re.MULTILINE)
    if not match:
        raise RuntimeError(f"Cannot determine page count for {pdf}")
    return int(match.group(1))


SOURCE_MAP = {
    "C2GES": [
        ["figure_sources/generate_dual_panel_frameworks.py", "C2GES/paper_applsci.tex"],
        ["C2GES/scripts/generate_figures.py", "C2GES/supplementary/transferable/rights_safe_metadata/rights_safe_report_metadata.json"],
        ["C2GES/scripts/generate_figures.py", "C2GES/supplementary/transferable/audits/aggregate_metrics.json"],
        ["C2GES/scripts/generate_figures.py", "C2GES/supplementary/transferable/figure_inputs/paired_rougel_differences_nonverbatim.csv"],
        ["C2GES/figures/generate_p60_additions.py", "C2GES/figures/lineage_sources/fig05_output_length.csv"],
        ["C2GES/figures/generate_p60_additions.py", "C2GES/paper_applsci.tex"],
    ],
    "MA_SQLGrid": [
        ["figure_sources/generate_dual_panel_frameworks.py", "MA_SQLGrid/paper_applsci.tex"],
        ["MA_SQLGrid/figures/rebuild_publication_figures.py", "MA_SQLGrid/figures/lineage_sources/fig02_cell_summary_v2.csv"],
        ["MA_SQLGrid/figures/rebuild_publication_figures.py", "MA_SQLGrid/figures/lineage_sources/fig03_table_primary_effects.csv"],
        ["MA_SQLGrid/figures/rebuild_publication_figures.py", "MA_SQLGrid/figures/lineage_sources/fig04_build_manuscript_semantic_figure.py", "MA_SQLGrid/figures/lineage_sources/fig04_clustered_contrasts.csv", "MA_SQLGrid/figures/lineage_sources/fig04_exact_cluster_sign_tests.csv", "MA_SQLGrid/figures/lineage_sources/fig04_suite_outcomes.csv"],
        ["MA_SQLGrid/figures/generate_p60_additions.py", "MA_SQLGrid/figures/lineage_sources/fig05_selector_diagnostics.csv"],
        ["MA_SQLGrid/figures/generate_p60_additions.py", "MA_SQLGrid/paper_applsci.tex"],
    ],
}


def figure_blocks(tex: str) -> list[dict]:
    blocks = []
    for match in re.finditer(r"\\begin\{figure\}.*?\\end\{figure\}", tex, flags=re.DOTALL):
        block = match.group(0)
        graphic = re.search(r"\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}", block)
        caption = re.search(r"\\caption\{(.*?)\}\s*\\label", block, flags=re.DOTALL)
        label = re.search(r"\\label\{([^}]+)\}", block)
        if graphic:
            blocks.append({
                "graphic": graphic.group(1),
                "caption": re.sub(r"\s+", " ", caption.group(1)).strip() if caption else None,
                "label": label.group(1) if label else None,
            })
    return blocks


def build_paper(paper: str) -> dict:
    paper_root = ROOT / paper
    tex_path = paper_root / "paper_applsci.tex"
    tex = tex_path.read_text(encoding="utf-8")
    blocks = figure_blocks(tex)
    if len(blocks) != 6:
        raise ValueError(f"{paper}: expected six used figures, found {len(blocks)}")
    figures = []
    for number, (block, sources) in enumerate(zip(blocks, SOURCE_MAP[paper]), start=1):
        output_pdf = paper_root / block["graphic"]
        outputs = [record(output_pdf)]
        for suffix in (".svg", ".png"):
            sibling = output_pdf.with_suffix(suffix)
            if sibling.is_file():
                outputs.append(record(sibling))
        figures.append({
            "figure_number": number,
            "label": block["label"],
            "caption_claim_boundary": block["caption"],
            "outputs": outputs,
            "sources": [record(ROOT / source) for source in sources],
        })
    lineage = {
        "schema_version": "applied-sciences-current-six-figure-lineage-v1",
        "paper": paper,
        "release_root": "formal_submission_reference_revision_20260809",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "all_used_figures_covered": True,
        "figure_count": 6,
        "figures": figures,
    }
    (paper_root / "figures" / "FIGURE_LINEAGE.json").write_text(json.dumps(lineage, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    pdf = paper_root / "paper_applsci.pdf"
    bibs = sorted(paper_root.glob("*.bib"))
    result = {
        "paper": paper,
        "status": "current",
        "pages": page_count(pdf),
        "figures": 6,
        "tex": record(tex_path),
        "pdf": record(pdf),
        "bibliography": [record(path) for path in bibs],
        "figure_lineage": record(paper_root / "figures" / "FIGURE_LINEAGE.json"),
    }
    qa_manifest = paper_root / "VISUAL_QA_MANIFEST.json"
    if qa_manifest.is_file():
        qa = json.loads(qa_manifest.read_text(encoding="utf-8"))
        result["visual_qa"] = {
            "status": qa.get("status"),
            "manifest": record(qa_manifest),
        }
        qa_report = paper_root / "VISUAL_QA_REPORT.md"
        if qa_report.is_file():
            result["visual_qa"]["report"] = record(qa_report)
    return result


def main() -> None:
    papers = [build_paper("C2GES"), build_paper("MA_SQLGrid")]
    manifest = {
        "schema_version": "applied-sciences-dual-current-release-v1",
        "release_date": "2026-08-09",
        "audited_date": "2026-08-11",
        "canonical_root": ROOT.name,
        "version_boundary": record(ROOT / "VERSION_BOUNDARY.md"),
        "audit_correction_report": record(ROOT / "CURRENT_AUDIT_CORRECTION_REPORT_2026-08-11.md"),
        "current_papers": papers,
        "legacy_material": {
            "status": "isolated_not_current",
            "path": "_archive_pre_current_audit",
            "rule": "No audit or figure lineage under the archive may be cited as evidence for the current PDFs.",
        },
    }
    (ROOT / "CURRENT_RELEASE_MANIFEST.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({paper["paper"]: {"pages": paper["pages"], "figures": paper["figures"], "pdf_sha256": paper["pdf"]["sha256"]} for paper in papers}, indent=2))


if __name__ == "__main__":
    main()
