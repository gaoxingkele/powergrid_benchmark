"""Audit manuscript/evidence overlap for the two Mintou companion-paper pairs."""

from __future__ import annotations

import csv
import hashlib
import json
import re
from difflib import SequenceMatcher
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "reviews" / "mintou_2026-08-09_journal_fit_audit"
PAIRS = [
    ("mintou_p3_samode_distribution_planning", "mintou_p4_shield_resilience_planning"),
    ("mintou_p5_trace_moea_feasibility_review", "mintou_p6_bilonsga_project_review"),
]


def sentences(text: str) -> list[str]:
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    candidates = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])|\n+", text)
    return [re.sub(r"\s+", " ", s).strip() for s in candidates if len(s.split()) >= 10]


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def relevant_files(project: str) -> dict[str, list[Path]]:
    roots = [ROOT / "papers" / "mintou" / project, ROOT / "paper_projects" / project]
    out = {"figures": [], "tables": []}
    for base in roots:
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file():
                continue
            suffix = path.suffix.lower()
            if suffix in {".png", ".jpg", ".jpeg", ".svg", ".pdf"}:
                out["figures"].append(path)
            elif suffix in {".csv", ".json"} and any(
                token in path.name.lower()
                for token in ("result", "leaderboard", "significance", "summary", "backtest", "validation")
            ):
                out["tables"].append(path)
    return out


def hash_overlap(left: list[Path], right: list[Path]) -> list[dict[str, str]]:
    by_hash: dict[str, list[Path]] = {}
    for path in right:
        by_hash.setdefault(digest(path), []).append(path)
    rows = []
    for path in left:
        value = digest(path)
        for other in by_hash.get(value, []):
            rows.append(
                {
                    "left": str(path.relative_to(ROOT)),
                    "right": str(other.relative_to(ROOT)),
                    "sha256": value,
                }
            )
    return rows


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    summary = {}
    sentence_rows = []
    for left, right in PAIRS:
        left_path = ROOT / "paper_projects" / left / "manuscript" / "MANUSCRIPT.md"
        right_path = ROOT / "paper_projects" / right / "manuscript" / "MANUSCRIPT.md"
        ls = sentences(left_path.read_text(encoding="utf-8"))
        rs = sentences(right_path.read_text(encoding="utf-8"))
        right_norm = {norm(s): s for s in rs}
        exact = [(s, right_norm[norm(s)]) for s in ls if norm(s) in right_norm]

        near = []
        for a in ls:
            na = norm(a)
            for b in rs:
                nb = norm(b)
                if abs(len(na) - len(nb)) > max(len(na), len(nb)) * 0.25:
                    continue
                ratio = SequenceMatcher(None, na, nb, autojunk=False).ratio()
                if ratio >= 0.88 and na != nb:
                    near.append((ratio, a, b))
        near.sort(reverse=True)

        lf, rf = relevant_files(left), relevant_files(right)
        figure_overlap = hash_overlap(lf["figures"], rf["figures"])
        table_overlap = hash_overlap(lf["tables"], rf["tables"])
        pair_key = f"{left}__{right}"
        summary[pair_key] = {
            "left_sentences": len(ls),
            "right_sentences": len(rs),
            "exact_sentence_overlap": len(exact),
            "near_sentence_overlap_ge_0_88": len(near),
            "identical_figure_files": figure_overlap,
            "identical_result_table_files": table_overlap,
        }
        for kind, records in (("exact", [(1.0, a, b) for a, b in exact]), ("near", near)):
            for ratio, a, b in records:
                sentence_rows.append(
                    {"pair": pair_key, "kind": kind, "similarity": f"{ratio:.4f}", "left": a, "right": b}
                )

    (OUT / "companion_independence_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    with (OUT / "companion_sentence_overlap.csv").open("w", newline="", encoding="utf-8-sig") as fh:
        writer = csv.DictWriter(fh, fieldnames=["pair", "kind", "similarity", "left", "right"])
        writer.writeheader()
        writer.writerows(sentence_rows)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
