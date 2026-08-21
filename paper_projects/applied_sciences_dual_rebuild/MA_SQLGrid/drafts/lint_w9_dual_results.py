#!/usr/bin/env python3
"""Lint the bounded MA-SQLGrid dual-backbone Results/Discussion staging draft."""

from __future__ import annotations

import json
import re
from pathlib import Path


HERE = Path(__file__).resolve().parent
DRAFT = HERE / "W9_DUAL_BACKBONE_RESULTS_DISCUSSION.md"
REPORT = HERE / "W9_DUAL_RESULTS_LINT.json"
RELEASE = HERE.parent / "canonical_dual_backbone"
CLAIM_RE = re.compile(r"<!-- CLAIM (MA-C\d+) \| STATUS ([A-Z0-9-]+) \| SOURCE (.+?) -->")
NUMBER_RE = re.compile(r"(?<![A-Za-z])(?:\d+\.\d+|\d+\s*[×x]\s*\d+|\d+\s+of\s+\d+)")


def main() -> None:
    text = DRAFT.read_text(encoding="utf-8")
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    markers = CLAIM_RE.findall(text)
    numeric_without_marker = []
    for i, paragraph in enumerate(paragraphs):
        if paragraph.startswith(("#", ">", "-", "<!--")):
            continue
        following = paragraphs[i + 1] if i + 1 < len(paragraphs) else ""
        if NUMBER_RE.search(paragraph) and not (CLAIM_RE.search(paragraph) or CLAIM_RE.fullmatch(following)):
            numeric_without_marker.append(paragraph[:160])

    required = [
        "bounded two-backbone sensitivity analysis",
        "not evidence of general model-family robustness",
        "positive for both backbones",
        "Granite's interval [−0.0200, +0.3665] crosses zero",
        "−0.1611",
        "three-way interaction is +0.1889",
        "AUTO_CANDIDATE",
        "HUMAN-DEPENDENT",
        "Comparative efficiency also remains PENDING",
    ]
    missing_required = [phrase for phrase in required if phrase not in text]
    prohibited = {
        "general_family_robustness": r"(?:demonstrates|establishes|proves) (?:general )?model-family robustness",
        "granite_exec_significance": r"Granite(?:'s)? execution (?:shape-hint )?(?:main )?effect (?:is|was) significant",
        "external_accuracy": r"(?:RTS-GMLC|SimBench)\s+(?:achieved|obtained|reached|scored|outperformed)",
        "efficiency_result": r"(?:Qwen|Granite)\s+(?:was|is) (?:faster|more efficient|cheaper)",
        "global_backbone_rank": r"Qwen (?:globally|universally|overall) outperforms Granite",
    }
    hits = {name: re.findall(pattern, text, flags=re.I) for name, pattern in prohibited.items()}
    hits = {name: values for name, values in hits.items() if values}
    required_claims = {"MA-C03", "MA-C06", "MA-C08", "MA-C09", "MA-C12", "MA-C13", "MA-C14", "MA-C15"}
    observed = {c for c, _, _ in markers}
    artifacts = [
        "release_manifest.json", "CAPTIONS.md", "VISUAL_QA.md",
        "tables/table01_dual_cell_accuracy.csv", "tables/table02_backbone_factorial_effects.csv",
        "tables/table03_backbone_effect_modifiers.csv", "tables/table04_shape_effect_replication.csv",
        "tables/table05_cross_backbone_cells.csv", "figures/fig01_dual_cell_accuracy.svg",
        "figures/fig02_backbone_factorial_effects.svg", "figures/fig03_backbone_effect_modifiers.svg",
        "figures/fig04_shape_effect_replication.svg", "figures/fig05_cross_backbone_cells.svg",
    ]
    missing_artifacts = [p for p in artifacts if not (RELEASE / p).is_file()]
    report = {
        "draft": DRAFT.name,
        "passed": not numeric_without_marker and not missing_required and not hits and not (required_claims - observed) and not missing_artifacts,
        "word_count": len(re.findall(r"\b[A-Za-z][A-Za-z0-9'–-]*\b", re.sub(r"<!--.*?-->", "", text, flags=re.S))),
        "paragraph_count": sum(1 for p in paragraphs if not p.startswith(("#", "<!--", "-"))),
        "claim_marker_count": len(markers),
        "observed_claims": sorted(observed),
        "missing_required_claims": sorted(required_claims - observed),
        "numeric_paragraphs_without_marker": numeric_without_marker,
        "missing_required_phrases": missing_required,
        "prohibited_hits": hits,
        "missing_artifacts": missing_artifacts,
        "scope": "Two quantized instruction backbones, one GridDB; external/human/efficiency gates remain open.",
    }
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    raise SystemExit(0 if report["passed"] else 1)


if __name__ == "__main__":
    main()
