"""Build a leakage-controlled NERC executive-summary benchmark.

The official executive-summary section is the reference. Candidate sentences
come from the already segmented report JSON after removing the matching prefix.
No LLM or network call is made by this script.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[4]
PDF_ROOT = ROOT / "data/public_datasets/reliability_reports/c2ges_nerc_reports"
PDF_MANIFEST = PDF_ROOT / "metadata/c2ges_nerc_report_manifest.json"
SEGMENTED_ROOT = (
    ROOT
    / "paper_projects/2026_c2ges_engineeringletters/workspace/verification_pilot/agent_audit_40doc"
)

START_RE = re.compile(r"(?im)^\s*executive\s+summary\s*$")
END_RE = re.compile(
    r"(?im)^\s*(?:chapter\s+1\b.*|key\s+contributors|key\s+findings|introduction|background|"
    r"event\s+(?:overview|description)|recommendations?|purpose|scope)\s*$"
)
WORD_RE = re.compile(r"[A-Za-z0-9]+")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def pdf_text(path: Path) -> str:
    cp = subprocess.run(
        ["pdftotext", "-layout", "-enc", "UTF-8", str(path), "-"],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return cp.stdout.replace("\r\n", "\n")


def clean_summary(text: str) -> str:
    lines = []
    for raw in text.replace("\f", "\n").splitlines():
        line = re.sub(r"\s+", " ", raw).strip()
        if not line or line.lower() in {"<public>", "public"}:
            continue
        if re.fullmatch(r"\d+", line):
            continue
        if re.search(r"\bpage\s+\d+\s+of\s+\d+\b", line, re.I):
            continue
        lines.append(line)
    joined = " ".join(lines)
    joined = re.sub(r"\s+", " ", joined).strip()
    return joined


def executive_summary(text: str) -> tuple[str | None, str]:
    start = START_RE.search(text)
    if not start:
        return None, "missing_executive_summary_heading"
    tail = text[start.end() :]
    end = None
    for match in END_RE.finditer(tail):
        if match.start() >= 500:
            end = match.start()
            break
    if end is None:
        return None, "missing_summary_end_heading"
    summary = clean_summary(tail[:end])
    if len(WORD_RE.findall(summary)) < 80:
        return None, "summary_too_short"
    return summary, "included"


def tokens(text: str) -> set[str]:
    return {x.lower() for x in WORD_RE.findall(text) if len(x) > 2}


def containment(sentence: str, summary_tokens: set[str]) -> float:
    st = tokens(sentence)
    return len(st & summary_tokens) / max(1, len(st))


def split_name(doc_id: str) -> str:
    bucket = int(hashlib.sha256(doc_id.encode("utf-8")).hexdigest()[:8], 16) % 10
    return "dev" if bucket < 3 else "test"


def jsonl_write(path: Path, rows: Iterable[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def build(output_dir: Path) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    pdf_manifest = json.loads(PDF_MANIFEST.read_text(encoding="utf-8"))
    rows, audit = [], []
    for item in pdf_manifest:
        doc_id = item["doc_id"]
        pdf = PDF_ROOT / item["local_pdf"]
        segmented = SEGMENTED_ROOT / f"{doc_id}.json"
        if not pdf.exists() or not segmented.exists():
            audit.append({"doc_id": doc_id, "status": "missing_local_input"})
            continue
        reference, status = executive_summary(pdf_text(pdf))
        if reference is None:
            audit.append({"doc_id": doc_id, "status": status, "pdf_sha256": sha256(pdf)})
            continue
        source = json.loads(segmented.read_text(encoding="utf-8"))
        sentences = source["sentences"]
        ref_tokens = tokens(reference)
        prefix_limit = min(40, max(8, len(sentences) // 3))
        matched = [
            idx
            for idx, sent in enumerate(sentences[:prefix_limit])
            if containment(sent["text"], ref_tokens) >= 0.62
            or "executive summary" in sent["text"].lower()
        ]
        cut = max(matched) + 1 if matched else 0
        candidates = sentences[cut:]
        if len(candidates) < 12:
            audit.append({"doc_id": doc_id, "status": "too_few_candidates", "cut": cut})
            continue
        evidence_text = {}
        by_sid = {s["sid"]: s["text"] for s in sentences}
        for question in source["causal_questions"]:
            evidence_text[question["role"]] = [
                {"sid": sid, "text": by_sid[sid]}
                for sid in question.get("evidence_sentence_ids", [])
                if sid in by_sid
            ]
        row = {
            "doc_id": doc_id,
            "title": source["title"],
            "split": split_name(doc_id),
            "source_url": source["source_url"],
            "reference_summary": reference,
            "reference_provenance": "official_NERC_executive_summary",
            "candidate_sentences": candidates,
            "removed_prefix_count": cut,
            "silver_role_evidence": evidence_text,
            "silver_label_provenance": "agent_verified_candidate_not_human_gold",
            "pdf_sha256": sha256(pdf),
            "segmented_json_sha256": sha256(segmented),
        }
        rows.append(row)
        audit.append(
            {
                "doc_id": doc_id,
                "status": "included",
                "split": row["split"],
                "candidate_count": len(candidates),
                "removed_prefix_count": cut,
                "reference_words": len(WORD_RE.findall(reference)),
                "pdf_sha256": row["pdf_sha256"],
            }
        )
    rows.sort(key=lambda x: x["doc_id"])
    audit.sort(key=lambda x: x["doc_id"])
    jsonl = output_dir / "nerc_executive_summary_benchmark.jsonl"
    jsonl_write(jsonl, rows)
    manifest = {
        "protocol": "C2GES-NERC-EXECUTIVE-SUMMARY-v0.1",
        "included": len(rows),
        "dev": sum(r["split"] == "dev" for r in rows),
        "test": sum(r["split"] == "test" for r in rows),
        "excluded": len(audit) - len(rows),
        "dataset_sha256": sha256(jsonl),
        "source_manifest_sha256": sha256(PDF_MANIFEST),
        "segmented_manifest_sha256": sha256(SEGMENTED_ROOT / "manifest.json"),
        "audit": audit,
    }
    (output_dir / "build_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    print(json.dumps(build(args.output), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
