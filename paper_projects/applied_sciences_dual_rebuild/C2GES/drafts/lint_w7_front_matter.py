"""Lint the C2GES W7 front matter, claims, abstract, and citations."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
DRAFT = Path(__file__).with_name("W7_FRONT_MATTER_DRAFT.md")
REPORT = Path(__file__).with_name("W7_FRONT_MATTER_LINT.json")
BIB = ROOT / "paper_projects/CMC/C2GES/06_Applied_Sciences_Current/references_applsci.bib"
MARKER_RE = re.compile(
    r"<!-- CLAIM: (?P<claim>C2-C\d{2}) \| STATUS: (?P<status>[A-Z0-9-]+) "
    r"\| ARTIFACT: (?P<artifact>[^|]+?) \| KEYS: (?P<keys>.+?) -->"
)
WORD_RE = re.compile(r"\b[A-Za-z0-9][A-Za-z0-9'–-]*\b")


def is_prose(block: str) -> bool:
    stripped = block.strip()
    return bool(stripped) and not stripped.startswith(("#", "<!--", "|", "- "))


def main() -> int:
    text = DRAFT.read_text(encoding="utf-8")
    bib_text = BIB.read_text(encoding="utf-8")
    abstract_match = re.search(r"## Abstract\s+(.+?)\s+<!-- CLAIM:", text, flags=re.DOTALL)
    abstract = abstract_match.group(1).strip() if abstract_match else ""
    abstract_words = len(WORD_RE.findall(abstract))

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

    cited_keys = set()
    for citation in re.findall(r"\\cite\{([^}]+)\}", text):
        cited_keys.update(key.strip() for key in citation.split(","))
    bib_keys = set(re.findall(r"^@\w+\{([^,]+),", bib_text, flags=re.MULTILINE))

    required_claims = {f"C2-C{i:02d}" for i in range(1, 10)}
    present_claims = {marker.group("claim") for marker in markers}
    obsolete_numbers = re.findall(r"(?<!\d)(?:4000|800)(?!\d)", text)
    dangerous_patterns = {
        "fever_as_power_grid": r"\bFEVER (?:is|was|provides?) (?:a )?power-grid (?:dataset|corpus|data)",
        "role_gain_positive": r"(?:^|[.!?]\s+)Role conditioning (?:reliably |significantly )?improves?",
        "blanket_bm25_positive": r"(?:^|[.!?]\s+)C2GES (?:broadly|uniformly|consistently) outperforms? BM25",
        "oracle_end_to_end_positive": r"\boracle(?:-label)? (?:is|was) end-to-end\b",
        "nerc_human_gold_positive": r"\bNERC (?:is|was|provides?) (?:a )?human[- ]gold\b",
    }
    dangerous_hits = {
        name: re.findall(pattern, text, flags=re.IGNORECASE | re.MULTILINE)
        for name, pattern in dangerous_patterns.items()
        if re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE)
    }

    required_phrases = [
        "C2GES: Interpretable Extractive Evidence Selection for Power Grid Reliability Reports",
        "document-conditioned evidence-selection corpus—not power-grid data",
        "oracle-label, leakage-controlled predicted-label, and label-blind protocols",
        "five fixed training seeds",
        "BM25 is stronger at \\(K=1\\)",
        "primary role-conditioning claim NO-GO",
        "blanket superiority over BM25 is also NO-GO",
        "agent-verified silver rather than human gold",
        "Verified Citation Claim–Key Map",
    ]
    missing_disclosures = [phrase for phrase in required_phrases if phrase not in text]

    issues = {
        "abstract_missing": not bool(abstract),
        "abstract_over_200_words": abstract_words > 200,
        "prose_without_adjacent_claim_marker": missing_markers,
        "missing_artifact_paths": sorted(set(missing_paths)),
        "missing_claim_ids": sorted(required_claims - present_claims),
        "missing_bibliography_keys": sorted(cited_keys - bib_keys),
        "obsolete_split_numbers": obsolete_numbers,
        "dangerous_positive_claims": dangerous_hits,
        "missing_required_disclosures": missing_disclosures,
    }
    passed = not any(issues.values())
    report = {
        "draft": str(DRAFT.relative_to(ROOT)).replace("\\", "/"),
        "passed": passed,
        "abstract_word_count": abstract_words,
        "english_word_count": len(WORD_RE.findall(text)),
        "prose_paragraph_count": len(prose_indices),
        "claim_marker_count": len(markers),
        "citation_key_count": len(cited_keys),
        "citation_keys": sorted(cited_keys),
        "claims_present": sorted(present_claims),
        "issues": issues,
    }
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
