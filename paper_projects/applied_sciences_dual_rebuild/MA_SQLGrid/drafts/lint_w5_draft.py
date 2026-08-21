"""Evidence-bound lint for the MA-SQLGrid W5 staging draft."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
DRAFT = Path(__file__).with_name("W5_METHOD_DATA_DRAFT.md")
REPORT = Path(__file__).with_name("W5_DRAFT_LINT.json")

MARKER_RE = re.compile(
    r"<!-- CLAIM: (?P<claim>MA-C\d{2}) \| STATUS: (?P<status>[A-Z0-9-]+) "
    r"\| ARTIFACT: (?P<artifact>[^|]+?) \| KEYS: (?P<keys>.+?) -->"
)
WORD_RE = re.compile(r"\b[A-Za-z0-9][A-Za-z0-9'–-]*\b")


def is_prose(block: str) -> bool:
    stripped = block.strip()
    skip_prefixes = ("#", "<!--", "```", "\\[", "|", "- ", "1. ", "2. ", "3. ", "4. ")
    equation_leadin = stripped.endswith(" as")
    return bool(stripped) and not stripped.startswith(skip_prefixes) and not equation_leadin


def main() -> int:
    text = DRAFT.read_text(encoding="utf-8")
    blocks = [block.strip() for block in re.split(r"\n\s*\n", text) if block.strip()]
    prose_indices = [i for i, block in enumerate(blocks) if is_prose(block)]
    missing_markers = []
    for index in prose_indices:
        next_index = index + 1
        while next_index < len(blocks) and blocks[next_index].startswith("\\["):
            next_index += 1
        following = blocks[next_index] if next_index < len(blocks) else ""
        if not MARKER_RE.fullmatch(following):
            missing_markers.append(blocks[index][:120])

    markers = list(MARKER_RE.finditer(text))
    missing_artifacts = []
    for marker in markers:
        relative = marker.group("artifact").strip()
        if not (ROOT / relative).exists():
            missing_artifacts.append(relative)

    required_claims = {f"MA-C{i:02d}" for i in range(1, 10)}
    present_claims = {marker.group("claim") for marker in markers}
    missing_claims = sorted(required_claims - present_claims)

    dangerous_patterns = {
        "positive_human_gold": r"\b(?:is|are) human-gold\b",
        "positive_sealed_benchmark": r"\b(?:is|are|as) (?:a )?sealed benchmark\b",
        "positive_publication_ready": r"\b(?:is|are|as) publication-ready gold\b",
        "unsupported_outperformance": r"\b(?:outperforms?|surpasses?)\b",
    }
    dangerous_hits = {
        name: re.findall(pattern, text, flags=re.IGNORECASE)
        for name, pattern in dangerous_patterns.items()
        if re.search(pattern, text, flags=re.IGNORECASE)
    }

    required_phrases = [
        "zero predictions and zero scores",
        "development-visible",
        "non-human-reviewed",
        "non-sealed",
        "No explicit GridDB redistribution license",
        "Four SimBench reference queries return empty result sets",
        "no completed expert forms",
        "PENDING-EVIDENCE",
    ]
    missing_phrases = [phrase for phrase in required_phrases if phrase not in text]

    issues = {
        "prose_without_adjacent_claim_marker": missing_markers,
        "missing_artifact_paths": sorted(set(missing_artifacts)),
        "missing_claim_ids": missing_claims,
        "dangerous_positive_claims": dangerous_hits,
        "missing_required_disclosures": missing_phrases,
    }
    passed = not any(issues.values())
    report = {
        "draft": str(DRAFT.relative_to(ROOT)).replace("\\", "/"),
        "passed": passed,
        "english_word_count": len(WORD_RE.findall(text)),
        "prose_paragraph_count": len(prose_indices),
        "claim_marker_count": len(markers),
        "pending_evidence_occurrences": text.count("PENDING-EVIDENCE"),
        "pending_table_cells": text.count("**PENDING"),
        "claims_present": sorted(present_claims),
        "issues": issues,
    }
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
