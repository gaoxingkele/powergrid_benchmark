#!/usr/bin/env python3
"""Deterministic cross-split Wikipedia title alias/near-duplicate audit.

This is an explainable title-level screen, not a semantic-duplicate proof.  It
reports exact aliases after conservative normalization, shared base titles
after parenthetical disambiguators are removed, and high-similarity candidates.
Every candidate is retained for review rather than silently reclassified.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA = ROOT / "workspace/fever_benchmark_document_grouped"
DEFAULT_OUT = ROOT / "workspace/fever_benchmark_document_grouped/title_alias_audit"
SPLIT_PAIRS = (("train", "dev"), ("train", "test"), ("dev", "test"))


def normalized_title(title: str) -> str:
    value = unicodedata.normalize("NFKC", unquote(title)).replace("_", " ")
    value = value.casefold().replace("&", " and ")
    value = re.sub(r"[^\w\s()]", " ", value, flags=re.UNICODE)
    return re.sub(r"\s+", " ", value).strip()


def base_title(title: str) -> str:
    value = re.sub(r"\s*\([^()]*\)\s*$", "", normalized_title(title)).strip()
    value = re.sub(r"^the\s+", "", value)
    return value


def char_ngrams(value: str, n: int = 3) -> set[str]:
    padded = f"  {value}  "
    return {padded[index : index + n] for index in range(max(1, len(padded) - n + 1))}


def jaccard(left: set[str], right: set[str]) -> float:
    return len(left & right) / len(left | right) if left or right else 1.0


def load_titles(data: Path) -> dict[str, list[str]]:
    result = {}
    for split in ("train", "dev", "test"):
        values = set()
        for path in sorted((data / split).glob("*.json")):
            doc = json.loads(path.read_text(encoding="utf-8"))
            title = doc.get("wikipedia_title") or doc.get("underlying_document_id") or doc.get("document_id") or doc.get("title")
            if title:
                values.add(str(title))
        result[split] = sorted(values)
    return result


def audit_pairs(titles: dict[str, list[str]], similarity_threshold: float, ngram_threshold: float) -> list[dict]:
    prepared = {
        split: [
            {
                "title": title,
                "normalized": normalized_title(title),
                "base": base_title(title),
                "ngrams": char_ngrams(normalized_title(title)),
            }
            for title in values
        ]
        for split, values in titles.items()
    }
    candidates = []
    for left_split, right_split in SPLIT_PAIRS:
        for left in prepared[left_split]:
            for right in prepared[right_split]:
                reasons = []
                if left["normalized"] == right["normalized"]:
                    reasons.append("exact_normalized_alias")
                if left["base"] and left["base"] == right["base"] and left["normalized"] != right["normalized"]:
                    reasons.append("shared_base_after_disambiguator_removal")
                # An inexpensive deterministic block avoids treating unrelated
                # short titles as near duplicates.
                jac = jaccard(left["ngrams"], right["ngrams"])
                seq = 0.0
                if jac >= ngram_threshold:
                    seq = SequenceMatcher(None, left["normalized"], right["normalized"], autojunk=False).ratio()
                    if seq >= similarity_threshold and left["normalized"] != right["normalized"]:
                        reasons.append("high_title_string_similarity")
                if reasons:
                    candidates.append(
                        {
                            "left_split": left_split,
                            "left_title": left["title"],
                            "left_normalized": left["normalized"],
                            "right_split": right_split,
                            "right_title": right["title"],
                            "right_normalized": right["normalized"],
                            "sequence_similarity": round(seq, 6),
                            "trigram_jaccard": round(jac, 6),
                            "reasons": reasons,
                            "review_status": "unreviewed_candidate",
                        }
                    )
    return sorted(candidates, key=lambda row: (row["left_split"], row["right_split"], row["left_title"], row["right_title"]))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--similarity-threshold", type=float, default=0.92)
    parser.add_argument("--ngram-threshold", type=float, default=0.72)
    parser.add_argument("--review-decisions", type=Path, help="Optional JSON list of manually evidenced candidate decisions.")
    args = parser.parse_args()
    if not 0 < args.similarity_threshold <= 1 or not 0 < args.ngram_threshold <= 1:
        parser.error("thresholds must be in (0, 1]")
    if args.out.exists() and any(args.out.iterdir()):
        parser.error(f"refusing to overwrite non-empty output directory: {args.out}")
    args.out.mkdir(parents=True, exist_ok=True)

    titles = load_titles(args.data)
    candidates = audit_pairs(titles, args.similarity_threshold, args.ngram_threshold)
    if args.review_decisions:
        decisions = json.loads(args.review_decisions.read_text(encoding="utf-8"))
        decision_map = {
            (item["left_split"], item["left_title"], item["right_split"], item["right_title"]): item
            for item in decisions
        }
        for candidate in candidates:
            key = (candidate["left_split"], candidate["left_title"], candidate["right_split"], candidate["right_title"])
            if key in decision_map:
                decision = decision_map[key]
                candidate["review_status"] = decision["review_status"]
                candidate["review_rationale"] = decision.get("review_rationale", "")
                candidate["review_evidence"] = decision.get("review_evidence", [])
    hard = [row for row in candidates if "exact_normalized_alias" in row["reasons"]]
    review = [row for row in candidates if "exact_normalized_alias" not in row["reasons"]]
    unreviewed = [row for row in review if row["review_status"] == "unreviewed_candidate"]
    confirmed = [row for row in review if row["review_status"] == "confirmed_alias"]
    distinct = [row for row in review if row["review_status"] == "reviewed_distinct_entities"]
    summary = {
        "method_scope": "Wikipedia title strings only; does not prove absence of semantic, redirect, content, or entity aliases",
        "normalization": "URL decode + Unicode NFKC + casefold + underscore/space and punctuation normalization",
        "base_alias_rule": "remove one trailing parenthetical disambiguator and leading 'the'",
        "near_duplicate_rule": {
            "sequence_matcher_threshold": args.similarity_threshold,
            "character_trigram_jaccard_prefilter": args.ngram_threshold,
        },
        "unique_titles": {split: len(values) for split, values in titles.items()},
        "cross_split_pairs_examined": sum(len(titles[left]) * len(titles[right]) for left, right in SPLIT_PAIRS),
        "hard_exact_alias_count": len(hard),
        "review_candidate_count": len(review),
        "unreviewed_candidate_count": len(unreviewed),
        "confirmed_alias_count": len(confirmed),
        "reviewed_distinct_entity_count": len(distinct),
        "automatic_exact_alias_gate_passed": not hard,
        "canonical_freeze_ready": not hard and not confirmed and not unreviewed,
        "caveat": "A passing automatic gate must not be described as complete semantic deduplication.",
        "candidates": candidates,
    }
    json_path = args.out / "title_alias_audit.json"
    json_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    fields = [
        "left_split", "left_title", "left_normalized", "right_split", "right_title", "right_normalized",
        "sequence_similarity", "trigram_jaccard", "reasons", "review_status", "review_rationale", "review_evidence",
    ]
    with (args.out / "title_alias_candidates.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in candidates:
            writer.writerow({
                **row,
                "reasons": ";".join(row["reasons"]),
                "review_evidence": json.dumps(row.get("review_evidence", []), ensure_ascii=False),
            })
    summary["audit_json_sha256"] = hashlib.sha256(json_path.read_bytes()).hexdigest()
    (args.out / "summary.json").write_text(json.dumps({key: value for key, value in summary.items() if key != "candidates"}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({key: value for key, value in summary.items() if key != "candidates"}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
