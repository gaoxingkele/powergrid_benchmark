#!/usr/bin/env python3
"""Lint W8 Qwen-only Results/Discussion claim and scope boundaries."""

from __future__ import annotations

import json
import re
from pathlib import Path


HERE = Path(__file__).resolve().parent
DRAFT = HERE / "W8_QWEN_RESULTS_DISCUSSION.md"
REPORT = HERE / "W8_QWEN_RESULTS_LINT.json"
RELEASE = HERE.parent / "canonical_qwen7b"

CLAIM_RE = re.compile(r"<!-- CLAIM (MA-C\d+) \| STATUS ([A-Z0-9-]+) \| SOURCE (.+?) -->")
NUMBER_RE = re.compile(r"(?<![A-Za-z])(?:\d+\.\d+|\d+\s*[×x]\s*\d+|\d+\s+of\s+\d+)")


def main() -> None:
    text = DRAFT.read_text(encoding="utf-8")
    markers = CLAIM_RE.findall(text)
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    numeric_without_marker = []
    for index, paragraph in enumerate(paragraphs):
        if paragraph.startswith(("#", ">", "-", "<!--")):
            continue
        if NUMBER_RE.search(paragraph):
            following = paragraphs[index + 1] if index + 1 < len(paragraphs) else ""
            if not (CLAIM_RE.search(paragraph) or CLAIM_RE.fullmatch(following)):
                numeric_without_marker.append(paragraph[:140])

    required_phrases = [
        "one quantized Qwen model and one execution seed",
        "GridDB",
        "Granite robustness is PENDING",
        "HUMAN-DEPENDENT",
        "AUTO_CANDIDATE",
        "quarantined_not_eligible_for_claim_promotion",
        "does not contain a comparable latency",
        "MA-C03 is consequently NO–GO",
    ]
    missing_phrases = [phrase for phrase in required_phrases if phrase not in text]
    prohibited_patterns = {
        "granite_result": r"Granite\s+(?:achieved|obtained|outperformed|improved)",
        "external_accuracy_result": r"(?:RTS-GMLC|SimBench)\s+(?:achieved|obtained|outperformed|reached|scored)",
        "broad_generalization": r"generalizes\s+across\s+(?:models|databases)",
        "independent_positive_claim": r"compact context and (?:the )?shape hint(?:s)? (?:have|show|provide) independent positive",
        "contaminated_input_promotion": r"quarantined(?: run| directory)?.{0,80}(?:used as|included in|promoted to) (?:a )?(?:canonical|eligible|result)",
    }
    prohibited_hits = {name: re.findall(pattern, text, flags=re.IGNORECASE) for name, pattern in prohibited_patterns.items()}
    prohibited_hits = {name: hits for name, hits in prohibited_hits.items() if hits}

    required_claims = {"MA-C02", "MA-C03", "MA-C06", "MA-C09", "MA-C10", "MA-C11", "MA-C12"}
    observed_claims = {claim for claim, _, _ in markers}
    missing_artifacts = []
    for relative in [
        "release_manifest.json",
        "tables/table01_cell_accuracy.csv",
        "tables/table02_factorial_effects.csv",
        "tables/table03_registered_contrasts.csv",
        "tables/table04_error_taxonomy.csv",
        "tables/table05_family_error_summary.csv",
        "figures/fig01_cell_accuracy.svg",
        "figures/fig02_factorial_effects.svg",
        "figures/fig03_execution_shape_tradeoff.svg",
        "figures/fig04_registered_contrasts.svg",
        "figures/fig05_error_taxonomy.svg",
        "figures/fig06_family_execution_heatmap.svg",
    ]:
        if not (RELEASE / relative).is_file():
            missing_artifacts.append(relative)

    report = {
        "draft": DRAFT.name,
        "passed": not numeric_without_marker and not missing_phrases and not prohibited_hits and not (required_claims - observed_claims) and not missing_artifacts,
        "word_count": len(re.findall(r"\b[A-Za-z][A-Za-z0-9'–-]*\b", re.sub(r"<!--.*?-->", "", text, flags=re.S))),
        "paragraph_count": sum(1 for p in paragraphs if not p.startswith(("#", "<!--", "-"))),
        "claim_marker_count": len(markers),
        "observed_claims": sorted(observed_claims),
        "missing_required_claims": sorted(required_claims - observed_claims),
        "numeric_paragraphs_without_marker": numeric_without_marker,
        "missing_required_phrases": missing_phrases,
        "prohibited_hits": prohibited_hits,
        "missing_artifacts": missing_artifacts,
        "scope": "Qwen-7B/GridDB only; Granite, external accuracy, efficiency, and human review remain gated.",
    }
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    raise SystemExit(0 if report["passed"] else 1)


if __name__ == "__main__":
    main()
