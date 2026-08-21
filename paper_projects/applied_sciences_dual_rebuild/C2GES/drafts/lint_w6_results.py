"""Lint C2GES W6 results/discussion against frozen claim boundaries."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
DRAFT = Path(__file__).with_name("W6_RESULTS_DISCUSSION_DRAFT.md")
REPORT = Path(__file__).with_name("W6_RESULTS_LINT.json")
MARKER_RE = re.compile(
    r"<!-- CLAIM: (?P<claim>C2-C\d{2}) \| STATUS: (?P<status>[A-Z0-9-]+) "
    r"\| ARTIFACT: (?P<artifact>[^|]+?) \| KEYS: (?P<keys>.+?) -->"
)
WORD_RE = re.compile(r"\b[A-Za-z0-9][A-Za-z0-9'–-]*\b")


def is_prose(block: str) -> bool:
    stripped = block.strip()
    skip = ("#", "<!--", "|", "- ", "```", "\\[")
    return bool(stripped) and not stripped.startswith(skip)


def main() -> int:
    text = DRAFT.read_text(encoding="utf-8")
    blocks = [part.strip() for part in re.split(r"\n\s*\n", text) if part.strip()]
    prose_indices = [i for i, block in enumerate(blocks) if is_prose(block)]
    missing_markers = []
    for index in prose_indices:
        following = blocks[index + 1] if index + 1 < len(blocks) else ""
        if not MARKER_RE.fullmatch(following):
            missing_markers.append(blocks[index][:140])

    markers = list(MARKER_RE.finditer(text))
    missing_paths = []
    for marker in markers:
        relative = marker.group("artifact").strip()
        if not (ROOT / relative).exists():
            missing_paths.append(relative)

    required_claims = {f"C2-C{i:02d}" for i in range(1, 10)}
    present_claims = {marker.group("claim") for marker in markers}
    obsolete_numbers = re.findall(r"(?<!\d)(?:4000|800)(?!\d)", text)

    dangerous_patterns = {
        "role_gain_positive": r"(?:^|[.!?]\s+)Role conditioning (?:reliably |significantly )?improves?\b",
        "blanket_bm25_positive": r"(?:^|[.!?]\s+)C2GES (?:broadly|uniformly|consistently) outperforms? BM25\b",
        "oracle_end_to_end_positive": r"\boracle(?:-label)? (?:is|was) end-to-end\b",
        "nerc_human_gold_positive": r"\bNERC (?:is|was|provides?) (?:a )?human[- ]gold\b",
        "nerc_superiority_positive": r"\bNERC (?:proves?|demonstrates?) (?:quantitative )?(?:domain )?superiority\b",
    }
    dangerous_hits = {
        name: re.findall(pattern, text, flags=re.IGNORECASE)
        for name, pattern in dangerous_patterns.items()
        if re.search(pattern, text, flags=re.IGNORECASE)
    }

    required_phrases = [
        "primary role-conditioning claim is a frozen **NO-GO**",
        "blanket superiority over BM25 is also **NO-GO**",
        "BM25 was clearly stronger at \\(K=1\\)",
        "oracle-label and predicted-label C2GES had tiny positive differences",
        "label-blind comparison did not pass at \\(K=3\\)",
        "minimum attainable two-sided p-value of \\(2/32=0.0625\\)",
        "oracle branch is not",
        "agent-rewritten, agent-verified silver",
        "Preferred option",
        "Alternative option",
    ]
    missing_disclosures = [phrase for phrase in required_phrases if phrase not in text]

    issues = {
        "prose_without_adjacent_claim_marker": missing_markers,
        "missing_artifact_paths": sorted(set(missing_paths)),
        "missing_claim_ids": sorted(required_claims - present_claims),
        "obsolete_split_numbers": obsolete_numbers,
        "dangerous_positive_claims": dangerous_hits,
        "missing_required_disclosures": missing_disclosures,
    }
    passed = not any(issues.values())
    report = {
        "draft": str(DRAFT.relative_to(ROOT)).replace("\\", "/"),
        "passed": passed,
        "english_word_count": len(WORD_RE.findall(text)),
        "prose_paragraph_count": len(prose_indices),
        "claim_marker_count": len(markers),
        "no_go_occurrences": text.count("NO-GO"),
        "claims_present": sorted(present_claims),
        "issues": issues,
    }
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
