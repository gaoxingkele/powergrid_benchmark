#!/usr/bin/env python3
"""Download FEVER evidence-selection data and convert to C2GES sentence-ID schema.

Uses the filtered FEVER evidence-selection release (human gold evidence lines):
  lukasellinger/filtered_fever-evidence_selection

Output layout (one JSON per claim/document instance):
  paper_projects/2026_c2ges_engineeringletters/workspace/fever_benchmark/{split}/*.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]  # .../2026_c2ges_engineeringletters
DEFAULT_OUT = ROOT / "workspace/fever_benchmark"


def parse_lines(lines_field: str) -> list[dict]:
    sentences = []
    for raw in (lines_field or "").split("\n"):
        raw = raw.strip("\r")
        if not raw:
            continue
        if "\t" not in raw:
            continue
        sid_str, text = raw.split("\t", 1)
        text = text.strip()
        if not text:
            continue
        try:
            sid_int = int(sid_str)
        except ValueError:
            continue
        sentences.append({"sid": f"s{sid_int:03d}", "text": text, "wiki_line_id": sid_int})
    return sentences


def parse_evidence_lines(ev_field: str) -> list[int]:
    if ev_field is None:
        return []
    if isinstance(ev_field, list):
        out = []
        for x in ev_field:
            try:
                out.append(int(x))
            except (TypeError, ValueError):
                continue
        return sorted(set(out))
    s = str(ev_field).strip()
    if not s:
        return []
    parts = re.split(r"[\s,;]+", s)
    out = []
    for p in parts:
        if not p:
            continue
        try:
            out.append(int(p))
        except ValueError:
            continue
    return sorted(set(out))


def role_from_label(label: str) -> str:
    lab = (label or "").upper().replace(" ", "_")
    if lab.startswith("SUPPORT"):
        return "supports"
    if lab.startswith("REFUTE"):
        return "refutes"
    return "other"


def canonical_document_id(value: object) -> str:
    """Return the untouched FEVER Wikipedia title used as the grouping key."""
    return str(value or "").strip()


def convert_row(row: dict, split: str, *, source_split: str | None = None) -> dict | None:
    sentences = parse_lines(row.get("lines") or "")
    if len(sentences) < 2:
        return None
    gold_ids = parse_evidence_lines(row.get("evidence_lines") or "")
    if not gold_ids:
        return None
    sid_by_wiki = {s["wiki_line_id"]: s["sid"] for s in sentences}
    evidence = [sid_by_wiki[i] for i in gold_ids if i in sid_by_wiki]
    if not evidence:
        return None
    role = role_from_label(row.get("label") or "")
    if role == "other":
        return None
    claim_id = int(row.get("id") or 0)
    wikipedia_title = canonical_document_id(row.get("document_id"))
    if not wikipedia_title:
        return None
    doc_key = re.sub(r"[^A-Za-z0-9._-]+", "_", wikipedia_title)[:80]
    doc_id = f"fever_{split}_{claim_id}_{doc_key}"
    claim = (row.get("claim") or "").strip()
    if not claim:
        return None
    q = {
        "qid": f"{doc_id}::{role}",
        "role": role,
        "question": claim,
        "answer": "",
        "evidence_sentence_ids": evidence,
        "verification_status": "fever_human_gold",
        "source_annotation": "fever_filtered_evidence_selection",
        "label": row.get("label"),
        "notes": "Human-annotated FEVER evidence sentence IDs.",
    }
    return {
        "doc_id": doc_id,
        # Keep both names: doc_id is a claim/document *instance*, whereas the
        # fields below identify the shared underlying Wikipedia document.
        "document_id": wikipedia_title,
        "underlying_document_id": wikipedia_title,
        "wikipedia_title": wikipedia_title,
        "title": wikipedia_title,
        "source_url": "https://fever.ai/dataset/fever.html",
        "source_page": "https://huggingface.co/datasets/lukasellinger/filtered_fever-evidence_selection",
        "dataset": "fever_evidence_selection",
        "split": split,
        "source_split": source_split or split,
        "sentences": [{"sid": s["sid"], "text": s["text"]} for s in sentences],
        "causal_questions": [q],
    }


def write_split(rows, out_dir: Path, split: str, limit: int | None) -> int:
    out_dir.mkdir(parents=True, exist_ok=True)
    n = 0
    for row in rows:
        obj = convert_row(row, split, source_split=split)
        if obj is None:
            continue
        path = out_dir / f"{obj['doc_id']}.json"
        path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")
        n += 1
        if limit is not None and n >= limit:
            break
    return n


def assigned_split(document_id: str, train_fraction: float, dev_fraction: float) -> str:
    """Assign all claims from a Wikipedia document to one deterministic split."""
    digest = hashlib.sha256(document_id.encode("utf-8")).digest()
    value = int.from_bytes(digest[:8], "big") / float(2**64)
    if value < train_fraction:
        return "train"
    if value < train_fraction + dev_fraction:
        return "dev"
    return "test"


def write_document_grouped(ds, out: Path, limits: dict[str, int | None], train_fraction: float, dev_fraction: float) -> dict[str, int]:
    """Pool source splits, then write complete Wikipedia-document groups.

    Limits are enforced at the document boundary.  A page is therefore either
    included with all of its converted claims or omitted entirely; a limit can
    leave a split slightly under target, but never creates a partial document.
    """
    counts = {split: 0 for split in ("train", "dev", "test")}
    seen_instances: set[tuple[int, str]] = set()
    grouped: dict[str, dict[str, list[dict]]] = {
        split: defaultdict(list) for split in ("train", "dev", "test")
    }
    for source_split in ("train", "dev", "test"):
        for row in ds[source_split]:
            document_id = canonical_document_id(row.get("document_id"))
            if not document_id:
                continue
            target_split = assigned_split(document_id, train_fraction, dev_fraction)
            instance_key = (int(row.get("id") or 0), document_id)
            if instance_key in seen_instances:
                continue
            obj = convert_row(row, target_split, source_split=source_split)
            if obj is None:
                continue
            seen_instances.add(instance_key)
            grouped[target_split][document_id].append(obj)

    for target_split in ("train", "dev", "test"):
        split_dir = out / target_split
        split_dir.mkdir(parents=True, exist_ok=True)
        limit = limits[target_split]
        for document_id in sorted(grouped[target_split]):
            objects = sorted(grouped[target_split][document_id], key=lambda obj: obj["doc_id"])
            if limit is not None and counts[target_split] + len(objects) > limit:
                continue
            split_dir = out / target_split
            for obj in objects:
                (split_dir / f"{obj['doc_id']}.json").write_text(
                    json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8"
                )
            counts[target_split] += len(objects)
    return counts


def leakage_audit(out: Path) -> dict:
    split_docs: dict[str, set[str]] = defaultdict(set)
    split_instances: dict[str, int] = defaultdict(int)
    for split in ("train", "dev", "test"):
        for path in sorted((out / split).glob("*.json")):
            obj = json.loads(path.read_text(encoding="utf-8"))
            document_id = obj.get("underlying_document_id") or obj.get("document_id") or obj.get("wikipedia_title") or obj.get("title")
            if document_id:
                split_docs[split].add(str(document_id))
            split_instances[split] += 1
    pairs = {}
    all_overlap: set[str] = set()
    for left, right in (("train", "dev"), ("train", "test"), ("dev", "test")):
        overlap = sorted(split_docs[left] & split_docs[right])
        pairs[f"{left}_vs_{right}"] = {"count": len(overlap), "document_ids": overlap}
        all_overlap.update(overlap)
    return {
        "grouping_key": "underlying_document_id (original FEVER Wikipedia document_id/title)",
        "instances": dict(split_instances),
        "unique_documents": {split: len(split_docs[split]) for split in ("train", "dev", "test")},
        "pairwise_overlap": pairs,
        "overlap_document_count": len(all_overlap),
        "passed": not all_overlap,
    }


def content_hashes(out: Path) -> dict:
    """Hash every generated instance without making the manifest enormous."""
    result = {}
    corpus_digest = hashlib.sha256()
    for split in ("train", "dev", "test"):
        split_digest = hashlib.sha256()
        files = sorted((out / split).glob("*.json"), key=lambda path: path.name)
        for path in files:
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            split_digest.update(path.name.encode("utf-8"))
            split_digest.update(digest.encode("ascii"))
        split_hash = split_digest.hexdigest()
        result[split] = {"sha256": split_hash, "file_count": len(files)}
        corpus_digest.update(split.encode("ascii"))
        corpus_digest.update(split_hash.encode("ascii"))
    result["corpus_sha256"] = corpus_digest.hexdigest()
    return result


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--train-limit", type=int, default=10000)
    ap.add_argument("--dev-limit", type=int, default=2000)
    ap.add_argument("--test-limit", type=int, default=1685)
    ap.add_argument(
        "--split-strategy",
        choices=("document_grouped", "source"),
        default="document_grouped",
        help="document_grouped prevents the same Wikipedia page appearing across splits; source preserves the upstream split for legacy reproduction.",
    )
    ap.add_argument("--train-fraction", type=float, default=0.8)
    ap.add_argument("--dev-fraction", type=float, default=0.1)
    ap.add_argument(
        "--clean-output",
        action="store_true",
        help="Explicitly remove prior generated JSON files before rebuilding; prevents stale instances from contaminating a new split.",
    )
    args = ap.parse_args()

    existing = [path for split in ("train", "dev", "test") for path in (args.out / split).glob("*.json")]
    if existing and not args.clean_output:
        ap.error(
            f"output already contains {len(existing)} generated instances; use a fresh --out path or explicitly pass --clean-output"
        )
    if args.clean_output:
        # Delete only the generator-owned files at known depths, never recurse.
        for path in existing:
            path.unlink()
        for name in ("manifest.json", "leakage_audit.json"):
            path = args.out / name
            if path.exists():
                path.unlink()

    from datasets import load_dataset

    ds = load_dataset("lukasellinger/filtered_fever-evidence_selection")
    if not (0 < args.train_fraction < 1 and 0 < args.dev_fraction < 1 and args.train_fraction + args.dev_fraction < 1):
        ap.error("train/dev fractions must be positive and sum to less than one")
    limits = {"train": args.train_limit, "dev": args.dev_limit, "test": args.test_limit}
    if args.split_strategy == "document_grouped":
        counts = write_document_grouped(ds, args.out, limits, args.train_fraction, args.dev_fraction)
    else:
        counts = {
            split: write_split(ds[split], args.out / split, split, limits[split])
            for split in ("train", "dev", "test")
        }
    audit = leakage_audit(args.out)
    meta = {
        "source": "lukasellinger/filtered_fever-evidence_selection",
        "counts": counts,
        "split_strategy": args.split_strategy,
        "split_grouping_key": "underlying_document_id",
        "leakage_audit": audit,
        "content_hashes": content_hashes(args.out),
        "roles": ["supports", "refutes"],
        "notes": "Human-gold FEVER evidence sentence selection converted to C2GES schema.",
    }
    (args.out / "manifest.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    (args.out / "leakage_audit.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(meta, indent=2))


if __name__ == "__main__":
    main()
