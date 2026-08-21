"""Evidence and boundary lint for the C2GES W5 staging draft."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
DRAFT = Path(__file__).with_name("W5_METHOD_DATA_DRAFT.md")
REPORT = Path(__file__).with_name("W5_DRAFT_LINT.json")

MARKER_RE = re.compile(
    r"<!-- CLAIM: (?P<claim>C2-C\d{2}) \| STATUS: (?P<status>[A-Z0-9-]+) "
    r"\| ARTIFACT: (?P<artifact>[^|]+?) \| KEYS: (?P<keys>.+?) -->"
)
WORD_RE = re.compile(r"\b[A-Za-z0-9][A-Za-z0-9'–-]*\b")


def is_prose(block: str) -> bool:
    stripped = block.strip()
    skip = ("#", "<!--", "```", "\\[", "|", "- ", "1. ", "2. ", "3. ", "4. ", "5. ", "6. ")
    return bool(stripped) and not stripped.startswith(skip)


def main() -> int:
    text = DRAFT.read_text(encoding="utf-8")
    blocks = [part.strip() for part in re.split(r"\n\s*\n", text) if part.strip()]
    prose_indices = [index for index, block in enumerate(blocks) if is_prose(block)]
    missing_markers = []
    counted_prose = []
    for index in prose_indices:
        # A short prose block immediately introducing a display equation inherits
        # the evidence marker attached to the explanatory paragraph after it.
        if index + 1 < len(blocks) and blocks[index + 1].startswith("\\["):
            continue
        counted_prose.append(index)
        following = blocks[index + 1] if index + 1 < len(blocks) else ""
        if not MARKER_RE.fullmatch(following):
            missing_markers.append(blocks[index][:140])

    markers = list(MARKER_RE.finditer(text))
    missing_artifacts = []
    for marker in markers:
        relative = marker.group("artifact").strip()
        if not (ROOT / relative).exists():
            missing_artifacts.append(relative)

    required_claims = {f"C2-C{i:02d}" for i in range(1, 10)}
    present_claims = {marker.group("claim") for marker in markers}
    missing_claims = sorted(required_claims - present_claims)

    # The rejected historical split must not enter the new methods draft.
    obsolete_split_hits = re.findall(r"(?<!\d)(?:4000|800)(?!\d)", text)
    dangerous_patterns = {
        "oracle_presented_end_to_end": r"oracle-label[^.]{0,80}\bis end-to-end\b",
        "broad_bm25_superiority": r"\b(?:broadly|consistently|significantly) outperforms? BM25\b",
        "nerc_human_gold_positive": r"NERC[^.]{0,100}\b(?:is|are) (?:a )?human[- ]gold\b",
        "nerc_quantitative_superiority": r"NERC[^.]{0,160}\b(?:proves?|demonstrates?) (?:quantitative )?(?:domain )?superiority\b",
    }
    dangerous_hits = {
        name: re.findall(pattern, text, flags=re.IGNORECASE)
        for name, pattern in dangerous_patterns.items()
        if re.search(pattern, text, flags=re.IGNORECASE)
    }

    required_phrases = [
        "8000 training, 1500 development, and 1500 test",
        "745, 141, and 145 unique documents",
        "document-grouped OOF",
        "classifier fitted only on the training partition",
        "label-blind",
        "end_to_end=false",
        "145 test documents",
        "PENDING-EVIDENCE",
        "five-seed",
        "agent-rewritten and agent-verified silver",
        "47 of 47",
    ]
    missing_phrases = [phrase for phrase in required_phrases if phrase not in text]

    issues = {
        "prose_without_adjacent_claim_marker": missing_markers,
        "missing_artifact_paths": sorted(set(missing_artifacts)),
        "missing_claim_ids": missing_claims,
        "obsolete_split_numbers": obsolete_split_hits,
        "dangerous_positive_claims": dangerous_hits,
        "missing_required_disclosures": missing_phrases,
    }
    passed = not any(issues.values())
    report = {
        "draft": str(DRAFT.relative_to(ROOT)).replace("\\", "/"),
        "passed": passed,
        "english_word_count": len(WORD_RE.findall(text)),
        "evidence_checked_prose_paragraph_count": len(counted_prose),
        "equation_leadin_count": len(prose_indices) - len(counted_prose),
        "claim_marker_count": len(markers),
        "pending_evidence_occurrences": text.count("PENDING-EVIDENCE"),
        "pending_result_cells": text.count("**PENDING"),
        "claims_present": sorted(present_claims),
        "issues": issues,
    }
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
