"""G1b: budget-efficiency curve on the frozen external corpus.

The v3 arm run showed that the role layer looks positive under an equal-unit
budget and negative under an equal-word budget.  The mechanism claim is that the
equal-unit protocol hands the role-conditioned arms *more text* (they pick fewer,
longer units), so the curve below recomputes every arm at five word budgets and
four unit budgets and reports both ROUGE-L and the realised words-per-unit.

That turns "the gain is a length artefact" from an interpretation into a
measurable property of the same frozen corpus.  No tuning, no new documents.

Usage:
    python -B run_external_arms_curve_v4.py --json external_arms_curve_v4.json
"""

from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path

HERE = Path(__file__).resolve().parent

import run_external_arms_v3 as A3  # noqa: E402

WORD_BUDGETS = (110, 180, 260, 400, 600)
UNIT_BUDGETS = (3, 5, 10, 15)
ARMS = ("AB0", "AB1", "AB2", "no_path", "Full", "TextRank", "Lead")


def markdown_dir(explicit: Path | None = None) -> Path:
    """Locate the converted Markdown corpus.

    The third-party Markdown conversions are deliberately outside the release
    scope, so a released copy of this script must be pointed at them (or at the
    working copy) before it can run.  The default keeps the historical layout.
    """
    candidates = []
    if explicit:
        candidates.append(explicit)
    candidates.append(HERE / "markdown")
    for parent in HERE.parents:
        candidates.append(parent / "05_External_Prospective_20260922" / "markdown")
    for candidate in candidates:
        if candidate.is_dir() and any(candidate.glob("*.md")):
            return candidate
    raise SystemExit(
        "no Markdown corpus found; pass the directory that holds the converted "
        "third-party reports as the first positional argument"
    )


def build_corpus(corpus_dir: Path):
    """Same frozen corpus construction as v3 (identical ordering and dedup)."""
    built = []
    for md in sorted(corpus_dir.glob("*.md")):
        row = A3.V2.build_report(md)
        if row:
            built.append(row)
    built.sort(key=lambda r: (-len(r["candidate_sentences"]), -len(r["reference_summary"].split()), r["doc_id"]))
    reports = []
    for row in built:
        if any(A3.V2.is_same_incident(row["doc_id"], kept["doc_id"]) for kept in reports):
            continue
        reports.append(row)
    return reports


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", required=True)
    parser.add_argument("--corpus-dir", type=Path, default=None, help="directory holding the converted Markdown reports")
    args = parser.parse_args()

    settings = A3.R.load_protocol()["textrank"]
    corpus = markdown_dir(args.corpus_dir)
    print(f"corpus: {corpus}", flush=True)
    reports = build_corpus(corpus)
    rows = []
    for index, row in enumerate(reports, start=1):
        prepared = A3.R.prepare_report(row)
        for kind, budgets in (("word", WORD_BUDGETS), ("unit", UNIT_BUDGETS)):
            for budget in budgets:
                for condition in ARMS:
                    result = A3.run_condition(prepared, condition, kind, budget, settings)
                    rows.append(
                        {
                            "doc_id": row["doc_id"],
                            "family": row["report_series_id"],
                            "condition": condition,
                            "kind": kind,
                            "budget": budget,
                            "key": f"{kind}:{budget}",
                            "rougeL_f1": result["rougeL_f1"],
                            "units": result["units"],
                            "words": result["words"],
                        }
                    )
        print(f"[{index}/{len(reports)}] {row['doc_id'][:60]}", flush=True)

    curve = {}
    for row in rows:
        curve.setdefault(row["key"], {}).setdefault(row["condition"], []).append(row)
    summary = {}
    for key, arms in curve.items():
        summary[key] = {}
        for condition, items in arms.items():
            summary[key][condition] = {
                "n": len(items),
                "mean_rougeL": round(statistics.fmean(r["rougeL_f1"] for r in items), 5),
                "mean_units": round(statistics.fmean(r["units"] for r in items), 2),
                "mean_words": round(statistics.fmean(r["words"] for r in items), 1),
                "words_per_unit": round(
                    statistics.fmean(r["words"] for r in items) / max(1e-9, statistics.fmean(r["units"] for r in items)),
                    1,
                ),
            }

    contrasts = []
    for kind, budgets in (("word", WORD_BUDGETS), ("unit", UNIT_BUDGETS)):
        for budget in budgets:
            key = f"{kind}:{budget}"
            for cand in ("AB2", "AB1", "Full", "TextRank", "Lead"):
                ref = "AB0" if cand in ("AB2", "AB1") else "no_path"
                item = A3.contrast(rows, ref, cand, key)
                if item:
                    contrasts.append(item)

    payload = {
        "schema": "c2ges-external-arms-curve-v4",
        "corpus": "same frozen external corpus, same dedup and ordering as external_arms_v3",
        "documents": len(reports),
        "families": sorted({r["report_series_id"] for r in reports}),
        "word_budgets": list(WORD_BUDGETS),
        "unit_budgets": list(UNIT_BUDGETS),
        "arms": list(ARMS),
        "summary": summary,
        "contrasts": contrasts,
        "rows": rows,
    }
    Path(args.json).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {args.json} with {len(rows)} rows over {len(reports)} documents")
    for key in [f"word:{b}" for b in WORD_BUDGETS] + [f"unit:{b}" for b in UNIT_BUDGETS]:
        arms = summary.get(key, {})
        line = ", ".join(
            f"{name}={arms[name]['mean_rougeL']:.4f} ({arms[name]['words_per_unit']}w/u)"
            for name in ("AB0", "AB2", "no_path", "Full", "TextRank", "Lead")
            if name in arms
        )
        print(f"  {key:9s} {line}")


if __name__ == "__main__":
    main()
